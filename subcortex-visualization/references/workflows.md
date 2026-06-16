# Workflows

Use this reference for concrete task execution.

## 1. Region table to figure

1. Inspect the table columns and first rows.
2. Confirm `region`, `Hemisphere`, and the numeric value column.
3. Validate names against the selected atlas.
4. Plot with vector outputs.

```bash
python scripts/inspect_subcortex_atlas.py --atlas aseg_subcortex
python scripts/validate_subcortex_table.py \
  --input values.csv \
  --atlas aseg_subcortex \
  --value-column value
python scripts/plot_subcortex_table.py \
  --input values.csv \
  --output-prefix figure_subcortex \
  --atlas aseg_subcortex \
  --value-column value \
  --hemisphere both \
  --cmap coolwarm \
  --midpoint 0 \
  --formats svg,pdf,png
```

For magnitude-only data, prefer a sequential colormap and pass `--midpoint nan`.

## 2. NIfTI map to ROI table

1. Confirm the map is in an atlas-supported MNI space.
2. Choose atlas and statistic(s).
3. Use nearest-neighbor interpolation only for atlas labels.
4. Save the long CSV before plotting.

```bash
python scripts/extract_subcortex_segstats.py \
  --input map.nii.gz \
  --atlas aseg_subcortex \
  --atlas-space MNI152NLin6Asym \
  --stats mean median std \
  --interpolation nearest \
  --output subcortex_roi_values_long.csv
```

The wrapper also supports `absmean` as a convenience statistic for magnitude summaries when signed values might cancel.

## 3. Multiple atlases

`parcel_segstats` supports multiple atlases. Use this for sensitivity checks or design comparisons.

```bash
python scripts/extract_subcortex_segstats.py \
  --input map.nii.gz \
  --atlas aseg_subcortex CIT168_subcortex \
  --atlas-space MNI152NLin6Asym \
  --stats mean \
  --output subcortex_multiatlas_long.csv
```

Plot each atlas separately by filtering the `Atlas` column.

## 4. Significance transparency

If the table has a p-value column, pass it to the plotting wrapper:

```bash
python scripts/plot_subcortex_table.py \
  --input values.csv \
  --output-prefix figure_sig \
  --atlas aseg_subcortex \
  --value-column beta \
  --pvalue-column p_fdr \
  --hemisphere both
```

The wrapper renames the p-value column to `p_value` and enables `fill_by_significance`.

## 5. Reproducible output bundle

For a finished figure, keep:

- input CSV or NIfTI path list;
- validation output;
- exact command or script;
- SVG/PDF output;
- optional PNG preview;
- Methods/caption text with provenance.

## Validation checklist

- Region names match package names.
- `Hemisphere` labels are valid for the atlas.
- Color scale limits are intentional and shared across panels when comparing panels.
- SVG/PDF files exist and are not empty.
- The command and environment are saved near the outputs.
