"""Unit tests for typosquatting detection."""

import pytest
from mcp_notary.core.typosquatting import _levenshtein, check_typosquatting


class TestLevenshtein:
    def test_identical_strings(self):
        assert _levenshtein("abc", "abc") == 0

    def test_empty_string(self):
        assert _levenshtein("", "abc") == 3
        assert _levenshtein("abc", "") == 3

    def test_single_substitution(self):
        assert _levenshtein("abc", "abd") == 1

    def test_single_insertion(self):
        assert _levenshtein("ac", "abc") == 1

    def test_single_deletion(self):
        assert _levenshtein("abbc", "abc") == 1

    def test_known_typosquat(self):
        # "filesysterm-mcp" vs "filesystem-mcp" — one transposition
        assert _levenshtein("filesysterm-mcp", "filesystem-mcp") == 1

    def test_symmetric(self):
        assert _levenshtein("abc", "xyz") == _levenshtein("xyz", "abc")


class TestCheckTyposquatting:
    def test_exact_match_not_returned(self):
        """An exact match against a known server should not be flagged."""
        results = check_typosquatting("filesystem-mcp")
        names = [r["name"] for r in results]
        assert "filesystem-mcp" not in names

    def test_typosquat_detected(self):
        """A one-character typo of a known server should be detected."""
        results = check_typosquatting("filesysterm-mcp")
        names = [r["name"] for r in results]
        assert "filesystem-mcp" in names

    def test_version_stripped(self):
        """Version suffix should be ignored in comparison."""
        results_no_ver = check_typosquatting("filesysterm-mcp")
        results_ver = check_typosquatting("filesysterm-mcp@1.0.0")
        assert [r["name"] for r in results_no_ver] == [r["name"] for r in results_ver]

    def test_unrelated_name_no_match(self):
        """A completely different name should return no matches."""
        results = check_typosquatting("totally-unrelated-zzz-xqy")
        assert results == []

    def test_results_sorted_by_distance(self):
        """Results should be sorted ascending by Levenshtein distance."""
        results = check_typosquatting("filesysterm-mcp")
        distances = [r["distance"] for r in results]
        assert distances == sorted(distances)

    def test_case_insensitive(self):
        """Check should be case-insensitive."""
        lower = check_typosquatting("filesystem-mcp")
        upper = check_typosquatting("FILESYSTEM-MCP")
        # Both should return same results (excluding self-match)
        assert [r["name"] for r in lower] == [r["name"] for r in upper]

    def test_mcp_server_prefix_typo(self):
        """mcp-server-X prefix must be stripped before comparison."""
        results = check_typosquatting("mcp-server-filesytem")
        names = [r["name"] for r in results]
        assert any("filesystem" in n for n in names), f"Expected filesystem match, got: {names}"

    def test_scoped_package_typo(self):
        """@scope/server-X must strip scope and server- prefix before comparison."""
        results = check_typosquatting("@modelcontextprotocol/server-filesytem")
        names = [r["name"] for r in results]
        assert any("filesystem" in n for n in names), f"Expected filesystem match, got: {names}"

    def test_mcp_server_github_typo(self):
        """mcp-server-githb must normalize to 'githb' and match 'github'."""
        results = check_typosquatting("mcp-server-githb")
        names = [r["name"] for r in results]
        assert any("github" in n for n in names), f"Expected github match, got: {names}"
