# dev-skills

A collection of general software-development agent skills. Installable via
either the [Vercel Labs `skills` CLI](https://github.com/vercel-labs/skills) or
[Claude Code's built-in plugin system](https://code.claude.com/docs/en/plugins).

## Install

### Via Claude Code (recommended for Claude Code users)

```bash
# Add this repo as a plugin marketplace, then install
/plugin marketplace add SebastianElvis/dev-skills
/plugin install dev-skills@dev-skills
```

After installing, run `/reload-plugins` to activate. Skills are namespaced
under the plugin name, e.g. invoke `pr-gen` as `/dev-skills:pr-gen`. You can
also browse and manage installed plugins via the `/plugin` interactive menu.

### Via the `skills` CLI (works with any agent)

```bash
# All skills in this repo
npx skills add SebastianElvis/dev-skills

# Just one skill
npx skills add SebastianElvis/dev-skills --skill pr-gen

# Global install (all projects)
npx skills add SebastianElvis/dev-skills -g
```

Works with Claude Code, Codex, Cursor, OpenCode, and every other agent the
`skills` CLI supports.

## Skills

| Skill | What it does |
| --- | --- |
| [`pr-gen`](skills/pr-gen) | Generate or update a GitHub PR title and description from the actual code changes on the current branch. |
| [`pr-review`](skills/pr-review) | The agent reviews the problem, specification, architecture, necessity, root cause, correctness, security, and project rules. It checks security at each stage. It asks for human confirmation before each later stage. |
| [`sweep-gh-unread`](skills/sweep-gh-unread) | Classify each GitHub notification thread, ask for confirmation, mark the threads without an open action as done, and list the action items. |
| [`visualize-arch`](skills/visualize-arch) | Create verified architecture figures with reference examples, editable sources, and visual checks. [Worked examples](skills/visualize-arch/references/worked-examples.md). |

## Layout

```
.claude-plugin/marketplace.json   # Marketplace catalog (lists this plugin)
.claude-plugin/plugin.json        # Claude Code plugin manifest
skills/<name>/SKILL.md            # Each skill (standard location for both ecosystems)
```

The repo doubles as both a **marketplace** (catalog at
`.claude-plugin/marketplace.json`) and the **plugin** itself (manifest at
`.claude-plugin/plugin.json`, source `"./"`), so a single
`/plugin marketplace add` registers the catalog and `/plugin install` pulls
the plugin from the same repo.

## Adding a new skill

```bash
cd skills && npx skills init <skill-name>
```

Then edit `skills/<skill-name>/SKILL.md` and add it to the table above.

## Evaluating skills

The repo ships an eval harness under `evals/`, modeled on Anthropic's
[Demystifying Evals for AI Agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents).
Functional trials and scoring use `codex exec`.
Triggering trials use Claude Code. Both commands use their existing login.

```bash
# Does the skill trigger on the right prompts and skip the wrong ones?
python3 evals/run.py triggering --skill pr-gen --trials 2 --parallel 6

# Given it triggered, is the output good? Runs against fresh tmp git repos.
python3 evals/run.py functional --skill pr-gen
```

See [evals/README.md](evals/README.md) for layout, judge design, and how to
add cases for a new skill.

## Acknowledgments

The `visualize-arch` skill adapts methods from these projects:

- [PaperBanana](https://github.com/dwzhu-pku/PaperBanana) informs the planning, style, generation, and review stages. Its evaluation dimensions inform our figure evaluation.
- [Top-Conf Figure Gallery / FigureForge](https://github.com/qwdwqfwq/topconf-paper-figure-gallery) informs reference selection and visual analysis before generation.

## License

MIT
