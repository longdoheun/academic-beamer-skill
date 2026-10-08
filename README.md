# academic-beamer-skill

A reusable Agent Skill and LaTeX Beamer design system distilled from an iteratively reviewed bilingual economics presentation. It combines an evidence-led design philosophy with calculated grids and editable components. No MCP server is required.

## Use

Invoke `$academic-beamer-skill` and specify the paper/material, language, talk length, and any layout preference, for example:

> Use $academic-beamer-skill to make a 15-minute bilingual talk. Use six columns, a 4+2 layout for the main result, and the neutral palette.

The Skill does not force a fixed number of slides or a specific research design.

## Local commands

Run from this directory with Python 3 and an existing TeX distribution:

```sh
python3 scripts/scaffold.py /path/to/new-presentation
python3 scripts/scaffold.py --list-presets
python3 scripts/scaffold.py /path/to/another-presentation --preset neutral
python3 scripts/build.py /path/to/new-presentation/main.tex --output /path/to/new-presentation/output --render
python3 scripts/self_test.py --output /path/to/temporary-layout-tests
```

The starter contains editable examples. `references/layout-api.md` documents the actual interfaces; `references/design-philosophy.md` distinguishes mathematical constraints from visual judgment. Configure colors, identity, margins, cover title inset, Korean body/block sizes, and equation size/spacing in the deck's `config.tex`. Outlines are optional: `none`, `start`, `sections`, or `both`. Numerical tables use paper-style booktabs; conceptual tables use accent labels and spacing, with no rules or background fills. Frame-wide notes sit above the footer; figure-specific notes follow the local figure title. Logos are optional local inputs, not included in this package.

## Extending templates

The stable theme facade loads shared palette/layout/component modules. Named presets and palettes live in separate files; adding a valid preset file makes it selectable without editing the scaffold. The approved `classic` remains the default, and `neutral` is its existing blue variant. Deck-specific overrides follow `\AcademicPreset{...}` in `config.tex`. See [the extension guide](references/extending-designs.md) for file locations, component hooks and compatibility checks. Existing generated decks are not changed automatically.

## Installation and distribution

The source repository is [longdoheun/academic-beamer-skill](https://github.com/longdoheun/academic-beamer-skill). To install manually, clone it into an unused personal Skill directory:

```sh
git clone https://github.com/longdoheun/academic-beamer-skill.git ~/.codex/skills/academic-beamer-skill
```

Do not overwrite an existing installation or maintain separate edited copies of the same Skill. Other agents can use their supported skill-installation mechanism with this repository's root folder.

The package can be versioned independently of a research repository. Include SKILL.md, agents/, references/, scripts/, assets/starter/, README.md and .gitignore. Do not publish generated output, private metadata, research data, institutional logos, downloaded fonts, satellite imagery or credentials. The rules and code are newly generalized from the user's approved design; IODS was a visual reference, not a redistributed template.

The original code, design guides and starter are distributed under the [MIT License](LICENSE). External logos, imagery and fonts added by users retain their own terms and are not covered by this package's license. A normal Skill is distinct from a gallery artifact template; using it does not authorize publication of the user's presentation or data.

## Verification

Validated locally on 2026-10-08: Skill format validation, 13 arithmetic checks, 40 positive/negative TeX cases (including custom presets/palettes, both table families, enlarged block equations, measured Korean block-size correction, all four outline modes, bottom notes and figure panels) and seven scaffold checks covering discovery, vector assets and overwrite protection. The existing baseline also covers compilation with spaces in paths. The thirteen demo slides retain the approved design; structural changes are checked against their previously reviewed render hashes. The only remaining build warning concerns intentionally disabled EPS shell escape; this starter uses no EPS inputs. These checks establish the current baseline, not a guarantee for future edited content.
