"""
Generate obs_model_general.png — Partial Observability figure for jcmacdonald.dev.

Based on IVAC_Poster/obs_model_general_figure.py but with:
- Shared palette module for consistent colors
- Larger, more prominent domain and column-type icons
- Better text contrast on the observed-data column (charcoal text)
- Slightly taller rows for breathing room
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from matplotlib.path import Path
import numpy as np
from palette import (
    BLUE_HEALTH, TEAL_ENVIRON, GREEN_EARTH, GOLD_ACCENT,
    TEAL_PRIMARY, TEAL_LIGHT, CHARCOAL, SLATE, LIGHT_BG, WHITE,
    apply_theme,
)

apply_theme()

# ── layout constants ───────────────────────────────────────────────────
FIG_W, FIG_H = 16, 10
DPI = 200

COL_X = [0.04, 0.38, 0.72]   # left edges of three columns
COL_W = [0.28, 0.28, 0.26]   # widths
N_ROWS = 4
ROW_GAP = 0.025
TOP_Y = 0.86
ROW_H = (TOP_Y - 0.04 - (N_ROWS - 1) * ROW_GAP) / N_ROWS

# ── domain data ────────────────────────────────────────────────────────
domains = [
    {
        "label": "Epidemiology",
        "color": BLUE_HEALTH,
        "latent": "Disease states\nimmune landscape\ntransmission intensity",
        "obs": "Reporting delay\nunder-detection\ntest sensitivity / specificity",
        "data": "Case counts\nseroprevalence\nhospitalizations",
        "icon": "cross",
    },
    {
        "label": "Marine / Environment",
        "color": TEAL_ENVIRON,
        "latent": "Ecosystem state\nspecies abundances\nnutrient cycling",
        "obs": "Sampling effort\nspatial aliasing\ninstrument calibration",
        "data": "Trawl surveys\nsatellite chlorophyll\neDNA concentrations",
        "icon": "wave",
    },
    {
        "label": "Terrestrial / Earth",
        "color": GREEN_EARTH,
        "latent": "Soil processes\nfire regime\nvegetation dynamics",
        "obs": "Sensor placement\ntemporal resolution\ncloud / canopy cover",
        "data": "Remote sensing indices\nflux tower readings\nfield transects",
        "icon": "triangle",
    },
    {
        "label": "Cultural / Human",
        "color": GOLD_ACCENT,
        "latent": "Cultural traits\ntransmission networks\npopulation structure",
        "obs": "Sampling bias\npreservation / recovery\ncoding subjectivity",
        "data": "Archaeological assemblages\nlinguistic records\ngenomic samples",
        "icon": "diamond",
    },
]

# ── helpers ────────────────────────────────────────────────────────────

def draw_box(ax, x, y, w, h, color, text, fontsize=13, alpha=0.92,
             text_color="white"):
    box = FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.012",
        facecolor=color, edgecolor="none", alpha=alpha,
        transform=ax.transAxes, zorder=2)
    ax.add_patch(box)
    ax.text(x + w / 2, y + h / 2, text,
            ha="center", va="center", fontsize=fontsize,
            color=text_color, fontweight="medium",
            transform=ax.transAxes, zorder=3, linespacing=1.35)


def draw_arrow(ax, x0, y0, x1, y1):
    arrow = FancyArrowPatch(
        (x0, y0), (x1, y1),
        arrowstyle="->,head_width=6,head_length=5",
        color=SLATE, linewidth=2.0,
        transform=ax.transAxes, zorder=4)
    ax.add_patch(arrow)


def draw_domain_icon(ax, icon_type, x, y, size=0.022, color="#ffffffcc"):
    """Draw a prominent domain icon at the top-left of a latent-process box."""
    if icon_type == "cross":
        hw = size * 0.35
        ax.plot([x - hw, x + hw], [y, y], color=color, lw=4,
                solid_capstyle="round", transform=ax.transAxes, zorder=5)
        ax.plot([x, x], [y - hw * 0.7, y + hw * 0.7], color=color, lw=4,
                solid_capstyle="round", transform=ax.transAxes, zorder=5)
    elif icon_type == "wave":
        xs = np.linspace(x - size * 0.6, x + size * 0.6, 50)
        ys = y + size * 0.25 * np.sin((xs - x) / (size * 0.3) * np.pi)
        ax.plot(xs, ys, color=color, lw=2.5, solid_capstyle="round",
                transform=ax.transAxes, zorder=5)
    elif icon_type == "triangle":
        s = size * 0.4
        verts = [(x, y + s * 0.7), (x - s, y - s * 0.5), (x + s, y - s * 0.5),
                 (x, y + s * 0.7)]
        codes = [Path.MOVETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY]
        tri = mpatches.PathPatch(Path(verts, codes), facecolor=color,
                                  edgecolor="none", transform=ax.transAxes, zorder=5)
        ax.add_patch(tri)
    elif icon_type == "diamond":
        s = size * 0.35
        verts = [(x, y + s), (x + s * 0.7, y), (x, y - s), (x - s * 0.7, y),
                 (x, y + s)]
        codes = [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY]
        dia = mpatches.PathPatch(Path(verts, codes), facecolor=color,
                                  edgecolor="none", transform=ax.transAxes, zorder=5)
        ax.add_patch(dia)


def draw_funnel_icon(ax, x, y, size=0.020, color="#ffffffcc"):
    """Draw a funnel/filter icon for the observation process column."""
    hw = size * 0.55
    verts = [(x - hw, y + size * 0.35), (x + hw, y + size * 0.35),
             (x + hw * 0.25, y - size * 0.35), (x - hw * 0.25, y - size * 0.35),
             (x - hw, y + size * 0.35)]
    codes = [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY]
    patch = mpatches.PathPatch(Path(verts, codes), facecolor=color,
                                edgecolor="none", transform=ax.transAxes, zorder=5)
    ax.add_patch(patch)


def draw_barchart_icon(ax, x, y, size=0.020, color="#ffffffcc"):
    """Draw a small bar chart icon for the observed data column."""
    bar_w = size * 0.22
    bar_gap = size * 0.08
    heights = [0.55, 0.85, 0.4]
    base_x = x - (len(heights) * bar_w + (len(heights) - 1) * bar_gap) / 2
    for i, h in enumerate(heights):
        bx = base_x + i * (bar_w + bar_gap)
        bh = size * h
        bar = mpatches.Rectangle(
            (bx, y - size * 0.3), bar_w, bh,
            facecolor=color, edgecolor="none",
            transform=ax.transAxes, zorder=5)
        ax.add_patch(bar)


# ── main figure ────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")

# Title
ax.text(0.50, 0.96, "Partial Observability Is the Common Structure",
        ha="center", va="center", fontsize=22, fontweight="bold",
        color=CHARCOAL, family="sans-serif")
ax.text(0.50, 0.925,
        "The full system state is never directly observed — "
        "every domain shares this architecture",
        ha="center", va="center", fontsize=13, color=SLATE,
        fontstyle="italic", family="sans-serif")

# Column headers
header_y = TOP_Y + 0.025
for cx, cw, label in zip(COL_X, COL_W,
    ["Latent process", "Observation process", "Observed data"]):
    ax.text(cx + cw / 2, header_y, label, ha="center", va="bottom",
            fontsize=14, fontweight="bold", color=CHARCOAL,
            transform=ax.transAxes)

# Draw rows
for i, dom in enumerate(domains):
    y = TOP_Y - i * (ROW_H + ROW_GAP) - ROW_H

    # Domain label (rotated, left sidebar)
    ax.text(0.015, y + ROW_H / 2, dom["label"],
            ha="left", va="center", fontsize=11, fontweight="bold",
            color=dom["color"], rotation=90, transform=ax.transAxes)

    # Column 1: Latent (domain colour)
    draw_box(ax, COL_X[0], y, COL_W[0], ROW_H, dom["color"],
             dom["latent"], fontsize=14)
    # Domain icon — prominent, upper-left of box
    draw_domain_icon(ax, dom["icon"],
                     COL_X[0] + 0.03, y + ROW_H - 0.025, size=0.028)

    # Column 2: Observation process (shared teal)
    draw_box(ax, COL_X[1], y, COL_W[1], ROW_H, TEAL_PRIMARY,
             dom["obs"], fontsize=13)
    draw_funnel_icon(ax, COL_X[1] + 0.03, y + ROW_H - 0.025, size=0.025)

    # Column 3: Observed data (lighter teal, dark text for contrast)
    draw_box(ax, COL_X[2], y, COL_W[2], ROW_H, TEAL_LIGHT,
             dom["data"], fontsize=13, text_color=CHARCOAL)
    draw_barchart_icon(ax, COL_X[2] + 0.03, y + ROW_H - 0.025, size=0.025,
                       color=CHARCOAL + "99")

    # Arrows between columns
    mid_y = y + ROW_H / 2
    draw_arrow(ax, COL_X[0] + COL_W[0] + 0.008, mid_y,
               COL_X[1] - 0.008, mid_y)
    draw_arrow(ax, COL_X[1] + COL_W[1] + 0.008, mid_y,
               COL_X[2] - 0.008, mid_y)

plt.tight_layout(rect=[0, 0, 1, 0.98])

out = os.path.join(os.path.dirname(__file__), "obs_model_general.png")
fig.savefig(out, dpi=DPI, bbox_inches="tight", facecolor="white")
plt.close(fig)
print(f"Saved: {out}")
