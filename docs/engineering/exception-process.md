# Standards exception process

An exception is a temporary, explicit risk decision. It is not permission for an agent to silently bypass a control.

## Required record

Document:

- Rule or control being bypassed
- Exact scope
- Business or technical reason
- Risk created
- Compensating controls
- Named human approver
- Effective date
- Expiration date
- Follow-up issue or remediation milestone
- Evidence required before closure

## Approval levels

- Low-risk engineering convention: technical owner
- Security, privacy, data, or production control: security or system owner
- Critical or irreversible risk: executive or accountable business owner

## Rules

- Exceptions must expire.
- Exceptions may not be approved by the agent requesting them.
- Expired exceptions block release until renewed or remediated.
- Permanent divergence requires an ADR and an update to the standards, not an indefinitely renewed exception.
