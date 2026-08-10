# Book 1 Reference Register

> **Status:** `IN_PROGRESS`; source identity is recorded, but systematic screening and exact locators remain incomplete.

| Source ID | Source | Tier | Role | State | Limitation / next check |
| --- | --- | --- | --- | --- | --- |
| `ECON-001` | BEA–BLS KLEMS, https://www.bea.gov/data/special-topics/integrated-industry-level-production-account-klems | PRIMARY/INSTITUTIONAL | production benchmark | located | lock release vintage and tables |
| `ECON-002` | BEA Input-Output Accounts, https://www.bea.gov/data/industries/input-output-accounts-data | PRIMARY/INSTITUTIONAL | production network | located | aggregation limits |
| `ECON-003` | EPA USEEIO, https://www.epa.gov/land-research/us-environmentally-extended-input-output-useeio-models | PRIMARY/INSTITUTIONAL | modelled environmental footprint | located | not transaction lineage |
| `ECON-004` | Bank of England, Money creation in the modern economy, https://www.bankofengland.co.uk/quarterly-bulletin/2014/q1/money-creation-in-the-modern-economy | AUTHORITATIVE_SECONDARY | bank deposit creation | appraised | compare U.S. institutional sources |
| `ECON-005` | Federal Reserve H.6/FRED M2SL, https://fred.stlouisfed.org/series/M2SL | PRIMARY | monetary aggregate | used | endogenous aggregate; vintage control needed |
| `ECON-006` | Federal Reserve Z.1, https://www.federalreserve.gov/apps/fof/About.htm | PRIMARY | sector sources-and-uses | used | net flows do not earmark payments |
| `ECON-007` | BLS CPI purchasing power, https://www.bls.gov/cpi/factsheets/purchasing-power-constant-dollars.htm | INSTITUTIONAL | internal purchasing power | appraised | basket average |
| `ECON-008` | BLS CPI individual experience, https://www.bls.gov/cpi/factsheets/averages-and-individual-experiences-differ.htm | INSTITUTIONAL | heterogeneity boundary | appraised | requires micro extension |
| `ECON-009` | Atlanta Fed DCPC, https://www.atlantafed.org/research-and-data/surveys/survey-and-diary-of-consumer-payment-choice | PRIMARY/INSTITUTIONAL | transaction/payment use | located | no complete payer-SKU-resource chain |
| `ECON-010` | BLS productivity and compensation gap, https://www.bls.gov/opub/btn/volume-6/understanding-the-labor-productivity-and-compensation-gap.htm | INSTITUTIONAL | construction comparison | appraised | deflator/universe dependent |
| `ECON-011` | EPI Productivity–Pay Gap, https://www.epi.org/productivity-pay-gap/ | SECONDARY/DATASET | exact source reproduction | used | keep separate from BLS comparator |
| `ECON-012` | EIA Annual Energy Review, https://www.eia.gov/totalenergy/data/annual/ | PRIMARY | energy throughput/history | used | heat basis and vintage required |
| `ECON-013` | USGS historical mineral statistics, https://www.usgs.gov/centers/national-minerals-information-center/historical-statistics-mineral-commodities-united | PRIMARY | physical material quantities | used | national totals only |
| `ECON-014` | Census Commodity Flow Survey, https://www.census.gov/programs-surveys/cfs/about.html | PRIMARY | shipment value/weight/geography | located | no financing lineage |
| `ECON-015` | SEC CompanyFacts API, https://www.sec.gov/search-filings/edgar-application-programming-interfaces | PRIMARY | public-firm funding channels | used | profit is not cash earmarking |
| `ECON-016` | USAspending, https://www.usaspending.gov/ | PRIMARY | federal awards/obligations/outlays | used | not bank settlement or invoice ledger |
| `ECON-017` | SBA Small Business FAQ 2024, https://advocacy.sba.gov/2024/07/23/frequently-asked-questions-about-small-business-2024/ | INSTITUTIONAL | U.S. small-business scope | appraised | definition/year specific |
| `ECON-018` | OECD Society at a Glance 2024, https://www.oecd.org/en/publications/society-at-a-glance-2024_918d8db3-en/ | AUTHORITATIVE_SECONDARY | fertility mechanisms | located | OECD scope; no intent inference |
| `ECON-019` | Federal Reserve History: Great Depression, https://www.federalreservehistory.org/essays/great-depression | AUTHORITATIVE_SECONDARY | monetary/history synthesis | appraised | supplement with specialist research |
| `ECON-020` | NBER Working Paper 2198, https://www.nber.org/papers/w2198 | PRIMARY_RESEARCH | gold-standard transmission | located | version appraisal needed |
| `ECON-021` | World Bank Adjusted Net Savings, https://datacatalog.worldbank.org/search/dataset/0037653/adjusted-net-savings | PRIMARY/INSTITUTIONAL | natural-capital robustness | located | valuation assumptions |
| `ECON-022` | UN SEEA Ecosystem Accounting, https://unstats.un.org/unsd/envaccounting/seearev/eea_final_en.pdf | AUTHORITATIVE_STANDARD | environmental accounts | located | physical and monetary accounts remain distinct |

A source becomes `used` only after exact claim mapping and locator verification. This register is not a completed systematic review and does not close W03 or W04.
