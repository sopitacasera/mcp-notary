"""Provenance verification for MCP servers via GitHub API."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class ProvenanceStatus(str, Enum):
    VERIFIED = "verified"
    UNVERIFIED = "unverified"
    UNKNOWN = "unknown"
    ERROR = "error"


@dataclass
class ProvenanceResult:
    status: ProvenanceStatus
    source_url: str = ""
    version: str = ""
    commit_hash: str = ""
    manifest_hash: str = ""
    details: str = ""
    warnings: list[str] = field(default_factory=list)


def verify_provenance(server_name: str, version: str | None = None) -> ProvenanceResult:
    """Verify provenance of a MCP server release.

    Currently returns UNKNOWN for servers without a registered manifest.
    Full implementation in Sprint 1 development phase.
    """
    # TODO: implement GitHub API lookup in Sprint 1
    return ProvenanceResult(
        status=ProvenanceStatus.UNKNOWN,
        details=(
            f"No signed manifest found for {server_name}. "
            "Ask the server author to publish a signed manifest with mcp-notary."
        ),
    )
