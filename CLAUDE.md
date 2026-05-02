# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A collection of agent skills for software-development tasks, distributed two ways
from the same source tree:

- As a **Claude Code plugin** via `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` (`/plugin marketplace add SebastianElvis/dev-skills`).
- As **plain skills** consumable by any agent supporting the [agentskills.io](https://agentskills.io) format via `npx skills add SebastianElvis/dev-skills`.

Both ecosystems read from `skills/<name>/SKILL.md`. There is no build step, no tests, and no runtime — this repo ships Markdown.

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

## Authoring rules — agentskills.io spec, Anthropic guide & best practices

Every skill in `skills/` must conform to the [agentskills.io specification](https://agentskills.io/specification) and the [Complete Guide to Building Skills for Claude](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf). The rules below are load-bearing — Codex review and CI tooling will flag violations.

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

| Layer            | Goal                              | What to run |
| ---------------- | --------------------------------- | ----------- |
| Triggering       | Loads on the right prompts, skips the wrong ones. | 8–10 should-trigger + 8–10 near-miss should-not-trigger queries; run each 3–5×; pass threshold ≈ 0.5. |
| Functional       | Produces correct output.          | Realistic scenarios; assert outputs, API calls, error handling, edge cases. |
| Performance      | Beats the no-skill baseline.      | Compare tool calls, retries, tokens, back-and-forth message count with vs. without the skill. |

Split eval queries into ~60% train / ~40% validation to avoid overfitting the description to specific phrasings.

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
