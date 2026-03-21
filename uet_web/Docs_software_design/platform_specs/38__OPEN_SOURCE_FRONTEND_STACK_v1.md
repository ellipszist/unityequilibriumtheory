# 🌐 38. UET Open-Source Frontend Stack (v1.0)

> **Related:** [[35__UX_UI_DESIGN_STANDARD_v1]]

To bypass years of complex UI development and focus explicitly on the Rust `uet_core` Backend System Architecture, the UET platform utilizes 5 "Battle-Tested" Open-Source UI Frameworks. We will fork these repositories, strip out their heavy backends, skin them with UET's aesthetic, and wire them up to our Rust APIs.

---

## 🤖 1. LobeChat (WorkChat + AI Agent Studio)
- **Role:** The primary command center for communicating with the AI, forming Swarms, and designing Multi-Agent workflows.
- **Why Chosen:** Features cutting-edge Glassmorphism UI, supports multi-agent plugins out of the box, and feels significantly lighter than traditional IDEs.
- **Repository:** [https://github.com/lobehub/lobe-chat](https://github.com/lobehub/lobe-chat)
- **🛠️ Custom Modification Required (The "NotebookLM" Panel):**
  We must append a structural **"Knowledge Source Panel"** into the LobeChat layout. Because UET relies heavily on deep research files and Vector Data (RAG), the user needs a dedicated panel beside the chat showing exactly *which* PDF, equation, or document the AI is currently citing (identical to Google NotebookLM's UX).

---

## 🗂️ 2. Rocket.Chat (Project & Workspace)
- **Role:** Real-time collaboration space. The place where Human-to-Human team members and Human-to-Agent cohorts coordinate complex projects.
- **Why Chosen:** Completely free, open-source Enterprise-grade stability. It replaces the need for expensive tools like *Plane*, handling workspace segmentation brilliantly.
- **Repository:** [https://github.com/RocketChat/Rocket.Chat](https://github.com/RocketChat/Rocket.Chat)

---

## 👥 3. Revolt + Custom Feeds (Community & Social Feed)
- **Role:** The public square and primary discovery engine. It serves as an isolated, focused workspace away from mainstream toxic social media (Facebook, Instagram, TikTok).
- **Core Features (The Dual-Feed System):**
  1. **Post Feed:** Traditional text/article discussions (Reddit/Discord style).
  2. **Reels / Shorts Feed:** A vertical scrolling video feed for quick, engaging educational clips (TikTok style). 
- **AI Content Generation:** Our internal AI Agents can autonomously research and publish knowledge into both feeds to sustain the ecosystem's intellectual environment.
- **UX Pipeline (Reels-to-Project):** When a user watches a Reel and gets an idea, they can click an embedded link that instantly teleports them into a **Project (Rocket.Chat)** to start collaborating or executing on that idea.
- **Why Chosen:** A fully open-source Discord alternative. We will adapt the UI to inject the Reels interface, capturing market share from users seeking a high-quality, knowledge-driven network.
- **Repository:** [https://github.com/revoltchat/revolt](https://github.com/revoltchat/revolt)

---

## 📚 4. Outline (Manual & System Wiki)
- **Role:** The "Holy Book" of UET. Contains all the platform rules, mathematics documentation, API endpoints, and system logs.
- **Why Chosen:** Stunning, Notion-esque aesthetic. It operates almost like a lightweight IDE for documentation, but remains completely focused, clean, and collaborative.
- **Repository:** [https://github.com/outline/outline](https://github.com/outline/outline)

---

## 📊 5. Tremor (Economy & KPI Dashboards)
- **Role:** Renders the complex UET Tokenomics, Energy Units ($\Omega$), and global transaction flows perfectly.
- **Why Chosen:** Avoids the heavy setup of systems like *Apache Superset*. Tremor provides stunning, fast-loading React+Tailwind statistics components that we can directly inject data into via the ClickHouse/Rust backend API.
- **Link/Components:** [https://tremor.so/](https://tremor.so/)

---

### Implementation Target
All of the above frontends must be consolidated under a single **Single Sign-On (SSO)** / Identity flow driven by the `SBT / DID` user credential mechanism before allowing API access.
