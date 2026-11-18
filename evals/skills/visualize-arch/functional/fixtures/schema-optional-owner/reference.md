# Reference schema

The schema has three entities: projects, owners, and jobs.
Each entity has a primary key named id.
Each job references exactly one project through project_id.
Each project can have zero or more jobs.
Each job references zero or one owner through nullable owner_id.
Each owner can have zero or more jobs.
The figure states these cardinalities explicitly.
The figure has no ordered workflow numbers.
The final width is 85 mm. Every label has at least 8 pt effective text size.
The output includes editable TeX and valid vector files.
The Makefile path is docs/assets/Makefile.
The final response lists the outputs and completed checks.
