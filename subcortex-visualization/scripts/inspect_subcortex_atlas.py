#!/usr/bin/env python3
"""List or export exact region names for a subcortex_visualization atlas."""
from __future__ import annotations

import argparse
import csv
from pathlib import Path


def flatten_regions(obj):
    """Flatten arrays/tuples returned by get_atlas_regions."""
    if isinstance(obj, tuple):
        out = []
        for part in obj:
            out.extend(list(part))
        return out
    return list(obj)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--atlas", required=True, help="Atlas name, e.g. aseg_subcortex or SUIT_cerebellar_lobule")
    p.add_argument("--output", default=None, help="Optional CSV output path")
    args = p.parse_args()

    try:
        from subcortex_visualization.utils import get_atlas_regions
    except Exception as e:  # pragma: no cover
        raise SystemExit(
            "Could not import subcortex_visualization. Install with: "
            "python -m pip install subcortex-visualization\n"
            f"Original error: {e}"
        )

    raw = get_atlas_regions(args.atlas)
    rows = []
    if isinstance(raw, tuple):
        group_names = ["hemisphere_regions", "midline_or_vermis_regions"]
        for group, part in zip(group_names, raw):
            for i, region in enumerate(list(part), 1):
                rows.append({"atlas": args.atlas, "group": group, "order": i, "region": str(region)})
    else:
        for i, region in enumerate(list(raw), 1):
            rows.append({"atlas": args.atlas, "group": "regions", "order": i, "region": str(region)})

    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["atlas", "group", "order", "region"])
            writer.writeheader()
            writer.writerows(rows)
        print(f"Wrote {len(rows)} regions to {out}")
    else:
        print(f"Atlas: {args.atlas}")
        print(f"Regions: {len(rows)}")
        for row in rows:
            print(f"{row['order']:>3}\t{row['group']}\t{row['region']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
