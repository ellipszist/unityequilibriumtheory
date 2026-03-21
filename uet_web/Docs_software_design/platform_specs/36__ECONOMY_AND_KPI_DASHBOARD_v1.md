# UET v5.0 — Economy & KPI Dashboard Spec v1

> **Related:** [[09__PLATFORM_ENERGY_UNITS]] · [[12__MATHNICRY_ECONOMIC_CONSTITUTION]] · [[21__ECONOMIC_POLICY_v5.0]] · [[22__MARKET_INFRASTRUCTURE_v5.0]] · [[33__CREDIT_AND_SUBSCRIPTION_SPEC_v1]]

## 1. Vision & Purpose
The Economy & KPI Dashboard is the **public square of transparency** for the UET ecosystem. It unifies system performance metrics (KPIs) with economic circulation data onto a single, highly secure, public-facing page. 

Its goals are clear:
- **Absolute Transparency:** Show exactly how much energy is minted, how many users are active, and where donations/reserves flow.
- **Maximum Security:** Public data must never expose PII (Personally Identifiable Information) or create attack vectors to the main write-database.
- **Ecosystem Expansion:** Serve as the gateway for external Web3 integrations (Wallets, NFTs, DeFi).

---

## 2. Dashboard Interface & Metrics Displayed

The dashboard is divided into three primary panels:

### 2.1 The KPI Engine (System Health)
- **Active Participants:** Daily/Monthly Active Users (DAU/MAU).
- **AI Throughput:** Total AI queries handled, tokens processed, and `uet_core` CPU time consumed.
- **System Uptime:** LiveKit, Rocket.Chat, and Agent API latency/uptime.
- **Knowledge Sync:** Total vectors embedded, total documents in the registry.

### 2.2 The Macro-Economy (Circulation & Supply)
- **Total UET Coin Mined (PoUW):** Live counter of tokens minted via Thermodynamic work.
- **Global Energy Consumed:** Estimated Terawatt-hours (TWh) backing the minted coins.
- **AMM Pool Liquidity:** Current USD/External value locked in the UET Market (Doc 22).
- **Credits (AEU) Burn Rate:** Velocity of platform usage (How fast credits are being spent on AI).

### 2.3 The Transparent Treasury (Donations & Equity)
- **The State 50% Reserve:** Live balance of the collective state fund used for infrastructure.
- **Public Donation Tracker:** Real-time inflow of external donations (Crypto & Fiat) feeding the system.
- **Dividend Distributions:** Amount of UET distributed to citizens this epoch.

---

## 3. Economy vs Account Routing
The system enforces a strict separation between global metrics and personal metrics using identical Bento Grid layouts:

**`/economy` (Global System View):**
- `/economy/wallet` (State reserves, Treasury total)
- `/economy/apikey` (Global API usage stats)
- `/economy/billing` (System operational overview)
- `/economy/credits` (Total Credits in circulation)
- `/economy/mining` (Global PoUW hash rate / energy consumed)
- `/economy/market` (AMM Liquidity pools status)

**`/account` (Personal User View):**
- `/account/wallet` (Personal crypto balances)
- `/account/apikey` (User API keys for developer access)
- `/account/billing` (Stripe subscription management)
- `/account/credits` (Personal credit balance & top-ups)
- `/account/mining` (Personal contribution to PoUW)
- `/account/market` (Personal trade history)
- `/account/pricing` (Comparison of subscription tiers - Account ONLY, excluded from economy)

---

## 3. Data Architecture & Maximum Security

Exposing global system data directly from the main PostgreSQL database to the public internet is a massive security risk. We must use a **Decoupled Read Architecture**.

### 3.1 The Security Flow
```
[Main PostgreSQL DB (Produces Data)]
      │
      ▼ (Asynchronous Aggregation Cron Job - Every 5 mins)
[Aggregate Metrics Engine (Rust / Python)] 
      │ (Pre-calculates DAU, sums, averages. Strips ALL PII)
      ▼
[Read-Only Redis / ClickHouse DB (Public Facing)]
      │
      ▼ (API Layer with Rate Limiting via Cloudflare)
[Next.js Dashboard Frontend]
```

### 3.2 Security Rules
1. **No direct query:** The public dashboard NEVER sends custom SQL or GraphQL to the main database.
2. **Aggregated only:** Data is pre-calculated (e.g., `SELECT count(*) FROM users` happens in the secure background job and is pushed to Redis as `{"total_users": 15000}`).
3. **Immutability:** The dashboard frontend has no mutation endpoints regarding economic data.

---

## 4. Web3 & Crypto Ecosystem Integrations

To expand UET beyond its internal boundaries and increase network effects, we will integrate with the broader Web3 ecosystem.

### 4.1 Wallet Integration (MetaMask, Rabby, WalletConnect)
- **Web3 Login:** Allow users to bind their EVM-compatible wallets to their UET Platform accounts.
- **Self-Custody UET:** Citizens can withdraw their 25% liquid UET Coin dividend directly to their personal MetaMask wallets via bridging smart contracts.

### 4.2 Credentials & NFTs (Soulbound Tokens - SBT)
Academic credentials shouldn't be tradeable JPEGs; they should be proof of identity and skill.
- **Proof of Contribution (PoC):** When a user publishes a highly-rated paper or provides significant peer review, they are minted an **SBT (Non-transferable NFT)** on a fast L2 (e.g., Polygon or Arbitrum).
- **Role Verification:** Certain platform roles (e.g., *Council*, *Guardian* from Doc 19) are verified via possessing specific SBTs in the connected wallet.

### 4.3 DeFi & External Liquidity
- **External DEX Listing:** While UET has an internal AMM (Doc 22), wrapping UET Coin onto Ethereum/Polygon allows it to trade on Uniswap for massive external liquidity.
- **Chainlink Oracles:** Use Decentralized Oracles to feed real-world energy prices (USD/kWh) directly into the `uet_economic` module to adjust the PoUW issuance budget dynamically.

### 4.4 The Transparent Donation Smart Contract
- **Problem:** Users want to donate to UET but want a guarantee the money isn't stolen.
- **Solution:** Deploy a public `UET_Treasury` Smart Contract. 
- **Mechanism:** Anyone can send ETH, USDC, or USDT to this contract. The contract programmatically bridges the funds to pay for system API costs (OpenRouter, Stripe, Server hosting) or auto-buys UET Coin to burn, increasing the value of everyone's holding. The front-end Dashboard reads this contract live via `ethers.js` or `viem`.

---

*Last updated: 2026-03-20 | Author: Cascade AI | Version: 1.0*
