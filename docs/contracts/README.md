# Contracts

Machine-consumable contracts are authoritative for interfaces.

Recommended locations:

- `docs/contracts/openapi.yaml` for HTTP APIs.
- `docs/contracts/events/` for event schemas.
- `docs/contracts/schemas/` for files, configuration, or messages.

Contract changes must document compatibility, consumers, migration, versioning, deprecation, and verification. Do not rely on prose alone when a schema can be validated automatically.
