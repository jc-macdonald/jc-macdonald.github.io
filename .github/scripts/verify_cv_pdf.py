#!/usr/bin/env python3
"""Check basic PDF metadata, tagging, fonts and extractable reading content.

These checks catch common publication regressions. They are not a claim of
PDF/UA conformance and do not replace manual assistive-technology review.
"""

import argparse
import re
import subprocess
from pathlib import Path


def command(*args):
    completed = subprocess.run(args, check=True, capture_output=True, text=True)
    return completed.stdout


def fields(output):
    return {
        key.strip(): value.strip()
        for line in output.splitlines()
        if ":" in line
        for key, value in [line.split(":", 1)]
    }


def source_name(source):
    match = re.search(r"(?m)^  name:\s*[\"']?([^\n\"']+)", source.read_text())
    if not match:
        raise ValueError("Cannot read the CV name from its source")
    return match.group(1).strip()


def verify(pdf, source):
    if not pdf.read_bytes().startswith(b"%PDF-"):
        raise ValueError("CV output is not a PDF")

    expected_name = source_name(source)
    info = fields(command("pdfinfo", str(pdf)))
    required = {
        "Tagged": "yes",
        "Suspects": "no",
        "Encrypted": "no",
        "JavaScript": "no",
    }
    for key, value in required.items():
        if info.get(key, "").lower() != value:
            raise ValueError(f"Unexpected PDF metadata: {key}={info.get(key)!r}")
    if expected_name not in info.get("Title", "") or expected_name not in info.get("Author", ""):
        raise ValueError("PDF title and author must identify the CV owner")
    pages = int(info.get("Pages", "0"))
    if pages < 1:
        raise ValueError("PDF has no pages")

    font_rows = command("pdffonts", str(pdf)).splitlines()[2:]
    if not font_rows or any(not re.search(r"\s+yes\s+yes\s+yes\s+\d+\s+\d+$", row) for row in font_rows if row.strip()):
        raise ValueError("Every PDF font must be embedded, subset and Unicode-mapped")

    extracted = command("pdftotext", "-layout", str(pdf), "-")
    extracted_pages = [page for page in extracted.split("\f") if page.strip()]
    if len(extracted_pages) != pages or expected_name not in extracted_pages[0]:
        raise ValueError("PDF text extraction or page reading order is incomplete")
    if any(len(re.sub(r"\s+", "", page)) < 40 for page in extracted_pages):
        raise ValueError("A PDF page has too little extractable text")

    print(f"Verified basic PDF semantics for {pages} pages and {len(font_rows)} fonts")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--source", type=Path, default=Path("_data/cv.yml"))
    arguments = parser.parse_args()
    verify(arguments.pdf, arguments.source)
