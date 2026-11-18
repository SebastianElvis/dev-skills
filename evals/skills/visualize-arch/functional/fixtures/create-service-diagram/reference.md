# Reference figure set

The approved scope has two figures: a static system overview and a scheduled worker workflow.
The overview has 178 mm final width. The worker workflow has 85 mm final width.
Every label has at least 8 pt effective text size.

## Static overview

The diagram has two actors: Operator and Viewer.
The owned system contains the command-line interface (CLI), Dashboard, application programming interface (API) service, SQLite, Worker, and Scheduler.
The Carrier API is an external system.
The Operator connects to the CLI. The CLI connects to the API service.
The Viewer connects to the Dashboard. The Dashboard connects to the API service.
The API service and Worker depend on SQLite.
The Worker calls the Carrier API. The Scheduler starts the Worker.
The schedule configuration belongs to the owned system.
The Scheduler runs every five minutes. The config.toml file sets interval_minutes to 5.
Unnumbered black or gray links show static relationships.
A directed static link can show a dependency. It does not specify an ordered action.
The overview shows structure. The workflow shows ordered actions.

## Scheduled worker workflow

The Scheduler starts the Worker.
The Worker reads a stored job from SQLite.
The Worker calls the Carrier API.
The Worker stores the returned result in SQLite.
The workflow preserves this order and final outcome.
The schedule configuration has no ordered step number.

## Outputs

The result includes editable TeX, valid vector files, and a Makefile.
The vector files use Scalable Vector Graphics (SVG) and Portable Document Format (PDF).
The design record includes reference choices, design constraints, and captions.
The final response identifies each source and vector file by its exact path.
The final response states the build command and completed checks.
