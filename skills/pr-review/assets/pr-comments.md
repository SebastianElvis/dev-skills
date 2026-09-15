# PR comment templates

The agent writes the top comment and inline comments as separate drafts after the session report.
Draft labels remain outside comment bodies.
The agent does not wrap drafts in an outer code fence.
Comment bodies use GitHub Markdown and the shared code-link and Simplified Technical English rules.
Comment bodies omit draft labels, stage counters, report sections, category markers, severity markers, and verdict markers.
The human posts the comments unless the user directly requests publication.

## Top comment

The top comment states the recommendation and reason in at most six lines.
The comment gives no PR summary.

```markdown
**<The agent inserts one allowed first-person result from the shared rules.>**

<The agent gives the reason and any unresolved disagreement.>

The review covers <areas>. The review excludes <areas and reasons>.
```

## Inline finding

Each finding starts with one bold claim of at most 25 words.
The comment then states the current implementation, problem, and proposal.
The agent uses bullets for multiple evidence points or required edits.
The agent keeps one finding per root cause.

````markdown
**<The agent states the claim in one sentence.>**

**Current implementation:** The [<operation>](https://github.com/<repo>/blob/<sha>/path/file.go#L104-L106) <has this behavior>.

**Problem:** <The agent states the failure condition and effect.>

**Proposal:** <The agent describes the fix and required tests.>

```suggestion
<The agent inserts the complete replacement for the selected lines.>
```
````

## Suggestions

The agent includes a `suggestion` fence when a concrete fix fits one selectable range in the PR diff.
The replacement uses at most 10 lines.
This limit is a skill rule, not a GitHub limit.
The agent puts the block last and links the exact head-side range that the human must select.
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

## Template check

- [ ] The top comment uses an allowed recommendation and at most six lines.
- [ ] Each finding has a bold claim, current implementation, problem, and proposal.
- [ ] Each code link identifies verified lines at the reviewed revision.
- [ ] Each applicable suggestion contains the complete replacement with at most 10 lines.
- [ ] Each suggestion preserves required context within its selected range.
- [ ] Each omitted suggestion has a report reason and a proposed fix in the comment.
- [ ] Comment bodies omit report sections and format commentary.
- [ ] Each comment follows Simplified Technical English.
