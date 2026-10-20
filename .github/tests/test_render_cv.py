"""Exercise real RenderCV output and reject stale or invalid publication inputs."""

import importlib.util
import json
import os
import re
import shutil
import subprocess
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "render_cv", ROOT / ".github/scripts/render_cv.py"
)
CV = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CV)
REVISION = "0123456789abcdef0123456789abcdef01234567"


def copy_inputs(source):
    for name in CV.INPUTS:
        target = source / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / name, target)


class RenderTests(unittest.TestCase):
    def test_fresh_pdfs_and_provenance_reject_stale_inputs(self):
        with TemporaryDirectory() as directory:
            source, output = Path(directory) / "source", Path(directory) / "artifact"
            copy_inputs(source)
            cv_source = source / "_data/cv.yml"
            updated, replacements = re.subn(
                r"(?m)^  name: [^\n]+$",
                "  name: CV Publication Probe",
                cv_source.read_text(),
                count=1,
            )
            self.assertEqual(replacements, 1)
            cv_source.write_text(updated)
            stale = source / "assets/rendercv/rendercv_output/Stale_CV.pdf"
            stale.parent.mkdir(parents=True, exist_ok=True)
            stale.write_bytes(b"%PDF-stale")
            old_download = source / CV.DOWNLOAD
            old_download.parent.mkdir(parents=True, exist_ok=True)
            old_download.write_bytes(b"%PDF-stale")
            CV.render(source, output, REVISION)
            manifest = CV.verify(source, output, REVISION)
            self.assertEqual(
                (output / manifest["rendered_pdf"]).read_bytes(),
                (output / CV.DOWNLOAD).read_bytes(),
            )
            self.assertEqual(
                old_download.read_bytes(),
                b"%PDF-stale",
                "PR rendering must not edit source",
            )
            text = subprocess.check_output(
                ["pdftotext", str(output / CV.DOWNLOAD), "-"], text=True
            )
            self.assertIn("CV Publication Probe", text)
            with self.assertRaisesRegex(ValueError, "source revision"):
                CV.verify(source, output, "f" * 40)
            settings = source / "assets/rendercv/settings.yaml"
            settings.write_text(settings.read_text() + "\n# settings changed\n")
            with self.assertRaisesRegex(ValueError, "inputs"):
                CV.verify(source, output, REVISION)
            settings.write_bytes((ROOT / "assets/rendercv/settings.yaml").read_bytes())
            (output / CV.DOWNLOAD).write_bytes(b"%PDF-tampered")
            with self.assertRaisesRegex(ValueError, "PDF content"):
                CV.verify(source, output, REVISION)
            with self.assertRaisesRegex(ValueError, "empty"):
                CV.render(source, output, REVISION)

    def test_design_locale_and_continuation_templates_reach_pdf(self):
        with TemporaryDirectory() as directory:
            source, output = Path(directory) / "source", Path(directory) / "artifact"
            copy_inputs(source)
            records = [
                {
                    "name": f"Record {index}",
                    "start_date": 2024,
                    "end_date": "present",
                    "summary": "A description of the research and contribution. " * 8,
                }
                for index in range(12)
            ]
            (source / "_data/cv.yml").write_text(json.dumps({
                "cv": {"name": "Design Probe", "sections": {"Probe Records": records}}
            }))
            # Deliberately differ from both renderer defaults and the site's design.
            (source / "assets/rendercv/design.yaml").write_text(
                "design:\n  theme: classic\n  page:\n    size: a5\n"
                "    show_footer: true\n    show_top_note: false\n"
                "  templates:\n    footer: Configuration Applied PAGE_NUMBER / TOTAL_PAGES\n"
            )
            (source / "assets/rendercv/locale.yaml").write_text(
                "locale:\n  language: english\n  present: ongoing-probe\n"
            )
            CV.render(source, output, REVISION)
            pdf = output / CV.DOWNLOAD
            info = subprocess.check_output(["pdfinfo", str(pdf)], text=True)
            dimensions = re.search(r"Page size:\s+([\d.]+) x ([\d.]+)", info)
            self.assertIsNotNone(dimensions)
            self.assertAlmostEqual(float(dimensions[1]), 419.528, delta=1)
            self.assertAlmostEqual(float(dimensions[2]), 595.276, delta=1)
            text = subprocess.check_output(["pdftotext", str(pdf), "-"], text=True)
            pages = [page for page in text.split("\f") if page.strip()]
            self.assertGreater(len(pages), 1)
            self.assertNotIn("(continued)", pages[0])
            self.assertTrue(pages[1].startswith("Probe Records (continued)"))
            for page in pages:
                self.assertIn("Configuration Applied", page)
                self.assertNotIn("Last updated", page)
            self.assertIn("ongoing-probe", text)
            self.assertIn("Record 11", text)
            # A template-only change invalidates an artifact just like a data change.
            template = source / "_data/classic/Preamble.j2.typ"
            template.write_text(template.read_text() + "\n// changed\n")
            with self.assertRaisesRegex(ValueError, "inputs"):
                CV.verify(source, output, REVISION)

    def test_invalid_schema_cannot_reuse_stale_pdf(self):
        with TemporaryDirectory() as directory:
            source, output = Path(directory) / "source", Path(directory) / "artifact"
            copy_inputs(source)
            (source / "_data/cv.yml").write_text("cv:\n  name: [invalid, name]\n")
            stale = source / CV.DOWNLOAD
            stale.parent.mkdir(parents=True, exist_ok=True)
            stale.write_bytes(b"%PDF-stale")
            with self.assertRaises((subprocess.CalledProcessError, ValueError)):
                CV.render(source, output, REVISION)
            self.assertFalse((output / CV.MANIFEST).exists())
            self.assertFalse((output / CV.DOWNLOAD).exists())

    @unittest.skipUnless(
        os.environ.get("CV_SITE_INTEGRATION") == "1",
        "optional full Jekyll publication check",
    )
    def test_source_only_change_reaches_html_and_download(self):
        with TemporaryDirectory() as directory:
            source = Path(directory) / "site"
            shutil.copytree(
                ROOT,
                source,
                ignore=shutil.ignore_patterns(
                    ".git",
                    "_site",
                    "node_modules",
                    ".jekyll-cache",
                    ".bundle",
                    ".venv",
                    "vendor",
                ),
            )
            cv_source = source / "_data/cv.yml"
            updated, replacements = re.subn(
                r"(?m)^  name: [^\n]+$",
                "  name: CV Publication Probe",
                cv_source.read_text(),
                count=1,
            )
            self.assertEqual(replacements, 1)
            cv_source.write_text(updated)
            output = Path(directory) / "artifact"
            CV.render(source, output, REVISION)
            shutil.copytree(output, source, dirs_exist_ok=True)
            CV.verify(source, source, REVISION)
            subprocess.run(
                ["bundle", "exec", "jekyll", "build"],
                cwd=source,
                env={**os.environ, "JEKYLL_ENV": "production"},
                check=True,
            )
            html = (source / "_site/cv/index.html").read_text()
            self.assertIn("CV Publication Probe", html)
            pdf = source / "_site/assets/pdf/cv.pdf"
            self.assertEqual(pdf.read_bytes(), (output / CV.DOWNLOAD).read_bytes())
            self.assertIn(
                "CV Publication Probe",
                subprocess.check_output(["pdftotext", str(pdf), "-"], text=True),
            )
            self.assertEqual(
                json.loads((source / "_site" / CV.MANIFEST).read_text())[
                    "source_revision"
                ],
                REVISION,
            )


if __name__ == "__main__":
    unittest.main()
