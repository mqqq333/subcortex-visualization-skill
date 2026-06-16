# R usage reference

Use this file when the user chooses R, provides R/tidyverse data, wants patchwork composites, or asks whether the R plotting tutorial is supported. This reference is based on the project R tutorial and R API documentation.

## Backend position

R is a first-class backend for `subcortex_visualization` through the `subcortexVisualizationR` package. It is especially useful when the user wants:

- tidyverse-style data wrangling;
- ggplot2/patchwork objects;
- combination with R `ggseg` cortical panels;
- R-native SVG/PDF export.

If the user chooses R, do all final plotting, previewing, and export in R. Do not silently switch to Python for rendering.

## Install

```r
install.packages("remotes")
remotes::install_github("anniegbryant/subcortex_visualization", subdir = "subcortexVisualizationR")
```

The source repository also documents an `renv` workflow for reproducing the R environment.

## Core functions

```r
library(subcortexVisualizationR)

plot_subcortical_data()
parcel_segstats()
get_atlas_regions()
```

## `plot_subcortical_data` essentials

```r
plot_subcortical_data(
  subcortex_data = NULL,
  atlas = "aseg_subcortex",
  value_column = "value",
  hemisphere = "L",
  views = c("medial", "lateral"),
  line_color = "black",
  line_thickness = 0.5,
  cmap = "viridis",
  NA_fill = "#cccccc",
  fill_alpha = 1.0,
  fill_by_significance = FALSE,
  nonsig_fill_alpha = 0.5,
  vmin = NULL,
  vmax = NULL,
  midpoint = NULL,
  show_legend = TRUE,
  fill_title = "values",
  fontsize = 12
)
```

Input data frame should contain:

- `region`: exact atlas region name;
- `Hemisphere`: `L`, `R`, `B`, or `V` depending on atlas;
- value column, usually `value`;
- optional `p_value` if `fill_by_significance = TRUE`.

The function returns a ggplot2/patchwork object.

## Minimal R ROI-table example

```r
library(subcortexVisualizationR)
library(ggplot2)

regions <- get_atlas_regions("Thalamus_THOMAS")

set.seed(1)
df <- rbind(
  data.frame(region = regions, Hemisphere = "L", value = rnorm(length(regions))),
  data.frame(region = regions, Hemisphere = "R", value = rnorm(length(regions)))
)

p <- plot_subcortical_data(
  subcortex_data = df,
  atlas = "Thalamus_THOMAS",
  value_column = "value",
  hemisphere = "both",
  cmap = colorRampPalette(c("#3b4cc0", "white", "#b40426")),
  midpoint = 0,
  fill_title = "Simulated signed effect"
)

ggsave("thalamus_THOMAS_demo.svg", p, width = 8, height = 3)
ggsave("thalamus_THOMAS_demo.pdf", p, width = 8, height = 3)
ggsave("thalamus_THOMAS_demo.png", p, width = 8, height = 3, dpi = 300)
```

## Views and special atlases

Default views are medial and lateral. Supported view names include:

- `medial`
- `lateral`
- `superior`
- `inferior`

Special cases from the R tutorial:

- `SUIT_cerebellar_lobule` is not a standard left/right subcortical mesh. It includes cerebellar hemispheric regions and vermis regions; use `hemisphere = "both"` for most demos.
- `Brainstem_Navigator` contains hemispheric and midline regions. `get_atlas_regions("Brainstem_Navigator")` returns a named list with `hemisphere_regions` and `midline_regions`.
- `get_atlas_regions("SUIT_cerebellar_lobule")` returns a named list with `hemisphere_regions` and `vermis_regions`.

## Significance transparency

If the data frame has `p_value`, use:

```r
p <- plot_subcortical_data(
  subcortex_data = df,
  atlas = "SUIT_cerebellar_lobule",
  hemisphere = "both",
  fill_by_significance = TRUE,
  nonsig_fill_alpha = 0.5
)
```

The tutorial states that non-significant regions (`p_value >= 0.05`) are dimmed through lower alpha and thinner outlines.

## Exact region-name check

The R tutorial stresses that empirical data region names must exactly match the atlas definitions.

```r
regions <- get_atlas_regions("aseg_subcortex")
print(regions)
```

For named-list atlases:

```r
suit_regions <- get_atlas_regions("SUIT_cerebellar_lobule")
suit_regions$hemisphere_regions
suit_regions$vermis_regions

brainstem_regions <- get_atlas_regions("Brainstem_Navigator")
brainstem_regions$hemisphere_regions
brainstem_regions$midline_regions
```

## NIfTI to ROI table in R

The R tutorial uses `parcel_segstats()` to summarize volumetric maps into a data frame that can be directly passed to `plot_subcortical_data()`.

```r
func_df <- parcel_segstats(
  input_vol = "map.nii.gz",
  atlas_space = "MNI152NLin6Asym",
  atlas = "Thalamus_THOMAS",
  func_name = "Functional map",
  parc_stat = mean,
  interpolation = "nearest"
)

p <- plot_subcortical_data(
  subcortex_data = func_df,
  atlas = "Thalamus_THOMAS",
  value_column = "value",
  hemisphere = "both"
)
```

The supported atlas spaces are `MNI152NLin6Asym` and `MNI152NLin2009cAsym`. If affine or dimensions do not match and `interpolation = NULL`, `parcel_segstats()` raises an error. Use `interpolation = "nearest"` for atlas labels when resampling is appropriate.

## Multiple atlases in R

`parcel_segstats()` accepts a vector/list of atlas names and adds an `Atlas` column.

```r
atlases <- c("Thalamus_THOMAS", "Brainstem_Navigator", "SUIT_cerebellar_lobule")
func_df <- parcel_segstats(
  input_vol = "map.nii.gz",
  atlas_space = "MNI152NLin6Asym",
  atlas = atlases,
  parc_stat = mean,
  interpolation = "nearest"
)

plots <- lapply(atlases, function(a) {
  plot_subcortical_data(
    subcortex_data = subset(func_df, Atlas == a),
    atlas = a,
    value_column = "value",
    hemisphere = "both",
    vmin = min(func_df$value, na.rm = TRUE),
    vmax = max(func_df$value, na.rm = TRUE)
  )
})
```

## Combining with cortical figures

The R tutorial demonstrates combining subcortical/cerebellar outputs with cortical visualizations. In R, prefer `patchwork` for composites and keep shared color limits when values are comparable.

## R QC checklist

Before final export:

- confirm `region`, `Hemisphere`, and value column;
- run `get_atlas_regions()` and compare names;
- check whether `SUIT` or `Brainstem` returned a named list;
- set `vmin`, `vmax`, and `midpoint` intentionally;
- export SVG/PDF and PNG preview;
- record atlas, MNI space, statistic, interpolation, and package/backend.
