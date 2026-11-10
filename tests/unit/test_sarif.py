"""Unit tests for SARIF output generation."""

from mcp_notary.core.provenance import ProvenanceResult, ProvenanceStatus
from mcp_notary.output.sarif import build_sarif


def _make_provenance(status: ProvenanceStatus, details: str = "") -> ProvenanceResult:
    return ProvenanceResult(status=status, details=details)


class TestBuildSarif:
    def test_sarif_version(self):
        sarif = build_sarif("test-mcp", _make_provenance(ProvenanceStatus.VERIFIED), [])
        assert sarif["version"] == "2.1.0"

    def test_no_issues_empty_results(self):
        sarif = build_sarif("test-mcp", _make_provenance(ProvenanceStatus.VERIFIED), [])
        assert sarif["runs"][0]["results"] == []

    def test_typosquat_generates_warning(self):
        typosquats = [{"name": "filesystem-mcp", "distance": 1}]
        sarif = build_sarif("filesysterm-mcp", _make_provenance(ProvenanceStatus.UNKNOWN), typosquats)
        results = sarif["runs"][0]["results"]
        assert any(r["ruleId"] == "MN001" and r["level"] == "warning" for r in results)

    def test_error_provenance_generates_error(self):
        sarif = build_sarif("bad-mcp", _make_provenance(ProvenanceStatus.ERROR, "failed"), [])
        results = sarif["runs"][0]["results"]
        assert any(r["ruleId"] == "MN002" and r["level"] == "error" for r in results)

    def test_tool_name_in_output(self):
        sarif = build_sarif("test-mcp", _make_provenance(ProvenanceStatus.UNKNOWN), [])
        assert sarif["runs"][0]["tool"]["driver"]["name"] == "mcp-notary"
