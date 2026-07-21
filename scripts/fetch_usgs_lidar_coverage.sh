#!/bin/bash
# Fetch USGS 3DEP LiDAR tile coverage for a project and build a GeoJSON coverage layer.
#
# Usage:
#   ./fetch_usgs_lidar_coverage.sh <PROJECT> <SUBPROJECT> <OUT_NAME>
#
# Example (what we used for Miami-Dade):
#   ./fetch_usgs_lidar_coverage.sh FL_MiamiDade_D23 FL_MiamiDade_1_D23 miamidade_coverage
#
# To find PROJECT/SUBPROJECT names for a different county:
#   1. Browse https://prd-tnm.s3.amazonaws.com/?prefix=StagedProducts/Elevation/LPC/Projects/
#      (or curl it, see find_usgs_project.sh below)
#   2. Look for a folder matching the county/state you need
#
# Requires: curl, python3 (no extra pip packages needed)

set -e

PROJECT="$1"
SUBPROJECT="$2"
OUT_NAME="${3:-coverage}"

if [ -z "$PROJECT" ] || [ -z "$SUBPROJECT" ]; then
  echo "Usage: $0 <PROJECT> <SUBPROJECT> <OUT_NAME>"
  echo "Example: $0 FL_MiamiDade_D23 FL_MiamiDade_1_D23 miamidade_coverage"
  exit 1
fi

BASE_URL="https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/LPC/Projects/${PROJECT}/${SUBPROJECT}"
WORKDIR="$(mktemp -d)"
OUTDIR="$(dirname "$0")/../laz-viewer/data"
mkdir -p "$OUTDIR"

echo "Step 1/4: fetching tile download-link list..."
curl -s "${BASE_URL}/0_file_download_links.txt" -o "${WORKDIR}/download_links.txt"
TILE_COUNT=$(wc -l < "${WORKDIR}/download_links.txt" | tr -d ' ')
echo "  found ${TILE_COUNT} tiles"

echo "Step 2/4: deriving metadata XML URLs..."
sed -E 's#/LAZ/#/metadata/#; s#\.laz$#.xml#' "${WORKDIR}/download_links.txt" > "${WORKDIR}/meta_urls.txt"

echo "Step 3/4: downloading metadata XML files (parallel, this is the slow step)..."
mkdir -p "${WORKDIR}/meta"
cd "${WORKDIR}/meta"
xargs -P 30 -n 1 curl -s -O < "${WORKDIR}/meta_urls.txt"
cd - > /dev/null
echo "  downloaded $(ls "${WORKDIR}/meta" | wc -l | tr -d ' ') metadata files"

echo "Step 4/4: parsing bounding boxes into GeoJSON..."
python3 << PYEOF
import glob, re, json, os

# build filename -> authoritative download URL lookup from the real USGS link list,
# rather than reconstructing URLs by hand (avoids assuming a URL host/structure)
url_by_name = {}
with open("${WORKDIR}/download_links.txt") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        fname = os.path.basename(line).replace('.laz', '')
        url_by_name[fname] = line

files = glob.glob("${WORKDIR}/meta/*.xml")
pat = re.compile(r'<westbc>([-\d.]+)</westbc>\s*<eastbc>([-\d.]+)</eastbc>\s*<northbc>([-\d.]+)</northbc>\s*<southbc>([-\d.]+)</southbc>')
date_pat = re.compile(r'<caldate>(\d+)</caldate>')

features = []
failed = 0
for fp in files:
    with open(fp, 'r', errors='ignore') as f:
        content = f.read()
    m = pat.search(content)
    if not m:
        failed += 1
        continue
    west, east, north, south = map(float, m.groups())
    dm = date_pat.search(content)
    date = dm.group(1) if dm else None
    name = os.path.basename(fp).replace('.xml', '')
    tile_code = re.sub(r'^.*_LID\d+_', '', name)  # short code (e.g. 319653_0901) instead of the full filename
    features.append({
        "type": "Feature",
        "properties": {
            "tile": tile_code,
            "source": "USGS 3DEP",
            "project": "${PROJECT}",
            "date": date,
            "laz_url": url_by_name.get(name, ""),
        },
        "geometry": {
            "type": "Polygon",
            "coordinates": [[[west, south], [east, south], [east, north], [west, north], [west, south]]],
        },
    })

print(f"  parsed {len(features)} tiles, {failed} failed to parse")

fc = {"type": "FeatureCollection", "features": features}
out_path = "${OUTDIR}/${OUT_NAME}.geojson"
with open(out_path, "w") as f:
    json.dump(fc, f)
print(f"  wrote {out_path} ({os.path.getsize(out_path)} bytes)")
PYEOF

rm -rf "${WORKDIR}"
echo "Done."
