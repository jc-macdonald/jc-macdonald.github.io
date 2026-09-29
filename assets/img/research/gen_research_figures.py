"""Generate the research-program diagrams used on jcmacdonald.dev.

The figures intentionally favor a small number of large, durable labels so they
remain readable both on project cards and on narrow screens. Run this file from
any directory; outputs are written beside the script.
"""

from __future__ import annotations

from itertools import pairwise
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

HERE = Path(__file__).resolve().parent

from palette import (
    BLUE_HEALTH,
    CHARCOAL,
    GOLD_ACCENT,
    GREEN_EARTH,
    SLATE,
    TEAL_ENVIRON,
    TEAL_PRIMARY,
    WHITE,
    apply_theme,
)

apply_theme()

DPI = 220
PALE_BLUE = "#E8F0FE"
PALE_TEAL = "#E8F6F3"
PALE_GREEN = "#E8F8F5"
PALE_GOLD = "#FEF9E7"
PALE_GRAY = "#EEF2F3"
RED = "#B03A2E"
PALE_RED = "#FDEDEC"


def canvas(
    title: str,
    subtitle: str,
    *,
    size: tuple[float, float] = (14, 8),
    title_size: float = 24,
    subtitle_y: float = 0.902,
) -> tuple[Figure, Axes]:
    fig, ax = plt.subplots(figsize=size)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.text(
        0.5,
        0.955,
        title,
        ha="center",
        va="top",
        fontsize=title_size,
        fontweight="bold",
        color=CHARCOAL,
    )
    ax.text(
        0.5,
        subtitle_y,
        subtitle,
        ha="center",
        va="top",
        fontsize=12.5,
        color=SLATE,
    )
    return fig, ax


def box(
    ax: Axes,
    x: float,
    y: float,
    w: float,
    h: float,
    title: str,
    body: str = "",
    *,
    face: str = WHITE,
    edge: str = TEAL_PRIMARY,
    title_color: str | None = None,
    body_color: str = CHARCOAL,
    title_size: float = 15,
    body_size: float = 10.5,
    linewidth: float = 2,
    linestyle: str = "-",
) -> None:
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.010,rounding_size=0.018",
        facecolor=face,
        edgecolor=edge,
        linewidth=linewidth,
        linestyle=linestyle,
        transform=ax.transAxes,
        zorder=2,
    )
    ax.add_patch(patch)
    color = title_color or edge
    if body:
        ax.text(
            x + w / 2,
            y + h * 0.68,
            title,
            ha="center",
            va="center",
            fontsize=title_size,
            fontweight="bold",
            color=color,
            transform=ax.transAxes,
            zorder=3,
        )
        ax.text(
            x + w / 2,
            y + h * 0.35,
            body,
            ha="center",
            va="center",
            fontsize=body_size,
            color=body_color,
            linespacing=1.35,
            transform=ax.transAxes,
            zorder=3,
        )
    else:
        ax.text(
            x + w / 2,
            y + h / 2,
            title,
            ha="center",
            va="center",
            fontsize=title_size,
            fontweight="bold",
            color=color,
            linespacing=1.25,
            transform=ax.transAxes,
            zorder=3,
        )


def arrow(
    ax: Axes,
    start: tuple[float, float],
    end: tuple[float, float],
    *,
    color: str = SLATE,
    width: float = 2.2,
) -> None:
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle="-|>",
            mutation_scale=14,
            linewidth=width,
            color=color,
            transform=ax.transAxes,
            zorder=1,
        )
    )


def badge(
    ax: Axes, x: float, y: float, text: str, color: str, *, width: float = 0.105
) -> None:
    patch = FancyBboxPatch(
        (x, y),
        width,
        0.048,
        boxstyle="round,pad=0.006,rounding_size=0.018",
        facecolor=color,
        edgecolor="none",
        transform=ax.transAxes,
        zorder=2,
    )
    ax.add_patch(patch)
    ax.text(
        x + width / 2,
        y + 0.024,
        text,
        ha="center",
        va="center",
        fontsize=9.5,
        color=WHITE,
        fontweight="bold",
        zorder=3,
    )


def footer(ax: Axes, text: str) -> None:
    ax.text(
        0.5,
        0.045,
        text,
        ha="center",
        va="center",
        fontsize=10.5,
        color=SLATE,
        fontstyle="italic",
    )


def save(fig: Figure, name: str) -> None:
    fig.savefig(HERE / name, dpi=DPI, bbox_inches="tight", facecolor=WHITE)
    plt.close(fig)
    print(f"saved {name}")


def beyond_onehealth() -> None:
    fig, ax = canvas(
        "A Shared Stack for Partially Observed Systems",
        "Reusable infrastructure, domain-specific models, and explicit maturity levels",
        size=(14, 8.5),
    )
    layers = [
        ("Specification", "OP System", BLUE_HEALTH, PALE_BLUE),
        ("Execution", "OP Engine", TEAL_PRIMARY, PALE_TEAL),
        ("Orchestration", "FlepiMoP2", TEAL_ENVIRON, PALE_GREEN),
        (
            "Design &\nevaluation",
            "trade-study\nstructural scores",
            GOLD_ACCENT,
            PALE_GOLD,
        ),
        ("Inference", "VBPCApy\npp-eigentest", GREEN_EARTH, PALE_GREEN),
    ]
    xs = np.linspace(0.035, 0.825, len(layers))
    for x, (label, tool, color, pale) in zip(xs, layers):
        box(
            ax,
            x,
            0.64,
            0.14,
            0.16,
            label,
            tool,
            face=pale,
            edge=color,
            title_size=11.8,
            body_size=9.5,
        )
    for x0, x1 in pairwise(xs):
        arrow(ax, (x0 + 0.155, 0.72), (x1 - 0.015, 0.72), width=1.8)

    # A shared bus makes clear that the complete stack—not one component alone—
    # supports each domain application.
    ax.plot([0.12, 0.88], [0.575, 0.575], color=SLATE, linewidth=1.7)
    for x in xs:
        arrow(ax, (x + 0.07, 0.625), (x + 0.07, 0.586), width=1.3)
    domains = [
        (
            0.05,
            "Infectious disease",
            "Scenario modeling\nVaccination policy\nSurveillance design",
            BLUE_HEALTH,
            "OPERATIONAL",
        ),
        (
            0.285,
            "Marine ecosystems",
            "TRIDENT\nTrait-structured dynamics\nSampling design",
            TEAL_ENVIRON,
            "ACTIVE RESEARCH",
        ),
        (
            0.52,
            "Wildlife & One Health",
            "CCHF transmission\nCross-scale surveillance\nField-cost tradeoffs",
            GREEN_EARTH,
            "ACTIVE RESEARCH",
        ),
        (
            0.755,
            "New domains",
            "Earth systems\nAgriculture\nCultural evolution",
            GOLD_ACCENT,
            "PLANNED",
        ),
    ]
    for x, title, body, color, status in domains:
        style = "--" if status == "PLANNED" else "-"
        box(
            ax,
            x,
            0.20,
            0.195,
            0.28,
            title,
            body,
            face=WHITE,
            edge=color,
            title_size=13,
            body_size=10,
            linestyle=style,
        )
        ax.text(
            x + 0.0975,
            0.165,
            status,
            ha="center",
            va="center",
            fontsize=8.7,
            fontweight="bold",
            color=color,
        )
        arrow(
            ax,
            (x + 0.0975, 0.56),
            (x + 0.0975, 0.502),
            color=color,
            width=1.4,
        )
    footer(
        ax,
        "Shared components reduce duplicated implementation; domain assumptions and validation remain explicit.",
    )
    save(fig, "beyond_onehealth.png")


def flepimop2() -> None:
    fig, ax = canvas(
        "FlepiMoP2",
        "Configuration-driven orchestration for reproducible scenario campaigns",
        size=(14, 8),
    )
    steps = [
        (
            0.03,
            "Configuration\ntarget",
            "validated YAML\nlocations · scenarios\nparameter grids",
            BLUE_HEALTH,
            PALE_BLUE,
        ),
        (
            0.235,
            "Plugin\nresolution",
            "System · Engine\nParameters · Backend\noptional Process / Job",
            TEAL_PRIMARY,
            PALE_TEAL,
        ),
        (
            0.435,
            "Simulator",
            "typed interfaces\ndynamic providers\nvalidated execution plan",
            TEAL_ENVIRON,
            PALE_GREEN,
        ),
        (
            0.635,
            "Campaign\nexecution",
            "scenario × location\nreplicates · batches\nlocal or scheduled jobs",
            GOLD_ACCENT,
            PALE_GOLD,
        ),
        (
            0.835,
            "Outputs",
            "persisted results\nmetadata · provenance\npost-processing",
            GREEN_EARTH,
            PALE_GREEN,
        ),
    ]
    for x, title, body, color, pale in steps:
        box(
            ax,
            x,
            0.49,
            0.145,
            0.25,
            title,
            body,
            face=pale,
            edge=color,
            title_size=13.5,
            body_size=10,
        )
    for left, right in pairwise(steps):
        arrow(ax, (left[0] + 0.163, 0.615), (right[0] - 0.018, 0.615))

    ax.text(
        0.5,
        0.405,
        "PROVIDER EXAMPLES",
        ha="center",
        fontsize=10.5,
        fontweight="bold",
        color=SLATE,
    )
    badge(ax, 0.245, 0.325, "OP System", BLUE_HEALTH, width=0.14)
    badge(ax, 0.405, 0.325, "OP Engine", TEAL_PRIMARY, width=0.14)
    badge(ax, 0.565, 0.325, "custom plugins", TEAL_ENVIRON, width=0.15)
    box(
        ax,
        0.20,
        0.13,
        0.60,
        0.12,
        "Current command surface",
        "flepimop2 pattern  ·  flepimop2 simulate CONFIG\nflepimop2 job …",
        face=PALE_GRAY,
        edge=SLATE,
        title_size=11,
        body_size=9.5,
    )
    footer(
        ax,
        "System and Engine are replaceable providers—not hard-coded pipeline internals.",
    )
    save(fig, "flepimop2_slide.png")


def future_directions() -> None:
    fig, ax = canvas(
        "Research Program: Generalize, Harden, Operationalize",
        "A closed loop from partially observed systems to defensible decisions",
        size=(14, 7.3),
    )
    columns = [
        (
            0.025,
            "GENERALIZE",
            "New systems",
            "Multi-host zoonoses\nMarine ecosystems\nEarth & spatial processes\nCultural evolution",
            BLUE_HEALTH,
            PALE_BLUE,
        ),
        (
            0.365,
            "HARDEN",
            "Inference &\nevaluation",
            "VBPCApy\npp-eigentest: fit–check–select\ntrade-study\nStructural scores · calibration",
            TEAL_PRIMARY,
            PALE_TEAL,
        ),
        (
            0.705,
            "OPERATIONALIZE",
            "Policy &\nsurveillance",
            "Vaccination strategy\nScenario-modeling campaigns\nCCHF surveillance design\nReproducible decision support",
            GOLD_ACCENT,
            PALE_GOLD,
        ),
    ]
    for x, heading, title, body, color, pale in columns:
        ax.text(
            x + 0.135,
            0.805,
            heading,
            ha="center",
            va="center",
            fontsize=12,
            fontweight="bold",
            color=color,
        )
        box(
            ax,
            x,
            0.28,
            0.27,
            0.46,
            title,
            body,
            face=pale,
            edge=color,
            title_size=15,
            body_size=12,
        )
    arrow(ax, (0.313, 0.51), (0.347, 0.51), width=2)
    arrow(ax, (0.653, 0.51), (0.687, 0.51), width=2)
    arrow(ax, (0.825, 0.245), (0.175, 0.245), color=TEAL_PRIMARY, width=2.4)
    ax.text(
        0.5,
        0.175,
        "observations, diagnostics, and policy feedback close the loop",
        ha="center",
        fontsize=11.5,
        color=TEAL_PRIMARY,
        fontweight="bold",
    )
    footer(
        ax,
        "Status is stated in the surrounding project pages; planned capabilities are not presented as deployed.",
    )
    save(fig, "future_directions_general.png")


def obs_model() -> None:
    fig, ax = canvas(
        "Partial Observability Is the Common Structure",
        "The decision-relevant state is rarely fully observed",
        size=(14, 8.5),
    )
    headers = [
        (0.2625, "Latent process"),
        (0.5425, "Observation model  p(y | x, θobs)"),
        (0.8225, "Observed data"),
    ]
    for x, text in headers:
        ax.text(
            x,
            0.82,
            text,
            ha="center",
            fontsize=12.5,
            fontweight="bold",
            color=CHARCOAL,
        )
    rows = [
        (
            0.65,
            "Epidemiology",
            "Disease states\nTransmission",
            "Detection · delay\nSensitivity",
            "Cases · admissions\nSerology",
            BLUE_HEALTH,
        ),
        (
            0.48,
            "Marine /\nenvironment",
            "Ecosystem state\nNutrient cycling",
            "Sampling effort\nSpatial aliasing",
            "Surveys · eDNA\nRemote sensing",
            TEAL_ENVIRON,
        ),
        (
            0.31,
            "Terrestrial /\nearth",
            "Soil · fire\nVegetation",
            "Sensor placement\nCloud / canopy",
            "Indices · fluxes\nField transects",
            GREEN_EARTH,
        ),
        (
            0.14,
            "Cultural /\nhuman",
            "Traits · networks\nPopulation structure",
            "Recovery bias\nCoding / sampling",
            "Assemblages\nLanguage · genomics",
            GOLD_ACCENT,
        ),
    ]
    for y, domain, latent, observation, data, color in rows:
        ax.text(
            0.025,
            y + 0.065,
            domain,
            ha="left",
            va="center",
            fontsize=10.5,
            fontweight="bold",
            color=color,
        )
        box(
            ax,
            0.16,
            y,
            0.205,
            0.13,
            latent,
            face=color,
            edge=color,
            title_color=WHITE,
            title_size=12.5,
        )
        box(
            ax,
            0.44,
            y,
            0.205,
            0.13,
            observation,
            face=PALE_TEAL,
            edge=TEAL_PRIMARY,
            title_size=11.5,
        )
        box(
            ax,
            0.72,
            y,
            0.205,
            0.13,
            data,
            face=PALE_GRAY,
            edge=SLATE,
            title_size=11.5,
        )
        arrow(ax, (0.383, y + 0.065), (0.422, y + 0.065), color=color, width=1.7)
        arrow(ax, (0.663, y + 0.065), (0.702, y + 0.065), color=color, width=1.7)
    footer(
        ax,
        "Shared mathematics does not erase domain-specific observation assumptions or validation requirements.",
    )
    save(fig, "obs_model_general.png")


def op_engine() -> None:
    fig, ax = canvas(
        "OP Engine",
        "Portable integration semantics with backend-native execution providers",
        size=(14, 8.2),
    )
    items = [
        (
            0.035,
            "Prepared model",
            "RHS · operators\nstructured state\nreusable execution plan",
            BLUE_HEALTH,
            PALE_BLUE,
        ),
        (
            0.27,
            "Kernel families",
            "explicit & adaptive\nIMEX / implicit\nstochastic SSA / tau-leap",
            TEAL_PRIMARY,
            PALE_TEAL,
        ),
        (
            0.51,
            "Execution\nprovider",
            "native control flow\ncompilation · checkpointing\nschedule validation",
            TEAL_ENVIRON,
            PALE_GREEN,
        ),
        (
            0.75,
            "Results &\ndiagnostics",
            "backend-native arrays\nstep / accuracy metadata\nreplay checks",
            GOLD_ACCENT,
            PALE_GOLD,
        ),
    ]
    widths = [0.17, 0.17, 0.17, 0.20]
    for item_index, ((x, title, body, color, pale), item_width) in enumerate(
        zip(items, widths)
    ):
        box(
            ax,
            x,
            0.48,
            item_width,
            0.27,
            title,
            body,
            face=pale,
            edge=color,
            title_size=12.5 if item_index == 3 else 13,
            body_size=10,
        )
    for (left, left_width), right in zip(zip(items[:-1], widths[:-1]), items[1:]):
        arrow(
            ax,
            (left[0] + left_width + 0.018, 0.615),
            (right[0] - 0.018, 0.615),
        )

    ax.text(
        0.5,
        0.405,
        "ARRAY-API AND PROVIDER BOUNDARIES",
        ha="center",
        fontsize=11,
        fontweight="bold",
        color=SLATE,
    )
    badge(ax, 0.20, 0.325, "NumPy", BLUE_HEALTH)
    badge(ax, 0.325, 0.325, "JAX", TEAL_PRIMARY)
    badge(ax, 0.45, 0.325, "PyTorch", TEAL_ENVIRON)
    badge(ax, 0.575, 0.325, "CuPy*", GREEN_EARTH)
    ax.text(
        0.70,
        0.35,
        "* compatible paths; method parity varies",
        ha="left",
        va="center",
        fontsize=9.5,
        color=SLATE,
    )
    box(
        ax,
        0.17,
        0.14,
        0.66,
        0.12,
        "Method choice is capability-aware",
        "operator structure · stiffness · accuracy · stochasticity · backend support",
        face=PALE_GRAY,
        edge=SLATE,
        title_size=11.5,
        body_size=10,
    )
    footer(
        ax,
        "Adaptive mesh discovery and differentiable replay are separate operations.",
    )
    save(fig, "op_engine_slide.png")


def op_system() -> None:
    fig, ax = canvas(
        "OP System",
        "A restricted model language compiled through typed IR to portable evaluators",
        size=(14, 8.2),
    )
    box(
        ax,
        0.035,
        0.54,
        0.20,
        0.22,
        "Governing\nequations",
        "states · parameters\naxes · expressions\noperators",
        face=PALE_BLUE,
        edge=BLUE_HEALTH,
        title_size=14,
    )
    box(
        ax,
        0.035,
        0.25,
        0.20,
        0.22,
        "Transition\ndiagrams",
        "compartments · rates\nstratified flows\nstaged chains",
        face=PALE_GREEN,
        edge=GREEN_EARTH,
        title_size=14,
    )
    arrow(ax, (0.252, 0.65), (0.302, 0.57), color=BLUE_HEALTH)
    arrow(ax, (0.252, 0.36), (0.302, 0.48), color=GREEN_EARTH)
    box(
        ax,
        0.32,
        0.39,
        0.19,
        0.27,
        "Parse & validate",
        "restricted syntax\ntemplate expansion\naxis / reducer checks",
        face=PALE_GRAY,
        edge=SLATE,
        title_size=14,
    )
    arrow(ax, (0.528, 0.525), (0.557, 0.525))
    box(
        ax,
        0.575,
        0.39,
        0.16,
        0.27,
        "Typed IR",
        "aliases · routes\nreactions · kernels\noperators · history",
        face=PALE_TEAL,
        edge=TEAL_PRIMARY,
        title_size=15,
    )
    arrow(ax, (0.753, 0.525), (0.782, 0.525))
    box(
        ax,
        0.80,
        0.39,
        0.16,
        0.27,
        "Vectorized\ncodegen",
        "restricted bytecode\nArray-API operations\npicklable artifacts",
        face=PALE_GOLD,
        edge=GOLD_ACCENT,
        title_size=13,
    )

    ax.text(
        0.5,
        0.315,
        "COMPILED OUTPUTS",
        ha="center",
        fontsize=10.5,
        fontweight="bold",
        color=SLATE,
    )
    outputs = [
        (0.27, "flat evaluator", BLUE_HEALTH),
        (0.435, "PyTree evaluator", TEAL_PRIMARY),
        (0.60, "block-PyTree", TEAL_ENVIRON),
        (0.765, "structured metadata", GOLD_ACCENT),
    ]
    for x, label, color in outputs:
        badge(ax, x, 0.23, label, color, width=0.145)
    ax.text(
        0.5,
        0.145,
        "One compiled model surface for NumPy, JAX, and PyTorch array execution",
        ha="center",
        fontsize=11.5,
        color=CHARCOAL,
        fontweight="bold",
    )
    footer(
        ax,
        "Structured ODE, PDE, and multiphysics models—within an explicit validated schema.",
    )
    save(fig, "op_system_slide.png")


def optimal_design() -> None:
    fig, ax = canvas(
        "Observation Design Under Cost and Uncertainty",
        "An application example: compare feasible designs without assuming one universal winner",
        size=(14, 8.5),
    )
    levers = [
        (0.04, "WHAT", "states · assays\nvariables", BLUE_HEALTH, PALE_BLUE),
        (0.04, "WHEN", "frequency\ntiming", TEAL_PRIMARY, PALE_TEAL),
        (0.04, "WHERE", "sites · strata\nreplicates", GREEN_EARTH, PALE_GREEN),
    ]
    for i, (x, title, body, color, pale) in enumerate(levers):
        box(
            ax,
            x,
            0.62 - 0.19 * i,
            0.19,
            0.145,
            title,
            body,
            face=pale,
            edge=color,
            title_size=13,
            body_size=10,
        )
    arrow(ax, (0.252, 0.52), (0.292, 0.52))
    box(
        ax,
        0.31,
        0.33,
        0.20,
        0.38,
        "Candidate designs",
        "A  low-cost baseline\nB  dense temporal sampling\nC  more spatial coverage\nD  balanced design\nE  high-cost reference",
        face=PALE_GRAY,
        edge=SLATE,
        title_size=15,
        body_size=11,
    )
    arrow(ax, (0.532, 0.52), (0.595, 0.52))

    plot_ax = fig.add_axes([0.62, 0.22, 0.31, 0.48])
    costs = np.array([1.0, 2.1, 3.0, 3.7, 5.4])
    info = np.array([0.28, 0.45, 0.43, 0.72, 0.80])
    labels = list("ABCDE")
    colors = [SLATE, BLUE_HEALTH, TEAL_ENVIRON, GOLD_ACCENT, GREEN_EARTH]
    plot_ax.scatter(costs, info, s=95, c=colors, zorder=3)
    for x, y, label in zip(costs, info, labels):
        plot_ax.text(
            x + 0.08,
            y + 0.015,
            label,
            fontsize=10,
            fontweight="bold",
            color=CHARCOAL,
        )
    plot_ax.plot(
        costs[[0, 1, 3, 4]],
        info[[0, 1, 3, 4]],
        color=TEAL_PRIMARY,
        linestyle="--",
        linewidth=1.8,
        label="Pareto frontier",
    )
    plot_ax.axvline(4.0, color=GOLD_ACCENT, linewidth=1.4, alpha=0.8)
    plot_ax.annotate(
        "selected under\nstated budget",
        xy=(3.7, 0.72),
        xytext=(4.15, 0.56),
        arrowprops={"arrowstyle": "->", "color": GOLD_ACCENT},
        fontsize=9,
        color=CHARCOAL,
    )
    plot_ax.set_xlabel("Total declared cost", fontsize=10)
    plot_ax.set_ylabel("Expected information / utility", fontsize=10)
    plot_ax.set_xlim(0.6, 6.0)
    plot_ax.set_ylim(0.18, 0.9)
    plot_ax.grid(alpha=0.18)
    plot_ax.legend(frameon=False, fontsize=9, loc="lower right")
    footer(
        ax,
        "A preferred design requires a declared budget, utility, constraints, or other decision rule.",
    )
    save(fig, "optimal_design.png")


def pp_eigentest() -> None:
    fig, ax = canvas(
        "pp-eigentest: Fit · Check · Select",
        "Posterior-predictive rank selection with explicit diagnostics and stopping behavior",
        size=(14, 7.2),
    )
    steps = [
        (
            0.035,
            "1  FIT",
            "Observed matrix\n+ mask",
            "Fit PPCA / VBPCA to\nobserved entries; choose capacity\nand refit the selected model",
            BLUE_HEALTH,
            PALE_BLUE,
        ),
        (
            0.375,
            "2  CHECK",
            "Predictive reliability",
            "Held-out RMSE / log score / CRPS\ncoverage · convergence\ncapacity and stopping diagnostics",
            TEAL_PRIMARY,
            PALE_TEAL,
        ),
        (
            0.715,
            "3  SELECT",
            "Model-implied\nspectra",
            "Posterior-predictive PA\nor ordered sequential testing\n→ rank + diagnostics",
            GOLD_ACCENT,
            PALE_GOLD,
        ),
    ]
    for x, heading, title, body, color, pale in steps:
        ax.text(
            x + 0.125,
            0.79,
            heading,
            ha="center",
            fontsize=12,
            color=color,
            fontweight="bold",
        )
        box(
            ax,
            x,
            0.32,
            0.25,
            0.39,
            title,
            body,
            face=pale,
            edge=color,
            title_size=16,
            body_size=11,
        )
    arrow(ax, (0.302, 0.515), (0.358, 0.515), width=2.2)
    arrow(ax, (0.642, 0.515), (0.698, 0.515), width=2.2)
    box(
        ax,
        0.22,
        0.12,
        0.56,
        0.12,
        "Not the primary method",
        "Earlier integer-rank consensus is retained only as a supplementary negative result.",
        face=PALE_RED,
        edge=RED,
        title_size=11.5,
        body_size=10,
    )
    footer(
        ax,
        "Mask-aware fitting does not identify or model the missingness mechanism.",
    )
    save(fig, "pp_eigentest_schematic.png")


def structural_fidelity() -> None:
    fig, ax = canvas(
        "A Better Predictive Score Need Not Imply Structural Admissibility",
        "Outcome-based accuracy and declared scientific constraints answer different questions",
        size=(14, 6.3),
        title_size=19.5,
        subtitle_y=0.89,
    )
    plot_ax = fig.add_axes([0.08, 0.27, 0.54, 0.49])
    time = np.linspace(0, 12, 120)
    lawful = 0.18 + 0.72 / (1 + np.exp(-(time - 5.2) / 1.55))
    violating = 0.16 + 0.96 / (1 + np.exp(-(time - 6.2) / 1.45))
    plot_ax.fill_between(
        time, lawful - 0.06, lawful + 0.06, color=TEAL_ENVIRON, alpha=0.15
    )
    plot_ax.fill_between(
        time,
        violating - 0.05,
        violating + 0.05,
        color=BLUE_HEALTH,
        alpha=0.14,
    )
    plot_ax.plot(
        time,
        lawful,
        color=TEAL_ENVIRON,
        linewidth=2.6,
        label="Forecast A: lawful",
    )
    plot_ax.plot(
        time,
        violating,
        color=BLUE_HEALTH,
        linewidth=2.6,
        label="Forecast B: lower WIS",
    )
    plot_ax.axhline(
        1.0,
        color=RED,
        linestyle="--",
        linewidth=1.8,
        label="declared prevalence bound",
    )
    plot_ax.fill_between(time, 1.0, 1.18, color=RED, alpha=0.08)
    plot_ax.set_xlabel("Forecast horizon")
    plot_ax.set_ylabel("Prevalence proportion")
    plot_ax.set_ylim(0, 1.18)
    plot_ax.grid(alpha=0.18)
    plot_ax.legend(
        frameon=True,
        facecolor=WHITE,
        edgecolor="none",
        framealpha=0.9,
        fontsize=9,
        loc="upper left",
    )

    box(
        ax,
        0.69,
        0.54,
        0.25,
        0.22,
        "Outcome score",
        "WIS / CRPS / log score\ncompares forecasts with\nrealized observations",
        face=PALE_BLUE,
        edge=BLUE_HEALTH,
        title_size=14,
        body_size=10.5,
    )
    box(
        ax,
        0.69,
        0.25,
        0.25,
        0.22,
        "Structural evaluation",
        "checks positivity, bounds,\nconservation, monotonicity,\nor other declared laws",
        face=PALE_RED,
        edge=RED,
        title_size=14,
        body_size=10.5,
    )
    footer(
        ax,
        "Use proper predictive scores and structural diagnostics together; neither substitutes for the other.",
    )
    save(fig, "structural_fidelity_comparison.png")


def vbpca() -> None:
    fig, ax = canvas(
        "VBPCApy",
        "Variational Bayesian PCA for incomplete data with calibrated predictive uncertainty",
        size=(14, 7.2),
    )
    steps = [
        (
            0.035,
            "Observed entries",
            "matrix + explicit mask\nno simple imputation\nmechanism not modeled",
            BLUE_HEALTH,
            PALE_BLUE,
        ),
        (
            0.275,
            "Variational fit",
            "loadings · scores · bias\nnoise variance · ARD\nshared-pattern updates",
            TEAL_PRIMARY,
            PALE_TEAL,
        ),
        (
            0.525,
            "Check & select",
            "convergence diagnostics\nCV component selection\nregime-aware configuration",
            GOLD_ACCENT,
            PALE_GOLD,
        ),
        (
            0.775,
            "Posterior output",
            "factor covariances\ncalibrated predictive\nvariance\nreconstruction / transform",
            GREEN_EARTH,
            PALE_GREEN,
        ),
    ]
    for x, title, body, color, pale in steps:
        box(
            ax,
            x,
            0.35,
            0.18,
            0.36,
            title,
            body,
            face=pale,
            edge=color,
            title_size=14,
            body_size=10,
        )
    for left, right in pairwise(steps):
        arrow(ax, (left[0] + 0.198, 0.53), (right[0] - 0.018, 0.53))
    badge(ax, 0.25, 0.21, "missing-aware", BLUE_HEALTH, width=0.15)
    badge(ax, 0.425, 0.21, "scikit-learn API", TEAL_PRIMARY, width=0.16)
    badge(ax, 0.61, 0.21, "C++ autotuning", TEAL_ENVIRON, width=0.15)
    footer(
        ax,
        "Native masking supports arbitrary observed-entry patterns; it does not by itself make MNAR assumptions identifiable.",
    )
    save(fig, "vbpca_py_schematic.png")


def trade_study() -> None:
    fig, ax = canvas(
        "trade-study",
        "Protocol-driven design and evaluation for scientific simulation studies",
        size=(14, 8),
    )
    steps = [
        (
            0.025,
            "Design space",
            "factors · constraints\nfull / adaptive search\nhierarchical phases",
            BLUE_HEALTH,
            PALE_BLUE,
        ),
        (
            0.275,
            "Simulator\nprotocol",
            "configuration →\ntruth + observations\nreproducible replicates",
            TEAL_PRIMARY,
            PALE_TEAL,
        ),
        (
            0.525,
            "Scoring",
            "proper scores\nstructural diagnostics\ncost and feasibility",
            TEAL_ENVIRON,
            PALE_GREEN,
        ),
        (
            0.775,
            "Decision\nsupport",
            "Pareto fronts\nstacking · sensitivity\nsurrogate recommendations",
            GOLD_ACCENT,
            PALE_GOLD,
        ),
    ]
    for x, title, body, color, pale in steps:
        box(
            ax,
            x,
            0.47,
            0.18,
            0.29,
            title,
            body,
            face=pale,
            edge=color,
            title_size=14,
            body_size=10,
        )
    for left, right in pairwise(steps):
        arrow(ax, (left[0] + 0.198, 0.615), (right[0] - 0.018, 0.615))
    ax.text(
        0.5,
        0.395,
        "SCALE EXPENSIVE STUDIES",
        ha="center",
        fontsize=10.5,
        fontweight="bold",
        color=SLATE,
    )
    badge(ax, 0.195, 0.305, "Hyperband", BLUE_HEALTH, width=0.13)
    badge(ax, 0.345, 0.305, "GP / RF surrogates", TEAL_PRIMARY, width=0.17)
    badge(ax, 0.535, 0.305, "Morris / Sobol", TEAL_ENVIRON, width=0.15)
    badge(ax, 0.705, 0.305, "model stacking", GOLD_ACCENT, width=0.15)
    box(
        ax,
        0.18,
        0.12,
        0.64,
        0.12,
        "General-purpose",
        "model formulations · solver choices · measurement strategies · operational configurations",
        face=PALE_GRAY,
        edge=SLATE,
        title_size=11.5,
        body_size=10,
    )
    footer(
        ax,
        "Synthetic benchmarks make tradeoffs explicit before methods are transferred to real observational data.",
    )
    save(fig, "trade_study_slide.png")


def main() -> None:
    beyond_onehealth()
    flepimop2()
    future_directions()
    obs_model()
    op_engine()
    op_system()
    optimal_design()
    pp_eigentest()
    structural_fidelity()
    vbpca()
    trade_study()


if __name__ == "__main__":
    main()
