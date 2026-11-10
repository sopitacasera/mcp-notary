"""mcp-notary CLI entry point."""

from __future__ import annotations

import typer

from mcp_notary import __version__
from mcp_notary.commands.check import check

app = typer.Typer(
    name="mcp-notary",
    help="Pre-install trust verification for MCP servers.",
    add_completion=False,
)

app.command(name="check")(check)


def version_callback(value: bool) -> None:
    if value:
        print(f"mcp-notary {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        None, "--version", "-v", callback=version_callback, is_eager=True,
        help="Show version and exit.",
    ),
) -> None:
    """mcp-notary — verify MCP servers before you install them."""
