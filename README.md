# P3-LiDAR — LIDACore

Problem 03 (Detect × NEET Hackathon): an integrated LiDAR platform for transmission
route planning — checks a proposed corridor against existing LiDAR coverage, flags
hazards (buildings, vegetation, water, elevation changes), and estimates new
collection cost for any gaps.

## Where things are

The web app lives under `laz-viewer/`, not the repo root:

- `laz-viewer/coverage-map.html` — the main tool (self-contained, data inlined).
  Open this directly in a browser.
- `laz-viewer/coverage-map.src.html` — the same tool, but loading its GeoJSON/raster
  data via `fetch()` instead of inlining it. Edit this one; it needs to be served
  over HTTP (not opened as a `file://` URL) since it fetches from `laz-viewer/data/`.
- `laz-viewer/data/` — coverage GeoJSON (USGS 3DEP, NOAA Digital Coast) and derived
  CHM/quality/slope rasters.
- `laz-viewer/index.html` / `miami-lidar-viewer.html` — a raw 3D point cloud viewer
  for a single sample tile.

`presentation.html` (repo root) is the pitch deck; its "Open live demo" link points
at `laz-viewer/coverage-map.html`.

## Data processing scripts

`scripts/` — Python (see `requirements.txt`) and shell scripts that turn raw `.laz`
point clouds into the GeoJSON/raster data consumed by the web app:

- `fetch_usgs_lidar_coverage.sh` — pulls USGS 3DEP coverage metadata for a bbox.
- `laz_to_coverage.py` — converts `.laz` files into coverage footprint polygons.
- `derived_rasters.py` — generates CHM / quality / slope rasters from a `.laz` file
  (depends on `laz_to_coverage.py`).

```
pip install -r requirements.txt
python scripts/laz_to_coverage.py file.laz --out laz-viewer/data/coverage.geojson
python scripts/derived_rasters.py chm file.laz --out-dir laz-viewer/data/chm
```

## Sample data

`sample-data/` holds raw `.laz` tiles used for local testing and is gitignored
(several hundred MB) — not part of the repo.
