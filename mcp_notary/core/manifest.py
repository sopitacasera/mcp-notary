"""MCP server manifest parser — static reads only, no code execution."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from mcp_notary.exceptions import ManifestNotFoundError


def parse_manifest(source: str | Path) -> dict[str, Any]:
    """Parse a manifest JSON file from a local path or string content."""
    if isinstance(source, Path):
        if not source.exists():
            raise ManifestNotFoundError(f"Manifest not found: {source}")
        content = source.read_text(encoding="utf-8")
    else:
        content = source
    try:
        return json.loads(content)
    except json.JSONDecodeError as exc:
        raise ManifestNotFoundError(f"Invalid manifest JSON: {exc}") from exc


def hash_manifest(content: str) -> str:
    """Return sha256 hex digest of manifest content."""
    return "sha256:" + hashlib.sha256(content.encode()).hexdigest()


def extract_tools(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    """Extract tool definitions from a parsed manifest."""
    return manifest.get("tools", [])
