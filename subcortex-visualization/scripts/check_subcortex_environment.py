#!/usr/bin/env python3
"""Check Python/R environment readiness for subcortex_visualization workflows."""
from __future__ import annotations

import argparse
import importlib
import platform
import shutil
import subprocess
import sys


def check_python() -> int:
    print("== Python environment ==")
    print("executable:", sys.executable)
    print("version:", sys.version.split()[0])
    if sys.version_info < (3, 11):
        print("WARNING: project docs state Python >= 3.11 is required for the released package.")

    modules = [
        "numpy",
        "pandas",
        "matplotlib",
        "svgpath2mpl",
        "nibabel",
        "nilearn",
        "subcortex_visualization",
    ]
    missing = []
    for name in modules:
        try:
            mod = importlib.import_module(name)
            version = getattr(mod, "__version__", "")
            path = getattr(mod, "__file__", "")
            print(f"OK {name} {version} {path}")
        except Exception as e:
            print(f"MISSING {name}: {e!r}")
            missing.append(name)

    if "subcortex_visualization" not in missing:
        try:
            from subcortex_visualization.utils import get_atlas_regions
            regions = get_atlas_regions("Thalamus_THOMAS")
            print("OK get_atlas_regions('Thalamus_THOMAS'):", len(list(regions)), "regions")
        except Exception as e:
            print("WARNING package imported but atlas region check failed:", repr(e))
            return 1

    if missing:
        print("\nSuggested Python install commands:")
        print("  python -m pip install subcortex-visualization")
        print("  # if NIfTI extraction dependencies are still missing:")
        print("  python -m pip install pandas numpy matplotlib svgpath2mpl nibabel nilearn")
        return 1
    print("Python backend looks ready.")
    return 0


def run_rscript(code: str) -> tuple[int, str]:
    exe = shutil.which("Rscript")
    if not exe:
        return 127, "Rscript not found on PATH"
    proc = subprocess.run([exe, "-e", code], capture_output=True, text=True)
    return proc.returncode, (proc.stdout + proc.stderr).strip()


def check_r() -> int:
    print("== R environment ==")
    exe = shutil.which("Rscript")
    print("Rscript:", exe or "NOT FOUND")
    if not exe:
        print("Suggested R setup: install R, then run the package install command below from R.")
        print('  install.packages("remotes")')
        print('  remotes::install_github("anniegbryant/subcortex_visualization", subdir = "subcortexVisualizationR")')
        return 1

    code = r'''
cat(R.version.string, "\n")
needed <- c("subcortexVisualizationR", "ggplot2", "patchwork", "RNifti")
for (p in needed) {
  ok <- requireNamespace(p, quietly=TRUE)
  cat(ifelse(ok, "OK ", "MISSING "), p, "\n", sep="")
}
if (requireNamespace("subcortexVisualizationR", quietly=TRUE)) {
  library(subcortexVisualizationR)
  x <- get_atlas_regions("Thalamus_THOMAS")
  cat("OK get_atlas_regions Thalamus_THOMAS length=", length(x), "\n", sep="")
}
'''
    rc, out = run_rscript(code)
    print(out)
    if rc != 0 or "MISSING subcortexVisualizationR" in out:
        print("\nSuggested R install commands:")
        print('  install.packages("remotes")')
        print('  remotes::install_github("anniegbryant/subcortex_visualization", subdir = "subcortexVisualizationR")')
        return 1
    print("R backend check completed.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backend", choices=["python", "r", "both"], default="both")
    args = parser.parse_args()
    print("platform:", platform.platform())
    codes = []
    if args.backend in {"python", "both"}:
        codes.append(check_python())
    if args.backend in {"r", "both"}:
        codes.append(check_r())
    return 0 if all(c == 0 for c in codes) else 1


if __name__ == "__main__":
    raise SystemExit(main())
