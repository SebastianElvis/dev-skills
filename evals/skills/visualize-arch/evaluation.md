# Architecture figure evaluation

## Sources and scope

The four visual dimensions follow the concepts in
[PaperBanana's diagram evaluation](https://github.com/dwzhu-pku/PaperBanana/blob/main/prompts/diagram_eval_prompts.py).
The rubrics use original wording for repository architecture figures.
They do not reproduce PaperBananaBench or claim comparable scores.

The reference selection follows
[FigureForge's example analysis](https://github.com/qwdwqfwq/topconf-paper-figure-gallery/blob/main/README.en.md).
Its retrieval tests measure reference search, not the quality of a generated architecture figure.
This evaluation therefore inspects the output images directly.

The evaluation design follows
[Anthropic's evaluation guidance](https://www.anthropic.com/research/demystifying-evals-for-ai-agents).

## Cases

| Case | Split | Reference facts | Main condition |
| --- | --- | --- | --- |
| create-service-diagram | Train | Adjacent reference.md | The set separates a system overview from ordered behavior. |
| schema-optional-owner | Train | Adjacent reference.md | The schema preserves optional ownership and cardinalities. |
| refresh-worker-flow | Validation | Adjacent reference.md | The update preserves the build process and both outcomes. |

Each trial uses a fresh temporary repository.
The validation case checks transfer to an existing diagram.
Do not tune the skill to validation output. Add a new validation case after any such correction.

## Checks

- The harness verifies the requested source and vector files.
- The independent checker measures text at the requested final width.
- The checker renders color and grayscale previews from the actual Portable Document Format (PDF) output.
- Separate judges inspect faithfulness, readability, conciseness, and aesthetics.
- The faithfulness judge receives the original repository evidence, editable source, and rendered figures.
- The visual judges receive rendered figures rather than the agent's claims.
- Each judge can return `unknown: true`. An unknown result does not pass.
- The response judge checks the output paths and completed checks.

The harness retains judge artifacts beside the report.
The agent's self-review does not determine the evaluation score.

## Commands

Run the deterministic checks first:

```bash
python3 -m unittest discover -s evals/skills/visualize-arch
```

Run one difficult case before the full evaluation:

```bash
python3 evals/run.py functional --skill visualize-arch --case create-service-diagram
```

Run a basic regression case repeatedly:

```bash
python3 evals/run.py functional --skill visualize-arch --case create-service-diagram --trials 3
```

Use a frozen plugin directory to compare the previous skill:

```bash
python3 evals/run.py functional --skill visualize-arch --trials 3 --plugin-dir /absolute/path/to/frozen-plugin
```

Use identical cases, models, dimensions, and trial counts for a controlled comparison.
Compare per-dimension pass rates, pass^k, pass@k, tool calls, tokens, duration, and cost.
Count revision rounds from the retained transcripts.
Do not infer a performance improvement from different trial counts.

## Acceptance and calibration

Require every deterministic check and every judge dimension to pass each trial.
Target pass^3 of 1.0 on this small suite before release.
This target measures local consistency, not general publication quality.

Read the first 20 available trial transcripts and their rendered figures manually.
Record separate manual decisions for all four dimensions.
Require at least 80 percent agreement before you trust automatic visual scores.
Use known defective figures to check that a judge rejects wrong arrows, small text, and unreadable routes.
Preserve a correct simple figure as a positive control.

Inspect fixtures and rubrics before you change the skill after a repeated failure.
Report unknown results, unavailable tools, skipped trials, and uncalibrated judges separately.

## Validation record: 2026-11-17

Codex generated and scored three trials for each case.

| Case | Passed trials | Result |
| --- | --- | --- |
| create-service-diagram | 3/3 | Pass |
| schema-optional-owner | 3/3 | Pass |
| refresh-worker-flow | 3/3 | Pass |

All nine trials pass the deterministic checks and all five judge dimensions.
The four visual dimensions each pass 9/9 trials. The handoff dimension passes 9/9 trials.
The suite has pass^3 of 1.0 and pass@3 of 1.0.

The 12 architecture tests pass. The 9 notification tests pass.
The existing PR generation case passes with Codex generation and scoring.
Both skill validators accept the revised skill.
The three bundled examples compile and pass final-size checks.

The scorer passes four positive and negative controls for faithfulness and handoff.
These controls do not replace human calibration of all visual dimensions.
The suite contains three local cases. It does not establish performance on PaperBananaBench.
The run does not measure automatic skill triggering.

The early runs found an ambiguous Makefile path and incomplete evidence for the scorer.
The corrected fixture names the requested Makefile path explicitly.
The corrected scorer receives original code, schema, and configuration alongside the reference summary.
The handoff rubric requires source and vector paths. A separate Makefile link is optional.
The original reports and prior verdicts remain available beside the corrected reports.

## Codex scoring

Codex generates each candidate from the specified skill path.
A separate read-only Codex process scores each dimension.
The scorer receives actual preview images as attachments.
The scorer receives editable source as text for the faithfulness check.
The scorer uses a JSON Schema for its result.
The harness rejects malformed scores and unknown results.

Use `--judge-model` to select the scorer model explicitly.
Use `--runner-model` to select the generation model explicitly.
Claude plugin triggering remains a separate evaluation.

## Reference standard update: 2026-11-17

The user sets Kriterion's documentation figures as the minimum visual quality.
The revised catalog adds inspected public references from Mooncake, Ray, vLLM, and SGLang.
The original examples under `assets/examples/` serve only as renderer fixtures.

The earlier 9/9 result measures the earlier functional requirements.
Those scores do not establish compliance with this new visual minimum.
A future quality evaluation must give the scorer the selected reference images for direct comparison.
The evaluator must use comparable figure types and display widths.

## Direct comparison suite

The stronger suite uses a separate dispatch platform with executable source and nine related database tables.
A separate import workflow supplied validation before its failures informed the skill.

| Case | Split | Main condition |
| --- | --- | --- |
| reference-system | Demonstration / regression | The figure covers multiple actors, grouped components, queues, shared storage, and external services. |
| reference-schema | Train | The figure organizes nine tables with complete relationships, cardinalities, and important constraints. |
| reference-lifecycle | Train after the first evaluation | The figure separates intake errors, bounded retries, stored outcomes, manual retry, and asynchronous notices. |

| reference-recovery | Train after the confirmation check | The figure covers credential-dependent resume, bounded backoff, cancellation, retained history, and independent indexing. |
| reference-paper-schema | Demonstration / regression | The complete nine-table schema fits 180 mm width with at least 8 pt text. |
| reference-publish | Demonstration / regression | The figure preserves approval checks, event writes, bounded retries, cancellation, and independent publication. |

The source fixture tests success, timeouts, manual retry, provider rejection, and intake errors.
The recovery fixture tests resume, retained history, backoff limits, cancellation, quarantine, and indexing failures.
The generator receives the selected reference images before it defines the style.
A separate `reference-quality` scorer compares the actual result with those images.
All six dimensions must pass. The earlier three cases remain basic regression tests.

Prepare the authorized reference cache:

```bash
python3 evals/skills/visualize-arch/prepare_references.py --output .context/visual-quality-eval/references
```

Run each stronger case three times:

```bash
python3 evals/run.py functional --skill visualize-arch --case reference-system --trials 3 --reference-dir .context/visual-quality-eval/references
python3 evals/run.py functional --skill visualize-arch --case reference-schema --trials 3 --reference-dir .context/visual-quality-eval/references
python3 evals/run.py functional --skill visualize-arch --case reference-lifecycle --trials 3 --reference-dir .context/visual-quality-eval/references
python3 evals/run.py functional --skill visualize-arch --case reference-recovery --trials 3 --reference-dir .context/visual-quality-eval/references
python3 evals/run.py functional --skill visualize-arch --case reference-paper-schema --trials 3 --reference-dir .context/visual-quality-eval/references
```

The first image reference sets the Kriterion minimum.
The architecture case also receives Mooncake's architecture figure.
The lifecycle case also receives Ray's request and result figure.
The schema case uses Kriterion's data model directly.

The harness freezes reference images before generation and records their hashes.
The scorer receives those references at the same display width as the generated image.
The report preserves failed attempts and unavailable comparisons.
A weak example must fail the comparison control before the suite can establish a quality result.

## Correction record

The architecture pilot omitted the scope of authorization checks.
The skill now records checked operations and meaningful exceptions.

The initial lifecycle evaluation omitted the permanent sequence for attempt history.
The skill now separates reset counters from retained identifiers, sequence numbers, and history.
The lifecycle case now belongs to training because its failure informed that correction.
The separate recovery case supplied validation for that phase.

The third schema trial replaced some required relationship routes with notes.
The skill now requires a visible route for each in-scope foreign key.
The scorer rubrics remain unchanged after the comparison controls.

The scorer returns an unavailable result when Codex reports a provider error.
The evaluator preserves the original transcript.
A scoring retry uses the same candidate artifacts and scorer rules.
A scoring retry never replaces a known failure.
The report states each incomplete trial separately.

## GLM calibration limit

GLM passes the broad controls but misses two real failed candidates.
GLM accepts a schema that replaces required routes with notes.
GLM also accepts a lifecycle that omits retained sequence behavior.
The evaluation therefore treats those GLM dimensions as provisional.
Codex must confirm correctness and reference quality for each final candidate.
The evaluator keeps the GLM responses and Codex confirmations separate.
The evaluator never replaces a known candidate failure with a different scorer's passing result.

The Codex confirmation found omitted intake and cancellation events in one recovery trial.
The skill now records event writes for each in-scope operation.
The recovery case now belongs to training. The paper-width case supplied validation before the bundle exposed its source facts.

## Measurement audit and correction loop

An independent PyMuPDF audit measures 8.47 pt labels in the first two release figures.
The original visual verdicts incorrectly claim text below 8 pt.
The audit preserves the original verdicts and the later disagreements.
The evaluation never selects a later passing verdict for an unchanged candidate.

The final scorer receives verified PDF font measurements.
The PDF checker uses a larger extraction scale to reduce rounding error.
The scorer checks visual legibility separately from numeric font size.
The rubric still requires at least 8 pt text and the same visual minimum.

The correction loop gives each failed candidate its review findings.
The agent edits the existing figure within the same task.
Separate Codex reviewers check correctness and visual quality.
The evaluator then scores the corrected output with the unchanged rubrics.
The loop permits three correction rounds. The report keeps every round.
The report separates first-pass results from results after correction.

## Results from 2026-11-17

The latest case cohorts contain 15 trials across five cases.
The first-pass scores total 11/15. The scores after review total 15/15.
The table combines case cohorts from successive frozen skill versions.
The results measure completion after review. They do not establish one-pass consistency for one final frozen version.

| Case | First pass | After review |
| --- | --- | --- |
| System architecture | 3/3 | 3/3 |
| Complete schema at 300 mm | 3/3 | 3/3 |
| Complete schema at 180 mm | 3/3 | 3/3 |
| Import recovery | 2/3 | 3/3 |
| Independent release workflow | 0/3 | 3/3 |

The four flagged candidates need one or two correction rounds.
The final verification scores all four corrected candidates against the canonical task.
The generator alone receives prior review findings. The scorer receives no correction feedback.
The report preserves the original failures, measurement disagreements, and every correction round.

Codex scores correctness and reference quality. GLM scores the other four dimensions in the follow-up cases.
The earlier architecture cohort uses Codex for all six dimensions.
The deterministic checks verify artifact formats, font size, bounds, and unchanged application files.
All 41 local tests pass. The skill validator passes.

The first-pass pass@3 is 80%. The first-pass pass^3 is 60%.
Both metrics reach 100% after review for these five case cohorts.
The evaluator does not claim official PaperBanana or FigureForge benchmark scores.
The evaluator does not measure trigger accuracy or improvement over a no-skill performance baseline.
The small control sets do not replace expert calibration on 20 transcripts.

The local report is `.context/visual-quality-eval/report.md`.
The machine-readable report is `.context/visual-quality-eval/report.json`.
The ignored result directories retain source files, vector files, previews, and scorer transcripts.

## Bundled demonstrations from 2026-11-18

The skill now bundles three worked examples from the reviewed source figures.
The bundle includes synthetic source evidence, editable figures, vector outputs, and previews.
The architecture comes from `reference-system`.
The schema comes from `reference-paper-schema`. The workflow comes from `reference-publish`.
Those cases now serve as demonstrations and regression tests.
The shared dispatch cases also expose the same source facts.

Future validation must use unseen source facts and figure requirements.
An agent can read the bundled answers, so these cases cannot measure independent generalization.
The historical scores above predate this bundle.
The packaging check rebuilds each figure and verifies text size and bounds.
The packaging check also inspects color and grayscale previews.
This update adds no new model evaluation score.
