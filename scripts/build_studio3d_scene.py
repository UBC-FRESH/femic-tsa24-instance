#!/usr/bin/env python3
"""Build the TSA 24 studio-3D scene pack.

TSA 24 has 458,708 blocks and no local DEM/CHM.  The scene therefore uses public
SRTM terrain and aggregates blocks into 1 km forest cells.  It is a large-landscape
LOD screen, not an all-tree render.
"""

from __future__ import annotations

import argparse
import datetime as dt
import gzip
import json
import math
import sys
import urllib.request
from collections import defaultdict
from pathlib import Path
from typing import Any

import fiona
import numpy as np
import pandas as pd
from pyproj import Transformer
from rasterio.features import rasterize
from rasterio.transform import from_origin
from shapely.geometry import Polygon, shape
from shapely.geometry.base import BaseGeometry

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = Path("/srv/shared-data/gep/ws4")
FRESH_URBAN_SRC = WORKSPACE / "fresh-urban-forest-lab" / "src"
GEOMETRY = ROOT / "runtime/geometry/tsa24-blocks-overview.geojson"
SCHEDULE = ROOT / "runtime/tsa24-ltsy-schedule.csv"
OUT = ROOT / "planning/studio3d/tsa24_scene.json"
SRTM_CACHE = ROOT / "data/downloads/srtm"

SOURCE_CRS = "EPSG:3005"
SCENE_CRS = "EPSG:3157"
GRID_RESOLUTION_M = 300.0
CELL_SIZE_M = 1000.0
TREATMENT_REMOVAL = {"CC": 1.0, "CT35": 0.35, "CT40": 0.40, "CT45": 0.45}


def _download_tiles(bounds: tuple[float, float, float, float]) -> dict[str, np.ndarray]:
    left, bottom, right, top = bounds
    lat_min = max(47, math.floor(bottom) - 1)
    lat_max = min(55, math.floor(top) + 1)
    lon_min = max(-132, math.floor(left) - 1)
    lon_max = min(-122, math.floor(right) + 1)
    SRTM_CACHE.mkdir(parents=True, exist_ok=True)
    tiles: dict[str, np.ndarray] = {}
    for lat in range(lat_min, lat_max + 1):
        for lon in range(lon_min, lon_max + 1):
            name = f"N{lat:02d}W{abs(lon):03d}"
            hgt = SRTM_CACHE / f"{name}.hgt"
            if not hgt.is_file():
                url = f"https://s3.amazonaws.com/elevation-tiles-prod/skadi/{name[:3]}/{name}.hgt.gz"
                print(f"download {name} …", flush=True)
                with urllib.request.urlopen(url, timeout=120) as response:
                    hgt.write_bytes(gzip.decompress(response.read()))
            array = (
                np.frombuffer(hgt.read_bytes(), dtype=">i2")
                .reshape((3601, 3601))
                .astype(np.float32)
            )
            array[array <= -1000] = np.nan
            tiles[name] = array
    return tiles


def _sample_tiles(
    tiles: dict[str, np.ndarray], lon: np.ndarray, lat: np.ndarray
) -> np.ndarray:
    result = np.full(lon.shape, np.nan, dtype=np.float64)
    for name, tile in tiles.items():
        tile_lat = int(name[1:3])
        west = -int(name[4:7])
        mask = (
            (lat >= tile_lat)
            & (lat <= tile_lat + 1)
            & (lon >= west)
            & (lon <= west + 1)
        )
        if not mask.any():
            continue
        rows = np.clip((tile_lat + 1.0 - lat[mask]) * 3600.0, 0, 3600)
        cols = np.clip((lon[mask] - west) * 3600.0, 0, 3600)
        r0 = np.floor(rows).astype(int)
        c0 = np.floor(cols).astype(int)
        r1 = np.minimum(r0 + 1, 3600)
        c1 = np.minimum(c0 + 1, 3600)
        tr = rows - r0
        tc = cols - c0
        a = tile[r0, c0] * (1 - tr) + tile[r1, c0] * tr
        b = tile[r0, c1] * (1 - tr) + tile[r1, c1] * tr
        result[mask] = a * (1 - tc) + b * tc
    return result


def _height_from_age(age: float) -> float:
    years = max(1.0, float(age) if math.isfinite(float(age)) else 1.0)
    return min(
        34.0,
        1.5
        + 31.0
        * (1.0 - math.exp(-years / 52.0))
        * (1.0 - 0.18 * math.exp(-years / 8.0)),
    )


def _solar(lon: float, lat: float) -> dict[str, Any]:
    if FRESH_URBAN_SRC.is_dir() and str(FRESH_URBAN_SRC) not in sys.path:
        sys.path.insert(0, str(FRESH_URBAN_SRC))
    try:
        from fresh_urban_forest.solar import parse_clock, solar_position, timezone
    except Exception:  # noqa: BLE001 - optional solar engine
        return {"tracks": []}
    zone = timezone()
    tracks: list[dict[str, Any]] = []
    for date_text in ("2026-06-21", "2026-09-21", "2026-12-21"):
        date = dt.date.fromisoformat(date_text)
        samples = []
        for clock in ("08:00", "10:00", "12:00", "14:00", "16:00", "18:00"):
            when = dt.datetime.combine(date, parse_clock(clock), tzinfo=zone)
            pos = solar_position(when, lon, lat)
            samples.append(
                {
                    "time": clock,
                    "when": when.isoformat(),
                    "altitude_deg": round(pos.altitude_deg, 3),
                    "azimuth_deg": round(pos.azimuth_deg, 3),
                    "is_daylight": bool(pos.is_daylight),
                }
            )
        tracks.append({"date": date_text, "samples": samples})
    return {
        "source": "fresh-urban-forest-lab NOAA solar-position engine",
        "timezone": str(zone),
        "tracks": tracks,
    }


def build(args: argparse.Namespace) -> dict[str, Any]:
    """Build the TSA 24 scene payload."""
    schedule = pd.read_csv(SCHEDULE)
    schedule["block_id"] = schedule["block_id"].astype(str)
    schedule = (
        schedule.sort_values("offset")
        .drop_duplicates("block_id", keep="first")
        .set_index("block_id")
    )

    cells: dict[tuple[int, int], dict[str, Any]] = defaultdict(
        lambda: {
            "area": 0.0,
            "age_area": 0.0,
            "age": 0.0,
            "count": 0,
            "treatment": "",
            "treat_year": None,
            "removal": 0.0,
        }
    )
    bounds = [math.inf, math.inf, -math.inf, -math.inf]
    to_scene = Transformer.from_crs(SOURCE_CRS, SCENE_CRS, always_xy=True)
    with fiona.open(GEOMETRY) as source:
        for feature in source:
            geom = shape(feature["geometry"])
            if geom.is_empty:
                continue
            props = feature["properties"]
            block_id = str(props.get("block_id"))
            area = float(props.get("area_ha") or 0.0)
            age = float(props.get("age") or 80.0)
            centroid = geom.centroid
            x, y = to_scene.transform(centroid.x, centroid.y)
            key = (math.floor(x / CELL_SIZE_M), math.floor(y / CELL_SIZE_M))
            cell = cells[key]
            cell["area"] += area
            cell["age_area"] += area * age
            cell["count"] += 1
            if block_id in schedule.index and not cell["treatment"]:
                scheduled = schedule.loc[block_id]
                treatment = str(scheduled.get("treatment", "") or "")
                try:
                    treat_year = round(float(scheduled.get("offset")))
                except (TypeError, ValueError):
                    treat_year = None
                cell["treatment"] = treatment
                cell["treat_year"] = treat_year
                cell["removal"] = TREATMENT_REMOVAL.get(treatment, 0.0)
            bounds[0] = min(bounds[0], x)
            bounds[1] = min(bounds[1], y)
            bounds[2] = max(bounds[2], x)
            bounds[3] = max(bounds[3], y)
    if not cells:
        raise RuntimeError("no TSA 24 blocks found")
    for cell in cells.values():
        cell["age"] = cell["age_area"] / max(cell["area"], 1e-9)

    left, bottom, right, top = bounds
    pad = 5000.0
    left -= pad
    right += pad
    bottom -= pad
    top += pad
    x0, y0 = left, bottom
    x1, y1 = right, top
    nx = max(2, round((x1 - x0) / GRID_RESOLUTION_M) + 1)
    ny = max(2, round((y1 - y0) / GRID_RESOLUTION_M) + 1)
    dx = (x1 - x0) / (nx - 1)
    dy = (y1 - y0) / (ny - 1)

    to_wgs = Transformer.from_crs(SCENE_CRS, "EPSG:4326", always_xy=True)
    xs = x0 + np.arange(nx) * dx
    zs = np.arange(ny) * dy
    xx, zz = np.meshgrid(xs, zs)
    yy = y1 - zz
    lon, lat = to_wgs.transform(xx, yy)
    tiles = _download_tiles(
        (
            float(np.nanmin(lon)),
            float(np.nanmin(lat)),
            float(np.nanmax(lon)),
            float(np.nanmax(lat)),
        )
    )
    elevations = _sample_tiles(tiles, lon, lat)
    elevations = np.where(np.isfinite(elevations), elevations, np.nan)
    if not np.isfinite(elevations).all():
        from scipy.ndimage import distance_transform_edt

        valid = np.isfinite(elevations)
        if valid.any():
            indices = distance_transform_edt(
                ~valid, return_distances=False, return_indices=True
            )
            elevations = elevations[tuple(indices)]
        else:
            elevations = np.zeros_like(elevations)

    blocks: list[dict[str, Any]] = []
    canopy_shapes: list[tuple[BaseGeometry, float]] = []
    for (cx, cz), cell in cells.items():
        area = max(0.01, cell["area"])
        age = max(1.0, cell["age"])
        height = _height_from_age(age)
        center_x = (cx + 0.5) * CELL_SIZE_M
        center_y = (cz + 0.5) * CELL_SIZE_M
        center_z = y1 - center_y
        half = CELL_SIZE_M * 0.5
        polygon = [
            [round(center_x - half - x0, 2), round(center_z - half, 2)],
            [round(center_x + half - x0, 2), round(center_z - half, 2)],
            [round(center_x + half - x0, 2), round(center_z + half, 2)],
            [round(center_x - half - x0, 2), round(center_z + half, 2)],
            [round(center_x - half - x0, 2), round(center_z - half, 2)],
        ]
        blocks.append(
            {
                "id": f"{cx}:{cz}",
                "polygon": polygon,
                "centroid": [round(center_x - x0, 2), round(center_z, 2)],
                "area_ha": round(area, 3),
                "density": 700.0,
                "height_m": round(height, 2),
                "volume_per_ha_m3": 0.0,
                "au_id": "",
                "species": [["CONIFER", 100.0]],
                "treatment": str(cell["treatment"]),
                "treat_year": cell["treat_year"],
                "removal": round(float(cell["removal"]), 3),
                "retention": round(1.0 - float(cell["removal"]), 3),
                "age": round(age, 1),
                "block_count": int(cell["count"]),
            }
        )
        canopy_shapes.append(
            (
                Polygon(
                    [
                        (center_x - half, center_y - half),
                        (center_x + half, center_y - half),
                        (center_x + half, center_y + half),
                        (center_x - half, center_y + half),
                    ]
                ),
                height,
            )
        )
    canopy_values = rasterize(
        canopy_shapes,
        out_shape=(ny, nx),
        transform=from_origin(x0, y1, dx, dy),
        fill=0.0,
        dtype="float32",
    )
    center_x = x0 + (x1 - x0) * 0.5
    center_y = y0 + (y1 - y0) * 0.5
    default = (
        min(
            blocks,
            key=lambda item: (
                (item["centroid"][0] - (center_x - x0)) ** 2
                + (item["centroid"][1] - (y1 - center_y)) ** 2
            ),
        )
        if blocks
        else None
    )
    lon_c, lat_c = to_wgs.transform(center_x, center_y)
    return {
        "schema": "ws4.studio3d.v1",
        "label": "TSA 24 · 3D landscape",
        "subtitle": "North Island TSA 24 · aggregated 1 km forest cells",
        "generated_utc": dt.datetime.now(dt.UTC).isoformat(),
        "crs": SCENE_CRS,
        "source_note": (
            "Terrain: public SRTM 1 arcsecond tiles. Forest: TSA 24 blocks aggregated "
            "to 1 km cells; heights are age-derived visual values because no local CHM is "
            "installed. Treatment: LT-SY schedule. All-tree rendering is disabled."
        ),
        "bounds": {
            "min_x": 0.0,
            "max_x": round(x1 - x0, 2),
            "min_z": 0.0,
            "max_z": round(y1 - y0, 2),
        },
        "terrain": {
            "x0": 0.0,
            "z0": 0.0,
            "dx": round(dx, 3),
            "dy": round(dy, 3),
            "nx": nx,
            "ny": ny,
            "values": np.round(elevations, 1).tolist(),
        },
        "canopy": {
            "x0": 0.0,
            "z0": 0.0,
            "dx": round(dx, 3),
            "dy": round(dy, 3),
            "nx": nx,
            "ny": ny,
            "values": np.round(canopy_values, 1).tolist(),
        },
        "synthetic_canopy": True,
        "blocks": blocks,
        "default_block": default["id"] if default else None,
        "default_center": default["centroid"] if default else [0.0, 0.0],
        "solar": _solar(float(lon_c), float(lat_c)),
        "light": None,
        "all_trees_default": False,
        "all_trees_available": False,
        "default_view_distance": 350.0,
        "default_shadows": False,
        "far_density": 0.2,
        "mid_density": 0.8,
        "far_point_size": 8.0,
        "mid_point_size": 5.0,
        "show_block_outlines": False,
        "method": {
            "terrain": "SRTM 1-arcsecond AWS terrain tiles sampled to local scene grid",
            "forest": "458,708 TSA 24 blocks aggregated to 1 km cells",
            "height": "age-derived visual curve; no CHM",
            "all_tree": "disabled for this landscape",
        },
    }


def main() -> None:
    """Command-line entry point."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=str(OUT))
    args = parser.parse_args()
    payload = build(args)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, separators=(",", ":")), encoding="utf-8")
    print(f"wrote {out} ({out.stat().st_size / 1_000_000:.1f} MB)")
    terrain = payload["terrain"]
    print(f"terrain {terrain['nx']}x{terrain['ny']} · {len(payload['blocks'])} cells")


if __name__ == "__main__":
    main()
