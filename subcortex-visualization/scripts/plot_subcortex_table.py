#!/usr/bin/env python3
"""Plot region-level subcortical data using subcortex_visualization."""
from __future__ import annotations

import argparse
from pathlib import Path


def parse_size(text: str) -> tuple[float, float]:
    if "," in text:
        a, b = text.split(",", 1)
    else:
        a, b = text.split("x", 1)
    return float(a), float(b)


def flatten_regions(obj) -> set[str]:
    if isinstance(obj, tuple):
        out = []
        for part in obj:
            out.extend(list(part))
        return {str(x) for x in out}
    return {str(x) for x in list(obj)}


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", required=True, help="CSV/TSV file with region-level values")
    p.add_argument("--output-prefix", required=True, help="Output path prefix without extension")
    p.add_argument("--atlas", default="aseg_subcortex", help="Atlas name for plotting")
    p.add_argument("--value-column", default="value", help="Column containing values to color")
    p.add_argument("--label-column", default="region", help="Column containing region names; renamed to region for plotting")
    p.add_argument("--hemisphere", default="both", help="Hemisphere view: both, L, R, or package-supported value")
    p.add_argument("--views", default="medial,lateral", help="Comma-separated views, e.g. medial,lateral or superior,inferior")
    p.add_argument("--pvalue-column", default=None, help="Optional p-value column copied to p_value")
    p.add_argument("--filter", action="append", default=[], help="Column=value filter; can repeat")
    p.add_argument("--cmap", default="coolwarm", help="Matplotlib colormap")
    p.add_argument("--fill-title", default="value", help="Colorbar title")
    p.add_argument("--vmin", type=float, default=None)
    p.add_argument("--vmax", type=float, default=None)
    p.add_argument("--midpoint", default="0", help="Use 0 for signed maps; pass nan to disable")
    p.add_argument("--figsize", default="5,4", help="Figure size, e.g. 5,4")
    p.add_argument("--line-color", default="black")
    p.add_argument("--line-thickness", type=float, default=1.5)
    p.add_argument("--nonsig-fill-alpha", type=float, default=0.35)
    p.add_argument("--fontsize", type=int, default=12)
    p.add_argument("--formats", default="svg,pdf,png", help="Comma-separated output formats")
    p.add_argument("--strict-regions", action="store_true", help="Error if table regions are not in atlas")
    args = p.parse_args()

    try:
        import pandas as pd
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        # Compatibility for older Matplotlib (<3.7) used in some local environments.
        if hasattr(matplotlib, "colormaps") and not hasattr(matplotlib.colormaps, "get_cmap"):
            matplotlib.colormaps.get_cmap = lambda name=None: plt.get_cmap(name)
        from subcortex_visualization.plotting import plot_subcortical_data
        from subcortex_visualization.utils import get_atlas_regions
    except Exception as e:  # pragma: no cover
        raise SystemExit(
            "Could not import plotting dependencies. Install with: "
            "python -m pip install subcortex-visualization matplotlib pandas\n"
            f"Original error: {e}"
        )

    sep = "\t" if args.input.endswith((".tsv", ".txt")) else ","
    df = pd.read_csv(args.input, sep=sep)
    for filt in args.filter:
        if "=" not in filt:
            raise ValueError(f"Filter must be Column=value, got: {filt}")
        col, val = filt.split("=", 1)
        if col not in df.columns:
            raise KeyError(f"Missing filter column: {col}")
        df = df[df[col].astype(str) == val]

    if df.empty:
        raise SystemExit("No rows remain after filtering")
    for col in [args.value_column, args.label_column]:
        if col not in df.columns:
            raise KeyError(f"Missing required column: {col}")
    if args.label_column != "region":
        df = df.rename(columns={args.label_column: "region"})
    if args.pvalue_column:
        if args.pvalue_column not in df.columns:
            raise KeyError(f"Missing p-value column: {args.pvalue_column}")
        if args.pvalue_column != "p_value":
            df = df.rename(columns={args.pvalue_column: "p_value"})

    atlas_regions = flatten_regions(get_atlas_regions(args.atlas))
    table_regions = {str(x) for x in df["region"].dropna().unique()}
    missing = sorted(table_regions - atlas_regions)
    if missing:
        msg = "Regions not found in atlas {0}: {1}".format(args.atlas, ", ".join(missing[:20]))
        if len(missing) > 20:
            msg += f" ... (+{len(missing)-20} more)"
        if args.strict_regions:
            raise SystemExit(msg)
        print("WARNING:", msg)

    midpoint = None if str(args.midpoint).lower() == "nan" else float(args.midpoint)
    kwargs = dict(
        subcortex_data=df,
        atlas=args.atlas,
        value_column=args.value_column,
        hemisphere=args.hemisphere,
        views=[x.strip() for x in args.views.split(",") if x.strip()],
        line_thickness=args.line_thickness,
        line_color=args.line_color,
        fill_title=args.fill_title,
        cmap=args.cmap,
        fill_by_significance=bool(args.pvalue_column),
        nonsig_fill_alpha=args.nonsig_fill_alpha,
        vmin=args.vmin,
        vmax=args.vmax,
        midpoint=midpoint,
        show_figure=False,
        fontsize=args.fontsize,
    )

    obj = plot_subcortical_data(**kwargs)
    fig = obj if hasattr(obj, "savefig") else plt.gcf()
    try:
        fig.set_size_inches(*parse_size(args.figsize))
    except Exception:
        pass
    out_prefix = Path(args.output_prefix)
    out_prefix.parent.mkdir(parents=True, exist_ok=True)
    for fmt in [x.strip().lstrip(".") for x in args.formats.split(",") if x.strip()]:
        out = out_prefix.with_suffix("." + fmt)
        fig.savefig(out, bbox_inches="tight", dpi=300)
        print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

