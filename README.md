# mcp-notary

> Pre-install trust verification for MCP servers — provenance, integrity and typosquatting detection.

[![CI](https://github.com/sopitacasera/mcp-notary/actions/workflows/ci.yml/badge.svg)](https://github.com/sopitacasera/mcp-notary/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/mcp-notary)](https://pypi.org/project/mcp-notary/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)

---

## The problem

MCP servers have access to your files, shell and APIs. Almost none of them sign their releases.
You install a server, you have no way to verify it's the real thing — until something goes wrong.

**mcp-notary** verifies a server **before** you install it:

- ✅ **Provenance check** — did this release come from the expected GitHub repo and tag?
- ✅ **Typosquatting detection** — is this name suspiciously similar to a known server?
- ✅ **GitHub Action** — integrate in your CI in 3 lines

Pairs with [mcp-guardian](https://github.com/sopitacasera/mcp-guardian) for post-install scanning.

---

## Quickstart (< 2 minutes)

```bash
pip install mcp-notary

# Check a server before installing
mcp-notary check filesystem-mcp@1.2.3
```

```
  Server       filesystem-mcp
  Version      1.2.3
  ─────────────────────────────
  Provenance   UNKNOWN — no signed manifest found
  Typosquatting  No matches found
```

---

## Usage

```bash
# Verify provenance and check for typosquatting
mcp-notary check <server>[@version]

# Output as JSON (machine-readable)
mcp-notary check filesystem-mcp --json

# Output as SARIF (GitHub Security tab)
mcp-notary check filesystem-mcp --sarif

# Offline mode (typosquatting only, no network)
mcp-notary check filesystem-mcp --offline
```

---

## GitHub Action

```yaml
- name: Verify MCP server
  uses: sopitacasera/mcp-notary@v1
  with:
    server: filesystem-mcp@1.2.3
```

---

## Recommended pipeline with mcp-guardian

```bash
# 1. Verify before installing
mcp-notary check filesystem-mcp@1.2.3

# 2. Install
npx @modelcontextprotocol/filesystem-mcp

# 3. Scan after installing
mcp-guardian scan filesystem-mcp
```

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). To add a server to the typosquatting detection list, open a PR editing `mcp_notary/data/mcp-known-servers.json`.

## Security

See [SECURITY.md](SECURITY.md) for responsible disclosure policy.

## License

MIT © [Johanna Huaraca](https://sopitacasera.github.io)
