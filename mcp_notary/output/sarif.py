"""SARIF export for GitHub Security tab integration."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mcp_notary.core.provenance import ProvenanceResult


SARIF_VERSION = "2.1.0"
TOOL_NAME = "mcp-notary"
TOOL_VERSION = "0.1.0"


def build_sarif(
    server: str,
    provenance: ProvenanceResult,
    typosquats: list[dict],
) -> dict:
    """Build a SARIF 2.1.0 report for a check result."""
    results = []

    if typosquats:
        for typo in typosquats:
            results.append({
                "ruleId": "MN001",
                "level": "warning",
                "message": {
                    "text": (
                        f"Server name '{server}' is similar to known server "
                        f"'{typo['name']}' (Levenshtein distance: {typo['distance']}). "
                        "Possible typosquatting."
                    )
                },
            })

    if provenance.status.value in ("unverified", "error"):
        results.append({
            "ruleId": "MN002",
            "level": "error",
            "message": {"text": f"Provenance verification failed: {provenance.details}"},
        })

    return {
        "version": SARIF_VERSION,
        "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": TOOL_NAME,
                        "version": TOOL_VERSION,
                        "rules": [
                            {"id": "MN001", "name": "TyposquattingDetected", "shortDescription": {"text": "Possible typosquatting"}},
                            {"id": "MN002", "name": "ProvenanceFailed", "shortDescription": {"text": "Provenance verification failed"}},
                        ],
                    }
                },
                "results": results,
            }
        ],
    }


def print_sarif(server: str, provenance: ProvenanceResult, typosquats: list[dict]) -> None:
    print(json.dumps(build_sarif(server, provenance, typosquats), indent=2))
