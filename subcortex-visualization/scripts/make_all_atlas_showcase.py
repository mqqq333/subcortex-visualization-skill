#!/usr/bin/env python3
"""Generate a local all-atlas showcase image for README/gallery use.

This script does not copy images from the upstream project. It calls the installed
subcortex_visualization plotting API and renders the supported atlas templates
locally with atlas-index colors.
"""
from __future__ import annotations

import argparse
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="assets/gallery/all_atlas_showcase.png", help="Output PNG path")
    parser.add_argument("--dpi", type=int, default=220, help="DPI for each atlas tile render")
    args = parser.parse_args()

    import numpy as np
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from PIL import Image, ImageDraw, ImageFont, ImageOps

    # Compatibility for older Matplotlib (<3.7) used in some local environments.
    if hasattr(matplotlib, "colormaps") and not hasattr(matplotlib.colormaps, "get_cmap"):
        matplotlib.colormaps.get_cmap = lambda name=None: plt.get_cmap(name)

    from subcortex_visualization.plotting import plot_subcortical_data
    from subcortex_visualization.utils import get_atlas_regions

    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "DejaVu Sans", "Liberation Sans"],
        "svg.fonttype": "none",
    })

    atlases = [
        ("aseg_subcortex", "Subcortex overview", ["medial", "lateral"]),
        ("Melbourne_S1", "Melbourne S1", ["medial", "lateral"]),
        ("Melbourne_S2", "Melbourne S2", ["medial", "lateral"]),
        ("Melbourne_S3", "Melbourne S3", ["medial", "lateral"]),
        ("Melbourne_S4", "Melbourne S4", ["medial", "lateral"]),
        ("CIT168_subcortex", "CIT168 nuclei", ["medial", "lateral"]),
        ("Brainnetome_subcortex", "Brainnetome", ["medial", "lateral"]),
        ("AICHA_subcortex", "AICHA", ["medial", "lateral"]),
        ("Thalamus_HCP", "Thalamus HCP", ["medial", "lateral"]),
        ("Thalamus_THOMAS", "Thalamus THOMAS", ["medial", "lateral"]),
        ("Brainstem_Navigator", "Brainstem Navigator", ["superior", "inferior"]),
        ("SUIT_cerebellar_lobule", "SUIT cerebellum", ["medial", "lateral"]),
    ]

    def flatten_regions(obj) -> list[str]:
        if isinstance(obj, tuple):
            out = []
            for part in obj:
                out.extend(list(part))
            return [str(x) for x in out]
        if isinstance(obj, dict):
            out = []
            for part in obj.values():
                out.extend(list(part))
            return [str(x) for x in out]
        return [str(x) for x in list(obj)]

    try:
        font_title = ImageFont.truetype("arial.ttf", 30)
        font_meta = ImageFont.truetype("arial.ttf", 21)
        font_header = ImageFont.truetype("arial.ttf", 42)
        font_sub = ImageFont.truetype("arial.ttf", 24)
    except Exception:
        font_title = font_meta = font_header = font_sub = ImageFont.load_default()

    palettes = ["viridis", "magma", "plasma", "cividis", "turbo", "YlGnBu", "PuRd", "GnBu", "coolwarm", "RdBu_r", "viridis", "terrain"]
    tiles = []

    for idx, (atlas, label, views) in enumerate(atlases):
        fig = plot_subcortical_data(
            subcortex_data=None,
            atlas=atlas,
            hemisphere="both",
            views=views,
            cmap=palettes[idx % len(palettes)],
            fill_title="region index",
            line_color="#2E2E2E",
            line_thickness=0.75,
            show_legend=False,
            show_figure=False,
            fontsize=7,
        )
        if not hasattr(fig, "savefig"):
            fig = plt.gcf()
        fig.set_size_inches(4.4, 2.55)
        tmp_png = Path(args.output).with_name(f"._tile_{idx:02d}_{atlas}.png")
        fig.savefig(tmp_png, dpi=args.dpi, bbox_inches="tight", facecolor="white")
        plt.close(fig)

        im = Image.open(tmp_png).convert("RGB")
        try:
            tmp_png.unlink()
        except OSError:
            pass

        region_n = len(set(flatten_regions(get_atlas_regions(atlas))))
        im = ImageOps.expand(im, border=10, fill="white")
        im.thumbnail((610, 292), Image.LANCZOS)

        tile = Image.new("RGB", (650, 385), "white")
        draw = ImageDraw.Draw(tile)
        draw.rounded_rectangle((8, 8, 642, 377), radius=22, outline="#E6E6E6", width=2, fill="white")
        tile.paste(im, ((650 - im.width) // 2, 70 + (280 - im.height) // 2))
        draw.text((30, 24), label, fill="#222222", font=font_title)
        draw.text((30, 55), f"{atlas} · {region_n} regions", fill="#666666", font=font_meta)
        tiles.append(tile)

    cols, rows = 3, 4
    margin_x, margin_y = 56, 130
    gap_x, gap_y = 28, 28
    tile_w, tile_h = 650, 385
    width = margin_x * 2 + cols * tile_w + (cols - 1) * gap_x
    height = margin_y + rows * tile_h + (rows - 1) * gap_y + 55

    canvas = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(canvas)
    draw.text((margin_x, 34), "Subcortex visualization atlas showcase", fill="#161616", font=font_header)
    draw.text((margin_x, 84), "Locally rendered with subcortex_visualization; atlas-index colours preview templates for ROI maps.", fill="#555555", font=font_sub)

    for i, tile in enumerate(tiles):
        row, col = divmod(i, cols)
        x = margin_x + col * (tile_w + gap_x)
        y = margin_y + row * (tile_h + gap_y)
        canvas.paste(tile, (x, y))

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out, optimize=True, quality=92)
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
