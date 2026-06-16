# Environment setup and dependency bootstrap

Use this reference when the user just installed the skill, chooses Python/R, or an import/render step fails because dependencies are missing.

## Policy

- Diagnose before installing.
- Do not install packages silently. In Codex, ask the user before running `pip`, `conda`, `install.packages()`, or `remotes::install_github()`.
- Stay within the selected backend. If the user chose R and R packages are missing, do not render a substitute Python figure unless the user explicitly changes backend.
- If network access is unavailable, provide commands and a manual checklist instead of pretending the environment is ready.

## Quick diagnostic

Python/R combined:

```bash
python scripts/check_subcortex_environment.py --backend both
```

Python only:

```bash
python scripts/check_subcortex_environment.py --backend python
```

R only:

```bash
python scripts/check_subcortex_environment.py --backend r
```

## Python setup

The project documentation states that the released Python package requires Python >= 3.11.

Recommended clean environment:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install subcortex-visualization
```

If NIfTI extraction or plotting dependencies are still missing:

```bash
python -m pip install pandas numpy matplotlib svgpath2mpl nibabel nilearn
```

From GitHub source:

```bash
git clone https://github.com/anniegbryant/subcortex_visualization.git
cd subcortex_visualization
python -m pip install .
```

Python readiness test:

```bash
python - <<'PY'
from subcortex_visualization.utils import get_atlas_regions
print(get_atlas_regions("Thalamus_THOMAS"))
PY
```

## R setup

Install R first, then in R:

```r
install.packages("remotes")
remotes::install_github("anniegbryant/subcortex_visualization", subdir = "subcortexVisualizationR")
```

The project docs mention R dependencies including tidyverse, xml2, patchwork, RNifti, scales, svgparser, ANTsR, and extrantsr. GitHub-sourced dependencies are handled by the package install route where possible.

R readiness test:

```r
library(subcortexVisualizationR)
get_atlas_regions("Thalamus_THOMAS")
```

## Common dependency failures

### `No module named subcortex_visualization`

Install the Python package in the active environment:

```bash
python -m pip install subcortex-visualization
```

### `No module named svgpath2mpl`

Install the missing plotting dependency:

```bash
python -m pip install svgpath2mpl
```

### Matplotlib version mismatch

The project pins newer Matplotlib in its docs. If plotting fails with a colormap registry error, either upgrade Matplotlib or use the bundled Python wrapper, which includes a compatibility shim for older Matplotlib:

```bash
python -m pip install --upgrade matplotlib
```

### `Rscript not found`

Install R and ensure `Rscript` is on PATH. If the user cannot change PATH, provide an RStudio-based workflow instead.

## Response pattern for new users

1. Acknowledge that a fresh skill install does not include Python/R package dependencies.
2. Ask backend if missing.
3. Run or propose the diagnostic script.
4. Report exactly what is missing.
5. Ask permission before installing.
6. Re-run the diagnostic.
7. Only then render/export the figure.
