# ============================================================
# 06_integrate_profile_keypoints_P1_P2_P3_P4.py
# ============================================================
# Integrates all key geomorphic points (P1–P4) per transversal
# profile into a single geospatial dataset.
#
# Inputs:
#   - SAC_profile_keypoints_P1_P2_P3.shp
#   - SAC_profile_keypoints_P4.shp
#
# Outputs:
#   - SAC_profile_keypoints_P1_P2_P3_P4.shp
#   - SAC_profile_keypoints_P1_P2_P3_P4.csv
#
# CRS:
#   UTM 18S (projected)
#
# Author: Marco Antonio Viveros Velásquez
# Project: SAC – Bührig Metrics Pipeline
# ============================================================

import geopandas as gpd
import pandas as pd

# ------------------------------------------------------------
# Paths
# ------------------------------------------------------------
P123_PATH = r"data/processed/SAC_profile_keypoints_P1_P2_P3.shp"
P4_PATH   = r"data/processed/SAC_profile_keypoints_P4.shp"

OUT_SHP = r"data/processed/SAC_profile_keypoints_P1_P2_P3_P4.shp"
OUT_CSV = r"data/processed/SAC_profile_keypoints_P1_P2_P3_P4.csv"

# ------------------------------------------------------------
# Load datasets
# ------------------------------------------------------------
gdf_p123 = gpd.read_file(P123_PATH)
gdf_p4   = gpd.read_file(P4_PATH)

# ------------------------------------------------------------
# Standardize columns
# ------------------------------------------------------------
COMMON_FIELDS = [
    "profile_id",
    "point_id",
    "point_name",
    "x_utm",
    "y_utm",
    "z_m",
    "geometry"
]

gdf_p123 = gdf_p123[COMMON_FIELDS]
gdf_p4   = gdf_p4[COMMON_FIELDS]

# ------------------------------------------------------------
# Concatenate datasets
# ------------------------------------------------------------
gdf_all = gpd.GeoDataFrame(
    pd.concat([gdf_p123, gdf_p4], ignore_index=True),
    crs=gdf_p123.crs
)

# ------------------------------------------------------------
# Sort for clarity
# ------------------------------------------------------------
gdf_all = gdf_all.sort_values(
    by=["profile_id", "point_id"]
).reset_index(drop=True)

# ------------------------------------------------------------
# Export outputs
# ------------------------------------------------------------
gdf_all.to_file(OUT_SHP)

df_csv = gdf_all.drop(columns="geometry")
df_csv.to_csv(OUT_CSV, index=False)

# ------------------------------------------------------------
# Summary
# ------------------------------------------------------------
print("==============================================")
print("STAGE 06 COMPLETED")
print(f"Total profiles: {gdf_all['profile_id'].nunique()}")
print(f"Total key points: {len(gdf_all)}")
print(f"Shapefile: {OUT_SHP}")
print(f"CSV: {OUT_CSV}")
print("==============================================")
