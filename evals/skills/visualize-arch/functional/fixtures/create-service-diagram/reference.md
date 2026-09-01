# Reference architecture

The diagram has two actors: Operator and Viewer.

The owned system contains the command-line interface (CLI), Dashboard, application programming interface (API) service, SQLite, Worker, and Scheduler.

The Carrier API is an external system.

The operator flow starts at Operator. It passes through the CLI and API service before SQLite stores the job.

The viewer flow starts at Viewer. It passes through the Dashboard and API service. The API service reads SQLite and returns the status.

The scheduled flow starts at the Scheduler. The Worker reads SQLite, calls the Carrier API, and stores the result.

The schedule configuration uses a neutral relationship. It has no ordered step number.

The result includes editable TeX and valid generated files. These files use Scalable Vector Graphics (SVG) and Portable Document Format (PDF).

The result also includes a Makefile. The final response lists each file and the checks.
