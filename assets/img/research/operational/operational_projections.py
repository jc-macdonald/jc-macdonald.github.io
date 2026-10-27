# /// script
# requires-python = ">=3.12"
# dependencies = ["matplotlib==3.11.2", "numpy==2.5.4", "pandas==2.3.3", "pyarrow==21.0.0"]
# ///
"""Plot ACCIDDA's public submission to the Flu Scenario Modeling Hub, 2025-26 Round 1.

The source is the team's submission file in the public hub repository
(midas-network/flu-scenario-modeling-hub, model-output/ACCIDDA-FlepiMoP/
2025-08-10-ACCIDDA-FlepiMoP.gz.parquet; MIT licence in the team's model
metadata). ``--from-hub PATH`` reduces that 28 MB file to two small tables beside
this script: national weekly quantiles of incident hospitalizations by scenario,
and each trajectory's season total. Without it, the script plots from those
tables; ``--check`` verifies the committed hashes and regenerates.

These are scenario projections from one team's model, conditional on the
round's scenario assumptions. They are not forecasts, not the hub ensemble and
not an evaluation against observed data.
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
        "svg.hashsalt": "jcmacdonald-operational",
        "figure.facecolor": "white",
    }
)

HUB_FILE = "model-output/ACCIDDA-FlepiMoP/2025-08-10-ACCIDDA-FlepiMoP.gz.parquet"
# Round 1 2025-26 scenario table in the hub README (commit 1603bd4).
SCENARIOS = {
    "A-2025-07-29": ("A. Usual coverage", TEAL, "-"),
    "B-2025-07-29": ("B. Low coverage", GOLD, "--"),
    "C-2025-07-29": ("C. No vaccination", RED, "-."),
}
QUANTILES = (0.05, 0.25, 0.5, 0.75, 0.95)
WEEKLY = "flu_2025_26_round1_us_weekly_quantiles.csv"
TOTALS = "flu_2025_26_round1_us_season_totals.csv"
DESCRIPTIONS = {
    "flu_scenario_projections": (
        "ACCIDDA's 2025-26 influenza scenario projections for the United States",
        "Panel a: projected weekly incident influenza hospitalizations in the United States "
        "over 43 weeks from 10 August 2025, under three vaccination scenarios: business as "
        "usual coverage, low coverage and no vaccination. Each scenario shows the median "
        "across 600 trajectories and a shaded 5th to 95th percentile band; the no-vaccination "
        "curve is highest. Panel b: season hospitalizations averted relative to no "
        "vaccination, computed per paired trajectory, as box plots for business as usual "
        "and low coverage; both are positive, and business as usual averts more.",
    ),
}


def reduce_hub_file(parquet):
    """Write the two small tables from the hub submission (national, all ages)."""
    import pandas as pd

    df = pd.read_parquet(parquet, filters=[("target", "==", "inc hosp")])
    us = df[(df.location == "US") & (df.age_group == "0-130")]
    assert set(us.scenario_id) == set(SCENARIOS)
    weekly = (
        us.groupby(["scenario_id", "horizon"])["value"]
        .quantile(list(QUANTILES))
        .unstack()
        .reset_index()
    )
    weekly.columns = ["scenario_id", "horizon", *[f"q{int(100 * q):02d}" for q in QUANTILES]]
    weekly.to_csv(HERE / WEEKLY, index=False, float_format="%.6g")
    totals = (
        us.groupby(["scenario_id", "run_grouping", "stochastic_run"])["value"].sum().reset_index()
    )
    totals.columns = ["scenario_id", "run_grouping", "stochastic_run", "season_total"]
    totals.to_csv(HERE / TOTALS, index=False, float_format="%.6g")
    return {"source_file": HUB_FILE, "source_sha256": digest(Path(parquet))}


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


def flu_scenario_projections():
    weekly = read_csv(WEEKLY)
    totals = read_csv(TOTALS)
    paired = {}
    for row in totals:
        key = (row["run_grouping"], row["stochastic_run"])
        paired.setdefault(key, {})[row["scenario_id"]] = float(row["season_total"])
    assert all(len(v) == len(SCENARIOS) for v in paired.values()), "Unpaired trajectory"
    keys = sorted(paired, key=lambda k: (int(k[0]), int(k[1])))
    averted = {
        s: np.array([paired[k]["C-2025-07-29"] - paired[k][s] for k in keys])
        for s in ("A-2025-07-29", "B-2025-07-29")
    }
    medians = {s: float(np.median([paired[k][s] for k in keys])) for s in SCENARIOS}
    assert medians["C-2025-07-29"] > medians["B-2025-07-29"] > medians["A-2025-07-29"]

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.4), layout="constrained", width_ratios=(1.6, 1))
    for scenario, (label, color, ls) in SCENARIOS.items():
        rows = sorted((r for r in weekly if r["scenario_id"] == scenario), key=lambda r: int(r["horizon"]))
        h = np.array([int(r["horizon"]) for r in rows])
        q = {k: np.array([float(r[k]) for r in rows]) / 1000 for k in ("q05", "q50", "q95")}
        axes[0].fill_between(h, q["q05"], q["q95"], color=color, alpha=0.15, lw=0)
        axes[0].plot(h, q["q50"], color=color, ls=ls, lw=2.2, label=label)
    axes[0].set(
        xlabel="Weeks after 10 August 2025",
        ylabel="Weekly hospitalizations (×1000)",
        xlim=(1, 43),
    )
    axes[0].set_ylim(bottom=0)
    axes[0].legend(loc="upper left", fontsize=11, title="Scenario", title_fontsize=11)

    positions = (0, 1)
    for x, scenario in zip(positions, averted, strict=True):
        label, color, _ = SCENARIOS[scenario]
        axes[1].boxplot(
            averted[scenario] / 1000, positions=[x], widths=0.55, showfliers=False, patch_artist=True,
            boxprops={"facecolor": color, "alpha": 0.35, "edgecolor": color},
            medianprops={"color": CHARCOAL, "lw": 2}, whiskerprops={"color": color}, capprops={"color": color},
        )
    axes[1].axhline(0, color=GREY, lw=1)
    axes[1].set(
        xticks=positions, xticklabels=["A. Usual\ncoverage", "B. Low\ncoverage"],
        ylabel="Averted vs no vaccination (×1000)",
    )
    letter_panels(axes)
    export(fig, "flu_scenario_projections")
    return {
        "season_total_median": medians,
        "averted_median": {s: float(np.median(v)) for s, v in averted.items()},
        "averted_q05_q95": {s: [float(np.quantile(v, 0.05)), float(np.quantile(v, 0.95))] for s, v in averted.items()},
        "fraction_trajectories_with_positive_averted": {s: float(np.mean(v > 0)) for s, v in averted.items()},
        "trajectories": len(keys),
    }


FIGURES = ["flu_scenario_projections"]


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def generate(output, source=None):
    global OUTPUT
    OUTPUT = Path(output)
    data = {"flu_scenario_projections": flu_scenario_projections()}
    (OUTPUT / "operational_data.json").write_text(json.dumps(data, indent=1) + "\n")
    previous = {}
    if (HERE / "provenance.json").exists():
        previous = json.loads((HERE / "provenance.json").read_text()).get("hub", {})
    files = {f"{n}{s}": digest(OUTPUT / f"{n}{s}") for n in FIGURES for s in (".svg", ".pdf", ".png")}
    files["operational_data.json"] = digest(OUTPUT / "operational_data.json")
    manifest = {
        "schema_version": 1,
        "hub": source or previous,
        "source_sha256": digest(Path(__file__)),
        "inputs_sha256": {name: digest(HERE / name) for name in (WEEKLY, TOTALS)},
        "files_sha256": files,
    }
    (OUTPUT / "provenance.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return data


def check():
    manifest = json.loads((HERE / "provenance.json").read_text())
    assert manifest["source_sha256"] == digest(Path(__file__)), "Source changed; regenerate"
    for name, expected in {**manifest["inputs_sha256"], **manifest["files_sha256"]}.items():
        assert digest(HERE / name) == expected, f"Hash mismatch: {name}"
    committed = json.loads((HERE / "operational_data.json").read_text())
    with TemporaryDirectory(prefix="operational-") as folder:
        fresh = flu_scenario_projections_in(folder)
    assert fresh == committed["flu_scenario_projections"], "Recomputed summaries differ"
    print(f"Verified {len(manifest['files_sha256'])} operational artifacts and recomputed summaries")


def flu_scenario_projections_in(folder):
    global OUTPUT
    OUTPUT = Path(folder)
    return flu_scenario_projections()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--from-hub", metavar="PARQUET", help="Reduce the hub submission file first")
    args = parser.parse_args()
    if args.check:
        check()
        return
    source = reduce_hub_file(args.from_hub) if args.from_hub else None
    generate(HERE, source)
    print("Wrote", ", ".join(FIGURES))


if __name__ == "__main__":
    main()
