"""Unit tests for manifest parsing."""

import json
import pytest
from mcp_notary.core.manifest import parse_manifest, hash_manifest, extract_tools
from mcp_notary.exceptions import ManifestNotFoundError


SAMPLE_MANIFEST = {
    "name": "filesystem-mcp",
    "version": "1.2.3",
    "tools": [
        {"name": "read_file", "description": "Read a file"},
        {"name": "write_file", "description": "Write a file"},
    ],
}


class TestParseManifest:
    def test_parse_valid_json_string(self):
        result = parse_manifest(json.dumps(SAMPLE_MANIFEST))
        assert result["name"] == "filesystem-mcp"
        assert result["version"] == "1.2.3"

    def test_parse_from_path(self, tmp_path):
        manifest_file = tmp_path / "manifest.json"
        manifest_file.write_text(json.dumps(SAMPLE_MANIFEST), encoding="utf-8")
        result = parse_manifest(manifest_file)
        assert result["name"] == "filesystem-mcp"

    def test_missing_file_raises(self, tmp_path):
        with pytest.raises(ManifestNotFoundError):
            parse_manifest(tmp_path / "nonexistent.json")

    def test_invalid_json_raises(self):
        with pytest.raises(ManifestNotFoundError):
            parse_manifest("not valid json {{{")


class TestHashManifest:
    def test_hash_format(self):
        digest = hash_manifest('{"test": 1}')
        assert digest.startswith("sha256:")
        assert len(digest) == 71  # "sha256:" + 64 hex chars

    def test_hash_deterministic(self):
        content = json.dumps(SAMPLE_MANIFEST)
        assert hash_manifest(content) == hash_manifest(content)

    def test_different_content_different_hash(self):
        h1 = hash_manifest('{"a": 1}')
        h2 = hash_manifest('{"a": 2}')
        assert h1 != h2


class TestExtractTools:
    def test_extracts_tools(self):
        tools = extract_tools(SAMPLE_MANIFEST)
        assert len(tools) == 2
        assert tools[0]["name"] == "read_file"

    def test_empty_tools(self):
        assert extract_tools({"name": "test"}) == []
