# Claim Inventory

This inventory tracks repository-level wording that affects credibility and public
interpretation. It is a working governance artifact, not a scientific paper.

| Claim text | Previous wording | Evidence source | Code or script | Dataset or citation | Baseline | Confidence level | Approved public wording |
|:--|:--|:--|:--|:--|:--|:--|:--|
| UET repository status | "400+ Verified" / "Platinum Standard" | Repository inspection | N/A | N/A | N/A | Low | Repository metadata is standardized in the current release; scientific support remains topic-specific. |
| Galaxy rotation topic | "Zero curve fitting" | Topic README and verification scripts | `Research_Galaxy_Rotation.py`, `Verify_Galaxy_Rotation.py` | `sparc_data.json`, SPARC citation | Comparator scripts in topic | Medium | Internal numerical agreement is reported against selected galaxy datasets; fitting status must be stated explicitly where parameters are optimized. |
| Hubble tension topic | "Resolves the 5 sigma tension" | Topic README and research scripts | Topic research scripts | Planck 2018, SH0ES 2022 | LCDM as documented comparator | Low to medium | Repository documentation presents a proposed mechanism and internal benchmark comparisons for the Hubble-tension topic. |
| Fluid dynamics topic | "Solve the Navier-Stokes Millennium Problem" | Topic README and benchmark docs | Topic engine and benchmark scripts | Canonical fluid references and internal configs | Navier-Stokes benchmark implementation | Low | Repository documentation reports an alternative internal solver formulation and benchmark claims that require topic-level review. |
| Yang-Mills topic | "Mass gap proved" | Topic README | Topic engine/proof scripts | Lattice-QCD benchmarks cited in topic | Published benchmark values | Low | Repository documentation currently treats the Yang-Mills mass-gap topic as a hypothesis-driven internal module, not a resolved Clay problem. |
