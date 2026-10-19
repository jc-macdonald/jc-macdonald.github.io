"""Publication regressions must fail for order, author and citation errors."""

import importlib.util
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "verify_publications", ROOT / ".github/scripts/verify_publications.py"
)
PUBLICATIONS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PUBLICATIONS)

EXPECTED = {
    "published_order": ["new", "old"],
    "records": {
        "new-doi": {"authors": ["First Author", "Second Author"], "pagination": "e51"},
        "old-doi": {"authors": ["Third Author"], "volumeNumber": "6"},
    },
}


def entry(key, doi, names, **fields):
    record = {
        "@type": "ScholarlyArticle",
        "identifier": doi,
        "author": [{"name": name} for name in names],
        **fields,
    }
    return f'<div id="{key}" data-publication-status="published"></div><script type="application/ld+json">{json.dumps(record)}</script>'


NEW = entry("new", "new-doi", ["First Author", "Second Author"], pagination="e51")
OLD = entry("old", "old-doi", ["Third Author"], isPartOf={"@type": "PublicationVolume", "volumeNumber": "6"})


class PublicationTests(unittest.TestCase):
    def check_html(self, html):
        with TemporaryDirectory() as directory:
            site = Path(directory)
            (site / "publications").mkdir()
            (site / "publications/index.html").write_text(html)
            PUBLICATIONS.verify(site, EXPECTED)

    def test_verified_order_and_complete_metadata_pass(self):
        self.check_html(NEW + OLD)

    def test_append_new_paper_at_end_fails(self):
        with self.assertRaisesRegex(ValueError, "Published order differs"):
            self.check_html(OLD + NEW)

    def test_swapped_authors_fail(self):
        wrong = entry("new", "new-doi", ["Second Author", "First Author"], pagination="e51")
        with self.assertRaisesRegex(ValueError, "Author names/order differ"):
            self.check_html(wrong + OLD)

    def test_wrong_article_number_fails(self):
        with self.assertRaisesRegex(ValueError, "Incorrect pagination"):
            self.check_html(NEW.replace("e51", "e45") + OLD)
