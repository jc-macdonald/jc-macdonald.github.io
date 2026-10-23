"""Deterministic contrast checks for site tokens and retained figure colors."""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def relative_luminance(value):
    """Return WCAG relative luminance for a six-digit hex color."""
    channels = [int(value[index : index + 2], 16) / 255 for index in (1, 3, 5)]
    linear = [
        channel / 12.92 if channel <= 0.04045 else ((channel + 0.055) / 1.055) ** 2.4
        for channel in channels
    ]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast(first, second):
    """Return an unrounded WCAG contrast ratio."""
    luminances = sorted((relative_luminance(first), relative_luminance(second)))
    return (luminances[1] + 0.05) / (luminances[0] + 0.05)


class ColorContrastTests(unittest.TestCase):
    def assert_contrast(self, foreground, background, minimum, label):
        self.assertGreaterEqual(
            contrast(foreground, background),
            minimum,
            f"{label}: {foreground} on {background}",
        )

    def test_semantic_text_and_control_tokens(self):
        pairs = [
            ("#000000", "#ffffff", 4.5, "light body"),
            ("#5f6368", "#ffffff", 4.5, "light muted text"),
            ("#0d6b6e", "#ffffff", 4.5, "light link"),
            ("#ffffff", "#0d6b6e", 4.5, "light filled control"),
            ("#767676", "#ffffff", 3.0, "light control boundary"),
            ("#e8e8e8", "#1c1c1d", 4.5, "dark body"),
            ("#e8e8e8", "#212529", 4.5, "dark card body"),
            ("#a3a3a3", "#1c1c1d", 4.5, "dark muted text"),
            ("#4da8ab", "#1c1c1d", 4.5, "dark link"),
            ("#1c1c1d", "#4da8ab", 4.5, "dark filled control"),
            ("#a3a3a3", "#1c1c1d", 3.0, "dark control boundary"),
        ]
        for foreground, background, minimum, label in pairs:
            with self.subTest(label=label):
                self.assert_contrast(foreground, background, minimum, label)

        variables = (ROOT / "_sass/_variables.scss").read_text().lower()
        themes = (ROOT / "_sass/_themes.scss").read_text()
        for declaration in (
            "$muted-color-light: #5f6368;",
            "$muted-color-dark: #a3a3a3;",
            "$control-border-color-light: #767676;",
            "$control-border-color-dark: #a3a3a3;",
            "$code-bg-color-light: #f6f8fa;",
            "$code-bg-color-dark: #1f2328;",
        ):
            self.assertIn(declaration, variables)
        self.assertIn("--global-theme-on-color: #{v.$white-color};", themes)
        self.assertIn("--global-theme-on-color: #{v.$grey-color-dark};", themes)

    def test_admonition_tokens(self):
        pairs = [
            ("#215d42", "#e2f5ec", "light tip"),
            ("#6b5900", "#fff8d8", "light warning"),
            ("#cc0000", "#ffe0e0", "light danger"),
            ("#beffe2", "#215d42", "dark tip"),
            ("#fff2af", "#6b5900", "dark warning"),
            ("#ffb9b9", "#660000", "dark danger"),
        ]
        for foreground, background, label in pairs:
            with self.subTest(label=label):
                self.assert_contrast(foreground, background, 4.5, label)

    def test_bootstrap_tables_follow_theme_tokens_before_javascript(self):
        typography = (ROOT / "_sass/_typography.scss").read_text()
        self.assertRegex(
            typography,
            r"table,\s*\.table\s*\{\s*color:\s*var\(--global-text-color\);",
        )
        table_rule = re.search(
            r"table,\s*\.table\s*\{(?P<body>.*?)\n\}",
            typography,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(table_rule)
        self.assertIn(
            "border-color: var(--global-divider-color);", table_rule.group("body")
        )

    def test_mdb_card_text_follows_theme_tokens(self):
        components = (ROOT / "_sass/_components.scss").read_text()
        self.assertRegex(
            components,
            r"(?s)\.card-body\s*\{.*?\.card-text\s*\{\s*"
            r"color:\s*var\(--global-text-color\);",
        )

    def test_syntax_palettes(self):
        palettes = [
            (
                ROOT / "assets/css/jekyll-pygments-themes-github.css",
                ("#f6f8fa", "#fff8c5"),
            ),
            (
                ROOT / "assets/css/jekyll-pygments-themes-native.css",
                ("#1f2328", "#2d333b"),
            ),
        ]
        for path, backgrounds in palettes:
            source = path.read_text().lower()
            foregrounds = set(re.findall(r"(?<!-)color:\s*(#[0-9a-f]{6})", source))
            self.assertTrue(foregrounds, path)
            for foreground in foregrounds:
                for background in backgrounds:
                    with self.subTest(
                        path=path.name, color=foreground, background=background
                    ):
                        self.assert_contrast(foreground, background, 4.5, path.name)

        self.assert_contrast("#b31d28", "#ffebe9", 4.5, "light error token")
        self.assert_contrast("#116329", "#dafbe1", 4.5, "light inserted token")
        self.assert_contrast("#ff7b72", "#4c1f24", 4.5, "dark error token")

    def test_figure_line_colors(self):
        palette_source = (ROOT / "assets/img/research/palette.py").read_text()
        computed_source = (
            ROOT / "assets/img/research/computed/computed_examples.py"
        ).read_text()
        colors = set(
            re.findall(
                r'(?:TEAL_PRIMARY|BLUE_HEALTH|TEAL_ENVIRON|GREEN_EARTH|GOLD_ACCENT|CHARCOAL|SLATE)\s*=\s*"(#[0-9A-Fa-f]{6})"',
                palette_source,
            )
        )
        computed_match = re.search(
            r'TEAL, BLUE, GOLD, GREY = ("#[0-9a-f]{6}", ){3}"#[0-9a-f]{6}"',
            computed_source,
        )
        self.assertIsNotNone(computed_match)
        colors.update(re.findall(r"#[0-9a-f]{6}", computed_match.group(0)))
        self.assertIn("#87641A", colors)
        for color in colors:
            with self.subTest(color=color):
                self.assert_contrast(color, "#ffffff", 3.0, "figure line")


if __name__ == "__main__":
    unittest.main()
