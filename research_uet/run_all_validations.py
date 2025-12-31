"""
🔬 UET Master Validation Runner
================================
รันทุก Test Script และบันทึกผลลัพธ์ไปยัง validation_outputs/

Usage:
    python run_all_validations.py
"""

import subprocess
import os
import sys
from datetime import datetime

# Output directory
OUTPUT_DIR = "validation_outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# All test scripts to run
TESTS = [
    # === GALAXIES ===
    ("Galaxies (SPARC 154)", "lab/galaxies/test_175_galaxies_v4.py"),
    # === FUNDAMENTAL FORCES ===
    ("Strong Force (Binding)", "lab/strong_nuclear/test_strong_force.py"),
    ("Weak Force (Neutrino)", "lab/weak_nuclear/test_weak_force.py"),
    ("EM (Casimir)", "lab/electromagnetic/casimir_test.py"),
    ("Quantum", "lab/quantum/test_quantum_mechanics.py"),
    # === CONDENSED MATTER ===
    ("Superconductivity", "lab/condensed_matter/test_superconductivity.py"),
    ("Superfluidity", "lab/condensed_matter/test_superfluidity.py"),
    ("Josephson Tunneling", "lab/condensed_matter/test_josephson_tunneling.py"),
    # === ASTROPHYSICS ===
    ("Black Holes", "lab/black_holes/test_black_holes.py"),
    ("Plasma (JET/Parker)", "lab/plasma/test_plasma_physics.py"),
    # === COSMOLOGY ===
    ("Cosmology (Hubble)", "evidence/test_real_cosmology.py"),
    ("Cosmic History", "evidence/run_cosmic_history.py"),
]


def run_test(name, script_path):
    """Run a single test and capture output."""
    full_path = os.path.join(os.path.dirname(__file__), script_path)

    if not os.path.exists(full_path):
        return f"SKIP: File not found: {script_path}"

    try:
        # Fix Windows Unicode encoding issue
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"

        result = subprocess.run(
            [sys.executable, full_path],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=os.path.dirname(__file__),
            env=env,
            encoding="utf-8",
            errors="replace",
        )
        output = result.stdout + result.stderr
        if result.returncode == 0:
            return f"PASS\n{output}"
        else:
            return f"ERROR (code {result.returncode})\n{output}"
    except subprocess.TimeoutExpired:
        return "TIMEOUT (>120s)"
    except Exception as e:
        return f"EXCEPTION: {e}"


def main():
    print("=" * 70)
    print("🔬 UET MASTER VALIDATION RUNNER")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    print()

    results = []
    passed = 0
    failed = 0
    skipped = 0

    for name, script in TESTS:
        print(f"🔄 Running: {name}...")
        output = run_test(name, script)

        # Count results
        if output.startswith("PASS"):
            passed += 1
            status = "PASS"
        elif output.startswith("SKIP"):
            skipped += 1
            status = "SKIP"
        else:
            failed += 1
            status = "FAIL"

        results.append((name, status, output))

        # Save individual output
        safe_name = name.replace(" ", "_").replace("/", "_").replace("(", "").replace(")", "")
        output_file = os.path.join(OUTPUT_DIR, f"{safe_name}.txt")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"# {name}\n")
            f.write(f"# Script: {script}\n")
            f.write(f"# Date: {datetime.now()}\n")
            f.write("=" * 50 + "\n\n")
            f.write(output)

        print(f"   → {status} (saved to {output_file})")

    # Generate summary
    print()
    print("=" * 70)
    print("📊 SUMMARY")
    print("=" * 70)
    print(f"✅ Passed:  {passed}")
    print(f"❌ Failed:  {failed}")
    print(f"⏭️ Skipped: {skipped}")
    print(f"📁 Outputs saved to: {os.path.abspath(OUTPUT_DIR)}/")
    print("=" * 70)

    # Save master summary
    summary_file = os.path.join(OUTPUT_DIR, "MASTER_SUMMARY.md")
    with open(summary_file, "w", encoding="utf-8") as f:
        f.write("# 🔬 UET Validation Summary\n\n")
        f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("## Results\n\n")
        f.write(f"- ✅ Passed: {passed}\n")
        f.write(f"- ❌ Failed: {failed}\n")
        f.write(f"- ⏭️ Skipped: {skipped}\n\n")
        f.write("## Individual Tests\n\n")
        f.write("| Test | Status |\n")
        f.write("| :--- | :---: |\n")
        for name, status, _ in results:
            icon = "✅" if status == "PASS" else ("⏭️" if status == "SKIP" else "❌")
            f.write(f"| {name} | {icon} {status} |\n")

    print(f"\n📝 Summary saved to: {summary_file}")
    print("\n✅ Validation Runner Complete!")


if __name__ == "__main__":
    main()
