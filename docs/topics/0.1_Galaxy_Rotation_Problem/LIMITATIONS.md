# Limitations

- The checked-in verifier input is a summary-row working copy, not a full upstream
  SPARC radial-curve archive.
- The current benchmark uses one recorded radius and one recorded observed
  velocity per processed galaxy row, so it cannot by itself establish whole-curve
  agreement.
- The engine contains heuristic bridge terms and hidden scaling anchors that still
  need explicit derivation, dependency mapping, and sensitivity analysis.
- The meaning of `R_disk_kpc` in the working copy needs tighter source-locking so
  the enclosed-mass relation is not applied against an ambiguous radius
  convention.
- Internal pass rates do not establish out-of-sample performance, nor do they
  replace comparator baseline evaluation against MOND or dark-matter models.
- The artifact-level `WARN` means the verifier ran; it does not mean the model passed. The current `galaxy_model_gate` must keep dark-matter replacement and galaxy-closure claims blocked while the summary-row residual gate fails.
- No fresh external replication package is documented in this hardening pass.

## Current Claim Boundary

| Claim area | Allowed wording now | Blocker to stronger wording |
| :-- | :-- | :-- |
| Run contract | internal summary-row verifier ran | does not imply model acceptance |
| Summary-row model | residual blocker over repository working copy | average error must pass threshold and pass rate must be nonzero under a declared metric |
| SPARC replication | not supported | source-locked full curve arrays, row semantics, and preprocessing manifest |
| Dark-matter replacement | not supported | comparator baselines, lensing/rotation evidence, uncertainty, and out-of-sample tests |
