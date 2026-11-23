---
name: api-shield
description: "Cloudflare API Shield Reference: Expert guidance for API Shield - comprehensive API security suite for discovery, protection, and monitoring."
disable-model-invocation: true
---

> Vendored from themusebook/skills (derived from cloudflare/skills, Apache-2.0). This snapshot may be outdated: confirm limits, pricing, API signatures and config options against https://developers.cloudflare.com/ before you cite them. When this file and the docs disagree, trust the docs.

**When invoked:** read every file in this skill's directory before answering, so you have the full reference: `api.md`, `configuration.md`, `gotchas.md`, `patterns.md`. Then answer the user's question (or, if none was given, summarise the product: what it is, config, API, patterns and gotchas). Related products are sibling skills, linked as `../<product>/`.

# Cloudflare API Shield Reference

Expert guidance for API Shield - comprehensive API security suite for discovery, protection, and monitoring.

## Reading Order

| Task | Files to Read |
|------|---------------|
| Initial setup | README → configuration.md |
| Implement JWT validation | configuration.md → api.md |
| Add schema validation | configuration.md → patterns.md |
| Detect API attacks | patterns.md → api.md |
| Debug issues | gotchas.md |

## Feature Selection

What protection do you need?

```
├─ Validate request/response structure → Schema Validation 2.0 (configuration.md)
├─ Verify auth tokens → JWT Validation (configuration.md)
├─ Client certificates → mTLS (configuration.md)
├─ Detect BOLA attacks → BOLA Detection (patterns.md)
├─ Track auth coverage → Auth Posture (patterns.md)
├─ Stop volumetric abuse → Abuse Detection (patterns.md)
└─ Discover shadow APIs → API Discovery (api.md)
```

## In This Reference

- **[configuration.md](configuration.md)** - Setup, session identifiers, rules, token/mTLS configs
- **[api.md](api.md)** - Endpoint management, discovery, validation APIs, GraphQL operations
- **[patterns.md](patterns.md)** - Common patterns, progressive rollout, OWASP mappings, workflows
- **[gotchas.md](gotchas.md)** - Troubleshooting, false positives, performance, best practices

## Quick Start

API Shield: Enterprise-grade API security (Discovery, Schema Validation 2.0, JWT, mTLS, BOLA Detection, Auth Posture). Available as Enterprise add-on with preview access.

## See Also

- [API Shield Docs](https://developers.cloudflare.com/api-shield/)
- [API Reference](https://developers.cloudflare.com/api/resources/api_gateway/)
- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)
