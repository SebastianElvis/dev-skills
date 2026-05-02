# Judge dimension: template-fit (structure only)

Score the **structure** of the candidate. Do not judge prose quality, tone, or
word choice. A terse but correctly structured description scores 1; a verbose
but correctly structured one also scores 1.

Score **0** if any of these structural rules is violated:

- Title is missing, or omits an imperative-mood summary, or exceeds ~80 chars.
- Body is shorter than 3 non-empty lines (effectively empty), or longer than
  60 non-empty lines (padded).
- For a bugfix PR (the reference will say so): body is missing either an
  invariant statement OR a section listing the regression test(s) added.
- The body contains a `Co-Authored-By: Claude` line or a "Generated with
  Claude Code" footer.

Score **1** otherwise.

Set **unknown: true** only if the candidate is empty or unparseable.

Reply with strict JSON: `{"score": 0|1, "reason": "...", "unknown": true|false}`.
