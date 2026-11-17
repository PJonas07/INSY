"""Tests for scripts/build_world_data.py.

Run from the project folder:
    python3.12 -m unittest discover tests
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import build_world_data as world  # noqa: E402  (import needs the path line above)

# Two arcs on a grid with step 1 degree, starting at (10, 20).
TOPOLOGY = {
    "transform": {"scale": [1, 1], "translate": [10, 20]},
    "arcs": [
        [[0, 0], [1, 0], [0, 1]],  # (10,20) -> (11,20) -> (11,21)
        [[1, 1], [-1, 0], [0, -1]],  # (11,21) -> (10,21) -> (10,20)
    ],
    "objects": {"countries": {"geometries": [
        {"type": "Polygon", "arcs": [[0, 1]], "properties": {"name": "Square"}},
        {"type": "MultiPolygon", "arcs": [[[~1, ~0]]], "properties": {"name": "Backwards"}},
        {"type": None, "properties": {"name": "No outline"}},
    ]}},
}


class WorldDataTests(unittest.TestCase):
    def test_decode_adds_up_steps_and_scales(self) -> None:
        arcs = world.decode_arcs(TOPOLOGY)
        self.assertEqual(arcs[0], [[10, 20], [11, 20], [11, 21]])
        self.assertEqual(arcs[1], [[11, 21], [10, 21], [10, 20]])

    def test_ring_joins_arcs_without_duplicate_points(self) -> None:
        ring = world.build_ring([0, 1], world.decode_arcs(TOPOLOGY))
        self.assertEqual(ring, [[10, 20], [11, 20], [11, 21], [10, 21], [10, 20]])

    def test_negative_index_walks_arc_backwards(self) -> None:
        ring = world.build_ring([~1], world.decode_arcs(TOPOLOGY))
        self.assertEqual(ring, [[10, 20], [10, 21], [11, 21]])

    def test_build_world_skips_geometry_without_outline(self) -> None:
        countries = world.build_world(TOPOLOGY)
        self.assertEqual([country["name"] for country in countries], ["Square", "Backwards"])
        self.assertEqual(len(countries[1]["rings"]), 1)


if __name__ == "__main__":
    unittest.main()
