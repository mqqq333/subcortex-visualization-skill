# Interactive workflow

Use this file when the user wants to create, design, improve, or debug a subcortical/cerebellar visualization. The interaction should feel like a compact figure-design assistant, not a static command manual.

## Step 0: backend gate

For any request that will produce plotting/extraction code or render a figure, choose backend before the visualization contract.

Ask and stop if not specified:

"Do you want to use Python or R? Python is better for NIfTI/Python neuroimaging pipelines; R is better for tidyverse, patchwork, and ggseg-style composite figures."

Proceed without asking only when:

- the user explicitly says Python or R;
- the input is clearly backend-specific, such as an R script or Python notebook;
- the user asks only for conceptual planning, atlas choice, or Methods wording.

## Step 1: environment bootstrap

After backend selection and before rendering, check whether the selected backend is ready when the user is new, says the skill was just installed, or an import/package error appears.

Preferred diagnostic:

```bash
python scripts/check_subcortex_environment.py --backend python   # Python track
python scripts/check_subcortex_environment.py --backend r        # R track
python scripts/check_subcortex_environment.py --backend both     # if undecided/testing
``` 

If dependencies are missing, read `environment_setup.md`, report the exact blocker, and ask permission before installing anything. Do not silently fall back to the other backend.

## Visualization contract

After backend is selected, fill this contract. Do not over-question. If the user has already implied an answer, write it down and proceed.

| Field | Options / examples |
|---|---|
| Backend | Python or R |
| Purpose | atlas showcase; empirical ROI map; NIfTI-to-parcel map; multi-atlas sensitivity; focused subsystem; custom atlas; caption/Methods |
| Input | CSV/TSV table; NIfTI map; segmentation + lookup; no data yet |
| Structure | subcortex overview; thalamus; brainstem; cerebellum; custom |
| Atlas | `aseg_subcortex`, `Melbourne_S1`-`S4`, `CIT168_subcortex`, `Thalamus_HCP`, `Thalamus_THOMAS`, `Brainstem_Navigator`, `SUIT_cerebellar_lobule`, etc. |
| Visual claim | pattern, localization, comparison, quality-control, or demonstration |
| Encoding | signed diverging; magnitude sequential; categorical/index; significance alpha |
| Output | SVG/PDF final; PNG preview; CSV diagnostics; Methods/caption |

## First response templates

### If backend is missing and code/rendering is requested

Ask:

"Do you want to use Python or R? Python is better for NIfTI/Python neuroimaging pipelines; R is better for tidyverse, patchwork, and ggseg-style composite figures."

Then wait.

### If the user has no data yet

Offer three routes after backend choice:

1. atlas showcase, to learn supported templates;
2. simulated table demo, to test plotting and style;
3. workflow plan, to prepare their real data.

### If the user has a table

Say you will validate region names first. Ask only for missing essentials: atlas name or value column. Then validate before plotting.

### If the user has a NIfTI map

Ask or infer the MNI space and desired atlas. State that extraction will produce a long ROI table before plotting.

### If the user asks for a nicer figure

Diagnose first:

- Is the problem scientific logic, atlas choice, color scale, layout, labels, or export quality?
- Suggest one primary fix and one optional refinement.

## Interaction loop

Use this loop repeatedly:

1. **Choose backend**: Python or R.
2. **Check environment**: diagnose missing packages, ask before install, re-check.
3. **Propose**: "I suggest `<scene>` with `<atlas>` because `<reason>`."
4. **Validate**: check columns, regions, values, atlas, and space.
5. **Preview**: make or describe a minimal preview with conservative defaults in the selected backend.
6. **QC**: report issues explicitly: unmatched regions, missing values, color limits, ambiguous claims.
7. **Refine**: offer 2-3 next actions, such as change atlas, adjust colormap, add significance alpha, split panels, or write caption.
8. **Finalize**: export vector outputs and write provenance.

## Question style

Ask one concise question at a time. Prefer concrete options.

Good:

"Do you want Python or R? Python is better for NIfTI/Python pipelines; R is better for tidyverse/patchwork/ggseg composites."

Good:

"Do you want this as (1) a compact subcortex overview with `aseg_subcortex`, (2) a nuclei-level map with `CIT168_subcortex`, or (3) a cerebellar lobule figure with `SUIT_cerebellar_lobule`?"

Avoid:

"Please provide all details about your data, atlas, aims, statistical design, style, color, output, and caption."

## Defaults when the user wants speed

- Backend: ask first if actual plotting/rendering is needed.
- Atlas: `aseg_subcortex` for general subcortex overview; `Thalamus_THOMAS` for thalamic demo.
- Hemisphere: `both` when bilateral data are present, otherwise `L` default package behavior for atlas showcase.
- Colormap: diverging `coolwarm` or blue-white-red with midpoint 0 for signed values; sequential `viridis` for magnitude or index.
- Outputs: SVG and PDF, plus PNG preview.
- Validation: always check region names before plotting user data.


