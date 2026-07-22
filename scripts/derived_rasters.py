"""
Derived raster products from a LAZ/LAS point cloud: canopy height model
(CHM) for now, with reusable grid/raster helpers meant to be shared by
other derived layers (density, slope) later.

A CHM highlights vegetation height near a route — the single highest-value
derived product for transmission clearance risk, since existing LiDAR plus
known growth rates can flag likely clearance violations even on ground
that's already "covered."

Output per file: a color-mapped PNG (transparent where there's no ground
point to compute height above, so we never fabricate a value) plus a JSON
sidecar with the image's WGS84 bounds and legend stops, ready for a Leaflet
L.imageOverlay.

Usage:
    python derived_rasters.py chm file.laz --out-dir ../laz-viewer/data/chm
"""

import argparse
import json
from pathlib import Path

import laspy
import numpy as np
import pyproj
from PIL import Image

import laz_to_coverage as lc

GROUND_CLASS = 2
TARGET_GRID_CELLS_ACROSS = 400


def vertical_unit_to_meters(header):
    """Height values (Z) can be in a different unit than X/Y in a compound
    CRS (e.g. a vertical datum defined in US survey feet). Falls back to
    the horizontal unit if there's no separate vertical component."""
    crs = header.parse_crs()
    if crs is not None and crs.is_compound:
        for sub in crs.sub_crs_list:
            if sub.is_vertical:
                return sub.axis_info[0].unit_conversion_factor
    return lc.unit_to_meters(lc.horizontal_crs(header))

# (height_m, RGBA) stops; height below the first stop or above the last
# clamps to that stop's color. Interpolated linearly in between.
CHM_COLOR_STOPS = [
    (0.0, (0, 0, 0, 0)),        # bare ground / no vegetation: transparent
    (0.5, (200, 230, 180, 140)),  # low grass/shrub
    (2.0, (120, 200, 120, 170)),  # shrub/small trees
    (5.0, (255, 235, 80, 190)),   # medium trees
    (10.0, (255, 150, 40, 210)),  # tall trees
    (20.0, (230, 40, 40, 230)),   # very tall — review clearance
]


def grid_extent(x, y, target_cells_across=TARGET_GRID_CELLS_ACROSS):
    xmin, xmax = x.min(), x.max()
    ymin, ymax = y.min(), y.max()
    span = max(xmax - xmin, ymax - ymin)
    cell_size = span / target_cells_across
    nx = int(np.ceil((xmax - xmin) / cell_size)) + 1
    ny = int(np.ceil((ymax - ymin) / cell_size)) + 1
    return xmin, ymin, cell_size, nx, ny


def grid_index(values, coord, origin, cell_size, n):
    idx = np.floor((coord - origin) / cell_size).astype(int)
    return np.clip(idx, 0, n - 1)


def compute_chm(las_path):
    with laspy.open(las_path) as f:
        header = f.header
        crs = lc.horizontal_crs(header)
        las = f.read()

    keep = ~np.isin(las.classification, list(lc.NOISE_CLASSES))
    x = np.asarray(las.x)[keep]
    y = np.asarray(las.y)[keep]
    z = np.asarray(las.z)[keep]
    classification = np.asarray(las.classification)[keep]

    xmin, ymin, cell_size, nx, ny = grid_extent(x, y)
    ix = grid_index(x, x, xmin, cell_size, nx)
    iy = grid_index(y, y, ymin, cell_size, ny)

    flat_idx = iy * nx + ix

    # highest point per cell (any non-noise class) = reflective surface top
    dsm_flat = np.full(nx * ny, -np.inf)
    np.maximum.at(dsm_flat, flat_idx, z)
    dsm_flat[np.isneginf(dsm_flat)] = np.nan
    dsm = dsm_flat.reshape(ny, nx)

    # lowest ground-classified point per cell = bare earth (via negated max)
    dem_flat = np.full(nx * ny, np.nan)
    ground_mask = classification == GROUND_CLASS
    if ground_mask.any():
        neg_min = np.full(nx * ny, -np.inf)
        np.maximum.at(neg_min, flat_idx[ground_mask], -z[ground_mask])
        has_ground = np.isfinite(neg_min)
        dem_flat[has_ground] = -neg_min[has_ground]
    dem = dem_flat.reshape(ny, nx)

    chm = dsm - dem  # NaN propagates where either is missing; still in native (x/y) linear units
    chm = chm * vertical_unit_to_meters(header)  # convert height to meters for the color stops/stats
    chm = np.where(chm < 0, 0, chm)  # noise can make DSM briefly dip below DEM in a cell

    return {
        "chm": chm,
        "bounds_wgs84": grid_corners_wgs84(xmin, ymin, cell_size, nx, ny, crs),
        "cell_size_m": cell_size * lc.unit_to_meters(crs),
        "name": Path(las_path).stem,
    }


QUALITY_COLOR_STOPS = [
    (0.0, (220, 40, 40, 200)),    # low quality: edge-of-swath, high scan angle
    (0.5, (255, 210, 60, 190)),
    (0.8, (140, 210, 100, 170)),
    (1.0, (60, 180, 90, 150)),    # high quality: near-nadir
]

MAX_REFERENCE_SCAN_ANGLE_DEG = 30.0  # typical aerial LiDAR swath half-angle


def color_for_value(v, stops):
    if np.isnan(v):
        return (0, 0, 0, 0)
    if v <= stops[0][0]:
        return stops[0][1]
    if v >= stops[-1][0]:
        return stops[-1][1]
    for (v0, c0), (v1, c1) in zip(stops, stops[1:]):
        if v0 <= v <= v1:
            t = (v - v0) / (v1 - v0)
            return tuple(int(c0[i] + t * (c1[i] - c0[i])) for i in range(4))
    return (0, 0, 0, 0)


def render_grid_png(grid, stops, out_path):
    ny, nx = grid.shape
    flat = grid.ravel()

    out = np.zeros((ny * nx, 4), dtype=np.uint8)
    # precompute color for each distinct value rather than calling color_for_value per-pixel
    for v in np.unique(flat[~np.isnan(flat)]):
        out[flat == v] = color_for_value(v, stops)
    rgba = out.reshape(ny, nx, 4)

    # row 0 of our grid is the southernmost row, but image row 0 is the top (north)
    rgba = np.flipud(rgba)
    Image.fromarray(rgba, mode="RGBA").save(out_path)


def grid_corners_wgs84(xmin, ymin, cell_size, nx, ny, crs):
    to_wgs84 = pyproj.Transformer.from_crs(crs, "EPSG:4326", always_xy=True).transform
    xmax, ymax = xmin + nx * cell_size, ymin + ny * cell_size
    lons, lats = to_wgs84([xmin, xmax, xmin, xmax], [ymin, ymin, ymax, ymax])
    return {"south": min(lats), "north": max(lats), "west": min(lons), "east": max(lons)}


def compute_quality(las_path):
    """Per-cell mean |scan angle| turned into a 0-1 quality score — points
    captured near-nadir (scan angle near 0) are geometrically more accurate
    than edge-of-swath points, so "covered" isn't binary; this flags where
    coverage exists but is lower-confidence."""
    with laspy.open(las_path) as f:
        header = f.header
        crs = lc.horizontal_crs(header)
        las = f.read()

    keep = ~np.isin(las.classification, list(lc.NOISE_CLASSES))
    x = np.asarray(las.x)[keep]
    y = np.asarray(las.y)[keep]
    # LAS 1.4 extended scan angle is stored in units of 0.006 degrees
    scan_angle_deg = np.abs(np.asarray(las.scan_angle)[keep].astype(np.float64) * 0.006)

    xmin, ymin, cell_size, nx, ny = grid_extent(x, y)
    ix = grid_index(x, x, xmin, cell_size, nx)
    iy = grid_index(y, y, ymin, cell_size, ny)
    flat_idx = iy * nx + ix

    sums = np.zeros(nx * ny)
    counts = np.zeros(nx * ny)
    np.add.at(sums, flat_idx, scan_angle_deg)
    np.add.at(counts, flat_idx, 1)

    mean_angle = np.full(nx * ny, np.nan)
    has_data = counts > 0
    mean_angle[has_data] = sums[has_data] / counts[has_data]
    quality = 1.0 - np.clip(mean_angle / MAX_REFERENCE_SCAN_ANGLE_DEG, 0, 1)

    return {
        "quality": quality.reshape(ny, nx),
        "bounds_wgs84": grid_corners_wgs84(xmin, ymin, cell_size, nx, ny, crs),
        "cell_size_m": cell_size * lc.unit_to_meters(crs),
        "name": Path(las_path).stem,
    }


SLOPE_COLOR_STOPS = [
    (0.0, (60, 180, 90, 150)),    # flat
    (5.0, (255, 210, 60, 170)),
    (15.0, (255, 140, 40, 190)),
    (30.0, (220, 40, 40, 210)),   # steep — engineering review for tower siting
]


def compute_slope(las_path):
    """Terrain slope in degrees from the ground-point DEM — affects flight
    altitude planning and tower-siting engineering risk."""
    with laspy.open(las_path) as f:
        header = f.header
        crs = lc.horizontal_crs(header)
        las = f.read()

    classification = np.asarray(las.classification)
    ground_mask = classification == GROUND_CLASS
    x = np.asarray(las.x)[ground_mask]
    y = np.asarray(las.y)[ground_mask]
    z = np.asarray(las.z)[ground_mask]
    if x.size == 0:
        raise ValueError(f"{las_path}: no ground-classified points to build a DEM from")

    xmin, ymin, cell_size, nx, ny = grid_extent(x, y)
    ix = grid_index(x, x, xmin, cell_size, nx)
    iy = grid_index(y, y, ymin, cell_size, ny)
    flat_idx = iy * nx + ix

    neg_min = np.full(nx * ny, -np.inf)
    np.maximum.at(neg_min, flat_idx, -z)
    dem_flat = np.full(nx * ny, np.nan)
    has_ground = np.isfinite(neg_min)
    dem_flat[has_ground] = -neg_min[has_ground]
    dem = dem_flat.reshape(ny, nx) * vertical_unit_to_meters(header)

    cell_size_m = cell_size * lc.unit_to_meters(crs)
    dzdy, dzdx = np.gradient(dem, cell_size_m)
    slope_deg = np.degrees(np.arctan(np.sqrt(dzdx**2 + dzdy**2)))

    return {
        "slope": slope_deg,
        "bounds_wgs84": grid_corners_wgs84(xmin, ymin, cell_size, nx, ny, crs),
        "cell_size_m": cell_size_m,
        "name": Path(las_path).stem,
    }


def build_raster(las_path, out_dir, kind):
    if kind == "chm":
        result = compute_chm(las_path)
        grid, stops, value_key = result["chm"], CHM_COLOR_STOPS, "height_m"
        stat_prefix = "height_m"
    elif kind == "quality":
        result = compute_quality(las_path)
        grid, stops, value_key = result["quality"], QUALITY_COLOR_STOPS, "quality"
        stat_prefix = "quality"
    elif kind == "slope":
        result = compute_slope(las_path)
        grid, stops, value_key = result["slope"], SLOPE_COLOR_STOPS, "slope_deg"
        stat_prefix = "slope_deg"
    else:
        raise ValueError(f"unknown raster kind: {kind}")

    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    png_path = out_dir / f"{result['name']}_{kind}.png"
    render_grid_png(grid, stops, png_path)

    valid = grid[~np.isnan(grid)]
    meta = {
        "name": result["name"],
        "image": png_path.name,
        "bounds_wgs84": result["bounds_wgs84"],
        "cell_size_m": round(result["cell_size_m"], 2),
        "legend": [{value_key: v, "color": f"rgba({c[0]},{c[1]},{c[2]},{c[3]/255:.2f})"} for v, c in stops],
        f"max_{stat_prefix}": round(float(valid.max()), 2) if valid.size else None,
        f"mean_{stat_prefix}": round(float(valid.mean()), 2) if valid.size else None,
    }
    json_path = out_dir / f"{result['name']}_{kind}.json"
    with open(json_path, "w") as f:
        json.dump(meta, f, indent=2)

    update_manifest(out_dir, meta)
    return meta


def build_chm(las_path, out_dir):
    return build_raster(las_path, out_dir, "chm")


def build_quality(las_path, out_dir):
    return build_raster(las_path, out_dir, "quality")


def update_manifest(out_dir, meta):
    manifest_path = Path(out_dir) / "manifest.json"
    manifest = []
    if manifest_path.exists():
        with open(manifest_path) as f:
            manifest = json.load(f)
    manifest = [m for m in manifest if m["name"] != meta["name"]]
    manifest.append(meta)
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["chm", "quality", "slope"])
    parser.add_argument("las_file")
    parser.add_argument("--out-dir", default=None)
    args = parser.parse_args()

    out_dir = args.out_dir or f"../laz-viewer/data/{args.command}"
    meta = build_raster(args.las_file, out_dir, args.command)
    print(json.dumps(meta, indent=2))


if __name__ == "__main__":
    main()
