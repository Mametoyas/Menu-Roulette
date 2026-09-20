"""Vercel entry point.

Exposes the Flask WSGI app from src/web_app.py as ``app`` so Vercel's
Python runtime can serve the entire application through a single function.
"""

import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_SRC = _PROJECT_ROOT / "src"

for _path in (str(_PROJECT_ROOT), str(_SRC)):
    if _path not in sys.path:
        sys.path.insert(0, _path)

from web_app import app  # noqa: E402