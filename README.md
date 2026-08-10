# Soil Temperature Tracker

Collects daily soil temperature and surface moisture data for the Cincinnati, OH area using the free [Open-Meteo API](https://open-meteo.com/) (no API key required). A GitHub Actions workflow runs every day at 10AM Eastern, fetches the data, and commits a new row to `data/soil_temperatures.csv`.

## Data collected

Each daily row includes soil temperature (°F) at four depths — surface (0cm), 6cm, 18cm, and 54cm — plus topsoil moisture (0–1cm, m³/m³). The 6cm depth is roughly seed depth, useful for planting decisions.

## Setup

1. Create a new GitHub repository and push these files to it.
2. Go to the repo's **Settings → Actions → General → Workflow permissions** and select **"Read and write permissions"** so the workflow can commit the CSV.
3. That's it. The workflow runs automatically at 10AM Eastern every day. You can also trigger it manually from the **Actions** tab via "Run workflow" to test it.

## Customizing your location

Edit the constants at the top of `collect_soil_data.py`:

```python
LATITUDE = 39.10      # your latitude
LONGITUDE = -84.51    # your longitude
TIMEZONE = "America/New_York"
```

## How the 10AM schedule works

GitHub Actions cron schedules run in UTC and don't understand daylight saving time. The workflow triggers at both 14:00 and 15:00 UTC, then a guard step checks the actual Eastern time and only proceeds when it's 10AM locally. Note that GitHub scheduled runs can start a few minutes late during periods of high load — the script records the actual collection time in the CSV.
