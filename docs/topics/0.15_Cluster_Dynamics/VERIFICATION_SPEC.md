# Verification Spec

- Primary command:
  - `python docs/topics/0.15_Cluster_Dynamics/Code/03_Research/Research_BulletCluster_Offset.py`
- Inputs:
  - `Data/03_Research/chandra_clusters_2006.json`
  - `Data/03_Research/cluster_virial_1998.json`
  - `Data/03_Research/cluster_virial_data.json`
  - `Data/03_Research/download_data.py`
- Baseline:
  - Bullet Cluster coordinates, Chandra working files, and cited cluster references.
- Reported metrics:
  - mass residuals, offset mismatch, and script-reported cluster-fit diagnostics
- Fixed threshold:
  - Working threshold for this standards pass: the primary script must run without error, use the stated input package, and write a summary artifact under Result/artifacts/. A stronger numeric acceptance threshold must be frozen in a later BASELINE_COMPARISON.md pass.
- Artifact target:
  - Result/artifacts/0_15_cluster_dynamics_verification.json
- Interpretation:
  - Treat output as an internal benchmark artifact only. Do not upgrade claim language to 'solved', 'verified', or 'exact' until a topic-specific baseline-comparison pass is complete.
