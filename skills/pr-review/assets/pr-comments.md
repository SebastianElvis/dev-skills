# PR comment templates

Draft labels remain outside comment bodies.
The agent does not wrap drafts in an outer code fence.
Comment bodies use GitHub Markdown.
Comment bodies omit draft labels, stage counters, report sections, category markers, severity markers, and verdict markers.

## Attribution footnote

The agent adds the footnote below to every PR comment, including replies.
The footnote follows all comment content, including suggestion blocks.
The agent inserts a horizontal rule (`---`) above the footnote, with a blank line on each side.
The agent replaces `@<submitter>` with the comment submitter's GitHub username.
The agent uses the username that the human supplies, or `gh api user --jq .login` for the authenticated submitter.
The agent asks for the username if the submitter's identity remains unclear.
The agent states that discussion occurred only after the agent discusses that comment with the submitter.
An earlier stage confirmation alone does not establish discussion of a later comment.
Before that discussion, the draft footnote uses `The agent awaits discussion with @<submitter>.` as its second sentence.
The agent completes that discussion before publication.

## Top comment

The top comment states the recommendation and reason in at most six lines, excluding the footnote.

```markdown
**<The agent inserts one allowed first-person result from the shared rules.>**

<The agent gives the reason and any unresolved disagreement.>

The review covers <areas>. The review excludes <areas and reasons>.

---

*The [pr-review skill](https://github.com/SebastianElvis/dev-skills/blob/main/skills/pr-review/SKILL.md) created this comment. The agent discussed this comment with @<submitter>.*
```

## Inline finding

Each finding starts with one bold claim of at most 25 words.
The comment then states the current implementation, problem, and proposal.
The agent uses bullets for multiple evidence points or required edits.

````markdown
**<The agent states the claim in one sentence.>**

**Current implementation:** The [<operation>](https://github.com/<repo>/blob/<sha>/path/file.go#L104-L106) <has this behavior>.

**Problem:** <The agent states the failure condition and effect.>

**Proposal:** <The agent describes the fix and required tests.>

```suggestion
<The agent inserts the complete replacement for the selected lines.>
```

---

*The [pr-review skill](https://github.com/SebastianElvis/dev-skills/blob/main/skills/pr-review/SKILL.md) created this comment. The agent discussed this comment with @<submitter>.*
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

    **The comparison rejects requests at the permitted limit.**

    **Current implementation:** The [limit check](https://github.com/<repo>/blob/<sha>/internal/limits/check.go#L104) accepts only `limit < max`.

    **Problem:** A request with `limit == max` fails, although the requirement permits it.

    **Proposal:** You must accept equality. You must test values below, at, and above the limit.

    ```suggestion
    return limit <= max
    ```

    ---

    *The [pr-review skill](https://github.com/SebastianElvis/dev-skills/blob/main/skills/pr-review/SKILL.md) created this comment. The agent discussed this comment with @<submitter>.*

## Template check

- [ ] Each finding has a bold claim, current implementation, problem, and proposal.
- [ ] Each applicable suggestion contains the complete replacement with at most 10 lines.
- [ ] Each suggestion preserves required context within its selected range.
- [ ] Each omitted suggestion has a report reason and a proposed fix in the comment.
- [ ] Comment bodies omit report sections and format commentary.
- [ ] Each footnote follows a horizontal rule with a blank line on each side.
- [ ] Each footnote includes the skill link, submitter's GitHub username, and accurate discussion status.
