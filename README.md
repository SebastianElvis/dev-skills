# dev-skills

A collection of general software-development agent skills, packaged for the
[Vercel Labs `skills`](https://github.com/vercel-labs/skills) ecosystem.

## Install

```bash
# Install every skill in this repo into the current project
npx skills add SebastianElvis/dev-skills

# Or install globally for all projects
npx skills add SebastianElvis/dev-skills -g

# Or install just one skill
npx skills add SebastianElvis/dev-skills --skill pr-gen
```

Works with Claude Code, Codex, Cursor, OpenCode, and every other agent the
`skills` CLI supports.

## Skills

| Skill | What it does |
| --- | --- |
| [`pr-gen`](pr-gen) | Generate or update a GitHub PR title and description from the actual code changes on the current branch. |

## Adding a new skill

```bash
npx skills init <skill-name>
```

Then edit `<skill-name>/SKILL.md`, commit, and add it to the table above.

## License

MIT
