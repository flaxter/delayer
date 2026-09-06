#!/usr/bin/env python3
"""Fetch the Kaiserslautern forecast and write data/forecast.json.

Stdlib only. The site also fetches Open-Meteo live in the browser; this snapshot
is what the page paints with instantly on load, and what it falls back to when
the network is unavailable. Run from anywhere:

    python3 scripts/update_forecast.py
"""
import json
import pathlib
import sys
import urllib.request
from datetime import datetime, timezone

LAT, LON = 49.4447, 7.7689          # Kaiserslautern
ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "forecast.json"

FORECAST = (
    "https://api.open-meteo.com/v1/forecast"
    f"?latitude={LAT}&longitude={LON}"
    "&hourly=temperature_2m,apparent_temperature,precipitation,precipitation_probability,"
    "weather_code,wind_speed_10m,wind_gusts_10m,cloud_cover,relative_humidity_2m"
    "&daily=sunrise,sunset,temperature_2m_min,temperature_2m_max,"
    "apparent_temperature_min,apparent_temperature_max,precipitation_sum,"
    "precipitation_probability_max,weather_code"
    "&models=icon_seamless&timezone=Europe%2FBerlin&forecast_days=9"
)
ALERTS = f"https://api.brightsky.dev/alerts?lat={LAT}&lon={LON}"


def get(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": "kl-weather/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def main():
    try:
        forecast = get(FORECAST)
    except Exception as e:
        # Leave the previous snapshot in place rather than publishing nothing.
        print(f"ERROR: forecast fetch failed: {e}", file=sys.stderr)
        return 1

    if not forecast.get("hourly", {}).get("time"):
        print("ERROR: forecast response has no hourly data", file=sys.stderr)
        return 1

    # Warnings are nice to have; a failure here must not sink the run.
    try:
        alerts = get(ALERTS).get("alerts", [])
    except Exception as e:
        print(f"WARN: alerts fetch failed: {e}", file=sys.stderr)
        alerts = []

    payload = {
        "fetched": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "forecast": forecast,
        "alerts": alerts,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, separators=(",", ":")) + "\n")
    days = forecast["daily"]["time"]
    print(f"wrote {OUT} ({OUT.stat().st_size // 1024} KB), {days[0]} to {days[-1]}, "
          f"{len(alerts)} alert(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
