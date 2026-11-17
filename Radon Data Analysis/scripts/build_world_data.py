"""Build website/world.js (country outlines for the globe) from Dataset/countries-110m.json.

The source is the npm package world-atlas 2.0.2 (Natural Earth 1:110 million, public domain),
stored in TopoJSON. TopoJSON saves every border only once as an "arc"; a country lists the arcs
that make up its outline. This script turns that back into plain lists of [lon, lat] points.

Run from the project folder:
    python3.12 scripts/build_world_data.py
"""

from __future__ import annotations

import json
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
SOURCE_PATH = PROJECT_DIR / "Dataset" / "countries-110m.json"
OUTPUT_PATH = PROJECT_DIR / "website" / "world.js"
# One decimal place is about 11 km, finer than the globe can show.
COORDINATE_DECIMALS = 1

Point = list[float]
Ring = list[Point]


def decode_arcs(topology: dict) -> list[Ring]:
    """Arcs are stored as integer steps from the previous point; add them up and scale to degrees."""
    scale_x, scale_y = topology["transform"]["scale"]
    shift_x, shift_y = topology["transform"]["translate"]
    arcs = []
    for encoded in topology["arcs"]:
        x = y = 0
        points = []
        for step_x, step_y in encoded:
            x += step_x
            y += step_y
            points.append([x * scale_x + shift_x, y * scale_y + shift_y])
        arcs.append(points)
    return arcs


def build_ring(arc_indexes: list[int], arcs: list[Ring]) -> Ring:
    """Join arcs to one closed outline. A negative index ~i means arc i walked backwards."""
    ring: Ring = []
    for index in arc_indexes:
        arc = arcs[index] if index >= 0 else list(reversed(arcs[~index]))
        # Consecutive arcs share their end and start point; keep it only once.
        ring.extend(arc if not ring else arc[1:])
    return ring


def country_rings(geometry: dict, arcs: list[Ring]) -> list[Ring]:
    polygons = [geometry["arcs"]] if geometry["type"] == "Polygon" else geometry["arcs"]
    return [build_ring(ring, arcs) for polygon in polygons for ring in polygon]


def rounded_ring(ring: Ring) -> Ring:
    return [[round(lon, COORDINATE_DECIMALS), round(lat, COORDINATE_DECIMALS)] for lon, lat in ring]


def build_world(topology: dict) -> list[dict]:
    arcs = decode_arcs(topology)
    countries = []
    for geometry in topology["objects"]["countries"]["geometries"]:
        if "arcs" not in geometry:
            continue  # a few tiny territories have no outline at this scale
        rings = [rounded_ring(ring) for ring in country_rings(geometry, arcs)]
        countries.append({"name": geometry["properties"]["name"], "rings": rings})
    return countries


def main() -> None:
    topology = json.loads(SOURCE_PATH.read_text(encoding="utf-8"))
    countries = build_world(topology)
    json_text = json.dumps(countries, ensure_ascii=False, separators=(",", ":"))
    OUTPUT_PATH.write_text(f"window.WORLD_COUNTRIES = {json_text};\n", encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH.relative_to(PROJECT_DIR)} ({len(countries)} countries, {OUTPUT_PATH.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
