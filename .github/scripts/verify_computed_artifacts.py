"""Require built numerical downloads to retain their source provenance hashes."""

import argparse
import hashlib
import json
from pathlib import Path

RELATIVE = Path("assets/img/research/computed")
OP_INFER_RELATIVE = RELATIVE / "op_infer_normal_sbc"
OP_INFER_SOURCE = {
    "schema_version": 1,
    "repository": "ACCIDDA/op_infer",
    "revision": "6a066d918e2d8460a32a6cabd6be964deb7654bb",
    "asset_path": "docs/assets/normal-sbc",
    "generator_paths": [
        "examples/illustrate_normal_sbc.py",
        "examples/normal_sbc.py",
        "examples/illustration_artifacts.py",
    ],
    "upstream_manifest_sha256": "d8c0e50829fdb86cd96c1bc9d8b3edff2e042d5cb6d8154b9376262796072e52",
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest_bytes(value):
    return hashlib.sha256(value).hexdigest()


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
    expected_inputs = {
        "computed_data.json": digest(source / RELATIVE / "computed_data.json"),
        "op_infer_normal_sbc/data.json": digest(source / OP_INFER_RELATIVE / "data.json"),
    }
    if manifest.get("schema_version") != 2 or manifest["input_sha256"] != expected_inputs:
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


def verify_imported_op_infer(source, site):
    """Verify the exact public upstream op_infer artifact and local aliases."""
    original, built = source / OP_INFER_RELATIVE, site / OP_INFER_RELATIVE
    source_record = json.loads((original / "source.json").read_text())
    if source_record != OP_INFER_SOURCE:
        raise ValueError("Unexpected op_infer source identity")

    manifest_path = original / "manifest.json"
    if digest(manifest_path) != source_record["upstream_manifest_sha256"]:
        raise ValueError("Imported op_infer manifest differs from reviewed upstream")
    manifest = json.loads(manifest_path.read_text())
    exports = manifest.get("exports")
    if not isinstance(exports, dict) or exports.get("data.json") != manifest.get("data_sha256"):
        raise ValueError("Malformed op_infer export manifest")

    for name, expected in exports.items():
        if Path(name).name != name or name not in {"data.json", "figure.svg", "figure.pdf"}:
            raise ValueError(f"Unexpected op_infer artifact path: {name}")
        for directory in (original, built):
            path = directory / name
            if not path.is_file() or digest(path) != expected:
                raise ValueError(f"Imported op_infer artifact differs or is missing: {path}")

    for name in ("manifest.json", "source.json", "summary.txt"):
        if (built / name).read_bytes() != (original / name).read_bytes():
            raise ValueError(f"Built op_infer metadata differs: {name}")

    for suffix in ("svg", "pdf"):
        alias = source / RELATIVE / f"op_infer_normal_sbc.{suffix}"
        built_alias = site / RELATIVE / f"op_infer_normal_sbc.{suffix}"
        expected = (original / f"figure.{suffix}").read_bytes()
        if alias.read_bytes() != expected or built_alias.read_bytes() != expected:
            raise ValueError(f"op_infer {suffix.upper()} alias differs from upstream export")
    print("Verified imported op_infer artifact, source identity and site aliases")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("site", type=Path)
    parser.add_argument("--source", type=Path, default=Path("."))
    args = parser.parse_args()
    verify(args.source.resolve(), args.site.resolve())
    verify_previews(args.source.resolve(), args.site.resolve())
    verify_imported_op_infer(args.source.resolve(), args.site.resolve())
