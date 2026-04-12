"""Digest rendering scaffolding for Kasandra."""

from __future__ import annotations

from typing import Iterable


def render_digest(lines: Iterable[str]) -> str:
    """Render a simple line-based digest."""
    return "\n".join(lines)
