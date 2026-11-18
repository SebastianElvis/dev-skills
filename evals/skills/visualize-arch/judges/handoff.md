# Judge dimension: handoff

Score the final response against the requested figure set.
Write the reason in Simplified Technical English.

Score 1 when the response gives each source path and vector output path.
Links can identify those paths. The vector files use Scalable Vector Graphics (SVG) and Portable Document Format (PDF).
The response must state the build command or completed checks.
A build command can identify the Makefile. The response does not need a separate Makefile link.
The response does not need to list temporary previews, logs, or support files unless the task requests those paths.

Score 0 when the response omits a figure source or vector output.
Score 0 when the response claims an unverified result.
A directory path alone does not identify each required output.
Set `unknown` to true when the available response does not permit a decision.
