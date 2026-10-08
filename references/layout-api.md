# LaTeX API and geometry

## Configuration

Use `\documentclass[10pt,aspectratio=169,compress]{beamer}` and the bundled theme. `\LayoutSetup{...}` is preamble-only:

```tex
\AcademicPreset{classic}
% Optional deck-specific overrides follow the preset:
\LayoutSetup{columns=6, margin-left=7mm, margin-right=7mm, gutter=6mm,
  row-gap=3mm, max-row-height=55mm,
  padding-x=3mm, padding-title=1.5mm, padding-body=2.2mm,
  radius=1.4mm, equation-gap=4mm, block-equation-gap=4.5mm,
  equation-size=12pt, equation-leading=15pt, title-top=22mm,
  korean-scale=0.92, korean-body-scale=0.90, korean-block-scale=0.87}
\AcademicOutlineSetup{mode=start,title=Outline,toc-options=hideallsubsections}
\AcademicPalette{skku}
\AcademicIdentity{Sample University}
```

Bundled presets: `classic` (approved green baseline), `neutral` (same geometry and components, blue palette). `\AcademicPreset{...}` is preamble-only and loads the corresponding file in `theme/presets/`; later explicit settings override it. Existing direct `LayoutSetup`/`AcademicPalette` usage remains supported. Discover available presets with `python3 scripts/scaffold.py --list-presets`; new named files are detected automatically.

Palette choices: `skku` (RGB 141/198/63 accent, dark green ink), `neutral` (blue accent/ink). `\AcademicPalette{...}` loads `theme/palettes/<name>.tex`. `\AcademicColors{accent RGB}{ink RGB}` defines the two semantic colors and refreshes the related Beamer color roles. Palette and identity are independent. Author/title/event are ordinary Beamer short metadata: `\author[Short]{Full}`, `\title[Short]{Full}`, `\date[Event]{Event}`. `\AcademicLogo{path/to/logo.pdf}` is optional, disabled by default. No logo or specific identity is bundled. See [extending-designs.md](extending-designs.md) for additional designs and compatibility rules.

Korean support is loaded by the starter when koTeX is installed. The body scale 0.90 applies at nominal font sizes 8.5--10.5pt; other sizes keep the general scale 0.92. Block bodies, including Korean bullets and bold text, use a separate 0.87 scale; block headings retain the title hierarchy. This is a glyph-size correction, not a reduction of Latin body text or mathematics. Only pdfLaTeX Nanum Myeongjo shapes are retuned; other engines/faces are not automatically corrected. Configure these before `\begin{document}` and check optical balance. Missing koTeX is not an error for an English-only deck; Korean content requires it.

`title-top` is the inset from the top-aligned cover's text area before its title. It does not change ordinary frame titles. The 22mm default starts the title slightly lower than the previous centered composition; increase/decrease it without changing the author gap.

## Optional outline

`\AcademicOutlineSetup{mode=...}` is preamble-only. Modes are `none` (theme default), `start`, `sections`, and `both`. The starter selects `start` to demonstrate the opening outline. Put `\AcademicOutline` immediately after the title frame; it becomes a no-op when the opening outline is disabled. Section outlines use Beamer's section hook and highlight the current section. This hook can be replaced by an existing deck's own `\AtBeginSection` handler.

The `title` and `toc-options` keys control wording and standard Beamer TOC options. Use `toc-options={sectionstyle=show/show,subsectionstyle=show/show/hide}` or other valid Beamer options when more detail is useful. For a manually placed outline, use `\AcademicOutlineFrame[Roadmap]{hideallsubsections}` at the desired location. Outline pages count as main-talk frames. TOC entries require the usual multi-pass build; the builder runs latexmk to resolve them.

## Rows and cells

```tex
\begin{GridRow}
  \begin{GridCell}{4}
    % Figure, table or text, using \linewidth
  \end{GridCell}
  \begin{GridCell}{2}
    \begin{block}{Interpretation}
      Evidence-supported interpretation.
    \end{block}
  \end{GridCell}
\end{GridRow}
```

Rows top-align cells and insert exactly one configured gutter between adjacent cells. They validate positive integer spans, exact track totals, natural box width and maximum row height. Do not insert `\hfill`, extra horizontal skips or ordinary Beamer columns between cells. Content must not escape its minipage. Nested GridRows are intentionally unsupported; use a new row or regular content inside one cell.

`\GridBlank{1}` consumes one intentionally empty track. `\GridRow[columns=8]` overrides the track count for that row only; it preserves margins and gutter. `\GridSpanWidth{4}` exposes a span width inside the current row. `\LayoutSetup` changes the deck defaults, not a slide mid-document.

Arithmetic uses the current row's `\linewidth`, so cells and component padding share one source of truth. Grid tests allow <=0.01pt rounding, well below one visible pixel. The engine checks a declared maximum for each row; only the complete-frame log check detects the sum of rows/title/notes exceeding available frame height.

## Components

- Ordinary `block` and `alertblock` use configurable padding, rounded corners and a thin outline. Avoid nested blocks; they share measured box registers.
- `\AcademicEquation{...}` uses actual 12pt display math (15pt leading), with 4mm above/below outside blocks and 4.5mm inside blocks. The block gap is additional to the block's body padding. All four values are configurable through `LayoutSetup`; leading must be at least the equation size. `AcademicEquation` measures the enlarged expression and reports an error if it exceeds the local content width. Use `aligned`, a wider span, or another slide instead of graphic scaling. Ordinary `$...$` variable names retain the surrounding text size; use this component for focal equations.
- `\AcademicNote{...}` puts a muted 7pt reference/qualification in Beamer's measured bottom-of-frame region above the footer, without a marker. Multiple notes stack there, even when requested from a GridCell. The region reserves height rather than overlaying content. Essential assumptions belong in the body. Existing numbered footnotes keep their markers.
- `\AcademicFigureTitle{...}` and `\AcademicFigureNote{...}` are local components: a 9pt bold title followed by a 7pt muted note, using the same note styling as the frame-level notes.
- `AcademicFigurePanel` takes two arguments (title, note) and a body containing a graphic or code-generated plot. It keeps that local sequence together and works inside a GridCell. Its title/note height consumes part of the row's maximum height; enlarge the slot or shorten the note if needed.
- `\AcademicTitleFrame` uses current metadata, a horizontally centered title at the configured cover inset and separated author/identity, with the same footer as content slides.
- `\AcademicAppendix` enters the appendix, hides navigation and labels backup pages without pretending they belong to the main-talk count.
- `\AcademicFigure[height=35mm]{file.pdf}` preserves aspect ratio and fits the local width and declared maximum height. Optional keys `native-width`, `native-height`, `native-font`, `min-font` activate a readability check, e.g. `native-width=100mm,native-height=60mm,native-font=10,min-font=8`. Font values are TeX points. Supply all three native fields or none. Unknown metadata produces an explicitly unverified fit, not a readability certificate.

```tex
\begin{AcademicFigurePanel}{Observed and Comparison Paths}{Monthly index; source and scope.}
  \centering
  \AcademicFigure[height=35mm]{figures/result.pdf}
\end{AcademicFigurePanel}
% Elsewhere in the same frame:
\AcademicNote{Frame-wide qualification or source.}
```

## Boundaries

This is a multi-file, locally compiled Beamer project. It needs existing Beamer, TikZ, graphicx and a working TeX engine. NewTX/koTeX are optional unless their typography/language is requested. The demo uses pgfplots only for an illustrative, reproducible chart; the theme itself does not require it. Scripts never install packages.

The engine is intentionally conservative: invalid rows stop compilation. Oversized figures fit geometrically, but unreadable essential labels require redesign. Whole-page optical overlap and dense text still need render review. No algorithm proves that a sparse slide has the correct narrative or a causal claim is warranted.

## Two table families

Use `AcademicStatTable` for numerical evidence: summary statistics, regression/estimation tables, and statistical tests. It follows the paper's restrained `booktabs` convention: black top/bottom rules supplied by the component, a caller-supplied `\midrule` below the header, no vertical rules, panel labels and space between groups. The default is 9pt/11pt with row stretch 1.3 and 5pt column padding. Use `r` columns for numeric alignment and one flexible `X` label column; `siunitx` alignment can be used if already available in the deck. Do not automatically round, add stars, or change reported numbers.

```tex
\begin{AcademicStatTable}{Xrr}
  & \textbf{(1)} & \textbf{(2)}\\
  & Baseline & Alternative\\\midrule
  Exposure & 0.12 & 0.08\\
  & (0.09) & (0.11)\\\addlinespace[2mm]
  Observations & 1,200 & 1,180\\
\end{AcademicStatTable}
\AcademicNote{Illustrative numbers only; parentheses show standard errors.}
```

Use `AcademicRelationTable` for concepts, literature comparisons, or mappings between sources and roles. No top/mid/bottom/vertical rules or background fills by default: organize with distinct headings/key labels and whitespace. The default is 10pt/12pt with row stretch 1.6 and 7pt column padding. Keep substantial text ragged-right, not justified; place a comparison in a wider span if it wraps excessively. `\AcademicTableHeading{...}` is black bold text for column headings; `\AcademicTableLabel{...}` is dark-accent regular text for row labels. Other cell content stays black regular. This separates the heading from the data by both color and weight, rather than styling every label identically. An extra 1mm after the heading row reinforces grouping without rules. Do not introduce alternating shaded rows or a colored header band merely to fill the layout. Color signals grouping, not significance or an invented substantive distinction.

```tex
\begin{AcademicRelationTable}{>{\raggedright\arraybackslash}X >{\raggedright\arraybackslash}X}
  \AcademicTableHeading{Measure} & \AcademicTableHeading{Role}\\[1mm]
  \AcademicTableLabel{Income} & Resource received\\[2mm]
  \AcademicTableLabel{Local sales} & Spending retained locally\\
\end{AcademicRelationTable}
```

Both environments use local `\linewidth`, work in grid cells and accept ordinary `tabularx` column specifications. They capture their body to let `tabularx` measure it correctly. Do not nest them or put a floating `table` inside a grid cell. Neither component shrinks an oversized table: reduce displayed columns or split it across slides. Frame notes use `AcademicNote`, rather than shrinking explanatory content into the table itself.
