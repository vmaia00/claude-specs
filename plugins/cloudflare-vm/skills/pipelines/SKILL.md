---
name: pipelines
description: "Cloudflare Pipelines: Streaming ingest: receive events over HTTP/Workers/Logpush, transform with SQL, write to R2 as Iceberg tables or Parquet/JSON files."
disable-model-invocation: true
---

> Vendored from themusebook/skills (derived from cloudflare/skills, Apache-2.0). This snapshot may be outdated: confirm limits, pricing, API signatures and config options against https://developers.cloudflare.com/ before you cite them. When this file and the docs disagree, trust the docs.

**When invoked:** read every file in this skill's directory before answering, so you have the full reference: `api.md`, `configuration.md`, `gotchas.md`, `patterns.md`. Then answer the user's question (or, if none was given, summarise the product: what it is, config, API, patterns and gotchas). Related products are sibling skills, linked as `../<product>/`.

# Cloudflare Pipelines

Streaming ingest: receive events over HTTP/Workers/Logpush, transform with SQL, write to R2 as Iceberg tables or Parquet/JSON files.

## Documentation

This reference is a fast-start with verified code and gotchas. For limits, settings, full SQL syntax, and pricing, **retrieve the live docs** — use the `cloudflare-docs` MCP/search tool if available, otherwise `webfetch` the URL. Docs are source of truth over this file.

| Topic | URL |
|-------|-----|
| Overview / getting started | `https://developers.cloudflare.com/pipelines/getting-started/` |
| Streams (write, manage, Logpush) | `https://developers.cloudflare.com/pipelines/streams/` |
| Sinks | `https://developers.cloudflare.com/pipelines/sinks/` |
| Pipelines & SQL transforms | `https://developers.cloudflare.com/pipelines/pipelines/` |
| SQL reference (statements, types) | `https://developers.cloudflare.com/pipelines/sql-reference/` |
| Wrangler commands | `https://developers.cloudflare.com/pipelines/reference/wrangler-commands/` |
| Terraform | `https://developers.cloudflare.com/pipelines/reference/terraform/` |
| Limits | `https://developers.cloudflare.com/pipelines/platform/limits/` |
| Pricing | `https://developers.cloudflare.com/pipelines/platform/pricing/` |
| Metrics (GraphQL) | `https://developers.cloudflare.com/pipelines/observability/metrics/` |

## Three Components

```
Sources → Stream → Pipeline (SQL) → Sink → R2
          ↑          ↓                 ↓
   HTTP / Workers / Transform     Iceberg (Data Catalog)
   Logpush          (row-level)   or Parquet/JSON files
```

| Component | Purpose |
|-----------|---------|
| **Stream** | Receives events (HTTP endpoint, Worker binding, or Logpush). Structured (schema-validated) or unstructured. |
| **Pipeline** | SQL connecting a stream to a sink. Row-level transforms only — no GROUP BY/aggregation. |
| **Sink** | Writes to R2 — Iceberg via Data Catalog, or raw Parquet/JSON. |

**Status:** Open beta (Workers Paid for production). Pricing announced; verify billing status in docs.

## Quick Start

```bash
# Interactive — creates stream + sink + pipeline, optionally bucket + catalog
npx wrangler pipelines setup
```

Minimal Worker producer:
```typescript
interface Env { MY_STREAM: Pipeline; }

export default {
  async fetch(req: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    ctx.waitUntil(env.MY_STREAM.send([{ event_id: crypto.randomUUID(), amount: 29.99 }]));
    return new Response("OK");
  }
} satisfies ExportedHandler<Env>;
```

## Which Sink Type?

```
Need SQL queries / ACID / time-travel on the data?
  → R2 Data Catalog (Iceberg)   ✅ R2 SQL, schema evolution   ❌ more setup

Just archival / external tools (Spark, Athena)?
  → R2 raw files (Parquet/JSON) ✅ simple, partitioned files  ❌ no built-in SQL
```

## Critical Behaviors (read before building)

These are non-obvious and prevent most failures — see [gotchas.md](gotchas.md) for detail.

- **Everything is immutable after creation** — stream schema, pipeline SQL, sink config. To change, delete and recreate.
- **Sinks create their own table** — they cannot target an existing Iceberg table.
- **`__ingest_ts` is added automatically** (TIMESTAMP, partitioned by day). Don't define it in your schema.
- **Data isn't queryable immediately** — first flush takes **3–7 minutes** (warm-up + table creation) even with a short roll interval.
- **Schema validation is deferred** — invalid events are accepted then silently dropped. Monitor via GraphQL error metrics.
- **Binding field renamed `pipeline` → `stream`** (June 2026); old field still accepted.

## Reading Order

1. [configuration.md](configuration.md) — schema, streams, sinks, pipelines (CLI + REST + Terraform), bindings
2. [api.md](api.md) — `send()`, HTTP ingest, REST API, pipeline SQL, lifecycle states
3. [patterns.md](patterns.md) — fire-and-forget, validation, Logpush, observability, end-to-end
4. [gotchas.md](gotchas.md) — silent drops, immutability, REST≠CLI field names

## See Also

- [r2-data-catalog](../r2-data-catalog/) — Iceberg sink destination
- [r2-sql](../r2-sql/) — query the ingested data
- [r2](../r2/) · [queues](../queues/) · [workers](../workers/)
