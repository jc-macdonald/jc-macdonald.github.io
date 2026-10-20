"""Controls for the CV's rendered HTML accessibility checks."""

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "verify_cv_html", ROOT / ".github/scripts/verify_cv_html.py"
)
CV = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CV)

HTML = """<main><h1>CV</h1>
<a href="/assets/pdf/cv.pdf"><i aria-hidden="true"></i> Download CV (PDF)</a>
<nav aria-label="CV sections"><details><summary>Jump to a CV section</summary>
<ul><li><a href="#appointments">Appointments</a></li></ul></details></nav>
<section aria-labelledby="appointments"><h2 id="appointments">Appointments</h2>
<h3>Assistant Scientist</h3></section></main>"""


class CVHTMLTests(unittest.TestCase):
    def test_named_download_and_ordered_sections_pass(self):
        CV.verify(HTML)

    def test_icon_only_download_fails(self):
        with self.assertRaisesRegex(ValueError, "named PDF"):
            CV.verify(HTML.replace(" Download CV (PDF)", ""))

    def test_skipped_heading_level_fails(self):
        with self.assertRaisesRegex(ValueError, "skips a level"):
            CV.verify(HTML.replace(
                '<h2 id="appointments">Appointments</h2>',
                '<h3 id="appointments">Appointments</h3>',
            ))

    def test_broken_section_navigation_fails(self):
        with self.assertRaisesRegex(ValueError, "navigation"):
            CV.verify(HTML.replace('href="#appointments"', 'href="#missing"'))

    def test_duplicate_section_id_fails(self):
        with self.assertRaisesRegex(ValueError, "duplicate IDs"):
            CV.verify(HTML.replace('<h3>', '<h3 id="appointments">'))


if __name__ == "__main__":
    unittest.main()
