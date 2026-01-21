# Bührig Metrics Reproducible Pipeline

**Reproducible geometric and computational pipeline for Bührig-type metrics in submarine canyons**

**Version:** v1.0.0  
**Status:** Stable methodological release

## Overview

This repository contains the **reproducible computational implementation** of a geometric pipeline designed to compute **Bührig-type transverse metrics** in real submarine canyons, with particular emphasis on **shore-connected systems** characterized by asymmetric geometry, lack of ideal orthogonality to the thalweg, and complex bathymetric relief. The pipeline was developed to explicitly resolve the gap between the conceptual definitions of Bührig metrics and their rigorous application to transverse profiles extracted from real submarine digital elevation models.

The project is conceived as a **methodological infrastructure**, rather than a collection of isolated scripts, integrating geometric formalization, computational traceability, and geomorphological validation at both individual-profile and global scales.

---

## Project scope

This repository corresponds to **Block 2** of the **Bührig Metrics** project and contains exclusively the **computational implementation** of the method. The complete **conceptual, geometric, and methodological framework** is documented in an independent manual (Block 1), entitled:

**Manual for the reproducible geometric and computational implementation of Bührig-type metrics in submarine canyons**

This manual will be published shortly on **Zenodo** with its own DOI and constitutes the primary reference for the formal definition of the metrics, geometric assumptions, and pipeline design.

---

## Repository structure

The project is organized to ensure reproducibility, traceability, and full scientific auditability:

```
BUHRIG_METRICS_PIPELINE
│
├── data
│   ├── raw            # Original input data (DEM, shapefiles)
│   ├── processed      # Reprojected and derived data
│   └── intermediate   # Intermediate pipeline outputs
│
├── src
│   ├── 01_prepare_dem.py
│   ├── 02_generate_thalweg_points_2km.py
│   ├── 03_generate_transversal_profiles.py
│   ├── 04_extract_profile_keypoints_P1_P2_P3.py
│   ├── 05_calculate_P4_Wmax_Dmax_intersection.py
│   ├── 06_integrate_profile_keypoints_P1_P2_P3_P4.py
│   ├── 07_calculate_buhring_metrics.py
│   ├── 08_test_single_profile_geometry.py
│   └── 09_All_profiles_validation.py
│
├── outputs
│   ├── example
│   └── validation_profiles
│
├── docs
├── requirements.txt
└── README.md
```

The pipeline consists of **nine strictly sequential stages**, executed in order from DEM preparation to individual and global geomorphological validation of transverse profiles.

---

## Input data

The pipeline relies on a minimal and explicitly defined set of input data:

* A submarine **Digital Elevation Model (DEM)** derived from GMRT, reprojected to a metric coordinate system (UTM).
* A shapefile representing the **main canyon thalweg**.
* Shapefiles representing the **left and right canyon edges**.

These datasets constitute the geometric foundation for transverse profile generation, key-point definition (P1–P4), and morphometric metric computation.

---

## Access and use status

This repository is **closed** and is provided solely for **scientific reference, methodological documentation, and citation purposes**. Access to the full source code, processed data, and pipeline execution is restricted.

The closed nature of the repository reflects the **pre-publication and pre-commercial** status of the development, which constitutes an original scientific–technological asset.

---

## Citation

Once a DOI is assigned to this repository via Zenodo, the pipeline should be cited as **versioned software**. The exact citation format will be provided in this README after DOI publication.

The methodological manual (Block 1) must be cited independently as a document with its own DOI.

---

## Authorship

**Author:**
Marco Antonio Viveros Velásquez

**ORCID:**
[https://orcid.org/0009-0001-3653-5758](https://orcid.org/0009-0001-3653-5758)
(https://github.com/MAVIVEROSVELASQUEZ)
---

## License

© 2026 Marco Antonio Viveros Velásquez.
All rights reserved.

This repository is not distributed under an open-source license. Any use, reproduction, or redistribution of its contents requires explicit authorization from the author.

---

If you want, next we can:

* tailor this README **exactly** to Zenodo’s metadata fields,
* write the **proprietary LICENSE** file,
* or prepare the **official citation (APA + BibTeX)** for both the pipeline and the manual.
