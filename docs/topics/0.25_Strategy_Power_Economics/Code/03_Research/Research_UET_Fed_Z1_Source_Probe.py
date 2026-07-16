from pathlib import Path
import json,zipfile
ROOT=Path(__file__).resolve().parents[2]
ZIP=Path("docs/data/external/economics/us_historical/fed_z1/2026-07-16/z1_csv_files.zip")
ART=ROOT/"Result/artifacts/0_25_fed_z1_source_probe.json"
def main():
 with zipfile.ZipFile(ZIP) as z:names=z.namelist()
 tables=[n.split("/")[-1] for n in names if n.endswith(".csv")];transaction=[n for n in tables if n.startswith("F") and "_t" in n];levels=[n for n in tables if n.startswith("L")];sector=[n for n in tables if n.startswith("S")];out={"schema_version":"1.0","status":"PASS" if len(transaction)>=20 and len(levels)>=20 else "WARN","release_vintage":"2026:Q1 current release","zip_path":str(ZIP).replace("\\","/"),"table_counts":{"all_csv":len(tables),"transaction_tables":len(transaction),"levels_tables":len(levels),"sector_tables":len(sector)},"sample_transaction_tables":transaction[:20],"sample_levels_tables":levels[:20],"coverage_policy":"Use observations through 2024 only for the Topic primary freeze; preserve current-release vintage separately.","claim_boundary":"Z.1 provides sectoral financial-account evidence, not anonymous individual payment provenance; variable mapping and accounting reconciliation are required before causal use.","blockers":["No preregistered mapping yet links specific Z.1 instrument/sector columns to labor/resource/output transactions.","Current release is revised 2026 vintage; a historical-as-of release comparison is still required for revision control."]};ART.write_text(json.dumps(out,indent=2)+"\n");print("Fed Z1 source probe:",out["status"],out["table_counts"])
if __name__=="__main__":main()
