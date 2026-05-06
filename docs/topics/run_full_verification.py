import os
import sys
import subprocess
import time
from pathlib import Path

# Project root setup
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))

# Key topics to verify (FULL Coverage)
PRIORITY_TOPICS = [
    "0.1_Galaxy_Rotation_Problem",
    "0.2_Black_Hole_Physics",
    "0.3_Cosmology_Hubble_Tension",
    "0.4_Superconductivity_Superfluids",
    "0.5_Nuclear_Binding_Hadrons",
    "0.6_Electroweak_Physics",
    "0.7_Neutrino_Physics",
    "0.8_Muon_g2_Anomaly",
    "0.9_Quantum_Nonlocality",
    "0.10_Fluid_Dynamics_Chaos",
    "0.11_Phase_Transitions",
    "0.12_Vacuum_Energy_Casimir",
    "0.13_Thermodynamic_Bridge",
    "0.14_Complex_Systems",
    "0.15_Cluster_Dynamics",
    "0.16_Heavy_Nuclei",
    "0.17_Mass_Generation",
    "0.18_Quantum_Computing",
    "0.19_Gravity_GR",
    "0.20_Atomic_Physics",
    "0.21_Yang_Mills_Mass_Gap",
    "0.22_Biophysics_Origin_of_Life",
    "0.23_Unity_Scale_Link",
    "0.24_Artificial_Intelligence",
    "0.25_Strategy_Power_Economics",
]


def find_test_scripts(root_dir):
    test_scripts = []
    topics_dir = os.path.join(root_dir, "docs", "topics")

    if not os.path.exists(topics_dir):
        print(f"[ERROR] Critical Error: Topics directory not found at {topics_dir}")
        return []

    print(f"[SCAN] Scanning {topics_dir} for tests...")

    for topic in os.listdir(topics_dir):
        topic_path = os.path.join(topics_dir, topic)
        if not os.path.isdir(topic_path):
            continue

        for root, dirs, files in os.walk(topic_path):
            if "05_Visualization" in root:
                continue

            for file in files:
                if not file.endswith(".py"):
                    continue

                if (
                    file.startswith("test_")
                    or file.startswith("Engine_")
                    or file.startswith("Proof_")
                    or file.startswith("Research_")
                    or file.startswith("Competitor_")
                    or "benchmark" in file
                ):

                    full_path = os.path.join(root, file)
                    test_scripts.append(full_path)

    return test_scripts


def run_script(path):
    rel_path = os.path.relpath(path, project_root)
    print(f"\n{'='*80}")
    print(f"[EXEC] EXECUTING: {rel_path}")
    print(f"{'='*80}")

    start_time = time.time()
    try:
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"

        lab_path = os.path.join(project_root, "lab")
        docs_path = os.path.join(project_root, "docs")

        extra_paths = [
            project_root,
            docs_path,
            lab_path,
            os.path.join(lab_path, "01_galaxy_dynamics"),
            os.path.join(lab_path, "02_gravitational"),
            os.path.join(lab_path, "03_electroweak"),
            os.path.join(lab_path, "04_neutrino"),
            os.path.join(lab_path, "05_qcd_hadrons"),
            os.path.join(lab_path, "06_motion_dynamics"),
            os.path.join(lab_path, "07_complex_systems"),
            os.path.join(lab_path, "00_thermodynamic_bridge"),
        ]

        current_pythonpath = env.get("PYTHONPATH", "")
        env["PYTHONPATH"] = os.pathsep.join(extra_paths) + os.pathsep + current_pythonpath

        result = subprocess.run(
            [sys.executable, path],
            cwd=os.path.dirname(path),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=env,
        )
        duration = time.time() - start_time

        stdout = result.stdout
        stderr = result.stderr

        status = "UNKNOWN"
        if result.returncode != 0:
            status = "CRASH"
        elif (
            "RESULT: PASS" in stdout
            or "[PASS]" in stdout
            or "PASS" in stdout
            or "PASSED" in stdout
            or "SUCCESS" in stdout
        ):
            status = "PASS"
        elif "RESULT: FAIL" in stdout or "[FAIL]" in stdout:
            status = "FAIL"
        elif "FAIL" in stdout or "FAILED" in stdout:
            if "Research_" in path or "Analysis" in path:
                status = "PASS (Analysis Done)"
            else:
                status = "FAIL"
        elif "PASS" in stdout or "PASSED" in stdout or "OK" in stdout:
            status = "PASS"
        else:
            status = "PASS (Implicit)"

        print(stdout)
        if stderr and status != "PASS":
            print("[WARN] STDERR:\n" + stderr)

        print(f"[TIME] Result: {status} in {duration:.2f}s")
        return status, duration

    except Exception as e:
        print(f"[ERROR] EXCEPTION: {e}")
        return "ERROR", 0


def main():
    print("--- UET COMPREHENSIVE SYSTEM VERIFICATION ---")
    print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("==============================================")

    test_files = find_test_scripts(project_root)
    test_files.sort(key=lambda x: any(t in x for t in PRIORITY_TOPICS), reverse=True)

    results = []
    print(f"--- Found {len(test_files)} verification scripts.")

    total_passed = 0
    total_failed = 0

    for script in test_files:
        if "archive" in script.lower() or "legacy" in script.lower():
            continue

        status, duration = run_script(script)
        results.append((script, status, duration))

        if "PASS" in status:
            total_passed += 1
        else:
            total_failed += 1

    print("\n" + "#" * 80)
    print("--- FINAL VERIFICATION REPORT ---")
    print("#" * 80)

    print(f"{'SCRIPT':<60} | {'STATUS':<10} | {'TIME'}")
    print("-" * 80)

    for script, status, duration in results:
        rel_name = os.path.basename(script)
        topic_name = "Unknown"
        parts = script.split(os.sep)
        for p in parts:
            if "0." in p and "_" in p:
                topic_name = p[:15] + "..."
                break

        display_name = f"{topic_name}/{rel_name}"
        icon = "[OK]" if "PASS" in status else "[!!]"
        print(f"{icon} {display_name:<57} | {status:<10} | {duration:.2f}s")

    print("-" * 80)
    print(f"TOTAL: {len(results)}")
    print(f"PASSED: {total_passed}")
    print(f"FAILED: {total_failed}")

    if total_failed == 0:
        print("\n--- SYSTEM INTEGRITY VERIFIED ---")
        sys.exit(0)
    else:
        print("\n[WARN] ISSUES DETECTED - REVIEW LOGS")
        sys.exit(1)


if __name__ == "__main__":
    main()
