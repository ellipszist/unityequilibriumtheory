from pathlib import Path
import csv,json,tempfile
ROOT=Path(__file__).resolve().parents[2]
RAW=Path("docs/data/external/economics/global/wdi/2026-07-16")
OUT=ROOT/"Data/03_Research/uet_global_wdi_panel.csv"
ART=ROOT/"Result/artifacts/0_25_global_wdi_panel.json"
def main():
 s={}
 for p in RAW.glob("*.json"):
  if p.name=="source_manifest.json": continue
  d=json.loads(p.read_text())
  for x in d[1]:
   c=x.get("country",{}).get("id"); y=x.get("date"); v=x.get("value")
   if c and y and v is not None:s.setdefault((c,int(y)),{})[p.stem]=float(v)
 rows=[{"country_code":c,"year":y,**v} for (c,y),v in sorted(s.items()) if len(v)==3]
 fields=["country_code","year"]+sorted({k for r in rows for k in r if k not in {"country_code","year"}});OUT.parent.mkdir(parents=True,exist_ok=True)
 with tempfile.NamedTemporaryFile("w",newline="",encoding="utf-8",delete=False,dir=OUT.parent) as h: w=csv.DictWriter(h,fieldnames=fields);w.writeheader();w.writerows(rows);t=Path(h.name)
 t.replace(OUT)
 cov={};[cov.setdefault(r["country_code"],set()).add(r["year"]) for r in rows]; n=sum(len(v)>=20 for v in cov.values()); a={"schema_version":"1.0","status":"PASS" if n>=30 else "WARN","rows":len(rows),"countries_with_20_plus_years":n,"panel_path":str(OUT).replace("\\","/"),"missingness_policy":"no imputation"};ART.parent.mkdir(parents=True,exist_ok=True);ART.write_text(json.dumps(a,indent=2)+"\n");print("Global WDI panel:",a["status"],len(rows),n)
if __name__=="__main__":main()
