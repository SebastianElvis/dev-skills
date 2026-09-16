# Judge dimension: Simplified Technical English

The judge checks the output against the repository's Simplified Technical English (ASD-STE100) rules.
The judge checks these requirements:

- Each sentence contains one idea and an explicit subject.
- Each sentence uses active voice and a simple tense.
- Each instruction contains at most 20 words.
- Each descriptive sentence contains at most 25 words.
- The output uses one term for each concept.
- The output contains no idioms, metaphors, or `-ing` verb forms.

The judge permits imperative titles, headings, identifiers, exact quotations, and command output.
The judge does not require the licensed dictionary.
The judge returns `0` for a clear violation or `1` when all requirements pass.
The judge sets `unknown` to `true` when the output contains too little prose for a decision.
The judge writes its reason in Simplified Technical English.
The judge returns only this JSON object:

`{"score": 0|1, "reason": "...", "unknown": true|false}`
