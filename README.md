# Buhrig_Metrics_Reproducible_Pipeline

**Reproducible geometric and computational pipeline for Bührig-type metrics (Wmax, Dmax, SWmax) in submarine canyons**

**Version:** v1.0.0  
**Status:** Stable methodological release

---

## Overview

## Overview

Reproducible Python 3.12.5 implementation of Bührig-type morphometric metrics Wmax, Dmax, and SWmax for real submarine canyons. Validated using GMRT submarine DEM data, with the San Antonio Submarine Canyon as case study. Associated manual DOI: https://doi.org/10.5281/zenodo.18446821

## Project Description

## Project Description

This repository contains the reproducible computational (Python 3.12.5) implementation of a geometric pipeline designed to compute Bührig-type morphometric metrics in real submarine canyons, with particular emphasis on shore-connected systems characterized by asymmetric geometry and complex bathymetric relief. The primary case study is the San Antonio Submarine Canyon (SAC), Chile, used as a fully documented application example of the methodological framework.

The terminology and conceptual basis of the implemented metrics derive from:

Bührig, L. H., Colombera, L., Patacci, M., Mountney, N. P. & McCaffrey, W. D. (2022). *A global analysis of controls on submarine-canyon geomorphology*. Earth-Science Reviews, 233, 104150. https://doi.org/10.1016/j.earscirev.2022.104150

The pipeline explicitly resolves the gap between the conceptual definition of Bührig metrics as presented in that study and their rigorous application to transverse profiles extracted from real submarine Digital Elevation Models (DEMs). The objective is to transform a conceptual geomorphological framework into a traceable, computationally reproducible methodology applicable to high-resolution bathymetric datasets.

## Input Data and Geometric Framework

The Bührig metrics pipeline developed in this study is built upon a reduced, explicit, and strictly controlled set of input data, organized under criteria of reproducible curation and geometric traceability. The primary input consists of a submarine Digital Elevation Model (DEM) obtained from the Global Multi-Resolution Topography (GMRT), which integrates multi-source bathymetric data at regional and global scales.

The DEM was downloaded in GeoTIFF format with a mean spatial resolution of 122.30 m per node, suitable for the geometric characterization of a kilometer-scale submarine canyon without introducing artificial over-sampling. The selected area covers approximately 1119 × 999 nodes, within a spatial domain bounded between 72.79° W and 71.56° W longitude, and 33.78° S and 32.86° S latitude, ensuring complete coverage of the analyzed shore-connected system. The original product is provided in geographic coordinates WGS84 (EPSG:4326) and corresponds to GMRT version 4.4, released in August 2025.

This DEM constitutes the continuous base from which real depth profiles are extracted and the transverse geometry of the canyon is reconstructed.

As part of Block 2 of the pipeline, the original DEM is reprojected to a metric coordinate system (UTM 18S) using the script `01_prepare_dem.py`, generating the file `SAC_GMRT_DEM_UTM18S.tif`, which is used consistently throughout all subsequent stages. This reprojection is essential to ensure dimensional coherence in the calculation of distances, slopes, and angles, avoiding errors associated with the use of angular coordinates in geometric analyses.

## Methodological Philosophy

This project is conceived as a methodological infrastructure rather than a collection of isolated scripts. It integrates explicit geometric formalization, full computational traceability, and geomorphological validation at both the individual-profile scale and the global canyon-system scale.


## Implemented Metrics

The pipeline formally implements the following transverse morphometric metrics derived from Bührig et al. (2022):

**Wmax (Maximum Canyon Width).**  
Wmax is defined as the maximum horizontal distance between the geomorphological edges of a transverse canyon profile. These edges correspond to the transition points between canyon flanks and the adjacent surface. It represents the total transverse extent of the canyon at a given cross-section.

**Dmax (Maximum Canyon Depth).**  
Dmax is defined as the vertical difference between a reference line connecting both canyon edges and the minimum elevation point within the profile, typically located at or near the thalweg. It quantifies the maximum incision depth of the canyon at the transverse section.

**SWmax (Steepest-Flank Width).**  
SWmax corresponds to the horizontal distance between the thalweg and the canyon edge associated with the steepest flank. This metric explicitly captures geometric asymmetry and is particularly relevant in shore-connected systems, where bilateral symmetry is rarely observed.

From these primary measurements, the width-to-depth ratio (Wmax/Dmax) is computed as a fundamental morphometric descriptor of transverse incision geometry.

## Geomorphological Scope

Unlike idealized approaches, this pipeline does not assume perfect orthogonality between transects and the thalweg, nor does it assume bilateral symmetry of canyon profiles. Instead, it incorporates explicit geometric validation of key points and allows quantitative assessment of asymmetric morphology.

The methodological framework is especially suited for shore-connected submarine canyons, highly incised head sectors, and systems influenced by complex sediment dynamics or coastal infrastructure.

The ultimate goal is to provide a reproducible, geometrically explicit, and scientifically robust infrastructure for applying Bührig-type metrics to real submarine canyon systems.

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

## Repository structure

```text
Buhrig_Metrics_Reproducible_Pipeline
│
├─ data/
│  ├─ raw/                    # Original input data (DEM, thalweg, edges)
│  └─ processed/              # Processed and derived pipeline data
│
├─ docs/                      # Technical and auxiliary documentation
│
├─ outputs/                   # Pipeline results and visualizations
│  └─ validation_profiles/
│     └─ All_Profiles/
│
├─ src/                       # Reproducible computational implementation
│  ├─ 01_prepare_dem.py
│  ├─ 02_generate_thalweg_points_2km.py
│  ├─ 03_generate_transversal_profiles.py
│  ├─ 04_extract_profile_keypoints_P1_P2_P3.py
│  ├─ 05_calculate_P4_Wmax_Dmax_intersection.py
│  ├─ 06_integrate_profile_keypoints_P1_P2_P3_P4.py
│  ├─ 07_calculate_buhring_metrics.py
│  ├─ 08_test_single_profile_geometry.py
│  └─ 09_All_profiles_SAC.py
│
├─ .gitignore
├─ CITATION.cff
├─ LICENSE
├─ README.md
└─ requirements.txt
```


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
