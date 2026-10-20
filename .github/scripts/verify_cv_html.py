"""Check CV navigation, heading order, and the PDF link after a Jekyll build."""

import re
import sys
from html.parser import HTMLParser
from pathlib import Path


class CVParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_main = False
        self.headings = []
        self.ids = []
        self.navigation_targets = []
        self.download_names = []
        self.heading = None
        self.anchor = None
        self.in_navigation = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "main":
            self.in_main = True
        if not self.in_main:
            return
        if attrs.get("id"):
            self.ids.append(attrs["id"])
        if re.fullmatch(r"h[1-6]", tag):
            self.heading = [int(tag[1]), "", attrs.get("id")]
        if tag == "nav" and attrs.get("aria-label") == "CV sections":
            self.in_navigation = True
        if tag == "a":
            href = attrs.get("href", "")
            self.anchor = [href, "", attrs.get("aria-label")]
            if self.in_navigation and href.startswith("#"):
                self.navigation_targets.append(href[1:])

    def handle_data(self, data):
        if self.heading is not None:
            self.heading[1] += data
        if self.anchor is not None:
            self.anchor[1] += data

    def handle_endtag(self, tag):
        if self.heading is not None and re.fullmatch(r"h[1-6]", tag):
            self.headings.append(self.heading)
            self.heading = None
        if tag == "a" and self.anchor is not None:
            href, text, label = self.anchor
            if href.endswith("/assets/pdf/cv.pdf"):
                self.download_names.append((label or text).strip())
            self.anchor = None
        if tag == "nav":
            self.in_navigation = False
        if tag == "main":
            self.in_main = False


def verify(html):
    cv = CVParser()
    cv.feed(html)
    if cv.download_names != ["Download CV (PDF)"]:
        raise ValueError("CV needs one named PDF download link")
    if not cv.headings or cv.headings[0][0] != 1:
        raise ValueError("CV must start with an h1")
    previous = 0
    for level, text, _ in cv.headings:
        if not text.strip() or level > previous + 1:
            raise ValueError("CV heading is empty or skips a level")
        previous = level
    if len(cv.ids) != len(set(cv.ids)):
        raise ValueError("CV has duplicate IDs")
    sections = [identifier for level, _, identifier in cv.headings if level == 2]
    if not sections or cv.navigation_targets != sections:
        raise ValueError("CV navigation must link to each section in reading order")
    print(f"Verified named CV download, heading order and {len(sections)} section links")


if __name__ == "__main__":
    verify((Path(sys.argv[1]) / "cv/index.html").read_text())
