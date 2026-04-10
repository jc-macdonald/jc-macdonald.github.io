"""
Unified color palette for all research figures and presentations.

Option A: Dark teal core, domain siblings, gold accent.

Usage:
    from palette import COLORS, DOMAIN, ROLE, apply_theme
"""

# ── Core brand colors ─────────────────────────────────────────────────────────

TEAL_PRIMARY = "#0D6B6E"  # Primary brand — bridges health-blue and environmental-green
TEAL_LIGHT = "#4DA8AB"  # Light mode variant (dark-mode links, lighter accents)

BLUE_HEALTH = "#2471A3"  # Health systems domain — clinical, institutional
TEAL_ENVIRON = "#148F77"  # Environmental domain — marine, ocean, living systems
GREEN_EARTH = "#1E8449"  # Earth/terrestrial domain — agriculture, land, fire
GOLD_ACCENT = "#D4AC0D"  # Decision support / outputs / enabling — punchline color

CHARCOAL = "#2C3E50"  # Theory, infrastructure, dark text
SLATE = "#5D6D7E"  # Secondary text, labels
LIGHT_BG = "#F7F9F9"  # Panel backgrounds (light)
WHITE = "#FFFFFF"

# ── Semantic groupings ────────────────────────────────────────────────────────

DOMAIN = {
    "health": BLUE_HEALTH,
    "environment": TEAL_ENVIRON,
    "earth": GREEN_EARTH,
    "epi": BLUE_HEALTH,  # alias
    "ocean": TEAL_ENVIRON,  # alias
    "marine": TEAL_ENVIRON,  # alias
    "fire": GOLD_ACCENT,  # terrestrial hazard → accent
    "agri": GREEN_EARTH,  # alias
}

ROLE = {
    "primary": TEAL_PRIMARY,
    "primary_light": TEAL_LIGHT,
    "accent": GOLD_ACCENT,
    "text": CHARCOAL,
    "text_light": SLATE,
    "bg": LIGHT_BG,
    "foundation": CHARCOAL,  # infrastructure layer
}

# ── Per-figure color dictionaries (drop-in replacements) ──────────────────────

# beyond_onehealth_figure.py
BEYOND_ONEHEALTH = {
    "foundation": {"bg": LIGHT_BG, "accent": SLATE, "dark": CHARCOAL},
    "epi": {"bg": "#E8F0FE", "accent": BLUE_HEALTH, "dark": "#1A5276"},
    "ocean": {"bg": "#E8F6F3", "accent": TEAL_ENVIRON, "dark": "#0E6655"},
    "fire": {"bg": "#FEF9E7", "accent": GOLD_ACCENT, "dark": "#9A7D0A"},
    "agri": {"bg": "#E8F8F5", "accent": GREEN_EARTH, "dark": "#145A32"},
}

# future_directions_figure.py
FUTURE_DIRECTIONS = {
    "generalize": {"bg": "#E8F0FE", "accent": BLUE_HEALTH, "dark": "#1A5276"},
    "extend": {"bg": "#E8F8F5", "accent": GREEN_EARTH, "dark": "#145A32"},
    "enable": {"bg": "#FEF9E7", "accent": GOLD_ACCENT, "dark": "#7D6608"},
}

# op_engine / op_system figures
INFRA = {
    "system": {"bg": "#E8F0FE", "accent": BLUE_HEALTH, "dark": "#1A5276"},
    "engine": {"bg": "#E8F6F3", "accent": TEAL_ENVIRON, "dark": "#0E6655"},
    "output": {"bg": "#FEF9E7", "accent": GOLD_ACCENT, "dark": "#7D6608"},
}


def apply_theme() -> None:
    """Apply consistent matplotlib rcParams for all figures."""
    import matplotlib.pyplot as plt

    plt.rcParams.update(
        {
            "font.size": 12,
            "font.family": "sans-serif",
            "figure.facecolor": WHITE,
            "axes.facecolor": WHITE,
            "text.color": CHARCOAL,
            "axes.labelcolor": CHARCOAL,
            "xtick.color": SLATE,
            "ytick.color": SLATE,
        }
    )
