---
name: visualize-arch
description: >-
  Use this skill to create or update verified architecture figures from a software repository.
  Use it for system overviews, components, actors, database schemas, user stories, and data or control flows.
  Use it to plan figure sets, improve diagram quality, or refresh figures after code changes.
  Use it for publication figures with editable TikZ and vector outputs.
  Do NOT use it for charts, dashboards, interface mockups, class diagrams, isolated call sequences, or decorative illustrations.
---

# Visualize architecture

Create figures that explain verified structure and behavior at their final display size.
Keep the source editable. Generate Scalable Vector Graphics (SVG) and Portable Document Format (PDF) outputs.
Use Simplified Technical English in figures, captions, plans, and reports.

This workflow adapts the reference selection in FigureForge and the planning, style, generation, and review stages in PaperBanana.
The stages describe separate decisions. One agent can perform every stage.

## Critical requirements

- Read the repository instructions before you inspect its files.
- Verify every actor, component, boundary, relationship, and flow from repository evidence.
- Use reference figures for visual design only. Never use them as evidence about the target system.
- Preserve the verified model when you change a layout.
- Preserve the current source format and build process when they exist.
- Use TikZ for new figures unless the user requests another editable format.
- Keep system code unchanged. Do not commit, push, or open a PR without a user request.
- Report unavailable references, tools, or visual checks. Never claim that compilation proves visual quality.

## 1. Plan the content

Inspect architecture documents, entry points, storage, configuration, external clients, and relevant tests.
Trace each important flow from its real actor or trigger to its outcome.
Resolve conflicting evidence before you draw. Mark unresolved assumptions explicitly.

Identify the audience, system boundary, and current or proposed state.
For each figure, record its question, main message, type, included elements, and excluded details.
Separate figures when their questions, actors, or outcomes differ.
Keep a static overview separate from detailed ordered behavior when their combination obscures either view.

Give the user a concise numbered plan with the figure count and each figure's purpose.
Continue within the requested scope unless the user requests approval before generation.
Ask a question only when missing information changes the meaning or scope.

Create a temporary evidence model before generation:

- Record each node's identifier, kind, label, owner, source path, and source symbol.
- Record each relationship's source, target, meaning, source path, and source symbol.
- Record each ordered flow's trigger, ordered actions, response path, and outcome.
- Record each in-scope state change and its event or data writes, including intake and cancellation.
- Keep static relationships separate from ordered actions.
- Record which operations use each important check and which operations bypass that check.
- Record which counters reset during retries and which identifiers, sequence numbers, and history persist.

For large repositories, use read-only subagents when available.
Give each subagent a separate evidence area. Require claims, source paths, source symbols, and unresolved questions.
Keep generation under one agent's control.

## 2. Select reference examples

Read [references/examples.md](references/examples.md).
Select two to four examples that match the figure's question and structure.
Prefer the user's examples and current repository figures when they fit.
Use janosh/diagrams and PetarV-/TikZ as the references for the modern visual style.

Inspect the actual images. Do not select references from captions alone.
Compare their panel arrangement, hierarchy, density, text size, grouping, and routes.
Record which design choices apply and which choices do not apply.
Choose one primary example for composition. Use other examples for specific supporting choices.

Identify the diagram type. Use the Kriterion figure of that type to choose the notation and required elements.
Use the bundled worked example of the same type when Kriterion access is unavailable.
Read [references/worked-examples.md](references/worked-examples.md) for complete architecture, schema, and workflow examples.
The bundled worked examples include evidence, design choices, review corrections, and editable outputs.
Report an incomplete visual comparison when no suitable reference is available.
Do not claim that an inaccessible image influenced the design.

## 3. Define the style

Read [references/design-principles.md](references/design-principles.md).
Create a temporary design specification for each figure:

- State the main message and the primary reference.
- State the final width, height limit, and intended medium.
- State the panel arrangement, reading direction, groups, and omitted details.
- State the minimum text size, font family, spacing, and line weights.
- Define each color, line style, marker, and schema notation.
- State how the figure preserves its meaning in grayscale.
- Draft a caption that answers the figure's question.

Use the venue's dimensions when available.
Otherwise use 85 mm for a paper column, 178 mm for a paper-wide figure, or 180 mm for repository documentation.
Use at least 8 pt text at the final width unless the venue specifies another minimum.
Choose a larger figure or split panels when labels cannot fit at that size.

Use the modern theme from the design principles for every figure.
Choose notation by figure type. Number ordered behavior only.
Use labels, line styles, or shapes in addition to color.
Compare two rough layouts for dense figures before you refine either layout.

## 4. Generate the figure

For TikZ, read [references/tikz.md](references/tikz.md).
Use the bundled styles as a starting point. Replace their sample structure with the verified model.
Use the selected composition rather than a fixed actor-left arrangement.

Use nouns for components. Use short action labels for ordered arrows.
Draw every in-scope schema relationship as a visible connection.
Show its keys and cardinalities. Use notes only for constraints.
Draw each required guard as a decision with visible success and rejection paths.
Use notes for shared invariants. Never replace a required branch with prose.
Keep each box's responsibility clear. Use explicit junctions for shared actions.
Give different actions separate line segments.

Keep the evidence model and design specification separate from generated presentation files.
Recheck evidence whenever a content change occurs.

## 5. Render and review

Build the figure with the current repository command or the bundled renderer:

```bash
python3 path/to/visualize-arch/scripts/render_tikz.py docs/assets/system-architecture.tex
python3 path/to/visualize-arch/scripts/check_figure.py docs/assets/system-architecture.pdf --width-mm 180
```

The checker requires Poppler's `pdftohtml` and `pdftoppm` commands.
It reports effective text size, page bounds, and text collisions.
It creates color and grayscale previews at the requested width.
Its checks cannot establish semantic correctness or detect every visual defect.

Read [references/review.md](references/review.md).
Inspect both previews at their final display size. Inspect an enlarged preview for route defects.
Use a separate Codex reviewer for the correctness review against the evidence model.
Use read-only subagents when the host supports them.
Give the reviewer the rendered figure, editable source, relevant repository evidence, and design specification.
Use another Codex reviewer for the visual review against the design specification and selected reference images.
Compare the figures at equivalent display widths. Record any material deficit against the selected references.
Record each defect with its location, effect, and proposed correction.

Correct the highest-impact defect first. Rebuild after each correction.
Repeat both reviews after any change that moves a node, label, or route.
Use three correction rounds as the default limit.
If defects remain, simplify the layout within scope or report the limitation.
Never label an unfinished figure as publication-ready.

## 6. Deliver the result

Keep the editable source, SVG output, and PDF output together.
Provide one documented build command for a new maintained figure.
Ignore temporary renderer files. Preserve requested generated outputs.
Change repository instructions or PR templates only when the user requests those changes.

List the exact path of every editable source and generated vector file.
Use one row or bullet for each figure. Give the caption path when the caption has a separate file.
State the final width, effective minimum text size, reference choices, and completed checks.
Report unresolved assumptions and unavailable checks.
Keep temporary evidence and review files uncommitted unless the user requests them.

## Gotchas

- A large canvas can hide unreadable text after publication scales the figure down.
- A workflow's colored steps do not describe schema cardinality or static ownership.
- A successful build does not identify an incorrect arrow or a weak main message.
- A paper's acceptance tier does not establish the quality of its figure.
- A reference image supplies design examples, not permission to copy its artwork.

## Final checklist

- [ ] Repository evidence supports every element and relationship.
- [ ] The figure answers its stated question within the requested scope.
- [ ] Actual reference images informed the recorded design choices.
- [ ] The figure shows every element that its diagram type requires, or the report names the missing element.
- [ ] The notation matches the diagram type.
- [ ] The final width preserves the required minimum text size.
- [ ] Labels and line styles preserve meaning in grayscale.
- [ ] The figure uses the modern theme styles and no emoji.
- [ ] The correctness review confirms each boundary, direction, and outcome.
- [ ] The visual review confirms hierarchy, spacing, routes, and readable labels.
- [ ] The editable source and generated outputs match.
- [ ] The report names unresolved defects and unavailable checks.
- [ ] Every figure, caption, and response uses Simplified Technical English.
