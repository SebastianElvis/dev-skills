# dev-skills

A collection of general software-development agent skills. Installable via
either the [Vercel Labs `skills` CLI](https://github.com/vercel-labs/skills) or
[Claude Code's built-in plugin system](https://code.claude.com/docs/en/plugins).

## Install

### Via Claude Code (recommended for Claude Code users)

```bash
# Add this repo as a plugin marketplace, then install
/plugin marketplace add SebastianElvis/dev-skills
/plugin install dev-skills
```

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

## Layout

```
.claude-plugin/plugin.json   # Claude Code plugin manifest
skills/<name>/SKILL.md       # Each skill (standard location for both ecosystems)
```

## Adding a new skill

```bash
cd skills && npx skills init <skill-name>
```

Then edit `skills/<skill-name>/SKILL.md` and add it to the table above.

## License

MIT
