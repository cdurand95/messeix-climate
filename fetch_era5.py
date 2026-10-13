import urllib.request, json, time, os, sys
import pandas as pd

lat, lon = 45.62, 2.54
VARS = "temperature_2m_max,temperature_2m_min,temperature_2m_mean,precipitation_sum,snowfall_sum,et0_fao_evapotranspiration,windspeed_10m_max,shortwave_radiation_sum,precipitation_hours"
OUTDIR = "data/era5_openmeteo_chunks"
os.makedirs(OUTDIR, exist_ok=True)


def fetch(s, e):
    url = (f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}"
           f"&start_date={s}&end_date={e}&daily={VARS}&timezone=UTC")
    for attempt in range(10):
        try:
            with urllib.request.urlopen(url, timeout=180) as r:
                return json.load(r)
        except Exception as ex:
            w = 15 * (attempt + 1)
            print(f"retry {attempt} {s} {ex} sleep {w}", flush=True)
            time.sleep(w)
    raise RuntimeError("fetch failed " + s)


chunks = [("1940-01-01", "1949-12-31"), ("1950-01-01", "1959-12-31"),
          ("1960-01-01", "1969-12-31"), ("1970-01-01", "1979-12-31"),
          ("1980-01-01", "1989-12-31"), ("1990-01-01", "1999-12-31"),
          ("2000-01-01", "2009-12-31"), ("2010-01-01", "2019-12-31"),
          ("2020-01-01", "2026-12-31")]

for s, e in chunks:
    outfile = os.path.join(OUTDIR, f"{s[:4]}_{e[:4]}.csv")
    if os.path.exists(outfile):
        print(f"skip {s} (exists)", flush=True)
        continue
    d = fetch(s, e)
    df = pd.DataFrame(d["daily"])
    df["date"] = pd.to_datetime(df["time"])
    df.to_csv(outfile, index=False)
    print(f"done {s} rows={len(df)} last={df['date'].max().date()}", flush=True)
    time.sleep(10)

print("ALL_CHUNKS_DONE", flush=True)
