# Methods and captions

Use this reference when writing manuscript text for outputs made with this skill.

## Required provenance fields

Include these when relevant:

- package name: `subcortex_visualization` or `subcortexVisualizationR`;
- package version or Git commit if known;
- atlas name;
- atlas/template space for NIfTI extraction;
- input type: region table or NIfTI map;
- ROI statistic, such as mean or median;
- resampling/interpolation method;
- color scale and midpoint;
- significance-display rule, if used;
- export format, especially SVG/PDF.

## Minimal Methods sentence

"Region-level values were visualized with the `subcortex_visualization` package using the `<atlas>` atlas. For volumetric inputs, parcel summaries were extracted in `<atlas_space>` with `<statistic>` as the ROI statistic; atlas labels were resampled with nearest-neighbor interpolation when needed. Figures were exported as SVG/PDF vector graphics."

## Caption sentence

"Colors show `<value_column>` mapped to `<atlas>` regions; gray indicates regions with missing values. The same color limits were used across panels where direct comparison was intended."

## Avoid

- Do not say a figure proves statistical significance unless a statistical test and threshold are shown.
- Do not say MNI atlas extraction is subject-native segmentation.
- Do not hide atlas or space details in supplemental code only.
