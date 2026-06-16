# Troubleshooting and quality control

Use this as the QC gate after validation, preview, or export. It follows the same pattern as the core interaction: diagnose first, then fix one issue at a time.

## QC contract

Report these items after every real plotting run:

- atlas and atlas space;
- number of input rows and unique regions;
- matched and unmatched regions;
- missing or non-numeric values;
- hemisphere labels seen;
- color limits, midpoint, and colormap;
- output files written;
- claim boundary.

## Common failures

### Region names do not plot

Likely cause: table names do not exactly match the atlas lookup. Run:

```bash
python scripts/inspect_subcortex_atlas.py --atlas <atlas>
python scripts/validate_subcortex_table.py --input values.csv --atlas <atlas> --value-column <col>
```

Fix interactively by offering:

1. rename regions to exact package names;
2. switch atlas;
3. drop unmatched rows with a clear note.

### Empty or wrong hemisphere panel

Likely cause: `Hemisphere` labels do not match package conventions. Check whether the atlas expects `L`, `R`, `B`, `V`, or `both` behavior.

### Extraction fails with affine or shape mismatch

Likely cause: input map and atlas do not share grid/affine. If they are in the same MNI space but on different grids, use nearest-neighbor interpolation for atlas labels. If they are not in the same anatomical space, register/resample before extraction.

### Figure has misleading colors

Likely cause: color scale is automatic and differs across panels. Set `vmin`, `vmax`, and `midpoint` deliberately.

### The figure looks correct but the claim is too strong

Rewrite the claim from "this structure is involved" to "region-level values were visualized within this atlas" unless statistical analysis supports the stronger statement.

## Revision prompts

After QC, offer 2-3 concrete next refinements:

- change atlas granularity;
- adjust color scale or midpoint;
- split by hemisphere/view;
- add significance transparency;
- export final SVG/PDF;
- draft Methods/caption.
