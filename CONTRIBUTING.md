# Contributing to mcp-notary

## Setup

```bash
git clone https://github.com/sopitacasera/mcp-notary
cd mcp-notary
pip install -e ".[dev]"
pytest
```

## Adding a server to the known-servers list

Edit `mcp_notary/data/mcp-known-servers.json` and open a PR. Include:
- The server name exactly as it appears on npm/PyPI/GitHub
- A link to the official source

## Running tests

```bash
pytest                    # all tests
pytest tests/unit/        # unit tests only
pytest -v                 # verbose
```

## Code style

This project uses `ruff` for linting:

```bash
pip install ruff
ruff check mcp_notary/ tests/
```
