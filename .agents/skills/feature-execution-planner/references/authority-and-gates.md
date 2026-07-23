# Authority and gates

Gate 0 owns product intent. Gate 1 owns decision revisions. Gate 2 owns execution and release composition. A separate implementation-authorization event permits named work to begin.

Gate PRs are separate diffs. A mixed Gate 0, Gate 1, Gate 2, authorization, or implementation diff fails classification.

Primary decision ownership is path-based through CODEOWNERS. Cross-domain co-approval is checked against the protected approval-role registry. In team mode, a current-head approval from someone other than the PR author is required. Solo mode records the authority limitation and relies on the repository owner and protected merge action.

Generated files never carry authority. Effective approval comes from the exact content hash, current PR head, passing checks, required authenticated reviewers, and protected merge.
