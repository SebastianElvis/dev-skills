# Judge dimension: faithfulness

Inspect the figure and source artifacts before you score.
Compare them with the original repository evidence, reference facts, and requested scope.
The original code, schema, and configuration can support details that the reference summary omits.
Score 1 when the figure preserves every necessary component, boundary, direction, relationship, and outcome.
Allow simplification when it preserves those facts.
Score 0 for an invented element, reversed dependency, missing necessary path, incorrect cardinality, or scope violation.
Use `unknown: true` when an artifact is absent or illegible.
Write the reason in Simplified Technical English.
