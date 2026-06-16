# Third-party notices — `core` skills

Some skills bundled in this plugin are vendored **verbatim** from third-party MIT-licensed repos.
Their copyright and license are retained below, as the MIT License requires.

## mattpocock/skills
- **Source:** https://github.com/mattpocock/skills
- **Commit:** `694fa30311e02c2639942308513555e61ee84a6f`
- **Vendored:** 2026-06-16
- **License:** MIT — Copyright (c) 2026 Matt Pocock
- **Skills used** (verbatim, under `plugins/core/skills/<name>/`): `diagnose`, `zoom-out`,
  `write-a-skill`, `handoff`, `caveman`.

The `caveman` skill in mattpocock/skills is itself adapted from **JuliusBrussee/caveman**
(https://github.com/JuliusBrussee/caveman, MIT). Only the markdown skill is vendored here — *not*
caveman's auto-activation hook or its JS/Python sub-skills (`/caveman-commit|review|stats`).

### MIT License (mattpocock/skills)
```
MIT License

Copyright (c) 2026 Matt Pocock

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

*To refresh: re-clone the upstream repo at a newer commit, re-copy the skill folders, and update
the commit SHA above.*
