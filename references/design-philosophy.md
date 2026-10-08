# Design philosophy: evidence-led, grid-based, bilingual

The goal is a readable academic argument, not a dense dashboard or a uniform series of cards. Audience attention is limited: prioritize the question and the evidence needed to answer it. A short question can deserve its own slide. A fitting graph can deserve a large footprint even when a compact gap graph exists.

## Hard geometry

For slide width W, left/right margins M_L and M_R, n tracks and gutter G:

    U = W - M_L - M_R
    C = (U - (n-1)G) / n
    span(k) = kC + (k-1)G
    x(j) = M_L + (j-1)(C+G)

Require positive usable width and track width, integer n >= 1, nonnegative margins/gutter, integer spans k >= 1, and each row's spans summing exactly to n. Intentional blank space uses an explicit GridBlank span. The tiny rounding tolerance is for TeX scaled-point arithmetic, not approximate manual percentages.

Default: 160x90mm, 7mm side margins, 6 tracks, 6mm gutter. C=19.3333mm, span(2)=44.6667mm, span(3)=70mm, span(4)=95.3333mm. These are an approved starting preset, not an empirically universal optimum. For a different aspect ratio, recalculate and inspect, rather than scaling fonts blindly.

For component outer width W_i and side padding P_L, P_R:

    W_content = W_i - P_L - P_R > 0

For title, body, padding and semantic gap:

    H_required = P_T + H_title + d + H_content + P_B
    H_required <= H_available

Equation whitespace belongs to H_content. Never hide overflow with clipped boxes or a negative vertical skip. Row height checks complement the full frame overflow check; they do not account for other rows, notes or title height by themselves.

## Soft objectives, not a fake optimum

For a component importance score p_i > 0, a proposed normalized target share is:

    a_i* = p_i / sum(p_j)

Allocate minimum readable width/height first; then distribute remaining space. Map the result to integer spans, not fractional manual widths. Importance is a human/agent judgment, not an observed physical quantity. Do not present these weights as scientific measurements or let the formula override a deliberate sparse question slide.

Optional layout-review objective:

    L = w_A sum(|a_i-a_i*|) + w_G grouping_penalty
        + w_R alignment_penalty + w_E unnecessary_emphasis

All penalties must use a defined, normalized scale before comparing them. Weights and the objective are discussion aids only. The implementation does not claim to optimize comprehension or automatically rank interpretations.

## Semantic spacing

Require d_between > d_within for separate content groups. Default rhythm: 2mm for a label/detail relationship, 3mm within a group, 6mm between independent groups. Font metrics, equations and optically dense figures may justify a documented adjustment.

Align comparable elements to the same top baseline; match card heights only when the comparison benefits from it. Do not pad short explanations to imitate a long one. Grid alignment is geometric; optical alignment is checked in the render.

## Figure readability

For native figure size W_f,H_f and slot W_s,H_s:

    s_fit = min(W_s/W_f, H_s/H_f)
    s_required = f_min / f_native
    accept only when s_fit >= s_required

Font values must refer to the same physical units and include the smallest essential tick/legend label. A 2x PNG alone is not sufficient to infer native physical font size. If metadata is unknown, mark readability unverified and inspect the render. Failure means a wider slot, a cleaner figure, or another slide; not further shrinking. Preserve uncertainty, units, axes and evidence while removing only redundant decoration.

## Typography and emphasis

Use distinct title/body/note roles. Korean body glyphs default to 0.90 of the corresponding Latin size; inside block bodies they use 0.87, including bullets. Other roles retain 0.92. The bundled pdfLaTeX Nanum face applies the ordinary body correction at nominal 8.5--10.5pt. These font-specific settings are configurable and must not shrink Latin mathematics. Body is 10pt on this 160mm-wide canvas; focal equations use actual 12pt math, 4mm outside-block or 4.5mm inside-block whitespace on each side, in addition to block padding. Footnotes are 7pt for nonessential references only. Do not compare these directly with 13.33-inch PowerPoint point sizes without accounting for physical canvas scale.

Use muted text for references, not for information needed to interpret the outcome. Color denotes role, not a new category on each page. Light gradients and thin borders support continuity; they should not compete with the plot. Rounded blocks keep 3mm horizontal padding, 1.5mm title padding, 2.2mm body padding, 1.4mm corner radius and a 0.4pt outline as the default preset.

Place frame-wide qualifications and source notes in the measured bottom-note region above the footer. Keep figure-specific context local: figure title, muted figure note immediately beneath it, then the graphic. Do not confuse an interpretation with a small-print note. Note heights count against the usable content space; bottom placement must never cover a graph.

The cover is top-aligned with a configurable 22mm inset before the title, retaining the title/subtitle/author hierarchy. Opening and section outlines are optional navigation tools, not compulsory slides. Choose them according to the talk's structure and length.

## Academic integrity and editing

Choose the table family by meaning. Numerical/statistical evidence follows the paper's booktabs style: a few black horizontal rules, aligned numeric columns, panels and uncertainty/notes where relevant, no vertical rules. Conceptual relationships and literature comparisons use rule-free rows and generous spacing, with no background fills by default, not regression-table scaffolding. Give column headings black bold text, row labels dark-accent regular text, and descriptive cells black regular text; do not make headings and all row labels equally colored and bold. Neither family permits whole-table shrinking to solve overflow. State the relevant comparator and units where useful, without repeating every definition on every slide. Keep conclusions aligned with the study question and distinguish possible mechanisms from separately identified effects. Editing design must not silently change estimands, dates, samples, significance, or definitions.

Use author-year citations close to claims and a single continuous reference list in the appendix. A journal name or an unsupported percentage is not a substitute for a verified reference. Literature comparisons should distinguish unit of observation, outcome, horizon and payment context when those differences affect interpretation.

## Composition patterns

- A question: one focused sentence in a central four-span cell, with one blank track on each side. Do not add decoration simply to fill the page.
- A main result: a four-span graph and a two-span interpretation, or a full-width graph with a short lower caption when temporal detail needs space.
- Comparable results: three-plus-three spans, aligned scales and top baselines. Use two-plus-two-plus-two only if all three panels remain readable.
- Data: definitions before summary statistics; a large map or photograph may take four or all six tracks. Remove nonessential words before reducing the image.
- Literature: a full-width sequence of compact entries or lightly grouped rows; do not imply numeric equivalence between different measurement concepts.
- Mathematics: a full-width equation where possible, generous space above and below, and nearby variable definitions. Group secondary definitions instead of making a box for every symbol.

Choose a pattern because it fits the argument. The patterns are not mandatory section templates.
