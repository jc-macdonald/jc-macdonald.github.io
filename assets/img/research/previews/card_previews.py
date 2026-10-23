# /// script
# requires-python = ">=3.12,<3.14"
# dependencies = ["matplotlib==3.11.2", "numpy==2.5.4"]
# ///
"""Render small-card previews from retained synthetic package computations.

The compact panels and explicit references adapt the author's figure-style
conventions in structural_scores and VBPCApy. No private results are imported.
The full figures and numerical checks remain in the computed directory.
"""

import argparse
import hashlib
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "computed/computed_data.json"
OP_INFER_DATA = HERE.parent / "computed/op_infer_normal_sbc/data.json"
TEAL, GOLD = "#0d6b6e", "#aa7914"
plt.rcParams.update(
    {
        "font.size": 14,
        "axes.labelsize": 14,
        "legend.fontsize": 10,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "svg.hashsalt": "jcm-research-card-previews",
        "figure.facecolor": "white",
    }
)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def panel():
    return plt.subplots(figsize=(7.2, 4.5), layout="constrained")


def export(figure, name):
    path = HERE / f"{name}.svg"
    figure.savefig(path, dpi=300, metadata={"Date": None})
    path.write_text(
        "\n".join(line.rstrip() for line in path.read_text().splitlines()) + "\n"
    )
    plt.close(figure)


def render():
    data = json.loads(DATA.read_text())
    d = data["spatial_diffusion"]
    figure, ax = panel()
    image = ax.pcolormesh(
        d["x"],
        d["times"],
        d["history"],
        shading="nearest",
        cmap="viridis",
        vmin=0.2,
        vmax=1.8,
        rasterized=True,
    )
    ax.set(xlabel="Position on periodic domain", ylabel="Time")
    figure.colorbar(image, ax=ax, label="Field value", shrink=0.85)
    export(figure, "spatial_diffusion")

    d = data["stochastic_ensemble"]
    times, history = np.asarray(d["times"]), np.asarray(d["history"])
    lo, hi = np.quantile(history, [0.05, 0.95], axis=1)
    figure, ax = panel()
    ax.fill_between(
        times, lo, hi, color=TEAL, alpha=0.16, label="Pointwise 5th–95th percentiles"
    )
    ax.plot(times, lo, color=TEAL, linestyle=":", linewidth=1.2)
    ax.plot(times, hi, color=TEAL, linestyle=":", linewidth=1.2)
    for index in range(6):
        ax.step(times, history[:, index], where="post", color=TEAL, alpha=0.7, lw=0.7)
    ax.plot(times, d["reference_mean"], color=GOLD, lw=2.3, label="Analytic mean")
    ax.set(xlabel="Time", ylabel="Transferred units", ylim=(0, 41))
    ax.legend(loc="lower right", frameon=False)
    export(figure, "stochastic_ensemble")

    d = data["replicated_tradeoff"]
    scores, configs, front = np.asarray(d["means"]), d["mean_configs"], d["front"]
    figure, ax = panel()
    for noise, color, marker in [(1.0, TEAL, "o"), (1.5, GOLD, "s")]:
        indices = [i for i, config in enumerate(configs) if config["noise"] == noise]
        ax.scatter(
            scores[indices, 1],
            scores[indices, 0],
            color=color,
            marker=marker,
            s=45,
            label=f"Measurement SD {noise:g}",
        )
    ax.scatter(
        scores[front, 1],
        scores[front, 0],
        facecolors="none",
        edgecolors="#323b43",
        s=135,
        label="Nondominated",
    )
    ax.set(
        xlabel="Assumed cost (arbitrary units)",
        ylabel="Mean squared error",
        yscale="log",
    )
    ax.legend(frameon=False)
    export(figure, "replicated_tradeoff")

    d = data["incomplete_reconstruction"]
    figure, ax = panel()
    limit = float(np.max(np.abs(np.asarray(d["truth"]))))
    image = ax.imshow(
        d["reconstruction"],
        aspect="auto",
        cmap="RdBu_r",
        vmin=-limit,
        vmax=limit,
        interpolation="nearest",
        rasterized=True,
    )
    ax.set(xlabel="Sample", ylabel="Feature")
    figure.colorbar(image, ax=ax, label="Reconstructed value", shrink=0.85)
    export(figure, "incomplete_reconstruction")

    pits = np.asarray(json.loads(OP_INFER_DATA.read_text())["pits"])
    figure, ax = panel()
    bins = 16
    ax.hist(pits, bins=bins, range=(0, 1), color=TEAL, edgecolor="white")
    ax.axhline(
        pits.size / bins,
        color=GOLD,
        linewidth=2,
        linestyle="--",
        label="Uniform expected bin count",
    )
    ax.set(
        xlabel="Randomized-rank PIT",
        ylabel="Replicate count",
        title="64-replicate SBC demonstration",
        xlim=(0, 1),
    )
    ax.text(
        0.02,
        0.96,
        "Underpowered; not calibration evidence",
        transform=ax.transAxes,
        ha="left",
        va="top",
        color="#323b43",
        fontsize=11,
    )
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.18), frameon=False)
    export(figure, "op_infer_normal_sbc")
    manifest = {
        "schema_version": 2,
        "source_sha256": digest(Path(__file__)),
        "input_sha256": {
            "computed_data.json": digest(DATA),
            "op_infer_normal_sbc/data.json": digest(OP_INFER_DATA),
        },
        "files_sha256": {
            path.name: digest(path) for path in sorted(HERE.glob("*.svg"))
        },
    }
    (HERE / "provenance.json").write_text(json.dumps(manifest, indent=2) + "\n")


def check():
    manifest = json.loads((HERE / "provenance.json").read_text())
    if (
        manifest.get("schema_version") != 2
        or manifest["source_sha256"] != digest(Path(__file__))
        or manifest["input_sha256"]
        != {
            "computed_data.json": digest(DATA),
            "op_infer_normal_sbc/data.json": digest(OP_INFER_DATA),
        }
    ):
        raise ValueError("Preview inputs changed; regenerate the compact figures")
    for name, expected in manifest["files_sha256"].items():
        if (
            Path(name).name != name
            or not name.endswith(".svg")
            or digest(HERE / name) != expected
        ):
            raise ValueError(f"Preview artifact changed: {name}")
    print("Verified five compact previews and their source/data hashes")


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--check", action="store_true")
    args = cli.parse_args()
    check() if args.check else render()
