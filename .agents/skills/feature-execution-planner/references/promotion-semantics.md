# Promotion semantics

A milestone revision is a release contract. A promotion attempt is the actual deployment of that exact contract and has its own immutable identity, such as `MILESTONE-002/2#P1`.

Promotion retries may reuse a milestone revision only when composition, artifacts, decisions, evidence requirements, observability, rollout, and rollback remain unchanged. A code or contract change creates a new execution and milestone revision.

An enabling milestone declares what happens when its downstream consumer fails: retain for retry, rollback, retire, reuse pending approval, or forward recover. A live unconsumed enabler is owned, observable, time-bounded, and never counts as feature completion.

Production accountability transfers only after the replacement promotion reaches live. Failed corrections leave the prior live claimant accountable.
