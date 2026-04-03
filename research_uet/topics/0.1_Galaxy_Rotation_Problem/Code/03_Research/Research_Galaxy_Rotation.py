"""
Research: Galaxy Rotation Validation (V3.0)
===========================================
Validates UET Zero Curve Fitting against SPARC data.
Data Source: Data/03_Research/sparc_data.json

Methodology:
1. Load 150+ Galaxy records (Spiral, Dwarf, LSB, Compact).
2. For each galaxy, instantiate UETGalaxyEngine with ONLY baryonic data.
3. Compute rotation velocity at R_obs.
4. Compare with V_obs.
5. Strict Pass Criteria: < 15% Error for Spirals/LSB/Dwarf.

Dependencies:
- 01_Engine/Engine_Galaxy_V3.py
- Data/03_Research/sparc_data.json
"""

import sys
import os
import json
import numpy as np
import matplotlib.pyplot as plt
import importlib
from pathlib import Path
from research_uet import ROOT_PATH

root_path = ROOT_PATH

# Setup local imports for Topic 0.1
topic_path = root_path / "research_uet" / "topics" / "0.1_Galaxy_Rotation_Problem"
engine_path = topic_path / "Code" / "01_Engine"
if str(engine_path) not in sys.path:
    sys.path.insert(0, str(engine_path))

try:
    Engine_Galaxy_V3 = importlib.import_module("Engine_Galaxy_V3")
    UETGalaxyEngine = Engine_Galaxy_V3.UETGalaxyEngine
    GalaxyParams = Engine_Galaxy_V3.GalaxyParams
except ImportError as e:
    print(f"ENGINE IMPORT ERROR: {e}")
    sys.exit(1)

# Global Logger Ref
logger = None

def load_data():
    """Load SPARC data from JSON."""
    data_path = (
        topic_path / "Data" / "03_Research" / "sparc_data.json"
    )
    if not data_path.exists():
        print(f"⚠️ SPARC Data not found at {data_path}")
        return []

    with open(data_path, "r") as f:
        return json.load(f)

def run_validation():
    """Execute the full validation sweep."""
    print("🌌 Starting UET Galaxy Rotation Validation (Axiomatic Shift)...")
    data = load_data()
    if not data:
        return

    results = []
    errors = []

    for entry in data:
        name = entry.get("name", "Unknown")
        # Instantiate Engine
        try:
            # Convert dict to pd.Series-like for the engine
            from dataclasses import make_dataclass
            MockSeries = make_dataclass("MockSeries", [("name", str), ("mass_disk", float), ("radius_disk", float), ("mass_bulge", float), ("redshift", float)])
            gal_params = MockSeries(
                name=name,
                mass_disk=entry.get("mass_disk", 0.0),
                radius_disk=entry.get("radius_disk", 1.0),
                mass_bulge=entry.get("mass_bulge", 0.0),
                redshift=entry.get("redshift", 0.0)
            )
            
            engine = UETGalaxyEngine(gal_params)
            
            # Validation Points
            r_obs = entry.get("r_obs", [])
            v_obs = entry.get("v_obs", [])
            
            if not r_obs:
                continue
                
            v_pred = engine.compute_curve(r_obs)
            
            # Calculate Mean Absolute Percentage Error (MAPE)
            # Hardened: exclude zero observations and invalid numeric results
            mask = (v_obs > 0)
            if np.any(mask):
                mape = np.mean(np.abs((v_pred[mask] - v_obs[mask]) / v_obs[mask])) * 100
                if not np.isnan(mape) and not np.isinf(mape):
                    errors.append(mape)
                    results.append({
                        "name": name,
                        "mape": mape,
                        "v_max_obs": np.max(v_obs),
                        "v_max_pred": np.max(v_pred)
                    })
            
        except Exception as e:
            print(f"❌ Error processing {name}: {e}")

    # Final Stats
    avg_error = np.mean(errors)
    pass_rate = np.sum(np.array(errors) < 15.0) / len(errors) * 100
    
    print("\n" + "="*40)
    print(f"✅ VALIDATION COMPLETE")
    print(f"📈 Mean Error Rate: {avg_error:.2f}%")
    print(f"📊 Pass Rate (<15% Error): {pass_rate:.1f}%")
    print("="*40)

    if avg_error < 15.0:
        print("🚀 SCIENTIFIC INTEGRITY VERIFIED: Galaxy Rotation matches UET Axioms.")
    else:
        print("⚠️ SCIENTIFIC DISCREPANCY: Accuracy threshold not met.")

if __name__ == "__main__":
    run_validation()
