# Limitations

- The root baseline comparison now has a saved artifact, but the current raw McMillan model gate fails: average relative error is about 62.4 percent and only 1 of 10 rows is within 20 percent.
- Current data posture is "real source referenced", which is below a fully normalized archival dataset package.
- The topic still needs a clear separation between phenomenological fit behavior and stronger microscopic claims.
- The raw McMillan baseline currently has high residuals and should be treated as a model/baseline blocker, not a successful UET prediction.
- The inverse-McMillan diagnostic indicates the current working-copy `lambda_ep` values are systematically high relative to the values needed to reproduce observed `Tc` with the declared `Theta_D_K` and `mu_star` inputs.
- Calibrated `lambda` values and heuristic coherence/Z corrections must not be described as no-fit predictions.
- High-Tc cuprates and hydrides require separate source-backed verifiers before any claim upgrade.
- Internal script execution does not by itself establish external replication, formal proof, or broad physical closure.
- Source records for McMillan 1968, Allen-Dynes 1975, and NIMS SuperCon now exist, but raw NIMS MDR data is not yet mirrored or consumed by the verifier.
- Until row-level electron-phonon coupling, phonon temperature/log-frequency, and Coulomb pseudopotential provenance is source-normalized, the FAIL should be interpreted as a parameter-package/model-gate blocker.
