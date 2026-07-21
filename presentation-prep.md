# Presentation Prep — Problem 03: LiDAR Data Availability for Transmission Route Development

**Detect x NextEra Energy Transmission (NEET) Hackathon — Tuesday, July 21, 2026**

---

## 1. The actual goal (read this before building anything else)

Per Justin Lee, this hackathon is a **business development exercise**, not a build-a-finished-product exercise:
1. Showcase how AI can be used to iterate and build solutions.
2. Build a strong connection with NEET — make them comfortable reaching out to Detect for AI/product-building help.
3. Design a solution clear enough in business value that NEET could take it and formalize/build it out properly.

A fully working application is a bonus ("huge win"), not the bar. **The bar is a demo that reads as clear business value** to NEET leadership. Bias every decision toward narrative clarity and polish over feature completeness.

### Day schedule (Tuesday July 21)
- 8:45–9:00AM Introductions
- 9:00–10:00AM Problem discussion and knowledge sharing (the only window to ask NEET teammates clarifying questions before building)
- 10:00AM–12PM Hackathon (design iteration, building)
- 12–1PM Lunch
- 1–3PM Hackathon (building, presentation prep)
- 3–4:45PM Presentations — **10 min presentation / 10 min questions / 5 min buffer**

Only ~4 hours of actual build time. Presentation prep time matters as much as building.

---

## 2. Problem statement (as given)

**Problem 03 — LiDAR data availability for transmission route development**

Transmission route development often requires aerial LiDAR collection over potential study areas. This process can be costly and deadline-driven, and it depends on seasonal conditions that affect data quality. In many cases, usable LiDAR data already exists across public sources or previously acquired datasets, but there's no easy way to see what's already available for a given study area before committing to a new, expensive collection effort. Without centralized visibility, teams risk duplicating collection that's already been done elsewhere, or discovering usable data too late in a tight route-development window to take advantage of it.

**The opportunity (as stated):** Build a solution that identifies existing LiDAR coverage across public and previously-acquired sources, centralizes visibility into what's available for a study area, and helps teams reduce duplicate collection and minimize new data acquisition during tight route development timelines.

---

## 3. Discovery notes — pre-hackathon (Parthvi's own prep notes)

**Input**
- .LAZ file(s) of LiDAR — ?
- .KML file for powerline structures — GPS coordinates — ?

**Output expectations**
- Pain points?
- Map view → what we have (coverage LiDAR)
- Map view for powerline — ? (overlay)
- Stats / viz — ?

**Questions prepped to ask the team:**
1. How do you get input LiDAR data?
2. How do you get input powerline data? (format)
3. Why is it important? How do you use this?
4. What stats/visualizations are useful?
5. Integration with anything you have already?
6. What do we need to provide so you can use this info? (e.g. .KML filtered/uncovered)

---

## 4. Discovery notes — live, from the 9–10AM session with NEET

### Pain points (from NEET rep, verbatim)
1. Cost of publicly available data getting duplicated (i.e., re-flying LiDAR that's already public)
2. Building detection
3. Planning clearance, terrain

### Use cases
1. Route planning for a new build
2. Maintenance of an existing line
3. Upgrades

### Refined input/output (handwritten, live)
- Input: route is planned → GPS coordinates as **.KML + a polygon of land/offset** (right-of-way corridor), originally sourced from **ArcGIS**
- Check public LiDAR data for: point cloud density (bandwidth: high/medium/low), **staleness** (2yr cutoff as a quality filter), building detection quality (critical vs. other)
- Example filter: "300m from any property"
- **Flags to surface:**
  - Missing public/historic data
  - Stale data (≥2yrs, doesn't meet quality bar)
  - Building/hazards (vegetation, water)
  - Elevation change
- **Hazard identification list** should include: confidence, resolution, "clickable — pans to it in the map area", type (building/hazard: vegetation, water), elevation change
- Mentioned twice: a **chatbot** interface for reviewing/querying flagged threats (not built — out of scope for today, noted as a future idea)
- **Reroute suggestion was on the whiteboard but is explicitly OUT OF SCOPE for today's build** (per direct instruction after the discussion)

### Whiteboard flow (user → tool)
**User side:** ID use case (new line / maintenance / upgrades) → specify route + offsets (begin / end / tie points / criticality by segment) → plot route on map. Green annotation: **"Routify Tie-In"** — Routify appears to be an existing NextEra route-planning tool; route + offsets would ideally come from there.

**Tool side:** query database against constraints → ID areas that don't meet spec for route + constraints → provide a report (missing areas, insufficient resolution — broken down by density/date, shown on the map) **plus** areas we do have data for, **plus** building/hazard IDs.

**Report categories on the whiteboard:** Missing / Low Resolution / Hazards.

**Future work (noted, not in scope today):** switchable views, "Next Vision 2," Routify integration, export → DEM.

---

## 5. How the use case sharpened over the day

**Before the 9AM discussion:** "Show what LiDAR coverage already exists for a study area, so teams don't duplicate collection." (A coverage catalog / gap finder.)

**After the 9AM discussion:** The real ask is **hazard detection along an already-planned route** — given a real route (KML + right-of-way corridor polygon), check existing LiDAR against it and flag where the route runs into **buildings, vegetation, water, or elevation changes** — and flag where the *data itself* is too missing/stale/low-resolution to trust that hazard check in the first place. Coverage/gap detection (what was originally built) becomes one input into a hazard report, not the whole deliverable.

**Explicitly out of scope for today:** rerouting/reroute suggestions, chatbot interface, real Routify/ArcGIS integration.

**Update:** a real KML route was provided (`Mock_Route.kmz`) partway through the build — see section 6, this is no longer purely hypothetical.

---

## 6. What's actually been built

All of this lives in `laz-viewer/` and is self-contained (no server needed, just open the HTML file):

### `laz-viewer/coverage-map.html` — the main deliverable
A split-pane dashboard: map on the left, analysis panel on the right.
- **Map layers:** real USGS 3DEP LiDAR tile coverage for Miami-Dade (1,534 tiles, 2023–24 collection, pulled from USGS's public S3-hosted metadata, no API key) plus an older 2017 Everglades-area collection — both real, not mocked.
- **Route list, default/first entry is REAL data:** `Mock_Route.kmz`, provided by NEET partway through the build, is an actual ArcGIS Network Analyst output (has PathCost/ROUTE_NAME/BUFF_DIST fields) named **"Miami_Lauderdale_Line"** — a 15-vertex route from Miami up into Broward County, with a real 75ft right-of-way buffer width (parsed directly from the KML, not guessed). Run through the exact same analysis as everything else: **80.4% covered / 19.6% gap**, verified independently in Python/Shapely before wiring into the dashboard. This is the centerpiece for the demo — lead with it, not the sample routes.
- **4 additional sample study corridors** (kept for variety/backup, clearly labeled "(sample)" in the UI to distinguish from the real one), each with a genuinely different, verified-real-against-real-coverage-data result:
  - *Urban core corridor* — 100% covered, fully reusable
  - *Southwest corridor* — mixed coverage, includes a real duplicate-collection overlap zone
  - *Long-haul corridor* — mostly covered with a small real gap near the Everglades interior
  - *Northern extension corridor* — ~52% covered / ~48% gap (crosses into Broward County, genuinely outside both cataloged datasets) — the clean "partially covered" demo case
- **Corridor-width slider** (100–2,500 ft) re-runs the analysis live.
- **Recommendation banner** — plain-language verdict (reuse / partial / collect), color-coded, calls out duplicate-collection zones by name.
- **KPI tiles** — corridor area, % covered, gap remaining, reusable tile count, illustrative cost-avoided estimates (clearly labeled as estimates).
- **Coverage composition** — a single stacked bar (not a donut) splitting the corridor into 4 mutually-exclusive categories: fresh-only / duplicate-overlap / older-only / gap. Verified via an independent Python/Shapely re-implementation that these sum exactly to the study area (no double-counting).
- **Coverage-by-category bar chart** with a "View as table" toggle (accessibility-required data table for every chart).
- **Reusable tiles list** — every intersecting tile with source, era, and a direct LAZ download link.
- **Hazards panel (new, added post-discovery-pivot)** — mock hazard data (buildings, vegetation, water, elevation change) placed at realistic points along each route's actual geometry (interpolated along the real route line, not arbitrary), each with a confidence level and a note. Clickable hazard list pans the map to and opens a popup on the selected hazard. Legend + map markers colored by hazard type, sized by confidence.
- **Light mode (default) and dark mode**, toggle in the header, built on the Cobalt UI design system (`hackathon-design-system-reference.md`).

### `laz-viewer/miami-lidar-viewer.html` — supporting artifact
A standalone 3D point-cloud viewer (Three.js) rendering one real downloaded LAZ tile (1.6M points, Brickell/Downtown Miami). Mostly a "here's what raw LiDAR data actually looks like" demo piece, not the main deliverable — useful if the presentation wants a "wow, that's real point-cloud data" moment.

### `scripts/fetch_usgs_lidar_coverage.sh`
Reusable pipeline to pull real USGS 3DEP coverage data for any county/project (not just Miami-Dade), in case NEET's actual routes are elsewhere. Tested end-to-end, verified byte-for-byte reproducible.

### `sample-data/lidar/miami_brickell_sample.laz`
One real downloaded LiDAR tile (7.3MB, USGS 3DEP) backing the point-cloud viewer.

---

## 7. Design system

Everything is built against `hackathon-design-system-reference.md` (Cobalt UI): Cobalt blue for primary actions/links, pill buttons, AA-contrast-checked status colors (verified by hand with WCAG contrast math since Node/the automated dataviz color validator wasn't available in this environment), light and dark themes both fully supported, Instrument Sans throughout.

---

## 8. Suggested presentation narrative (10 minutes)

A possible structure for the 3PM demo, given the business-development framing:

1. **The problem, in NEET's own words** (30 sec) — duplicated LiDAR collection costs money and time; teams can't easily see what already exists before committing to a new expensive flight.
2. **Show the map** (2 min) — real Miami-Dade coverage, real 2017 vs. 2023–24 data, point out the duplicate-collection overlap zone found in real data.
3. **Pick a corridor, show the analysis** (2–3 min) — walk through the **real "Miami–Lauderdale Line" route NEET provided** (80.4% covered / 19.6% gap): some of it's reusable, some needs new collection, quantify both. This is the strongest moment in the demo — it's their own data, not a hypothetical.
4. **Show hazards** (2 min) — buildings/vegetation/water/elevation flagged along the route, tied back to NEET's own stated pain points (building detection, planning clearance, terrain).
5. **The business case** (1–2 min) — this took one AI-assisted build session to prototype against real public data; formalized, it directly targets NEET's stated cost-of-duplication pain point.
6. **What's next, if NEET wants it** (30 sec) — real KML/Routify integration, real internal LiDAR archive integration, the chatbot/reroute ideas from today's whiteboard.

---

## 9. Open items / things to double check before presenting

- **Coverage numbers for the real route (81% covered / 0.22 km² gap, corridor area 1.16 km²) are real** (computed against actual USGS coverage data) but the **route itself may be a mock/test file** (`Mock_Route.kmz` — filename suggests test data, not necessarily a real planned NextEra line). Confirm with the NEET rep whether this is a real corridor or a placeholder before stating it's "their real route" on stage — say "a route NEET provided" rather than asserting it's an actual planned line if unconfirmed.
- Mock hazard data (all buildings/vegetation/water/elevation flags, including on the provided route) is clearly mock — say so explicitly in the demo, don't imply it's real hazard detection output.
- **Visually verified as of 2026-07-21 11:22AM** (headless Chrome screenshots, both light and dark mode, both stored in `laz-viewer/screenshots/`) — the dashboard renders correctly end to end: map, route selector, hazards, KPI tiles, composition chart, bar chart, tile list. A real bug was caught and fixed in this pass: the corridor-width slider's `min="100"` HTML attribute was silently clamping the real route's intended 75ft width up to 100ft, while the label text still (incorrectly) displayed "75 ft" — so the numbers shown (1.54 km²/7.73 km² depending on which sample) didn't match the true 75ft analysis. Fixed by lowering the slider's min to 50 and step to 25; verified the corrected area (1.16 km²) matches an independent geodesic ground-truth calculation to within 0.5%. Still worth a live check on the actual presentation laptop/projector before 3PM, but the core numbers can now be trusted.
