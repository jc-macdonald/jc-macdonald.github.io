"""A build must preserve hashed bytes even when JSON values are unchanged."""

import hashlib
import importlib.util
import json
import shutil
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "verify_computed_artifacts", ROOT / ".github/scripts/verify_computed_artifacts.py"
)
ARTIFACTS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ARTIFACTS)


class ArtifactTests(unittest.TestCase):
    def test_identical_build_passes_and_json_reserialization_fails(self):
        with TemporaryDirectory() as directory:
            source, site = Path(directory) / "source", Path(directory) / "site"
            original = source / ARTIFACTS.RELATIVE
            original.mkdir(parents=True)
            values = {
                "computed_examples.py": b"# reproducible computation\n",
                "figures.json": b"[]\n",
                "computed_data.json": b'{"values":[1.0,2.0]}\n',
            }
            for name, content in values.items():
                (original / name).write_bytes(content)
            hashes = {
                name: hashlib.sha256(content).hexdigest()
                for name, content in values.items()
            }
            manifest = {
                "schema_version": 1,
                "source_sha256": hashes["computed_examples.py"],
                "registry_sha256": hashes["figures.json"],
                "files_sha256": {"computed_data.json": hashes["computed_data.json"]},
            }
            (original / "provenance.json").write_text(json.dumps(manifest) + "\n")
            built = site / ARTIFACTS.RELATIVE
            shutil.copytree(original, built)
            ARTIFACTS.verify(source, site)

            data = built / "computed_data.json"
            data.write_bytes(values["computed_data.json"].rstrip(b"\n"))
            self.assertEqual(json.loads(data.read_bytes()), {"values": [1.0, 2.0]})
            with self.assertRaisesRegex(ValueError, "hash differs"):
                ARTIFACTS.verify(source, site)

    def test_preview_manifest_binds_both_numerical_inputs(self):
        with TemporaryDirectory() as directory:
            source, site = Path(directory) / "source", Path(directory) / "site"
            computed = source / ARTIFACTS.RELATIVE
            imported = source / ARTIFACTS.OP_INFER_RELATIVE
            previews = source / "assets/img/research/previews"
            imported.mkdir(parents=True)
            previews.mkdir(parents=True)
            (computed / "computed_data.json").write_bytes(b'{}\n')
            (imported / "data.json").write_bytes(b'{"pits":[]}\n')
            (previews / "card_previews.py").write_bytes(b"# preview\n")
            (previews / "preview.svg").write_bytes(b"<svg/>\n")
            manifest = {
                "schema_version": 2,
                "source_sha256": ARTIFACTS.digest(previews / "card_previews.py"),
                "input_sha256": {
                    "computed_data.json": ARTIFACTS.digest(computed / "computed_data.json"),
                    "op_infer_normal_sbc/data.json": ARTIFACTS.digest(imported / "data.json"),
                },
                "files_sha256": {"preview.svg": ARTIFACTS.digest(previews / "preview.svg")},
            }
            (previews / "provenance.json").write_text(json.dumps(manifest) + "\n")
            shutil.copytree(previews, site / "assets/img/research/previews")
            ARTIFACTS.verify_previews(source, site)

            (imported / "data.json").write_bytes(b'{"pits":[0.5]}\n')
            with self.assertRaisesRegex(ValueError, "inputs do not match"):
                ARTIFACTS.verify_previews(source, site)

    def test_imported_op_infer_artifact_requires_exact_source_and_aliases(self):
        with TemporaryDirectory() as directory:
            source, site = Path(directory) / "source", Path(directory) / "site"
            original = source / ARTIFACTS.OP_INFER_RELATIVE
            original.mkdir(parents=True)
            values = {
                "data.json": b'{"pits":[0.5]}\n',
                "figure.svg": b"<svg/>\n",
                "figure.pdf": b"%PDF fixture\n",
            }
            manifest = {
                "source_sha256": "source-fixture",
                "data_sha256": ARTIFACTS.digest_bytes(values["data.json"]),
                "sources": ["illustrate_normal_sbc.py", "normal_sbc.py"],
                "rendered_with": {"numpy": "fixture", "matplotlib": "fixture"},
                "exports": {name: ARTIFACTS.digest_bytes(content) for name, content in values.items()},
            }
            manifest_bytes = (json.dumps(manifest, indent=2) + "\n").encode()
            source_record = dict(ARTIFACTS.OP_INFER_SOURCE)
            source_record["upstream_manifest_sha256"] = ARTIFACTS.digest_bytes(manifest_bytes)
            old_source = ARTIFACTS.OP_INFER_SOURCE
            self.addCleanup(setattr, ARTIFACTS, "OP_INFER_SOURCE", old_source)
            ARTIFACTS.OP_INFER_SOURCE = source_record
            for name, content in values.items():
                (original / name).write_bytes(content)
            (original / "manifest.json").write_bytes(manifest_bytes)
            (original / "source.json").write_text(json.dumps(source_record) + "\n")
            (original / "summary.txt").write_text("fixture\n")
            for suffix in ("svg", "pdf"):
                (source / ARTIFACTS.RELATIVE / f"op_infer_normal_sbc.{suffix}").write_bytes(
                    values[f"figure.{suffix}"]
                )
            shutil.copytree(source / ARTIFACTS.RELATIVE, site / ARTIFACTS.RELATIVE)
            ARTIFACTS.verify_imported_op_infer(source, site)

            (site / ARTIFACTS.RELATIVE / "op_infer_normal_sbc.svg").write_bytes(b"changed")
            with self.assertRaisesRegex(ValueError, "alias differs"):
                ARTIFACTS.verify_imported_op_infer(source, site)

    def test_existing_production_build_when_requested(self):
        import os

        if not os.environ.get("CHECK_COMPUTED_SITE"):
            self.skipTest("set CHECK_COMPUTED_SITE after a production Jekyll build")
        ARTIFACTS.verify(ROOT, ROOT / "_site")
