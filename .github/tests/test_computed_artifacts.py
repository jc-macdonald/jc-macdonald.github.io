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

    def test_existing_production_build_when_requested(self):
        import os

        if not os.environ.get("CHECK_COMPUTED_SITE"):
            self.skipTest("set CHECK_COMPUTED_SITE after a production Jekyll build")
        ARTIFACTS.verify(ROOT, ROOT / "_site")
