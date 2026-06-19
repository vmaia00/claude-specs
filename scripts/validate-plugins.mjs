#!/usr/bin/env node
// Validate the marketplace + plugin manifests and agent/skill frontmatter.
//
// Why: this repo is a Claude Code plugin marketplace. A malformed marketplace.json,
// plugin.json, or agent/skill frontmatter block silently breaks installation or routing —
// nothing else in CI catches it. Run by .github/workflows/quality.yml and usable locally:
//   node scripts/validate-plugins.mjs
//
// Vendored plugins (category "vendored" or tagged "vendored" in marketplace.json) are checked
// leniently: their frontmatter problems are warnings, not failures, since we don't own that code.
// First-party plugins are strict. Exit 1 on any error; warnings never fail the build.

import { readFileSync, readdirSync, statSync, existsSync } from "node:fs";
import { join, relative, basename } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(fileURLToPath(import.meta.url), "..", "..");
const errors = [];
const warnings = [];
const err = (file, msg) => errors.push(`${relative(ROOT, file)}: ${msg}`);
const warn = (file, msg) => warnings.push(`${relative(ROOT, file)}: ${msg}`);

function walk(dir, onFile) {
  for (const name of readdirSync(dir)) {
    if (name === ".git" || name === "node_modules") continue;
    const p = join(dir, name);
    const st = statSync(p);
    if (st.isDirectory()) walk(p, onFile);
    else onFile(p);
  }
}

function readJSON(file) {
  try {
    return JSON.parse(readFileSync(file, "utf8"));
  } catch (e) {
    err(file, `invalid JSON — ${e.message}`);
    return null;
  }
}

// --- Parse the leading `---` frontmatter block of a markdown file. ---
// Returns { ok, keys } where keys is the set of top-level `key:` names found.
// Deliberately line-based (no YAML dependency): we only assert presence of required keys,
// not full schema. Handles folded scalars like `description: >` (still starts with the key).
function frontmatter(file) {
  const text = readFileSync(file, "utf8").replace(/^﻿/, "");
  if (!text.startsWith("---")) return { ok: false, reason: "no frontmatter block (must start with ---)" };
  const lines = text.split(/\r?\n/);
  if (lines[0].trim() !== "---") return { ok: false, reason: "first line must be exactly ---" };
  let end = -1;
  for (let i = 1; i < lines.length; i++) {
    if (lines[i].trim() === "---") { end = i; break; }
  }
  if (end === -1) return { ok: false, reason: "frontmatter block is never closed with ---" };
  const keys = new Set();
  for (let i = 1; i < end; i++) {
    const m = /^([A-Za-z0-9_-]+):/.exec(lines[i]);
    if (m) keys.add(m[1]);
  }
  return { ok: true, keys, end };
}

function requireFrontmatter(file, { strict }) {
  const fm = frontmatter(file);
  const report = strict ? err : warn;
  if (!fm.ok) { report(file, fm.reason); return; }
  for (const key of ["name", "description"]) {
    if (!fm.keys.has(key)) report(file, `frontmatter missing required key: ${key}`);
  }
}

// --- 1. Marketplace manifest ---------------------------------------------------------------
const vendored = new Set();
const marketplacePath = join(ROOT, ".claude-plugin", "marketplace.json");
if (!existsSync(marketplacePath)) {
  err(marketplacePath, "marketplace manifest not found");
} else {
  const mk = readJSON(marketplacePath);
  if (mk) {
    for (const key of ["name", "owner", "plugins"]) {
      if (!(key in mk)) err(marketplacePath, `missing required key: ${key}`);
    }
    if (!Array.isArray(mk.plugins)) {
      err(marketplacePath, "`plugins` must be an array");
    } else {
      const names = new Set();
      for (const p of mk.plugins) {
        for (const key of ["name", "source", "description"]) {
          if (!p?.[key]) err(marketplacePath, `plugin entry missing "${key}": ${JSON.stringify(p?.name ?? p)}`);
        }
        if (p?.name) {
          if (names.has(p.name)) err(marketplacePath, `duplicate plugin name: ${p.name}`);
          names.add(p.name);
        }
        const isVendored = p?.category === "vendored" || (Array.isArray(p?.tags) && p.tags.includes("vendored"));
        if (isVendored && p?.name) vendored.add(p.name);
        if (p?.source) {
          const dir = join(ROOT, p.source);
          if (!existsSync(dir)) err(marketplacePath, `plugin "${p.name}" source does not exist: ${p.source}`);
        }
      }
    }
  }
}

// --- 2. plugin.json for every plugin -------------------------------------------------------
const pluginsDir = join(ROOT, "plugins");
if (existsSync(pluginsDir)) {
  for (const name of readdirSync(pluginsDir)) {
    const base = join(pluginsDir, name);
    if (!statSync(base).isDirectory()) continue;
    const manifest = join(base, ".claude-plugin", "plugin.json");
    if (!existsSync(manifest)) { err(manifest, `plugin "${name}" has no .claude-plugin/plugin.json`); continue; }
    const pj = readJSON(manifest);
    if (pj) {
      for (const key of ["name", "description", "version"]) {
        if (!pj[key]) err(manifest, `missing required key: ${key}`);
      }
    }

    // --- 3. agent + skill frontmatter (strict unless vendored) ---
    const strict = !vendored.has(name);
    const agentsDir = join(base, "agents");
    if (existsSync(agentsDir)) {
      walk(agentsDir, (f) => { if (f.endsWith(".md")) requireFrontmatter(f, { strict }); });
    }
    const skillsDir = join(base, "skills");
    if (existsSync(skillsDir)) {
      walk(skillsDir, (f) => { if (basename(f) === "SKILL.md") requireFrontmatter(f, { strict }); });
    }
  }
}

// --- Report --------------------------------------------------------------------------------
for (const w of warnings) console.log(`::warning::${w}`);
if (errors.length) {
  for (const e of errors) console.log(`::error::${e}`);
  console.error(`\n✗ ${errors.length} error(s), ${warnings.length} warning(s).`);
  process.exit(1);
}
console.log(`✓ manifests + frontmatter valid (${warnings.length} warning(s)).`);
