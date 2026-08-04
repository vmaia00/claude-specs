# Setting up a new repo: governance, gates, templates

A playbook for standing up a repository that other people will work in — typically an
external build team, sometimes with ownership transferring later. Ordered so each step
depends only on the ones before it.

**Scope.** This covers governance (who can merge, under what conditions), policy gates,
templates, and project tracking. For the **stack CI** — lint, tests, coverage, CodeQL,
release automation — use the `setup-ci` skill in this repo, which detects the stack and
scaffolds real workflows. Don't hand-write those here; the two are complementary and
`setup-ci` is better at its half.

**Order matters.** Push the scaffolding *before* protecting the branch, or you lock
yourself out of your own empty repo and have to bypass on the first commit.

---

## 0 · Decide these five things first

Answer them explicitly. Each changes what you build, and getting one wrong is expensive
to unwind later.

| Question | If yes | If no |
|---|---|---|
| Will ownership transfer to someone else? | Put the Project under the **destination org**, not your user. Plan a `CODEOWNERS` handover. | Anything works. |
| Does a spec exist that defines phases? | Milestones come from the spec's own phasing. | Don't invent milestones. Ship without them and add when phases are real. |
| Is the stack decided? | Run `setup-ci` now. | Ship the stack-independent gates only, and say in the README that build CI arrives with the stack. **Don't scaffold a pipeline that implies a stack nobody chose.** |
| Is the repo private? | GitHub's own secret scanning needs Advanced Security. Use a workflow instead. | Enable native secret scanning and push protection. |
| Will you be the only reviewer? | You **cannot approve your own PRs** (see Traps). Your own work lands via admin bypass, or you add a second reviewer. | Normal review flow works for everyone. |

---

## 1 · Repo settings

```bash
gh api -X PATCH repos/OWNER/REPO \
  -F delete_branch_on_merge=true \
  -F allow_rebase_merge=false \
  -F allow_auto_merge=false \
  -F has_wiki=false

# Dependency alerts are free on private repos; native secret scanning is not.
gh api -X PUT repos/OWNER/REPO/vulnerability-alerts
gh api -X PUT repos/OWNER/REPO/automated-security-fixes
```

`delete_branch_on_merge` matters more than it looks: without it, a year in, nobody can
tell which of eighty branches are alive.

---

## 2 · Files, before any protection exists

### `.github/CODEOWNERS`

```
*            @you
/.github/    @you
```

Owning `/.github/` separately is the point: without it, a PR can weaken the gates and
satisfy the gate it just weakened.

### `.github/pull_request_template.md`

```markdown
## What changes

<!-- One or two sentences. What becomes true that wasn't. -->

## Why

Closes #

## How to verify

<!-- What the reviewer runs or opens. -->

## Notes

- [ ] Linked to a milestone.
- [ ] The spec covers this. If it doesn't, I say here what I assumed.
- [ ] No internal material, credentials or work-in-progress notes.
```

### `.gitmessage` — the commit template

Activated per-clone with `git config commit.template .gitmessage`. Put that line in
`CONTRIBUTING.md`, because a template nobody activates is a file nobody reads.

```

# ── Subject ────────────────────────────────────────────────────────────────
# One line, 72 characters, no full stop.
# Say what becomes true, not what you did.
#
#   yes: Upload opens at the top of the Documents page
#   no:  Changed the screen to move the button
#
# ── Body ───────────────────────────────────────────────────────────────────
# Blank line, then the why, in prose.
#
# The diff already says what changed. The body is for what the diff cannot show:
# what was true before and stopped being true, why this choice, and what was
# deliberately not done. If the change is obvious, the body can be absent.
#
# Write for whoever reads this in a year with no context. Usually you.
#
# ── Closing ────────────────────────────────────────────────────────────────
#   Closes #12
#
# ── Out ────────────────────────────────────────────────────────────────────
# No assistant/tool attribution, no automatic co-authorship trailers.
# No "WIP", "various fixes", "tweaks": a commit you can't describe in one line
# is usually more than one commit.
```

**The single rule worth enforcing: the subject says what becomes true, not what you did.**
`Downloads count per package, not per part` beats `Fix the counter`, because the first
answers "when did this behaviour change" and the second only helps someone who already
knows.

---

## 3 · The content guard

A stack-independent gate that fails a PR when added lines carry material that doesn't
belong in this repo. Worth having from commit one, especially when the repo will be handed
to a client: it turns "never share internal notes" from discipline into mechanism.

**Two design rules, both learned the hard way.**

**It reads added lines only.** Blaming someone for a line that was already in `main`
teaches them the check is noise, and a check people route around is worse than none.

**Every rule explains itself.** An error that only says "policy violation" gets bypassed;
one that names the file, the match, the line and *why it doesn't belong* gets fixed.

`.github/workflows/content-guard.yml`:

```yaml
name: Content guard

on:
  pull_request:
    branches: [main]

permissions:
  contents: read
  pull-requests: read

jobs:
  guard:                       # this job id must equal the required-check context
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: Collect the lines this PR adds
        run: |
          git diff --unified=0 \
            "origin/${{ github.base_ref }}...${{ github.sha }}" \
            -- . ':(exclude).github/workflows/content-guard.yml' \
            > diff.txt
      - name: Look for material that does not belong here
        run: python3 .github/scripts/content_guard.py diff.txt
```

`.github/scripts/content_guard.py`:

```python
import io, os, re, sys

# (pattern, what it is, why it doesn't belong here)
RULES = [
    (r"_internal\b|scratchpad",
     "path to internal material",
     "points at material that does not live here and the reader does not have"),
    (r"\b(YourConsultancy|OtherVendor)\b",
     "name of a vendor external to the product",
     "the repo is the product's; who built it is discussed elsewhere"),
    (r"\bTODO\b|\bFIXME\b|\bXXX\b|\bHACK\b",
     "unfinished-work marker",
     "open an issue instead: a note in code has no owner"),
    (r"-----BEGIN [A-Z ]*PRIVATE KEY-----|\bAKIA[0-9A-Z]{16}\b|"
     r"\bgh[pousr]_[A-Za-z0-9]{20,}\b|\bxox[baprs]-[A-Za-z0-9-]{10,}\b",
     "credential in the clear",
     "rotate it now: a credential in a diff is a burnt credential"),
]
# Add project-specific rules: retired identifier code families, internal register
# numbering, references to internal rulebooks. Do NOT hardcode people's names —
# the list would live in this public file, which is the problem it tried to solve.


def main(path):
    if not os.path.exists(path):
        print("No diff to check.")
        return 0
    current, found = None, []
    with io.open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            if line.startswith("+++ b/"):
                current = line[6:].strip()
            elif line.startswith("+") and not line.startswith("+++"):
                body = line[1:].rstrip("\n")
                for pat, what, why in RULES:
                    for m in re.finditer(pat, body):
                        found.append((current or "?", what, why, m.group(0),
                                      body.strip()[:120]))
    if not found:
        print("Content guard: nothing to report.")
        return 0
    print("The content guard found %d occurrence(s).\n" % len(found))
    for fp, what, why, hit, ctx in found:
        print("  %s\n    %s: %r\n    why it doesn't belong: %s\n    line: %s\n"
              % (fp, what, hit, why, ctx))
    print("Fix the lines above, or explain in the PR why one is a false positive. "
          "The rule may be wrong; then fix the rule, with the concrete case as "
          "the justification.")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "diff.txt"))
```

---

## 4 · Secret scanning

On a private repo without Advanced Security, run it yourself. **Use the binary, not the
official action:** the action asks the API for the PR's commits to work out the range,
which makes it depend on `pull-requests: read` and on org licensing. The binary needs only
the history the checkout already fetched.

`.github/workflows/secrets.yml`:

```yaml
name: Secret scan

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

permissions:
  contents: read

jobs:
  secrets:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: Install gitleaks
        run: |
          set -euo pipefail
          V=8.28.0
          curl -sSfL -o gitleaks.tar.gz \
            "https://github.com/gitleaks/gitleaks/releases/download/v${V}/gitleaks_${V}_linux_x64.tar.gz"
          tar -xzf gitleaks.tar.gz gitleaks
      - name: Scan what this branch adds
        run: |
          set -euo pipefail
          if [ "${{ github.event_name }}" = "pull_request" ]; then
            ./gitleaks git . --no-banner --redact --exit-code 1 \
              --log-opts="origin/${{ github.base_ref }}..HEAD"
          else
            ./gitleaks git . --no-banner --redact --exit-code 1
          fi
```

Same asymmetry as the content guard: on a PR, scan only the branch's range. A secret
already in `main` is debt to rotate, not grounds to fail whoever opened today's PR.

---

## 5 · Dependabot

Before the stack exists, there is exactly one ecosystem worth watching — the workflows'
own actions. A config watching a manifest that doesn't exist is noise.

`.github/dependabot.yml`:

```yaml
version: 2
updates:
  - package-ecosystem: github-actions
    directory: /
    schedule:
      interval: weekly
    open-pull-requests-limit: 5
```

Add ecosystems when `setup-ci` runs, not before.

---

## 6 · Push, then protect

```bash
git add -A && git commit && git push origin main
```

Then the ruleset. Rulesets are the current mechanism; classic branch protection still
works but rulesets compose better and report bypasses explicitly.

```json
{
  "name": "Protect main",
  "target": "branch",
  "enforcement": "active",
  "conditions": { "ref_name": { "include": ["~DEFAULT_BRANCH"], "exclude": [] } },
  "bypass_actors": [
    { "actor_id": 5, "actor_type": "RepositoryRole", "bypass_mode": "always" }
  ],
  "rules": [
    { "type": "deletion" },
    { "type": "non_fast_forward" },
    { "type": "required_linear_history" },
    { "type": "pull_request", "parameters": {
        "required_approving_review_count": 1,
        "require_code_owner_review": true,
        "dismiss_stale_reviews_on_push": true,
        "require_last_push_approval": true,
        "required_review_thread_resolution": true,
        "allowed_merge_methods": ["squash", "merge"] } },
    { "type": "required_status_checks", "parameters": {
        "strict_required_status_checks_policy": true,
        "required_status_checks": [ {"context": "guard"}, {"context": "secrets"} ] } }
  ]
}
```

```bash
gh api -X POST repos/OWNER/REPO/rulesets --input ruleset.json
```

`actor_id: 5` is the repository **admin** role. That bypass is deliberate: without it the
ruleset locks you out of your own repo too. It is also why **the build team gets `Write`,
never `Admin`** — an admin on their side inherits the same bypass and can push straight to
`main`.

Add a required check **only after that check has run once and you know its reported name**
(see Traps).

---

## 7 · Prove the gates before anyone relies on them

Non-negotiable, and the step most often skipped. A guard whose diff extraction silently
produces nothing passes everything and reads exactly like a working guard.

```bash
git switch -c chore/prove-the-gates
# add a file containing, on purpose: an internal path, a TODO, a fake token
git push -u origin chore/prove-the-gates
gh pr create --fill
gh pr checks <n>          # expect the guard to FAIL and name each violation
gh pr close <n> --delete-branch
```

Read the failure log and confirm it names the file, the match and the reason. Then confirm
a clean PR passes. **Check `main` afterwards**: if you fixed a workflow on that throwaway
branch, deleting it takes the fix with it.

---

## 8 · Project and tracking — only if it earns its place

A board with no cadence behind it is theatre. If you'll actually run it:

```bash
gh project create --owner OWNER --title "PROJECT — Build"
gh project link <n> --owner OWNER --repo OWNER/REPO
gh project item-add <n> --owner OWNER --url <issue-url>
```

Then set every item's `Status`, or the board opens empty in that column and looks broken.

**Milestones come from the spec's phasing, never from imagination.** If there's a phased
plan, mirror its phases and its order. If there isn't, skip milestones — inventing five
plausible phases produces a plan nobody owns.

**Macro issues:** one per substantial piece, each with a *done when* that names an
observable outcome rather than an activity. "Contracts published, and the consumer-driven
test proving it runs in the pipeline" is checkable; "set up contracts" is not.

**If ownership will transfer, create the Project under the destination org.** A
user-owned Project does not travel with the repo (see Traps).

---

## 9 · `CONTRIBUTING.md`

Gather in one place: branch prefixes, how to activate the commit template, what each
required check does, and what to do when a check produces a false positive. That last one
matters — say plainly that the rule may be wrong and gets fixed with the concrete case as
justification. Otherwise people learn to work around gates instead of reporting them.

---

## Traps

Every one of these was hit in practice. They fail quietly, which is why they're listed.

**A required check's context must equal the reported check name**, which is the job's
`name:` or, absent that, its job id. Require a context that never reports and *every* PR
blocks forever with no useful message. Let the workflow run once, read the name from
`gh pr checks`, then require it.

**You cannot approve your own pull request.** As sole code owner your approval doesn't
register at all — `reviewDecision` stays `REVIEW_REQUIRED` and the reviews list is empty.
Your own work needs `gh pr merge --admin`; the team's PRs work normally because you approve
theirs.

**A ruleset with no `bypass_actors` locks out the owner too.** Correct for the team, fatal
for you, and you discover it on the first commit.

**A fix committed on a branch you then delete goes with it.** Especially dangerous right
after making a check required: `main` keeps the broken workflow and nothing can merge.
Check `main` after deleting any branch you fixed something on.

**A user-owned Project does not transfer with the repo.** Ownership moves, the board stays
with you, the link breaks. Decide before the transfer, not after.

**`CODEOWNERS` pointing at a non-collaborator fails quietly.** After a transfer, the
previous owner may no longer be a collaborator, and the code-owner requirement can't be
satisfied. Update it as part of the handover.

**`has_projects=true` is the legacy toggle.** It does not create or link a Project v2. You
can set it, see "projects enabled", and still have no board.

**The gitleaks action calls the PR-commits API.** It needs `pull-requests: read` and can
hit org licensing. The binary avoids both.

**Native secret scanning needs Advanced Security on private repos.** Check before promising
it; use a workflow otherwise.

**Non-ASCII through shell arguments gets mangled.** Titles and bodies in any language with
accents: write JSON to a temp file and use `gh api --input`, never `-f field=value`.

**`gh project item-edit --title` only works on draft issues**, and mixing it with field
flags fails with a bare help dump. For a draft-issue title use the GraphQL
`updateProjectV2DraftIssue` mutation.

**Excluding the guard's own workflow from its diff is a hole.** It stops the guard tripping
on its own rule text, but means a PR can weaken it unchecked. `CODEOWNERS` on `/.github/`
is what closes it.

---

## The order, condensed

1. Answer the five questions in §0.
2. Repo settings and dependency alerts.
3. Write the files: `CODEOWNERS`, PR template, `.gitmessage`, guard, secrets, Dependabot,
   `CONTRIBUTING.md`, `README.md`.
4. Push to `main` while it's still unprotected.
5. Let the workflows run once; read the reported check names.
6. Create the ruleset, with an admin bypass and those exact names.
7. Prove the gates with a deliberately violating PR, then check `main`.
8. `setup-ci` when the stack is decided.
9. Project, milestones and macro issues — only if you'll run them.
10. Grant the team `Write`. Never `Admin`.
