# UET Installation Matrix

This document outlines the four distinct installation paths for the Unity Equilibrium Theory (UET) project. Because UET is simultaneously a Python library, a research corpus, a verification harness, and a data repository, a single "quick start" command does not fit all use cases.

## Installation Paths Overview

| Persona | Goal | Path Name | Complexity |
| :--- | :--- | :--- | :--- |
| **Applied Engineer / Data Scientist** | Use UET's core equations, fluid dynamics engine, or math solvers in their own code. | [1. Python Library Install](#1-python-library-install) | Low |
| **Reviewer / Student** | Verify a specific scientific claim (e.g., Galaxy Rotation, Fluid Dynamics) against real data. | [2. Topic Verification Install](#2-topic-verification-install) | Medium |
| **Peer Reviewer / Internal Team** | Run the complete verification suite across all 31 domains. | [3. Full Research Suite Install](#3-full-research-suite-install) | High |
| **Core Contributor** | Modify the master equation, add new topics, or build UI/API layers. | [4. Developer Install](#4-developer-install) | High |

---

## 1. Python Library Install

**Best for:** Trying the API, running simulations, or integrating UET into an existing Python project.

**Requirements:**
- Python 3.9+
- Git

**Command:**
```bash
# Clone the repository
git clone https://github.com/unityequilibrium/UnityEquilibriumTheory.git
cd UnityEquilibriumTheory

# Install as a standard Python package
pip install .
```

**What you get:**
- Access to the `docs` namespace.
- Core Solvers: `uet.core`
- Hero APIs: `uet.fluid` (2D/3D), `uet.math` (Riemann), `uet.complexity`

**What is NOT included:**
- The automated research runners (`run_all_tests.py`).
- Automatic downloading of large external datasets.

---

## 2. Topic Verification Install

**Best for:** Reproducing the results of a specific topic (e.g., Topic 0.1 Galaxy Rotation) using the 5x4 scientific grid.

**Requirements:**
- Python 3.9+
- Git
- Virtual Environment (recommended)

**Command:**
```bash
# Setup environment
git clone https://github.com/unityequilibrium/UnityEquilibriumTheory.git
cd UnityEquilibriumTheory
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install in editable mode to access internal data paths
pip install -e .

# Optional: Install visualization tools if running Cine/Vis scripts
pip install seaborn
```

**Execution Example:**
To verify the Galaxy Rotation problem without dark matter:
```bash
python docs/topics/0.1_Galaxy_Rotation_Problem/Code/03_Research/Research_Galaxy_Rotation.py
```

**Notes:**
- Topic data is already included in `docs/topics/[Topic_ID]/Data/`.
- Generated plots will appear in the `Result/` folder of that topic.

---

## 3. Full Research Suite Install

**Best for:** Running the global test harness across all 31 pillars of truth.

**Requirements:**
- Python 3.9+
- Strong CPU (for parallel/fluid tests)
- Internet connection (for scripts that fetch external reference data)

**Command:**
```bash
# Clone and setup
git clone https://github.com/unityequilibrium/UnityEquilibriumTheory.git
cd UnityEquilibriumTheory
pip install -e .

# Run the master test runner
python docs/topics/run_all_tests.py
```

**⚠️ Important Caveats for Full Suite:**
1. **Legacy Path Assumptions:** The runner scripts attempt to inject paths (like `lab/01_galaxy_dynamics`) that may not exist in standard public clones. If a script fails with `ModuleNotFoundError`, it is likely due to these legacy environmental assumptions.
2. **Headless Mode:** Some visualization scripts will crash if run without a display. The harness attempts to force headless mode (`matplotlib.use("Agg")`), but user mileage may vary.
3. **Network Dependencies:** Certain topics (e.g., `0.8_Muon_g2_Anomaly`) contain `Download_*_Refs.py` scripts that query arXiv APIs. Ensure network access is available.

---

## 4. Developer Install

**Best for:** Contributing to the UET codebase, adding new equations, or building the web/API layers.

**Requirements:**
- Python 3.9+
- Rust 1.80+ (for API/MCP/Mining features)
- PostgreSQL + pgvector (for Knowledge Base)

**Command (Python Core):**
```bash
git clone https://github.com/unityequilibrium/UnityEquilibriumTheory.git
cd UnityEquilibriumTheory

# Install with development dependencies
pip install -e ".[dev]"
```

**Command (Rust Backend & Web):**
```bash
# Verify Rust workspace
cargo check --workspace

# Run local API
cargo run -p uet_api

# Run Next.js UI
cd uet_web
npm install
npm run dev
```

**Known Development Issues:**
- `setup.py` and `pyproject.toml` have minor discrepancies (e.g., `sympy` requirement). Rely on `pyproject.toml` as the source of truth for version constraints.

---

## Conclusion for Web Documentation

When presenting UET on the public documentation site (`docs.uet.ai`), we must avoid promising that a single `pip install` will magically configure the entire research verification suite. 

The primary CTA (Call to Action) should always be the **Python Library Install**, while the **Topic Verification** path should be prominently featured in the scientific documentation sections.
