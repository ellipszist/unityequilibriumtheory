# Method

## Problem target

This topic studies whether UET-inspired cluster-dynamics models can reproduce selected galaxy-cluster observables and offsets.

## Core components

### Engine components
- `Code/01_Engine/cluster_solver.py`
- `Code/01_Engine/Engine_Cluster_Dynamics.py`

### Proof-oriented components
- `Code/02_Proof/Proof_Virial_Mass.py`

### Research and comparison components
- `Code/03_Research/Research_BulletCluster_Offset.py`
- `Code/03_Research/Research_Cluster_Formation.py`
- `Code/03_Research/Research_Cluster_Virial.py`

## Variable framing

- Primary modeled quantities: cluster mass, virial quantities, spatial offsets, and cluster-formation terms

## Assumptions

- The topic is currently an effective astrophysical benchmark package around selected cluster observations.

## Domain of validity

- Selected cluster datasets such as Bullet Cluster and Chandra-derived working files.

## Excluded cases

- A universal replacement for dark-matter modeling across all cluster physics.

## Parameter sensitivity note

- Cluster selection, nuisance terms, and projection choices matter in the current comparisons.
