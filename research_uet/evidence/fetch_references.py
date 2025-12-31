"""
Fetch Reference Papers
======================
Downloads open-access scientific papers (PDFs) for UET validation evidence.
Sources: arXiv, EuroFusion, etc.
"""

import os
import urllib.request
import time

SAVE_DIR = "research_uet/evidence/papers_pdf"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

# (Name, arXiv_ID or URL, Filename)
PAPERS = [
    # --- GRAVITY ---
    (
        "SPARC Galaxy Data (Lelli 2016)",
        "https://arxiv.org/pdf/1606.09251.pdf",
        "Gravity_Lelli2016_SPARC.pdf",
    ),
    (
        "LITTLE THINGS Dwarfs (Oh 2015)",
        "https://arxiv.org/pdf/1502.01281.pdf",
        "Gravity_Oh2015_LITTLE_THINGS.pdf",
    ),
    # --- BLACK HOLES ---
    (
        "EHT M87* Shadow (Paper I)",
        "https://arxiv.org/pdf/1906.11238.pdf",
        "BlackHole_EHT2019_M87.pdf",
    ),
    (
        "LIGO GW150914 Discovery",
        "https://arxiv.org/pdf/1602.03837.pdf",
        "BlackHole_LIGO2016_GW150914.pdf",
    ),
    # --- NEUTRINOS ---
    (
        "KATRIN Neutrino Mass (2022)",
        "https://arxiv.org/pdf/2105.08533.pdf",
        "Neutrino_KATRIN2022_Limit.pdf",
    ),
    (
        "Borexino CNO Cycle (2020)",
        "https://arxiv.org/pdf/2006.15115.pdf",
        "Neutrino_Borexino2020_CNO.pdf",
    ),
    # --- QUANTUM ---
    (
        "Bell Inequality Loophole-Free (Hensen 2015)",
        "https://arxiv.org/pdf/1508.05949.pdf",
        "Quantum_Hensen2015_Bell.pdf",
    ),
    # --- STRONG/WEAK ---
    (
        "Lattice QCD Scale Setting (Sommer 2014)",
        "https://arxiv.org/pdf/1401.3270.pdf",
        "Strong_Sommer2014_QCD.pdf",
    ),
]


def fetch_papers():
    print(f"Downloading {len(PAPERS)} papers to {SAVE_DIR}...\n")

    for name, url, filename in PAPERS:
        filepath = os.path.join(SAVE_DIR, filename)

        if os.path.exists(filepath):
            print(f"[SKIP] {filename} (Already exists)")
            continue

        print(f"[DOWNLOADING] {name}...")
        try:
            # Fake user agent to avoid 403 forbidden
            req = urllib.request.Request(
                url,
                data=None,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                },
            )

            with urllib.request.urlopen(req) as response, open(filepath, "wb") as out_file:
                data = response.read()
                out_file.write(data)

            print(f"   -> Success! ({len(data)/1024:.1f} KB)")
            time.sleep(2)  # Be nice to arXiv API
        except Exception as e:
            print(f"   -> FAILED: {e}")

    # Create manifest file for manual downloads
    manifest_path = os.path.join(SAVE_DIR, "MANUAL_DOWNLOADS.md")
    with open(manifest_path, "w") as f:
        f.write("# References Requiring Manual Download/Subscription\n\n")
        f.write("| Topic | Paper | Source | Link |\n")
        f.write("|---|---|---|---|\n")
        f.write(
            "| Plasma | JET 69MJ Record (2024) | EuroFusion | [Press Release](https://www.euro-fusion.org/news/2024/jet-record) |\n"
        )
        f.write(
            "| Superfluid | He-4 Lambda Point | NIST | [NIST Webbook](https://webbook.nist.gov/) |\n"
        )
        f.write(
            "| Strong | PDG 2024 Review | Particle Data Group | [PDG Live](https://pdglive.lbl.gov/) |\n"
        )

    print(f"\nManifest created at {manifest_path}")


if __name__ == "__main__":
    fetch_papers()
