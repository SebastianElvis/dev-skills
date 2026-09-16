# Judge dimension: structure

The judge checks only the title, body structure, and length.
The judge ignores word choice and factual accuracy.

The judge returns `0` when any condition applies:

- The output lacks a title or body.
- The title exceeds 72 characters or lacks an imperative summary.
- The body exceeds 25 lines, including headings and blank lines.
- A bugfix body lacks Summary, an invariant or expected behavior section, The fix, or the matching test section in order.
- A feature body lacks Summary or Changes in order.
- The body includes an attribution footer that the user did not request.

The judge excludes title labels and code fences from the body line count.
The judge returns `1` when all requirements pass.
The judge sets `unknown` to `true` only when it cannot identify the title or body.
The judge writes its reason in Simplified Technical English (ASD-STE100).
The judge returns only this JSON object:

`{"score": 0|1, "reason": "...", "unknown": true|false}`
