# Secure implementation standards

## Mandatory review areas

- Authentication and session handling
- Authorization and tenant isolation
- Input validation and output encoding
- SQL, command, template, and path injection
- SSRF and untrusted network destinations
- CSRF, CORS, redirects, and browser security
- Deserialization and user-controlled execution
- Secrets and sensitive logging
- Cryptography and key management
- Race conditions and time-of-check/time-of-use defects
- Fail-open behavior
- Dependency and build provenance

## Boundary rules

- Validate external input at entry boundaries.
- Authorize every protected resource server-side.
- Scope data access by authenticated tenant or principal.
- Use parameterized database access.
- Restrict outbound network access and validate destinations.
- Use approved cryptographic libraries and algorithms.
- Redact sensitive data before logging.
- Use least privilege for services, CI, cloud identities, and databases.

## High-risk changes

Authentication, authorization, payments, secrets, IAM, cryptography, sensitive migrations, and user-controlled execution require threat modeling, abuse-case tests, independent security review, staged rollout, and explicit human approval.
