"""Tests for shared website and CV release metadata."""

import copy
import importlib.util
import json
import re
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "software_releases", ROOT / ".github/scripts/refresh_software_releases.py"
)
RELEASES = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RELEASES)


def zenodo_record(
    *,
    version="v0.10.0",
    repository="ACCIDDA/op_system",
    concept_doi="10.5281/zenodo.23604812",
    doi="10.5281/zenodo.23604813",
):
    """Return one fully qualified published software record."""
    return {
        "doi": doi,
        "conceptdoi": concept_doi,
        "status": "published",
        "metadata": {
            "doi": doi,
            "version": version,
            "resource_type": {"type": "software"},
            "related_identifiers": [
                {
                    "relation": "isSupplementTo",
                    "identifier": f"https://github.com/{repository}/tree/{version}",
                    "scheme": "url",
                    "resource_type": "software",
                }
            ],
        },
    }


class SoftwareReleaseTests(unittest.TestCase):
    def test_release_workflow_separates_validation_from_write_permissions(self):
        workflow = (ROOT / ".github/workflows/update-software-releases.yml").read_text()

        validation, writer = workflow.split("  open-review-pull-request:\n", 1)
        self.assertEqual(workflow.count("contents: write"), 1)
        self.assertNotIn("contents: write", validation)
        self.assertNotIn("GITHUB_TOKEN", workflow)
        self.assertIn("needs: refresh-and-validate", writer)
        self.assertNotIn("run:", writer)
        self.assertEqual(workflow.count("persist-credentials: false"), 2)
        self.assertIn(
            "path: |\n            _data/software_releases.json\n"
            "            _data/cv.yml",
            validation,
        )
        self.assertIn("path: _data", writer)
        self.assertIn(
            "add-paths: |\n            _data/software_releases.json\n"
            "            _data/cv.yml",
            writer,
        )

        action_references = re.findall(r"uses: [^\s]+@([^\s#]+)", workflow)
        self.assertTrue(action_references)
        for reference in action_references:
            with self.subTest(reference=reference):
                self.assertRegex(reference, r"^[0-9a-f]{40}$")

    def test_committed_manifest_and_cv_are_consistent(self):
        sources = json.loads(RELEASES.SOURCES.read_text())
        manifest = json.loads(RELEASES.MANIFEST.read_text())
        RELEASES.validate_manifest(manifest, sources)

    def test_release_phase_is_separate_from_maturity(self):
        self.assertEqual(RELEASES.release_phase("0.9.0", published=True), "final")
        self.assertEqual(RELEASES.release_phase("1.0.0b2", published=True), "beta")
        self.assertEqual(
            RELEASES.release_phase("0.5.0.dev0", published=False), "development"
        )

    def test_private_record_discloses_no_repository_or_version(self):
        manifest = json.loads(RELEASES.MANIFEST.read_text())
        record = manifest["packages"]["pp_eigentest"]
        self.assertEqual(
            record["display_status"],
            "Private; package maturity: alpha; unreleased",
        )
        self.assertIsNone(record["version"])
        self.assertIsNone(record["repository"])
        self.assertIsNone(record["source_url"])

    def test_new_op_archives_are_exact(self):
        manifest = json.loads(RELEASES.MANIFEST.read_text())
        expected = {
            "op_system": "10.5281/zenodo.23604813",
            "op_engine": "10.5281/zenodo.23606247",
        }
        for slug, doi in expected.items():
            with self.subTest(slug=slug):
                record = manifest["packages"][slug]
                self.assertFalse(record["archive_pending"])
                self.assertEqual(record["release_archive_doi"], doi)
                self.assertEqual(
                    record["release_archive_source"], "Zenodo concept lookup"
                )

    def test_flepimop_release_archive_is_exact(self):
        manifest = json.loads(RELEASES.MANIFEST.read_text())
        record = manifest["packages"]["flepimop2"]
        self.assertEqual(record["release_archive_doi"], "10.5281/zenodo.20649548")
        self.assertFalse(record["archive_pending"])
        self.assertEqual(record["docs_label"], "Release documentation")

    def test_registry_drift_requires_a_refresh(self):
        sources = json.loads(RELEASES.SOURCES.read_text())
        manifest = json.loads(RELEASES.MANIFEST.read_text())
        drifted = copy.deepcopy(sources)
        drifted["packages"]["trade_study"]["concept_doi"] = "10.5281/zenodo.99999999"
        with self.assertRaisesRegex(ValueError, "stale or invalid"):
            RELEASES.validate_manifest(manifest, drifted)

    def test_private_registry_cannot_expose_a_repository(self):
        sources = json.loads(RELEASES.SOURCES.read_text())
        manifest = json.loads(RELEASES.MANIFEST.read_text())
        unsafe = copy.deepcopy(sources)
        unsafe["packages"]["pp_eigentest"]["repository"] = "owner/private"
        with self.assertRaisesRegex(ValueError, "exposes metadata"):
            RELEASES.validate_manifest(manifest, unsafe)

    def test_private_refresh_cannot_generate_disclosive_metadata(self):
        sources = json.loads(RELEASES.SOURCES.read_text())
        base = sources["packages"]["pp_eigentest"]
        disclosures = {
            "version": "9.9.9",
            "docs_url": "https://private.example/docs",
            "concept_doi": "10.5281/zenodo.99999999",
            "release_archives": {"9.9.9": "10.5281/zenodo.99999998"},
        }
        for key, value in disclosures.items():
            with self.subTest(key=key):
                unsafe = copy.deepcopy(base)
                unsafe[key] = value
                with self.assertRaisesRegex(ValueError, "exposes metadata"):
                    RELEASES.build_record("pp_eigentest", unsafe)

    def test_source_specific_upstream_fields_are_required(self):
        sources = json.loads(RELEASES.SOURCES.read_text())
        manifest = json.loads(RELEASES.MANIFEST.read_text())
        cases = (
            ("op_system", "published_at", "PyPI release record"),
            ("inference_calibration", "source_revision", "GitHub release record"),
            ("inference_calibration", "source_ref", "GitHub release record"),
        )
        for slug, field, message in cases:
            with self.subTest(slug=slug, field=field):
                incomplete = copy.deepcopy(manifest)
                incomplete["packages"][slug].pop(field)
                with self.assertRaisesRegex(ValueError, message):
                    RELEASES.validate_manifest(incomplete, sources)

    def test_schema_versions_are_required(self):
        sources = json.loads(RELEASES.SOURCES.read_text())
        manifest = json.loads(RELEASES.MANIFEST.read_text())
        for value in (999, True, 1.0):
            with self.subTest(location="sources", value=value):
                invalid_sources = copy.deepcopy(sources)
                invalid_sources["schema_version"] = value
                with self.assertRaisesRegex(ValueError, "release-source"):
                    RELEASES.validate_manifest(manifest, invalid_sources)
            with self.subTest(location="manifest", value=value):
                invalid_manifest = copy.deepcopy(manifest)
                invalid_manifest["schema_version"] = value
                with self.assertRaisesRegex(ValueError, "release-manifest"):
                    RELEASES.validate_manifest(invalid_manifest, sources)

    def test_source_specific_upstream_fields_are_closed(self):
        sources = json.loads(RELEASES.SOURCES.read_text())
        manifest = json.loads(RELEASES.MANIFEST.read_text())
        cases = (
            ("pp_eigentest", "source_ref", "manual release record"),
            ("op_system", "source_revision", "pypi release record"),
            ("inference_calibration", "published_at", "github-main release record"),
        )
        for slug, field, message in cases:
            with self.subTest(slug=slug, field=field):
                unsafe = copy.deepcopy(manifest)
                unsafe["packages"][slug][field] = "unexpected"
                with self.assertRaisesRegex(ValueError, message):
                    RELEASES.validate_manifest(unsafe, sources)

    def test_version_rollover_drops_an_old_exact_archive(self):
        sources = json.loads(RELEASES.SOURCES.read_text())
        config = sources["packages"]["trade_study"]
        record = RELEASES.decorate_record(
            "trade_study",
            config,
            {
                "version": "0.7.0",
                "maturity": "alpha",
                "published": True,
                "published_at": "2026-11-01T00:00:00Z",
            },
        )
        self.assertTrue(record["archive_pending"])
        self.assertIn("trade-study/0.7.0/", record["cv_status"])
        self.assertNotIn("zenodo.23497881", record["cv_status"])

    def test_registry_archive_must_match_zenodo(self):
        config = {
            "package": "example-package",
            "repository": "example/project",
            "concept_doi": "10.5281/zenodo.1000",
            "release_archives": {"1.2.3": "10.5281/zenodo.1001"},
        }
        payload = {
            "info": {
                "version": "1.2.3",
                "classifiers": ["Development Status :: 3 - Alpha"],
            },
            "releases": {"1.2.3": [{"upload_time_iso_8601": "2026-10-23T00:00:00Z"}]},
        }
        with (
            mock.patch.object(RELEASES, "read_json_url", return_value=payload),
            mock.patch.object(
                RELEASES,
                "zenodo_release_doi",
                return_value="10.5281/zenodo.9999",
            ),
            self.assertRaisesRegex(ValueError, "does not match the exact Zenodo"),
        ):
            RELEASES.pypi_project(config)

    def test_versioned_docs_follow_the_current_release(self):
        sources = json.loads(RELEASES.SOURCES.read_text())
        config = sources["packages"]["op_system"]
        record = RELEASES.decorate_record(
            "op_system",
            config,
            {
                "version": "0.10.0",
                "maturity": "alpha",
                "published": True,
                "published_at": "2026-11-01T00:00:00Z",
            },
        )
        self.assertEqual(
            record["docs_url"],
            "https://accidda.github.io/op_system/0.10.0/guides/capabilities/",
        )

    def test_versioned_docs_preserve_prerelease_and_reject_invalid_version(self):
        sources = json.loads(RELEASES.SOURCES.read_text())
        config = sources["packages"]["op_system"]
        self.assertEqual(
            RELEASES.configured_docs_url(config, "0.11.0rc1"),
            "https://accidda.github.io/op_system/0.11.0rc1/guides/capabilities/",
        )
        with self.assertRaisesRegex(ValueError, "Cannot derive"):
            RELEASES.configured_docs_url(config, "development")

    def test_zenodo_match_requires_exact_version_and_repository_tag(self):
        config = {
            "repository": "ACCIDDA/op_system",
            "concept_doi": "10.5281/zenodo.23604812",
        }
        response = {"hits": {"hits": [zenodo_record()], "total": 1}}
        with mock.patch.object(RELEASES, "read_json_url", return_value=response):
            self.assertEqual(
                RELEASES.zenodo_release_doi(config, "0.10.0"),
                "10.5281/zenodo.23604813",
            )

    def test_zenodo_absent_version_is_pending(self):
        config = {
            "repository": "ACCIDDA/op_system",
            "concept_doi": "10.5281/zenodo.23604812",
        }
        response = {
            "hits": {
                "hits": [zenodo_record(version="v0.9.0")],
                "total": 1,
            }
        }
        with mock.patch.object(RELEASES, "read_json_url", return_value=response):
            self.assertIsNone(RELEASES.zenodo_release_doi(config, "0.10.0"))

    def test_zenodo_exact_version_fails_closed_on_bad_metadata(self):
        config = {
            "repository": "ACCIDDA/op_system",
            "concept_doi": "10.5281/zenodo.23604812",
        }
        cases = {
            "wrong source relation": zenodo_record(repository="other/project"),
            "not software": zenodo_record(),
            "not published": zenodo_record(),
            "inconsistent DOI": zenodo_record(),
        }
        cases["not software"]["metadata"]["resource_type"] = {"type": "dataset"}
        cases["not published"]["status"] = "draft"
        cases["inconsistent DOI"]["metadata"]["doi"] = "10.5281/zenodo.99999999"
        for message, record in cases.items():
            with self.subTest(message=message):
                response = {"hits": {"hits": [record], "total": 1}}
                with (
                    mock.patch.object(RELEASES, "read_json_url", return_value=response),
                    self.assertRaisesRegex(ValueError, message),
                ):
                    RELEASES.zenodo_release_doi(config, "0.10.0")

    def test_zenodo_lookup_traverses_all_pages(self):
        config = {
            "repository": "ACCIDDA/op_system",
            "concept_doi": "10.5281/zenodo.23604812",
        }
        older = [
            zenodo_record(version=f"v0.1.{index}", doi=f"10.5281/zenodo.{1000 + index}")
            for index in range(25)
        ]
        responses = [
            {"hits": {"hits": older, "total": 26}},
            {"hits": {"hits": [zenodo_record()], "total": 26}},
        ]
        with mock.patch.object(
            RELEASES, "read_json_url", side_effect=responses
        ) as read:
            self.assertEqual(
                RELEASES.zenodo_release_doi(config, "0.10.0"),
                "10.5281/zenodo.23604813",
            )
        self.assertEqual(read.call_count, 2)

    def test_zenodo_duplicate_exact_version_requires_review(self):
        config = {
            "repository": "ACCIDDA/op_system",
            "concept_doi": "10.5281/zenodo.23604812",
        }
        duplicate = zenodo_record(doi="10.5281/zenodo.23604814")
        response = {"hits": {"hits": [zenodo_record(), duplicate], "total": 2}}
        with (
            mock.patch.object(RELEASES, "read_json_url", return_value=response),
            self.assertRaisesRegex(ValueError, "multiple exact archives"),
        ):
            RELEASES.zenodo_release_doi(config, "0.10.0")

    def test_zenodo_malformed_pagination_fails_closed(self):
        config = {
            "repository": "ACCIDDA/op_system",
            "concept_doi": "10.5281/zenodo.23604812",
        }
        malformed = {"hits": {"hits": [], "total": "unknown"}}
        with (
            mock.patch.object(RELEASES, "read_json_url", return_value=malformed),
            self.assertRaisesRegex(ValueError, "invalid hits or total"),
        ):
            RELEASES.zenodo_release_doi(config, "0.10.0")

    def test_duplicate_cv_markers_fail(self):
        manifest = json.loads(RELEASES.MANIFEST.read_text())
        original = RELEASES.CV.read_text()
        marker = next(
            line
            for line in original.splitlines()
            if "software-release: op_system" in line
        )
        with tempfile.TemporaryDirectory() as directory:
            duplicate = Path(directory) / "cv.yml"
            duplicate.write_text(f"{original}\n{marker}\n")
            with (
                mock.patch.object(RELEASES, "CV", duplicate),
                self.assertRaisesRegex(ValueError, "Duplicate CV"),
            ):
                RELEASES.sync_cv(manifest, write=False)


if __name__ == "__main__":
    unittest.main()
