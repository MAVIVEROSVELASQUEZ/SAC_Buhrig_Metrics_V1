# Bührig Metrics Reproducible Pipeline

**Reproducible geometric and computational pipeline for Bührig-type metrics in submarine canyons**

**Version:** v1.0.0  
**Status:** Stable methodological release

---

## Overview

This repository contains the **reproducible computational implementation** of a geometric pipeline designed to compute **Bührig-type transverse metrics** in real submarine canyons, with particular emphasis on **shore-connected systems** characterized by asymmetric geometry, lack of ideal orthogonality to the thalweg, and complex bathymetric relief.

The pipeline explicitly resolves the gap between the **conceptual definition of Bührig metrics** and their **rigorous application** to transverse profiles extracted from real submarine digital elevation models (DEMs).

The project is conceived as a **methodological infrastructure**, not as a collection of isolated scripts, integrating explicit geometric formalization, computational traceability, and geomorphological validation at both individual-profile and global scales.

---

## Project scope and blocks

This repository corresponds to **Block 2 (Computational Implementation)** of the **Bührig Metrics Project** and contains exclusively the **reproducible computational pipeline**.

The complete **conceptual, geometric, and methodological framework** is documented in an independent manual (Block 1), published with DOI:

> **Viveros Velásquez, M. A. (2026).**  
> *Manual for the reproducible geometric and computational implementation of Bührig-type metrics in submarine canyons* (Version 1.0.0).  
> Zenodo. https://doi.org/10.5281/zenodo.18446821

The manual constitutes the **primary methodological reference** for metric definitions, geometric assumptions, key-point construction (P1–P4), and pipeline design logic.

This repository must be interpreted and cited **in conjunction with the manual**.

---

## Repository structure

The repository is organized to ensure **reproducibility, traceability, and full scientific auditability**:

SAC_BUHRING_METRICS_V1/
│
├─ data/
│ ├─ raw/ # Original input data (DEM, thalweg, edges)
│ └─ processed/ # Processed and derived pipeline data
│
├─ docs/ # Technical and auxiliary documentation
│
├─ outputs/ # Pipeline results and visualizations
│ └─ validation_profiles/
│ └─ All_Profiles/ # Batch validation figures (all profiles)
│
├─ src/ # Reproducible computational implementation
│ ├─ 01_prepare_dem.py
│ ├─ 02_generate_thalweg_points_2km.py
│ ├─ 03_generate_transversal_profiles.py
│ ├─ 04_extract_profile_keypoints_P1_P2_P3.py
│ ├─ 05_calculate_P4_Wmax_Dmax_intersection.py
│ ├─ 06_integrate_profile_keypoints_P1_P2_P3_P4.py
│ ├─ 07_calculate_buhring_metrics.py
│ ├─ 08_test_single_profile_geometry.py
│ └─ 09_All_profiles_SAC.py
│
├─ .gitignore 
├─ CITATION.cff 
├─ LICENSE 
├─ README.md 
└─ requirements.txt 


The pipeline consists of **nine strictly sequential stages**, executed from DEM preparation to **individual and global geomorphological validation** of transverse profiles.

---

## Input data

The pipeline requires a minimal and explicitly defined set of inputs:

- A submarine **Digital Elevation Model (DEM)** derived from GMRT, reprojected to a metric CRS (UTM).
- A vector representation of the **main canyon thalweg**.
- Vector representations of the **left and right canyon edges**.

These datasets constitute the geometric foundation for transversal profile generation, key-point extraction (P1–P4), and morphometric metric computation.

---

## Access and use status

This repository is **closed** and provided exclusively for:

- scientific reference,
- methodological documentation,
- and formal citation.

Access to the full source code, processed data, and pipeline execution is **restricted**.

The closed status reflects the **pre-commercial and research-grade nature** of the development, which constitutes an original scientific–technological asset.

---

## Citation

Until a dedicated DOI is assigned to this repository, the **methodological manual (Block 1)** should be cited as the authoritative reference:

> Viveros Velásquez, M. A. (2026). *Manual for the reproducible geometric and computational implementation of Bührig-type metrics in submarine canyons* (Version 1.0.0). Zenodo. https://doi.org/10.5281/zenodo.18446821

Once a DOI is assigned to this repository, the pipeline should be cited as **versioned software**, using the citation provided in `CITATION.cff`.

---

## Authorship

**Author:**  
Marco Antonio Viveros Velásquez  

**ORCID:**  
https://orcid.org/0009-0001-3653-5758  

**GitHub:**  
https://github.com/MAVIVEROSVELASQUEZ

---

## License

© 2026 Marco Antonio Viveros Velásquez.  
All rights reserved.

This repository is **not distributed under an open-source license**.  
Any use, reproduction, or redistribution requires **explicit written authorization** from the author.
