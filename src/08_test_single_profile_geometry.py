# ============================================================
# 08_test_single_profile_geometry.py
#
# Full Bührig geometry validation for a single profile
# V6 – Improved aspect ratio, labels, and vertical padding
# ============================================================

import os
import numpy as np
import geopandas as gpd
import rasterio
import matplotlib.pyplot as plt

# ------------------------------------------------------------
# PARAMETERS
# ------------------------------------------------------------
PROFILE_ID = 54
BUFFER_M = 4000

BASE_DIR = r"C:\Python2025_SAC\SAC_MetricsBu_Project\SAC_Buhring_Metrics_PIPELINE"

DEM_PATH = os.path.join(BASE_DIR, "data/processed/SAC_GMRT_DEM_UTM18S.tif")
TRANSECTS_PATH = os.path.join(BASE_DIR, "data/processed/SAC_transversal_profiles_Clean.shp")
KEYPOINTS_PATH = os.path.join(BASE_DIR, "data/processed/SAC_profile_keypoints_P1_P2_P3_P4.shp")

OUT_DIR = os.path.join(BASE_DIR, "outputs/validation_profiles")
os.makedirs(OUT_DIR, exist_ok=True)

OUT_PNG = os.path.join(
    OUT_DIR,
    f"profile_{PROFILE_ID:03d}_full_Buhring_geometry_v6.png"
)

# ------------------------------------------------------------
# HELPERS
# ------------------------------------------------------------
def to_depth(z):
    return -z

def dist_xy(A, B):
    return np.sqrt((A[0]-B[0])**2 + (A[1]-B[1])**2)

def dist3D(A, B):
    return np.sqrt(np.sum((A - B)**2))

def angle_cosine(a, b, c):
    cosv = (a*a + b*b - c*c) / (2*a*b)
    return np.degrees(np.arccos(np.clip(cosv, -1, 1)))

# ------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------
gdf_kp = gpd.read_file(KEYPOINTS_PATH)
gdf_tr = gpd.read_file(TRANSECTS_PATH)

kp = gdf_kp[gdf_kp["profile_id"] == PROFILE_ID]

P1 = kp[kp["point_id"] == 1].iloc[0]  # Talweg
P2 = kp[kp["point_id"] == 2].iloc[0]  # Edge left
P3 = kp[kp["point_id"] == 3].iloc[0]  # Edge right
P4 = kp[kp["point_id"] == 4].iloc[0]  # Wmax–Dmax intersection

transect = gdf_tr[gdf_tr["profile_id"] == PROFILE_ID].geometry.iloc[0]

# ------------------------------------------------------------
# SAMPLE DEM
# ------------------------------------------------------------
with rasterio.open(DEM_PATH) as src:
    n = 800
    s = np.linspace(0, transect.length, n)
    pts = [transect.interpolate(d) for d in s]
    coords = [(p.x, p.y) for p in pts]
    z_raw = np.array([v[0] for v in src.sample(coords)])

depth = to_depth(z_raw)

# ------------------------------------------------------------
# LOCAL s COORDINATES
# ------------------------------------------------------------
s2 = dist_xy((P2.x_utm, P2.y_utm), (pts[0].x, pts[0].y))
s3 = dist_xy((P3.x_utm, P3.y_utm), (pts[0].x, pts[0].y))
s4 = dist_xy((P4.x_utm, P4.y_utm), (pts[0].x, pts[0].y))
s1 = s4

P1z = to_depth(P1.z_m)
P2z = to_depth(P2.z_m)
P3z = to_depth(P3.z_m)
P4z = to_depth(P4.z_m)

# ------------------------------------------------------------
# CROP PROFILE
# ------------------------------------------------------------
smin = max(min(s2, s3) - BUFFER_M, 0)
smax = min(max(s2, s3) + BUFFER_M, transect.length)

mask = (s >= smin) & (s <= smax)

s_crop = s[mask]
d_crop = depth[mask]

# ------------------------------------------------------------
# METRICS
# ------------------------------------------------------------
P1v = np.array([P1.x_utm, P1.y_utm, P1z])
P2v = np.array([P2.x_utm, P2.y_utm, P2z])
P3v = np.array([P3.x_utm, P3.y_utm, P3z])
P4v = np.array([P4.x_utm, P4.y_utm, P4z])

W1 = dist3D(P2v, P4v)
W2 = dist3D(P4v, P3v)
W  = W1 + W2
D  = dist3D(P1v, P4v)
H1 = dist3D(P1v, P2v)
H2 = dist3D(P1v, P3v)

B1 = angle_cosine(H1, D, W1)
B2 = angle_cosine(H2, D, W2)

# ------------------------------------------------------------
# PLOT – V6
# ------------------------------------------------------------
fig, ax = plt.subplots(figsize=(14, 7))  # 🔹 más ancho (perfil)

ax.plot(s_crop, d_crop, color="0.6", lw=2, label="Real canyon profile (DEM)")
ax.plot([s2, s3], [P2z, P3z], "--", lw=2, label="Wmax")
ax.plot([s1, s1], [P1z, P4z], lw=2, label="Dmax")
ax.plot([s1, s2], [P1z, P2z], lw=1.2, label="H1")
ax.plot([s1, s3], [P1z, P3z], lw=1.2, label="H2")

# Points (bigger talweg)
ax.scatter([s1, s2, s3, s4],
           [P1z, P2z, P3z, P4z],
           s=[120, 70, 70, 70],
           zorder=6)

# Point labels
ax.text(s1, P1z, "P1", ha="center", va="top", fontsize=11, fontweight="bold")
ax.text(s2, P2z, "P2", ha="left", va="bottom", fontsize=10)
ax.text(s3, P3z, "P3", ha="right", va="bottom", fontsize=10)
ax.text(s4, P4z, "P4", ha="center", va="bottom", fontsize=10)

# 🔑 Vertical padding (extra space below talweg)
pad = (d_crop.max() - d_crop.min()) * 0.12
ax.set_ylim(d_crop.min(), d_crop.max() + pad)
ax.invert_yaxis()

txt = (
    f"W = {W/1000:.2f} km\n"
    f"Dmax = {D:.0f} m\n"
    f"B1 = {B1:.1f}°\n"
    f"B2 = {B2:.1f}°"
)

ax.text(0.015, 0.03, txt, transform=ax.transAxes,
        bbox=dict(facecolor="white", alpha=0.9))

ax.set_xlabel("Distance along profile (m)")
ax.set_ylabel("Depth (m)")
ax.set_title(f"Profile {PROFILE_ID} – Full Bührig geometry (validated)")
ax.grid(True)
ax.legend()

plt.tight_layout()
plt.savefig(OUT_PNG, dpi=300)
plt.close()

print("==============================================")
print("STAGE 08 COMPLETED – PROFILE VALIDATION (V6)")
print("Saved:", OUT_PNG)
print("==============================================")
