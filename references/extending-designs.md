# Extending designs without changing existing decks

The design layer is independent of talk content. Keep one shared layout engine and stable content commands; add named styles rather than copying the whole theme for each new look.

## Current structure and load order

```text
assets/starter/
  main.tex                    illustrative content; replace per talk
  config.tex                  design selection, overrides, metadata and outline
  theme/
    academic-beamer.sty        stable entry point and named-file loader
    parts/
      palette.tex             identity and semantic color API
      layout.tex              grid, measured math/figures, validation and TOC API
      components.tex          default typography, blocks, tables, notes and chrome
    palettes/
      skku.tex                approved green colors
      neutral.tex             existing blue colors
    presets/
      classic.tex             approved default geometry and palette
      neutral.tex             inherits classic; changes palette only
```

Load the common theme first, select one preset in `config.tex`, then apply deck-specific overrides. A preset may inherit another preset, but inheritance must be acyclic. Select designs in the preamble, not slide by slide. Adding a file does not activate it or alter the default.

`classic` preserves the approved layout. `neutral` is a color variant, not a new academic narrative or slide order. Author, school, event, logos, research data and actual content never belong in a reusable preset.

## Add a palette

Create `theme/palettes/<name>.tex`:

```tex
% Example colors only; review contrast before adopting.
\AcademicColors{94,114,168}{24,55,78}
```

Select it with `\AcademicPalette{<name>}` after a preset. The first RGB triple is the accent; the second is dark text ink. Related structure/block/navigation/footer colors update together. Keep statistical table rules black and preserve relationship-table heading/label hierarchy; do not recolor each cell independently.

## Add a preset

Create `theme/presets/<name>.tex`, using only the differences from its base:

```tex
\AcademicPreset{classic}
\AcademicPalette{neutral}
\LayoutSetup{columns=8,gutter=4mm}
% Optional: \input{theme/extensions/my-components.tex}
```

Names start with a lowercase letter and contain lowercase letters, digits or hyphens. The TeX loader rejects path traversal and unknown designs. The scaffold discovers valid preset filenames automatically; there is no second registry to synchronize.

```sh
python3 scripts/scaffold.py --list-presets
python3 scripts/scaffold.py /absolute/path/to/new-deck --preset <name>
```

Scaffolding copies the shared engine, presets, palettes and any added component files into the new deck. It retains legitimate vector PDF assets while excluding build products. Existing destination directories are rejected. Previously generated decks keep their own copied design files; changing the Skill does not migrate them silently.

## Add components or a substantially different look

Create a component file under `theme/extensions/` only when an actual new component is needed, and load it from its preset. Prefer ordinary Beamer font/color/template hooks or new, uniquely named semantic components. A new cover or footline may override the public rendering component while preserving metadata arguments. A substantially different content starter can use the same facade; the current scaffold selects design presets only, not arbitrary slide narratives.

Keep these interfaces compatible:

- `GridRow`, `GridCell`, `GridBlank`, `GridSpanWidth`: exact local-width grid accounting.
- `LayoutSetup`: centralized geometry and spacing validation.
- `AcademicEquation`, `AcademicFigure`: measured content; no automatic shrinking to hide overflow.
- `AcademicNote`, `AcademicFigurePanel`: measured bottom notes and title/note/figure sequence.
- `AcademicStatTable`, `AcademicRelationTable`, `AcademicTableHeading`, `AcademicTableLabel`: statistical vs conceptual meaning and text hierarchy.
- `AcademicTitleFrame`, `AcademicAppendix`, `AcademicOutlineSetup`: stable metadata/navigation behavior.

Do not bypass the shared engine's checks, shadow another component name accidentally, or edit `parts/layout.tex` merely to produce a new look. If a genuine API change is necessary, document migration explicitly and retain compatibility where practical. New public defaults belong in a new preset unless the user approves a change to `classic`.

## Verify an extension

1. Add compiler tests that exercise the new preset or component, including local grid widths and relevant failure modes. Test actual colors/geometry, not merely that its filename appears.
2. Confirm scaffold discovery and generated-deck compilation. Check any external assets and fonts without installing dependencies automatically.
3. Render representative bilingual text, block equations, both table families, large figures and footer/notes. Review the extension's own output before treating it as an approved design.
4. Rebuild `classic`. Compare per-page PNG hashes with the previously reviewed baseline: a pure structural change should leave every pixel unchanged. Changed pages need visual review.

Package the shared engine and only licensed reusable design assets. No template addition authorizes publishing private content, committing or uploading to GitHub.
