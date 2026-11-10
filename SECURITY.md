# Security Policy

## Supported Versions

| Version | Supported |
| ------- | --------- |
| 0.1.x   | ✅        |

## Reporting a Vulnerability

**Do not open a public GitHub issue for security vulnerabilities.**

Please report security issues via [GitHub Security Advisories](https://github.com/sopitacasera/mcp-notary/security/advisories/new).

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (optional)

**SLA:**
- Acknowledgment: within 72 hours
- Fix for critical issues: within 14 days
- Fix for non-critical issues: within 30 days

## Scope

In-scope:
- Vulnerabilities in `mcp-notary` itself that could allow bypass of security checks
- False negatives in typosquatting detection for known malicious patterns
- Supply chain issues in `mcp-notary`'s own dependencies

Out of scope:
- False positives in typosquatting detection
- Issues in MCP servers that `mcp-notary` checks (report those to the respective projects)
- Theoretical attacks without proof of concept
