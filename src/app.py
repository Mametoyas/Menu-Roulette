"""Vercel entry point.

Vercel auto-detects Flask by looking for a module-level ``app`` instance in a
recognized entry file (src/app.py). Keep this file minimal — it only re-exports
the real Flask app from web_app.py so routing stays unchanged.
"""

import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parent
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from web_app import app  # noqa: E402