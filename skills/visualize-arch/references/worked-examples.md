# Worked examples

These examples show complete synthetic systems with verified structure and behavior.
Each example includes editable TikZ, a Portable Document Format (PDF) file, and a Scalable Vector Graphics (SVG) file.
Each example also includes color and grayscale previews.
The evidence files let you check the content without access to an external repository.

| Example | Preview | Editable source | Vector outputs | Final width | Intended medium |
| --- | --- | --- | --- | --- | --- |
| Dispatch Hub architecture | [Color](../assets/worked-examples/system-color.png), [grayscale](../assets/worked-examples/system-gray.png) | [system.tex](../assets/worked-examples/system.tex) | [PDF](../assets/worked-examples/system.pdf), [SVG](../assets/worked-examples/system.svg) | 300 mm | Wide documentation |
| Dispatch Hub data model | [Color](../assets/worked-examples/schema-color.png), [grayscale](../assets/worked-examples/schema-gray.png) | [schema.tex](../assets/worked-examples/schema.tex) | [PDF](../assets/worked-examples/schema.pdf), [SVG](../assets/worked-examples/schema.svg) | 180 mm | Paper figure |
| Release Desk workflow | [Color](../assets/worked-examples/workflow-color.png), [grayscale](../assets/worked-examples/workflow-gray.png) | [workflow.tex](../assets/worked-examples/workflow.tex) | [PDF](../assets/worked-examples/workflow.pdf), [SVG](../assets/worked-examples/workflow.svg) | 180 mm | Tall documentation |

Select an example by its question and structure.
Inspect its preview before you read its source.
Use the [reference catalog](examples.md) for the modern style references.

All three examples use the modern theme from [design-principles.md](design-principles.md#modern-theme).
The restyle on 2026-11-22 changed colors, fonts, fills, and some text widths.
The restyle did not change a node, a relationship, or a route.
Keep the target repository's actual facts when you adapt a composition.

## Dispatch Hub architecture

Caption: Dispatch Hub connects shared records to authorized submissions, dispatch work, status reads, and notice delivery.

### Brief and evidence

The figure explains how dispatch work, status reads, and notices share one logical system.
The command line interface (CLI) and Web client call the application programming interface (API).
The Dispatcher submits work. The Auditor reads status.
The [dispatch source](../assets/worked-examples/evidence/dispatch.py) defines authorization, intake, retry, scheduling, and notice delivery.
The [schema](../assets/worked-examples/evidence/schema.sql) defines the shared records.
The [configuration](../assets/worked-examples/evidence/deployment.toml) identifies logical components and external services.

Authorization checks submissions and manual retries. Status reads bypass that check.
The worker permits one automatic timeout retry. Provider rejection and a second timeout fail the stored run.
An accepted run creates a receipt and a notice entry.
The queues represent internal objects. Their boundaries make no claim about separate deployment services.

### Design choices

- The ownership boundary separates system components from ParcelCarrier and MailRelay.
- Separate actor nodes distinguish submission from audit access.
- Solid, dashed, and dotted paths distinguish work, status returns, and storage access.
- The orange accent marks the work path. Status and storage paths use the ink color.
- Explicit junctions show where client paths share the same request or response.
- The scheduler, worker, and notifier retain distinct responsibilities.
- Short notes explain conditions that affect the overview without turning it into a lifecycle figure.

### Review record

The architecture pilot applied authorization too broadly.
The corrected figure attaches the role check to submission and retry.
Its status note names the exception explicitly.
The selected source passed the six local evaluation dimensions in `reference-system`, trial 1.
The architecture case used Codex for all six dimensions.

The packaging check flags twelve pairs of text bounds inside component boxes.
The pairs describe adjacent lines. Visual inspection confirms separate baselines and readable glyphs.

The 300 mm composition serves wide documentation.
A paper layout needs a new composition at its required width.
Simple reduction to 180 mm would make its text too small.

## Dispatch Hub data model

Caption: The data model groups nine tables by identity, dispatch, and evidence. Its constraints preserve optional audit actors and unique receipts.

### Brief and evidence

The figure explains ownership, dispatch records, and stored evidence across nine related tables.
The [schema](../assets/worked-examples/evidence/schema.sql) supplies every field and relationship.
The Identity group contains four tables. Dispatch contains two tables. Evidence contains three tables.
The figure shows all 11 foreign-key relationships.

Each membership has a unique tenant, account, and role combination.
Each provider attempt has a unique run and sequence combination.
Each run permits at most one delivery receipt.
An automated audit event can omit its actor.

### Design choices

- Three columns preserve the domain groups at 180 mm width.
- Each table separates its name, fields, and constraints.
- Every foreign key has a visible route to its parent.
- Endpoint labels show cardinality. A dashed route identifies the optional audit actor.
- The legend defines type and key symbols without dependence on color.

### Review record

One earlier schema trial replaced relationship routes with notes.
That trial failed the visual comparison.
This example keeps all routes visible and uses notes for constraints.
The selected source passed the six local evaluation dimensions in `reference-paper-schema`, trial 1.
Codex also confirmed correctness and reference quality.

The figure fits 180 mm width and a 219 mm height.
The page layout must also reserve space for its caption.
The example does not establish readability at a single-column width.

## Release Desk workflow

Caption: Release Desk preserves event history across bounded build retries, manual recovery, cancellation, and independent publication.

### Brief and evidence

The figure explains release creation, approval, builds, manual recovery, cancellation, and independent publication.
The [release source](../assets/worked-examples/evidence/releases.py) defines every guard, state change, and event write.
The Operator calls these methods through a command line interface (CLI).
The external Runner and Registry expose application programming interfaces (APIs).

Only approval and manual retry require the maintainer role.
The second transient build result exhausts automatic retries.
Manual retry resets the attempt count and retains the release identifier and event history.
Publication changes `publish_state` and preserves the successful `built` state.
The source stores this model in memory.

### Design choices

- Four panels separate intake, build execution, recovery, and publication.
- Decision nodes show each guard with success and rejection paths.
- Orange dashed paths and orange outlined boxes mark rejections and failures.
- The event marker identifies the exact event beside the action or outcome that writes it.
- Matching continuation circles preserve connections across panels.
- Dashed service boxes distinguish external calls from local actions.
- The footer records shared history rules and the scope of role checks.

### Review record

The initial release figure used prose for several rejected operations.
The review requested explicit rejection paths and clearer labels.
One correction produced the selected source from `reference-publish`, trial 1.
A separate final evaluation used the canonical task without earlier critique in the scorer prompt.
The corrected source passed all six dimensions. Codex scored correctness and reference quality.
GLM scored readability, conciseness, aesthetics, and the final response.

The packaged figure adds definitions for its interface abbreviations.
Its tall composition targets documentation at 180 mm width.
A paper layout must split its panels to satisfy the page height limit.
Each separate panel must retain its continuation labels and necessary legend entries.

## Rebuild and verify

The renderer requires Python 3, `latexmk`, and `pdf2svg` or `pdftocairo`.
The checker also requires `pdftohtml` and `pdftoppm`.
These commands run from the skill directory:

```bash
python3 scripts/render_tikz.py assets/worked-examples/system.tex
python3 scripts/render_tikz.py assets/worked-examples/schema.tex
python3 scripts/render_tikz.py assets/worked-examples/workflow.tex
python3 scripts/check_figure.py assets/worked-examples/system.pdf --width-mm 300
python3 scripts/check_figure.py assets/worked-examples/schema.pdf --width-mm 180
python3 scripts/check_figure.py assets/worked-examples/workflow.pdf --width-mm 180
```

The checker creates the color and grayscale previews beside each figure.
The checker reports text size, bounds, and possible text collisions.
The visual review must still inspect routes, labels, and meaning at the final width.

## Provenance and evaluation use

The source figures come from the local evaluations on 2026-11-17.
The examples depict synthetic fixtures from this repository.
The bundle contains original figure sources and their renders.
The external artwork stays in the linked reference catalog or the authorized local cache.
The packaging check rebuilds the sources and verifies their dimensions.

These source cases now supply demonstrations and regression tests.
Future validation must use unseen systems and source facts.
The historical evaluation scores predate this bundle and its abbreviation definitions.
Those scores also predate the modern restyle.
Those scores do not prove performance on new systems.
