# Rollback and disablement

Every production change must have a recovery path before deployment.

Document:

- Rollback trigger thresholds
- Feature flag or kill switch
- Previous known-good artifact
- Database compatibility
- Migration rollback or forward-fix
- Maximum acceptable recovery time
- Responsible owner
- Verification after recovery

Do not call a migration reversible when data meaning or deleted information cannot be restored.
