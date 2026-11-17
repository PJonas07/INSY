"""Build website/data.js from the raw radon CSV.

The website only draws charts. Every number it shows is calculated here, so the
calculation can be read and tested in one place.

Run from the project folder:
    python3.12 scripts/build_site_data.py
"""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path
from statistics import fmean, median

PROJECT_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = PROJECT_DIR / "Dataset" / "radon_sample_data.csv"
OUTPUT_PATH = PROJECT_DIR / "website" / "data.js"

LOCAL_TIME_COLUMN = "Zeit (Europe/Vienna)"
RADON_SUFFIX = " – Radon (Bq/m³)"
UPTIME_SUFFIX = " – Betriebszeit (min)"
KITCHEN_CO2_COLUMN = "Kueche (Luft) – CO₂ (ppm)"

# Display name -> name used in the CSV header.
ROOMS = {
    "Büro": "Buero",
    "Küche": "Kueche",
    "Küche-Sockel": "Kueche - Sockel",
    "Schlafzimmer": "Schlafzimmer",
    "Technikraum": "Technikraum",
    "Werkstatt": "Werkstatt",
    "Wohnzimmer": "Wohnzimmer",
}
# The two groups behave differently (correlation inside a group > 0.8, between them ~0.55).
LIVING_ROOMS = ["Büro", "Küche", "Küche-Sockel", "Schlafzimmer", "Wohnzimmer"]
UTILITY_ROOMS = ["Technikraum", "Werkstatt"]

# A sensor reports 0 Bq/m³ while it warms up after a restart. These are not measurements.
RESTART_WINDOW_MIN = 90

# Days on which the house was empty all day (found via CO₂, see docs/ergebnisse-sichtung.md).
VACATION_FIRST_DAY = date(2026, 8, 1)
VACATION_LAST_DAY = date(2026, 8, 6)
VACATION_CHART_START = datetime(2026, 7, 29)
VACATION_CHART_END = datetime(2026, 8, 9)

# Assumed start of the ventilation system (drop in the kitchen data, not confirmed).
VENTILATION_START_DAY = date(2026, 3, 31)
VENTILATION_CHART_LAST_DAY = date(2026, 4, 20)
VENTILATION_COMPARE_LAST_DAY = date(2026, 4, 30)

# Second day without residents (about 07:00 to 24:00), left out of the everyday room profiles.
ABSENCE_DAY = date(2026, 7, 20)
# A month with fewer hours is not compared (March has a single day after the ventilation start).
MIN_HOURS_PER_MONTH = 240

HIGH_LEVEL = 100
REFERENCE_LEVEL = 300  # Austrian reference level, annual mean in Bq/m³

Points = list[tuple[datetime, float]]
HourlySeries = dict[datetime, float]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def extract_points(rows: list[dict[str, str]], column: str) -> Points:
    """Return (local time, value) for every row where the column is filled."""
    points: Points = []
    for row in rows:
        cell = row[column]
        if cell == "":
            continue
        points.append((datetime.fromisoformat(row[LOCAL_TIME_COLUMN]), float(cell)))
    return points


def is_restart_zero(radon: float, uptime_cell: str) -> bool:
    if radon != 0 or uptime_cell == "":
        return False
    return float(uptime_cell) <= RESTART_WINDOW_MIN


def extract_radon(rows: list[dict[str, str]], csv_room: str) -> Points:
    """Radon values of one room without the zeros reported right after a restart."""
    radon_column = csv_room + RADON_SUFFIX
    uptime_column = csv_room + UPTIME_SUFFIX
    points: Points = []
    for row in rows:
        cell = row[radon_column]
        if cell == "":
            continue
        # The bedroom sensor is a different device type and has no uptime column.
        uptime_cell = row.get(uptime_column, "")
        if is_restart_zero(float(cell), uptime_cell):
            continue
        points.append((datetime.fromisoformat(row[LOCAL_TIME_COLUMN]), float(cell)))
    return points


def hourly_means(points: Points) -> HourlySeries:
    groups: dict[datetime, list[float]] = defaultdict(list)
    for time, value in points:
        groups[time.replace(minute=0, second=0, microsecond=0)].append(value)
    return {hour: fmean(values) for hour, values in groups.items()}


def daily_means(points: Points) -> dict[date, float]:
    groups: dict[date, list[float]] = defaultdict(list)
    for time, value in points:
        groups[time.date()].append(value)
    return {day: fmean(values) for day, values in groups.items()}


def mean_across(series_list: list[dict], key: object) -> float | None:
    """Mean of all series that have a value for this key, None if none has one."""
    values = [series[key] for series in series_list if key in series]
    if not values:
        return None
    return fmean(values)


def is_vacation(hour: datetime) -> bool:
    return VACATION_FIRST_DAY <= hour.date() <= VACATION_LAST_DAY


def rank_rooms(hourly: dict[str, HourlySeries], hours: list[datetime]) -> list[dict]:
    """Statistics per room over the given hours, highest mean first."""
    ranking = []
    for room, series in hourly.items():
        values = [series[hour] for hour in hours]
        ranking.append(
            {
                "room": room,
                "mean": round(fmean(values)),
                "median": round(median(values)),
                "max": round(max(values)),
                "shareOverHigh": round(100 * sum(v > HIGH_LEVEL for v in values) / len(values), 1),
                "hoursOverReference": sum(v > REFERENCE_LEVEL for v in values),
            }
        )
    return sorted(ranking, key=lambda entry: entry["mean"], reverse=True)


def hour_of_day_profile(series_list: list[HourlySeries]) -> list[float]:
    """Mean value for each hour of the day (0-23), vacation excluded."""
    groups: dict[int, list[float]] = defaultdict(list)
    for series in series_list:
        for hour, value in series.items():
            if not is_vacation(hour):
                groups[hour.hour].append(value)
    return [round(fmean(groups[hour_of_day]), 1) for hour_of_day in range(24)]


def is_everyday(hour: datetime) -> bool:
    """True for hours with ventilation running and residents at home (as far as known)."""
    if hour.date() < VENTILATION_START_DAY or hour.date() == ABSENCE_DAY:
        return False
    return not is_vacation(hour)


def describe_room(room: str, series: HourlySeries) -> dict:
    """When one room is highest: by hour of the day and by month, everyday hours only."""
    by_hour: dict[int, list[float]] = defaultdict(list)
    by_month: dict[int, list[float]] = defaultdict(list)
    for hour, value in series.items():
        if is_everyday(hour):
            by_hour[hour.hour].append(value)
            by_month[hour.month].append(value)
    hour_means = {hour_of_day: fmean(values) for hour_of_day, values in by_hour.items()}
    month_means = {
        month: fmean(values) for month, values in by_month.items() if len(values) >= MIN_HOURS_PER_MONTH
    }
    peak_hour = max(hour_means, key=hour_means.get)
    low_hour = min(hour_means, key=hour_means.get)
    peak_month = max(month_means, key=month_means.get)
    everyday_values = [value for values in by_hour.values() for value in values]
    return {
        "room": room,
        "mean": round(fmean(everyday_values)),
        "peakHour": peak_hour,
        "peakHourMean": round(hour_means[peak_hour]),
        "lowHour": low_hour,
        "lowHourMean": round(hour_means[low_hour]),
        "peakMonth": peak_month,
        "peakMonthMean": round(month_means[peak_month]),
        "hoursOverHigh": sum(value > HIGH_LEVEL for value in everyday_values),
    }


def date_range(first: date, last: date) -> list[date]:
    day_count = (last - first).days + 1
    return [first + timedelta(days=offset) for offset in range(day_count)]


def hour_range(start: datetime, end: datetime) -> list[datetime]:
    hour_count = int((end - start).total_seconds() // 3600)
    return [start + timedelta(hours=offset) for offset in range(hour_count)]


def rounded(value: float | None) -> float | None:
    return None if value is None else round(value, 1)


def build_data(rows: list[dict[str, str]]) -> dict:
    radon = {room: extract_radon(rows, csv_room) for room, csv_room in ROOMS.items()}
    hourly = {room: hourly_means(points) for room, points in radon.items()}
    daily = {room: daily_means(points) for room, points in radon.items()}
    kitchen_co2 = hourly_means(extract_points(rows, KITCHEN_CO2_COLUMN))

    living_hourly = [hourly[room] for room in LIVING_ROOMS]
    utility_hourly = [hourly[room] for room in UTILITY_ROOMS]
    living_daily = [daily[room] for room in LIVING_ROOMS]
    utility_daily = [daily[room] for room in UTILITY_ROOMS]

    first_time = datetime.fromisoformat(rows[0][LOCAL_TIME_COLUMN])
    last_time = datetime.fromisoformat(rows[-1][LOCAL_TIME_COLUMN])
    days = date_range(first_time.date(), last_time.date())

    # Rooms are only comparable in hours where all seven sensors measured.
    common_hours = sorted(set.intersection(*(set(series) for series in hourly.values())))
    everyday_hours = [hour for hour in common_hours if not is_vacation(hour)]
    vacation_hours = [hour for hour in common_hours if is_vacation(hour)]

    everyday_living = [mean_across(living_hourly, hour) for hour in everyday_hours]
    vacation_living = [mean_across(living_hourly, hour) for hour in vacation_hours]

    vacation_chart_hours = hour_range(VACATION_CHART_START, VACATION_CHART_END)
    ventilation_days = date_range(days[0], VENTILATION_CHART_LAST_DAY)
    kitchen_before = [
        value for time, value in radon["Küche"] if time.date() < VENTILATION_START_DAY
    ]
    kitchen_after = [
        value
        for time, value in radon["Küche"]
        if VENTILATION_START_DAY <= time.date() <= VENTILATION_COMPARE_LAST_DAY
    ]

    return {
        "meta": {
            "rowCount": len(rows),
            "firstDay": days[0].isoformat(),
            "lastDay": days[-1].isoformat(),
            "dayCount": len(days),
            "commonHourCount": len(common_hours),
            "referenceLevel": REFERENCE_LEVEL,
            "highLevel": HIGH_LEVEL,
        },
        "kpis": {
            "everydayLivingMean": round(fmean(everyday_living)),
            "vacationLivingMean": round(fmean(vacation_living)),
            "vacationFactor": round(fmean(vacation_living) / fmean(everyday_living), 1),
            "kitchenBeforeVentilation": round(fmean(kitchen_before)),
            "kitchenAfterVentilation": round(fmean(kitchen_after)),
        },
        "daily": {
            "days": [day.isoformat() for day in days],
            "living": [rounded(mean_across(living_daily, day)) for day in days],
            "utility": [rounded(mean_across(utility_daily, day)) for day in days],
        },
        "vacation": {
            "hours": [hour.isoformat() for hour in vacation_chart_hours],
            "living": [rounded(mean_across(living_hourly, h)) for h in vacation_chart_hours],
            "utility": [rounded(mean_across(utility_hourly, h)) for h in vacation_chart_hours],
            "kitchenCo2": [rounded(kitchen_co2.get(h)) for h in vacation_chart_hours],
        },
        "ranking": {
            "everyday": rank_rooms(hourly, everyday_hours),
            "vacation": rank_rooms(hourly, vacation_hours),
            "everydayHourCount": len(everyday_hours),
            "vacationHourCount": len(vacation_hours),
        },
        "ventilation": {
            "days": [day.isoformat() for day in ventilation_days],
            "kitchen": [rounded(daily["Küche"].get(day)) for day in ventilation_days],
            "startDay": VENTILATION_START_DAY.isoformat(),
        },
        "roomProfiles": sorted(
            (describe_room(room, series) for room, series in hourly.items()),
            key=lambda profile: profile["mean"],
            reverse=True,
        ),
        "hourOfDay": {
            "living": hour_of_day_profile(living_hourly),
            "utility": hour_of_day_profile(utility_hourly),
        },
    }


def main() -> None:
    data = build_data(read_rows(CSV_PATH))
    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    # A .js file instead of .json: the page can then be opened by double-click (file://),
    # where the browser blocks fetch() of local JSON files.
    json_text = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    OUTPUT_PATH.write_text(f"window.RADON_DATA = {json_text};\n", encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH.relative_to(PROJECT_DIR)} ({OUTPUT_PATH.stat().st_size} bytes)")
    print(json.dumps(data["kpis"], ensure_ascii=False))


if __name__ == "__main__":
    main()
