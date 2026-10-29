# PR comment templates

Draft labels remain outside comment bodies.
The agent does not wrap drafts in an outer code fence.
Comment bodies use GitHub Markdown.
Comment bodies omit draft labels, stage counters, report sections, category markers, severity markers, and verdict markers.

## Attribution footnote

The agent adds the footnote below to every PR comment, including replies.
The footnote follows all comment content, including suggestion blocks.
The agent inserts a horizontal rule (`---`) above the footnote, with a blank line on each side.
The agent replaces `<harness>` with the agent application name, such as `Codex` or `Claude Code`.
The agent replaces `<model>` and `<effort>` with the model name and reasoning effort from the session.
The agent uses `unknown` for unavailable names and omits `(<effort>)` when the reasoning effort is unavailable.
The agent uses session metadata or explicit user information for these values, without guesses.
The agent replaces `@<submitter>` with the comment submitter's GitHub username.
The agent uses the username that the human supplies, or `gh api user --jq .login` for the authenticated submitter.
The agent asks for the username if the submitter's identity remains unclear.

## Top comment

The top comment states the recommendation and reason in at most three lines, excluding the footnote.

```markdown
**<The agent inserts one allowed first-person result from the shared rules.>**

<The agent gives the reason and any unresolved disagreement.>

---

*<harness> + <model> (<effort>) + [pr-review skill](https://github.com/SebastianElvis/dev-skills/blob/main/skills/pr-review/SKILL.md) created this comment. @<submitter> requested the publication.*
```

## Inline finding

A non-blocking finding uses at most 40 words, excluding the footnote.
It states the point and its reason.
It ends with a question.

    The new retry loop repeats the [backoff helper](https://github.com/<repo>/blob/<sha>/internal/retry/backoff.go#L12). Can this PR reuse it?

A blocking finding starts with one bold claim of at most 25 words.
The comment then states the current implementation, problem, and proposal.

````markdown
**<The agent states the claim in one sentence.>**

**Current implementation:** The [<operation>](https://github.com/<repo>/blob/<sha>/path/file.go#L104-L106) <has this behavior>.

**Problem:** <The agent states the failure condition and effect.>

**Proposal:** <The agent describes the fix and required tests.>

```suggestion
<The agent inserts the complete replacement for the selected lines.>
```

---

*<harness> + <model> (<effort>) + [pr-review skill](https://github.com/SebastianElvis/dev-skills/blob/main/skills/pr-review/SKILL.md) created this comment. @<submitter> requested the publication.*
````

## Suggestions

The agent includes a `suggestion` fence when a concrete fix fits one selectable range in the PR diff.
The replacement uses at most 10 lines.
This limit is a skill rule, not a GitHub limit.
The agent links the exact head-side range that the human must select.
The agent verifies each suggestion against the reviewed revision.
The replacement includes unchanged lines within that range.
The replacement omits diff prefixes and placeholders.
An empty `suggestion` block represents a deletion.

The agent includes a safe local suggestion even when other edits are necessary.
The proposal describes those edits and required tests separately.
The agent omits suggestions that need coordinated edits to remain valid.
The agent also omits suggestions above 10 lines, with unresolved design decisions, or without a selectable range.
The comment describes the proposed fix when the suggestion does not apply.
The session report records the omission reason.
Comment bodies omit commentary about the output format.

## Worked finding

The selected line contains `return limit < max`.
The requirement permits requests at the limit.
The example uses placeholders; actual output uses verified links.
The example assumes that the session identifies Codex, GPT-6 Astra, and High reasoning effort.

    **The comparison rejects requests at the permitted limit.**

    **Current implementation:** The [limit check](https://github.com/<repo>/blob/<sha>/internal/limits/check.go#L104) accepts only `limit < max`.

    **Problem:** A request with `limit == max` fails, although the requirement permits it.

    **Proposal:** The comparison `<=` accepts the limit. Tests for values below, at, and above the limit cover the boundary.

    ```suggestion
    return limit <= max
    ```

    ---

    *Codex + GPT-6 Astra (High) + [pr-review skill](https://github.com/SebastianElvis/dev-skills/blob/main/skills/pr-review/SKILL.md) created this comment. @<submitter> requested the publication.*

## Replies and publication

A reply to a person uses short paragraphs without bullets.
When the author is right, the reply accepts the point in one sentence.

The request of the user selects the GitHub review event:

| Request | Event |
| --- | --- |
| "approve" | `APPROVE` |
| "comment" or "post" | `COMMENT` |
| "request changes" | `REQUEST_CHANGES` |

An `APPROVE` review includes all inline comment drafts.
An approval request makes the remaining findings non-blocking.
The top comment of an `APPROVE` review then uses `I recommend merge.`

## Template check

- [ ] Each blocking finding has a bold claim, current implementation, problem, and proposal.
- [ ] Each non-blocking finding is a question of at most 40 words.
- [ ] Each applicable suggestion contains the complete replacement with at most 10 lines.
- [ ] Each suggestion preserves required context within its selected range.
- [ ] Each omitted suggestion has a report reason and a proposed fix in the comment.
- [ ] Comment bodies omit report sections and format commentary.
- [ ] Each footnote follows a horizontal rule with a blank line on each side.
- [ ] Each footnote identifies the harness and model, marks unknown names, and includes the reasoning effort when available.
- [ ] Each footnote includes the skill link and the submitter's GitHub username.
