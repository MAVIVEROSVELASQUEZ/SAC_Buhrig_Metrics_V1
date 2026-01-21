"""
03_generate_transversal_profiles.py
-----------------------------------

Generation of canyon-constrained transversal profiles perpendicular to
the submarine canyon thalweg.

For each point sampled every 2 km along the thalweg, this script attempts
to construct a transversal profile perpendicular to the local thalweg
direction.

Primary method:
- Edge-constrained transversal profiles intersecting both canyon margins
  (left and right edges) and extended 3 km beyond each margin.

Fallback method:
- For thalweg points where edge-constrained profiles cannot be defined,
  a fixed-length orthogonal profile (17 km total length) is generated.
  These fallback profiles ensure full spatial coverage and are explicitly
  flagged for posterior expert review and filtering.

This approach guarantees that all thalweg sampling points are associated
with a transversal geometry, while preserving a clear distinction between
fully constrained and fallback profiles for subsequent quality control
and metric computation.

---------------------------------------------------------------------
INPUTS
---------------------------------------------------------------------
- data/raw/SAC_Thalweg.shp
- data/processed/thalweg_points_2km.shp
- data/raw/SAC_Edge.shp

---------------------------------------------------------------------
OUTPUT
---------------------------------------------------------------------
- data/processed/SAC_transversal_profiles.shp

---------------------------------------------------------------------
AUTHOR
---------------------------------------------------------------------
Marco Antonio Viveros Velásquez
Project: SAC – Bührig Metrics Pipeline
"""

import geopandas as gpd
import numpy as np
from shapely.geometry import LineString
from shapely.ops import unary_union

# ------------------------------------------------------------
# Paths
# ------------------------------------------------------------
THALWEG_PATH = r"data/raw/SAC_Thalweg.shp"
POINTS_PATH  = r"data/processed/thalweg_points_2km.shp"
EDGE_PATH    = r"data/raw/SAC_Edge.shp"
OUTPUT_PATH  = r"data/processed/SAC_transversal_profiles.shp"

# ------------------------------------------------------------
# Parameters
# ------------------------------------------------------------
EXTRA_EXTENSION   = 3000.0     # meters beyond each canyon edge
TANGENT_DELTA     = 10.0       # meters for local tangent estimation
FALLBACK_HALF_LEN = 8500.0     # 17 km total fallback profile (±8.5 km)

# ------------------------------------------------------------
# Load data
# ------------------------------------------------------------
thalweg = gpd.read_file(THALWEG_PATH).geometry.iloc[0]
points  = gpd.read_file(POINTS_PATH)
edges   = gpd.read_file(EDGE_PATH)

edges_left  = edges[edges["LeftRight"] == "Left"].geometry
edges_right = edges[edges["LeftRight"] == "Right"].geometry

edge_left_union  = unary_union(edges_left)
edge_right_union = unary_union(edges_right)

profiles = []

# ------------------------------------------------------------
# Generate transversal profiles
# ------------------------------------------------------------
for _, row in points.iterrows():

    profile_id = int(row["profile_id"])
    center_pt  = row.geometry
    d_center   = row["distance_m"]

    # --- Tangent vector (local thalweg direction) ---
    d0 = max(d_center - TANGENT_DELTA, 0)
    d1 = min(d_center + TANGENT_DELTA, thalweg.length)

    p0 = thalweg.interpolate(d0)
    p1 = thalweg.interpolate(d1)

    dx = p1.x - p0.x
    dy = p1.y - p0.y
    norm = np.hypot(dx, dy)

    if norm == 0:
        continue

    dx /= norm
    dy /= norm

    # --- Normal vector (orthogonal direction) ---
    nx = -dy
    ny = dx

    # --- Long provisional profile ---
    provisional = LineString([
        (center_pt.x - nx * 20000, center_pt.y - ny * 20000),
        (center_pt.x + nx * 20000, center_pt.y + ny * 20000)
    ])

    # --- Intersections with canyon edges ---
    inter_left  = provisional.intersection(edge_left_union)
    inter_right = provisional.intersection(edge_right_union)

    # =========================================================
    # CASE 1: EDGE-CONSTRAINED PROFILE (preferred)
    # =========================================================
    if not inter_left.is_empty and not inter_right.is_empty:

        p_left  = inter_left.centroid
        p_right = inter_right.centroid

        start = (
            p_left.x  - nx * EXTRA_EXTENSION,
            p_left.y  - ny * EXTRA_EXTENSION
        )
        end = (
            p_right.x + nx * EXTRA_EXTENSION,
            p_right.y + ny * EXTRA_EXTENSION
        )

        profile = LineString([start, end])

        profiles.append({
            "profile_id": profile_id,
            "profile_type": "edge_constrained",
            "geometry": profile
        })

    # =========================================================
    # CASE 2: FALLBACK ORTHOGONAL PROFILE
    # =========================================================
    else:

        start = (
            center_pt.x - nx * FALLBACK_HALF_LEN,
            center_pt.y - ny * FALLBACK_HALF_LEN
        )
        end = (
            center_pt.x + nx * FALLBACK_HALF_LEN,
            center_pt.y + ny * FALLBACK_HALF_LEN
        )

        profile = LineString([start, end])

        profiles.append({
            "profile_id": profile_id,
            "profile_type": "fallback_orthogonal",
            "geometry": profile
        })

# ------------------------------------------------------------
# Save output
# ------------------------------------------------------------
gdf_profiles = gpd.GeoDataFrame(profiles, crs=points.crs)
gdf_profiles.to_file(OUTPUT_PATH)

print("==============================================")
print("STAGE 03 COMPLETED (TRANSVERSAL PROFILES, 2 km)")
print(f"Total profiles generated: {len(gdf_profiles)}")
print(f"Output: {OUTPUT_PATH}")
print("==============================================")
