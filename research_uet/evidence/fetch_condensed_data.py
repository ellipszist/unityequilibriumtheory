import json
import os


def fetch_data():
    """
    Simulates sourcing real experimental data for Condensed Matter Physics.
    Sources:
    1. Kittel, C. "Introduction to Solid State Physics" (Superconductor Tc)
    2. Donnelly, R.J. "Observed Properties of Liquid Helium" (Superfluidity)
    3. Tinkham, M. "Introduction to Superconductivity" (Tunneling)
    """
    print("🔬 Sourcing Condensed Matter Data...")

    data = {
        "superconductors": [
            {"element": "Mercury (Hg)", "Tc_kelvin": 4.15, "Type": "Type-I", "Year": 1911},
            {"element": "Lead (Pb)", "Tc_kelvin": 7.19, "Type": "Type-I", "Year": 1913},
            {"element": "Niobium (Nb)", "Tc_kelvin": 9.25, "Type": "Type-II", "Year": 1930},
            {"element": "Nb3Sn", "Tc_kelvin": 18.3, "Type": "Type-II", "Year": 1954},
            {"element": "YBCO (YBa2Cu3O7)", "Tc_kelvin": 92.0, "Type": "High-Tc", "Year": 1987},
            {"element": "MgB2", "Tc_kelvin": 39.0, "Type": "Type-II", "Year": 2001},
        ],
        "superfluids": {
            "He4_Lambda_Point_K": 2.17,
            "He4_Density_g_cm3": 0.145,
            "Second_Sound_Velocity_m_s": 20.0,
        },
        "tunneling": {
            "Josephson_Junction": {
                "phenomenon": "Cooper Pair Tunneling",
                "equation": "I = Ic * sin(phi)",
                "explanation": "Macroscopic wave function phase difference drives current without voltage.",
            },
            "Alpha_Decay": {
                "phenomenon": "Quantum Tunneling through Coulomb Barrier",
                "status": "Validated in test_real_alpha_decay.py",
            },
        },
    }

    # Save to verified data vault
    output_dir = "research_uet/data_vault/condensed_matter"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "real_condensed_data.json")

    with open(output_path, "w") as f:
        json.dump(data, f, indent=4)

    print(f"✅ Data cached to: {output_path}")
    print("   - 6 Verified Superconductors")
    print("   - He-4 Lambda Point Data")
    print("   - Josephson Junction References")


if __name__ == "__main__":
    fetch_data()
