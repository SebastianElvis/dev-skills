# Reference figures

Read this file before you define the figure's style.
Inspect the actual figures before you adopt their design choices.
Select references by purpose, structure, and useful detail.

## Bundled worked examples

Read [worked-examples.md](worked-examples.md) when you need a complete local example without external access.
The bundle includes a system architecture, a nine-table schema, and a workflow with explicit guards and event writes.
Each example includes evidence, design choices, correction notes, editable source, vector outputs, and previews.
The guide states each example's width and intended medium.
Use the Kriterion figures for the diagram type when access permits.

## Modern style references

Use these two MIT-licensed galleries for the modern visual style.
They show concepts in machine learning and physics, not software systems.
Use them for fills, line weights, label placement, and density. Use the diagram types below for notation.

| Gallery | Inspected revision | Figures to inspect |
| --- | --- | --- |
| [janosh/diagrams](https://github.com/janosh/diagrams) ([site](https://janosh.github.io/diagrams)) | `7a79b3114e201fad9b6785e936eab859d1bc8c12` | [Generative Adversarial Network](https://janosh.github.io/diagrams/generative-adversarial-network), [CycleGAN](https://janosh.github.io/diagrams/cyclegan), [Self-Attention](https://janosh.github.io/diagrams/self-attention) |
| [PetarV-/TikZ](https://github.com/PetarV-/TikZ) | `86aee049f5355d77c598b936399e42caf8941e60` | The CycleGAN and Self-attention folders. janosh/diagrams hosts rendered copies. |

The inspected figures share these design choices:

- Flat node fills without outlines, and one saturated accent for the decision point.
- Black lines of one weight, with dashed lines for a second relationship kind.
- Short labels above an arrow, and the role name below the arrow.
- Wide white space instead of boundary boxes.

Adopt the flat fills, the single accent, and the label placement.
Do not adopt the mathematical labels or the serif font. Architecture figures use nouns and short action labels.
Each janosh/diagrams figure has a `.tex` source. Read the source to copy a TikZ technique, not a topology.

## Diagram types: Kriterion

The figures in [Kriterion's documentation](https://github.com/SebastianElvis/kriterion/tree/main/docs) show three diagram types.
The inspected revision is `420b229ceaafed446bffd5504d877cbc92a6b6e4`.
Access to this repository requires authorization.
Use the bundled worked example of the same type when that access is unavailable.

| Diagram type | Kriterion figure | Worked example | The type shows |
| --- | --- | --- | --- |
| System architecture | [System architecture](https://github.com/SebastianElvis/kriterion/blob/420b229ceaafed446bffd5504d877cbc92a6b6e4/docs/assets/system-architecture.png) | `system` | Actors, responsibilities, stores, boundaries, and complete interaction paths. |
| Workflow or lifecycle | [Submission lifecycle](https://github.com/SebastianElvis/kriterion/blob/420b229ceaafed446bffd5504d877cbc92a6b6e4/docs/assets/submission-lifecycle.png) | `workflow` | Activities, decisions, outcomes, failure paths, and information-only relationships. |
| Data model | [Data model](https://github.com/SebastianElvis/kriterion/blob/420b229ceaafed446bffd5504d877cbc92a6b6e4/docs/assets/data-model.png) | `schema` | Groups of related entities, keys, cardinalities, and important constraints. |

Select the figure that matches the target diagram type.
Use it to choose the notation and the elements that the type must show.
Do not use it as the visual style. The modern style references above set the style.
Keep the target system's actual scope. Never add components to match a reference's node count.
Improve crowded routes or small labels rather than copy those defects.
Adapt the composition to the final display size.
Use separate panels when a paper column cannot preserve the necessary detail.

## Selection and comparison

1. Choose the Kriterion figure or worked example that matches the diagram type.
2. Choose one or two modern style references for specific design decisions.
3. Record each source, figure number, useful choice, and rejected choice.
4. Inspect the source images at comparable display widths.
5. Compare semantic coverage, hierarchy, grouping, notation, routes, and final-size text.
6. Record any material quality deficit before you accept the result.

## Access and offline operation

Keep cached source pages and previews in a local, uncommitted directory.
Record the source URL and figure number beside each cached image.
Keep private reference images outside this distributed skill.
Link to public artwork unless its license permits redistribution.

Use an available cached reference when network access fails.
If no suitable reference is available, report that the visual comparison remains incomplete.
Keep the editable output, but withhold a claim of a complete visual comparison.

## Method sources

[PaperBanana](https://github.com/dwzhu-pku/PaperBanana) supplies the planning, style, generation, and review workflow.
[FigureForge](https://github.com/qwdwqfwq/topconf-paper-figure-gallery/blob/main/README.en.md) supplies the example selection and analysis approach.
This skill applies those methods to verified repository structure and behavior.
