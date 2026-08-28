# TikZ architecture diagrams

Read this file when you create a new TikZ diagram or repair a current TikZ diagram.

## Start the diagram

Copy `assets/architecture-template.tex` to the repository diagram path. Replace every sample label, node, and flow with verified content.

Copy `assets/Makefile` beside the TeX file when the repository needs a durable build command. Set `SOURCE` in the Makefile when the file name differs.

Do not keep a sample node that has no repository evidence.

## Use the styles

Use these style roles consistently:

- `actor` for people and external initiators.
- `component` for owned runtime components.
- `store` for owned persistent storage.
- `external` for systems outside the owned boundary.
- `network` for an external network.
- `relation` for configuration and static relationships.
- One flow style for each user story.

Use a color-blind-safe palette. The template supplies five flow colors with strong contrast.

## Route flows

Use orthogonal paths by default. Add a junction when two entry paths use the same execution path.

Share one segment only when two paths use the same action. Use separate segments for different actions.

Keep two paths apart when they carry different user stories. Do not solve a path overlap with label movement alone.

Attach arrows to different box anchors when many paths use one component. Increase the component size when the anchors remain too close.

Put the step marker and action label near the middle of the related segment. Keep the label background transparent.

## Build and inspect

Run the bundled renderer from the skill directory:

```bash
python3 scripts/render_tikz.py path/to/system-architecture.tex
```

The renderer requires `latexmk` and `pdftocairo`. It creates Portable Document Format (PDF) and Scalable Vector Graphics (SVG) files.

Use `pdftoppm` when it exists to make a PNG preview:

```bash
pdftoppm -png -singlefile -r 120 system-architecture.pdf /tmp/system-architecture
```

Inspect the preview after each source change. Check the final SVG as XML when `xmllint` exists.

```bash
xmllint --noout system-architecture.svg
```

## Keep repository files current

Store the TeX, SVG, and PDF files together when the repository tracks generated files. Do not edit the generated files directly.

Ignore these common temporary files:

```text
*.aux
*.fdb_latexmk
*.fls
*.log
*.out
*.synctex.gz
```
