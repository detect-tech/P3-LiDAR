"""
Converts one or more LAZ/LAS point cloud files into 2D coverage footprint
polygons, merges footprints that overlap (including against coverage
already in an existing GeoJSON file) into single combined polygons, and
writes a GeoJSON FeatureCollection matching the schema the web app expects
(see web/app.js):

    properties: name, source, source_type ("public"|"internal"),
                collected (date), point_density_ppsm

Approach per file:
  1. Read points, drop noise-classified points (LAS class 7 = low noise,
     18 = high noise) so stray returns don't distort the footprint.
  2. Bin points into a grid in the file's native (projected) CRS units and
     keep only cells with enough points to count as "covered" — this
     hugs the actual flown area instead of a convex hull ballooning across
     empty space on winding corridor flights.
  3. Union the occupied cells into a polygon, morphologically close small
     gaps, drop stray single-cell speckle, simplify.
  4. Reproject the polygon boundary (not every point) to EPSG:4326 using
     the CRS embedded in the LAZ header — LAZ files store coordinates in
     whatever projected CRS the survey used (state plane, UTM, etc.), not
     lon/lat.

Records are a common dict shape used throughout (`polygon`, `point_count`,
`name`, `collected`, `source`, `source_type`, `source_files`) so freshly
extracted LAZ footprints and footprints loaded back from a previous
GeoJSON output can be merged together identically.

Usage:
    python laz_to_coverage.py file1.laz file2.laz ... --out ../laz-viewer/data/coverage.geojson
"""

import argparse
import json
import math
from pathlib import Path

import laspy
import numpy as np
import pyproj
from shapely.geometry import MultiPolygon, box, mapping, shape
from shapely.ops import transform as shapely_transform
from shapely.ops import unary_union

NOISE_CLASSES = {7, 18}
TARGET_GRID_CELLS_ACROSS = 150
MIN_POINTS_PER_CELL = 3
WATER_CLASS = 9
WIRE_TOWER_CLASSES = {13, 14, 15, 16}  # ASPRS: wire guard/conductor, transmission tower, wire connector


def horizontal_crs(header):
    crs = header.parse_crs()
    if crs is None:
        raise ValueError("LAZ file has no embedded CRS — cannot reproject to lon/lat")
    if crs.is_compound:
        for sub in crs.sub_crs_list:
            if sub.is_projected or sub.is_geographic:
                return sub
        raise ValueError("Compound CRS has no horizontal component")
    return crs


def unit_to_meters(crs):
    axis = crs.axis_info[0]
    return axis.unit_conversion_factor


def area_m2_wgs84(polygon):
    lon, lat = polygon.centroid.x, polygon.centroid.y
    aeqd = pyproj.CRS.from_proj4(f"+proj=aeqd +lat_0={lat} +lon_0={lon} +units=m")
    to_aeqd = pyproj.Transformer.from_crs("EPSG:4326", aeqd, always_xy=True).transform
    return shapely_transform(to_aeqd, polygon).area


def extract_footprint(las_path, source="Internal LiDAR (uploaded)", source_type="internal"):
    with laspy.open(las_path) as f:
        header = f.header
        crs = horizontal_crs(header)
        las = f.read()

    keep = ~np.isin(las.classification, list(NOISE_CLASSES))
    x = np.asarray(las.x)[keep]
    y = np.asarray(las.y)[keep]
    classification = np.asarray(las.classification)[keep]
    point_count = int(keep.sum())

    water_pct = round(100 * float(np.mean(classification == WATER_CLASS)), 2) if point_count else 0.0
    wire_tower_mask = np.isin(classification, list(WIRE_TOWER_CLASSES))
    wire_tower_count = int(wire_tower_mask.sum())

    xmin, xmax = x.min(), x.max()
    ymin, ymax = y.min(), y.max()
    span = max(xmax - xmin, ymax - ymin)
    cell_size = span / TARGET_GRID_CELLS_ACROSS

    nx = int(math.ceil((xmax - xmin) / cell_size)) + 1
    ny = int(math.ceil((ymax - ymin) / cell_size)) + 1

    counts, xedges, yedges = np.histogram2d(
        x, y, bins=[nx, ny], range=[[xmin, xmin + nx * cell_size], [ymin, ymin + ny * cell_size]]
    )

    occupied = np.argwhere(counts >= MIN_POINTS_PER_CELL)
    cells = [
        box(xedges[i], yedges[j], xedges[i + 1], yedges[j + 1])
        for i, j in occupied
    ]
    if not cells:
        raise ValueError(f"{las_path}: no cells passed the point-density threshold")

    # Morphological closing: fills small gaps and fuses nearby cells so the
    # outline reads as one coherent shape instead of a jagged cell grid.
    footprint = unary_union(cells).buffer(cell_size).buffer(-cell_size)

    # Stray single-cell blips (sensor noise, reflective surfaces) show up as
    # tiny disconnected polygons — drop anything under 5% of the largest
    # piece's area rather than let them clutter the footprint.
    if isinstance(footprint, MultiPolygon):
        polys = list(footprint.geoms)
        max_area = max(p.area for p in polys)
        footprint = unary_union([p for p in polys if p.area >= max_area * 0.05])

    footprint = footprint.simplify(cell_size * 0.5, preserve_topology=True)

    to_wgs84 = pyproj.Transformer.from_crs(crs, "EPSG:4326", always_xy=True).transform
    footprint_wgs84 = shapely_transform(to_wgs84, footprint)

    return {
        "polygon": footprint_wgs84,
        "point_count": point_count,
        "name": Path(las_path).stem,
        "collected": str(header.creation_date) if header.creation_date else "unknown",
        "source": source,
        "source_type": source_type,
        "source_files": [Path(las_path).stem],
        "water_pct": water_pct,
        "wire_tower_count": wire_tower_count,
    }


def load_existing_coverage(path):
    with open(path) as f:
        geojson = json.load(f)

    records = []
    for feature in geojson.get("features", []):
        polygon = shape(feature["geometry"])
        props = feature["properties"]
        area = area_m2_wgs84(polygon)
        point_count = round(props.get("point_density_ppsm", 0) * area)
        records.append({
            "polygon": polygon,
            "point_count": point_count,
            "name": props.get("name", "unknown"),
            "collected": props.get("collected", "unknown"),
            "source": props.get("source", "unknown"),
            "source_type": props.get("source_type", "internal"),
            "source_files": props.get("source_files", [props.get("name", "unknown")]),
            "water_pct": props.get("water_pct", 0.0),
            "wire_tower_count": props.get("wire_tower_count", 0),
        })
    return records


def merge_overlapping(records):
    n = len(records)
    parent = list(range(n))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    def union(i, j):
        ri, rj = find(i), find(j)
        if ri != rj:
            parent[ri] = rj

    for i in range(n):
        for j in range(i + 1, n):
            if records[i]["polygon"].intersects(records[j]["polygon"]):
                union(i, j)

    groups = {}
    for i in range(n):
        groups.setdefault(find(i), []).append(records[i])

    merged = []
    for group in groups.values():
        if len(group) == 1:
            merged.append(group[0])
            continue

        source_types = {g["source_type"] for g in group}
        sources = list(dict.fromkeys(g["source"] for g in group))
        collected_values = sorted(g["collected"] for g in group)
        total_points = sum(g["point_count"] for g in group)
        weighted_water_pct = (
            sum(g["water_pct"] * g["point_count"] for g in group) / total_points if total_points else 0.0
        )

        merged.append({
            "polygon": unary_union([g["polygon"] for g in group]),
            "name": " + ".join(g["name"] for g in group),
            "collected": collected_values[0] if len(collected_values) == 1
                else f"{collected_values[0]} – {collected_values[-1]}",
            "point_count": total_points,
            "source": " + ".join(sources),
            "source_type": "internal" if "internal" in source_types else "public",
            "source_files": sum((g["source_files"] for g in group), []),
            "water_pct": round(weighted_water_pct, 2),
            "wire_tower_count": sum(g["wire_tower_count"] for g in group),
        })
    return merged


def records_to_geojson(records):
    features = []
    for r in records:
        area = area_m2_wgs84(r["polygon"])
        density = r["point_count"] / area if area > 0 else 0
        features.append({
            "type": "Feature",
            "geometry": mapping(r["polygon"]),
            "properties": {
                "name": r["name"],
                "source": r["source"],
                "source_type": r["source_type"],
                "collected": r["collected"],
                "point_density_ppsm": round(density, 2),
                "source_files": r["source_files"],
                "water_pct": r.get("water_pct", 0.0),
                "wire_tower_count": r.get("wire_tower_count", 0),
            },
        })
    return {"type": "FeatureCollection", "features": features}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("laz_files", nargs="+")
    parser.add_argument("--out", default="../laz-viewer/data/coverage.geojson")
    parser.add_argument("--source", default="Internal LiDAR (uploaded)")
    parser.add_argument("--source-type", default="internal", choices=["internal", "public"])
    parser.add_argument("--fresh", action="store_true", help="ignore existing --out contents instead of merging against them")
    args = parser.parse_args()

    existing = []
    if not args.fresh and Path(args.out).exists():
        existing = load_existing_coverage(args.out)
        print(f"Loaded {len(existing)} existing feature(s) from {args.out}")

    new_records = [extract_footprint(p, args.source, args.source_type) for p in args.laz_files]
    print(f"Extracted {len(new_records)} footprint(s) from {len(args.laz_files)} file(s)")

    merged = merge_overlapping(existing + new_records)
    print(f"Merged into {len(merged)} feature(s) after overlap dissolve")

    geojson = records_to_geojson(merged)

    with open(args.out, "w") as f:
        json.dump(geojson, f, indent=2)
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
