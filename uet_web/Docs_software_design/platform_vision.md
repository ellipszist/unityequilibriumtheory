# Platform Ecosystem Architecture

## 1. Core Vision
Transform intellectual labor and physical computation into value (Uet-Cash) through a unified platform that combines:
- **Scientific Computing** (Physics equations/models)
- **Financial Computation** (Mining, Ledger, Smart Contracts)
- **Collaboration** (Project management, AI model training)
- **Social Economy** (Knowledge sharing, reputation)

## 2. Main Pillars of the Platform

### A. The Compute & Economy Engine (Rust Backend - `uet_core`, `uet_chain`)
- **Physics Mining:** Users contribute compute power to solve UET Master Equations.
- **Financial Ledger:** Quantum-resistant blockchain storing Uet-Cash transactions.
- **AI Model Training (Future):** Using the solved equations to train AI models that can generate further value.

### B. The Social & Collaboration Hub (Next.js Frontend - `uet_web`)
- **Social Feed:** Share research, findings, and discussions.
- **Project Workspaces:** Collaborate on solving complex problems. Replacing traditional labor with intellectual collaboration.
- **Reputation System:** Earn credibility based on contributions (code, compute power, or knowledge).

### C. The Wallet & Identity System (Next.js & Rust)
- **Digital Identity:** Login system (already built).
- **Crypto Wallet:** Store Uet-Cash securely.
- **Transaction Interface:** Send/receive funds, stake compute power.

## 3. Immediate Next Steps (Phase: Web Platform Foundation)

To realize this vision within the current Next.js application (`uet_web`), we need to build the database schema and API foundation for these features.

### Step 1: Database Schema Design (PostgreSQL + Prisma/Drizzle)
We need to design tables for:
1. **Users & Wallets:** User profiles, wallet addresses, balances, security keys.
2. **Social Feed:** Posts, comments, likes, tags (focusing on scientific/technical content).
3. **Projects/Workspaces:** Collaborative spaces, tasks, contributors, compute allocations.
4. **Mining Logs:** Tracking a user's compute contributions and rewards from the Rust backend.

### Step 2: Backend Integration
- Connect the Next.js frontend to the Rust backend (`uet_chain` / `uet_miner`).
- Create APIs to fetch wallet balance, start/stop mining tasks, and submit proofs.

### Step 3: Frontend UI/UX
- **Dashboard:** Overview of wallet balance, current mining tasks, and social updates.
- **Wallet Page:** Transaction history, send/receive UI.
- **Social/Project Page:** Kanbans, forums, and knowledge base integration.

## 4. Why are we doing this?
Instead of money being created solely by burning electricity (like Bitcoin) or fiat (inflation), Uet-Cash is minted by *learning and solving*.
By building this social/collaboration wrapper around the mining engine, we create an ecosystem where intellectual work is directly monetized and shared.
