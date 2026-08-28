# Architecture diagram design principles

Use these rules to define the diagram content and layout.

## Correctness

- Inspect the code, configuration, and documentation before you draw.
- Draw only verified actors, components, responsibilities, and flows.
- Connect each actor to the component that the actor actually uses.
- Use a named role instead of a generic `User` actor.
- Separate a diagram defect from a system architecture defect.
- Mark an unresolved assumption. Do not invent a path.

## Scope and structure

- Show actors, system boundaries, internal components, external systems, and networks.
- Put owned configuration inside the system boundary.
- Place configuration by ownership, not by its file type.
- Put external systems and networks outside the system boundary.
- Split components when they have different responsibilities or owners.
- Merge details when they do not improve system clarity.
- Put only actor or component names inside boxes.
- Put actions on arrows.

## User stories

- Start each user story with the real actor or trigger.
- Separate source authors from runtime actors.
- Separate design-time actions from runtime actions.
- Show each request, response, and final outcome.
- Show manual and scheduled entry paths accurately.
- Merge shared execution paths at an explicit junction.
- Share a line segment only when both paths represent the same action.
- Keep a request action separate from a later start action.
- Do not duplicate one user story under different names.
- Show periodic behavior without an invented timer actor.
- Use a self-loop when a component starts its own periodic action.

## Flow notation

- Use unidirectional arrows for ordered actions.
- Use one color for each user story.
- Use numbered circles for ordered steps.
- Restart the numbers for each user story.
- Give alternative triggers the same number when they join one stage.
- Give each arrow a short action label.
- Use neutral lines for configuration or static relationships.
- Use one color for all arrows and labels in the same story.

## Layout

- Put actors on the left.
- Put the owned system in the center.
- Put external systems on the right.
- Put external networks beyond their systems.
- Increase the canvas before routes become dense.
- Give each user story a separate route.
- Give different actions separate line segments.
- Prevent arrow, label, and box overlap.
- Keep clear space between connected boxes.
- Use transparent label backgrounds.
- Use thick arrows and colors with clear contrast.
- Enlarge central components when they have many connections.
- Prefer explicit junctions over crossed or interleaved arrows.
- Split the view when clear routes are not possible.
- Do not change a verified flow to make the layout easier.

## Language

- Use simple component names.
- Avoid vague names such as `control plane`.
- Avoid diagram jargon such as `lane`.
- Use nouns for boxes.
- Use verbs for arrows.
- Describe the actual outcome of each actor workflow.

## Validation

- Keep an editable and deterministic diagram source.
- Generate Scalable Vector Graphics (SVG) and Portable Document Format (PDF) outputs when the toolchain supports them.
- Render and inspect the diagram after each source change.
- Do not treat a successful compilation as visual validation.
- Keep the source and generated files in sync.
- Provide one build command for a maintained repository diagram.
- Check the image for unwanted word breaks.
- Check each user story for a complete directed path.
