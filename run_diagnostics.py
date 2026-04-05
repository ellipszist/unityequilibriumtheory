import sys
from pathlib import Path
import os
import json
import re

# Add research_uet to path
sys.path.append(os.path.abspath("."))

from research_uet.topics.run_all_tests import find_all_tests, run_test

def main():
    print("Starting UET Diagnostics Sweep...")
    tests = find_all_tests()
    failures = []
    
    for t in tests:
        res = run_test(t["path"])
        if not res["passed"] or res["passed_count"] < res["total_count"]:
            solution = t["solution"]
            name = t["name"]
            output = res["output"]
            
            # Extract traceback or failure reason
            err_reason = output[-2000:] if len(output) > 2000 else output
            
            print(f"[!] FAILED: {solution} / {name}")
            failures.append({
                "topic": solution,
                "script": name,
                "error": err_reason
            })
        else:
            print(f"[OK] {t['solution']} / {t['name']}")

    with open("diagnostics_results.json", "w", encoding="utf-8") as f:
        json.dump(failures, f, indent=2)
        
    print(f"Diagnostics complete. {len(failures)} tests failed. Results saved to diagnostics_results.json")

if __name__ == "__main__":
    main()
