"""Unit tests for provenance verification."""

from mcp_notary.core.provenance import (
    ProvenanceResult,
    ProvenanceStatus,
    verify_provenance,
)


class TestProvenanceResult:
    def test_default_warnings_empty(self):
        result = ProvenanceResult(status=ProvenanceStatus.UNKNOWN)
        assert result.warnings == []

    def test_status_values(self):
        for status in ProvenanceStatus:
            result = ProvenanceResult(status=status)
            assert result.status == status


class TestVerifyProvenance:
    def test_unknown_server_returns_unknown(self):
        result = verify_provenance("some-mcp-server-xyz")
        assert result.status == ProvenanceStatus.UNKNOWN

    def test_result_has_details(self):
        result = verify_provenance("some-mcp-server-xyz")
        assert len(result.details) > 0

    def test_version_accepted(self):
        result = verify_provenance("some-mcp-server-xyz", version="1.0.0")
        assert result.status in list(ProvenanceStatus)
