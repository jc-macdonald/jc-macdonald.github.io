#!/usr/bin/env python3
"""
Regenerate op_engine_slide.png for jcmacdonald.dev.
Based on IVAC_Poster/op_engine_figure.py with subtitle positioning fixed.

Bug fix: subtitles ("State + Time Manager", "Method Selection",
"Operator Utilities") were placed at y+height+0.05, but FancyBboxPatch
pad=0.08 extends the border to y+height+0.08, causing the border line
to cut through the text.  Fix: offset subtitles to +0.15 and raise zorder.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
from palette import (
    BLUE_HEALTH,
    CHARCOAL,
    GOLD_ACCENT,
    LIGHT_BG,
    TEAL_ENVIRON,
    TEAL_PRIMARY,
    apply_theme,
)

apply_theme()

fig, ax = plt.subplots(1, 1, figsize=(14, 9))
ax.set_xlim(0, 14)
ax.set_ylim(0, 11)
ax.axis("off")

colors = {
    "core": BLUE_HEALTH,
    "solver": TEAL_PRIMARY,
    "matrix": TEAL_ENVIRON,
    "explicit": BLUE_HEALTH,
    "imex": TEAL_PRIMARY,
    "implicit": GOLD_ACCENT,
    "bg": LIGHT_BG,
    "text": CHARCOAL,
}

# === Title ===
ax.text(7, 10.3, "op_engine", fontsize=28, fontweight="bold", ha="center",
        color=colors["core"], fontfamily="monospace")
ax.text(7, 9.7, "One Surface, Many Methods", fontsize=16, ha="center",
        color=colors["text"], style="italic")

# === Domain agnostic banner ===
ax.text(7, 9.05, "Domain-Agnostic: ODEs • PDEs • Operator-Split Hybrids",
        fontsize=9, ha="center", color="gray", style="italic")

# === LEFT: ModelCore ===
core_x, core_width, core_y, core_height = 0.5, 3.2, 5.2, 3.0

ax.text(core_x + core_width / 2, core_y + core_height + 0.4, "ModelCore",
        fontsize=14, fontweight="bold", ha="center", color=colors["core"],
        fontfamily="monospace", zorder=10)
# FIX: offset from +0.05 → +0.15 to clear pad=0.08 border
ax.text(core_x + core_width / 2, core_y + core_height + 0.15,
        "State + Time Manager", fontsize=9, ha="center", color=colors["text"],
        zorder=10)

core_box = FancyBboxPatch((core_x, core_y), core_width, core_height,
    boxstyle="round,pad=0.08", facecolor="white", edgecolor=colors["core"],
    linewidth=2.5, zorder=1)
ax.add_patch(core_box)

core_items = [
    ("y(t)", "state tensor"), ("time_grid", "np.linspace(...)"),
    ("n_states", "primary dimension"), ("n_subgroups", "ensembles"),
    ("other_axes", "extra dims"), ("store_history", "full or final"),
]
for i, (attr, desc) in enumerate(core_items):
    y = core_y + core_height - 0.4 - i * 0.45
    ax.text(core_x + 0.15, y, attr, fontsize=8, fontfamily="monospace",
            fontweight="bold", color=colors["core"], zorder=5)
    ax.text(core_x + 1.5, y, desc, fontsize=7, color=colors["text"], zorder=5)

# === CENTER: CoreSolver Methods ===
solver_x, solver_width, solver_y, solver_height = 4.0, 5.8, 5.0, 3.0

ax.text(solver_x + solver_width / 2, solver_y + solver_height + 0.4,
        "CoreSolver", fontsize=14, fontweight="bold", ha="center",
        color=colors["solver"], fontfamily="monospace", zorder=10)
# FIX: offset from +0.05 → +0.15
ax.text(solver_x + solver_width / 2, solver_y + solver_height + 0.15,
        "Method Selection", fontsize=9, ha="center", color=colors["text"],
        zorder=10)

categories = [
    ("Explicit", colors["explicit"], ["euler", "heun"],
     "Non-stiff, cheap RHS", solver_y + 2.3),
    ("IMEX", colors["imex"], ["imex-euler", "imex-heun-tr", "imex-trbdf2"],
     "Moderate stiffness", solver_y + 1.15),
    ("Implicit", colors["implicit"],
     ["implicit-euler", "trap", "bdf2", "ros2"],
     "Stiff systems", solver_y + 0.0),
]

for cat_name, cat_color, methods, desc, y_base in categories:
    cat_box = FancyBboxPatch((solver_x, y_base), solver_width, 1.0,
        boxstyle="round,pad=0.03", facecolor=cat_color, alpha=0.12,
        edgecolor=cat_color, linewidth=1.5, zorder=1)
    ax.add_patch(cat_box)
    ax.text(solver_x + 0.15, y_base + 0.55, cat_name, fontsize=10,
            fontweight="bold", va="center", color=cat_color, zorder=5)

    pill_x_start = solver_x + 1.5
    for j, method in enumerate(methods):
        pill_w = 1.1 if len(method) > 8 else 0.9
        pill = FancyBboxPatch(
            (pill_x_start + j * (pill_w + 0.1), y_base + 0.3),
            pill_w, 0.45, boxstyle="round,pad=0.02", facecolor="white",
            edgecolor=cat_color, linewidth=1, zorder=2)
        ax.add_patch(pill)
        ax.text(pill_x_start + j * (pill_w + 0.1) + pill_w / 2,
                y_base + 0.52, method, fontsize=6, ha="center",
                fontfamily="monospace", color=cat_color, zorder=5)

# Arrow: ModelCore → CoreSolver
ax.annotate("", xy=(solver_x - 0.1, core_y + core_height / 2),
    xytext=(core_x + core_width + 0.1, core_y + core_height / 2),
    arrowprops=dict(arrowstyle="->", color=colors["text"], lw=2))

# === RIGHT: matrix_ops ===
matrix_x, matrix_width, matrix_y, matrix_height = 10.3, 3.2, 5.2, 3.0

ax.text(matrix_x + matrix_width / 2, matrix_y + matrix_height + 0.4,
        "matrix_ops", fontsize=14, fontweight="bold", ha="center",
        color=colors["matrix"], fontfamily="monospace", zorder=10)
# FIX: offset from +0.05 → +0.15
ax.text(matrix_x + matrix_width / 2, matrix_y + matrix_height + 0.15,
        "Operator Utilities", fontsize=9, ha="center",
        color=colors["text"], zorder=10)

matrix_box = FancyBboxPatch((matrix_x, matrix_y), matrix_width, matrix_height,
    boxstyle="round,pad=0.08", facecolor="white", edgecolor=colors["matrix"],
    linewidth=2.5, zorder=1)
ax.add_patch(matrix_box)

matrix_items = [
    "Laplacian builders", "Crank-Nicolson", "Implicit Euler/Trap",
    "Predictor-corrector", "Kronecker helpers", "Grouped aggregations",
]
for i, item in enumerate(matrix_items):
    y = matrix_y + matrix_height - 0.4 - i * 0.45
    ax.text(matrix_x + 0.15, y, "•", fontsize=10, color=colors["matrix"], zorder=5)
    ax.text(matrix_x + 0.4, y, item, fontsize=8, color=colors["text"], zorder=5)

# Arrow: CoreSolver → matrix_ops
ax.annotate("", xy=(matrix_x - 0.1, core_y + core_height / 2),
    xytext=(solver_x + solver_width + 0.1, core_y + core_height / 2),
    arrowprops=dict(arrowstyle="->", color=colors["text"], lw=2))

# === Bottom: Stiffness Spectrum ===
spec_y, spec_left, spec_right = 3.5, 1.5, 12.5
spec_width = spec_right - spec_left

ax.text(7, 4.6, "Choose Your Method", fontsize=12, fontweight="bold",
        ha="center", color=colors["text"])

n_segments = 80
for i in range(n_segments):
    x = spec_left + i * (spec_width / n_segments)
    t = i / n_segments
    if t < 0.5:
        r = 0.2 + 0.4 * (t / 0.5)
        g = 0.6 - 0.4 * (t / 0.5)
        b = 0.7 - 0.15 * (t / 0.5)
    else:
        t2 = (t - 0.5) / 0.5
        r = 0.6 + 0.3 * t2
        g = 0.2 - 0.1 * t2
        b = 0.55 - 0.35 * t2
    bar = Rectangle((x, spec_y), spec_width / n_segments + 0.02, 0.4,
                     facecolor=(r, g, b), edgecolor="none")
    ax.add_patch(bar)

ax.text(spec_left + 0.5, spec_y + 0.6, "Non-stiff", fontsize=9,
        ha="center", color=colors["explicit"])
ax.text(7, spec_y + 0.6, "Moderate", fontsize=9, ha="center",
        color=colors["imex"])
ax.text(spec_right - 0.5, spec_y + 0.6, "Stiff", fontsize=9,
        ha="center", color=colors["implicit"])

ax.text(spec_left + 0.5, spec_y - 0.25, "euler, heun", fontsize=7,
        ha="center", fontfamily="monospace", color=colors["explicit"])
ax.text(7, spec_y - 0.25, "imex-*", fontsize=7, ha="center",
        fontfamily="monospace", color=colors["imex"])
ax.text(spec_right - 0.5, spec_y - 0.25, "bdf2, ros2", fontsize=7,
        ha="center", fontfamily="monospace", color=colors["implicit"])

# === Domain examples ===
examples_y, ex_width = 1.8, 3.0
ax.text(7, 2.6, "Domain Agnostic", fontsize=10, fontweight="bold",
        ha="center", color=colors["text"])

domains = [
    ("Heat Diffusion", "implicit-euler"),
    ("Reaction-Diffusion", "imex-heun-tr"),
    ("Chemical Kinetics", "bdf2"),
    ("Population Dynamics", "heun"),
]
for i, (domain, method) in enumerate(domains):
    x = 0.4 + i * 3.4
    dom_box = FancyBboxPatch((x, examples_y - 0.3), ex_width, 0.8,
        boxstyle="round,pad=0.03", facecolor=colors["bg"], edgecolor="#ccc",
        linewidth=1)
    ax.add_patch(dom_box)
    ax.text(x + ex_width / 2, examples_y + 0.2, domain, fontsize=8,
            ha="center", fontweight="bold", color=colors["text"])
    ax.text(x + ex_width / 2, examples_y - 0.05, method, fontsize=7,
            ha="center", fontfamily="monospace", color=colors["solver"])

# === Tagline ===
ax.text(7, 0.6, '"Separates what to solve from how to solve it."',
        fontsize=11, ha="center", style="italic", color=colors["text"],
        bbox=dict(boxstyle="round,pad=0.4", facecolor="white",
                  edgecolor=colors["core"], alpha=0.5))

plt.tight_layout()

out = os.path.join(os.path.dirname(__file__), "op_engine_slide.png")
fig.savefig(out, dpi=300, bbox_inches="tight", facecolor="white")
print(f"Saved {out}")
plt.close()
