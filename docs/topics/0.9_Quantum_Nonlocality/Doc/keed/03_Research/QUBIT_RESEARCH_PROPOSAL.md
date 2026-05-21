# 🧬 Research Proposal: Qubit Mechanics in UET Matrix
> [!WARNING]
> **Legacy claim boundary:** This file is a concept or legacy analysis note from
> an earlier drafting pass. It is not the topic status authority and must not be
> used to claim UET proves nonlocality, derives CHSH from first principles,
> reconstructs raw Bell event counts, replaces standard quantum theory, or
> transfers CHSH PASS to qubit/double-slit/tunneling lanes. Current allowed
> claims are controlled by `README.md`, `LIMITATIONS.md`, `VERIFICATION_SPEC.md`,
> `DATA_MANIFEST.md`, and
> `Result/artifacts/0_9_quantum_nonlocality_verification.json`.

## 1. Objective
To simulate a **Single Qubit** (Transmon Type) using the UET Matrix Engine, verifying that "Quantum State" equates to "Information Equilibrium Vector" and that "Decoherence" equates to "Information Entropy Increase".

## 2. Real World Data Source 📊
We will strictly use **IBM Quantum Calibration Data** (Real Hardware Specs).
*   **Device:** `ibmq_manila` (or generic Transmon equivalent)
*   **Parameters to Load (JSON):**
    *   **Qubit Frequency ($f_{01}$):** ~4.9 GHz
    *   **T1 (Energy Relaxation Time):** ~154 $\mu s$
    *   **T2 (Dephasing Time):** ~68 $\mu s$
    *   **Anharmonicity:** ~ -340 MHz

**Reference:** *IBM Quantum Services - System Calibration Logs (2024)* or *Koch et al. (2007) "Charge-insensitive qubit design derived from the Cooper pair box".*

## 3. Implementation Plan 🛠️
We will create `Research_Qubit_Mechanics.py` in `topics/0.9_Quantum_Nonlocality`.

### Step 1: Data Loader
*   Script will load `ibm_qubit_calibrations.json` (Real Data).
*   **NO HARDCODING:** Values must come from the file.

### Step 2: The UET Model (The "Why")
Standard QM uses the Schrödinger Equation ($i\hbar \dot{\psi} = H \psi$).
**UET Matrix Engine** uses the Master Equation:
*   **State Vector ($\psi$):** Represented by the **Information Flux Vector** ($\vec{J}_I = \sigma \cdot \vec{v}$) in the Matrix.
*   **Bloch Sphere:** The 3D orientation of the Equilibrium State.
*   **Rabi Oscillation:** Applying an external "Force" (Microwave Pulse) rotates the vector.
*   **Decoherence (T1/T2):** The `diffusion` term in Matrix Engine naturally causes the focused vector to "smear out" over time.
    *   *Hypothesis:* **T1/T2 arises from $\kappa$ (Space Impedance) and $\beta$ (Coupling).**

### Step 3: Validation Experiment
1.  **Initialize:** Start in state $|1\rangle$ (Excited).
2.  **Decay:** Let the engine run without drive.
3.  **Measure:** Track the "Vector Magnitude" vs Time.
4.  **Grading:**
    *   Does it follow exponential decay $e^{-t/T1}$?
    *   Does the derived $T1$ match the loaded IBM Data?

## 4. Expected Outcome
*   **PASS:** If UET's `diffusion` constant naturally predicts exponential decay matching real hardware timescale.
*   **FAIL:** If decay is linear or instantaneous.

## 5. Approval Request
Do you approve this methodology? Specifially the use of **IBM Quantum Data** as the ground truth?
