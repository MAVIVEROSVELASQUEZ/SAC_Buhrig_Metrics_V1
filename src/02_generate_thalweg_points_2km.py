# ============================================================
# 02_generate_thalweg_points_2km.py
# ============================================================
# Generate regularly spaced points every 2 km along the SAC
# thalweg. These points define the center of transversal
# profiles used for Bührig metrics computation.
#
# Input:
#   data/raw/SAC_Thalweg.shp
#
# Output:
#   data/processed/thalweg_points_2km.shp
#
# CRS:
#   Projected CRS (UTM 18S)
#
# Author: Marco Antonio Viveros Velásquez
# Project: SAC – Bührig Metrics Pipeline
# ============================================================

import geopandas as gpd
import numpy as np
from shapely.geometry import Point

# ------------------------------------------------------------
# Paths
# ------------------------------------------------------------
THALWEG_PATH = r"data/raw/SAC_Thalweg.shp"
OUTPUT_PATH  = r"data/processed/thalweg_points_2km.shp"

# ------------------------------------------------------------
# Parameters
# ------------------------------------------------------------
STEP_DISTANCE = 2000  # meters (2 km spacing)

# ------------------------------------------------------------
# Load thalweg
# ------------------------------------------------------------
gdf_thalweg = gpd.read_file(THALWEG_PATH)

if len(gdf_thalweg) != 1:
    raise ValueError("Thalweg shapefile must contain exactly one polyline.")

thalweg_line = gdf_thalweg.geometry.iloc[0]

# ------------------------------------------------------------
# Generate distances along the thalweg
# ------------------------------------------------------------
total_length = thalweg_line.length
distances = np.arange(0, total_length, STEP_DISTANCE)

# ------------------------------------------------------------
# Generate points
# ------------------------------------------------------------
points = []
profile_ids = []

for i, d in enumerate(distances):
    pt = thalweg_line.interpolate(d)
    points.append(pt)
    profile_ids.append(i)

# ------------------------------------------------------------
# Create GeoDataFrame
# ------------------------------------------------------------
gdf_points = gpd.GeoDataFrame(
    {
        "profile_id": profile_ids,
        "distance_m": distances
    },
    geometry=points,
    crs=gdf_thalweg.crs
)

# ------------------------------------------------------------
# Save output
# ------------------------------------------------------------
gdf_points.to_file(OUTPUT_PATH)

print("==============================================")
print("STAGE 02 COMPLETED (2 km spacing)")
print(f"Total points generated: {len(gdf_points)}")
print(f"Output: {OUTPUT_PATH}")
print("==============================================")
