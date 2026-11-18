# Reference figures and minimum quality

Read this file before you define the figure's style.
Inspect the actual figures before you adopt their design choices.
Select references by purpose, structure, and useful detail.

## Bundled worked examples

Read [worked-examples.md](worked-examples.md) when you need a complete local example without external access.
The bundle includes a system architecture, a nine-table schema, and a workflow with explicit guards and event writes.
Each example includes evidence, design choices, correction notes, editable source, vector outputs, and previews.
The guide states each example's width and intended medium.
Use an external reference for an independent quality comparison when access permits.

## Minimum quality: Kriterion

The maintainer sets the minimum with the figures in
[Kriterion's documentation](https://github.com/SebastianElvis/kriterion/tree/main/docs).
The inspected revision is `420b229ceaafed446bffd5504d877cbc92a6b6e4`.
Access to this repository requires authorization.
Use the public references below when that access is unavailable.

| Reference | Minimum requirement |
| --- | --- |
| [System architecture](https://github.com/SebastianElvis/kriterion/blob/420b229ceaafed446bffd5504d877cbc92a6b6e4/docs/assets/system-architecture.png) | The figure distinguishes actors, responsibilities, stores, boundaries, and complete interaction paths. |
| [Submission lifecycle](https://github.com/SebastianElvis/kriterion/blob/420b229ceaafed446bffd5504d877cbc92a6b6e4/docs/assets/submission-lifecycle.png) | The figure distinguishes activities, decisions, outcomes, failure paths, and information-only relationships. |
| [Data model](https://github.com/SebastianElvis/kriterion/blob/420b229ceaafed446bffd5504d877cbc92a6b6e4/docs/assets/data-model.png) | The figure groups related entities and shows keys, cardinalities, and important constraints. |

Use these figures to assess semantic coverage, visual notation, hierarchy, and density.
Keep the target system's actual scope. Never add components to match a reference's node count.
Improve crowded routes or small labels rather than copy those defects.
Adapt the composition to the final display size.
Use separate panels when a paper column cannot preserve the necessary detail.

## Public shortlist

These annotations follow visual inspection of the source pages.
The page numbers below count from the first page of each linked document.
They include a conference cover when that document has one.

| Identifier | Source figure | Page | Use |
| --- | --- | --- | --- |
| `mooncake-architecture` | Mooncake, Figure 2 | 3 | Use it as a primary architecture reference. |
| `mooncake-workflow` | Mooncake, Figure 3 | 5 | Use it as a primary reference for transfers across resource boundaries. |
| `ray-task-flow` | Ray, Figure 7 | 9 | Use it as a primary reference for request and result workflows. |
| `vllm-block-mapping` | PagedAttention, Figure 6 | 6 | Use it as a primary reference for mapping between logical and physical data. |
| `sglang-state-series` | SGLang, Figure 3 | 5 | Use it as a supporting reference for state changes across panels. |

### Mooncake: architecture

[Open Figure 2](https://www.usenix.org/system/files/fast25-qin.pdf#page=3).
[Open the publication record](https://www.usenix.org/conference/fast25/presentation/qin).

The figure separates scheduling, repeated instances, resource tiers, transfers, and optimization goals.
Its grouped regions explain several responsibilities within one coherent composition.

- Use nested groups when ownership and resources require different boundaries.
- Align repeated instances so the reader can compare their internal structure.
- Place important constraints beside the affected groups.
- Keep internal resource detail only when it explains the architecture.
- Define the target figure's abbreviations. Do not copy the source's small labels without a size check.

### Mooncake: workflow across resource boundaries

[Open Figure 3](https://www.usenix.org/system/files/fast25-qin.pdf#page=5).

The figure aligns two instances and separates their processor and memory regions.
Its labeled paths show distinct stages and asynchronous transfers.

- Use aligned regions when a transfer crosses similar resource types.
- Distinguish local work from cross-instance communication.
- Label stages where order matters.
- Preserve real failure and response paths when the target system has them.
- Use a separate lifecycle view when the question concerns decisions and outcomes.

### Ray: request and result workflows

[Open Figure 7](https://www.usenix.org/system/files/osdi18-moritz.pdf#page=9).
[Open the publication record](https://www.usenix.org/conference/osdi18/presentation/moritz).

The two panels keep the same component positions while they explain execution and result retrieval.
Numbered actions and different line styles distinguish the two kinds of communication.

- Preserve component positions across related workflow panels.
- Show the state or table entry that makes an important interaction possible.
- Distinguish control messages from data movement when that distinction matters.
- Replace source-code excerpts with short labels when the code adds no necessary information.
- Simplify crowded routes before you reduce text size.

### vLLM: data mapping

[Open Figure 6](https://arxiv.org/pdf/2309.06180v1#page=6).
[Open the authors' explanation](https://vllm-project.github.io/2023/06/20/vllm.html).

The figure connects logical blocks, an explicit translation table, and physical blocks.
Concrete contents make the mapping easier to verify than generic boxes alone.

- Use aligned rows or cells to explain a data transformation.
- Show an intermediate table when the table explains the relationship.
- Use small concrete examples when they clarify an interface or stored representation.
- Keep arrows attached to the exact cells that they connect.
- Use another reference for actors, deployment, or database cardinalities.

### SGLang: state changes across panels

[Open Figure 3](https://papers.nips.cc/paper_files/paper/2024/file/724be4472168f31ba1c9ac630f15dec8-Paper-Conference.pdf#page=5).

The numbered panels show successive states of one structure.
The repeated layout and visual markers distinguish new, retained, and removed content.

- Keep identifiers stable across successive states.
- Mark changes with labels or shapes as well as color.
- Select the states that explain the target question.
- Split the figure when a large panel set forces unreadable text.
- Use this reference for state comparison, not for a complete system overview.

## Selection and comparison

1. Choose one primary reference that matches the figure's question.
2. Choose supporting references only for specific design decisions.
3. Record each source, figure number, useful choice, and rejected choice.
4. Inspect the source images at comparable display widths.
5. Compare semantic coverage, hierarchy, grouping, notation, routes, and final-size text.
6. Record any material quality deficit before you accept the result.

The [Top-Conf Figure Gallery](https://qwdwqfwq.github.io/topconf-paper-figure-gallery/) remains a discovery source.
A conference label or acceptance tier does not establish figure quality.
Reject images with unreadable labels, arbitrary grouping, unclear arrows, or excessive crossings.
A large node count does not compensate for those defects.

The inspected Pagila schema image fails this selection because its crossings and small labels obscure relationships.
The simpler Ray architecture overview and DistServe runtime overview can support layout choices.
They do not replace a reference that covers the target figure's full question.

## Access and offline operation

Keep cached source pages and previews in a local, uncommitted directory.
Record the source URL and figure number beside each cached image.
Keep private reference images outside this distributed skill.
Link to public artwork unless its license permits redistribution.

Use an available cached reference when network access fails.
If no suitable reference is available, report that the visual comparison remains incomplete.
Keep the editable output, but withhold a claim that it meets the minimum quality.

The files under `assets/examples/` are basic renderer fixtures.
They test notation and compilation. They do not establish the minimum visual quality.
Use their source mechanics only after you select an appropriate reference composition.

## Method sources

[PaperBanana](https://github.com/dwzhu-pku/PaperBanana) supplies the planning, style, generation, and review workflow.
[FigureForge](https://github.com/qwdwqfwq/topconf-paper-figure-gallery/blob/main/README.en.md) supplies the example selection and analysis approach.
This skill applies those methods to verified repository structure and behavior.
