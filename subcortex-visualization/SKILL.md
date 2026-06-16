---
name: subcortex-visualization
description: Interactive creation of reproducible subcortical, thalamic, brainstem, and cerebellar ROI visualizations using Annie Bryant's subcortex_visualization package in Python or R. Use when Codex should first help the user choose a backend, then guide them through a visualization contract, scene selection, atlas choice, input validation, style decisions, preview/QC loops, and final SVG/PDF export for two-dimensional vector brain figures below the cortical mantle; plot region-level subcortex/cerebellum tables; extract parcel statistics from MNI-space NIfTI maps; list, validate, or choose among the package's twelve supported atlases; plan a custom segmentation-to-SVG atlas workflow; or write Methods/captions/provenance based on the project homepage, bioRxiv preprint, and GitHub source.
---

# Subcortex Visualization

Create interactive, reproducible 2D vector visualizations for region-level data in non-cortical brain structures: subcortex, thalamus, brainstem, and cerebellum.

## First move: backend gate, then visualization contract

For any task that will generate, preview, export, or debug a figure, establish the backend first.

**Backend selection is a gate.** If the user has not explicitly chosen Python or R, and the request requires plotting/extraction code, ask one concise question and stop:

"Do you want to use Python or R? Python is better for NIfTI/Python neuroimaging pipelines; R is better for tidyverse, patchwork, and ggseg-style composite figures."

Do not generate the final plotting script or render the figure until the backend is selected. If the user only wants conceptual advice, scene planning, atlas choice, or manuscript wording, you may discuss both backends without stopping.

**Environment bootstrap is the next gate.** After backend selection, check whether the selected backend is ready. For a fresh skill install or any missing-package error, read `references/environment_setup.md` and use `scripts/check_subcortex_environment.py` when possible. Diagnose first, ask permission before installing dependencies, then re-check before plotting.

After backend selection, establish a small visualization contract:

1. **Purpose**: atlas showcase, empirical ROI table, NIfTI-to-parcel map, multi-atlas comparison, focused thalamus/brainstem/cerebellum panel, custom atlas workflow, or Methods/caption support.
2. **Input**: region table, NIfTI map, atlas/segmentation files, or no data yet.
3. **Atlas**: exact package atlas name, or a recommended atlas from `references/atlas_catalog.md`.
4. **Visual claim**: what the figure should let the reader see, not just what it should look like.
5. **Style/export**: colormap type, midpoint, hemisphere/views, SVG/PDF/PNG outputs, and whether a quick preview is needed.
6. **QC risks**: region-name mismatch, atlas-space mismatch, misleading color scale, missing values, or overclaiming.

If two or more contract fields are missing after backend selection, ask one concise question with 2-3 concrete options and wait. If only one field is missing, choose a sensible default and state it.

## Backend rules

- **Python track**: use bundled Python helper scripts and `subcortex_visualization` Python APIs. Use this track for NIfTI-heavy workflows, Matplotlib outputs, and Python data pipelines.
- **R track**: use `subcortexVisualizationR` APIs from `references/r_usage.md`. Use this track for tidyverse tables, patchwork composites, and ggseg-style R figure workflows.
- Do not silently switch backend during rendering. If the selected backend is missing dependencies, report the blocker, read `references/environment_setup.md`, and provide installation commands or a selected-backend script. Ask before installing.
- Non-selected languages may be used only for non-visual file inspection if they do not create/alter the final visual output.

## Default operating stance

- Treat every figure as a visual argument below the cortical mantle, not as a decorative brain icon.
- Prefer a short guided loop: **backend -> environment check -> intake -> scene proposal -> validation -> preview/export -> QC -> revision options**.
- Offer choices in small sets, such as "Python/R", "overview atlas / nuclei atlas / cerebellum atlas", or "signed diverging / magnitude sequential".
- Validate exact region names before plotting empirical data.
- Use source-grounded package names and API arguments. Do not invent atlases or region labels.
- Finish with reproducible commands and a short provenance note.

## Source grounding

The source project addresses a gap in cortex-focused neuroimaging visualization tools. It standardizes two-dimensional vector graphics for non-cortical atlases so users can map empirical region-level values without relying on ad hoc slice screenshots or lighting-sensitive 3D renders.

Use `references/source_scope.md` for the source boundary and `references/design_principles.md` for the figure-design logic derived from the project homepage and preprint.

## Task routing

1. **Backend choice**: if plotting/extraction code is needed, ask Python or R unless already specified.
2. **Environment readiness**: for fresh installs or missing dependencies, read `references/environment_setup.md`; run `scripts/check_subcortex_environment.py --backend python`, `--backend r`, or `--backend both`; ask before installing packages.
3. **Interactive intake or broad figure request**: read `references/interactive_workflow.md` and `references/scene_recipes.md`.
4. **Atlas choice**: read `references/atlas_catalog.md`; start with the coarsest atlas that answers the question, then move to finer atlases if localization is needed.
5. **Python region table/NIfTI workflow**: read `references/workflows.md`; use bundled Python scripts.
6. **R workflow**: read `references/r_usage.md` if the user chooses R, works in tidyverse/patchwork, or wants to combine with R `ggseg` panels.
7. **Custom atlas or new visualization scaffold**: read `references/custom_atlas.md`; plan segmentation, lookup table, SVG scaffold, ordering CSVs, and validation before plotting values.
8. **Methods/captions/provenance**: read `references/methods_and_captions.md` and report package, atlas, space, statistic, resampling, color scale, and vector export format.
9. **Troubleshooting/QC**: read `references/troubleshooting.md` when a plot is empty, regions are unmatched, or outputs look wrong.
10. **API uncertainty**: read `references/package_api.md` and inspect the installed package or GitHub source before writing final code.

## Required checks

- Confirm backend: Python or R.
- Confirm selected backend environment is ready, or provide a dependency setup path.
- Confirm exact atlas name and exact region names. Use `get_atlas_regions` in the selected backend.
- Confirm atlas space for NIfTI extraction: `MNI152NLin6Asym` or `MNI152NLin2009cAsym`.
- Use nearest-neighbor interpolation for atlas labels. Do not linearly resample integer labels.
- Keep signed and magnitude-only quantities visually distinct: diverging colormap centered at zero for signed values; sequential colormap for magnitudes.
- Export SVG/PDF as primary outputs. PNG is only a preview.
- Do not describe the package atlas `aseg_subcortex` as a subject-native FreeSurfer `aseg.mgz` segmentation.

## Environment diagnostic

```bash
python scripts/check_subcortex_environment.py --backend both
``` 

## Minimal Python commands

```bash
python scripts/inspect_subcortex_atlas.py --atlas aseg_subcortex
python scripts/validate_subcortex_table.py --input values.csv --atlas aseg_subcortex --value-column value
python scripts/plot_subcortex_table.py --input values.csv --output-prefix subcortex_roi_map --atlas aseg_subcortex --value-column value --hemisphere both --formats svg,pdf,png
```

## Minimal R pattern

```r
library(subcortexVisualizationR)
regions <- get_atlas_regions("Thalamus_THOMAS")
# build a data.frame with region, Hemisphere, and value
p <- plot_subcortical_data(subcortex_data = df, atlas = "Thalamus_THOMAS", hemisphere = "both", value_column = "value")
ggplot2::ggsave("thalamus.svg", p, width = 8, height = 3)
```

## Output standard

When relevant, produce:

- backend choice and visualization contract;
- a validated long ROI CSV or R data frame specification;
- an SVG/PDF figure plus optional PNG preview;
- unmatched-region and missing-value diagnostics;
- exact commands or scripts needed to reproduce the result;
- a short provenance note and claim boundary.

## Claim boundary

A `subcortex_visualization` figure supports reproducible visualization of region-level data below the cortical mantle. It does not by itself establish biological causality, subject-native anatomy, statistical significance, or cross-atlas equivalence.

## Related files

| File | Open when |
|---|---|
| `references/interactive_workflow.md` | Need to guide backend choice and figure contract |
| `references/environment_setup.md` | User has a fresh install, missing dependencies, or needs Python/R setup |
| `references/r_usage.md` | User chooses R or asks about the R plotting tutorial |
| `references/scene_recipes.md` | Need to propose figure scenarios or demos |
| `references/atlas_catalog.md` | Need to choose an atlas |
| `references/workflows.md` | Need Python table/NIfTI extraction and plotting commands |
| `references/custom_atlas.md` | Need custom segmentation-to-SVG planning |
| `references/methods_and_captions.md` | Need manuscript prose or provenance |
| `references/troubleshooting.md` | Need QC or bug diagnosis |
| `references/package_api.md` | Need exact function signatures or package behavior |


