# Delayer

װיפֿל שיכטן, און דאַרף מען אַ רעגן־מאַנטל? — how many layers, and do I need a
raincoat? A one-page Kaiserslautern forecast in Yiddish that answers the two
questions you actually have at 6:30am.

Live at <https://flaxter.github.io/delayer/>.

The day is split into four periods — 07:00–12:00, 12:00–16:00, 16:00–20:00 and
20:00–07:00 overnight — each judged on its own hours. Arrows step five days back
and a week forward.

## How the calls are made

Layers come from **apparent** temperature (wind chill and humidity included),
taken as the coldest hour in the period:

| feels like | verdict |
|---|---|
| ≥ 23 °C | טי־העמד (t-shirt) |
| 15–23 °C | 1 שיכט → סװעטער (sweater) |
| 7–15 °C | 2 שיכטן → סװעטער + רעקל (sweater + jacket) |
| 0–7 °C | 3 שיכטן → װאַרעמער מאַנטל (warm coat) |
| < 0 °C | 3 שיכטן → װאַרעמער מאַנטל, הוט און הענטשקעס |

Rain uses peak probability, accumulated millimetres and gusts across the period:
≥ 1 mm or ≥ 60 % says raincoat, ≥ 0.2 mm or ≥ 30 % says umbrella, otherwise
nothing. Above 40 km/h gusts it says raincoat instead of umbrella, because an
umbrella is useless at that point. When the verdict is rain, the outermost layer
becomes the waterproof one (רעגן־מאַנטל).

Legs are called separately, from the period's *warmest* hour: הײזקעס (shorts) at
22 °C and above, otherwise הױזן (trousers).

Adjust the bands in `layerCall()`, `rainCall()` and `SHORTS_ABOVE` in
`index.html`.

## Data

- Forecast: DWD ICON-D2 / ICON-EU via [Open-Meteo](https://open-meteo.com/),
  seamless blend, hourly, five days back and nine forward.
- Warnings: official DWD warnings for the Kaiserslautern-Stadt warn cell
  (707312001) via [Bright Sky](https://brightsky.dev/).

Both are fetched **live in the browser** on every load, and again whenever you
return to the tab. There is no build step, no stored data and no scheduled job:
the page is a single HTML file, and what you see is never staler than the moment
you opened it. If the fetch fails it says so rather than showing old numbers.

## Language

Yiddish (klal Yiddish, YIVO orthography), right-to-left. Latin numerals, clock
times and units are wrapped in `.num` spans with `unicode-bidi: isolate` so they
keep their own run inside Yiddish text. The hour-by-hour plot and the day
stepper stay left-to-right — the first is a numeric time axis, the second by
preference.

## Local

```bash
python3 -m http.server 8000   # http://localhost:8000
```

Every push to `main` redeploys via `.github/workflows/pages.yml`.
