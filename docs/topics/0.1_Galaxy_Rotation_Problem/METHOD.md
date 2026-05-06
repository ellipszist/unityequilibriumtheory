# Method

- Solver component: `Code/01_Engine/Engine_Galaxy_V3.py`
- Proof component: `Code/02_Proof/Proof_Unity_Density_Law.py`
- Internal benchmark script: `Code/03_Research/Research_Galaxy_Rotation.py`
- Calibration-aware verification script: `Code/03_Research/Verify_Galaxy_Rotation.py`

Method boundary:

- The current topic-level verifier maps one repository summary row per galaxy into
  baryonic engine inputs, predicts velocity at the recorded radius, and compares
  that prediction against the recorded observed velocity.
- `Engine_Galaxy_V3.py` combines an exponential-disk enclosed-mass relation, a
  heuristic bulge enclosure rule, an information-mass bridge, and a galactic
  velocity law using `G_GALACTIC`.
- The current engine still contains hidden benchmark anchors in the information
  mass bridge, including the `11.7` beta scaling and `0.075` coupling factor.
- Because the repository includes both derivation-facing and calibration-aware
  scripts, the topic must not be described as purely parameter-free.

Current verification meaning:

- A `PASS` means the checked-in summary-row benchmark averages below the current
  `15%` mean absolute percentage error gate.
- A `WARN` means valid comparisons exist but the benchmark misses that gate.
- Neither status alone proves that the theory reproduces full observed rotation
  curves across galaxy classes without further source-locked curve-level testing.
