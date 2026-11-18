# Skill evaluations

Eval harness for the skills in this repo, modeled on Anthropic's
[Demystifying Evals for AI Agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents).

Functional trials and scoring use `codex exec` by default.
Triggering trials use Claude Code. Each command uses its existing login.
Use `--runner claude` when a functional trial must test the Claude plugin.
The scorer always uses Codex.

## Layers

| Layer        | What it asks                                                  | Grader                            |
| ------------ | ------------------------------------------------------------- | --------------------------------- |
| `triggering` | Does Claude pick the skill on right prompts, skip on wrong?   | Code (parse `Skill` tool calls).  |
| `functional` | Given the skill triggered, is the output good?                | Hybrid: code checks + LLM judge.  |

A regression layer (replay both with the skill disabled, lock the delta as a
baseline, fail CI on >10% drift) is the natural next step but is not yet built.

## Layout

```
evals/
  run.py
  skills/<skill>/
    triggering/
      should-trigger.jsonl       # ~10 prompts that MUST load the skill
      should-not-trigger.jsonl   # ~10 near-miss prompts that must NOT
    functional/
      fixtures/<case>/
        setup.sh                 # builds a fresh tmp git repo, prints its path
        task.json                # prompt + grader config + judge dimensions
        reference.md             # gold-standard reference (Anthropic: always ship one)
    judges/
      <dim>.md                   # one rubric per dimension; one judge call per dim
  results/                       # gitignored: per-trial transcripts + report.json
```

## Usage

```bash
# Triggering layer (cheap; ~20 prompts × 3 trials)
python3 evals/run.py triggering --skill pr-gen --trials 3 --parallel 4

# Functional layer (more expensive; runs the actual skill end-to-end)
python3 evals/run.py functional --skill pr-gen --trials 1
python3 evals/run.py functional --skill pr-gen --case feature-add-helper

# Keep a fixture dir around for debugging a failing case
KEEP_FIXTURE=1 python3 evals/run.py functional --case bugfix-with-test
```

Each run writes per-trial stream-json transcripts and a `report.json` summary
to `evals/results/<layer>/<skill>/<timestamp>/`.

A skill can also ship deterministic tests beside its fixtures. Run them with
`python3 -m unittest discover -s evals/skills/<skill>`. The
`sweep-gh-unread` tests replay a synthetic inbox through a stub `gh`.

A functional `task.json` can set `env` for the agent process. The value
`{fixture}` expands to the fixture path, for example to point `SWEEP_GH` at a
stub binary.

## How the harness stays hermetic

- Triggering trials run in `mktemp -d` so no project `CLAUDE.md` is auto-loaded.
- Codex trials receive the exact skill path from the requested plugin directory.
- Claude trials load the plugin through `--plugin-dir`.
- Codex processes ignore user configuration and disable apps and subagents.
- Claude processes disable external Model Context Protocol (MCP) servers.
- Codex uses ephemeral sessions. Claude disables session persistence.
- Functional fixtures are fresh tmp git repos rebuilt by `setup.sh` per trial;
  the harness deletes them after (override with `KEEP_FIXTURE=1`).

## How the LLM judge works

For each functional case, the harness starts a separate Codex process for each dimension in `task.json`.
The scorer uses read-only mode with shell access disabled.
The scorer receives image attachments and text artifacts directly.
A JSON Schema restricts the final response to the required score fields.

The judge sees the rubric, the original user prompt, the reference, and the
candidate output. It returns `{"score": 0|1, "reason": "...", "unknown": bool}`.
Each dimension is scored in isolation (Anthropic's recommendation: don't mix
dimensions in one judge call). The `unknown` escape hatch suppresses
hallucinated verdicts.

A case passes only when all code checks and judge dimensions pass.
Claude functional trials also require a successful Skill invocation.
Codex functional trials receive the exact skill path. They do not measure automatic skill selection.

## Adding a new skill

1. `evals/skills/<skill>/triggering/{should-trigger,should-not-trigger}.jsonl` —
   ~10 each. Be aggressive on near-misses; class imbalance distorts results
   (Anthropic: balance positive vs negative cases).
2. `evals/skills/<skill>/functional/fixtures/<case>/{setup.sh,task.json,reference.md}` —
   each `setup.sh` must print a fresh tmp dir on stdout. Hand-grade the first
   ~5 cases yourself before trusting the LLM judge.
3. `evals/skills/<skill>/judges/<dim>.md` per judge dimension named in `task.json`.
4. Run, read the first few transcripts, tune.

A file creation task sets `allow_writes` to `true`. Its setup script must create
a direct temporary directory with the `<skill>-eval-` prefix.

Use `required_artifacts` for deterministic file checks. Each item specifies a
relative `path`, an optional `format`, and optional text requirements.

## Calibration cadence

Hand-grade a sample (~20 cases) every quarter or after touching a rubric;
compare against judge verdicts. If agreement < 80%, fix the rubric, not the
skill.

## Anti-patterns this harness guards against

These come straight out of the Anthropic article — see code comments at the
referenced lines for enforcement:

- **0% pass rate ≠ bad skill.** Inspect the task and grader first. (Symptom:
  identical failures across all trials of a case → broken fixture or grader.)
- **Shared state across runs.** Each trial gets its own tmpdir + tmp git repo.
- **One-sided eval.** Negative cases are first-class — the summary reports
  positive and negative pass rates separately, not a single blended number.
- **Brittle path-checking.** Graders score the agent's *final output*, not
  which intermediate tools it called.
- **Mixed-dimension judge calls.** The scorer uses one Codex process per dimension.
- **Judge fabrication.** `"unknown": true` escape hatch in every rubric.

## Rendered figure evaluation

A task can set `artifact_checks` to command argument lists from trusted fixtures.
The harness expands `{repo}` and `{fixture}` in each argument.
The harness requires each command to return zero.
The harness saves each command's output beside the report.

A task can map judge dimensions to relative paths through `judge_artifacts`.
The harness retains those files beside the report.
The scorer receives images as attachments and text artifacts inside its prompt.
A missing artifact fails the dimension with an unknown result.
Scorers use read-only mode with shell access disabled.

The functional command accepts `--plugin-dir` for a frozen baseline plugin.
The functional report includes pass^k and pass@k across cases.
Read [the architecture evaluation](skills/visualize-arch/evaluation.md) for figure-specific checks.

## Model selection

Use `--runner-model` and `--judge-model` to select Codex models explicitly.
The default uses the Codex command's default model.
The report records both selections and every scorer transcript.
The report leaves monetary cost unavailable when Codex does not supply it.

```bash
python3 evals/run.py functional --skill visualize-arch --case create-service-diagram --trials 3
```

The Codex adapter follows the [official CLI guidance](https://developers.openai.com/codex/non-interactive-mode) for structured output.

## Visual reference comparisons

Tasks with visual references use `visual_references` and `reference_width_mm` in task.json.
Each reference specifies a relative image path and a label.
The `--reference-dir` option identifies the local cache.
The harness gives the same reference images to the generator and comparison scorer.
The harness freezes each reference before generation.

The harness records each reference's Secure Hash Algorithm 256 (SHA-256) hash.
The scorer receives candidates first and references last.
The first reference sets the minimum quality.

The harness normalizes reference width to match the candidate's final display width.
The harness retains the original references, normalized references, source files, and requested outputs beside the report.
Private images remain in the local cache and ignored result directories.
Pillow supplies image normalization. Poppler supplies document rendering.

```bash
python3 evals/skills/visualize-arch/prepare_references.py --output .context/visual-quality-eval/references
python3 evals/run.py functional --skill visualize-arch --case reference-system --trials 3 --reference-dir .context/visual-quality-eval/references
```

The preparation command uses the existing GitHub login for authorized Kriterion access.
The command pins the Kriterion revision and records the public paper sources.

### Optional GLM scorer

Codex remains the default scorer.
Use GLM when the user selects it or authorizes it as a fallback.
The GLM scorer uses the existing `OPENROUTER_API_KEY` environment variable.
The default GLM model is `z-ai/glm-4.6v`. This model accepts image input.
For `visualize-arch`, Codex always scores correctness and reference quality.
GLM scores the other dimensions when the user selects the GLM backend.
Codex uses its default model for those two dimensions.

The scorer sends the task, reference solution, source artifacts, and images to OpenRouter.
The scorer sends no shell tools. The scorer validates each returned score locally.
The transcript stores the provider response and token use. The transcript contains no API key.

A provider error produces an unavailable result. A provider error never produces a passing score.

Keep scores from different providers separate. Run the comparison controls for each provider.
Use known failed candidates as controls.
Require another scorer when a provider accepts a known failure.

```bash
python3 evals/run.py functional --skill visualize-arch --case reference-recovery --trials 3 --reference-dir .context/visual-quality-eval/references --judge-backend glm
```

The implementation uses OpenRouter's [image input](https://openrouter.ai/docs/guides/overview/multimodal/image-understanding) and [structured response](https://openrouter.ai/docs/guides/features/structured-outputs) formats.

The figure checker supplies verified font measurements to the visual scorers.
The scorers assess visual legibility separately from numeric point sizes.
Codex generation for `visualize-arch` permits read-only reviewer agents.
Scorer processes still have no shell or agent tools.
