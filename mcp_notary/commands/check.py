"""mcp-notary check command — pre-install verification."""

from __future__ import annotations

import json as _json

import typer

from mcp_notary.core.provenance import ProvenanceStatus, verify_provenance
from mcp_notary.core.typosquatting import check_typosquatting
from mcp_notary.output.sarif import print_sarif
from mcp_notary.output.table import print_check_result


def check(
    server: str = typer.Argument(..., help="MCP server name, optionally with @version (e.g. filesystem-mcp@1.2.3)"),
    json: bool = typer.Option(False, "--json", help="Output as JSON"),
    sarif: bool = typer.Option(False, "--sarif", help="Output as SARIF for GitHub Security tab"),
    offline: bool = typer.Option(False, "--offline", help="Skip network checks (typosquatting only)"),
) -> None:
    """Verify a MCP server before installing it.

    Checks provenance, manifest integrity and detects typosquatting.
    """
    # Pass full name to check_typosquatting; it handles scope and version stripping.
    typosquats = check_typosquatting(server)

    # Extract base_name (no version) and version for provenance, scoped-package-aware.
    if server.startswith("@"):
        slash_pos = server.find("/")
        if slash_pos != -1:
            pkg_part = server[slash_pos + 1:]
            pkg_parts = pkg_part.split("@")
            base_name = server[:slash_pos + 1] + pkg_parts[0]
            version = pkg_parts[1] if len(pkg_parts) > 1 else None
        else:
            base_name = server
            version = None
    else:
        parts = server.split("@")
        base_name = parts[0]
        version = parts[1] if len(parts) > 1 else None

    if offline:
        from mcp_notary.core.provenance import ProvenanceResult
        provenance = ProvenanceResult(
            status=ProvenanceStatus.UNKNOWN,
            details="Offline mode: provenance check skipped.",
        )
    else:
        provenance = verify_provenance(base_name, version)

    if sarif:
        print_sarif(server, provenance, typosquats)
    elif json:
        result = {
            "server": server,
            "provenance": {
                "status": provenance.status.value,
                "source_url": provenance.source_url,
                "version": provenance.version,
                "details": provenance.details,
                "warnings": provenance.warnings,
            },
            "typosquatting": typosquats,
        }
        print(_json.dumps(result, indent=2))
    else:
        print_check_result(server, provenance, typosquats)

    # Exit 1 if provenance failed or typosquats found
    if provenance.status == ProvenanceStatus.ERROR or typosquats:
        raise typer.Exit(1)
