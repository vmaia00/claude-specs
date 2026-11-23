---
name: ddos
description: "Cloudflare DDoS Protection: Autonomous, always-on protection against DDoS attacks across L3/4 and L7."
disable-model-invocation: true
---

> Vendored from themusebook/skills (derived from cloudflare/skills, Apache-2.0). This snapshot may be outdated: confirm limits, pricing, API signatures and config options against https://developers.cloudflare.com/ before you cite them. When this file and the docs disagree, trust the docs.

**When invoked:** read every file in this skill's directory before answering, so you have the full reference: `api.md`, `configuration.md`, `gotchas.md`, `patterns.md`. Then answer the user's question (or, if none was given, summarise the product: what it is, config, API, patterns and gotchas). Related products are sibling skills, linked as `../<product>/`.

# Cloudflare DDoS Protection

Autonomous, always-on protection against DDoS attacks across L3/4 and L7.

## Protection Types

- **HTTP DDoS (L7)**: Protects HTTP/HTTPS traffic, phase `ddos_l7`, zone/account level
- **Network DDoS (L3/4)**: UDP/SYN/DNS floods, phase `ddos_l4`, account level only
- **Adaptive DDoS**: Learns 7-day baseline, detects deviations, 4 profile types (Origins, User-Agents, Locations, Protocols)

## Plan Availability

| Feature | Free | Pro | Business | Enterprise | Enterprise Advanced |
|---------|------|-----|----------|------------|---------------------|
| HTTP DDoS (L7) | ✓ | ✓ | ✓ | ✓ | ✓ |
| Network DDoS (L3/4) | ✓ | ✓ | ✓ | ✓ | ✓ |
| Override rules | 1 | 1 | 1 | 1 | 10 |
| Custom expressions | ✗ | ✗ | ✗ | ✗ | ✓ |
| Log action | ✗ | ✗ | ✗ | ✗ | ✓ |
| Adaptive DDoS | ✗ | ✗ | ✗ | ✓ | ✓ |
| Alert filters | Basic | Basic | Basic | Advanced | Advanced |

## Actions & Sensitivity

- **Actions**: `block`, `managed_challenge`, `challenge`, `log` (Enterprise Advanced only)
- **Sensitivity**: `default` (high), `medium`, `low`, `eoff` (essentially off)
- **Override**: By category/tag or individual rule ID
- **Scope**: Zone-level overrides take precedence over account-level

## Reading Order

| File | Purpose | Start Here If... |
|------|---------|------------------|
| [configuration.md](./configuration.md) | Dashboard setup, rule structure, adaptive profiles | You're setting up DDoS protection for the first time |
| [api.md](./api.md) | API endpoints, SDK usage, ruleset ID discovery | You're automating configuration or need programmatic access |
| [patterns.md](./patterns.md) | Protection strategies, defense-in-depth, dynamic response | You need implementation patterns or layered security |
| [gotchas.md](./gotchas.md) | False positives, tuning, error handling | You're troubleshooting or optimizing existing protection |

## See Also
- [waf](../waf/) - Application-layer security rules
- [bot-management](../bot-management/) - Bot detection and mitigation
