---
name: academic-beamer-skill
description: "Create or revise academic LaTeX Beamer presentations using calculated column grids, bilingual typography, reusable themes, and render-based layout checks. Use for Beamer slide design and content layout; not for writing a paper or changing empirical results."
---

# Academic Beamer Skill

Use the supplied LaTeX components to preserve a coherent academic visual system across presentations. This is a normal source-backed Skill, not a gallery artifact template or an MCP server.

## Design contract

- Read [design-philosophy.md](references/design-philosophy.md) before composing a deck. Treat exact geometry and evidence integrity as hard constraints; visual priority and grouping are judgment-guided objectives.
- A six-column grid is a system of alignment tracks, not a requirement for six boxes. Choose spans according to the question, evidence and comparison: 4+2, 3+3, 2+2+2, or a full-width six-span row.
- Keep the question, the evidence, and the supported answer connected. Separate findings from hypotheses. Do not invent numbers, citations, confidence intervals, or causal interpretations to fill layouts.
- Preserve source figure axes, uncertainty, units and comparison groups. Crop only noninformative whitespace. Prefer reproducible scientific plots and vector PDF, not image generation for empirical charts.
- Use blocks selectively for grouping or emphasis. Keep supporting text flat when a box adds no meaning. Reduce content or split slides before shrinking body text or equation spacing.
- Distinguish numerical evidence tables (paper-style booktabs, aligned numbers) from conceptual relationship tables (no rules or background fills; accent labels and whitespace). Preserve reported values and uncertainty; table design must not change results.
- Keep main-talk and appendix structure flexible. No fixed slide count, section order, research model, university, author, or event is imposed.

## Use the package

1. For a new deck, scaffold the bundled starter with `python3 scripts/scaffold.py /absolute/path/to/new-deck --preset classic`. Use `--list-presets` to discover other available designs. The destination must not exist; never overwrite an existing deck. For an existing deck, inspect its sources and rendered relevant slides first, then adapt only requested pieces.
2. Read [layout-api.md](references/layout-api.md). Configure grid, margins, gutter, palette, metadata, cover title position, Korean body scaling and optional outline in `config.tex`. Keep school logos external and optional. The SKKU green palette is available, with no school identity attached.
3. Use `GridRow` and `GridCell` spans for horizontal composition, `AcademicEquation` for larger, spaced display math, and ordinary Beamer blocks with the padded component theme and separate Korean body correction. Select `AcademicStatTable` or `AcademicRelationTable` by content. Use `AcademicNote` for bottom-of-slide notes and `AcademicFigurePanel` for figure title, muted figure note and graphic, in that order. Use the local `\linewidth` inside every component. A figure-fit helper refuses known unreadable scaling; do not fabricate native font-size metadata.
4. Author sections in separate files when the deck grows. For an unfamiliar component, first render a representative mockup for approval if the user requested that checkpoint.
5. Follow [verification.md](references/verification.md). Build with `python3 scripts/build.py /absolute/path/to/main.tex --output /absolute/path/to/output --render`. Inspect every rendered slide, repair clipping/overlap and update the same final PDF. Geometry/log checks do not certify narrative quality or optical readability.

## Adding or changing designs

Read [extending-designs.md](references/extending-designs.md) when adding a template, palette, or component family. Preserve the stable content API and shared geometry checks. Add a named preset rather than silently changing the approved `classic` default; keep deck content and identity outside design modules. Existing decks retain their copied theme unless the user requests an update.

## Practical safeguards

- Keep the user's existing content and final files intact unless the requested edit changes them. Do not accumulate backups or archive copies automatically.
- Do not install TeX, fonts, Python packages, or global configuration without authorization. Use existing local tools and report missing dependencies.
- On macOS, a long build may run under `caffeinate -i` tied to the build process. Never leave a persistent sleep-prevention process running.
- Use built-in LaTeX preview for supported standalone files. This starter is a multi-file project; use an existing local TeX toolchain when the native compiler cannot resolve its project files.
- Creating a deck or using this Skill does not authorize commits, pushes, repository creation, publication, or uploads. Ask separately when required.

## Resources

- `assets/starter/`: editable demo and stable theme facade; common `theme/parts/`, selectable `theme/presets/` and `theme/palettes/`. Its data are explicitly illustrative.
- `scripts/geometry.py`: arithmetic and figure-readability checks, no external dependencies.
- `scripts/self_test.py`: positive and negative compiler tests, including 4/6/8-column grids.
- `README.md`: installation and GitHub packaging notes. No research data, satellite imagery, institution logo or fonts are distributed.
