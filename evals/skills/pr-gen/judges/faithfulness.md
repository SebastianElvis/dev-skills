# Judge dimension: faithfulness

Score **1** if every concrete claim in the candidate PR description is faithful
to the final-state diff that the user produced. Score **0** if any claim is
fabricated, contradicts the diff, or describes work that was added then removed
(present in commit history but absent from `HEAD`).

Concrete claims include:
- File paths, function/symbol names, test names.
- Statements about *what* the change does (added X, removed Y, renamed Z).
- Behavior or invariant claims that imply specific code.

Set **unknown: true** only if the candidate output is empty, malformed, or
references material that is plausibly real but not present in the reference.
Prefer 0 over unknown when the candidate clearly invents content (e.g. a file
path or symbol the reference says was deleted).

Examples:
- Mentions `multiply` function in `src/math.py` and the reference confirms it
  was added → 1.
- Mentions a `scratch.py` file that the reference notes was added then deleted →
  0 (fabrication-by-history).
- Says "fixes off-by-one" and reference confirms the fix → 1.
- Lists a test name not present in the reference's test list → 0.
