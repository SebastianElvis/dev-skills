# Reference worker workflow

The current provider is ParcelCarrier. LegacyCarrier is obsolete.
The Worker reads a job from the queue and calls ParcelCarrier.
The success path stores the result in the database and returns sent.
The timeout path marks the job failed in the database and returns failed.
The timeout path does not store a success result.
The figure distinguishes both outcomes without invented retry behavior.
The source remains TikZ. The Makefile still builds worker.tex.
The application code stays unchanged.
The final width is 85 mm. Every label has at least 8 pt effective text size.
The final response lists the source, vector outputs, and completed checks.
