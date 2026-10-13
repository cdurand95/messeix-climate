# Climate Intelligence Report — Messeix (Puy-de-Dôme, France)

## Project goal

Produce a **highly technical, data-driven climate report** for the commune of
Messeix (Auvergne-Rhône-Alpes, Puy-de-Dôme, Massif Central, France). The report
must quantify the observed and projected evolution of the local climate and
translate it into an **agricultural adaptation plan** for the coming decades.

All analytical work is notebook-first (`.ipynb`) using the `data` agent, and the
final narrative is delivered as a standalone markdown report. Every quantitative
claim must trace back to a reproducible cell in the notebook and a cited source
(ERA5 and/or Météo-France). No invented figures.

## Geographic context (fixed inputs, do not guess)

- **Location:** Messeix, Puy-de-Dôme (63), Massif Central.
- **Approximate coordinates:** ~45.62° N, ~2.54° E (verify and hard-code once
  used). Confirm with a gazetteer before analysis.
- **Elevation:** ~700–800 m a.s.l. (mountainous upland plateau). Verify the
  actual commune centroid elevation and use it consistently.
- **Regime:** montane variant of the oceanic climate, with cold winters,
  frequent frost, significant winter snow, and warm but short summers.

Record the exact coordinates, elevation, and the CRS used (EPSG:2154 for France /
EPSG:4326 for reanalysis grid extraction) in the notebook metadata.

## Data sources

### 1. ERA5 (Copernicus Climate Data Store)

Pull single-level reanalysis variables for the grid cell(s) closest to Messeix:

- **Essential variables:** 2-m air temperature (`t2m`, daily mean/min/max),
  total precipitation (`tp`), 10-m wind (`u10`, `v10`), surface solar radiation
  downwards (`ssrd`), 2-m dewpoint (`d2m`), surface pressure (`sp`), snow depth
  (`sd`), evapotranspiration (`e`), total soil moisture layers (`swvl1..4`),
  and relative humidity (derived from `d2m`/`t2m`).
- **Time extent:** monthly aggregates 1940–present for trend analysis, and daily
  or sub-daily (`hourly`) for index computation over a recent 30-year climate
  normal (1991–2020) and the last full year.
- **Access:** CDS API (`cdsapi`), product `reanalysis-era5-single-levels`.
  Include the exact `area` bounding box around Messeix (small window, e.g.
  45.3–45.9° N, 2.1–2.9° E) and select the nearest grid point (~0.25° resolution).
- Document the ERA5 version/date and any known biases (ERA5 tends to be cooler /
  slightly wetter than station obs in mountain valleys) in a caveats section.

### 2. Météo-France nearest station

- Identify the nearest operational Météo-France (or Météo-France climatology /
  SAFRAN) station to Messeix using the official open-data station registry
  (postes SYNOP / Climatologie). Nearest candidate is typically in the
  Clermont-Ferrand–Puy-de-Dôme or Bourbonnais/Limousin corridor; **verify** the
  single closest station to the commune centroid and note its ID, name,
  elevation, and period of record.
- Pull daily series (Tmin, Tmax, Tmean, precipitation, wind, snow depth if
  available) from Météo-France open data (Climatologie API / `meteofrance-api` /
  DRIAS-adjacent datasets), covering at least 1981–present.
- **Reconcile** station vs ERA5: compute monthly biases and state whether the
  station is representative of the Messeix upland microclimate (elevation
  difference is a first-order bias source).

## Analyses to include (all quantitative, reproducible)

### A. Climatology and normals
- Monthly climatology (1991–2020) of Tmean/Tmin/Tmax, precipitation, frost days,
  and snow days, for both ERA5 and the station.
- Elevation/temperature lapse-rate adjustment if the station differs materially
  in altitude from Messeix.

### B. Trends and evolution
- Linear (OLS + Mann-Kendall with Sen's slope) trends for annual and seasonal
  temperature and precipitation over the full ERA5 record (1940→present).
- Decadal anomalies relative to the 1961–1990 baseline; report significance
  (p-value) and confidence intervals. Do not report noise as signal.
- Frost-free season length, growing season start/end (thermal thresholds, e.g.
  5 °C, 10 °C), heat extremes (Tmax > 30/35 °C), and heavy-precipitation indices.

### C. Agroclimatic / bioclimatic indicators
- Growing degree days (GDD, base 5 °C and 10 °C) and their trends.
- Huglin index (wine/thermal suitability) and De Martonne aridity index.
- Water balance: reference evapotranspiration (Hargreaves or FAO-56 PM from ERA5
  variables), climatic water balance (P − PET), soil moisture deficit across
  seasons, and drought frequency (e.g. SPI/SPEI or P − PET percentile thresholds).
- Frost risk windows (last spring frost, first autumn frost, probability of
  frost in each 10-day period) — critical for crop/variety selection in a
  montane site.

### D. Projection context (if CDS / DRIAS projection data is accessible)
- If ERA5-Land or EURO-CORDEX / DRIAS scenario data are accessible, summarise
  RCP/SSP (SSP2-4.5, SSP5-8.5) sign-of-change for temperature and summer drought.
  Clearly label projection data as scenarios, not forecasts. If not accessible,
  state this explicitly rather than inventing values.

## Agriculture adaptation plan (deliverable)

Translate the quantitative findings into an evidence-based plan for the coming
decades, tailored to a montane upland:

- **Crop and variety selection:** match thermal requirements (GDD, frost
  tolerance, chilling requirements) to the projected growing season; assess
  viability of higher-value crops (e.g. fruit/arboriculture, wine at the upper
  thermal limit, seed crops, protein crops) vs. current forage/pasture/livestock
  mix.
- **Water & irrigation:** quantify summer water deficit; assess need for
  storage/irrigation, drought-resistant cultivars, and soil-water conservation
  (mulching, cover crops, reduced tillage, organic-matter management).
- **Frost risk management:** strategies given a longer but frostier-risk shoulder
  season (late frost after early warm spells) — frost protection, later
  planting, hardy rootstocks/varieties, delayed pruning.
- **Livestock/pasture:** implications of warmer winters and summer dry spells on
  pasture productivity, forage stocks, and heat stress.
- **Diversification & risk:** climate-resilient rotations, agroforestry, and
  insurance/economic risk framing.
- Rank recommendations by robustness under both warm-wet and warm-dry scenarios;
  flag where decisions are sensitive to scenario choice.

## Deliverables

1. **`climate_messeix.ipynb`** — all data pulls, processing, trend/index
   computations, and figures. Every cell must execute; keep outputs and summaries
   concise.
2. **`CLIMATE_REPORT_Messeix.md`** — the final narrative report: executive
   summary, data & methods, results (with figures embedded or referenced), caveats
   (ERA5 vs station bias, projection uncertainty), and the agriculture adaptation
   plan.
3. **Figures** — trend plots, climatology plots, water-balance and frost-risk
   plots (saved as PNG/SVG into a `figures/` directory and referenced by the
   report).

## Technical standards & guardrails

- Notebook-first: append and execute cells; never claim a cell ran if it did not.
- Reproducibility: fixed seed where stochastic; record package versions
  (`environment.yml` or `pip freeze`); pin API request parameters.
- Units and CRS: keep SI units; state coordinate reference system for every
  spatial operation.
- Sources: cite ERA5 (CDS DOI) and Météo-France dataset/station IDs explicitly.
- Separate **data** (observed ERA5 + station) from **projections** (scenario
  model output) and from **recommendations** (judgment) throughout the report.
- Uncertainty: always report significance, confidence intervals, or a clear
  qualitative uncertainty rating for any trend or projection claim.
- No invented numbers: if a dataset is not retrievable (no CDS key, no station),
  document the gap and proceed with the available source, clearly labelled.
