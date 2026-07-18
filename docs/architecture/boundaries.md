# Architecture boundaries

Replace these defaults with project-specific rules while preserving explicit dependency direction.

## Default dependency rules

- UI depends on application contracts, not persistence implementations.
- Application services coordinate use cases and depend on domain interfaces.
- Domain logic does not depend on web frameworks, databases, queues, or UI code.
- Infrastructure adapters implement interfaces defined by inner layers.
- A service does not query another service's database directly.
- External providers sit behind explicit adapters.
- Authorization is enforced server-side at the use-case or resource boundary.
- Shared code contains stable cross-cutting primitives, not arbitrary business logic.

## Prohibited patterns

- Business rules duplicated across UI, API, and database triggers without an explicit source of truth.
- Circular module dependencies.
- Cross-tenant queries without explicit tenant scoping.
- Framework objects leaking into domain interfaces.
- Generic utility modules that become unowned dependency hubs.

## Enforcement

Record which rules are enforced by package boundaries, compiler settings, lints, architecture tests, CODEOWNERS, or review.
