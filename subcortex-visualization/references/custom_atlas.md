# Custom atlas workflow

Use this reference when the user wants to add a new atlas or create a new visualization scene.

The project documentation describes two routes from volumetric segmentation to a 2D SVG scaffold that can be used with `plot_subcortical_data`.

## Required inputs

- Atlas NIfTI segmentation (`.nii.gz`) with integer labels.
- Lookup table mapping region index to region name.
- Target template space.
- Desired views/layout.
- Hemisphere naming convention.

## Semi-automated route

Use this first for most atlases.

1. Build per-region 3D surface meshes from the segmentation.
2. Render each region as a transparent PNG.
3. Trace each PNG to SVG using a Potrace-style boundary tracing workflow.
4. Create region-ordering CSV files that define z-stack/layer order for each view.
5. Inspect and manually correct outlines or ordering where needed.

This route is faster and more scalable for atlases with many separable parcels.

## Manual route

Use this when small, crowded nuclei require manual control.

1. Render a composite surface mesh in a viewer such as Surf Ice.
2. Trace each region manually in a vector editor such as Inkscape.
3. Save SVG paths and lookup/order tables in the package-compatible structure.
4. Validate with a simple table using known region indices.

## Skill behavior for custom atlas tasks

Do not jump straight to final plotting. First create a validation plan and a tiny test table. Then verify that all region names in the lookup table can be plotted and that left/right/midline regions appear in the intended views.
