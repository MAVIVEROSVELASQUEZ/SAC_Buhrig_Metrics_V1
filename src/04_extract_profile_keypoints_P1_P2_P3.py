"""
04_extract_profile_keypoints_P1_P2_P3.py
---------------------------------------

Stage 04 of the SAC – Bührig Metrics Pipeline.

This script extracts the three fundamental geomorphological key points
(P1–P3) for each curated transversal profile and explicitly assigns
UTM coordinates (X, Y) and bathymetric depth (Z).

P1: Talweg intersection
P2: Left canyon edge intersection
P3: Right canyon edge intersection

Depth (Z) is sampled from the GMRT-derived DEM (negative values).

---------------------------------------------------------------------
INPUTS
---------------------------------------------------------------------
- data/processed/SAC_transversal_profiles_Clean.shp
- data/raw/SAC_Thalweg.shp
- data/raw/SAC_Edge.shp
- data/processed/SAC_GMRT_DEM_UTM18S.tif

---------------------------------------------------------------------
OUTPUTS
---------------------------------------------------------------------
- data/processed/SAC_profile_keypoints_P1_P2_P3.shp
- data/processed/SAC_profile_keypoints_P1_P2_P3.csv
"""

import geopandas as gpd
import rasterio
from shapely.geometry import Point

# ------------------------------------------------------------
# Paths
# ------------------------------------------------------------
PROFILES_PATH = r"data/processed/SAC_transversal_profiles_Clean.shp"
THALWEG_PATH  = r"data/raw/SAC_Thalweg.shp"
EDGE_PATH     = r"data/raw/SAC_Edge.shp"
DEM_PATH      = r"data/processed/SAC_GMRT_DEM_UTM18S.tif"

OUT_SHP = r"data/processed/SAC_profile_keypoints_P1_P2_P3.shp"
OUT_CSV = r"data/processed/SAC_profile_keypoints_P1_P2_P3.csv"

# ------------------------------------------------------------
# Load data
# ------------------------------------------------------------
profiles = gpd.read_file(PROFILES_PATH)
thalweg  = gpd.read_file(THALWEG_PATH).geometry.iloc[0]
edges    = gpd.read_file(EDGE_PATH)

edges_left  = edges[edges["LeftRight"] == "Left"].geometry.unary_union
edges_right = edges[edges["LeftRight"] == "Right"].geometry.unary_union

dem = rasterio.open(DEM_PATH)

records = []

# ------------------------------------------------------------
# Helper: sample DEM
# ------------------------------------------------------------
def sample_dem(point):
    row, col = dem.index(point.x, point.y)
    z = dem.read(1)[row, col]
    return float(z)

# ------------------------------------------------------------
# Loop through profiles
# ------------------------------------------------------------
for _, row in profiles.iterrows():

    profile_id = int(row["profile_id"])
    profile_ln = row.geometry
    center_pt  = profile_ln.interpolate(0.5, normalized=True)

    # =========================================================
    # P1 – Talweg
    # =========================================================
    inter_t = profile_ln.intersection(thalweg)
    if inter_t.is_empty:
        continue

    if inter_t.geom_type == "MultiPoint":
        p1 = min(inter_t.geoms, key=lambda p: p.distance(center_pt))
    else:
        p1 = inter_t

    records.append({
        "profile_id": profile_id,
        "point_id": 1,
        "point_name": "Talweg",
        "x_utm": p1.x,
        "y_utm": p1.y,
        "z_m": sample_dem(p1),
        "geometry": p1
    })

    # =========================================================
    # P2 – Edge Left
    # =========================================================
    inter_l = profile_ln.intersection(edges_left)
    if not inter_l.is_empty:
        p2 = inter_l.centroid
        records.append({
            "profile_id": profile_id,
            "point_id": 2,
            "point_name": "Edge_Left",
            "x_utm": p2.x,
            "y_utm": p2.y,
            "z_m": sample_dem(p2),
            "geometry": p2
        })

    # =========================================================
    # P3 – Edge Right
    # =========================================================
    inter_r = profile_ln.intersection(edges_right)
    if not inter_r.is_empty:
        p3 = inter_r.centroid
        records.append({
            "profile_id": profile_id,
            "point_id": 3,
            "point_name": "Edge_Right",
            "x_utm": p3.x,
            "y_utm": p3.y,
            "z_m": sample_dem(p3),
            "geometry": p3
        })

# ------------------------------------------------------------
# Export outputs
# ------------------------------------------------------------
gdf_pts = gpd.GeoDataFrame(records, crs=profiles.crs)

gdf_pts.to_file(OUT_SHP)
gdf_pts.drop(columns="geometry").to_csv(OUT_CSV, index=False)

print("==============================================")
print("STAGE 04 COMPLETED – P1, P2, P3 with X, Y, Z")
print(f"Total points generated: {len(gdf_pts)}")
print(f"Output SHP: {OUT_SHP}")
print(f"Output CSV: {OUT_CSV}")
print("==============================================")
