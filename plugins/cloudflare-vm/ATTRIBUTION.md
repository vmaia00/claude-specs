# Attribution — cloudflare-vm plugin

- **Source:** <https://github.com/themusebook/skills>, directory `skills/cloudflare/`,
  commit `1c523aba5cdf867a79f078847075492d7778092a`, vendored 2026-11-23.
- **Upstream of the source:** themusebook's skill extends Cloudflare's official
  <https://github.com/cloudflare/skills> (`skills/cloudflare/`, Apache-2.0). It covers
  63 products where cloudflare/skills now has 26. `LICENSE` here is the cloudflare/skills
  Apache-2.0 text.
- **⚠ Licence caveat:** themusebook/skills has **no LICENSE file** (GitHub reports null). The
  content is redistributed here on the basis of the Apache-2.0 upstream it derives from. Before
  redistributing beyond personal use, check with themusebook, or re-vendor only the products
  that exist in cloudflare/skills.
- **Changes:**
  - Each `references/<product>/` directory became its own skill, `skills/<product>/`, so it can
    be called as `/cloudflare-vm:<product>`. Its `README.md` became `SKILL.md`, with added
    frontmatter (`name`, a description taken from the README's title and first line,
    `disable-model-invocation: true`) and a short header: a staleness notice and an
    instruction to read every file in the directory. The other files are unchanged.
  - The top-level `SKILL.md` became `skills/cloudflare-vm/SKILL.md`. It has a new name and
    description, a paragraph on where the product skills live, and links changed from
    `references/<p>/` to `../<p>/`. The body is otherwise unchanged.
- **Re-vendoring:** the per-product layout is generated mechanically from the upstream tree.
  Re-run the same transform on a fresh checkout and bump `version` in `plugin.json`.
