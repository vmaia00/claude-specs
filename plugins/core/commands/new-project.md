---
description: Scaffold a new sub-project from this repo's _template/ folder
argument-hint: <project-name>
allowed-tools: Bash, Read, Edit, Glob
---

Scaffold a new sub-project named **$1** in this repo.

This is the generic, shared version. It assumes the repo keeps reusable, sub-project-style work
under a `projects/` (or similar) folder with a `_template/` scaffold inside it. If this repo has a
repo-local `new-project` command, that one overrides this and wins.

Steps:

1. Normalise the name: lowercase, kebab-case (e.g. "Acme Corp" → `acme-corp`). Call it `NAME`.
   If `$1` is empty, ask the user for a project name and stop.
2. Locate the template folder (commonly `projects/_template`). If none exists, tell the user and
   stop — don't invent a structure.
3. If the destination (`projects/NAME/`) already exists, stop and report it — do not overwrite.
4. Copy the template preserving its shape: `cp -r projects/_template projects/NAME`.
5. Replace every `<PROJECT_NAME>` placeholder in the copied `CLAUDE.md` / `README.md` with `NAME`.
6. Show the created tree and remind the user what to fill in.

Do **not** commit or push — leave the scaffold for the user to review. Portable/shared knowledge
should be referenced, not duplicated into the new project.
