# Atlas catalog and selection

Use exact atlas names.

## Supported atlas names

- `aseg_subcortex`
- `Melbourne_S1`
- `Melbourne_S2`
- `Melbourne_S3`
- `Melbourne_S4`
- `AICHA_subcortex`
- `Brainnetome_subcortex`
- `CIT168_subcortex`
- `Thalamus_HCP`
- `Thalamus_THOMAS`
- `Brainstem_Navigator`
- `SUIT_cerebellar_lobule`

The source tree provides atlas volumes in `MNI152NLin6Asym` and `MNI152NLin2009cAsym` for extraction workflows.

## Selection guide

- Compact subcortical overview: `aseg_subcortex`.
- Melbourne Subcortex Atlas with increasing granularity: `Melbourne_S1` to `Melbourne_S4`.
- AICHA-family analyses: `AICHA_subcortex`.
- Brainnetome-family analyses: `Brainnetome_subcortex`.
- Subcortical nuclei / reinforcement-learning-oriented detail: `CIT168_subcortex`.
- Thalamic nuclei: `Thalamus_HCP` or `Thalamus_THOMAS`.
- Brainstem nuclei: `Brainstem_Navigator`.
- Cerebellar lobules: `SUIT_cerebellar_lobule`.

## Caveats

- `aseg_subcortex` is a package atlas for standardized visualization/extraction. It is not a subject-native FreeSurfer `aseg.mgz` file.
- Atlas choice constrains interpretation. Do not claim finer anatomical localization than the atlas supports.
- Special atlases may contain midline, bilateral, or vermis regions. Validate region and hemisphere conventions before plotting.
