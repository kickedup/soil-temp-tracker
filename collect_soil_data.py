"""Collect soil temperature data for Cincinnati, OH from the Open-Meteo API.

Runs daily via GitHub Actions and appends a row to data/soil_temperatures.csv.
Open-Meteo is free and requires no API key.
"""

import csv
import os
from datetime import datetime
from zoneinfo import ZoneInfo

import requests

# --- Configuration: change these for your exact location ---
LATITUDE = 39.10
LONGITUDE = -84.51
TIMEZONE = "America/New_York"
CSV_PATH = os.path.join("data", "soil_temperatures.csv")

API_URL = "https://api.open-meteo.com/v1/forecast"
PARAMS = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "hourly": (
        "soil_temperature_0cm,soil_temperature_6cm,"
        "soil_temperature_18cm,soil_temperature_54cm,"
        "soil_moisture_0_to_1cm"
    ),
    "temperature_unit": "fahrenheit",
    "timezone": TIMEZONE,
    "forecast_days": 1,
}


def fetch_current_soil_data() -> dict:
    """Fetch today's hourly soil data and return the row closest to now."""
    response = requests.get(API_URL, params=PARAMS, timeout=30)
    response.raise_for_status()
    hourly = response.json()["hourly"]

    now = datetime.now(ZoneInfo(TIMEZONE))
    # Hourly timestamps look like "2026-08-10T10:00" in local time.
    target = now.strftime("%Y-%m-%dT%H:00")
    try:
        idx = hourly["time"].index(target)
    except ValueError:
        idx = len(hourly["time"]) - 1  # fall back to the latest available hour

    return {
        "date": now.strftime("%Y-%m-%d"),
        "time_local": now.strftime("%H:%M"),
        "soil_temp_surface_f": hourly["soil_temperature_0cm"][idx],
        "soil_temp_6cm_f": hourly["soil_temperature_6cm"][idx],
        "soil_temp_18cm_f": hourly["soil_temperature_18cm"][idx],
        "soil_temp_54cm_f": hourly["soil_temperature_54cm"][idx],
        "soil_moisture_0_1cm": hourly["soil_moisture_0_to_1cm"][idx],
    }


def append_row(row: dict) -> None:
    os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)
    file_exists = os.path.exists(CSV_PATH)
    with open(CSV_PATH, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(row.keys()))
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


if __name__ == "__main__":
    data = fetch_current_soil_data()
    append_row(data)
    print(f"Recorded soil data for {data['date']} {data['time_local']}: {data}")
