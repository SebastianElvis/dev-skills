# Reference data model

The data model has nine tables.
The identity group contains tenants, accounts, memberships, and api_tokens.
The dispatch group contains shipments and dispatch_runs.
The evidence group contains provider_attempts, delivery_receipts, and audit_events.

Each membership references exactly one tenant and one account.
A tenant and an account can each have zero or more memberships.
The combination of tenant_id, account_id, and role is unique.
Each token references exactly one account. Its token_hash is unique. Its revoked_at can be null.

Each shipment references exactly one tenant and one author account.
Each dispatch run references exactly one shipment and one requesting account.
Each shipment and account can have zero or more dispatch runs.
Each provider attempt references exactly one run. The combination of run_id and sequence is unique.
Each receipt references exactly one run. Each run has zero or one receipt because receipt.run_id is unique.
Each audit event references exactly one run and zero or one account.
A run can have zero or more provider attempts and audit events.
An automated audit event has a null actor_id.
The schema permits zero child rows for each referenced parent.

The diagram shows keys, foreign keys, nullability, cardinalities, and the important uniqueness constraints.
The diagram uses grouped entities and relationship notation rather than workflow step numbers.
The requested final width is 180 mm. The minimum text size is 8 pt.
The attached data model sets the minimum visual quality.

The 180 mm width tests a paper figure with two columns. The evaluator keeps the full schema requirements.
