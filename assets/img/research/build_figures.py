# /// script
# requires-python = ">=3.12"
# dependencies = ["matplotlib==3.11.2", "numpy==2.5.4"]
# ///
"""Build checked-in TikZ schematics and numerical illustrations for the website.

Run ``uv run assets/img/research/build_figures.py``. TeX and export tools are
needed only when regenerating figures; the Jekyll site serves static exports.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent
SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)
ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")


def source_hash(entry: dict[str, str]) -> str:
    """Include figure content, shared style and build settings in provenance."""
    paths = [HERE / entry["source"], Path(__file__)]
    paths.append(
        HERE
        / (
            "tikz/figure-style.tex"
            if entry["source"].endswith(".tex")
            else "palette.py"
        )
    )
    digest = hashlib.sha256()
    digest.update(json.dumps(entry, sort_keys=True).encode())
    for path in paths:
        digest.update(path.name.encode())
        digest.update(path.read_bytes())
    return digest.hexdigest()


def annotate_svg(path: Path, entry: dict[str, str]) -> None:
    """Embed an accessible description and source fingerprint; retain vectors."""
    root = ET.parse(path).getroot()
    root.set("role", "img")
    root.set("aria-labelledby", "title description")
    for index, (tag, value) in enumerate(
        [
            ("title", entry["title"]),
            ("desc", entry["description"]),
            (
                "metadata",
                json.dumps(
                    {"source": entry["source"], "source_sha256": source_hash(entry)},
                    sort_keys=True,
                ),
            ),
        ]
    ):
        element = ET.Element(f"{{{SVG_NS}}}{tag}")
        if tag != "metadata":
            element.set("id", "title" if tag == "title" else "description")
        element.text = value
        root.insert(index, element)
    x, y, width, height = root.attrib["viewBox"].split()
    root.insert(
        3,
        ET.Element(
            f"{{{SVG_NS}}}rect",
            {"x": x, "y": y, "width": width, "height": height, "fill": "#ffffff"},
        ),
    )
    ET.ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)


def run(args: list[str], *, cwd: Path, env: dict[str, str] | None = None) -> None:
    result = subprocess.run(
        args, cwd=cwd, env=env, capture_output=True, text=True, timeout=90
    )
    if result.returncode:
        raise RuntimeError(
            f"Command failed: {args!r}\n{result.stdout[-4000:]}\n{result.stderr[-4000:]}"
        )


def build_tex(entry: dict[str, str]) -> None:
    for executable in ("pdflatex", "pdftocairo"):
        if shutil.which(executable) is None:
            raise RuntimeError(
                f"Install {executable}; see assets/img/research/README.md"
            )
    name = entry["name"]
    with tempfile.TemporaryDirectory(prefix="research-figure-") as folder:
        work = Path(folder)
        env = os.environ.copy()
        env["SOURCE_DATE_EPOCH"] = "946684800"
        env["FORCE_SOURCE_DATE"] = "1"
        env["TEXINPUTS"] = str(HERE / "tikz") + os.pathsep + env.get("TEXINPUTS", "")
        run(
            [
                "pdflatex",
                "-no-shell-escape",
                "-halt-on-error",
                "-interaction=nonstopmode",
                str(HERE / entry["source"]),
            ],
            cwd=work,
            env=env,
        )
        log = (work / f"{name}.log").read_text()
        for warning in ("Overfull \\hbox", "Overfull \\vbox", "Missing character:"):
            if warning in log:
                position = log.index(warning)
                raise RuntimeError(
                    f"{name}: resolve TeX warning\n{log[position : position + 900]}"
                )
        pdf = work / f"{name}.pdf"
        # Poppler emits glyph paths, keeping the SVG independent of web fonts.
        run(["pdftocairo", "-svg", str(pdf), str(work / f"{name}.svg")], cwd=work)
        run(
            [
                "pdftocairo",
                "-png",
                "-singlefile",
                "-scale-to",
                "1600",
                str(pdf),
                str(work / name),
            ],
            cwd=work,
        )
        for suffix in (".svg", ".pdf", ".png"):
            shutil.copyfile(work / f"{name}{suffix}", HERE / f"{name}{suffix}")
    annotate_svg(HERE / f"{name}.svg", entry)


def check(entry: dict[str, str]) -> None:
    root = ET.parse(HERE / f"{entry['name']}.svg").getroot()
    assert root.tag == f"{{{SVG_NS}}}svg" and "viewBox" in root.attrib, entry["name"]
    metadata = root.find(f"{{{SVG_NS}}}metadata")
    assert metadata is not None and metadata.text
    assert json.loads(metadata.text)["source_sha256"] == source_hash(entry), (
        f"Regenerate {entry['name']}"
    )
    assert root.findtext(f"{{{SVG_NS}}}title") == entry["title"]
    assert root.findtext(f"{{{SVG_NS}}}desc") == entry["description"]
    assert root.get("aria-labelledby") == "title description"
    for element in root.iter():
        assert element.tag != f"{{{SVG_NS}}}script", entry["name"]
        for attr, value in element.attrib.items():
            if attr.endswith("href"):
                assert value.startswith("#"), (
                    f"External SVG dependency in {entry['name']}"
                )
    assert (HERE / f"{entry['name']}.pdf").read_bytes().startswith(b"%PDF")
    assert (HERE / f"{entry['name']}.png").read_bytes().startswith(b"\x89PNG\r\n\x1a\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check exports and source fingerprints without TeX.",
    )
    parser.add_argument(
        "--schematics",
        action="store_true",
        help="Select only TikZ figures; no Python plotting dependencies needed.",
    )
    parser.add_argument(
        "names", nargs="*", help="Optional figure names from figures.json."
    )
    args = parser.parse_args()
    entries = json.loads((HERE / "figures.json").read_text())
    if args.names:
        unknown = set(args.names) - {entry["name"] for entry in entries}
        if unknown:
            parser.error(f"Unknown figures: {sorted(unknown)}")
        entries = [entry for entry in entries if entry["name"] in args.names]
    if args.schematics:
        entries = [entry for entry in entries if entry["source"].endswith(".tex")]
    if not args.check:
        for entry in entries:
            if entry["source"].endswith(".tex"):
                build_tex(entry)
                print("Built", entry["name"], flush=True)
        plots = [entry for entry in entries if not entry["source"].endswith(".tex")]
        if plots:
            with tempfile.TemporaryDirectory(prefix="research-matplotlib-") as cache:
                env = os.environ.copy()
                env["MPLCONFIGDIR"] = cache
                env["PYTHONDONTWRITEBYTECODE"] = "1"
                run(
                    [sys.executable, str(HERE / "gen_research_figures.py")],
                    cwd=HERE,
                    env=env,
                )
            for entry in plots:
                annotate_svg(HERE / f"{entry['name']}.svg", entry)
    for entry in entries:
        check(entry)
    print(
        f"Verified {len(entries)} figures: sources, accessibility, static dependencies and SVG/PDF/PNG exports."
    )


if __name__ == "__main__":
    main()
