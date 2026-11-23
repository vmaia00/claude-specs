---
name: cloudflare-vm
description: "Cloudflare platform index: decision trees to pick the right product (Workers, Pages, KV, D1, R2, Durable Objects, Queues, Workers AI, Vectorize, Tunnel, WAF, Terraform, Pulumi and more) and pointers to per-product references. Use for any Cloudflare development task. Prefers live Cloudflare docs over pre-trained knowledge."
---

# Cloudflare Platform Skill

Product references live in sibling skill directories (`../r2/`, `../d1/`, ...; paths are relative to this skill's base directory). Each has `SKILL.md` (overview) plus `api.md`, `configuration.md`, `patterns.md` and `gotchas.md`. The user can also load one product directly with `/cloudflare-vm:<product>`, e.g. `/cloudflare-vm:r2`.

Consolidated skill for building on the Cloudflare platform. Use decision trees below to find the right product, then load detailed references.

Your knowledge of Cloudflare APIs, types, limits, and pricing may be outdated. **Prefer retrieval over pre-training** — the references in this skill are starting points, not source of truth.

## Retrieval Sources

Fetch the **latest** information before citing specific numbers, API signatures, or configuration options. Do not rely on baked-in knowledge or these reference files alone.

| Source | How to retrieve | Use for |
|--------|----------------|---------|
| Cloudflare docs | `cloudflare-docs` search tool or `https://developers.cloudflare.com/` | Limits, pricing, API reference, compatibility dates/flags |
| Workers types | `npm pack @cloudflare/workers-types` or check `node_modules` | Type signatures, binding shapes, handler types |
| Wrangler config schema | `node_modules/wrangler/config-schema.json` | Config fields, binding shapes, allowed values |
| Product changelogs | `https://developers.cloudflare.com/changelog/` | Recent changes to limits, features, deprecations |

When a reference file and the docs disagree, **trust the docs**. This is especially important for: numeric limits, pricing tiers, type signatures, and configuration options.

## Quick Decision Trees

### "I need feature flags"

```
Need feature flags?
└─ Feature toggles, targeting rules, percentage rollouts → flagship/
   ├─ Evaluate in Workers → Flagship binding (env.FLAGS)
   ├─ Evaluate in Node.js / browser → OpenFeature SDK (@cloudflare/flagship)
   └─ Manage flags via API → Flagship REST API
```

### "I need to run code"

```
Need to run code?
├─ Serverless functions at the edge → workers/
├─ Full-stack web app with Git deploys → pages/
├─ Stateful coordination/real-time → durable-objects/
├─ Long-running multi-step jobs → workflows/
├─ Run containers → containers/
├─ Multi-tenant (customers deploy code) → workers-for-platforms/
├─ Scheduled tasks (cron) → cron-triggers/
├─ Lightweight edge logic (modify HTTP) → snippets/
├─ Process Worker execution events (logs/observability) → tail-workers/
└─ Optimize latency to backend infrastructure → smart-placement/
```

### "I need to store data"

```
Need storage?
├─ Key-value (config, sessions, cache) → kv/
├─ Relational SQL → d1/ (SQLite) or hyperdrive/ (existing Postgres/MySQL)
├─ Object/file storage (S3-compatible) → r2/
├─ Versioned file trees (repos, build outputs, checkpoints) → artifacts/
├─ Message queue (async processing) → queues/
├─ Vector embeddings (AI/semantic search) → vectorize/
├─ Strongly-consistent per-entity state → durable-objects/ (DO storage)
├─ Secrets management → secrets-store/
├─ Streaming ETL to R2 → pipelines/
├─ Managed Apache Iceberg catalog on R2 → r2-data-catalog/
├─ Serverless SQL analytics over Iceberg tables → r2-sql/
└─ Persistent cache (long-term retention) → cache-reserve/
```

### "I need AI/ML"

```
Need AI?
├─ Run inference (LLMs, embeddings, images) → workers-ai/
├─ Vector database for RAG/search → vectorize/
├─ Build stateful AI agents → agents-sdk/
├─ Gateway for any AI provider (caching, routing) → ai-gateway/
└─ AI-powered search widget → ai-search/
```

### "I need networking/connectivity"

```
Need networking?
├─ Expose local service to internet → tunnel/
├─ TCP/UDP proxy (non-HTTP) → spectrum/
├─ WebRTC TURN server → turn/
├─ Private network connectivity → network-interconnect/
├─ Optimize routing → argo-smart-routing/
├─ Optimize latency to backend (not user) → smart-placement/
└─ Real-time video/audio → realtimekit/ or realtime-sfu/
```

### "I need security"

```
Need security?
├─ Web Application Firewall → waf/
├─ DDoS protection → ddos/
├─ Bot detection/management → bot-management/
├─ API protection → api-shield/
├─ CAPTCHA alternative → turnstile/
└─ Credential leak detection → waf/ (managed ruleset)
```

### "I need media/content"

```
Need media?
├─ Image optimization/transformation → images/
├─ Video streaming/encoding → stream/
├─ Browser automation/screenshots → browser-rendering/
└─ Third-party script management → zaraz/
```

### "I need analytics/metrics data"

```
Need analytics?
├─ Query across all Cloudflare products (HTTP, Workers, DNS, etc.) → graphql-api/
├─ Custom high-cardinality metrics from Workers → analytics-engine/
├─ Client-side (RUM) performance data → web-analytics/
├─ Workers Logs and real-time debugging → observability/
├─ SQL over Iceberg data lake (logs, events) → r2-sql/ (+ pipelines/, r2-data-catalog/)
└─ Raw logs (Logpush to external tools) → Cloudflare docs
```

### "I need infrastructure-as-code"

```
Need IaC? → pulumi/ (Pulumi), terraform/ (Terraform), or api/ (REST API)
```

## Product Index

### Feature Flags
| Product | Reference |
|---------|-----------|
| Flagship | `../flagship/` |

### Compute & Runtime
| Product | Reference |
|---------|-----------|
| Workers | `../workers/` |
| Pages | `../pages/` |
| Pages Functions | `../pages-functions/` |
| Durable Objects | `../durable-objects/` |
| Workflows | `../workflows/` |
| Containers | `../containers/` |
| Workers for Platforms | `../workers-for-platforms/` |
| Cron Triggers | `../cron-triggers/` |
| Tail Workers | `../tail-workers/` |
| Snippets | `../snippets/` |
| Smart Placement | `../smart-placement/` |

### Storage & Data
| Product | Reference |
|---------|-----------|
| KV | `../kv/` |
| D1 | `../d1/` |
| R2 | `../r2/` |
| Artifacts | `../artifacts/` |
| Queues | `../queues/` |
| Hyperdrive | `../hyperdrive/` |
| DO Storage | `../do-storage/` |
| Secrets Store | `../secrets-store/` |
| Pipelines | `../pipelines/` |
| R2 Data Catalog | `../r2-data-catalog/` |
| R2 SQL | `../r2-sql/` |

### AI & Machine Learning
| Product | Reference |
|---------|-----------|
| Workers AI | `../workers-ai/` |
| Vectorize | `../vectorize/` |
| Agents SDK | `../agents-sdk/` |
| AI Gateway | `../ai-gateway/` |
| AI Search | `../ai-search/` |

### Networking & Connectivity
| Product | Reference |
|---------|-----------|
| Tunnel | `../tunnel/` |
| Spectrum | `../spectrum/` |
| TURN | `../turn/` |
| Network Interconnect | `../network-interconnect/` |
| Argo Smart Routing | `../argo-smart-routing/` |
| Workers VPC | `../workers-vpc/` |

### Security
| Product | Reference |
|---------|-----------|
| WAF | `../waf/` |
| DDoS Protection | `../ddos/` |
| Bot Management | `../bot-management/` |
| API Shield | `../api-shield/` |
| Turnstile | `../turnstile/` |

### Media & Content
| Product | Reference |
|---------|-----------|
| Images | `../images/` |
| Stream | `../stream/` |
| Browser Rendering | `../browser-rendering/` |
| Zaraz | `../zaraz/` |

### Real-Time Communication
| Product | Reference |
|---------|-----------|
| RealtimeKit | `../realtimekit/` |
| Realtime SFU | `../realtime-sfu/` |

### Developer Tools
| Product | Reference |
|---------|-----------|
| Wrangler | `../wrangler/` |
| Miniflare | `../miniflare/` |
| C3 | `../c3/` |
| Observability | `../observability/` |
| GraphQL Analytics API | `../graphql-api/` |
| Analytics Engine | `../analytics-engine/` |
| Web Analytics | `../web-analytics/` |
| Sandbox | `../sandbox/` |
| Workerd | `../workerd/` |
| Workers Playground | `../workers-playground/` |

### Infrastructure as Code
| Product | Reference |
|---------|-----------|
| Pulumi | `../pulumi/` |
| Terraform | `../terraform/` |
| API | `../api/` |

### Other Services
| Product | Reference |
|---------|-----------|
| Email Routing | `../email-routing/` |
| Email Workers | `../email-workers/` |
| Static Assets | `../static-assets/` |
| Bindings | `../bindings/` |
| Cache Reserve | `../cache-reserve/` |
