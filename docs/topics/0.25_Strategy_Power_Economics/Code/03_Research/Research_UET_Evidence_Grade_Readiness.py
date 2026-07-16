from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/"Result/artifacts/0_25_evidence_grade_readiness.json"
SUB=ROOT/"Result/artifacts"
NAMES={"source_and_panel":"0_25_uet_economics_verification.json","measurement_validity":"0_25_uet_measurement_validity_audit.json","causal_identification":"0_25_causal_identification_gate.json","global_replication":"0_25_global_replication_readiness.json","independent_replication":"0_25_independent_replication_gate.json","publication_review":"0_25_publication_hardening_gate.json","regional_robustness":"0_25_global_wdi_leave_one_region_out.json"}
def main():
 checks={}
 for k,n in NAMES.items():
  d=json.loads((SUB/n).read_text(encoding="utf-8"));checks[k]=d.get("status")
 critical=[k for k,v in checks.items() if v not in {"PASS","DIAGNOSTIC_COMPLETE"}]
 out={"schema_version":"1.0","topic":"0.25_Strategy_Power_Economics","status":"BLOCKED" if critical else "CANDIDATE","target":"Evidence Grade A","checks":checks,"controlling_blockers":critical,"promotion_rule":"All critical source, measurement, causal, global, independent-replication, and publication checks must be PASS; no WARN/BLOCKED critical gate may be averaged away.","claim_boundary":"Current evidence supports only source-locked descriptive diagnostics. This readiness artifact does not promote Claim Class C."};ART.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print('Evidence Grade readiness:',out['status'],critical)
if __name__=="__main__":main()
