---
name: visualize-arch
description: >-
  Create or update an evidence-based system architecture diagram from a software repository.
  Use this skill for requests to visualize architecture, components, actors, user stories, data flows, or control flows.
  Use it to refresh a diagram after code changes or generate editable TikZ with Scalable Vector Graphics and Portable Document Format outputs.
  Do NOT use it for charts, dashboards, interface mockups, class diagrams, database schema diagrams, one-call sequence diagrams, or decorative illustrations.
---

# Visualize architecture

Create an architecture diagram that explains verified system behavior. Keep the diagram source editable and deterministic.

Generate Scalable Vector Graphics (SVG) and Portable Document Format (PDF) files when the toolchain supports them.

## Critical requirements

- Read the repository instructions before you inspect or edit files.
- Verify each actor, component, boundary, and flow from repository evidence.
- Do not infer a flow from file names alone.
- Do not invent an actor, report destination, network, or interaction.
- Do not change system code to make the diagram correct.
- Preserve the current diagram format and build process when they exist.
- Do not commit, push, or create a PR unless the user asks.

## Workflow

### 1. Set the scope

Identify whether the user wants a new diagram or an update. Identify the audience and the system boundary.

Use the requested output format. For a current diagram, keep its format. For a new diagram, use TikZ by default.

Show the current architecture unless the user requests a target architecture.

For a new TikZ diagram, read [references/tikz.md](references/tikz.md). Use the bundled template as a structural start.

### 2. Collect evidence

Inspect these sources when they exist:

1. Repository instructions and architecture documents.
2. Entry points, routes, commands, and public interfaces.
3. Schedulers, workers, queues, and event handlers.
4. Database schemas and storage adapters.
5. Configuration and deployment files.
6. Clients for external services and networks.
7. Tests that show end-to-end behavior.

Trace each important flow from its actor or trigger to its outcome. Include the response path when it helps the user.

Use read-only subagents when the repository is large and subagents are available. Give each subagent one evidence area:

1. Actors, entry points, and public interfaces.
2. Services, configuration, storage, and run control.
3. External systems, networks, and end-to-end flows.

Require each subagent to return claims, file paths, source symbols, confidence, and open questions. Do not let subagents edit the diagram.

Resolve conflicts between claims before you define the architecture model.

### 3. Define the architecture model

Make a temporary model before you edit the diagram. Do not commit the model unless the user asks.

Record each node with these fields:

- Identifier.
- Kind: actor, component, store, external system, or network.
- Label.
- Owner or system boundary.
- Evidence path.
- Evidence symbol.

Record each ordered step with these fields:

- User story.
- Step number.
- Source node.
- Action label.
- Target node.
- Evidence path.
- Evidence symbol.

Record configuration and other static relationships separately. Do not give a step number to a static relationship.

### 4. Check the model

Read [references/design-principles.md](references/design-principles.md). Apply its content, flow, layout, and language rules.

Check these questions:

- Does each actor connect to the component that the actor actually uses?
- Does each user story start with the real actor or trigger?
- Does the diagram separate design-time actions from runtime actions?
- Does each ordered flow show its request, response, and outcome?
- Do shared paths merge at one explicit junction?
- Does each box have one clear responsibility?
- Does the system boundary match ownership and deployment?

Resolve a system defect separately from a diagram defect. Tell the user when verified code behavior appears incorrect.

### 5. Create or update the diagram

Use nouns for actor and component labels. Use short verb phrases for arrow labels.

Use one direction and one color for each user story. Use numbered circles for its ordered steps.

Use neutral lines for configuration and static relationships. Keep those lines out of the ordered step sequence.

Give alternative triggers the same step number when they join one shared stage.

Place actors on the left. Place the owned system in the center. Place external systems and networks on the right.

Route shared execution through explicit junctions. Separate routes before you adjust individual labels.

Do not let two different actions share one line segment. Merge a segment only when both paths represent the same action.

Split the view when a clear route is not possible after one layout change.

### 6. Render and inspect

Run the current diagram build command. For a new TikZ diagram, use the bundled renderer:

```bash
python3 path/to/visualize-arch/scripts/render_tikz.py docs/assets/system-architecture.tex
```

Render the PDF to an image. Inspect the image at a readable size.

Check for these defects:

- Arrow overlap.
- Label overlap.
- A line through a box or label.
- A clipped title, label, or arrow.
- An unwanted word break.
- A small gap between connected boxes.
- An unclear arrow direction.
- Colors with weak contrast.
- A path that does not match the architecture model.
- Two different actions that share one line segment.

Compilation does not prove visual quality. Repeat the edit, build, and visual check until the diagram is clear.

### 7. Add repository support

For a new diagram, add one documented build command. Keep the source and all generated files together.

Ignore temporary renderer files. Do not ignore the requested SVG or PDF files.

Update repository instructions, contribution rules, or the PR template only when the user requests this support.

### 8. Report the result

List the editable source and each generated output. State the build command and the checks that you ran.

Report each unresolved assumption. Use Simplified Technical English in the diagram and in the final response.

## Final checklist

- [ ] Repository evidence supports every actor, component, boundary, and flow.
- [ ] Each actor connects to the correct component.
- [ ] Each box contains a name, not behavior.
- [ ] Each arrow uses a short action label.
- [ ] Each user story has one color and numbered steps.
- [ ] Static relationships have no step number.
- [ ] Shared paths use explicit junctions.
- [ ] Different actions do not share one line segment.
- [ ] No arrow, label, or box has an unwanted overlap.
- [ ] The editable source and generated outputs are current.
- [ ] A visual inspection confirms the final layout.
- [ ] All output uses Simplified Technical English.
