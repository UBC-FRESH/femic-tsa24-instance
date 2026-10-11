from __future__ import annotations

from importlib.util import find_spec
from pathlib import Path

project = "femic-tsa24-instance"
author = "UBC-FRESH"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]
autosummary_generate = True
autodoc_typehints = "description"
templates_path = ["_templates"]
exclude_patterns = ["_build"]

if find_spec("sphinx_rtd_theme"):
    html_theme = "sphinx_rtd_theme"
else:
    html_theme = "alabaster"
html_theme_options = {"collapse_navigation": False, "navigation_depth": 3}

_static_dir = Path(__file__).with_name("_static")
html_static_path = ["_static"] if _static_dir.exists() else []
