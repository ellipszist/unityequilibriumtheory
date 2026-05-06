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
- No fresh external replication package is documented in this hardening pass.
