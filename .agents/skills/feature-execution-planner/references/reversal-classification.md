# Reversal classification

Use reversal cost, not vague consequence language, to determine authority.

- `local`: undo within one module with no migration, consumer negotiation, or coordination.
- `bounded`: undo remains within one owned subsystem and one deployment boundary.
- `coordinated`: undo requires migration, consumer contract changes, multi-service deployment order, external correction, or cross-team work.
- `irreversible`: the former state cannot be reliably restored or correction leaves material residual risk.

Local and policy-permitted bounded choices may be selected by the planner and annotated. Coordinated and irreversible choices require a decision record and human Gate 1 approval.

Rollback is evaluated at the milestone composition level. A milestone that cannot be made reversible must reference an approved irreversibility decision and a forward-recovery strategy.
