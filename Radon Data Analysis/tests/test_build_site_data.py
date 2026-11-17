"""Tests for scripts/build_site_data.py.

Run from the project folder:
    python3.12 -m unittest discover tests
"""

import sys
import unittest
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import build_site_data as site  # noqa: E402  (import needs the path line above)

KITCHEN_RADON = "Kueche" + site.RADON_SUFFIX
KITCHEN_UPTIME = "Kueche" + site.UPTIME_SUFFIX


def make_row(time: str, radon: str, uptime: str) -> dict[str, str]:
    return {site.LOCAL_TIME_COLUMN: time, KITCHEN_RADON: radon, KITCHEN_UPTIME: uptime}


class RestartZeroTests(unittest.TestCase):
    def test_zero_right_after_restart_is_artifact(self) -> None:
        self.assertTrue(site.is_restart_zero(0.0, "5"))

    def test_zero_at_end_of_window_is_artifact(self) -> None:
        self.assertTrue(site.is_restart_zero(0.0, str(site.RESTART_WINDOW_MIN)))

    def test_zero_long_after_restart_is_kept(self) -> None:
        self.assertFalse(site.is_restart_zero(0.0, "5000"))

    def test_real_value_after_restart_is_kept(self) -> None:
        self.assertFalse(site.is_restart_zero(12.0, "5"))

    def test_sensor_without_uptime_is_kept(self) -> None:
        self.assertFalse(site.is_restart_zero(0.0, ""))


class ExtractRadonTests(unittest.TestCase):
    def test_skips_empty_cells_and_restart_zeros(self) -> None:
        rows = [
            make_row("2026-04-01 10:00:00", "40.0", "500"),
            make_row("2026-04-01 10:10:00", "", ""),
            make_row("2026-04-01 10:20:00", "0.0", "3"),
            make_row("2026-04-01 10:30:00", "0.0", "700"),
        ]
        points = site.extract_radon(rows, "Kueche")
        self.assertEqual([value for _, value in points], [40.0, 0.0])
        self.assertEqual(points[0][0], datetime(2026, 4, 1, 10, 0))


class MeanTests(unittest.TestCase):
    def setUp(self) -> None:
        self.points = [
            (datetime(2026, 4, 1, 10, 5), 10.0),
            (datetime(2026, 4, 1, 10, 55), 30.0),
            (datetime(2026, 4, 1, 11, 0), 50.0),
            (datetime(2026, 4, 2, 0, 0), 70.0),
        ]

    def test_hourly_means_group_by_full_hour(self) -> None:
        hourly = site.hourly_means(self.points)
        self.assertEqual(hourly[datetime(2026, 4, 1, 10)], 20.0)
        self.assertEqual(hourly[datetime(2026, 4, 1, 11)], 50.0)

    def test_daily_means_group_by_day(self) -> None:
        daily = site.daily_means(self.points)
        self.assertEqual(daily[date(2026, 4, 1)], 30.0)
        self.assertEqual(daily[date(2026, 4, 2)], 70.0)

    def test_mean_across_ignores_series_without_value(self) -> None:
        self.assertEqual(site.mean_across([{"a": 10.0}, {"a": 30.0}, {"b": 99.0}], "a"), 20.0)

    def test_mean_across_returns_none_without_any_value(self) -> None:
        self.assertIsNone(site.mean_across([{"a": 10.0}], "b"))


class RankingTests(unittest.TestCase):
    def test_rooms_are_sorted_by_mean_and_counted_against_levels(self) -> None:
        hours = [datetime(2026, 6, 1, hour) for hour in range(4)]
        hourly = {
            "low": dict(zip(hours, [10.0, 20.0, 30.0, 40.0])),
            "high": dict(zip(hours, [50.0, 150.0, 350.0, 450.0])),
        }
        ranking = site.rank_rooms(hourly, hours)
        self.assertEqual([entry["room"] for entry in ranking], ["high", "low"])
        self.assertEqual(ranking[0]["mean"], 250)
        self.assertEqual(ranking[0]["max"], 450)
        self.assertEqual(ranking[0]["shareOverHigh"], 75.0)
        self.assertEqual(ranking[0]["hoursOverReference"], 2)
        self.assertEqual(ranking[1]["hoursOverReference"], 0)


class PeriodTests(unittest.TestCase):
    def test_vacation_includes_first_and_last_day(self) -> None:
        self.assertTrue(site.is_vacation(datetime(2026, 8, 1, 0)))
        self.assertTrue(site.is_vacation(datetime(2026, 8, 6, 23)))

    def test_vacation_excludes_days_around_it(self) -> None:
        self.assertFalse(site.is_vacation(datetime(2026, 7, 31, 23)))
        self.assertFalse(site.is_vacation(datetime(2026, 8, 7, 0)))

    def test_hour_of_day_profile_leaves_out_vacation(self) -> None:
        series = {datetime(2026, 6, 1, 6): 40.0, datetime(2026, 6, 2, 6): 60.0, datetime(2026, 8, 3, 6): 900.0}
        for hour in range(24):
            series.setdefault(datetime(2026, 6, 1, hour), 10.0)
        profile = site.hour_of_day_profile([series])
        self.assertEqual(len(profile), 24)
        self.assertEqual(profile[6], 50.0)

    def test_ranges_have_expected_length(self) -> None:
        self.assertEqual(len(site.date_range(date(2026, 3, 30), date(2026, 4, 2))), 4)
        self.assertEqual(len(site.hour_range(datetime(2026, 8, 1), datetime(2026, 8, 2))), 24)


class RoomProfileTests(unittest.TestCase):
    def test_everyday_excludes_time_before_ventilation_absence_and_vacation(self) -> None:
        self.assertFalse(site.is_everyday(datetime(2026, 3, 30, 12)))
        self.assertFalse(site.is_everyday(datetime(2026, 7, 20, 12)))
        self.assertFalse(site.is_everyday(datetime(2026, 8, 3, 12)))
        self.assertTrue(site.is_everyday(datetime(2026, 6, 1, 12)))

    def test_describe_room_finds_peak_hour_and_month(self) -> None:
        series: dict[datetime, float] = {}
        for day in range(1, 21):
            for hour in range(24):
                # June: 20 everywhere, 80 at 6 o'clock. September: 10 everywhere.
                series[datetime(2026, 6, day, hour)] = 80.0 if hour == 6 else 20.0
                series[datetime(2026, 9, day, hour)] = 10.0
        # Extreme values that must be ignored: vacation and a month with too few hours.
        series[datetime(2026, 8, 3, 12)] = 900.0
        series[datetime(2026, 10, 1, 12)] = 700.0
        profile = site.describe_room("test", series)
        self.assertEqual(profile["peakHour"], 6)
        self.assertEqual(profile["peakHourMean"], 45)
        self.assertEqual(profile["peakMonth"], 6)
        self.assertEqual(profile["peakMonthMean"], 22)
        self.assertEqual(profile["hoursOverHigh"], 1)


if __name__ == "__main__":
    unittest.main()
