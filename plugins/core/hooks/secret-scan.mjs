#!/usr/bin/env node
// >>> SECRET_SCAN - PreToolUse guard for Write/Edit/MultiEdit <<<
//
// Blocks writing real-looking credentials into committed files. Reinforces the
// "{{SECRET}} placeholder" discipline: secrets belong in a gitignored .env, never in source.
//
// Protocol: receives the tool call as JSON on stdin. Exit 0 = allow; exit 2 = block
// (stderr is shown to Claude so it can correct course). Any parse/internal error fails OPEN
// (exit 0) — a scanner bug must never wedge every file write.

let raw = "";
process.stdin.setEncoding("utf8");
process.stdin.on("data", (c) => (raw += c));
process.stdin.on("end", () => {
  try {
    run(JSON.parse(raw || "{}"));
  } catch {
    process.exit(0); // fail open
  }
});

function run(payload) {
  const input = payload.tool_input || {};
  // Collect every string this tool would write to disk.
  const chunks = [];
  if (typeof input.content === "string") chunks.push(input.content); // Write
  if (typeof input.new_string === "string") chunks.push(input.new_string); // Edit
  if (Array.isArray(input.edits)) {
    for (const e of input.edits) {
      if (e && typeof e.new_string === "string") chunks.push(e.new_string); // MultiEdit
    }
  }
  const text = chunks.join("\n");
  if (!text.trim()) process.exit(0);

  // Patterns that strongly indicate a REAL secret value (not just the word "token").
  const RULES = [
    [/-----BEGIN (?:RSA |EC |OPENSSH |DSA |PGP )?PRIVATE KEY-----/, "private key block"],
    [/\b1000\.[a-f0-9]{20,}\.[a-f0-9]{20,}\b/i, "Zoho OAuth token (1000.<hex>.<hex>)"],
    [/\bsk-[A-Za-z0-9]{20,}\b/, "OpenAI-style secret key (sk-...)"],
    [/\bAKIA[0-9A-Z]{16}\b/, "AWS access key id (AKIA...)"],
    [/\bAIza[0-9A-Za-z\-_]{35}\b/, "Google API key (AIza...)"],
    [/\bxox[baprs]-[0-9A-Za-z-]{10,}\b/, "Slack token (xox.-...)"],
    [/\bghp_[A-Za-z0-9]{36}\b/, "GitHub personal access token (ghp_...)"],
    [/\bBearer\s+[A-Za-z0-9\-._~+/]{24,}=*/, "hard-coded Bearer token"],
    [
      // key = "long literal" assignments for secret-ish names
      /\b(?:api[_-]?key|secret|client[_-]?secret|token|access[_-]?token|refresh[_-]?token|password|passwd|pwd)\b\s*[:=]\s*["'][^"'\s]{8,}["']/i,
      "hard-coded credential assignment",
    ],
  ];

  // Allow obvious placeholders / references so we don't cry wolf.
  const PLACEHOLDER =
    /\{\{[^}]+\}\}|<[A-Z0-9_]+>|process\.env|os\.environ|\$\{[^}]+\}|\benv\.|REDACTED|EXAMPLE|xxxx+|your[_-]?(?:key|secret|token)/i;

  const hits = [];
  for (const [re, label] of RULES) {
    const m = text.match(re);
    if (!m) continue;
    const sample = m[0];
    if (PLACEHOLDER.test(sample)) continue; // looks like a placeholder, allow
    hits.push(`${label}: ${redact(sample)}`);
  }

  if (hits.length === 0) process.exit(0);

  const path = input.file_path || "(unknown file)";
  process.stderr.write(
    ">>> SECRET_SCAN - blocked write: possible real credential(s) detected <<<\n" +
      `File: ${path}\n` +
      hits.map((h) => `  - ${h}`).join("\n") +
      "\n\nPut the real value in a gitignored .env and reference a {{SECRET}} placeholder " +
      "in committed files. If this is a false positive, rename the value to a placeholder.\n"
  );
  process.exit(2); // block
}

function redact(s) {
  const t = s.length > 18 ? s.slice(0, 10) + "…" + s.slice(-4) : s;
  return t.replace(/\s+/g, " ");
}
