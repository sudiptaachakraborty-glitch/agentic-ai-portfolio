# Agentic AI Portfolio — Sudipta Chakraborty

> Eight hands-on projects covering the full modern agentic-AI stack:
> **OpenAI Agents SDK · CrewAI · LangGraph · AutoGen · Model Context Protocol (MCP)**.
>
> Built while completing Ed Donner's *"AI Engineer Agentic Track: The Complete Agent & MCP Course"* on Udemy. Each project here is restructured into a self-contained module with its own README, deploy guide, and (where applicable) a Hugging Face Space configuration so you can run a live demo.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![uv](https://img.shields.io/badge/built%20with-uv-DE5FE9.svg)](https://github.com/astral-sh/uv)
[![Course](https://img.shields.io/badge/course-Ed%20Donner%20Agentic%20AI-success.svg)](https://github.com/ed-donner/agents)

---

## About this portfolio

I'm a **Senior Technical Program Manager / Program Officer** with 15+ years across enterprise platform delivery (Bank of the West / BNP Paribas), public-health programs (WHO Beijing, CBM Germany, Blue Shield of California), and Patient & Family Advisory Council work at **Stanford Health Care Tri-Valley**.

Since March 2024, while recovering from a serious health event, I've used the time to build product prototypes that solve problems I lived through — and to learn the modern AI / agentic-AI toolchain hands-on. This repo is the technical proof-of-work behind two of those prototypes:

- **CareMatch** — *Tinder × Uber for senior caregiving.* A community-sourced marketplace where retirees and part-time caregivers swipe through nearby companion-care or clinical-care requests with location, photos, and transparent Uber-style payouts.
- **HerPath** — AI-powered platform that matches immigrant women to local job training and placement opportunities aligned to their professional level and preferred work type.

The eight projects below show the patterns and primitives I'm using to build the AI features behind those products: tool-using agents, multi-agent orchestration, RAG, structured-output planning, browser automation, agent-creator-agents, and **MCP** for clean tool-server boundaries.

---

## The eight projects

| # | Project | What it shows | Stack | Live demo |
|---|---|---|---|---|
| 1 | [Career Digital Twin](./01_career_digital_twin) | RAG-backed agent that role-plays you on your website; logs unanswered questions and captures lead emails | OpenAI · Gradio · Pushover | **[▶ Live on HF Spaces](https://huggingface.co/spaces/Life1Ok/career-digital-twin)** |
| 2 | [SDR (Sales Development Rep) Agent](./02_sdr_agent) | Multi-agent cold-email pipeline: drafter ↔ critic ↔ sender, with handoffs, tools, and guardrails | OpenAI Agents SDK · SendGrid | Notebook walkthrough |
| 3 | [Deep Research Agent Team](./03_deep_research) | Planner → parallel web-search agents → writer → emailer; produces a sourced research report from one query | OpenAI Agents SDK · Gradio · Serper | **[▶ Live on HF Spaces](https://huggingface.co/spaces/Life1Ok/deep-research-agent)** |
| 4 | [Stock Picker (Crew)](./04_stock_picker) | A CrewAI crew that scouts trending companies, deep-researches each, and recommends one — with structured-output schemas and memory | CrewAI · OpenAI · Pushover | CLI / `crewai run` |
| 5 | [Multi-Agent Engineering Team (Crew)](./05_engineering_team) | A 4-agent software team (engineering lead · backend · frontend · QA) that designs and builds a working Python app from a spec | CrewAI · OpenAI · Gradio | CLI / `crewai run` |
| 6 | [LangGraph Browser Sidekick](./06_langgraph_sidekick) | Stateful, persistent assistant with a Playwright-driven browser, push notifications, and an evaluator-optimizer loop | LangGraph · Playwright · Gradio · Pushover | [HF Space →](https://huggingface.co/spaces/) *(deploy guide)* |
| 7 | [AutoGen Agent Creator](./07_autogen_creator) | An AutoGen agent that *writes other AutoGen agents* and runs them in a shared world (the meta-agent pattern) | AutoGen AgentChat + Core | **[▶ Live on HF Spaces](https://huggingface.co/spaces/Life1Ok/autogen-agent-creator)** |
| 8 | [Autonomous Trading Floor (capstone)](./08_autonomous_trading_floor) | Six AI traders running 24/7 in parallel, each with their own MCP servers (accounts, market, push, RAG memory). End-to-end MCP architecture | MCP · OpenAI Agents SDK · Polygon · Gradio | [HF Space →](https://huggingface.co/spaces/) *(deploy guide)* |

> **3 of 8 demos are live** on Hugging Face Spaces under [`Life1Ok`](https://huggingface.co/Life1Ok) — projects 1, 3, and 7. The Space owner sets `OPENAI_API_KEY` in each Space's *Settings → Variables and secrets* (and optionally `SENDGRID_API_KEY` for the Deep Research email step, or `PUSHOVER_TOKEN`/`PUSHOVER_USER` for the Career Twin notifications). The remaining five projects (2, 4, 5, 6, 8) are runnable locally per [`docs/DEPLOY.md`](./docs/DEPLOY.md).

---

## Quick start (local)

Prereqs: Python 3.12, [uv](https://github.com/astral-sh/uv), and your own API keys.

```bash
git clone https://github.com/sudiptaachakraborty-glitch/agentic-ai-portfolio.git
cd agentic-ai-portfolio

# pick a project, e.g.:
cd 03_deep_research
cp .env.example .env        # then fill in your keys
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt
python deep_research.py     # or:  uv run gradio deep_research.py
```

Each project's README has the exact commands, the API keys required, and what the run will produce.

---

## API keys you'll need (across all 8 projects)

| Provider | Used by | Where to get it |
|---|---|---|
| **OpenAI** (required) | 1, 2, 3, 4, 5, 6, 7, 8 | https://platform.openai.com/api-keys |
| Anthropic (optional) | 5, 8 | https://console.anthropic.com/ |
| Google Gemini (optional) | 5, 8 | https://aistudio.google.com/apikey |
| DeepSeek / Groq (optional) | 5, 8 | provider site |
| **Serper** (Google search) | 3, 4, 6 | https://serper.dev/ — 2.5K free queries |
| **SendGrid** (email) | 2, 3 | https://sendgrid.com/ — free tier |
| **Pushover** (push notifications) | 1, 4, 6 | https://pushover.net/ |
| **Polygon** (market data) | 8 | https://polygon.io/ — free tier |
| Hugging Face write token | live demos | https://huggingface.co/settings/tokens |

> ⚠️ **Cost discipline.** Set OpenAI usage limits at https://platform.openai.com/usage. The 24/7 Trading Floor (project 8) in particular can burn API credits if left running — it ships with a 1-hour default loop that you can shorten or stop after the first cycle.

---

## Repository structure

```
agentic-ai-portfolio/
├── 01_career_digital_twin/     # OpenAI + Gradio
├── 02_sdr_agent/               # OpenAI Agents SDK
├── 03_deep_research/           # OpenAI Agents SDK + Gradio
├── 04_stock_picker/            # CrewAI
├── 05_engineering_team/        # CrewAI
├── 06_langgraph_sidekick/      # LangGraph + Playwright
├── 07_autogen_creator/         # AutoGen
├── 08_autonomous_trading_floor/# MCP capstone
├── docs/
│   ├── DEPLOY.md               # one-page deploy guide for HF Spaces
│   └── ARCHITECTURE.md         # how the pieces fit together
├── assets/
├── LICENSE                     # MIT
├── LICENSE.upstream            # Ed Donner's original MIT license
├── NOTICE                      # attribution
└── README.md                   # you are here
```

---

## Honest framing for reviewers

These are **portfolio / learning projects**, not production systems. Where the code is derived from Ed Donner's MIT-licensed course companion repo, it is clearly attributed in the per-file headers and in [NOTICE](./NOTICE). My contributions are: restructuring the curriculum into named, self-contained projects; documentation; deploy configuration; secret-handling templates; and per-project extensions noted in each README's *"My additions"* section.

If you're an investor or potential co-founder for **CareMatch** or **HerPath** and want to see the same patterns applied to those products' actual code, please [reach out](mailto:sudipta.chakraborty@example.com).

---

## License & attribution

- This repo: MIT (see [LICENSE](./LICENSE)).
- Upstream code: MIT, Copyright (c) 2025 Ed Donner (see [LICENSE.upstream](./LICENSE.upstream) and [NOTICE](./NOTICE)).
- Course: [AI Engineer Agentic Track: The Complete Agent & MCP Course](https://www.udemy.com/course/the-complete-agentic-ai-engineering-course/) on Udemy.
