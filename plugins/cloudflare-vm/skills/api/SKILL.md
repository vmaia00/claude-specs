---
name: api
description: "Cloudflare API Integration: Guide for working with Cloudflare's REST API - authentication, SDK usage, common patterns, and troubleshooting."
disable-model-invocation: true
---

> Vendored from themusebook/skills (derived from cloudflare/skills, Apache-2.0). This snapshot may be outdated: confirm limits, pricing, API signatures and config options against https://developers.cloudflare.com/ before you cite them. When this file and the docs disagree, trust the docs.

**When invoked:** read every file in this skill's directory before answering, so you have the full reference: `api.md`, `configuration.md`, `gotchas.md`, `patterns.md`. Then answer the user's question (or, if none was given, summarise the product: what it is, config, API, patterns and gotchas). Related products are sibling skills, linked as `../<product>/`.

# Cloudflare API Integration

Guide for working with Cloudflare's REST API - authentication, SDK usage, common patterns, and troubleshooting.

## Quick Decision Tree

```
How are you calling the Cloudflare API?
├─ From Workers runtime → Use bindings, not REST API (see ../bindings/)
├─ Server-side (Node/Python/Go) → Official SDK (see api.md)
├─ CLI/scripts → Wrangler or curl (see configuration.md)
├─ Infrastructure-as-code → See ../pulumi/ or ../terraform/
└─ One-off requests → curl examples (see api.md)
```

## SDK Selection

| Language | Package | Best For | Default Retries |
|----------|---------|----------|-----------------|
| TypeScript | `cloudflare` | Node.js, Bun, Next.js, Workers | 2 |
| Python | `cloudflare` | FastAPI, Django, scripts | 2 |
| Go | `cloudflare-go/v4` | CLI tools, microservices | 10 |

All SDKs are Stainless-generated from OpenAPI spec (consistent APIs).

## Authentication Methods

| Method | Security | Use Case | Scope |
|--------|----------|----------|-------|
| **API Token** ✓ | Scoped, rotatable | Production | Per-zone or account |
| API Key + Email | Full account access | Legacy only | Everything |
| User Service Key | Limited | Origin CA certs only | Origin CA |

**Always use API tokens** for new projects.

## Rate Limits

| Limit | Value |
|-------|-------|
| Per user/token | 1200 requests / 5 minutes |
| Per IP | 200 requests / second |
| GraphQL | 320 / 5 minutes (cost-based) |

## Reading Order

| Task | Files to Read |
|------|---------------|
| Initialize SDK client | api.md |
| Configure auth/timeout/retry | configuration.md |
| Find usage patterns | patterns.md |
| Debug errors/rate limits | gotchas.md |
| Product-specific APIs | ../workers/, ../r2/, ../kv/, etc. |

## In This Reference

- **[api.md](api.md)** - SDK client initialization, pagination, error handling, examples
- **[configuration.md](configuration.md)** - Environment variables, SDK config, Wrangler setup
- **[patterns.md](patterns.md)** - Real-world patterns, batch operations, workflows
- **[gotchas.md](gotchas.md)** - Rate limits, SDK-specific issues, troubleshooting

## See Also

- [Cloudflare API Docs](https://developers.cloudflare.com/api/)
- [Bindings Reference](../bindings/) - Workers runtime bindings (preferred over REST API)
- [Wrangler Reference](../wrangler/) - CLI tool for Cloudflare development
- [GraphQL Analytics API Reference](../graphql-api/) - Analytics data via GraphQL (separate endpoint from REST API)
