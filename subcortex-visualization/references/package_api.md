# Package API reference

Use this reference before writing code against `subcortex_visualization`.

## Installation

Python release:

```bash
python -m pip install subcortex-visualization
```

Development source:

```bash
git clone https://github.com/anniegbryant/subcortex_visualization.git
cd subcortex_visualization
python -m pip install .
```

## Python imports

```python
from subcortex_visualization.plotting import plot_subcortical_data
from subcortex_visualization.segmentation import parcel_segstats
from subcortex_visualization.utils import get_atlas_regions
```

## `plot_subcortical_data`

Source signature:

```python
plot_subcortical_data(
    subcortex_data=None,
    atlas="aseg_subcortex",
    value_column="value",
    hemisphere="L",
    views=["medial", "lateral"],
    line_thickness=1.5,
    line_color="black",
    fill_title="values",
    cmap=None,
    NA_fill="#cccccc",
    fill_alpha=1.0,
    fill_by_significance=False,
    nonsig_fill_alpha=0.5,
    vmin=None,
    vmax=None,
    midpoint=None,
    show_legend=True,
    show_figure=True,
    fontsize=12,
    ax=None,
)
```

Table expectation:

- `region`: exact atlas region name.
- `Hemisphere`: usually `L`, `R`, `B`, or `V`, depending on atlas/region.
- numeric `value_column`, default `value`.
- optional `p_value` when `fill_by_significance=True`.

Use `show_figure=False` in scripts so the returned Matplotlib figure can be saved.

## `parcel_segstats`

Source signature:

```python
parcel_segstats(
    input_vol,
    atlas_space="MNI152NLin6Asym",
    atlas="aseg_subcortex",
    func_name="Functional map",
    parc_stat=np.mean,
    ignore_background=True,
    background_value=0,
    interpolation=None,
)
```

Important behavior:

- `input_vol` may be a NIfTI path or nibabel image.
- `atlas` may be a string or list of strings.
- `parc_stat` may be a function or list of functions.
- Output is a DataFrame with columns like `stat`, `value`, `Atlas`, `Functional_Map`, `region`, `Hemisphere`, and `Region_Index`.
- If affine or spatial dimensions differ and `interpolation=None`, the function raises an error. For atlas labels, use `interpolation="nearest"`.

## `get_atlas_regions`

```python
get_atlas_regions(atlas_name)
```

Returns ordered region names. For `SUIT_cerebellar_lobule` and `Brainstem_Navigator`, it may return a tuple separating hemispheric and midline/vermis regions. Flatten this tuple when validating table region names.
