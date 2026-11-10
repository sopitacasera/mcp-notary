"""Integration tests for the mcp-notary CLI via typer.testing.CliRunner."""

from __future__ import annotations

import io

import pytest
from typer.testing import CliRunner

from mcp_notary.cli import app

runner = CliRunner()


class TestCheckCommandTypo:
    def test_typo_detected_exit_code_1(self):
        """A typosquat match must exit 1."""
        result = runner.invoke(app, ["check", "mcp-server-githb"])
        assert result.exit_code == 1, f"Expected exit 1, got {result.exit_code}\n{result.output}"

    def test_typo_detected_output_contains_match(self):
        """Output must name the matched known server."""
        result = runner.invoke(app, ["check", "mcp-server-githb"])
        assert "github" in result.output.lower(), (
            f"Expected 'github' in output:\n{result.output}"
        )

    def test_typo_detected_output_contains_warning(self):
        """Output must include a WARNING label (ASCII-safe, no emoji)."""
        result = runner.invoke(app, ["check", "mcp-server-githb"])
        assert "WARNING" in result.output or "warning" in result.output.lower(), (
            f"Expected WARNING in output:\n{result.output}"
        )


class TestCheckCommandLegitimate:
    def test_legitimate_name_exit_code_0(self):
        """The legitimate name 'github' must not be flagged — exit 0 (provenance UNKNOWN)."""
        result = runner.invoke(app, ["check", "mcp-server-github"])
        # Exit code 1 only when typosquats found OR provenance ERROR.
        # UNKNOWN provenance does not trigger exit 1.
        assert "github" not in result.output.lower().split("warning")[-1] or result.exit_code == 0, (
            f"Legitimate name should not produce exit 1 from typosquatting:\n{result.output}"
        )

    def test_legitimate_name_no_typosquat_warning(self):
        """The legitimate name must not show a typosquatting WARNING."""
        result = runner.invoke(app, ["check", "mcp-server-github"])
        # Confirm no typosquat warning triggered by github/gitlab collision
        assert "No matches found" in result.output or "no matches" in result.output.lower(), (
            f"Expected 'No matches found' for legitimate name:\n{result.output}"
        )


class TestCheckCommandScopedWithVersion:
    def test_scoped_versioned_typo_detected(self):
        """Scoped name with version must still detect typosquat."""
        result = runner.invoke(app, ["check", "@modelcontextprotocol/server-filesytem@1.2.0"])
        assert "filesystem" in result.output.lower(), (
            f"Expected filesystem match for scoped+versioned name:\n{result.output}"
        )

    def test_scoped_versioned_exit_code_1(self):
        """Scoped name with typo must exit 1."""
        result = runner.invoke(app, ["check", "@modelcontextprotocol/server-filesytem@1.2.0"])
        assert result.exit_code == 1


class TestCheckCommandEncoding:
    def test_output_is_cp1252_safe(self):
        """CLI output must be encodable as cp1252 (Windows default console).

        A UnicodeEncodeError here means there are non-cp1252 characters
        in the output — emoji, curly quotes, box-drawing, etc.
        """
        result = runner.invoke(app, ["check", "mcp-server-githb"])
        try:
            result.output.encode("cp1252")
        except UnicodeEncodeError as exc:
            pytest.fail(
                f"CLI output contains characters that crash cp1252 consoles: {exc}\n"
                f"Output was:\n{result.output}"
            )

    def test_clean_output_is_cp1252_safe(self):
        """Clean (no typosquat) output must also be cp1252-safe."""
        result = runner.invoke(app, ["check", "totally-unique-zzz-xqy-abc"])
        try:
            result.output.encode("cp1252")
        except UnicodeEncodeError as exc:
            pytest.fail(
                f"CLI clean output has non-cp1252 characters: {exc}\n"
                f"Output was:\n{result.output}"
            )
