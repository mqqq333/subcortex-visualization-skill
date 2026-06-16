#!/usr/bin/env python3
"""Extract subcortex_visualization parcel statistics from one or more NIfTI maps."""
from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Callable, Iterable

np = None  # assigned lazily in main after dependency checks


def _absmean(x):
    return float(np.nanmean(np.abs(np.asarray(x))))


def _nanmean(x):
    return float(np.nanmean(np.asarray(x)))


def _nanmedian(x):
    return float(np.nanmedian(np.asarray(x)))


def _nanstd(x):
    return float(np.nanstd(np.asarray(x)))


_absmean.__name__ = "absmean"
_nanmean.__name__ = "mean"
_nanmedian.__name__ = "median"
_nanstd.__name__ = "std"

STAT_FUNCS: dict[str, Callable] = {
    "mean": _nanmean,
    "absmean": _absmean,
    "median": _nanmedian,
    "std": _nanstd,
}


def infer_subject_id(path: Path, regex: str | None) -> str:
    name = path.name
    if regex:
        m = re.search(regex, name)
        if m:
            return m.group(1) if m.groups() else m.group(0)
    m = re.search(r"(?<!\d)(\d{5,7})(?!\d)", name)
    return m.group(1) if m else path.name.replace(".nii.gz", "").replace(".nii", "")


def infer_map_type(path: Path, explicit_name: str | None = None) -> str:
    if explicit_name:
        return explicit_name
    return path.name.replace(".nii.gz", "").replace(".nii", "")


def normalize_output(df):
    out = df.copy()
    if "label" in out.columns and "region" not in out.columns:
        out = out.rename(columns={"label": "region"})
    if "hemisphere" in out.columns and "Hemisphere" not in out.columns:
        out = out.rename(columns={"hemisphere": "Hemisphere"})
    return out


def melt_stat_columns(df, stat_names: Iterable[str]):
    stat_names = list(stat_names)
    existing = [s for s in stat_names if s in df.columns]
    if "value" in df.columns and "stat" in df.columns:
        return df
    if not existing:
        return df
    id_cols = [c for c in df.columns if c not in existing]
    return df.melt(id_vars=id_cols, value_vars=existing, var_name="stat", value_name="value")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", nargs="+", required=True, help="Input NIfTI file(s), e.g. *.nii.gz")
    p.add_argument("--output", required=True, help="Output CSV path")
    p.add_argument("--atlas", nargs="+", default=["aseg_subcortex"], help="One or more atlas names")
    p.add_argument("--atlas-space", default="MNI152NLin6Asym", help="MNI152NLin6Asym or MNI152NLin2009cAsym")
    p.add_argument("--stats", nargs="+", default=["mean", "absmean"], choices=sorted(STAT_FUNCS), help="ROI statistics")
    p.add_argument("--interpolation", default="nearest", help="Atlas resampling interpolation; use nearest for labels")
    p.add_argument("--subject-regex", default=None, help="Optional regex used to infer subject_id from filename")
    p.add_argument("--func-name", default=None, help="Optional Functional_Map label; defaults to each input filename stem")
    args = p.parse_args()

    try:
        global np
        import numpy as _np
        import pandas as pd
        from subcortex_visualization.segmentation import parcel_segstats
        np = _np
    except Exception as e:  # pragma: no cover
        raise SystemExit(
            "Could not import subcortex_visualization dependencies. Install with: "
            "python -m pip install subcortex-visualization pandas numpy nibabel nilearn\n"
            f"Original error: {e}"
        )

    funcs = [STAT_FUNCS[s] for s in args.stats]
    atlas_arg = args.atlas[0] if len(args.atlas) == 1 else args.atlas
    rows = []
    for item in args.input:
        path = Path(item)
        if not path.exists():
            raise FileNotFoundError(path)
        map_name = infer_map_type(path, args.func_name)
        df = parcel_segstats(
            str(path),
            atlas_space=args.atlas_space,
            atlas=atlas_arg,
            func_name=map_name,
            parc_stat=funcs,
            interpolation=args.interpolation,
        )
        df = normalize_output(pd.DataFrame(df))
        df = melt_stat_columns(df, args.stats)
        df.insert(0, "source_file", str(path))
        df.insert(1, "subject_id", infer_subject_id(path, args.subject_regex))
        df.insert(2, "map_type", map_name)
        rows.append(df)

    result = pd.concat(rows, ignore_index=True) if rows else pd.DataFrame()
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(args.output, index=False)
    print(f"Wrote {len(result)} rows to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
