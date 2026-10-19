"""Require built numerical downloads to retain their source provenance hashes."""

import argparse
import hashlib
import json
from pathlib import Path

RELATIVE = Path("assets/img/research/computed")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify(source, site):
    """Check both source and built exports against the committed manifest."""
    original, built = source / RELATIVE, site / RELATIVE
    manifest_path = original / "provenance.json"
    manifest = json.loads(manifest_path.read_text())
    if manifest.get("schema_version") != 1:
        raise ValueError("Unsupported computed-figure provenance schema")
    identities = {
        "computed_examples.py": manifest["source_sha256"],
        "figures.json": manifest["registry_sha256"],
        **manifest["files_sha256"],
    }
    for name, expected in identities.items():
        if Path(name).name != name:
            raise ValueError(f"Unexpected computed artifact path: {name}")
        for directory in (original, built):
            path = directory / name
            if not path.is_file() or digest(path) != expected:
                raise ValueError(f"Computed artifact hash differs or is missing: {path}")
    if (built / "provenance.json").read_bytes() != manifest_path.read_bytes():
        raise ValueError("Built computed provenance differs from source")
    print(f"Verified {len(identities)} computed artifacts and provenance after site build")


def verify_previews(source, site):
    """Keep compact previews tied to their retained numerical data."""
    relative = Path("assets/img/research/previews")
    original, built = source / relative, site / relative
    manifest_path = original / "provenance.json"
    manifest = json.loads(manifest_path.read_text())
    if manifest.get("schema_version") != 1 or manifest["data_sha256"] != digest(source / RELATIVE / "computed_data.json"):
        raise ValueError("Preview inputs do not match retained computed data")
    identities = {"card_previews.py": manifest["source_sha256"], **manifest["files_sha256"]}
    for name, expected in identities.items():
        if Path(name).name != name:
            raise ValueError(f"Unexpected preview artifact path: {name}")
        for directory in (original, built):
            if digest(directory / name) != expected:
                raise ValueError(f"Preview artifact hash differs: {directory / name}")
    if (built / "provenance.json").read_bytes() != manifest_path.read_bytes():
        raise ValueError("Built preview provenance differs from source")
    print(f"Verified {len(identities)} preview artifacts and provenance")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("site", type=Path)
    parser.add_argument("--source", type=Path, default=Path("."))
    args = parser.parse_args()
    verify(args.source.resolve(), args.site.resolve())
    verify_previews(args.source.resolve(), args.site.resolve())
