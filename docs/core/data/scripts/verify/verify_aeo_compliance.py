import os
import json
import re

def audit_aeo():
    # Fix: Get absolute path relative to script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # The script is in docs/scripts/verify/, so topics is at ../../../topics
    base_dir = os.path.abspath(os.path.join(script_dir, "..", "..", "topics"))
    
    if not os.path.exists(base_dir):
        print(f"❌ Error: Cannot find topics directory at {base_dir}")
        return

    report = []
    
    # Get all topic directories
    topics = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d)) and d[0].isdigit()]
    topics.sort()

    print(f"Auditing {len(topics)} topics for AEO v2.0 compliance...\n")

    for topic in topics:
        readme_path = os.path.join(base_dir, topic, "README.md")
        status = {"topic": topic, "schema": "❌ MISSING", "digest": "❌ MISSING", "pass": False}
        
        if os.path.exists(readme_path):
            with open(readme_path, "r", encoding="utf-8") as f:
                content = f.read()
                
                # Check for Schema.org (JSON-LD or Microdata)
                has_json_ld = '"@context": "https://schema.org"' in content
                has_microdata = 'itemtype="https://schema.org/' in content or 'itemtype="http://schema.org/' in content
                
                if has_json_ld or has_microdata:
                    status["schema"] = "✅ VALID"
                
                # Check for AI-Digest (EN/TH)
                if "> [!NOTE]" in content and "AI-Digest" in content:
                    status["digest"] = "✅ VALID"
                    
                if status["schema"] == "✅ VALID" and status["digest"] == "✅ VALID":
                    status["pass"] = True
        else:
            status["schema"] = "❌ NO README"
            status["digest"] = "❌ NO README"
            
        report.append(status)

    # Generate Formatted Report
    print(f"{'Topic ID':<45} | {'Schema.org':<12} | {'AI-Digest':<12}")
    print("-" * 75)
    for r in report:
        print(f"{r['topic']:<45} | {r['schema']:<12} | {r['digest']:<12}")

    passed_count = sum(1 for r in report if r["pass"])
    if len(topics) > 0:
        print(f"\nSummary: {passed_count}/{len(topics)} topics passed ({(passed_count/len(topics))*100:.1f}%)")
    else:
        print("\nSummary: No topics found to audit.")

if __name__ == "__main__":
    audit_aeo()
