---
origin: superpowers-ruby
name: rails-guides
description: Maps Rails topics to the official versioned guides at guides.rubyonrails.org for WebFetch. Use when asked about any Rails-specific topic including ActiveRecord, routing, controllers, views, mailers, jobs, Action Cable, Action Text, Active Storage, migrations, validations, callbacks, associations, caching, security, or internals — resolve the topic to its guide URL, substitute the project's exact Rails version, and fetch the live page.
---

# Rails Guides

Topic → URL index for the official Rails guides. **Do not answer Rails questions from memory** —
resolve the topic below, build the versioned URL, and fetch the live page with WebFetch.

> **Note:** this skill previously vendored ~48 offline copies of the guides under `references/`.
> That directory was removed deliberately (stale snapshots drift from the project's Rails version).
> Re-vendor version-matched guides only if offline grounding proves necessary.

## How to use

1. Find the project's **exact Rails version** in `Gemfile.lock` (the `rails (X.Y.Z)` line).
2. Build the URL: `https://guides.rubyonrails.org/v<VERSION>/<page>.html` — e.g. Rails 7.1.3 →
   `https://guides.rubyonrails.org/v7.1/active_record_querying.html` (major.minor is sufficient;
   full `vX.Y.Z` also resolves).
3. WebFetch that page and ground the answer in it, not in memory. If no version is known, fall
   back to the unversioned URL (latest stable): `https://guides.rubyonrails.org/<page>.html`.

## Topic map (`<page>` values)

### Getting started & configuration

| Topic | Page |
|---|---|
| Rails basics, MVC, first app | `getting_started` |
| `rails` command, generators, rake tasks | `command_line` |
| Environments, initialisers, credentials, database.yml | `configuring` |
| Zeitwerk autoloading, module naming, reload behaviour | `autoloading_and_reloading_constants` |
| Boot sequence, railties, engines | `initialization` |

### Active Record & Active Model

| Topic | Page |
|---|---|
| Models, CRUD, conventions | `active_record_basics` |
| Finders, scopes, joins, includes, explain | `active_record_querying` |
| Built-in and custom validators, errors | `active_record_validations` |
| Lifecycle hooks, after_commit, skip_callback | `active_record_callbacks` |
| belongs_to, has_many, polymorphic, eager loading | `association_basics` |
| Schema changes, reversible migrations | `active_record_migrations` |
| Encrypting attributes at rest | `active_record_encryption` |
| Composite primary keys | `active_record_composite_primary_keys` |
| Multi-DB setup, sharding, replicas | `active_record_multiple_databases` |
| PostgreSQL-specific features (jsonb, arrays) | `active_record_postgresql` |
| ActiveModel outside ActiveRecord, form objects | `active_model_basics` |

### Controllers & routing

| Topic | Page |
|---|---|
| Controllers, params, filters, sessions, cookies | `action_controller_overview` |
| Streaming, live, metal, HTTP auth | `action_controller_advanced_topics` |
| Resources, namespaces, constraints, URL helpers | `routing` |

### Views & frontend / Hotwire

| Topic | Page |
|---|---|
| Templates, partials, layouts, formats | `action_view_overview` |
| form_with, link_to, tag, asset helpers | `action_view_helpers` |
| Field helpers, nested forms, uploads | `form_helpers` |
| render, redirect_to, respond_to, layout inheritance | `layouts_and_rendering` |
| Import maps, Turbo, Stimulus overview | `working_with_javascript_in_rails` |
| Rich text with Trix, attachments | `action_text_overview` |

### Jobs, mailers, storage & real-time

| Topic | Page |
|---|---|
| Job classes, queues, retry, test helpers | `active_job_basics` |
| Mailers, templates, deliveries, previews | `action_mailer_basics` |
| Incoming email routing | `action_mailbox_basics` |
| File uploads, variants, direct uploads, S3/GCS | `active_storage_overview` |
| WebSockets, channels, broadcasting | `action_cable_overview` |

### Testing, security & performance

| Topic | Page |
|---|---|
| Minitest, fixtures, test types, assertions | `testing` |
| SQL injection, XSS, CSRF, mass assignment | `security` |
| Fragment/action/HTTP caching, cache stores | `caching_with_rails` |
| Sprockets, Propshaft, precompile, digests | `asset_pipeline` |
| Puma, connection pooling, GC tuning | `tuning_performance_for_deployment` |

### Internationalisation, API & Rack

| Topic | Page |
|---|---|
| Translation files, locale, pluralisation | `i18n` |
| API-only Rails, slim middleware stack | `api_app` |
| Middleware stack, Rack integration | `rails_on_rack` |

### Extending Rails & advanced

| Topic | Page |
|---|---|
| Mountable engines, isolated namespaces | `engines` |
| Custom generators, templates | `generators` |
| Gem-based plugins, core extensions | `plugins` |
| String/Array/Hash/Date core extensions | `active_support_core_extensions` |
| Notifications, log subscribers | `active_support_instrumentation` |
| debug gem, logger, web-console | `debugging_rails_applications` |
| Error::Reporter, Sentry integration | `error_reporting` |
| Thread safety, executor, reloader | `threading_and_code_execution` |
| Version upgrade paths, deprecations | `upgrading_ruby_on_rails` |
