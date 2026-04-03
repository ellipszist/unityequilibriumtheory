"""
Topic 0.34 Competitor Analysis: ASML vs. UET-ICN
==============================================
Benchmarking logistical complexity and capital expenditure.

Data Source:
-----------
- ASML Annual Report 2023 (EUV Specs)
- UET Topic 0.34 (ICN Theoretical Specs)
"""

import numpy as np

def run_benchmark():
    print("📉 COMPETITOR BENCHMARK: Industrial Paradigm Shift")
    print("-" * 50)
    
    metrics = {
        "Parameter": ["CAPEX (Machine Cost)", "Supply Chain Complexity", "Throughput (WPH)", "Energy / Gate (J)", "Mask Cost (per Layer)"],
        "ASML_EUV": ["$350M - $400M", "800+ Tier-1 Suppliers", "160 wafers/hr", "2.0e-4 J", "$500k+"],
        "UET_ICN": ["$5M - $10M (Est)", "Local Field Control", "300 wafers/hr (Est)", "1.5e-12 J", "$0 (Software Defined)"]
    }
    
    # 1. Supply Chain Drag (Information Cost I)
    # ASML = High Information Drag (Massive logistics)
    # ICN = Low Information Drag (Localized control)
    
    print(f"{'Metric':<25} | {'ASML EUV':<20} | {'UET ICN':<20}")
    print("-" * 75)
    for i in range(len(metrics["Parameter"])):
        print(f"{metrics['Parameter'][i]:<25} | {metrics['ASML_EUV'][i]:<20} | {metrics['UET_ICN'][i]:<20}")
    
    print("-" * 75)
    print("\n🔍 STRATEGIC INSIGHT (Axiom 2):")
    print("The real 'Necessity' is to decouple manufacturing from geopolitics.")
    print("ASML depends on Carl Zeiss (Optics) and TRUMPF (Laser).")
    print("UET ICN depends on local Information Resonators.")
    print("By moving the complexity into the Software Layer (Pattern I),")
    print("we reduce the Industrial Drag (Mass C) in the supply chain.")
    print("-" * 50)

if __name__ == "__main__":
    run_benchmark()
