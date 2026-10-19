"""Render fresh CV PDFs and verify their source revision before site publication."""

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from importlib.metadata import version
from pathlib import Path
from tempfile import TemporaryDirectory

INPUTS = (
    "_data/cv.yml",
    "assets/rendercv/design.yaml",
    "assets/rendercv/locale.yaml",
    "assets/rendercv/settings.yaml",
    "requirements-rendercv.txt",
    ".github/scripts/render_cv.py",
)
DOWNLOAD = "assets/pdf/cv.pdf"
MANIFEST = "assets/rendercv/provenance.json"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def input_hashes(root):
    return {name: digest(root / name) for name in INPUTS}


def pinned_version(root):
    lines = (root / "requirements-rendercv.txt").read_text().splitlines()
    return next(
        line.split("==", 1)[1].strip()
        for line in lines
        if line.startswith("rendercv[full]==")
    )


def render(root, output, revision):
    """Use an empty render tree so old/sample PDFs can never satisfy generation."""
    hashes = input_hashes(root)
    renderer = version("rendercv")
    if renderer != pinned_version(root):
        raise ValueError(
            "Install the pinned requirements-rendercv.txt before rendering"
        )
    if output.exists() and any(output.iterdir()):
        raise ValueError("CV artifact output must be empty; refusing to reuse old PDFs")
    with TemporaryDirectory(prefix="rendercv-") as temporary:
        fresh = Path(temporary)
        for name in INPUTS[:4]:
            destination = fresh / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(root / name, destination)
        subprocess.run(
            [
                sys.executable,
                "-m",
                "rendercv",
                "render",
                "_data/cv.yml",
                "--settings",
                "assets/rendercv/settings.yaml",
            ],
            cwd=fresh,
            check=True,
        )
        pdfs = list((fresh / "assets/rendercv/rendercv_output").glob("*.pdf"))
        if len(pdfs) != 1 or not pdfs[0].read_bytes().startswith(b"%PDF-"):
            raise ValueError("RenderCV must produce exactly one fresh PDF")
        if hashes != input_hashes(root):
            raise ValueError("CV inputs changed while rendering")
        rendered = pdfs[0].relative_to(fresh).as_posix()
        for name in (rendered, DOWNLOAD):
            destination = output / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(pdfs[0], destination)
        manifest = {
            "schema_version": 1,
            "source_revision": revision,
            "inputs_sha256": hashes,
            "rendercv_version": renderer,
            "rendered_pdf": rendered,
            "download_pdf": DOWNLOAD,
            "pdf_sha256": digest(pdfs[0]),
        }
        (output / MANIFEST).write_text(json.dumps(manifest, indent=2) + "\n")
    verify(root, output, revision)


def verify(root, artifact, revision):
    """Require matching source, renderer, inputs and two identical PDF copies."""
    manifest = json.loads((artifact / MANIFEST).read_text())
    if (
        manifest.get("schema_version") != 1
        or manifest.get("source_revision") != revision
        or manifest.get("inputs_sha256") != input_hashes(root)
        or manifest.get("rendercv_version") != pinned_version(root)
        or manifest.get("download_pdf") != DOWNLOAD
    ):
        raise ValueError("CV artifact does not match this source revision and inputs")
    rendered = Path(manifest["rendered_pdf"])
    if (
        rendered.parent.as_posix() != "assets/rendercv/rendercv_output"
        or rendered.suffix != ".pdf"
    ):
        raise ValueError("Unexpected rendered PDF path")
    for name in (rendered, Path(DOWNLOAD)):
        pdf = artifact / name
        if (
            not pdf.read_bytes().startswith(b"%PDF-")
            or digest(pdf) != manifest["pdf_sha256"]
        ):
            raise ValueError(f"CV artifact PDF content mismatch: {name}")
    print(f"Verified CV PDFs for source revision {revision}")
    return manifest


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("operation", choices=("render", "verify"))
    cli.add_argument("--source", type=Path, default=Path("."))
    cli.add_argument("--output-dir", type=Path, required=True)
    args = cli.parse_args()
    source = args.source.resolve()
    revision = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=source, text=True
    ).strip()
    function = render if args.operation == "render" else verify
    function(source, args.output_dir.resolve(), revision)
