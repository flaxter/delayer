# Delayer

How many layers, and do I need a raincoat? Kaiserslautern, every morning.

Live at <https://flaxter.github.io/delayer/>.

The day is split into four periods — 07:00–12:00, 12:00–16:00, 16:00–20:00, and
20:00–07:00 overnight — each judged on its own hours. Arrows at the top step
forward a week.

## How the calls are made

Layers come from **apparent** temperature (wind chill and humidity included),
taken as the coldest hour in the period:

| feels like | verdict |
|---|---|
| ≥ 23 °C | t-shirt |
| 15–23 °C | 1 layer → sweatshirt or jacket |
| 7–15 °C | 2 layers → sweatshirt + jacket |
| 0–7 °C | 3 layers → warm coat |
| < 0 °C | 3 layers → warm coat, hat and gloves |

Rain uses peak probability, accumulated millimetres and gusts across the period:
≥ 1 mm or ≥ 60 % says raincoat, ≥ 0.2 mm or ≥ 30 % says umbrella, otherwise
nothing. Above 40 km/h gusts it says raincoat instead of umbrella, because an
umbrella is useless at that point.

Adjust the bands in `layerCall()` / `rainCall()` in `index.html`.

## Data

- Forecast: DWD's ICON-D2 / ICON-EU via [Open-Meteo](https://open-meteo.com/),
  seamless blend, hourly, nine days.
- Warnings: official DWD warnings for the Kaiserslautern-Stadt warn cell
  (707312001) via [Bright Sky](https://brightsky.dev/).

The browser fetches both live on every load, so the page is never staler than
the moment you opened it. `data/forecast.json` is a committed snapshot, painted
instantly on load before the live request returns, and used as the fallback when
there is no network.

## Automation

`.github/workflows/update.yml` refreshes that snapshot **once a day** (03:20
UTC) and commits it only when it changed. Each run retries three times before
giving up and leaving the previous snapshot in place. Every push to `main`
redeploys via `.github/workflows/pages.yml`.

No server is involved: the schedule runs on GitHub's own ephemeral runners. The
snapshot does not need to be fresh to the hour, because the browser fetches the
live forecast on every load anyway.

## Local

```bash
python3 scripts/update_forecast.py   # refresh data/forecast.json (stdlib only)
python3 -m http.server 8000          # http://localhost:8000
```
