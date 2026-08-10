# Book 1 Claim Map

> **Version:** `BOOK1-CLAIMS-V3`
> **Default class:** hypothesis or Claim Class C internal diagnostic

| Claim ID | Claim family | Decision | Evidence lane | Allowed wording | Blocked wording |
| --- | --- | --- | --- | --- | --- |
| `B1-C001` | output, wealth, and welfare differ | retain | national/wealth accounts | definitional distinction | GDP is fake |
| `B1-C002` | services can be real output | retain | BEA/BLS accounts | measured service value added | only physical goods are wealth |
| `B1-C003` | GDP omits welfare/externality dimensions | rewrite | distribution/natural capital | GDP is incomplete for welfare | GDP growth is an illusion |
| `B1-C004` | production uses KLEMS inputs | benchmark | KLEMS | standard production accounting | UET law confirmed |
| `B1-C005` | resource transformation follows production networks | test | I-O/USEEIO/CFS | modelled sector footprint | observed invoice lineage |
| `B1-C006` | knowledge/institutions affect productivity | test | R&D/IP/institutions | association or identified effect | knowledge wins all |
| `B1-C007` | constraints affect innovation | rewrite | shock × capacity | sign-ambiguous hypothesis | necessity always creates innovation |
| `B1-C008` | infrastructure can raise capacity | test | capital/project designs | project-specific effect/NPV | borrowing automatically creates wealth |
| `B1-C009` | `R=N+K+I` | retire identity | formula audit | historical mnemonic only | wealth equation/law |
| `B1-C010` | purchasing power is basket specific | retain | CPI/PCE/CE | basket/group result | one scalar money value |
| `B1-C011` | `R/M` measures money value | retire | measurement audit | resource-coverage diagnostic | observed intrinsic value |
| `B1-C012` | Stone-in-Balloon mechanism | rewrite | inflation baselines/shocks | stylized conditional hypothesis | immediate one-for-one fiat dilution |
| `B1-C013` | banks create deposits through lending | retain | monetary accounts | institutional/accounting statement | every loan is costless wealth |
| `B1-C014` | secured debt is productive | rewrite | use-of-proceeds/outcomes | purpose- and outcome-specific finding | collateral guarantees production |
| `B1-C015` | payer money can be traced to resources | bounded | evidence levels L0–L4 | observed/inferred/modelled label | specific-dollar lineage without tag |
| `B1-C016` | productivity-pay gap exists | source-specific | EPI/BLS/CPS | construction-specific estimate | one universal gap |
| `B1-C017` | fiat caused the wage gap | block | causal design absent | no causal claim | fiat caused divergence |
| `B1-C018` | cost of living diverges from GDP | test | household baskets | declared welfare pattern | all households experienced same inflation |
| `B1-C019` | distribution changes welfare interpretation | retain/test | SCF/DFA/WID | distributional finding | average GDP proves welfare |
| `B1-C020` | tax cuts caused buybacks/wage effects | test | firm/policy design | identified estimate if passed | post-hoc causal narrative |
| `B1-C021` | SMEs employ most people | scope-lock | SUSB/BDS/QCEW | country/year/definition statistic | universal majority claim |
| `B1-C022` | upstream power squeezes SMEs/wages | test | I-O/concentration | exposure-based estimate | universal monopoly mechanism |
| `B1-C023` | government cannot create jobs directly | correct | public employment | comparative employment claim | literal impossibility |
| `B1-C024` | leisure creates demand | test | ATUS/CE | competing time-use effects | leisure always raises demand |
| `B1-C025` | tiered labor by nationality | quarantine | Thailand rights review | skill/job policy analysis | nationality-based endorsement |
| `B1-C026` | energy density drove industrialization | rewrite | energy services/history | multicausal transition finding | density alone caused growth |
| `B1-C027` | throughput equals density | block | unit gate | separate constructs | interchangeable terms |
| `B1-C028` | profit equals unpaid entropy | retire identity | externality accounts | private return vs external cost | thermodynamic identity |
| `B1-C029` | firewood was first industry/war target | quarantine | archaeology/history | competing hypothesis | established sequence |
| `B1-C030` | mathematics emerged before language for logistics | quarantine | specialist history | speculative interlude | historical fact |
| `B1-C031` | gold shortage caused Great Depression | rewrite | economic history | one mechanism among several | single-cause account |
| `B1-C032` | energy/resource money is validated | transfer Book 3 | design/simulation | proposal and failure modes | inflation-free/validated peg |
| `B1-C033` | fertility decline was designed | quarantine | demographic causal work | multicausal analysis | intent attribution |
| `B1-C034` | Singapore/HK chose gold hubs to escape fiat | quarantine | policy/trade documents | documented motive only | inferred national intent |
'
$refs=@'
# Book 1 Reference Register

> **Status:** `IN_PROGRESS`; source identity is recorded, but systematic screening and exact locators remain incomplete.

| Source ID | Source | Tier | Role | State | Limitation / next check |
| --- | --- | --- | --- | --- | --- |
| `ECON-001` | BEA–BLS Integrated Industry-Level Production Account (KLEMS), https://www.bea.gov/data/special-topics/integrated-industry-level-production-account-klems | PRIMARY/INSTITUTIONAL | production benchmark | located | lock release vintage and tables |
| `ECON-002` | BEA Input-Output Accounts, https://www.bea.gov/data/industries/input-output-accounts-data | PRIMARY/INSTITUTIONAL | production network | located | fixed-coefficient and aggregation limits |
| `ECON-003` | EPA USEEIO, https://www.epa.gov/land-research/us-environmentally-extended-input-output-useeio-models | PRIMARY/INSTITUTIONAL | modelled environmental footprint | located | not transaction lineage |
| `ECON-004` | Bank of England, Money creation in the modern economy, https://www.bankofengland.co.uk/quarterly-bulletin/2014/q1/money-creation-in-the-modern-economy | AUTHORITATIVE_SECONDARY | bank deposit creation | appraised | UK institutional exposition; compare U.S. sources |
| `ECON-005` | Federal Reserve H.6/FRED M2SL, https://fred.stlouisfed.org/series/M2SL | PRIMARY | monetary aggregate | used | endogenous aggregate; vintage control needed |
| `ECON-006` | Federal Reserve Z.1, https://www.federalreserve.gov/apps/fof/About.htm | PRIMARY | sector sources-and-uses | used | net flows do not earmark payments |
| `ECON-007` | BLS CPI purchasing power, https://www.bls.gov/cpi/factsheets/purchasing-power-constant-dollars.htm | INSTITUTIONAL | internal purchasing power | appraised | basket average |
| `ECON-008` | BLS CPI individual experience, https://www.bls.gov/cpi/factsheets/averages-and-individual-experiences-differ.htm | INSTITUTIONAL | heterogeneity boundary | appraised | requires micro/distributional extension |
| `ECON-009` | Atlanta Fed DCPC, https://www.atlantafed.org/research-and-data/surveys/survey-and-diary-of-consumer-payment-choice | PRIMARY/INSTITUTIONAL | transaction/payment use | located | no complete payer-SKU-resource chain |
| `ECON-010` | BLS productivity and compensation gap, https://www.bls.gov/opub/btn/volume-6/understanding-the-labor-productivity-and-compensation-gap.htm | INSTITUTIONAL | construction comparison | appraised | deflator/universe dependent |
| `ECON-011` | EPI Productivity–Pay Gap, https://www.epi.org/productivity-pay-gap/ | SECONDARY/DATASET | exact source reproduction | used | keep separate from BLS comparator |
| `ECON-012` | EIA Annual Energy Review, https://www.eia.gov/totalenergy/data/annual/ | PRIMARY | energy throughput/history | used | methodology/vintage and heat basis required |
| `ECON-013` | USGS historical mineral statistics, https://www.usgs.gov/centers/national-minerals-information-center/historical-statistics-mineral-commodities-united | PRIMARY | physical material quantities | used | national totals, no payer allocation |
| `ECON-014` | Census Commodity Flow Survey, https://www.census.gov/programs-surveys/cfs/about.html | PRIMARY | shipment value/weight/geography | located | no financing lineage |
| `ECON-015` | SEC EDGAR CompanyFacts API, https://www.sec.gov/search-filings/edgar-application-programming-interfaces | PRIMARY | public-firm funding channels | used | public firms; profit is not cash earmarking |
| `ECON-016` | USAspending, https://www.usaspending.gov/ | PRIMARY | federal awards/obligations/outlays | used | not bank settlement or invoice ledger |
| `ECON-017` | SBA Small Business FAQ 2024, https://advocacy.sba.gov/2024/07/23/frequently-asked-questions-about-small-business-2024/ | INSTITUTIONAL | U.S. small-business scope | appraised | definition/year specific |
| `ECON-018` | OECD Society at a Glance 2024 fertility review, https://www.oecd.org/en/publications/society-at-a-glance-2024_918d8db3-en/ | AUTHORITATIVE_SECONDARY | fertility mechanisms | located | OECD scope; no universal intent inference |
| `ECON-019` | Federal Reserve History, Great Depression, https://www.federalreservehistory.org/essays/great-depression | AUTHORITATIVE_SECONDARY | monetary/history synthesis | appraised | supplement with specialist primary research |
| `ECON-020` | NBER Working Paper 2198, https://www.nber.org/papers/w2198 | PRIMARY_RESEARCH | gold-standard transmission | located | working-paper/version appraisal needed |
| `ECON-021` | World Bank Adjusted Net Savings, https://datacatalog.worldbank.org/search/dataset/0037653/adjusted-net-savings | PRIMARY/INSTITUTIONAL | natural-capital robustness | located | valuation assumptions |
| `ECON-022` | UN SEEA Ecosystem Accounting, https://unstats.un.org/unsd/envaccounting/seearev/eea_final_en.pdf | AUTHORITATIVE_STANDARD | environmental accounts | located | monetary/physical accounts remain distinct |

## Register rule

A source becomes `used` only after exact claim mapping and locator verification. This table is not a completed systematic review and does not close W03 or W04.
