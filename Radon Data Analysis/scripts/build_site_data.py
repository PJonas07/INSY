"""Build website/data.js from the raw radon CSV.

The website only draws charts. Every number it shows is calculated here, so the
calculation can be read and tested in one place.

Run from the project folder:
    python3.12 scripts/build_site_data.py
"""

from __future__ import annotations

import csv
import json
import math
from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path
from statistics import fmean, linear_regression, median

PROJECT_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = PROJECT_DIR / "Dataset" / "radon_sample_data.csv"
OUTPUT_PATH = PROJECT_DIR / "website" / "data.js"

LOCAL_TIME_COLUMN = "Zeit (Europe/Vienna)"
RADON_SUFFIX = " – Radon (Bq/m³)"
UPTIME_SUFFIX = " – Betriebszeit (min)"
KITCHEN_CO2_COLUMN = "Kueche (Luft) – CO₂ (ppm)"
KITCHEN_TEMPERATURE_COLUMN = "Kueche (Luft) – Temperatur innen (°C)"
OUTDOOR_TEMPERATURE_COLUMN = "Wetter – Temperatur 2 m (°C)"

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

# From this day the windows were tilted (confirmed by the owner). The living rooms drop,
# the days before have only a few sensors and closed windows.
WINDOWS_TILTED_DAY = date(2026, 3, 31)

# The ventilation system was installed on this day (confirmed by the owner). It keeps the
# whole house at a slight overpressure, so no radon flows in from the ground.
VENTILATION_START_DAY = date(2026, 8, 24)
# Two weeks on each side: after the vacation and its after-effects, no other known change.
VENTILATION_COMPARE_DAYS = 14
VENTILATION_CHART_FIRST_DAY = date(2026, 8, 10)
VENTILATION_CHART_LAST_DAY = date(2026, 9, 20)

# Second day without residents (about 07:00 to 24:00), left out of the everyday room profiles.
ABSENCE_DAY = date(2026, 7, 20)
# A month with fewer hours is not compared (March has a single day with tilted windows).
MIN_HOURS_PER_MONTH = 240

# ---- House model: radon in a closed house behaves like a charging capacitor.
# dC/dt = entry - (air exchange + decay) * C  ->  C(t) = end - (end - start) * e^(-rate * t)
RADON_HALF_LIFE_HOURS = 3.8235 * 24
RADON_DECAY_PER_HOUR = math.log(2) / RADON_HALF_LIFE_HOURS
# Owner: three floors with 90 m² each, 2.5 m room height.
HOUSE_VOLUME_M3 = 3 * 90 * 2.5
# House empty, windows closed, no ventilation yet. Times from the 10-minute CO₂ data.
EMPTY_HOUSE_START = datetime(2026, 7, 31, 6)
EMPTY_HOUSE_END = datetime(2026, 8, 6, 20)
# After the return the windows were opened: the "capacitor" discharges within hours.
DISCHARGE_HOURS = 4
MODEL_CHART_HOURS = 240
# The rate is searched on a logarithmic grid between these values (per hour).
FIT_MIN_RATE = 0.001
FIT_MAX_RATE = 10.0
FIT_STEPS = 2000
# Typical winter day for the estimate.
WINTER_OUTDOOR_C = 0.0

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


def bucket_means(points: Points, minutes: int) -> HourlySeries:
    """Mean per time slot of the given length, e.g. 10:00-10:09 for minutes=10."""
    groups: dict[datetime, list[float]] = defaultdict(list)
    for time, value in points:
        slot_minute = time.minute - time.minute % minutes
        groups[time.replace(minute=slot_minute, second=0, microsecond=0)].append(value)
    return {slot: fmean(values) for slot, values in groups.items()}


def hourly_means(points: Points) -> HourlySeries:
    return bucket_means(points, 60)


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
    """True for hours with tilted windows or ventilation and residents at home (as far as known)."""
    if hour.date() < WINDOWS_TILTED_DAY or hour.date() == ABSENCE_DAY:
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


def compare_ventilation(daily: dict[str, dict[date, float]], rooms: list[str]) -> dict:
    """Mean of the daily means before and after the ventilation start, same number of days."""
    before_days = date_range(VENTILATION_START_DAY - timedelta(days=VENTILATION_COMPARE_DAYS),
                             VENTILATION_START_DAY - timedelta(days=1))
    after_days = date_range(VENTILATION_START_DAY,
                            VENTILATION_START_DAY + timedelta(days=VENTILATION_COMPARE_DAYS - 1))
    series_list = [daily[room] for room in rooms]
    before = [mean_across(series_list, day) for day in before_days]
    after = [mean_across(series_list, day) for day in after_days]
    return {
        "before": round(fmean(value for value in before if value is not None)),
        "after": round(fmean(value for value in after if value is not None)),
        "beforeFirstDay": before_days[0].isoformat(),
        "afterLastDay": after_days[-1].isoformat(),
    }


def exponential_curve(hours: float, start: float, end: float, rate: float) -> float:
    """Capacitor curve: starts at `start` and approaches `end`; 63 % of the way after 1/rate hours."""
    return end - (end - start) * math.exp(-rate * hours)


def hours_until(level: float, start: float, end: float, rate: float) -> float | None:
    """When the capacitor curve reaches the level; None if it never gets there."""
    if not start < level < end:
        return None
    return -math.log((end - level) / (end - start)) / rate


def required_hours_until(level: float, start: float, end: float, rate: float) -> float:
    """Like hours_until, but stops with a clear message if the curve never reaches the level."""
    hours = hours_until(level, start, end, rate)
    if hours is None:
        raise ValueError(f"Curve from {start:.0f} to {end:.0f} never reaches {level} Bq/m³")
    return hours


def fit_exponential(points: list[tuple[float, float]]) -> dict:
    """Find start, end and rate of the capacitor curve that fits the points best.

    For a fixed rate the curve is a straight line in x = 1 - e^(-rate * t), so start and end
    follow from an ordinary linear regression. The rate itself is found by trying many values.
    """
    values = [value for _, value in points]
    best: tuple[float, float, float, float] | None = None
    for step in range(FIT_STEPS + 1):
        rate = FIT_MIN_RATE * (FIT_MAX_RATE / FIT_MIN_RATE) ** (step / FIT_STEPS)
        xs = [1 - math.exp(-rate * hours) for hours, _ in points]
        slope, intercept = linear_regression(xs, values)
        error = sum((intercept + slope * x - value) ** 2 for x, value in zip(xs, values))
        if best is None or error < best[0]:
            best = (error, rate, intercept, intercept + slope)
    error, rate, start, end = best
    return {"rate": rate, "start": start, "end": end, "rmse": math.sqrt(error / len(points))}


def describe_house(fit: dict) -> dict:
    """Translate the fitted curve into air exchange and radon entry (mass balance at the end value)."""
    return {
        "tauHours": round(1 / fit["rate"]),
        "start": round(fit["start"]),
        "end": round(fit["end"]),
        "rmse": round(fit["rmse"], 1),
        "airExchangePerHour": round(fit["rate"] - RADON_DECAY_PER_HOUR, 4),
        "entryPerM3Hour": round(fit["rate"] * fit["end"], 1),
    }


def group_points(group_series: list[HourlySeries], start: datetime, end: datetime) -> list[tuple[float, float]]:
    """(hours since start, mean over the group) for every slot between start and end."""
    points = []
    for slot in sorted({slot for series in group_series for slot in series}):
        if start <= slot < end:
            points.append(((slot - start).total_seconds() / 3600, mean_across(group_series, slot)))
    return points


def winter_factor(slope: float, intercept: float, indoor: float, outdoor: float) -> float:
    """How much more radon enters at the given outdoor temperature than without temperature difference.

    The regression radon = intercept + slope * outdoor comes from the days with ventilation.
    The stack effect pulls soil air into the house in proportion to indoor minus outdoor temperature.
    """
    without_difference = intercept + slope * indoor
    increase_per_kelvin = -slope / without_difference
    return 1 + increase_per_kelvin * (indoor - outdoor)


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
    ventilation_days = date_range(VENTILATION_CHART_FIRST_DAY, VENTILATION_CHART_LAST_DAY)
    house_model = build_house_model(rows, radon, living_hourly, utility_hourly, living_daily, utility_daily)

    return {
        "meta": {
            "rowCount": len(rows),
            "firstDay": days[0].isoformat(),
            "lastDay": days[-1].isoformat(),
            "dayCount": len(days),
            "commonHourCount": len(common_hours),
            "referenceLevel": REFERENCE_LEVEL,
            "highLevel": HIGH_LEVEL,
            "windowsTiltedDay": WINDOWS_TILTED_DAY.isoformat(),
        },
        "kpis": {
            "everydayLivingMean": round(fmean(everyday_living)),
            "vacationLivingMean": round(fmean(vacation_living)),
            "vacationFactor": round(fmean(vacation_living) / fmean(everyday_living), 1),
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
            "living": [rounded(mean_across(living_daily, day)) for day in ventilation_days],
            "utility": [rounded(mean_across(utility_daily, day)) for day in ventilation_days],
            "startDay": VENTILATION_START_DAY.isoformat(),
            "livingCompare": compare_ventilation(daily, LIVING_ROOMS),
            "utilityCompare": compare_ventilation(daily, UTILITY_ROOMS),
        },
        "roomProfiles": sorted(
            (describe_room(room, series) for room, series in hourly.items()),
            key=lambda profile: profile["mean"],
            reverse=True,
        ),
        "houseModel": house_model,
        "hourOfDay": {
            "living": hour_of_day_profile(living_hourly),
            "utility": hour_of_day_profile(utility_hourly),
        },
    }


def build_house_model(
    rows: list[dict[str, str]],
    radon: dict[str, Points],
    living_hourly: list[HourlySeries],
    utility_hourly: list[HourlySeries],
    living_daily: list[dict[date, float]],
    utility_daily: list[dict[date, float]],
) -> dict:
    """Capacitor model of the empty house in summer and an estimate for winter."""
    living_charge = fit_exponential(group_points(living_hourly, EMPTY_HOUSE_START, EMPTY_HOUSE_END))
    utility_charge = fit_exponential(group_points(utility_hourly, EMPTY_HOUSE_START, EMPTY_HOUSE_END))
    # The discharge takes about an hour, so it needs the 10-minute values.
    living_ten_minutes = [bucket_means(radon[room], 10) for room in LIVING_ROOMS]
    discharge_end = EMPTY_HOUSE_END + timedelta(hours=DISCHARGE_HOURS)
    discharge = fit_exponential(group_points(living_ten_minutes, EMPTY_HOUSE_END, discharge_end))

    # With ventilation: daily radon against daily outdoor temperature.
    outdoor_daily = daily_means(extract_points(rows, OUTDOOR_TEMPERATURE_COLUMN))
    indoor_daily = daily_means(extract_points(rows, KITCHEN_TEMPERATURE_COLUMN))
    ventilated_days = [day for day in sorted(outdoor_daily) if day >= VENTILATION_START_DAY]
    temperatures = [outdoor_daily[day] for day in ventilated_days]
    living_slope, living_intercept = linear_regression(
        temperatures, [mean_across(living_daily, day) for day in ventilated_days])
    utility_slope, utility_intercept = linear_regression(
        temperatures, [mean_across(utility_daily, day) for day in ventilated_days])
    indoor = fmean(indoor_daily[day] for day in ventilated_days if day in indoor_daily)
    factor = winter_factor(living_slope, living_intercept, indoor, WINTER_OUTDOOR_C)
    winter_end = living_charge["end"] * factor

    chart_hours = list(range(MODEL_CHART_HOURS + 1))
    measured = dict(group_points(living_hourly, EMPTY_HOUSE_START, EMPTY_HOUSE_END))
    start = living_charge["start"]
    return {
        "volumeM3": HOUSE_VOLUME_M3,
        "decayPerHour": round(RADON_DECAY_PER_HOUR, 5),
        "living": describe_house(living_charge),
        "utility": describe_house(utility_charge),
        "entryHousePerHour": round(living_charge["rate"] * living_charge["end"] * HOUSE_VOLUME_M3, -2),
        "dischargeTauMinutes": round(60 / discharge["rate"]),
        "dischargeAirExchangePerHour": round(discharge["rate"] - RADON_DECAY_PER_HOUR, 1),
        "winter": {
            "outdoor": WINTER_OUTDOOR_C,
            "indoor": round(indoor, 1),
            "measuredOutdoorMin": round(min(temperatures), 1),
            "measuredOutdoorMax": round(max(temperatures), 1),
            "livingSlope": round(living_slope, 2),
            "utilitySlope": round(utility_slope, 2),
            "factor": round(factor, 1),
            "closedEnd": round(winter_end, -1),
            "closedHoursTo300": round(required_hours_until(REFERENCE_LEVEL, start, winter_end, living_charge["rate"])),
            "summerHoursTo300": round(required_hours_until(REFERENCE_LEVEL, start, living_charge["end"], living_charge["rate"])),
            "ventilatedLiving": round(living_intercept + living_slope * WINTER_OUTDOOR_C),
            "ventilatedUtility": round(utility_intercept + utility_slope * WINTER_OUTDOOR_C),
        },
        "chart": {
            "hours": chart_hours,
            "measured": [rounded(measured.get(float(hour))) for hour in chart_hours],
            "summer": [rounded(exponential_curve(h, start, living_charge["end"], living_charge["rate"])) for h in chart_hours],
            "winter": [rounded(exponential_curve(h, start, winter_end, living_charge["rate"])) for h in chart_hours],
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
