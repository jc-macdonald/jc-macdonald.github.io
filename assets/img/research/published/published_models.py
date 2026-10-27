# /// script
# requires-python = ">=3.12"
# dependencies = ["matplotlib==3.11.2", "numpy==2.5.4", "scipy==1.18.1"]
# ///
"""Recompute figures from the equations and published parameters of my papers.

Each function reproduces a qualitative result from a published paper using only
the model equations and the parameter values that the paper or its public code
repository released. Nothing is copied from a journal figure; the numerical
values belong to the recomputation. Inputs are the CSV files beside this
script, with their source stated in README.md.

Run with ``uv run --python 3.12 published_models.py``; ``--check`` verifies the
committed hashes and recomputes the references.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from tempfile import TemporaryDirectory

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.stats import spearmanr

HERE = Path(__file__).resolve().parent
OUTPUT = HERE
TEAL, BLUE, GOLD, RED, GREY, CHARCOAL = (
    "#148F77",
    "#2471A3",
    "#87641A",
    "#B03A2E",
    "#5D6D7E",
    "#2C3E50",
)
STRAIN_STYLE = {
    "SAT1": (BLUE, "-", "o"),
    "SAT2": (TEAL, "--", "s"),
    "SAT3": (GOLD, "-.", "^"),
}
# Display names follow Macdonald et al. (2024); the released tables use SAT1, SAT2, SAT3.
STRAIN_LABELS = {"SAT1": "SAT-1", "SAT2": "SAT-2", "SAT3": "SAT-3"}
SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)
ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")
plt.rcParams.update(
    {
        "font.size": 14,
        "axes.labelsize": 14,
        "legend.fontsize": 12,
        "text.color": CHARCOAL,
        "axes.labelcolor": CHARCOAL,
        "xtick.color": GREY,
        "ytick.color": GREY,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "svg.fonttype": "path",
        "svg.hashsalt": "jcmacdonald-published-models",
        "figure.facecolor": "white",
    }
)

DESCRIPTIONS = {
    "fmdv_within_host": (
        "Within-host foot-and-mouth disease virus dynamics by strain, recomputed",
        "Panel a: log10 viral load over 30 days for SAT-1, SAT-2 and SAT-3, recomputed from the "
        "published within-host model at each strain's median parameters; SAT-1 peaks highest "
        "and earliest, SAT-2 lowest, SAT-3 latest. Panel b: the adaptive immune response over the "
        "same period; in this median-parameter simulation SAT-1 rises first, SAT-2 next, and SAT-3 "
        "rises last to the lowest plateau. "
        "Panel c: the strain-level transmission rate against the median host replication rate, "
        "with the host range as a horizontal bar, for the three strains; both increase from "
        "SAT-3 to SAT-2 to SAT-1. Panel d: per-host infectious period against adaptive activation "
        "rate from the paper's host table, decreasing with activation rate.",
    ),
    "covid_lockdown_factor": (
        "Final and peak outbreak size scale as one over one plus the lockdown factor",
        "Panel a: cumulative infections as a percentage of population against the lockdown "
        "rate factor psi on log axes. A line shows the paper's closed-form relation at the U.S. "
        "median reproduction number. For each of 55 state and territorial jurisdictions, an open "
        "marker shows the closed form at its published reproduction number and psi, and a filled "
        "marker joined by a vertical segment shows the model solved over 400 days from its "
        "published initial infections with its published fatigue rate; the filled marker is never "
        "below the open one. Triangles identify fatigue half-lives under 15 days. Panel b: the "
        "same for peak outbreak size, the maximum of I over N.",
    ),
    "ehs_delta_scores": (
        "Tree-likeness of three Austronesian cultural classes, recomputed",
        "Panel a: per-culture delta scores, recomputed from the released cultural distance "
        "matrices, for religion, social organisation and subsistence, shown as box plots with "
        "the individual cultures and a bar at each class mean; religion has the highest scores "
        "and subsistence the lowest. Panel b: the recomputed delta score of each culture against "
        "the SplitsTree output released with the paper; the points lie on the line of equality.",
    ),
}


def letter_panels(axes):
    for label, ax in zip("abcdef", np.atleast_1d(axes).ravel(), strict=False):
        ax.text(
            -0.1, 1.04, f"({label})", transform=ax.transAxes, fontsize=14, fontweight="bold",
            ha="right", va="bottom", color=CHARCOAL,
        )


def annotate_svg(path, name):
    title, desc = DESCRIPTIONS[name]
    root = ET.parse(path).getroot()
    root.set("role", "img")
    root.set("aria-labelledby", "title description")
    for index, (tag, value) in enumerate((("title", title), ("desc", desc))):
        element = ET.Element(f"{{{SVG_NS}}}{tag}")
        element.set("id", "title" if tag == "title" else "description")
        element.text = value
        root.insert(index, element)
    x, y, width, height = root.attrib["viewBox"].split()
    root.insert(
        2,
        ET.Element(
            f"{{{SVG_NS}}}rect",
            {"x": x, "y": y, "width": width, "height": height, "fill": "#ffffff"},
        ),
    )
    ET.ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)


def export(figure, name):
    figure.savefig(OUTPUT / f"{name}.svg", dpi=600, metadata={"Date": None})
    annotate_svg(OUTPUT / f"{name}.svg", name)
    figure.savefig(OUTPUT / f"{name}.pdf", metadata={"CreationDate": None, "ModDate": None})
    figure.savefig(OUTPUT / f"{name}.png", dpi=200)
    plt.close(figure)


def read_csv(name):
    with (HERE / name).open(newline="") as handle:
        return list(csv.DictReader(handle))


# --------------------------------------------------------------------------- FMDV
# Macdonald et al. 2024, The American Naturalist 204(2):133-146, doi 10.1086/730703.
# Within-host model as fitted in the public repository (FMDV-Fitting-Bootstrap,
# Finalized_fitting/ContactDataHaptoStimes.m): innate response x (log10
# haptoglobin), blood virus V (log10 genome copies per mL) and adaptive response A
# (log10 neutralizing titre):
#   dx/dt = lambda + k V/(nu + V) x - d x,   d = 1/21.23,  lambda = 0.8 d min(x_data)
#   dV/dt = (r (1 - V/K) - delta A) V
#   dA/dt = b A V
# Strain-level parameters are medians over the 10 000 Monte Carlo estimates per
# strain released as Output_analysis/FMDVMeansMay9.csv (reduced to the three
# median rows in macdonald2024_amnat_strain_means.csv; README.md records the
# source commit and file hash); the per-host table Output_analysis/QualCompInd.csv
# carries the cross-scale quantities and is copied unchanged.
FMDV_D = 1.0 / 21.23


def fmdv_rhs(t, y, p):
    x, v, a = y
    lam = 0.8 * FMDV_D * p["x_floor"]
    return [
        lam + p["k"] * v / (p["nu"] + v) * x - FMDV_D * x,
        (p["r"] * (1 - v / p["K"]) - p["delta"] * a) * v,
        p["b"] * a * v,
    ]


def fmdv_within_host():
    means = {r["ID"]: r for r in read_csv("macdonald2024_amnat_strain_means.csv")}
    hosts = read_csv("macdonald2024_amnat_host_table.csv")
    strains = ("SAT1", "SAT2", "SAT3")
    params = {}
    for strain in strains:
        params[strain] = {
            key: float(means[strain][key]) for key in ("k", "K", "delta", "b", "r", "nu", "I0", "A0", "P0")
        }
        # The innate baseline used for lambda is the host's minimum haptoglobin;
        # at strain level the median initial innate value stands in for it.
        params[strain]["x_floor"] = params[strain]["I0"]
    times = np.linspace(0.0, 30.0, 601)
    curves = {}
    for strain in strains:
        p = params[strain]
        sol = solve_ivp(
            fmdv_rhs, (0.0, 30.0), [p["I0"], p["P0"], p["A0"]], t_eval=times,
            args=(p,), rtol=1e-10, atol=1e-12, method="DOP853",
        )
        curves[strain] = sol.y
    # Ordering of peak viral load and its timing, from the recomputation.
    peaks = {s: float(curves[s][1].max()) for s in strains}
    peak_times = {s: float(times[np.argmax(curves[s][1])]) for s in strains}
    assert peaks["SAT1"] > peaks["SAT3"] > peaks["SAT2"], peaks
    assert peak_times["SAT3"] > peak_times["SAT2"] > peak_times["SAT1"], peak_times
    rate = np.array([float(h["r"]) for h in hosts])
    beta = np.array([float(h["Transmission"]) for h in hosts])
    activation = np.array([float(h["b"]) for h in hosts])
    infectious = np.array([float(h["infectPeriod"]) for h in hosts])
    host_strain = np.array([h["Serotype"] for h in hosts])
    # Transmission rate was estimated per strain in the paper (one value per
    # strain), so the replication-transmission relation is drawn at strain level:
    # median host r against the strain's beta, with the host spread in r shown.
    strain_r = {s_: float(np.median(rate[host_strain == s_])) for s_ in strains}
    strain_r_range = {s_: (float(rate[host_strain == s_].min()), float(rate[host_strain == s_].max())) for s_ in strains}
    strain_beta = {s_: float(beta[host_strain == s_][0]) for s_ in strains}
    for s_ in strains:
        assert np.all(beta[host_strain == s_] == strain_beta[s_])
    rho_bg = spearmanr(activation, infectious)
    assert rho_bg.statistic < -0.7
    assert strain_beta["SAT1"] > strain_beta["SAT2"] > strain_beta["SAT3"]
    assert strain_r["SAT1"] > strain_r["SAT2"] > strain_r["SAT3"]

    fig, axes = plt.subplots(2, 2, figsize=(10, 8.4), layout="constrained")
    for strain in strains:
        color, ls, marker = STRAIN_STYLE[strain]
        axes[0, 0].plot(times, curves[strain][1], color=color, ls=ls, lw=2.2, label=STRAIN_LABELS[strain])
        axes[0, 1].plot(times, curves[strain][2], color=color, ls=ls, lw=2.2, label=STRAIN_LABELS[strain])
    axes[0, 0].set(xlabel="Days since infection", ylabel="Virus, log$_{10}$ copies per mL", ylim=(0, 9))
    axes[0, 1].set(xlabel="Days since infection", ylabel="Adaptive response, log$_{10}$ titre")
    axes[0, 0].legend(title="Strain, median parameters", loc="upper right", fontsize=11, title_fontsize=11)
    for strain in strains:
        color, _, marker = STRAIN_STYLE[strain]
        lo, hi = strain_r_range[strain]
        axes[1, 0].plot([lo, hi], [strain_beta[strain]] * 2, color=color, lw=1.6, alpha=0.7)
        axes[1, 0].plot(strain_r[strain], strain_beta[strain], marker, color=color, ms=10, mec="white", label=STRAIN_LABELS[strain])
        sel = host_strain == strain
        axes[1, 1].plot(activation[sel], infectious[sel], marker, color=color, ms=8, mec="white", label=STRAIN_LABELS[strain])
    axes[1, 0].set(
        xlabel="Replication rate $r$ (per day), host median and range",
        ylabel="Transmission rate $\\beta$ (per day)",
        ylim=(1.0, 3.0),
    )
    axes[1, 1].set(xlabel="Adaptive activation rate $b$, by host", ylabel="Infectious period (days)")
    axes[1, 0].legend(title="Strain", loc="upper left", fontsize=11, title_fontsize=11)
    axes[1, 1].legend(title="Strain, individual hosts", loc="upper right", fontsize=11, title_fontsize=11)
    letter_panels(axes)
    export(fig, "fmdv_within_host")
    return {
        "strain_median_parameters": params,
        "times": times.tolist(),
        "virus": {s: curves[s][1].tolist() for s in strains},
        "adaptive": {s: curves[s][2].tolist() for s in strains},
        "innate": {s: curves[s][0].tolist() for s in strains},
        "peak_log10_virus": peaks,
        "peak_time_days": peak_times,
        "hosts": {
            "r": rate.tolist(), "transmission": beta.tolist(),
            "b": activation.tolist(), "infectious_period": infectious.tolist(),
            "strain": [h["Serotype"] for h in hosts],
        },
        "strain_median_r": strain_r,
        "strain_r_range": strain_r_range,
        "strain_transmission": strain_beta,
        "spearman_b_vs_infectious_period_hosts": [float(rho_bg.statistic), float(rho_bg.pvalue)],
    }


# --------------------------------------------------------------------------- COVID-19
# Macdonald et al. 2021, Royal Society Open Science 8:210227, doi 10.1098/rsos.210227.
# Model (eq. 2.1; public code programfilesUSCOVID/USStateFitsSimplest.m, theModel):
#   dS/dt  = -(1 + psi) beta S I / N + alpha S_q
#   dSq/dt =  psi beta S I / N - alpha S_q
#   dI/dt  =  beta S I / N - I / T,   T = 7.5 days
# Closed forms (eqs. 4.1-4.2) with alpha = 0 and I0 -> 0:
#   ln s_inf = R0 (s_inf - 1),  C = (1 - s_inf) / (1 + psi),  P = (1/(1+psi)) (1/R0)(R0 - ln R0 - 1).
# Jurisdiction parameters are Table 2 of the paper (macdonald2021_rsos_table2.csv).
T_INF = 7.5


def covid_rhs(t, y, beta, psi, alpha):
    s, sq, i = y
    force = beta * i
    return [-(1 + psi) * force * s + alpha * sq, psi * force * s - alpha * sq, force * s - i / T_INF]


def covid_final_and_peak(r0, psi, alpha, days=400.0, i0=1e-6):
    """Cumulative infected fraction at ``days`` and the peak of I/N over [0, days]."""
    beta = r0 / T_INF
    sol = solve_ivp(
        covid_rhs, (0.0, days), [1.0 - i0, 0.0, i0], args=(beta, psi, alpha),
        rtol=1e-10, atol=1e-13, dense_output=True, max_step=0.5,
    )
    tt = np.linspace(0.0, days, 8001)
    s, sq, i = sol.sol(tt)
    cumulative = 1.0 - s[-1] - sq[-1]
    return float(cumulative), float(i.max())


def covid_closed_form(r0, psi):
    s_inf = brentq(lambda s: np.log(s) - r0 * (s - 1.0), 1e-12, 1.0 - 1e-12)
    final = (1.0 - s_inf) / (1.0 + psi)
    peak = (1.0 / (1.0 + psi)) * (1.0 / r0) * (r0 - np.log(r0) - 1.0)
    return float(final), float(peak)


def covid_lockdown_factor():
    """The paper's closed-form scaling, and how fatigue moves each jurisdiction off it.

    Equations 4.1 and 4.2 hold for alpha = 0 (no lockdown fatigue). At each
    jurisdiction's published R0 and psi the closed form gives a final size and
    a peak; solving the model with that jurisdiction's published fatigue rate
    shows the departure the paper discusses: fatigue returns quarantined people
    to circulation and raises both quantities above the no-fatigue value.
    """
    # The 55 state and territorial jurisdictions; the "United States" row is the
    # paper's national aggregate and is not a separate jurisdiction.
    table = [
        r for r in read_csv("macdonald2021_rsos_table2.csv")
        if r["state"] not in ("mean", "median", "std. dev.", "United States")
    ]
    assert len(table) == 55, len(table)
    r0_us = 2.32  # U.S. median R0 from the paper (Table 5; approximate 95% CI 2.21 to 2.36)
    psi_grid = np.geomspace(1.0, 1200.0, 200)
    closed = np.array([covid_closed_form(r0_us, p) for p in psi_grid])
    # The closed form assumes alpha = 0; check it against the solved model at alpha = 0.
    for p in (2.0, 20.0, 200.0):
        num = covid_final_and_peak(r0_us, p, 0.0, i0=1e-8)
        cf = covid_closed_form(r0_us, p)
        assert abs(num[0] - cf[0]) / cf[0] < 2e-3 and abs(num[1] - cf[1]) / cf[1] < 2e-3, (p, num, cf)
    points = []
    for row in table:
        r0, psi, half = float(row["R0"]), float(row["psi"]), float(row["fatigue_half_life_days"])
        i0 = float(row["I0"]) / float(row["population"])  # published initial infections, as a fraction
        alpha = np.log(2.0) / half
        cf_final, cf_peak = covid_closed_form(r0, psi)
        final, peak = covid_final_and_peak(r0, psi, alpha, i0=i0)
        points.append({
            "state": row["state"], "R0": r0, "psi": psi, "fatigue_half_life_days": half,
            "I0_fraction": i0,
            "closed_form_final": cf_final, "closed_form_peak": cf_peak,
            "model_final_400d": final, "model_peak_400d": peak,
        })
    # With fatigue, neither 400-day quantity falls below its no-fatigue closed form
    # (a small tolerance covers the finite I0 and horizon).
    assert all(p["model_final_400d"] >= 0.99 * p["closed_form_final"] for p in points)
    assert all(p["model_peak_400d"] >= 0.99 * p["closed_form_peak"] for p in points)
    strong = [p for p in points if p["fatigue_half_life_days"] < 15.0]
    weak = [p for p in points if p["fatigue_half_life_days"] >= 15.0]

    fig, axes = plt.subplots(1, 2, figsize=(10, 5.6), layout="constrained")
    for ax, key, ylabel in (
        (axes[0], "final", "Cumulative infections, % of population"),
        (axes[1], "peak", "Peak outbreak size, max $I/N$, % of population"),
    ):
        col = 0 if key == "final" else 1
        ax.plot(psi_grid, 100 * closed[:, col], color=CHARCOAL, lw=2.2, label=f"Closed form at $R_0$ = {r0_us}")
        for group, marker, color, label in (
            (weak, "o", TEAL, "fatigue half-life ≥ 15 days"),
            (strong, "^", RED, "fatigue half-life < 15 days"),
        ):
            xs = [p["psi"] for p in group]
            for p in group:
                ax.plot(
                    [p["psi"], p["psi"]],
                    [100 * p[f"closed_form_{key}"], 100 * p[f"model_{key}_400d"]],
                    color=color, lw=0.9, alpha=0.6,
                )
            ax.plot(
                xs, [100 * p[f"closed_form_{key}"] for p in group], marker, color=color, ms=5,
                mfc="white", mew=1.4, label=f"Closed form at each jurisdiction, {label}" if col == 0 else None,
            )
            ax.plot(
                xs, [100 * p[f"model_{key}_400d"] for p in group], marker, color=color, ms=6,
                mec="white", label=f"Model over 400 days with published fatigue, {label}" if col == 0 else None,
            )
        ax.set(xscale="log", yscale="log", xlabel="Lockdown rate factor $\\psi$", ylabel=ylabel)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="outside lower center", ncol=2, fontsize=10, frameon=True)
    letter_panels(axes)
    export(fig, "covid_lockdown_factor")
    return {
        "r0_reference": r0_us,
        "psi_grid": psi_grid.tolist(),
        "closed_form_final": closed[:, 0].tolist(),
        "closed_form_peak": closed[:, 1].tolist(),
        "jurisdictions": points,
    }


# --------------------------------------------------------------------------- EHS
# Macdonald, Blanco-Portillo, Feldman and Ram 2024, Evolutionary Human Sciences 6:e51,
# doi 10.1017/ehs.2024.45. Delta scores (Holland et al. 2002) of the pairwise cultural
# distance matrices released in yoavram-lab/Cultural-Clusters-and-Networks (dist/*.dist,
# commit eee7c25). For a quartet whose three pairings have distance sums
# s1 <= s2 <= s3, delta = (s3 - s2)/(s3 - s1), and zero when s3 = s1. A culture's
# score is the mean over all quartets that contain it. The SplitsTree output released
# in the same repository (csv/delta_*.csv) is the independent check.
EHS_CLASSES = (
    ("Religion", "rel", RED, "o"),
    ("Social organisation", "kin", BLUE, "s"),
    ("Subsistence", "sub", GOLD, "^"),
)
EHS_PAPER_MEANS = {"rel": 0.32, "kin": 0.25, "sub": 0.22}  # Figure 2a of the paper


def read_distances(name):
    lines = (HERE / name).read_text().split("\n")
    n = int(lines[0])
    names = [line.split()[0] for line in lines[1 : n + 1]]
    matrix = np.array([[float(x) for x in line.split()[1:]] for line in lines[1 : n + 1]])
    assert matrix.shape == (n, n) and np.allclose(matrix, matrix.T)
    return names, matrix


def quartet_delta(distances):
    """Mean delta score over all quartets containing each taxon."""
    n = len(distances)
    total, count = np.zeros(n), np.zeros(n)
    k_all, l_all = np.triu_indices(n, 1)
    for i in range(n - 3):
        for j in range(i + 1, n - 2):
            keep = k_all > j
            k, l = k_all[keep], l_all[keep]
            sums = np.sort(
                np.stack(
                    [
                        distances[i, j] + distances[k, l],
                        distances[i, k] + distances[j, l],
                        distances[i, l] + distances[j, k],
                    ]
                ),
                axis=0,
            )
            spread = sums[2] - sums[0]
            delta = np.where(spread > 0, (sums[2] - sums[1]) / np.where(spread > 0, spread, 1.0), 0.0)
            for index in (i, j):
                total[index] += delta.sum()
                count[index] += delta.size
            for index in (k, l):
                np.add.at(total, index, delta)
                np.add.at(count, index, 1)
    return total / count


def ehs_delta_scores():
    results = {}
    for label, key, _, _ in EHS_CLASSES:
        names, distances = read_distances(f"macdonald2024_ehs_{key}_distances.dist")
        delta = quartet_delta(distances)
        released = {
            row["Taxon"]: float(row["Delta Score "])
            for row in read_csv(f"macdonald2024_ehs_{key}_delta_splitstree.csv")
        }
        assert set(released) == set(names), key
        released_aligned = np.array([released[name] for name in names])
        assert np.max(np.abs(delta - released_aligned)) < 1e-3, key
        assert round(float(delta.mean()), 2) == EHS_PAPER_MEANS[key], (key, delta.mean())
        results[key] = {
            "label": label,
            "cultures": names,
            "delta": delta.tolist(),
            "delta_splitstree": released_aligned.tolist(),
            "mean": float(delta.mean()),
            "max_abs_difference_from_splitstree": float(np.max(np.abs(delta - released_aligned))),
        }
    assert results["rel"]["mean"] > results["kin"]["mean"] > results["sub"]["mean"]

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.6), layout="constrained")
    rng = np.random.default_rng(20241206)
    for x, (label, key, color, marker) in enumerate(EHS_CLASSES):
        values = np.array(results[key]["delta"])
        axes[0].boxplot(
            values, positions=[x], widths=0.55, showfliers=False,
            medianprops={"color": CHARCOAL}, boxprops={"color": GREY}, whiskerprops={"color": GREY},
            capprops={"color": GREY},
        )
        axes[0].plot(x + rng.uniform(-0.2, 0.2, values.size), values, marker, color=color, ms=4, alpha=0.55)
        axes[0].plot([x - 0.3, x + 0.3], [values.mean()] * 2, color=color, lw=3)
        axes[1].plot(results[key]["delta_splitstree"], values, marker, color=color, ms=5, alpha=0.7, label=label)
    axes[0].plot([], [], color=GREY, lw=3, label="Class mean")
    axes[0].set(
        xticks=range(len(EHS_CLASSES)), xticklabels=[label.replace(" ", "\n") for label, *_ in EHS_CLASSES],
        ylabel="$\\delta$-score per culture",
    )
    axes[0].legend(loc="upper right", fontsize=11)
    lo = min(min(r["delta"]) for r in results.values()) - 0.02
    hi = max(max(r["delta"]) for r in results.values()) + 0.02
    axes[1].plot([lo, hi], [lo, hi], color=CHARCOAL, ls=":", lw=1.4, label="Equality")
    axes[1].set(
        xlim=(lo, hi), ylim=(lo, hi), aspect="equal",
        xlabel="$\\delta$-score, released SplitsTree output", ylabel="$\\delta$-score, recomputed",
    )
    axes[1].legend(loc="upper left", fontsize=11)
    letter_panels(axes)
    export(fig, "ehs_delta_scores")
    return results


FIGURES = ["fmdv_within_host", "covid_lockdown_factor", "ehs_delta_scores"]
INPUTS = [
    "macdonald2024_amnat_strain_means.csv",
    "macdonald2024_amnat_host_table.csv",
    "macdonald2021_rsos_table2.csv",
    *(f"macdonald2024_ehs_{key}_distances.dist" for _, key, _, _ in EHS_CLASSES),
    *(f"macdonald2024_ehs_{key}_delta_splitstree.csv" for _, key, _, _ in EHS_CLASSES),
]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def generate(output):
    global OUTPUT
    OUTPUT = Path(output)
    data = {
        "fmdv_within_host": fmdv_within_host(),
        "covid_lockdown_factor": covid_lockdown_factor(),
        "ehs_delta_scores": ehs_delta_scores(),
    }
    (OUTPUT / "published_data.json").write_text(json.dumps(data, indent=1) + "\n")
    files = {}
    for name in FIGURES:
        for suffix in (".svg", ".pdf", ".png"):
            files[f"{name}{suffix}"] = digest(OUTPUT / f"{name}{suffix}")
    files["published_data.json"] = digest(OUTPUT / "published_data.json")
    manifest = {
        "schema_version": 1,
        "source_sha256": digest(Path(__file__)),
        "inputs_sha256": {name: digest(HERE / name) for name in INPUTS},
        "files_sha256": files,
    }
    (OUTPUT / "provenance.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return data


def check():
    manifest = json.loads((HERE / "provenance.json").read_text())
    assert manifest["source_sha256"] == digest(Path(__file__)), "Source changed; regenerate"
    for name, expected in manifest["inputs_sha256"].items():
        assert digest(HERE / name) == expected, f"Input changed: {name}"
    for name, expected in manifest["files_sha256"].items():
        assert digest(HERE / name) == expected, f"Hash mismatch: {name}"
    committed = json.loads((HERE / "published_data.json").read_text())
    with TemporaryDirectory(prefix="published-models-") as folder:
        fresh = generate(folder)
    for strain in ("SAT1", "SAT2", "SAT3"):
        for key in ("virus", "adaptive", "innate"):
            np.testing.assert_allclose(fresh["fmdv_within_host"][key][strain], committed["fmdv_within_host"][key][strain], rtol=1e-9)
    np.testing.assert_allclose(fresh["covid_lockdown_factor"]["closed_form_final"], committed["covid_lockdown_factor"]["closed_form_final"], rtol=1e-10)
    np.testing.assert_allclose(fresh["covid_lockdown_factor"]["closed_form_peak"], committed["covid_lockdown_factor"]["closed_form_peak"], rtol=1e-10)
    for key in ("model_final_400d", "model_peak_400d", "closed_form_final", "closed_form_peak"):
        np.testing.assert_allclose(
            [p[key] for p in fresh["covid_lockdown_factor"]["jurisdictions"]],
            [p[key] for p in committed["covid_lockdown_factor"]["jurisdictions"]], rtol=1e-8,
        )
    for _, key, _, _ in EHS_CLASSES:
        assert fresh["ehs_delta_scores"][key]["cultures"] == committed["ehs_delta_scores"][key]["cultures"]
        np.testing.assert_allclose(
            fresh["ehs_delta_scores"][key]["delta"], committed["ehs_delta_scores"][key]["delta"], rtol=1e-12
        )
    print(f"Verified {len(manifest['files_sha256'])} published-model artifacts and recomputed references")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        check()
    else:
        generate(HERE)
        print("Wrote", ", ".join(FIGURES))


if __name__ == "__main__":
    main()
