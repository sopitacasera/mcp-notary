"""Rich table output for mcp-notary check results."""

from __future__ import annotations

from typing import TYPE_CHECKING

try:
    from rich import box
    from rich.console import Console
    from rich.table import Table
    _RICH_AVAILABLE = True
except ImportError:
    _RICH_AVAILABLE = False

if TYPE_CHECKING:
    from mcp_notary.core.provenance import ProvenanceResult


console = Console() if _RICH_AVAILABLE else None


def print_check_result(
    server: str,
    provenance: ProvenanceResult,
    typosquats: list[dict],
    json_output: bool = False,
) -> None:
    """Print check result to stdout as a rich table or plain text."""
    if not _RICH_AVAILABLE or json_output:
        _print_plain(server, provenance, typosquats)
        return
    _print_rich(server, provenance, typosquats)


def _print_plain(server: str, provenance: ProvenanceResult, typosquats: list[dict]) -> None:
    print(f"mcp-notary check {server}")
    print(f"  Status:       {provenance.status.value.upper()}")
    print(f"  Details:      {provenance.details}")
    if typosquats:
        print(f"  Typosquatting WARNING: similar to {', '.join(t['name'] for t in typosquats)}")
    else:
        print("  Typosquatting: No matches found")


def _print_rich(server: str, provenance: ProvenanceResult, typosquats: list[dict]) -> None:
    assert console is not None
    # box.ASCII uses only +, -, | characters — safe for cp1252 and all Windows consoles.
    table = Table(title=f"mcp-notary check {server}", box=box.ASCII, show_header=False)
    table.add_column("Field", style="bold cyan")
    table.add_column("Value")
    table.add_row("Status", provenance.status.value.upper())
    if provenance.source_url:
        table.add_row("Source", provenance.source_url)
    if provenance.version:
        table.add_row("Version", provenance.version)
    table.add_row("Details", provenance.details)
    if typosquats:
        names = ", ".join(f"{t['name']} (d={t['distance']})" for t in typosquats)
        table.add_row("Typosquatting", f"[bold yellow]WARNING[/bold yellow] {names}")
    else:
        table.add_row("Typosquatting", "[green]No matches found[/green]")
    console.print(table)
