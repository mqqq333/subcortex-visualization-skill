#!/usr/bin/env python3
"""Validate a region-level table against a subcortex_visualization atlas."""
from __future__ import annotations

import argparse
import sys


def flatten_regions(obj) -> set[str]:
    if isinstance(obj, tuple):
        out = []
        for part in obj:
            out.extend(list(part))
        return {str(x) for x in out}
    return {str(x) for x in list(obj)}


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", required=True, help="CSV/TSV table to validate")
    p.add_argument("--atlas", required=True, help="Atlas name, e.g. aseg_subcortex")
    p.add_argument("--value-column", default="value", help="Numeric value column")
    p.add_argument("--label-column", default="region", help="Region-name column")
    p.add_argument("--hemi-column", default="Hemisphere", help="Hemisphere column; pass none to skip")
    p.add_argument("--strict", action="store_true", help="Exit nonzero on unmatched regions or invalid values")
    args = p.parse_args()

    try:
        import pandas as pd
        from subcortex_visualization.utils import get_atlas_regions
    except Exception as e:  # pragma: no cover
        raise SystemExit(
            "Could not import validation dependencies. Install with: "
            "python -m pip install subcortex-visualization pandas\n"
            f"Original error: {e}"
        )

    sep = "\t" if args.input.endswith((".tsv", ".txt")) else ","
    df = pd.read_csv(args.input, sep=sep)
    problems = []

    for col in [args.label_column, args.value_column]:
        if col not in df.columns:
            problems.append(f"missing required column: {col}")

    if problems:
        for msg in problems:
            print("ERROR:", msg)
        return 2

    numeric = pd.to_numeric(df[args.value_column], errors="coerce")
    bad_numeric = int(numeric.isna().sum() - df[args.value_column].isna().sum())
    if bad_numeric:
        problems.append(f"{bad_numeric} non-numeric value(s) in {args.value_column}")

    atlas_regions = flatten_regions(get_atlas_regions(args.atlas))
    table_regions = {str(x) for x in df[args.label_column].dropna().unique()}
    unmatched = sorted(table_regions - atlas_regions)
    missing_from_table = sorted(atlas_regions - table_regions)

    hemi_col = None if str(args.hemi_column).lower() == "none" else args.hemi_column
    if hemi_col and hemi_col in df.columns:
        valid_hemi = {"L", "R", "B", "V"}
        seen = {str(x) for x in df[hemi_col].dropna().unique()}
        invalid_hemi = sorted(seen - valid_hemi)
        if invalid_hemi:
            problems.append("unexpected hemisphere labels: " + ", ".join(invalid_hemi))
    elif hemi_col:
        print(f"WARNING: hemisphere column not found: {hemi_col}")

    print(f"Rows: {len(df)}")
    print(f"Unique table regions: {len(table_regions)}")
    print(f"Atlas regions: {len(atlas_regions)}")
    print(f"Matched regions: {len(table_regions & atlas_regions)}")

    if unmatched:
        print("UNMATCHED table regions:")
        for r in unmatched[:50]:
            print("  -", r)
        if len(unmatched) > 50:
            print(f"  ... +{len(unmatched)-50} more")
        problems.append(f"{len(unmatched)} unmatched table region(s)")

    if missing_from_table:
        print("Atlas regions absent from table (may be acceptable):")
        for r in missing_from_table[:30]:
            print("  -", r)
        if len(missing_from_table) > 30:
            print(f"  ... +{len(missing_from_table)-30} more")

    if problems:
        for msg in problems:
            print("PROBLEM:", msg, file=sys.stderr)
        return 1 if args.strict else 0

    print("Validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
