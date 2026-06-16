# Scene recipes

Use these recipes after the visualization contract is clear. Each recipe should be presented interactively: propose the scene, state why it fits, run the relevant validation, then offer refinement options.

## Recipe 1: Atlas showcase

**Use when**: the user wants to understand package coverage or create a demo without empirical data.

Contract defaults:

- Input: no data.
- Encoding: categorical/index colors.
- Output: SVG/PDF atlas panels or PNG preview.

Interaction:

1. Ask whether the showcase should be broad, subsystem-focused, or manuscript-style.
2. Suggest grouping panels as subcortex, thalamus, brainstem, and cerebellum.
3. Remind the user that colors are atlas indices, not empirical values.

## Recipe 2: Empirical ROI table map

**Use when**: the user has a CSV/TSV table with region-level values.

Contract defaults:

- Input: table with `region`, `Hemisphere`, and a numeric value column.
- Encoding: diverging if signed; sequential if magnitude.
- Output: validated SVG/PDF plus unmatched-region report.

Interaction:

1. Ask for atlas and value column if missing.
2. Validate region names before plotting.
3. Offer style refinements: color scale, labels, significance alpha, or panel split.

## Recipe 3: Volumetric map reduction

**Use when**: the user has NIfTI maps and needs region-level summaries.

Contract defaults:

- Input: NIfTI map in `MNI152NLin6Asym` unless specified.
- Atlas: `aseg_subcortex` for overview.
- Statistic: mean, median, std, or user-defined statistic.
- Interpolation: nearest for labels.

Interaction:

1. Ask for MNI space if unknown.
2. Extract a long ROI table first.
3. Validate and plot the table.
4. Report statistic and resampling in provenance.

## Recipe 4: Multi-atlas sensitivity figure

**Use when**: the user wants to show whether a pattern is robust to atlas granularity.

Contract defaults:

- Atlas pair: compact overview plus finer atlas.
- Encoding: shared color limits.
- Output: separate panels per atlas, not forced one-to-one region matching.

Interaction:

1. Ask whether the goal is overview robustness or anatomical localization.
2. Choose atlas pair accordingly.
3. Warn that region definitions differ across atlases.

## Recipe 5: Focused subsystem panel

**Use when**: the figure is specifically thalamus, brainstem, or cerebellum.

Atlas choices:

- Thalamus: `Thalamus_HCP` or `Thalamus_THOMAS`.
- Brainstem: `Brainstem_Navigator`.
- Cerebellum: `SUIT_cerebellar_lobule`.

Interaction:

1. Ask whether the user wants anatomical detail or a cleaner overview.
2. Validate special midline/vermis/bilateral region handling.
3. Offer a supplemental table if labels are dense.

## Recipe 6: Custom segmentation-to-SVG workflow

**Use when**: the user wants to add a new atlas or make a new scene.

Contract defaults:

- Input: segmentation NIfTI plus lookup table.
- First output: validation plan and tiny test table, not a final manuscript figure.

Interaction:

1. Ask for segmentation, lookup, target space, and preferred route: semi-automated or manual.
2. Plan the SVG scaffold and ordering CSVs.
3. Validate all regions before empirical overlay.

## Recipe 7: Cortex + non-cortex composite

**Use when**: the user wants subcortex/cerebellum beside cortical panels.

Contract defaults:

- Output: subcortex SVG/PDF to combine with cortical figure.
- Color scale: shared only if values are directly comparable.

Interaction:

1. Ask whether the composite is for a paper, slide, or methods schematic.
2. Suggest consistent color limits and aligned legends.
3. Write caption text that names both cortical and non-cortical tools.
