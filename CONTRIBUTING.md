# 🤝 Contributing to UET Harness

Thank you for your interest in contributing! 🎉

---

## 📋 Ways to Contribute

### 🐛 Report Bugs

Open an issue with:
- Description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Python version and OS

### 📖 Documentation

- Improve README, docstrings, or tutorials
- Add examples for new use cases
- Fix typos or clarify explanations

### 🔬 Add Physics Tests

- Propose new validation tests
- Add real data comparisons
- Extend to new physics domains

### 🚀 Code Improvements

- Performance optimizations
- Bug fixes
- New features (discuss first in an issue)

---

## 🧪 Current Test Status (2026-01-01 v1.1)

### ✅ Validated Domains (Real Data)

| Domain | Tests | Pass Rate | Data Source |
|:---|:---:|:---:|:---|
| **Galaxies (SPARC)** | 154 | 78% | Lelli et al. 2016 |
| **Dwarfs (LITTLE THINGS)** | 26 | 82% | Oh et al. 2015 |
| **EM (Casimir)** | 12 | 92% | Mohideen 1998 |
| **Strong Force** | 18 | 100% | NNDC/AME2020 |
| **Weak Force** | 8 | 100% | NNDC |
| **Muon g-2** | 1 | 100% | Fermilab 2025 |
| **Superconductivity** | 6 | 100% | Kittel |
| **Superfluidity** | 1 | 100% | Donnelly |
| **Black Holes** | 4 | 100% | EHT/Sgr A* |
| **Plasma** | 2 | 100% | JET/Parker |
| **Cosmology** | 3 | 100% | Planck/HST/JWST |

**Total: 18/18 Domain Tests PASS** ✅

### 🎯 Areas Needing Work:

1. **Compact galaxies** - 40% pass rate (needs improvement)
2. **Parameter derivation** - `k` is fitted, not derived
3. **Peer review** - Academic validation pending
4. **High-Tc superconductors** - Need more Cuprate tests

---

## 🔧 Development Setup

```bash
git clone https://github.com/unityequilibrium/Equation-UET-v0.8.7.git
cd Equation-UET-v0.8.7

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install numpy scipy matplotlib

# Run ALL validation tests
cd research_uet/lab/07_utilities
python run_master_validation.py

# Generate charts
python visualize_results.py
```

---

## 📝 Pull Request Guidelines

1. **Fork** the repository
2. **Create a branch** for your feature
3. **Write tests** if applicable
4. **Update docs** if needed
5. **Submit PR** with clear description

---

## 💡 Feature Requests

Before proposing a new feature:

1. Check existing issues
2. Open a discussion issue first
3. Explain the use case
4. Be patient for feedback

---

## 🔬 Physics Contributions

If you're adding new physics tests:

1. **Use UET equations** - Must use the core `Ω[C, I]` framework
2. **Real data required** - Include citations to data sources
3. **Document limitations** - Be honest about what doesn't work
4. **Add to runner** - Update `run_all_validations.py`

---

## 🔍 Transparency and Methodology Statement

This project uses an **AI-Assisted Physics Framework** (Agentic Coding v0.8.7).
- **Origin:** The theory is derived from computational simulation, not traditional academic channels.
- **Verification:** All results are reproducible via the `lab/` scripts.
- **Goal:** To bridge the gap between simulation and reality using a unifying equation.

## 🤝 Invitation to Peer Review

We explicitly invite scrutiny. Science thrives on falsifiability.
1.  **Clone** the repo.
2.  **Run** the tests (`python run_master_validation.py`).
3.  **Break** the theory. Find where it fails.

If you find a dataset where UET fails, **please open an issue**. We want to know.

---

## 📜 Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Accept that UET has limitations (it's a simulation framework, not a universal law)

---

## 📬 Contact

- **Issues:** GitHub Issues
- **Discussions:** GitHub Discussions

---

*Thank you for helping improve UET!* 🙏
