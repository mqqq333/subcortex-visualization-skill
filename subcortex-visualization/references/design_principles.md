# Design principles from the project and preprint

Use these principles when creating figures, examples, demos, or manuscript text.

## 1. Prefer vector graphics for region-level values

The project emphasizes 2D vector graphics because they are crisp, resolution-independent, editable in tools such as Inkscape or Illustrator, and avoid lighting artifacts that can make color-mapped 3D renderings hard to interpret.

## 2. Standardize across atlases

The package is inspired by `ggseg`: one consistent plotting function can map region-level values across multiple atlas families. When designing a figure set, keep layout, colormap, value range, and caption structure consistent across atlases.

## 3. Separate visualization from statistical inference

A colored region map is a communication layer. It should not be used as the only evidence for significance, laterality, or biological interpretation. If significance is shown, encode it explicitly, for example with package-supported significance transparency.

## 4. Keep atlas and space visible

Every output should record the atlas name and MNI space when NIfTI extraction was used. This prevents confusion between a package visualization atlas and a subject-native segmentation.

## 5. Match the scientific question to atlas granularity

Use a compact atlas for overview and interpretation. Use finer atlases for localization only when the data and research question justify finer anatomical claims.

## 6. Make the workflow reproducible

Save the source table, exact command/script, package version if available, atlas name, color scale, and exported vector file. Treat manual edits in Illustrator/Inkscape as a final polish step and document them.
