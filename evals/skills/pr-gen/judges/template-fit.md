# Judge dimension: structure

The judge checks only the title, body structure, and length.
The judge ignores word choice and factual accuracy.

The judge returns `0` when any condition applies:

- The output lacks a title or body.
- The title exceeds 72 characters or lacks an imperative summary.
- The default body exceeds 120 words, excluding required checklists and issue links.
- The default body lacks three short sections with headings: `## Problem`, `## Solution`, and `## Validation`, in order.
- A default section uses prose paragraphs or a bullet with multiple sentences or points.
- The body includes a risk section or risk rating without an explicit user or repository requirement.
- The body includes an attribution footer that the user did not request.

User instructions and required repository templates take precedence over the default format.
The judge excludes title labels and code fences from the body word count.
The judge returns `1` when all requirements pass.
The judge sets `unknown` to `true` only when it cannot identify the title or body.
The judge writes its reason in Simplified Technical English (ASD-STE100).
The judge returns only this JSON object:

`{"score": 0|1, "reason": "...", "unknown": true|false}`
