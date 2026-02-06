"""
01_prepare_dem.py
-----------------
# Author: Marco Antonio Viveros Velásquez
# Project: SAC_Buhring_Metrics_V1

Preparation of base bathymetric DEM for the SAC – Bühring Metrics Pipeline.

This script reprojects the raw GMRT bathymetric raster to a metric
coordinate reference system (UTM Zone 18S, WGS84), providing a
consistent spatial base for all subsequent geomorphological analyses
of the San Antonio Submarine Canyon (SAC).

---------------------------------------------------------------------
DATA SOURCE
--------------------------------------------------------------------
Global Multi-Resolution Topography (GMRT) Grid

Citation:
Ryan, W.B.F., S.M. Carbotte, J.O. Coplan, S. O'Hara, A. Melkonian,
R. Arko, R.A. Weissel, V. Ferrini, A. Goodwillie, F. Nitsche,
J. Bonczkowski, and R. Zemsky (2009).
Global Multi-Resolution Topography synthesis.
Geochemistry, Geophysics, Geosystems, 10, Q03014.
https://doi.org/10.1029/2008GC002332

GMRT Version:
    v4.4 (released August 2025)

---------------------------------------------------------------------
INPUT (RAW, IMMUTABLE)
---------------------------------------------------------------------
data/raw/GMRT_raster/GMRTv4_4_0_20260119topo-mask.tif

---------------------------------------------------------------------
OUTPUT (PROCESSED)
---------------------------------------------------------------------
data/processed/SAC_GMRT_DEM_UTM18S.tif
"""

import os
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
from pyproj import CRS


def main():

    # --------------------------------------------------------------
    # Project root (SAC_Buhring_Metrics_V1)
    # --------------------------------------------------------------
    project_root = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )

    # --------------------------------------------------------------
    # Input / Output paths (UPDATED PROJECT ROUTES)
    # --------------------------------------------------------------
    input_raster = os.path.join(
        project_root,
        "data", "raw", "GMRT_raster",
        "GMRTv4_4_0_20260119topo-mask.tif"
    )

    output_dir = os.path.join(
        project_root,
        "data", "processed"
    )

    output_raster = os.path.join(
        output_dir,
        "SAC_GMRT_DEM_UTM18S.tif"
    )

    os.makedirs(output_dir, exist_ok=True)

    # --------------------------------------------------------------
    # Target CRS: UTM Zone 18S (WGS84)
    # --------------------------------------------------------------
    target_crs = CRS.from_epsg(32718)

    # --------------------------------------------------------------
    # Open input raster
    # --------------------------------------------------------------
    with rasterio.open(input_raster) as src:

        if src.crs is None:
            raise ValueError("Input GMRT raster has no defined CRS.")

        print(f"Input CRS  : {src.crs}")
        print(f"Target CRS : {target_crs}")

        # ----------------------------------------------------------
        # Calculate transform and output geometry
        # ----------------------------------------------------------
        transform, width, height = calculate_default_transform(
            src.crs,
            target_crs,
            src.width,
            src.height,
            *src.bounds
        )

        meta = src.meta.copy()
        meta.update({
            "crs": target_crs,
            "transform": transform,
            "width": width,
            "height": height
        })

        # ----------------------------------------------------------
        # Reproject raster
        # ----------------------------------------------------------
        with rasterio.open(output_raster, "w", **meta) as dst:
            for band in range(1, src.count + 1):
                reproject(
                    source=rasterio.band(src, band),
                    destination=rasterio.band(dst, band),
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=transform,
                    dst_crs=target_crs,
                    resampling=Resampling.bilinear
                )

    # --------------------------------------------------------------
    # Basic QC check
    # --------------------------------------------------------------
    with rasterio.open(output_raster) as check:
        data = check.read(1, masked=True)

        if data.mask.all():
            raise RuntimeError(
                "QC failed: output raster contains only NoData values."
            )

        print("QC passed: output DEM contains valid data.")
        print(f"Output DEM written to:\n{output_raster}")


if __name__ == "__main__":
    main()
