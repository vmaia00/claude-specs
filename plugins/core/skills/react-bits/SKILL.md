---
name: react-bits
description: >
  Animated, interactive React components (react-bits) for adding motion and
  visual flair to front-end UI — the part Claude builds weakest. Use when
  building React/Next.js interfaces and the user wants animation, a memorable
  hero/landing, scroll/text effects, animated backgrounds, or to escape the
  generic shadcn look. Triggers: "react-bits", "add animation", "make it
  pop/feel premium", "animated background", "text animation", "fancy hero".
---

react-bits is a library of 130+ animated, interactive React components. Its value is
**motion and flair** — exactly the area generic AI-built UI is flat in, and the cheapest way to
make an interface feel intentional. Reach for it on top of a real brand layer, not as a substitute
for one.

## When to use it

- A hero/landing needs to feel memorable in a customer demo.
- The UI looks correct but generic ("everything Claude builds looks the same").
- You want a specific effect: animated text, scroll reveals, particle/gradient/wave backgrounds,
  interactive cards, custom cursors.

When **not** to use it: dense data/admin UIs, throwaway prototypes where speed beats polish, or
anywhere motion would distract. Don't sprinkle it everywhere — pick one or two signature moments.

## The anti-sameness point

Sameness is a **defaults** problem, not a missing-components problem. react-bits adds motion;
it does not fix generic typography, palette, radius, or spacing. Order of leverage:

1. **Tokens + typography** — your own fonts, color, radius, density (the biggest lever). For
   Bool work, start from the `bool-design` skill, not stock shadcn defaults.
2. **react-bits** — layer a few signature motions on top of that themed base.

If you skip step 1, react-bits just becomes the *new* sameness. It is a finisher, not a foundation.

## Install (per-project, not vendored here)

Components are copied into the consuming project — you own the code, no runtime lock-in. Two CLIs,
plus manual copy-paste from the site.

```bash
# shadcn registry (recommended; matches a shadcn/ui + Tailwind stack)
npx shadcn@latest add @react-bits/<Component-Variant>

# jsrepo is also supported
```

Every component ships in **4 variants** — pick the one that matches the project:

| Variant | Use when |
|---|---|
| `ts-tailwind` | TS + Tailwind (most common; shadcn stack) |
| `ts-css` | TS, plain CSS |
| `js-tailwind` | JS + Tailwind |
| `js-css` | JS, plain CSS |

A community **MCP server** also exists (search "react-bits" on mcp.directory) if you'd rather pull
components via MCP than the CLI.

## What's in it

Four categories. The live catalog at <https://reactbits.dev> is canonical and grows over time —
treat the names below as representative, not exhaustive.

- **Text Animations** — Split Text, Blur Text, Shiny Text, Gradient Text, Text Pressure,
  Scroll Reveal, Count Up, Decrypt Text.
- **Animations** — Animated Content, Fade Content, Magnet, Click Spark, Star Border,
  Pixel Transition, Blob Cursor, Splash Cursor.
- **Components** — Spotlight Card, Tilted Card, Dock, Gooey Nav, Carousel, Stack,
  Flowing Menu, Stepper.
- **Backgrounds** — Aurora, Particles, Waves, Dot Grid, Beams, Threads, Hyperspeed, Silk.

## License — read this before shipping to a client

react-bits is **MIT + Commons Clause**. Free for personal **and** commercial use, so using it inside
an MVP you deliver to a customer is fine. The Commons Clause only forbids *selling the components
themselves* as a standalone product or competing library. Practical line for a reseller: shipping
react-bits motion **as part of** a delivered app = allowed; repackaging react-bits **as** a product
you sell = not allowed.

Attribution and the upstream source are in `../../docs/THIRD-PARTY-NOTICES.md`.
