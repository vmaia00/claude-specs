#!/usr/bin/env node
// >>> SESSION_DIRECTIVE - SessionStart context injector <<<
//
// Emits the sibling session-directive.md as `additionalContext` so every session starts with the
// standing working directive (orchestrate, prefer existing skills/agents, verify, security baseline).
// Fails OPEN (exit 0, no output) on any error — a hook must never wedge session startup.

import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

try {
  const here = dirname(fileURLToPath(import.meta.url));
  const text = readFileSync(join(here, "session-directive.md"), "utf8").trim();
  if (text) {
    process.stdout.write(
      JSON.stringify({
        hookSpecificOutput: {
          hookEventName: "SessionStart",
          additionalContext: text,
        },
      })
    );
  }
} catch {
  // fail open — never block session startup
}
process.exit(0);
