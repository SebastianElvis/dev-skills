# TikZ generation

Read this file after you define the evidence model and design specification.

## Source and dimensions

Copy `assets/architecture-template.tex` to the target path.
Replace every sample label, node, and relationship with verified content.
Use the template's styles, not its sample topology.
Keep the template's modern theme for every figure in the set.
Read [design-principles.md](design-principles.md#modern-theme) for the meaning of each style.

The template uses the TeX dependencies of janosh/diagrams: the `standalone` class with TikZ, and `mathtools`.
It adds the `FiraSans` font package.
It loads the TikZ libraries `arrows.meta`, `backgrounds`, `calc`, `decorations.pathreplacing`, `fit`, `positioning`, and `shapes.geometric`.
TeX Live supplies all of these packages.

Set text sizes explicitly in points. Use at least 8 pt at the final width.
Avoid whole-figure scaling as a substitute for layout changes.
Estimate the complete width before you place nodes.
Use vertical stages or panels when a horizontal layout exceeds the final width.

Use [the worked examples](worked-examples.md) for complete compositions with verified source facts.

## Notation and routes

Use solid boxes for owned components and dashed boxes for external systems when this distinction fits the specification.
Use labeled boundaries for ownership or deployment.
Use numbered arrows for ordered actions only.
Use explicit cardinalities for schemas. Keep static relationships unnumbered.

Use one main direction per ordered flow. Route responses separately when they matter.
Use explicit junctions for shared actions.
Keep distinct actions on separate segments.
Place labels on clear route sections. Use a white label background only when it hides no meaningful line.

## Build and inspect

Run the bundled renderer:

```bash
python3 path/to/visualize-arch/scripts/render_tikz.py docs/assets/system-architecture.tex
python3 path/to/visualize-arch/scripts/check_figure.py docs/assets/system-architecture.pdf --width-mm 180
```

The renderer uses the same tools as janosh/diagrams.
It requires `latexmk`.
It converts the PDF to SVG with `pdf2svg` when that command exists. Otherwise, it uses `pdftocairo`.
It optimizes the SVG with `svgo --multipass` when that command exists.
The checker requires `pdftohtml` and `pdftoppm`.
Poppler supplies `pdftocairo`, `pdftohtml`, and `pdftoppm`.
Install the optional tools with `brew install pdf2svg` and `npm install --global svgo`.

Inspect the color and grayscale previews.
The checker estimates font size from Poppler's rounded font records.
The checker permits 0.15 pt tolerance for rounded font sizes.
Treat possible text collisions as review prompts. Mathematical labels can cause false alarms.
The checker does not detect arrow crossings, missing relationships, or weak hierarchy.

Copy `assets/Makefile` beside the source when the repository needs a maintained build command.
Set `SOURCE` to the actual source name.
Keep the editable source, Portable Document Format (PDF), and Scalable Vector Graphics (SVG) files together.
Ignore temporary TeX files. Keep previews temporary unless the user requests them.

## Gotchas

Use `edge label` for a custom style.
A custom style named `label` overrides TikZ's label command and can remove boundary headings.
Use `step badge` for a numbered marker.
A custom style named `step` conflicts with the TikZ grid key, and the build fails.
