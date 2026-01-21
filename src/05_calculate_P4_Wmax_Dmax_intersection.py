# ============================================================
# 05_calculate_P4_Wmax_Dmax_intersection.py
# ============================================================
# Calculation of Point P4 for each transversal profile.
#
# P4 is defined as the geometric intersection between:
#   - Wmax: segment connecting Edge_Left (P2) and Edge_Right (P3)
#   - Dmax: line passing through the talweg point (P1) and
#           perpendicular to Wmax
#
# The computation is performed in full vector geometry space
# using the original shapefile containing P1, P2 and P3.
#
# Outputs:
#   - Shapefile with Point P4 (geometry + attributes)
#   - CSV table with P4 coordinates and depth
#
# CRS: UTM 18S (meters)
#
# Author: Marco Antonio Viveros Velásquez
# Project: SAC – Bührig Metrics Pipeline
# ============================================================

import geopandas as gpd
import pandas as pd
import numpy as np
from shapely.geometry import Point, LineString

# ------------------------------------------------------------
# Paths
# ------------------------------------------------------------
INPUT_SHP = r"data/processed/SAC_profile_keypoints_P1_P2_P3.shp"
OUTPUT_SHP = r"data/processed/SAC_profile_keypoints_P4.shp"
OUTPUT_CSV = r"data/processed/SAC_profile_keypoints_P4.csv"

# ------------------------------------------------------------
# Load input keypoints
# ------------------------------------------------------------
gdf = gpd.read_file(INPUT_SHP)

required_cols = {"profile_id", "point_name", "x_utm", "y_utm", "z_m"}
if not required_cols.issubset(gdf.columns):
    raise ValueError("Input shapefile does not contain required fields.")

profiles = sorted(gdf["profile_id"].unique())
records = []

# ------------------------------------------------------------
# Loop over profiles
# ------------------------------------------------------------
for pid in profiles:

    sub = gdf[gdf["profile_id"] == pid]

    try:
        P1 = sub[sub["point_name"] == "Talweg"].iloc[0]
        P2 = sub[sub["point_name"] == "Edge_Left"].iloc[0]
        P3 = sub[sub["point_name"] == "Edge_Right"].iloc[0]
    except IndexError:
        # Skip incomplete profiles
        continue

    # Coordinates
    x1, y1, z1 = P1.x_utm, P1.y_utm, P1.z_m
    x2, y2, z2 = P2.x_utm, P2.y_utm, P2.z_m
    x3, y3, z3 = P3.x_utm, P3.y_utm, P3.z_m

    # --------------------------------------------------------
    # Vector projection of P1 onto Wmax (P2–P3)
    # --------------------------------------------------------
    v_w = np.array([x3 - x2, y3 - y2])
    v_p = np.array([x1 - x2, y1 - y2])

    denom = np.dot(v_w, v_w)
    if denom == 0:
        continue

    t = np.dot(v_p, v_w) / denom

    # Projected coordinates (P4)
    x4 = x2 + t * v_w[0]
    y4 = y2 + t * v_w[1]

    # Linear interpolation of depth along Wmax
    z4 = z2 + t * (z3 - z2)

    records.append({
        "profile_id": pid,
        "point_id": 4,
        "point_name": "Wmax_Dmax_Intersection",
        "x_utm": x4,
        "y_utm": y4,
        "z_m": z4,
        "geometry": Point(x4, y4)
    })

# ------------------------------------------------------------
# Create GeoDataFrame
# ------------------------------------------------------------
gdf_p4 = gpd.GeoDataFrame(records, crs=gdf.crs)

# ------------------------------------------------------------
# Save outputs
# ------------------------------------------------------------
gdf_p4.to_file(OUTPUT_SHP)

df_csv = pd.DataFrame(gdf_p4.drop(columns="geometry"))
df_csv.to_csv(OUTPUT_CSV, index=False)

print("==============================================")
print("STAGE 05 COMPLETED – P4 CALCULATION")
print(f"Total P4 points generated: {len(gdf_p4)}")
print(f"Shapefile: {OUTPUT_SHP}")
print(f"CSV:       {OUTPUT_CSV}")
print("==============================================")
