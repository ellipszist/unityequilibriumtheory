import sys
import json
import subprocess
import os
import re

target_scripts = [
    "Engine_Omni.py",
    "Verify_Omni.py",
    "Proof_Turbulence_Benchmarks.py",
    "Engine_Power_Dynamics.py",
    "Proof_Capital_Efficiency.py",
    "Proof_Resource_Cost.py",
    "Research_Bank_Data_Validation.py",
    "Research_Central_Bank_Digital_Currency.py",
    "Research_Global_Debt_Reset.py",
    "Research_Nature_Capital.py",
    "Research_Universal_Basic_Needs.py",
    "Scenario_Hyperinflation.py",
    "Research_Perovskite_LARP.py",
    "Research_Hubble_Comparison.py"
]

failed = []
base = r"c:\Users\santa\Desktop\uet_harness\research_uet\topics"

for root, _, files in os.walk(base):
    for f in files:
        if f in target_scripts:
            path = os.path.join(root, f)
            print(f"Running targeted: {f}...")
            env = dict(os.environ, PYTHONPATH=r"c:\Users\santa\Desktop\uet_harness")
            res = subprocess.run(
                [sys.executable, "-X", "utf8", path], 
                cwd=root, 
                env=env, 
                capture_output=True, 
                text=True, 
                encoding="utf-8", 
                errors="replace"
            )
            
            output = res.stdout + res.stderr
            # Check for generic failure or explicit string flags
            passed = res.returncode == 0
            match = re.search(r"(\d+)/(\d+)\s*PASS", output)
            if match and int(match.group(1)) < int(match.group(2)):
                passed = False
            if "Status: FAIL" in output:
                passed = False
                
            if not passed:
                err = output[-2000:]
                failed.append({
                    "script": f,
                    "error": err
                })

with open(r"c:\Users\santa\Desktop\uet_harness\targeted_diag.json", "w", encoding="utf-8") as out:
    json.dump(failed, out, indent=2)

print(f"Targeted Diagnostics done: {len(failed)} failures recorded in targeted_diag.json")
