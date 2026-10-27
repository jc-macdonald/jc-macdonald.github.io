# /// script
# requires-python = ">=3.12,<3.14"
# dependencies = [
#   "matplotlib==3.11.2", "numpy==2.5.4", "op-system==0.10.0",
#   "op-engine==0.9.0", "trade-study[pareto]==0.6.0", "vbpca-py==0.5.0",
# ]
# ///
"""Compute synthetic package demonstrations and retain their numerical inputs.

Run with ``uv run --python 3.12 computed_examples.py``. The figures illustrate
software behavior; they do not report findings from an application study.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import xml.etree.ElementTree as ET
from importlib.metadata import version
from pathlib import Path
from tempfile import TemporaryDirectory

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import trade_study as ts
from matplotlib.patches import Patch
from op_engine import BatchedDirectSSASolver, CoreSolver, FiringRecorder, ModelCore
from op_engine.core_solver import RunConfig
from op_system import compile_spec
from vbpca_py import VBPCA, MissingAwareOneHotEncoder

HERE = Path(__file__).resolve().parent
OUTPUT = HERE
SVG_NS = "http://www.w3.org/2000/svg"
SEED = 20261019
TEAL, BLUE, GOLD, GREY = "#0d6b6e", "#2471a3", "#aa7914", "#61717c"
plt.rcParams.update(
    {
        "font.size": 10,
        "axes.titlesize": 11,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "legend.frameon": False,
        "legend.fontsize": 8,
        "svg.hashsalt": "jcm-computed-examples",
        "pdf.fonttype": 42,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "savefig.dpi": 200,
    }
)


def export(figure, name):
    """Write vector and card exports with deterministic creation metadata."""
    figure.savefig(OUTPUT / f"{name}.svg", dpi=600, metadata={"Date": None})
    figure.savefig(
        OUTPUT / f"{name}.pdf", metadata={"CreationDate": None, "ModDate": None}
    )
    figure.savefig(OUTPUT / f"{name}.png")
    plt.close(figure)


def diffusion():
    """Compile a periodic spatial stencil and check its known Fourier modes."""
    n, diffusivity = 64, 0.02
    x, times = np.arange(n) / n, np.linspace(0, 3, 121)
    initial = 1 + 0.55 * np.cos(2 * np.pi * x) + 0.25 * np.cos(6 * np.pi * x)
    # Spatial discretization is explicit here: op_system compiles its named-axis
    # contraction, while op_engine supplies temporal integration.
    identity = np.eye(n)
    stencil = (
        diffusivity
        * n**2
        * (np.roll(identity, 1, axis=1) - 2 * identity + np.roll(identity, -1, axis=1))
    )
    spec = {
        "kind": "expr",
        "axes": [
            {
                "name": "cell",
                "type": "categorical",
                "coords": [f"c{i}" for i in range(n)],
            }
        ],
        "state": ["u[cell]"],
        "equations": {
            "u[cell]": "apply_along(L[cell,cell:j]*u[cell:j], cell=j, kernel=sum)"
        },
    }
    compiled = compile_spec(spec)
    np.testing.assert_allclose(
        compiled.eval_fn(0, initial, L=stencil), stencil @ initial, atol=2e-13
    )
    core = ModelCore(1, n, times)
    core.set_initial_state(initial[None, :])
    CoreSolver(core).run(
        lambda t, state: compiled.eval_fn(t, state.reshape(-1), L=stencil).reshape(
            1, n
        ),
        config=RunConfig(method="rk4", fixed_max_step=0.001),
    )
    history = np.asarray(core.state_array)[:, 0]
    reference = np.ones_like(history)
    for mode, amplitude in [(1, 0.55), (3, 0.25)]:
        eigenvalue = -4 * diffusivity * n**2 * np.sin(np.pi * mode / n) ** 2
        reference += (
            amplitude
            * np.exp(eigenvalue * times[:, None])
            * np.cos(2 * np.pi * mode * x)
        )
    error = float(np.max(np.abs(history - reference)))
    assert error < 2e-10
    np.testing.assert_allclose(history.mean(axis=1), 1, atol=1e-13)
    fig, axes = plt.subplots(1, 2, figsize=(8, 3.5), layout="constrained")
    image = axes[0].pcolormesh(
        x,
        times,
        history,
        shading="nearest",
        cmap="viridis",
        vmin=0.2,
        vmax=1.8,
        rasterized=True,
    )
    axes[0].set(
        xlabel="Position on a periodic domain",
        ylabel="Time",
        title="Periodic diffusion, 64 spatial cells",
    )
    fig.colorbar(image, ax=axes[0], label="Field value", shrink=0.8)
    profiles = [
        (0, BLUE, "-", "o"),
        (10, TEAL, "--", "s"),
        (40, GOLD, "-.", "^"),
        (120, GREY, ":", "D"),
    ]
    for i, color, line_style, marker in profiles:
        axes[1].plot(
            x,
            history[i],
            color=color,
            ls=line_style,
            marker=marker,
            markevery=8,
            ms=3.5,
            label=f"t = {times[i]:g}",
        )
    axes[1].set(
        xlabel="Position", ylabel="Field value", title="Field profiles", ylim=(0.1, 1.9)
    )
    axes[1].legend()
    export(fig, "spatial_diffusion")
    return {
        "spec": spec,
        "x": x.tolist(),
        "times": times.tolist(),
        "stencil": stencil.tolist(),
        "history": history.tolist(),
        "reference": reference.tolist(),
        "max_temporal_error": error,
    }


def ssa():
    """Run independent stochastic transfers and retain event-count evidence."""
    count, population, rate = 512, 40, 0.6
    times = np.linspace(0, 5, 81)
    initial = np.zeros((2, count))
    initial[0] = population
    core = ModelCore(2, count, times)
    core.set_initial_state(initial)
    recorder = FiringRecorder((0,))
    solver = BatchedDirectSSASolver(core, np.asarray([[-1.0], [1.0]]))
    solver.run(
        lambda _times, state: rate * state[:1],
        rng=np.random.SeedSequence(SEED),
        replicate_ids=tuple(range(count)),
        recorder=recorder,
    )
    history = np.asarray(core.state_array)[:, 1]
    np.testing.assert_array_equal(np.asarray(core.state_array).sum(axis=1), population)
    np.testing.assert_array_equal(recorder.cumulative[:, 0], history)
    mean, lo, hi = history.mean(axis=1), *np.quantile(history, [0.05, 0.95], axis=1)
    exact = population * (1 - np.exp(-rate * times))
    se = np.sqrt(
        population * (1 - np.exp(-rate * times)) * np.exp(-rate * times) / count
    )
    # Pointwise variability; this is not a simultaneous coverage test.
    assert np.max(np.abs(mean - exact) / np.maximum(se, 1e-12)) < 6
    fig, axes = plt.subplots(1, 2, figsize=(8, 3.5), layout="constrained")
    axes[0].fill_between(
        times, lo, hi, color=TEAL, alpha=0.18, label="5th–95th percentile of runs"
    )
    axes[0].plot(times, lo, color=TEAL, ls=":", lw=1.1)
    axes[0].plot(times, hi, color=TEAL, ls=":", lw=1.1)
    for i in range(4):
        axes[0].step(times, history[:, i], where="post", color=TEAL, alpha=0.7, lw=0.7)
    axes[0].plot(times, mean, color=TEAL, label="Mean of 512 independent runs")
    axes[0].plot(times, exact, color=GOLD, ls="--", label="Analytic mean")
    axes[0].set(
        xlabel="Time",
        ylabel="Transferred units",
        title="Stochastic transfer paths",
    )
    axes[0].legend(loc="lower right")
    values = np.arange(population + 1)
    import math

    p = 1 - np.exp(-rate * times[-1])
    pmf = np.asarray(
        [
            math.comb(population, int(k)) * p**k * (1 - p) ** (population - k)
            for k in values
        ]
    )
    axes[1].hist(
        history[-1],
        bins=np.arange(population + 2) - 0.5,
        density=True,
        color=TEAL,
        alpha=0.5,
        label="Simulated final values",
    )
    axes[1].plot(values, pmf, "o-", ms=3, color=GOLD, label="Binomial reference")
    axes[1].set(
        xlabel="Transferred units at t = 5",
        ylabel="Probability",
        title="Final distribution",
        xlim=(30, 40.5),
    )
    axes[1].legend()
    export(fig, "stochastic_ensemble")
    return {
        "seed": SEED,
        "rate": rate,
        "population": population,
        "replicate_ids": list(range(count)),
        "times": times.tolist(),
        "history": history.tolist(),
        "firing_counts": recorder.counts.tolist(),
        "reference_mean": exact.tolist(),
        "pointwise_se": se.tolist(),
    }


class SampleMean:
    """Nested sample banks keep comparisons paired across designs."""

    def generate(self, config, *, rep=0):
        bank = np.random.default_rng(np.random.SeedSequence([SEED, rep])).normal(
            size=128
        )
        n = int(config["samples"])
        # A cheaper measurement has deliberately specified, synthetic noise.
        noise = float(config["noise"])
        return 0.0, noise * bank[:n]


class ErrorCost:
    def score(self, truth, observed, config):
        n, noise = int(config["samples"]), float(config["noise"])
        return {
            "error": float((observed.mean() - truth) ** 2),
            "cost": float(
                n * (1.0 if noise == 1.0 else 0.55) + (8 if noise == 1.0 else 0)
            ),
        }


def tradeoff():
    """Use replicated study scores and the package's actual Pareto extractor."""
    grid = ts.build_grid(
        [
            ts.Factor("samples", ts.FactorType.DISCRETE, levels=[8, 16, 32, 64, 128]),
            ts.Factor("noise", ts.FactorType.DISCRETE, levels=[1.0, 1.5]),
        ],
        method="full",
    )
    observables = [
        ts.Observable("error", ts.Direction.MINIMIZE),
        ts.Observable("cost", ts.Direction.MINIMIZE),
    ]
    results = ts.run_grid(SampleMean(), ErrorCost(), grid, observables, n_reps=512)
    means = results.aggregate_replicates()
    front = ts.extract_front(means.scores, [o.direction for o in observables])
    for config, row in zip(means.configs, means.scores, strict=True):
        variance = float(config["noise"]) ** 2 / int(config["samples"])
        assert abs(row[0] - variance) < 6 * np.sqrt(2 / 512) * variance
    # Independent dominance check, including both objective directions.
    expected = [
        i
        for i, row in enumerate(means.scores)
        if not any(
            np.all(other <= row) and np.any(other < row) for other in means.scores
        )
    ]
    assert set(map(int, front)) == set(expected)
    fig, axes = plt.subplots(1, 2, figsize=(8, 3.5), layout="constrained")
    for noise, color, marker, line_style, reference_style, label in [
        (1.0, TEAL, "o", "-", ":", "Standard noise"),
        (1.5, GOLD, "s", "--", "-.", "Cheaper, noisier measurements"),
    ]:
        indices = [i for i, c in enumerate(means.configs) if c["noise"] == noise]
        indices.sort(key=lambda i: means.configs[i]["samples"])
        values = means.scores[indices]
        axes[0].plot(
            values[:, 1],
            values[:, 0],
            marker=marker,
            ls=line_style,
            ms=4,
            color=color,
            label=label,
        )
        n = np.asarray([means.configs[i]["samples"] for i in indices])
        axes[1].plot(
            n,
            values[:, 0],
            marker=marker,
            ls=line_style,
            color=color,
            label=label,
        )
        axes[1].plot(n, noise**2 / n, ls=reference_style, color=color)
    axes[0].scatter(
        means.scores[front, 1],
        means.scores[front, 0],
        s=90,
        facecolors="none",
        edgecolors=GREY,
        label="Nondominated designs",
    )
    axes[0].set(
        xlabel="Assumed measurement cost (arbitrary units)",
        ylabel="Mean squared estimation error",
        title="Mean error and assumed cost",
        yscale="log",
    )
    axes[0].legend()
    axes[1].set(
        xlabel="Measurements per replicate",
        ylabel="Mean squared estimation error",
        title="512 replicates per design",
        xscale="log",
        yscale="log",
    )
    axes[1].text(
        0.05,
        0.06,
        "Dotted/dash-dot curves: analytic variance σ² / n",
        transform=axes[1].transAxes,
        color=GREY,
        fontsize=8,
    )
    export(fig, "replicated_tradeoff")
    with (OUTPUT / "design_comparison.csv").open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["samples", "noise", "mean_squared_error", "assumed_cost", "pareto"]
        )
        for i, c in enumerate(means.configs):
            writer.writerow(
                [c["samples"], c["noise"], *means.scores[i], int(i in front)]
            )
    return {
        "seed": SEED,
        "replicates": 512,
        "configs": results.configs,
        "scores": results.scores.tolist(),
        "metadata": results.metadata,
        "mean_configs": means.configs,
        "means": means.scores.tolist(),
        "front": front.tolist(),
    }


def reconstruction():
    """Fit observed entries only and evaluate on an independent held-out mask."""
    rng = np.random.default_rng(SEED)
    features, samples = 24, 80
    position = np.linspace(0, 1, features)
    loadings = np.stack(
        [np.sin(2 * np.pi * position), np.cos(4 * np.pi * position)], axis=1
    )
    scores = rng.normal(size=(2, samples))
    truth = loadings @ scores
    data = truth + 0.2 * rng.normal(size=truth.shape)
    observed = rng.uniform(size=data.shape) > 0.35
    model = VBPCA(n_components=2, maxiters=300, random_state=SEED, verbose=0)
    model.fit_transform(data, mask=observed)
    reconstructed = np.asarray(model.reconstruction_)
    heldout = ~observed
    rmse = float(np.sqrt(np.mean((reconstructed[heldout] - data[heldout]) ** 2)))
    assert np.isfinite(reconstructed).all() and rmse < 0.5
    fig, axes = plt.subplots(1, 3, figsize=(9, 3.4), layout="constrained")
    cmap = plt.get_cmap("RdBu_r").copy()
    missing_color = "#5f6368"
    cmap.set_bad(missing_color)
    scale = 3
    for ax, matrix, title in zip(
        axes,
        [truth, np.where(observed, data, np.nan), reconstructed],
        [
            "Synthetic two-pattern signal",
            "Observed entries only",
            "VBPCA reconstruction",
        ],
    ):
        image = ax.imshow(
            matrix,
            aspect="auto",
            cmap=cmap,
            vmin=-scale,
            vmax=scale,
            interpolation="nearest",
        )
        ax.set(xlabel="Sample", ylabel="Feature", title=title)
    fig.colorbar(image, ax=axes, label="Value", shrink=0.75, extend="both")
    axes[1].legend(
        handles=[
            Patch(facecolor=missing_color, label="Not observed (excluded from fit)")
        ],
        loc="upper center",
        bbox_to_anchor=(0.5, -0.18),
        frameon=False,
        fontsize=8,
    )
    export(fig, "incomplete_reconstruction")
    return {
        "seed": SEED,
        "truth": truth.tolist(),
        "data": data.tolist(),
        "observed_mask": observed.tolist(),
        "reconstruction": reconstructed.tolist(),
        "heldout_rmse": rmse,
        "noise_sd": 0.2,
        "n_components": 2,
        "maxiters": 300,
    }


def project_simplex(values):
    """Euclidean projection of each column onto the probability simplex."""
    ordered = -np.sort(-values, axis=0)
    cumulative = np.cumsum(ordered, axis=0) - 1.0
    index = np.arange(1, values.shape[0] + 1)[:, None]
    positive = ordered - cumulative / index > 0
    last = positive.shape[0] - 1 - np.argmax(positive[::-1], axis=0)
    theta = cumulative[last, np.arange(values.shape[1])] / (last + 1)
    return np.maximum(values - theta, 0.0)


def archetypal_analysis(x, k, iterations=2000):
    """Archetypes Z = X C and memberships S with simplex columns, X (p x n) ~ Z S.

    Alternating projected-gradient steps on the objective of Morup and Hansen
    (2012), started from a furthest-sum choice of samples. The EHS analysis used
    py_pcha, whose last release (0.1.3) calls np.mat and does not run under
    NumPy 2, so the objective is minimized here directly.
    """
    n = x.shape[1]
    centre = x.mean(axis=1, keepdims=True)
    chosen = [int(np.argmax(np.linalg.norm(x - centre, axis=0)))]
    for _ in range(k - 1):
        distance = np.min([np.linalg.norm(x - x[:, [c]], axis=0) for c in chosen], axis=0)
        chosen.append(int(np.argmax(distance)))
    c = np.zeros((n, k))
    c[chosen, range(k)] = 1.0
    s = project_simplex(np.random.default_rng(SEED).random((k, n)))
    gram = x.T @ x
    for _ in range(iterations):
        z = x @ c
        s = project_simplex(s - z.T @ (z @ s - x) / np.linalg.norm(z.T @ z, 2))
        step = np.linalg.norm(gram, 2) * np.linalg.norm(s @ s.T, 2)
        c = project_simplex(c - (gram @ c @ s - gram) @ s.T / step)
    z = x @ c
    relative_sse = float(np.linalg.norm(x - z @ s) ** 2 / np.linalg.norm(x - centre) ** 2)
    return z, s, relative_sse


def matched(memberships, truth):
    """Order recovered archetypes to best match the generating ones."""
    k = truth.shape[1]
    order = max(
        itertools.permutations(range(k)),
        key=lambda perm: sum(np.corrcoef(memberships[perm[j]], truth[:, j])[0, 1] for j in range(k)),
    )
    return memberships[list(order)]


def archetype_recovery():
    """Missing-aware one-hot encoding, VBPCA and archetypes on synthetic categorical data."""
    rng = np.random.default_rng(SEED)
    k, samples, features, levels = 3, 150, 24, 3
    truth = rng.dirichlet([0.6] * k, size=samples)
    profiles = np.full((k, features, levels), 0.075)
    for j in range(k):
        for f in range(features):
            profiles[j, f, (j + f) % levels] = 0.85
    probs = np.einsum("nk,kpl->npl", truth, profiles)
    data = np.array(
        [[rng.choice(levels, p=probs[i, f]) for f in range(features)] for i in range(samples)],
        dtype=float,
    )
    observed = rng.uniform(size=data.shape) > 0.3
    encoder = MissingAwareOneHotEncoder(binary="both")
    encoded = encoder.fit_transform(np.where(observed, data, np.nan), mask=observed)
    encoded_mask = ~np.isnan(encoded)
    model = VBPCA(n_components=2, maxiters=300, random_state=SEED, verbose=0)
    model.fit_transform(np.nan_to_num(encoded.T), mask=encoded_mask.T)
    reconstructed = np.asarray(model.reconstruction_)
    _, memberships, relative_sse = archetypal_analysis(reconstructed, k)
    memberships = matched(memberships, truth)
    correlation = [float(np.corrcoef(memberships[j], truth[:, j])[0, 1]) for j in range(k)]
    complete = MissingAwareOneHotEncoder(binary="both").fit_transform(
        data, mask=np.ones_like(observed)
    )
    _, complete_memberships, _ = archetypal_analysis(complete.T, k)
    complete_memberships = matched(complete_memberships, truth)
    complete_correlation = [
        float(np.corrcoef(complete_memberships[j], truth[:, j])[0, 1]) for j in range(k)
    ]
    assert min(correlation) > 0.85 and min(complete_correlation) > min(correlation)

    colors = (TEAL, BLUE, GOLD)
    fig, axes = plt.subplots(1, 3, figsize=(9, 3.4), layout="constrained")
    cmap = plt.get_cmap("Greys").copy()
    cmap.set_bad("#d9822b")
    axes[0].imshow(encoded[:60], aspect="auto", cmap=cmap, vmin=0, vmax=1, interpolation="nearest")
    axes[0].set(xlabel="Indicator column", ylabel="Sample (first 60)", title="Missing-aware one-hot encoding")
    axes[0].legend(
        handles=[
            Patch(facecolor="black", label="Level present"),
            Patch(facecolor="#d9822b", label="Variable not observed"),
        ],
        loc="upper center",
        bbox_to_anchor=(0.5, -0.18),
        ncol=2,
        fontsize=8,
    )
    corners = np.array([[0.0, 0.0], [1.0, 0.0], [0.5, np.sqrt(3) / 2]])
    axes[1].plot(*np.vstack([corners, corners[:1]]).T, color=GREY, lw=0.8)
    points = memberships.T @ corners
    dominant = truth.argmax(axis=1)
    for j in range(k):
        axes[1].scatter(*points[dominant == j].T, s=10, color=colors[j], alpha=0.8, label=f"Mostly archetype {j + 1}")
        axes[1].text(*(corners[j] + [(-0.06, -0.07), (0.06, -0.07), (0, 0.04)][j]), f"A{j + 1}", ha="center", fontsize=9)
    axes[1].set(aspect="equal", title="Recovered memberships")
    axes[1].axis("off")
    axes[1].legend(loc="upper center", bbox_to_anchor=(0.5, -0.02), ncol=1, fontsize=8)
    for j in range(k):
        axes[2].scatter(truth[:, j], memberships[j], s=8, color=colors[j], alpha=0.6, label=f"A{j + 1}")
    axes[2].plot([0, 1], [0, 1], color=GREY, ls=":", lw=1)
    axes[2].set(
        xlim=(0, 1), ylim=(0, 1), aspect="equal", xlabel="Generating membership",
        ylabel="Recovered membership", title="Recovered against generating",
    )
    axes[2].legend(loc="upper left", fontsize=8)
    export(fig, "archetype_recovery")
    return {
        "seed": SEED,
        "archetypes": k,
        "samples": samples,
        "features": features,
        "levels": levels,
        "observed_fraction": float(observed.mean()),
        "encoded_columns": int(encoded.shape[1]),
        "n_components": 2,
        "truth": truth.tolist(),
        "memberships": memberships.tolist(),
        "correlation": correlation,
        "mean_absolute_error": float(np.mean(np.abs(memberships.T - truth))),
        "complete_data_correlation": complete_correlation,
        "relative_sse": relative_sse,
    }


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def generate(output):
    """Generate fresh outputs and a manifest tying data/exports to source."""
    global OUTPUT
    OUTPUT = output
    OUTPUT.mkdir(parents=True, exist_ok=True)
    packages = {
        name: version(name)
        for name in [
            "op-system",
            "op-engine",
            "trade-study",
            "vbpca-py",
            "numpy",
            "matplotlib",
        ]
    }
    data = {
        "packages": packages,
        "synthetic": True,
        "spatial_diffusion": diffusion(),
        "stochastic_ensemble": ssa(),
        "replicated_tradeoff": tradeoff(),
        "incomplete_reconstruction": reconstruction(),
        "archetype_recovery": archetype_recovery(),
    }
    (OUTPUT / "computed_data.json").write_text(
        json.dumps(data, separators=(",", ":")) + "\n"
    )
    entries = json.loads((HERE / "figures.json").read_text())
    source_hash = digest(Path(__file__))
    for entry in entries:
        path = OUTPUT / (entry["name"] + ".svg")
        root = ET.parse(path).getroot()
        root.set("role", "img")
        root.set("aria-labelledby", "title description")
        for index, (tag, value) in enumerate(
            [("title", entry["title"]), ("desc", entry["description"])]
        ):
            element = ET.Element(f"{{{SVG_NS}}}{tag}")
            element.set("id", "title" if tag == "title" else "description")
            element.text = value
            root.insert(index, element)
        ET.ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)
        path.write_text(
            "\n".join(line.rstrip() for line in path.read_text().splitlines()) + "\n"
        )
    names = ["computed_data.json", "design_comparison.csv"] + [
        entry["name"] + suffix
        for entry in entries
        for suffix in (".svg", ".pdf", ".png")
    ]
    manifest = {
        "schema_version": 1,
        "source_sha256": source_hash,
        "registry_sha256": digest(HERE / "figures.json"),
        "packages": packages,
        "files_sha256": {name: digest(OUTPUT / name) for name in names},
    }
    (OUTPUT / "provenance.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return data


def check():
    """Check committed provenance and regenerate independent numerical evidence."""
    manifest = json.loads((HERE / "provenance.json").read_text())
    assert manifest["source_sha256"] == digest(Path(__file__))
    assert manifest["registry_sha256"] == digest(HERE / "figures.json")
    for name, expected in manifest["files_sha256"].items():
        assert digest(HERE / name) == expected, f"Changed artifact: {name}"
    entries = json.loads((HERE / "figures.json").read_text())
    for entry in entries:
        root = ET.parse(HERE / (entry["name"] + ".svg")).getroot()
        assert root.findtext(f"{{{SVG_NS}}}title") == entry["title"]
        assert root.findtext(f"{{{SVG_NS}}}desc") == entry["description"]
        for element in root.iter():
            assert element.tag != f"{{{SVG_NS}}}script"
            for attr, value in element.attrib.items():
                if attr.endswith("href"):
                    assert value.startswith(("#", "data:image/png;base64,")), value
    committed = json.loads((HERE / "computed_data.json").read_text())
    with TemporaryDirectory(prefix="computed-examples-") as temporary:
        fresh = generate(Path(temporary))
        assert fresh["packages"] == committed["packages"]
        for key in ("history", "reference"):
            np.testing.assert_allclose(
                fresh["spatial_diffusion"][key],
                committed["spatial_diffusion"][key],
                rtol=1e-12,
                atol=1e-12,
            )
        np.testing.assert_array_equal(
            fresh["stochastic_ensemble"]["history"],
            committed["stochastic_ensemble"]["history"],
        )
        np.testing.assert_array_equal(
            fresh["stochastic_ensemble"]["firing_counts"],
            committed["stochastic_ensemble"]["firing_counts"],
        )
        np.testing.assert_allclose(
            fresh["replicated_tradeoff"]["scores"],
            committed["replicated_tradeoff"]["scores"],
            rtol=1e-12,
            atol=1e-12,
        )
        assert (
            fresh["replicated_tradeoff"]["front"]
            == committed["replicated_tradeoff"]["front"]
        )
        np.testing.assert_array_equal(
            fresh["incomplete_reconstruction"]["observed_mask"],
            committed["incomplete_reconstruction"]["observed_mask"],
        )
        np.testing.assert_allclose(
            fresh["incomplete_reconstruction"]["reconstruction"],
            committed["incomplete_reconstruction"]["reconstruction"],
            rtol=1e-7,
            atol=1e-8,
        )
        np.testing.assert_allclose(
            fresh["archetype_recovery"]["memberships"],
            committed["archetype_recovery"]["memberships"],
            rtol=1e-6,
            atol=1e-7,
        )
    print(
        "Verified five computed figures, retained data and independent numerical checks"
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    table = HERE.parents[3] / "_data/computed_designs.csv"
    if args.check:
        assert table.read_bytes() == (HERE / "design_comparison.csv").read_bytes()
        check()
    else:
        data = generate(HERE)
        table.write_bytes((HERE / "design_comparison.csv").read_bytes())
        print(
            json.dumps(
                {
                    "packages": data["packages"],
                    "diffusion_error": data["spatial_diffusion"]["max_temporal_error"],
                    "heldout_rmse": data["incomplete_reconstruction"]["heldout_rmse"],
                },
                indent=2,
            )
        )


if __name__ == "__main__":
    main()
