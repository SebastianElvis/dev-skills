# Figure design principles

Apply these rules after content planning and reference selection.

## Content and hierarchy

- Give each figure one question and one main message.
- Emphasize the components that explain the main message.
- Remove detail only when that detail does not change the meaning.
- Group components by verified responsibility, ownership, or deployment.
- Label the grouping rule. Do not imply that ownership always equals deployment.
- Keep external systems outside the owned boundary.
- Put configuration inside its actual ownership boundary.
- Separate design-time actions from runtime actions.
- Attach operation-specific checks to the operations that actually use them.
- Label an unchecked path explicitly when nearby operations use a check.
- Keep a shared component from implying a shared policy for every operation.

## Choose the composition

| Figure type | Default composition | Required notation |
| --- | --- | --- |
| System overview | Place groups around the main dependency path. | Name boundaries and relationships. |
| Ordered workflow | Arrange stages in one reading direction. | Show triggers, actions, responses, and outcomes. |
| Database schema | Place related entities near their relationships. | Show keys, relationship labels, and cardinalities. |
| Subsystem detail | Show an overview panel beside a detail panel. | Match identifiers across the panels. |
| Comparison | Align corresponding components in separate panels. | Use the same scale and notation in both panels. |

Use an actor-left arrangement when it clarifies an interaction.
Use a vertical arrangement when the final width limits horizontal space.
Use multiple panels when an overview and detail answer different parts of one question.
Use separate figures when panels still require incompatible scales.

## Notation

- Use nouns for component labels.
- Use verbs for ordered actions.
- Use explicit keys and cardinalities for schema relationships.
- Draw a connection for each in-scope foreign key in a complete schema.
- Keep relationship routes visible. Change the layout when routes cross.
- Use notes for constraints. Never replace a required relationship route with a note.
- Number steps only when order matters.
- Restart numbers for each independent workflow.
- Give alternative triggers the same number only when they enter the same stage.
- Use one accent per workflow when multiple workflows need distinction.
- Keep static relationships black or gray and unnumbered.
- Name each line style in a legend when its meaning is not obvious.
- Distinguish requests and responses when both matter.
- Show periodic behavior from its verified trigger. Never invent a timer actor.
- Merge shared actions at explicit junctions.
- Give different actions separate segments.

## Final dimensions

Use the venue's requirements first. Use these defaults when requirements are absent:

| Property | Default |
| --- | --- |
| Paper column width | 85 mm |
| Paper-wide width | 178 mm |
| Repository figure width | 180 mm |
| Minimum final text size | 8 pt |
| Main label size | 9–10 pt |
| Panel heading size | 10–11 pt |
| Main line width | 0.6–0.9 pt |
| Secondary line width | 0.5–0.6 pt |
| Clear space around labels | At least 2 mm |
| Gap between unrelated groups | At least 4 mm |

Measure text after any scaling. Keep one font family across the figure set.
Avoid a large title inside a paper figure when its caption supplies the title.
Use panel labels for cross-references. Define technical abbreviations in the caption or figure.

## Color and routes

- Use dark text on white or pale fills.
- Reserve saturated colors for the main distinctions.
- Use at most three semantic accents unless more distinctions are necessary.
- Repeat a color only when its meaning stays the same.
- Add labels, markers, or line patterns when color carries meaning.
- Check grayscale readability at the final width.
- Use orthogonal routes for dense dependency diagrams.
- Use direct routes for sparse diagrams when those routes reduce crossings.
- Keep arrows clear of boxes and labels.
- Increase space before you reduce text size.
- Split dense views before you change a verified path.

## Modern theme

Use one modern theme for every figure.
The theme takes its palette from the Metropolis Beamer theme.
It takes its flat fills and sparse lines from janosh/diagrams and PetarV-/TikZ.
`assets/architecture-template.tex` defines each style below.

| Element | Style | Meaning |
| --- | --- | --- |
| Text and static lines | `ink` (`#23373B`), Fira Sans | All text and every unnumbered relationship. |
| Main flow | `accent` (`#EB811B`), 0.9 pt, `step badge` | The ordered path that supports the main message. |
| Owned component | `component`: flat `primary` (`#9FCFCC`) fill, no outline | A component inside the system boundary. |
| Data store | `datastore`: `store` (`#D3DADD`) cylinder | A database, queue store, or file store. |
| Actor | `actor`: white pill with an `ink` outline | A person or a client that starts an action. |
| External system | `external`: white box with a dashed outline | A system outside the owned boundary. |
| Boundary | `group`: `zone` (`#F2F5F6`) fill, no outline | An ownership or deployment boundary. |

- Use flat fills. Do not use shadows, gradients, or 3D effects.
- Use `accent` for the main flow. Draw static relationships in `ink`.
- Add at most two more accents when independent workflows need distinction.
- Use a different line pattern, not a new hue, for a second relationship kind.
- Keep the shape for each node kind. Grayscale readers depend on the shape.
- Do not use emoji. The PDF build cannot render color emoji, and emoji lose their meaning in grayscale.
