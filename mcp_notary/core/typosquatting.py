"""Typosquatting detection for MCP server names."""

from __future__ import annotations

import json
from pathlib import Path

# Common prefixes and suffixes used in MCP server package names across registries.
# Stripped before comparison so "mcp-server-filesystem", "@org/server-filesystem"
# and "filesystem-mcp" all normalize to "filesystem".
_STRIP_PREFIXES = ("mcp-server-", "server-")
_STRIP_SUFFIXES = ("-mcp", "-server")


def _levenshtein(s1: str, s2: str) -> int:
    """Compute Levenshtein distance between two strings."""
    if len(s1) < len(s2):
        return _levenshtein(s2, s1)
    if len(s2) == 0:
        return len(s1)
    previous_row = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            current_row.append(min(
                previous_row[j + 1] + 1,
                current_row[j] + 1,
                previous_row[j] + (c1 != c2),
            ))
        previous_row = current_row
    return previous_row[-1]


def _strip_version(name: str) -> str:
    """Strip @version suffix, handling scoped packages (@scope/pkg@version).

    Scoped names start with @, so we can't split naively on the first @.
    """
    if name.startswith("@"):
        # @scope/pkg or @scope/pkg@version
        slash_pos = name.find("/")
        if slash_pos == -1:
            return name  # malformed scope, return as-is
        pkg_part = name[slash_pos + 1:]
        # Strip version from the pkg part only
        return name[:slash_pos + 1] + pkg_part.split("@")[0]
    return name.split("@")[0]


def _normalize_name(name: str) -> str:
    """Normalize a MCP server name for fuzzy comparison.

    Strips scope (@org/), common prefixes (mcp-server-, server-)
    and common suffixes (-mcp, -server), then lowercases.
    """
    # Strip @scope/ prefix
    if name.startswith("@") and "/" in name:
        name = name.split("/", 1)[1]

    name = name.lower()

    for prefix in _STRIP_PREFIXES:
        if name.startswith(prefix):
            name = name[len(prefix):]
            break

    for suffix in _STRIP_SUFFIXES:
        if name.endswith(suffix):
            name = name[: -len(suffix)]
            break

    return name


def _load_known_servers() -> list[str]:
    data_path = Path(__file__).parent.parent / "data" / "mcp-known-servers.json"
    with open(data_path, encoding="utf-8") as f:
        return json.load(f)["servers"]


def check_typosquatting(name: str, threshold: int = 2) -> list[dict[str, object]]:
    """Return known server names within Levenshtein distance of `name`.

    Comparison is done on normalized names (scope and common prefixes/suffixes
    stripped) so that "mcp-server-filesytem", "@org/server-filesytem" and
    "filesytem-mcp" all correctly match "filesystem".

    Returns list of {"name": str, "distance": int}, sorted by distance.
    Empty list means no suspicious matches found.
    """
    base_name = _strip_version(name)
    normalized_input = _normalize_name(base_name)

    seen_normalized: set[str] = set()
    matches = []

    for known_name in _load_known_servers():
        normalized_known = _normalize_name(known_name)

        # Skip exact match (not a typosquat)
        if normalized_known == normalized_input:
            continue

        # Deduplicate: multiple known entries that normalize to the same form
        # (e.g. "filesystem-mcp" and "filesystem") should produce one result.
        if normalized_known in seen_normalized:
            continue

        # Short names (<=6 chars) get a tighter threshold to avoid false positives
        # like "github" matching "gitlab" at distance 2.
        effective_threshold = threshold
        if len(normalized_input) <= 6 or len(normalized_known) <= 6:
            effective_threshold = min(threshold, 1)

        distance = _levenshtein(normalized_input, normalized_known)
        if distance <= effective_threshold:
            seen_normalized.add(normalized_known)
            matches.append({"name": known_name, "distance": distance})

    return sorted(matches, key=lambda x: x["distance"])
