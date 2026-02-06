# ============================================================
# 07_calculate_buhring_metrics.py
# ============================================================
# Computes Bührig-type geomorphic metrics from key points
# P1–P4 extracted along transversal canyon profiles.
#
# Author: Marco Antonio Viveros Velásquez
# Project: SAC_Buhring_Metrics_V1
# ============================================================

import os
import geopandas as gpd
import pandas as pd
import numpy as np

# ------------------------------------------------------------
# Project root (SAC_Buhring_Metrics_V1)
# ------------------------------------------------------------
project_root = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

# ------------------------------------------------------------
# Paths (UPDATED PROJECT ROUTES)
# ------------------------------------------------------------
INPUT_PATH = os.path.join(
    project_root,
    "data", "processed",
    "SAC_profile_keypoints_P1_P2_P3_P4.shp"
)

OUTPUT_CSV = os.path.join(
    project_root,
    "data", "processed",
    "SAC_Buhring_metrics_all_profiles.csv"
)

# ------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------
def horizontal_dist(p, q):
    """Horizontal (XY) distance"""
    return np.sqrt(
        (p["x_utm"] - q["x_utm"])**2 +
        (p["y_utm"] - q["y_utm"])**2
    )

def spatial_dist(p, q):
    """3D Euclidean distance"""
    return np.sqrt(
        (p["x_utm"] - q["x_utm"])**2 +
        (p["y_utm"] - q["y_utm"])**2 +
        (p["z_m"]   - q["z_m"])**2
    )

def angle_law_of_cosines(a, b, c):
    """
    Angle between sides a and b, opposite side c
    """
    cos_theta = (a*a + b*b - c*c) / (2 * a * b)
    cos_theta = np.clip(cos_theta, -1.0, 1.0)
    return np.degrees(np.arccos(cos_theta))

# ------------------------------------------------------------
# Load data
# ------------------------------------------------------------
gdf = gpd.read_file(INPUT_PATH)

records = []

# ------------------------------------------------------------
# Process each profile
# ------------------------------------------------------------
for profile_id, g in gdf.groupby("profile_id"):

    try:
        P1 = g[g["point_id"] == 1].iloc[0]  # Talweg
        P2 = g[g["point_id"] == 2].iloc[0]  # Edge_Left
        P3 = g[g["point_id"] == 3].iloc[0]  # Edge_Right
        P4 = g[g["point_id"] == 4].iloc[0]  # Wmax/Dmax intersection
    except IndexError:
        continue

    # --------------------------------------------------------
    # Distances
    # --------------------------------------------------------
    W1 = horizontal_dist(P2, P4)
    W2 = horizontal_dist(P3, P4)
    Wmax = W1 + W2

    Dmax = abs(P1["z_m"] - P4["z_m"])

    H1 = spatial_dist(P1, P2)
    H2 = spatial_dist(P1, P3)

    # --------------------------------------------------------
    # Angles (law of cosines)
    # --------------------------------------------------------
    B1 = angle_law_of_cosines(H1, Dmax, W1)
    B2 = angle_law_of_cosines(H2, Dmax, W2)

    SWmax = max(B1, B2)
    aspect_ratio = Wmax / Dmax if Dmax > 0 else np.nan

    records.append({
        "profile_id": profile_id,
        "Wmax_m": Wmax,
        "W1_m": W1,
        "W2_m": W2,
        "Dmax_m": Dmax,
        "H1_m": H1,
        "H2_m": H2,
        "B1_deg": B1,
        "B2_deg": B2,
        "SWmax_deg": SWmax,
        "Aspect_ratio_W_D": aspect_ratio
    })

# ------------------------------------------------------------
# Export results
# ------------------------------------------------------------
df_metrics = pd.DataFrame(records)
df_metrics.to_csv(OUTPUT_CSV, index=False)

print("==============================================")
print("STAGE 07 COMPLETED – BÜHRIG METRICS")
print(f"Profiles processed: {len(df_metrics)}")
print(f"Output: {OUTPUT_CSV}")
print("==============================================")
