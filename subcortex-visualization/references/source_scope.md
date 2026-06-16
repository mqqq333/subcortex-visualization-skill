# Source scope

This skill is intentionally grounded in three source families:

- Project documentation/homepage: `https://anniegbryant.github.io/subcortex_visualization/`
- bioRxiv preprint: Bryant, *Subcortex visualization: A toolbox for custom data visualization in the subcortex and cerebellum*, DOI `10.64898/2026.01.23.699785`
- GitHub source: `https://github.com/anniegbryant/subcortex_visualization`

Local PDFs, extracted GitHub zips, and paper text are build-time materials only. They are not needed at runtime and should not be committed with the skill.

## What the sources establish

The package exists because most reusable neuroimaging visualization tools focus on cortex. The paper and docs argue that subcortical/cerebellar visualization is fragmented across ad hoc pipelines, slice screenshots, atlas-specific scripts, and 3D renders that can be difficult to compare. `subcortex_visualization` provides Python and R interfaces for standardized two-dimensional vector graphics across twelve non-cortical atlas templates and includes a route for generating custom SVG scaffolds from new segmentations.

## Operational source of truth

Use the installed package or GitHub source for exact:

- atlas names;
- region names;
- hemisphere conventions;
- API argument names;
- data-frame column expectations;
- supported atlas spaces;
- behavior of `plot_subcortical_data`, `parcel_segstats`, and `get_atlas_regions`.

Do not infer exact region names or file layouts from memory. Validate them.
