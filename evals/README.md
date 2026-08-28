# Skill evaluations

Eval harness for the skills in this repo, modeled on Anthropic's
[Demystifying Evals for AI Agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents).

Both the runner and the LLM judge shell out to `claude -p` (headless mode), so
no API key is required — the eval uses whatever auth `claude` already has.

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

## How the harness stays hermetic

- Triggering trials run in `mktemp -d` so no project `CLAUDE.md` is auto-loaded.
- The plugin under test loads via `--plugin-dir <repo-root>`; we don't depend on
  the developer having installed it.
- MCP servers are stripped (`--strict-mcp-config --mcp-config '{...:{}}'`) to
  cut tens of thousands of init tokens and hide unrelated tools from the agent.
- `--no-session-persistence` keeps each trial isolated.
- Functional fixtures are fresh tmp git repos rebuilt by `setup.sh` per trial;
  the harness deletes them after (override with `KEEP_FIXTURE=1`).

## How the LLM judge works

For each functional case, the harness invokes a separate `claude -p` per
*dimension* listed in `task.json`:

```python
claude -p "<judge prompt>" \
  --system-prompt "You are a strict, calibrated evaluator. Reply with strict JSON only." \
  --tools "" --max-turns 1
```

The judge sees the rubric, the original user prompt, the reference, and the
candidate output. It returns `{"score": 0|1, "reason": "...", "unknown": bool}`.
Each dimension is scored in isolation (Anthropic's recommendation: don't mix
dimensions in one judge call). The `unknown` escape hatch suppresses
hallucinated verdicts.

A case passes only if: `triggered ∧ all-code-checks ∧ all-judges == 1`.

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
- **Mixed-dimension judge calls.** One `claude -p` invocation per dimension.
- **Judge fabrication.** `"unknown": true` escape hatch in every rubric.
