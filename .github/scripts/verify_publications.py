"""Check published order and public citation metadata after the Jekyll build."""

import argparse
import json
from html.parser import HTMLParser
from pathlib import Path


class Publications(HTMLParser):
    def __init__(self):
        super().__init__()
        self.order = []
        self.records = []
        self._json = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("data-publication-status") == "published":
            self.order.append(attrs["id"])
        if tag == "script" and attrs.get("type") == "application/ld+json":
            self._json = []

    def handle_data(self, data):
        if self._json is not None:
            self._json.append(data)

    def handle_endtag(self, tag):
        if tag == "script" and self._json is not None:
            record = json.loads("".join(self._json))
            if record.get("@type") == "ScholarlyArticle":
                self.records.append(record)
            self._json = None


def verify(site, expected):
    parsed = Publications()
    parsed.feed((site / "publications/index.html").read_text())
    wanted = expected["published_order"]
    if parsed.order != wanted:
        raise ValueError(f"Published order differs: {parsed.order}; expected {wanted}")
    actual = {record["identifier"]: record for record in parsed.records}
    if len(actual) != len(parsed.records) or set(actual) != set(expected["records"]):
        raise ValueError("Public citation metadata is missing or duplicated")
    for doi, fields in expected["records"].items():
        record = actual[doi]
        names = [author["name"] for author in record["author"]]
        if names != fields["authors"]:
            raise ValueError(f"Author names/order differ for {doi}: {names}")
        for field in ("headline", "pagination", "datePublished"):
            if field in fields and str(record.get(field)) != str(fields[field]):
                raise ValueError(f"Incorrect {field} for {doi}: {record.get(field)}")
        containers = {}
        part = record.get("isPartOf", {})
        while part:
            containers[part["@type"]] = part
            part = part.get("isPartOf", {})
        for field, kind in (("volumeNumber", "PublicationVolume"), ("issueNumber", "PublicationIssue")):
            if field in record or (field in fields and str(containers.get(kind, {}).get(field)) != str(fields[field])):
                raise ValueError(f"Incorrect {field} container for {doi}")
    print(f"Verified newest-first order and metadata for {len(actual)} public articles/preprints")


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("site", type=Path)
    args = cli.parse_args()
    root = Path(__file__).resolve().parents[2]
    verify(args.site, json.loads((root / ".github/publication-reference.json").read_text()))
