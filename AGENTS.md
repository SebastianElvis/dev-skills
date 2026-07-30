# AGENTS.md

Guidance for any coding agent that works in this repository. This file is the single source of
truth. `CLAUDE.md` is a symlink to it, so Claude Code reads the same rules.

**Read the [writing style](#writing-style--asd-ste100-simplified-technical-english) section before
you write any prose.** It applies to every file here, and to the text that a skill tells an agent
to produce at run time.

## What this repo is

A collection of agent skills for software-development tasks, distributed two ways
from the same source tree:

- As a **Claude Code plugin** via `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` (`/plugin marketplace add SebastianElvis/dev-skills`).
- As **plain skills** consumable by any agent supporting the [agentskills.io](https://agentskills.io) format via `npx skills add SebastianElvis/dev-skills`.

Both ecosystems read from `skills/<name>/SKILL.md`. There is no build step and no runtime — this repo ships Markdown. The `evals/` directory holds an optional skill-evaluation harness (see [Running the eval harness](#running-the-eval-harness)).

## Layout

```
.claude-plugin/plugin.json       # Claude Code plugin manifest
.claude-plugin/marketplace.json  # Claude Code marketplace entry
skills/<name>/SKILL.md           # Skill entry point — frontmatter + body
skills/<name>/references/        # On-demand reference docs
skills/<name>/assets/            # Templates and static resources
skills/<name>/scripts/           # Optional executable code
```

When adding a new skill, the standard scaffold is `cd skills && npx skills init <skill-name>`, then edit the resulting `SKILL.md` and add a row to the README's Skills table.

## Writing style — ASD-STE100 Simplified Technical English

**All English in this repository uses ASD-STE100 Simplified Technical English. There is no
exception.**

This applies to two things:

1. **Repository prose** — `SKILL.md` bodies, `references/`, `assets/`, `README.md`, eval docs,
   code comments, commit messages, and PR descriptions.
2. **Text that a skill tells an agent to produce at run time** — review comments, checkpoint
   questions, report bodies, and any other user-facing output. A skill must instruct the agent
   to write its output in Simplified Technical English, and its templates and examples must
   already obey the rules.

ASD-STE100 is the aerospace and defence standard for technical documentation. It has two parts:
a dictionary of approved words, and a set of writing rules. Full dictionary conformance needs the
licensed word list, which this repository does not ship. **Conform to the writing rules and to the
controlled vocabulary below.** That is the standard here, and it is checkable in review.

### Sentence rules

- **Procedural sentences: 20 words maximum. Descriptive sentences: 25 words maximum.**
- **One instruction per sentence.** Do not join two instructions with "and".
- **Use the active voice.** Name the actor. Write "the agent reads the issue", not "the issue is
  read".
- **Use simple tenses only** — simple present, simple past, simple future. Do not use the perfect
  or the progressive tenses.
- **Do not use `-ing` forms as verbs.** Write "when you review the diff", not "when reviewing the
  diff". An `-ing` word is acceptable only as part of an established technical name, such as
  "rolling deploy".
- **Write positively.** Do not use a double negative.
- **Keep to one topic per paragraph, six sentences maximum.** Put the topic sentence first.

### Word rules

- **One word, one meaning. One meaning, one word.** Choose a term and repeat it. Never vary a
  term for style. If a document says "finding", it says "finding" every time — not "issue",
  "observation", or "concern".
- **Use articles.** Write "read the file", not "read file".
- **Noun clusters: three words maximum.** Break up "review comment quality bar" into "the quality
  bar for a review comment".
- **Do not use an idiom, a metaphor, or slang.** This rule removes most of the vivid phrasing that
  technical writers reach for. It is the rule that this repository breaks most often.
- **Define an abbreviation at its first use** in each file. `PR` and `LOC` are exceptions; they
  are established technical names.

### Controlled vocabulary

Use the left column. Do not use the right column.

| Use | Do not use |
| --- | --- |
| symptomatic fix | band-aid, patch job, quick fix |
| fix depth, root-cause level | altitude |
| review pass, check | lens |
| split point | seam |
| bias check | anchoring guard |
| affected code, dependent code | blast radius |
| threshold | knee, inflection point |
| test, condition, requirement | gate, bar, hurdle |
| examine, test | probe, interrogate, drill into |
| low-quality contribution | slop |
| find, identify | surface, unearth, tease out |
| large, many | massive, huge, a ton of |
| important, necessary | load-bearing, critical path |
| show, cause | drive, unlock |

Add a row when a review finds a new metaphor. The table is the record of decisions, not a
suggestion.

**Technical names are permitted and are not metaphors.** "State machine", "trust boundary",
"pull request", "rolling deploy", "changelist", "root cause", "regression", and "race condition"
are the accepted names for the things they name. Keep them.

### Writing a skill that produces conformant output

A skill's own instructions are not enough. Do all three:

1. State the requirement in `SKILL.md`, in the section that describes the output.
2. Write every template and every worked example in Simplified Technical English. An agent copies
   the example, so a non-conformant example defeats the instruction.
3. Add a line to the skill's final checklist that tests the output.

### Checking conformance

There is no linter for this. Check by reading, and check these five first — they catch most
violations:

1. Sentence length above 20 words.
2. An `-ing` form used as a verb.
3. A metaphor from the table above.
4. Two names used for one concept in the same file.
5. The passive voice where an actor exists.

## Authoring rules — agentskills.io spec, Anthropic guide & best practices

Every skill in `skills/` must conform to the [agentskills.io specification](https://agentskills.io/specification) and the [Complete Guide to Building Skills for Claude](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf). Codex review and CI tooling flag a violation of the rules below.

### Three-level progressive disclosure (Anthropic terminology)

| Level | What loads                  | When                                   |
| ----- | --------------------------- | -------------------------------------- |
| 1     | YAML frontmatter (~100 tok) | Always, in Claude's system prompt.     |
| 2     | SKILL.md body               | When Claude decides the skill is relevant. |
| 3     | Files under `references/` / `scripts/` / `assets/` | Only when SKILL.md tells Claude to load them. |

Each level should hand off enough information for Claude to decide whether to descend to the next.

### `SKILL.md` frontmatter

| Field           | Required | Constraints |
| --------------- | -------- | ----------- |
| `name`          | yes      | ≤64 chars, lowercase `a-z` and `-`, no leading/trailing or consecutive hyphens, **must match the parent directory name**. |
| `description`   | yes      | ≤1024 chars. Imperative-trigger style ("Use when…"), describes both *what* and *when*. |
| `license`       | no       | License name or reference to a bundled file. |
| `compatibility` | no       | ≤500 chars. Include only when the skill has real environment requirements (binaries, network, runtime). |
| `metadata`      | no       | Free key-value map. |
| `allowed-tools` | no       | Space-separated pre-approved tools (experimental). |

#### Frontmatter forbidden values (security)

The frontmatter is injected into Claude's system prompt, so it is an injection surface. The Anthropic guide hard-bans:

- **XML angle brackets** (`<` `>`) anywhere in any field — would leak into the prompt structure.
- **Skill names starting with `claude` or `anthropic`** — reserved.
- **Code execution in YAML** — only safe YAML parsing is supported; tags like `!!python/object` will be rejected.

### Description quality (the trigger surface)

The description is the only thing loaded at startup, so it carries the entire burden of triggering. When writing or editing one:

- Imperative phrasing: "Use this skill when…", not "This skill does…".
- Focus on user intent, not implementation. Describe what the user is trying to achieve.
- Err pushy on triggers — list multiple realistic phrasings, including ones where the user does not name the domain directly.
- Mention **relevant file types and concrete trigger phrases** users would actually say (`.csv`, `Dockerfile`, "draft a PR", "summarize this branch").
- State explicit non-uses inline as **negative triggers** ("Do NOT use for X — use Y instead") to suppress false positives.
- Anthropic's recommended structure: `[What it does] + [When to use it] + [Key capabilities / negative triggers]`.
- Stay concise. A few sentences is right; do not pad to fill the 1024-char budget.

**Debugging trick:** ask Claude "When would you use the `<skill-name>` skill?" — it will quote the description back, exposing what is actually triggering and what is missing.

### Body content (`SKILL.md` after frontmatter)

- **Add what the agent lacks; omit what it knows.** Do not explain what a PDF / HTTP / git is. Project-specific conventions, non-obvious edge cases, particular tools/APIs.
- **Provide defaults, not menus.** Pick one approach and mention alternatives briefly. "Use pdfplumber" beats "you can use pypdf, pdfplumber, PyMuPDF, or pdf2image".
- **Procedures over declarations.** Teach an approach to a class of problems, not the answer to one instance.
- **Calibrate prescriptiveness to fragility.** Free-form steps for flexible tasks; exact commands and "do not modify" for fragile ones.
- **Gotchas section** for environment-specific facts that defy reasonable assumptions. When you have to correct an agent mistake while iterating, add it here.
- **Length target: under 500 lines / 5,000 tokens (≈5,000 words per Anthropic's guide).** Past that, move detail into `references/` and tell the agent *when* to load each file ("Read `references/api-errors.md` if the API returns non-200" — not a generic "see references/").
- **Surface critical instructions with `## Important` or `## Critical` headers**, or a `CRITICAL:` prefix on a step. Buried instructions get skipped.
- **Prefer scripts to prose for fragile validation.** "Code is deterministic; language interpretation isn't" — bundle a `scripts/validate.py` and have SKILL.md run it, rather than asking Claude to re-derive the check each call.

### Directory conventions

- `references/` — on-demand documentation. Keep individual files focused; the agent loads them only when SKILL.md tells it to.
- `assets/` — templates, static data, images.
- `scripts/` — executable code; self-contained or document dependencies.
- **No `README.md` inside the skill folder.** Anthropic's guide forbids it — all documentation lives in `SKILL.md` or `references/`. The repo-level README at the root of this monorepo is fine and intended for human visitors; per-skill READMEs are not.

These names are conventions, not hard requirements, but use them — Codex review treats deviations as a smell.

### Templates

Templates exist to lock in **output format**, not to enumerate every possible section.

- Required sections only — make optional sections explicitly optional with rules for when to include them.
- Do not include sections the agent will fill with platitudes (generic "Security Considerations", "Performance Impact", "Cost Impact", "Architecture diagrams"). If the writer has nothing specific to say, the section should not be there.
- Templates must not contradict SKILL.md. If SKILL.md says "15–30 line PR descriptions", a 160-line template is a bug.
- No nested triple-backtick fences inside outer `` ```markdown `` blocks — they terminate the outer fence on render. Use indentation or a different language tag.
- Do not include "Generated with Claude" / `Co-Authored-By: Claude` footers in user-facing output (PR bodies, issue bodies, etc.) unless the user asked for it.

### Validation

Use `skills-ref validate ./skills/<name>` to lint frontmatter and naming. Run it before opening a PR.

## Authoring workflow

1. **Pick a use case before writing.** Anthropic's guide recommends defining 2–3 concrete use cases with explicit triggers and steps before drafting any Markdown. Skills fall into three categories: document/asset creation, workflow automation, MCP enhancement.
2. **Iterate on a single hard task first.** Solve one challenging instance in a regular Claude conversation, capture corrections and the winning sequence, *then* extract it into a skill. Leverages in-context learning; gives faster signal than testing across many cases up front.
3. **Use `skill-creator`** in Claude Code or Claude.ai to generate the first draft and frontmatter, then revise.
4. **Update the version field in `metadata`** when shipping a behavioral change so users on auto-update can tell what shifted.

## Testing skills (three layers)

The canonical reference for everything in this section is Anthropic's
[Demystifying Evals for AI Agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents).
Read it before you design or change a skill eval. Every
important recommendation below comes from it.

| Layer            | Goal                              | What to run |
| ---------------- | --------------------------------- | ----------- |
| Triggering       | Loads on the right prompts, skips the wrong ones. | 8–10 should-trigger + 8–10 near-miss should-not-trigger queries; run each 3–5×; pass threshold ≈ 0.5. |
| Functional       | Produces correct output.          | Realistic scenarios; assert outputs, API calls, error handling, edge cases. |
| Performance      | Beats the no-skill baseline.      | Compare tool calls, retries, tokens, back-and-forth message count with vs. without the skill. |

Split eval queries into ~60% train / ~40% validation to avoid overfitting the description to specific phrasings.

### Eval design principles (from the article)

When **adding cases or tuning rubrics**, prioritize these — they are what make
evals trustworthy rather than vanity metrics:

- **Always ship a reference solution per task.** "Two domain experts would
  independently reach the same pass/fail verdict" is the quality bar. If a
  task lacks a reference, the grader is guessing.
- **Multiple trials per task.** Run each case 3–5× — model output varies. Score
  both **pass^k** (all trials correct, for consistency-critical behavior) and
  **pass@k** (≥1 correct, for capability checks). They diverge fast.
- **Balance positive and negative cases.** A skill that only has should-trigger
  prompts will be tuned into over-triggering. Always include should-NOT-trigger
  near-misses, and report positive vs negative pass rates separately.
- **Hybrid graders.** Prefer deterministic code checks where possible
  (substring presence, length bounds, structural assertions). Fall back to
  LLM-as-judge for anything fuzzy. Pure LLM judging is the last resort.
- **One judge call per dimension.** Don't ask one judge to score multiple
  dimensions at once — it conflates them. Faithfulness, structure, and
  signal-to-noise each get their own `claude -p` invocation.
- **Give every judge an "Unknown" escape hatch** — `{"score": 0|1, "unknown":
  bool}`. Suppresses hallucinated verdicts on ambiguous cases.
- **Read transcripts by hand for the first ~20 runs.** "You won't know if your
  graders work unless you read transcripts." Trust the LLM judge only after
  it agrees with you on a hand-graded sample (target ≥80% agreement).
- **0% pass rate ≠ broken skill.** Identical failures across all trials of a
  case usually mean the fixture or grader is broken. Inspect those before
  changing the skill.
- **Isolate environments per trial.** Shared state (leftover files, caches,
  git state) inflates apparent performance via correlated failures. Each
  trial gets its own tmpdir.
- **Don't grade the path, grade the output.** Pinning to a specific tool-call
  sequence penalizes valid alternative approaches. Grade the agent's final
  output (the PR title/body, the generated file) — not which tools it called
  to get there. (The exception: triggering-layer evals genuinely *do* care
  whether the Skill tool got invoked, so for those, tool-call detection is
  the correct signal.)

### Running the eval harness

The repo ships a working harness for the triggering and functional layers under
`evals/`. Both the runner and the LLM judge shell out to `claude -p`, so no
API key is required.

```bash
# Triggering: ~20 prompts × 2 trials, ~$3, ~3 min
python3 evals/run.py triggering --skill pr-gen --trials 2 --parallel 6

# Functional: real git fixtures, end-to-end, ~$0.30 / fixture
python3 evals/run.py functional --skill pr-gen
python3 evals/run.py functional --skill pr-gen --case feature-add-helper
KEEP_FIXTURE=1 python3 evals/run.py functional --case bugfix-with-test  # debug a failure
```

Reports land in `evals/results/<layer>/<skill>/<timestamp>/report.json`
(gitignored). Per-trial stream-json transcripts sit alongside.

When adding a new skill, scaffold `evals/skills/<skill>/{triggering,functional,judges}/`
following the `pr-gen` example. See [evals/README.md](evals/README.md) for
hermeticity choices, judge isolation, and the anti-patterns the harness guards
against (all from the [Anthropic evals article](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)).

## Common failure modes (from the Anthropic guide)

- **Skill won't upload** — usually `SKILL.md` is misnamed (must be exact case) or the folder name has spaces/capitals/underscores (must be kebab-case).
- **Skill never triggers** — description too vague or missing the user-intent phrasings. Fix the description, not the body.
- **Skill triggers on irrelevant queries** — add negative triggers (`Do NOT use for…`), be more specific about scope.
- **Loaded but instructions ignored** — instructions too verbose, buried below preamble, or ambiguous. Move critical steps to the top, gate them with `CRITICAL:`, replace prose with concrete bullets/commands.
- **Model laziness on long workflows** — add a short `## Performance Notes` block ("Take your time", "Quality over speed", "Do not skip validation steps"). Most effective in user prompts, but works as a SKILL.md hedge.
- **Slow / degraded responses** — too much loaded context. Either the SKILL.md is over 5,000 words (move detail to `references/`) or there are 20–50+ skills enabled simultaneously.

## Common workflow

```bash
# Lint a skill
npx skills-ref validate ./skills/pr-gen

# Add a new skill scaffold
cd skills && npx skills init my-skill

# Local plugin smoke-test from inside Claude Code
/plugin marketplace add /absolute/path/to/this/repo
/plugin install dev-skills
```
