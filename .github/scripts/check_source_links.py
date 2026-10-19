"""Collect external anchors after Jekyll has resolved Markdown and Liquid."""

import argparse
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit


class ExternalAnchors(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.urls = set()

    def handle_starttag(self, tag, attrs):
        if tag != "a":
            return
        for name, value in attrs:
            if name != "href" or not value:
                continue
            if "{{" in value or "{%" in value:
                raise ValueError(f"Unresolved Liquid in anchor: {value}")
            if value.startswith("//"):
                value = "https:" + value
            if urlsplit(value).scheme.lower() in {"http", "https"}:
                self.urls.add(value)


def collect(site, manifest):
    urls = set()
    for line in manifest.read_text().splitlines():
        pattern = line.split("#", 1)[0].strip()
        if not pattern:
            continue
        pages = sorted(site.glob(pattern))
        if not pages:
            raise ValueError(f"Maintained page pattern has no output: {pattern}")
        for page in pages:
            parser = ExternalAnchors()
            parser.feed(page.read_text())
            urls.update(parser.urls)
    if not urls:
        raise ValueError("No external anchors found in maintained pages")
    return sorted(urls)


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("site", type=Path)
    cli.add_argument("output", type=Path)
    cli.add_argument(
        "--manifest", type=Path, default=Path(".github/source-link-pages.txt")
    )
    args = cli.parse_args()
    links = collect(args.site, args.manifest)
    args.output.write_text("\n".join(links) + "\n")
    print(f"Collected {len(links)} distinct external anchors into {args.output}")
