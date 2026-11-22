# Figure review

Use this review after each render. Review correctness and visual quality separately.
Write all review notes in Simplified Technical English.

## Correctness review

Compare the rendered figure with the evidence model, not with the reference figures.

- Verify each actor, component, store, and external system.
- Verify each boundary against ownership or deployment evidence.
- Trace every ordered path from its trigger to its outcome.
- Require visible success and rejection paths for each in-scope guard.
- Fail when prose replaces a required decision or branch.
- Verify the state changes and event writes at each in-scope operation.
- Name the covered operations when a shared note describes event writes.
- Check request and response directions.
- Trace each retry loop. Verify which counters reset and which identifiers, sequence numbers, and history persist.
- Verify the scope of each authorization or validation check.
- Confirm that the figure identifies meaningful exceptions to those checks.
- Check static relationship labels and schema cardinalities.
- Match each in-scope foreign key to a visible route. Fail when notes replace required routes.
- Confirm that shared segments represent the same action.
- Confirm that each omission preserves the main message.

Fail this review when a figure adds an unsupported element or changes verified behavior.
Resolve a code defect separately from a diagram defect.

## Visual review

Compare the figure with its design specification and selected reference images.
Inspect the color preview and grayscale preview at the final width.
Use verified PDF measurements for numeric font sizes. Judge visual legibility separately.
Use an enlarged preview only for detailed route checks.
Place the result beside its primary reference at an equivalent display width.
Use the Kriterion figure of the same diagram type to check notation and required elements.
Use janosh/diagrams and PetarV-/TikZ to check the visual style.
Compare semantic coverage, visual notation, hierarchy, grouping, and route clarity.
Keep simple systems concise. Never add unsupported detail to imitate reference complexity.

Score each dimension separately:

| Dimension | 0: fail | 1: revise | 2: pass |
| --- | --- | --- | --- |
| Main message | The figure has no clear focus. | The reader must search for its focus. | The hierarchy shows its main message. |
| Text | Labels clip or violate the size requirement. | Labels fit but spacing hinders reading. | Labels remain clear at the final width. |
| Routes | Routes obscure relationships or directions. | Crossings require unnecessary effort. | Routes and directions remain clear. |
| Density | Detail hides the structure. | Some groups need more space. | Groups have clear boundaries and useful detail. |
| Consistency | Symbols or colors change meaning. | Some styles lack a clear purpose. | Notation stays consistent across figures. |
| Grayscale | Color loss removes meaning. | Some distinctions need stronger markers. | Labels and patterns preserve all distinctions. |

Accept a figure only when correctness passes and every visual dimension scores 2.
Require the direct reference comparison to pass as well.
Record a material deficit as an unmet requirement, even when the figure compiles and its labels remain readable.
Treat scores as review criteria, not objective proof of aesthetic quality.

## Correction record

Record each defect with these fields:

- State the figure and affected node, edge, or panel.
- Describe the visible defect.
- State its effect on correctness or readability.
- Specify one correction.
- Record the result after the next render.

Correct unsupported content first. Correct clipping and unreadable text next.
Correct ambiguous routes before minor spacing defects.
Recheck the full figure after each correction.

Use three correction rounds by default.
If a round makes no improvement, change the composition or reduce nonessential detail.
Report remaining defects when the round limit ends.
Preserve the last correct source and its matching outputs.

## Review example

- Figure: The worker workflow.
- Location: The arrow from Worker to Carrier.
- Defect: The label crosses the return arrow.
- Effect: The reader cannot identify the request direction.
- Correction: Place the return arrow below the request arrow.
- Result: Both labels remain clear at 85 mm width.
