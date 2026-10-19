"""Bounded behavioral controls for extraction and the production Lychee command."""

import importlib.util
import os
import subprocess
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from tempfile import TemporaryDirectory
from threading import Thread

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "source_links", ROOT / ".github/scripts/check_source_links.py"
)
SOURCE_LINKS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SOURCE_LINKS)


class LinkTests(unittest.TestCase):
    def test_extraction_uses_only_external_anchors(self):
        parser = SOURCE_LINKS.ExternalAnchors()
        parser.feed(
            '<a href="https://example.org/?a=1&amp;b=2">Link</a><a href="/cv/">CV</a>'
            '<script src="https://cdn.example.org/theme.js"></script>'
            '<a href="mailto:person@example.org">Email</a><a href="//example.org/">URL</a>'
        )
        self.assertEqual(
            parser.urls, {"https://example.org/?a=1&b=2", "https://example.org/"}
        )

    def test_unresolved_liquid_fails(self):
        with self.assertRaisesRegex(ValueError, "Liquid"):
            SOURCE_LINKS.ExternalAnchors().feed(
                '<a href="{{ site.url }}/project">Project</a>'
            )

    def test_missing_maintained_page_fails(self):
        with TemporaryDirectory() as directory:
            manifest = Path(directory) / "pages.txt"
            manifest.write_text("missing/index.html\n")
            with self.assertRaisesRegex(ValueError, "no output"):
                SOURCE_LINKS.collect(Path(directory), manifest)

    def test_checker_rejects_broken_target_and_accepts_correction(self):
        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200 if self.path == "/exists/README.md" else 404)
                self.end_headers()
                self.wfile.write(b"fixture")

            def log_message(self, *args):
                pass

        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        worker = Thread(target=server.serve_forever, daemon=True)
        worker.start()
        try:
            with TemporaryDirectory() as directory:
                fixture = Path(directory) / "links.txt"
                command = [
                    os.environ.get("LYCHEE", "lychee"),
                    "--config",
                    str(ROOT / ".github/lychee.toml"),
                    "--no-progress",
                    str(fixture),
                ]
                fixture.write_text(
                    f"http://127.0.0.1:{server.server_port}/missing/README.md\n"
                )
                broken = subprocess.run(
                    command, capture_output=True, text=True, timeout=60
                )
                self.assertNotEqual(broken.returncode, 0, broken.stdout + broken.stderr)
                self.assertIn("404", broken.stdout + broken.stderr)
                fixture.write_text(
                    f"http://127.0.0.1:{server.server_port}/exists/README.md\n"
                )
                corrected = subprocess.run(
                    command, capture_output=True, text=True, timeout=60
                )
                self.assertEqual(
                    corrected.returncode, 0, corrected.stdout + corrected.stderr
                )
        finally:
            server.shutdown()
            server.server_close()
            worker.join()


if __name__ == "__main__":
    unittest.main()
