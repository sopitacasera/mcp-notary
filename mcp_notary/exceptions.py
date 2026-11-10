class McpNotaryError(Exception):
    """Base exception for mcp-notary."""


class ManifestNotFoundError(McpNotaryError):
    """Raised when no signed manifest is found for a server."""


class ProvenanceError(McpNotaryError):
    """Raised when provenance verification fails."""


class NetworkError(McpNotaryError):
    """Raised when a required network request fails."""
