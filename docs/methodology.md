Methodology

This repository implements a reproducible geometric and computational pipeline for the calculation of Bührig-type transverse metrics in real submarine canyons. The methodology summarized here describes the general approach, geometric logic, and computational structure of the pipeline, while the complete conceptual and geometric formulation is documented in an independent methodological manual.

The method is designed for submarine canyons with complex geometry, particularly shore-connected systems, where transverse profiles commonly exhibit lateral asymmetry and lack ideal orthogonality relative to the thalweg. In this context, the methodology avoids idealized geometric assumptions and explicitly resolves the profile geometry using operationally defined points and segments.

General methodological framework

The methodological approach is based on the rigorous implementation of the original metrics defined by Bührig: Wmax (maximum canyon width), Dmax (maximum incision depth), and SWmax (maximum canyon sidewall steepness). These metrics are neither redefined nor conceptually modified. Instead, the method introduces explicit auxiliary geometric constructions that allow their reproducible computation from real transverse profiles derived from submarine digital elevation models.

The methodology clearly distinguishes between:
(i) the original Bührig metrics,
(ii) auxiliary geometric elements required for computational implementation, and
(iii) the minimal assumptions necessary to ensure reproducibility without imposing non-observable geometric idealizations.

Input data

The pipeline relies on a minimal and explicitly defined set of input data: a submarine Digital Elevation Model (DEM) derived from GMRT, a shapefile representing the main canyon thalweg, and shapefiles defining the left and right canyon edges. These datasets are treated as structural geomorphological references and are not modified during pipeline execution.

The original DEM is reprojected to a metric coordinate system (UTM) as the first processing stage, ensuring dimensional consistency for distance, slope, and angle calculations.

Pipeline structure

The methodology is implemented through a strictly sequential pipeline composed of nine stages, executed in fixed order. These stages include DEM preparation, thalweg discretization, transversal profile generation, extraction of observable geometric points, construction of auxiliary points, metric computation, and geomorphological validation.

Each stage is implemented as an independent, sequentially numbered script, allowing full data traceability and scientific auditability of the workflow.

Geometric definition of transverse profiles

For each transverse profile, four fundamental geometric points are defined. Point 1 (P1) corresponds to the canyon thalweg and represents the local maximum depth of the profile. Points 2 and 3 (P2 and P3) represent the left and right canyon edges and are directly observable in the DEM-derived profile. Point 4 (P4) is an auxiliary geometric point, defined as the intersection between the vertical line passing through the thalweg and the horizontal line defining the maximum canyon width.

This construction allows Dmax to be defined as a vertical segment colinear with the thalweg and Wmax to be defined as the horizontal distance between the canyon edges, without assuming symmetry or ideal orthogonality.

Metric computation

The metrics Wmax, Dmax, and SWmax are computed from the complete profile geometry. The SWmax metric is operationally defined as the maximum of the angles formed between Dmax and the geometric segments connecting the thalweg to each canyon edge. These angles are computed using the law of cosines, avoiding the use of the Pythagorean theorem and allowing rigorous treatment of real scalene profiles.

Additional auxiliary metrics required for geometric decomposition are computed but do not form part of the original Bührig metric set.

Geomorphological validation

The methodology incorporates explicit geomorphological validation at two levels. At the individual-profile level, selected profiles are fully reconstructed from the DEM and visualized together with all defined geometric elements, allowing detailed inspection of geometric coherence. At the global level, systematic visualizations are generated for all profiles, enabling assessment of metric stability and identification of potential local anomalies.

Scope and limitations

The method is designed to be reproducible and transferable to other submarine canyons, provided that an appropriate DEM and consistent definitions of the canyon thalweg and edges are available. The methodology does not attempt to automate the initial geomorphological interpretation, which continues to require expert judgment for defining the reference geomorphic entities.

Primary methodological reference

The complete conceptual and geometric formulation of the method is documented in the independent manual:

Manual for the reproducible geometric and computational implementation of Bührig-type metrics in submarine canyons

This document constitutes the authoritative reference for interpretation of the pipeline and its derived results.

© 2026 Marco Antonio Viveros Velásquez.
All rights reserved.