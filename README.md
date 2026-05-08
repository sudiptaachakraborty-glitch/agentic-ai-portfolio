# Sudipta Chakraborty — AI Product Portfolio

> Two product demos and an agentic-AI study portfolio, by **Sudipta Chakraborty** —
> Senior Technical Program Manager / Program Officer; Patient & Family Advisory Council
> Advisor at **Stanford Health Care Tri‑Valley**; founder/builder of **CareMatch** and
> **HerPath**.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Live on HF Spaces](https://img.shields.io/badge/live-HuggingFace%20Spaces-yellow.svg)](https://huggingface.co/Life1Ok)

---

## 🎯 The two products this portfolio is here to demonstrate

These are the products I am building as an Independent AI Consultant / founder. The eight
agent‑pattern projects further down in this README are the **technical study work** I did
in parallel — they're the primitives behind the AI features in CareMatch and HerPath.

| Product | One‑liner | Live demo |
|---|---|---|
| 💗 **[CareMatch](./09_carematch_v0)** | *Tinder × Uber for senior caregiving.* A community‑first marketplace where retirees and part‑time caregivers swipe through nearby companion‑care or clinical‑care requests with photos, location, AI‑generated match reasons, and transparent Uber‑style payouts. | **[▶ Live on HF Spaces](https://huggingface.co/spaces/Life1Ok/carematch-demo)** |
| 🌸 **[HerPath](./10_herpath_v0)** | *AI navigator for immigrant women's careers in the Bay Area.* The user fills a short profile (country, prior profession, English level, work type, location) and an AI re‑ranks 30 real Bay Area training/placement programs into a personalised top 5 with "why this fits you" reasoning. | **[▶ Live on HF Spaces](https://huggingface.co/spaces/Life1Ok/herpath-demo)** |

> **Status: v0 product demos.** Real matching logic, real AI reasoning, seeded supply‑side
> data (12 fictional caregiver profiles for CareMatch; 30 real Bay Area programs for HerPath).
> The v1 scope of each — production onboarding, payments, scheduling, multilingual UI,
> partnership APIs — is documented in the in‑app *"What's a v1?"* section and in each
> project's README. **Built for investor and co‑founder conversations.**

### What an investor sees, in 5 minutes

1. Open the **CareMatch** Space → fill the family‑side form (city, hours, budget, what
   your loved one needs) → click *Find caregivers* → the app shows you the top match
   with photo, badges, AI "why this match" sentence, and a transparent payout breakdown
   (rate × hours × weeks − 15% platform fee, *exactly* as the caregiver will see it).
   Hit **Accept / Pass / Skip** and walk through 5–6 cards. The accepted shortlist
   builds on the right.
2. Open the **HerPath** Space → fill the profile (country, prior profession, English
   level, work type) → click *Find my best 5 programs* → the LLM picks the 5 best of
   30 seeded programs with a personalised paragraph for each, plus the next‑step link
   the user can click today.
3. The agentic‑AI portfolio below shows that the underlying patterns — multi‑agent
   reasoning, RAG, structured output, browser automation, MCP — are work I have my
   hands in, not slides.

---

## 🛠️ The agentic‑AI study portfolio (8 hands‑on projects)

Built while completing Ed Donner's *"AI Engineer Agentic Track: The Complete Agent &
MCP Course"* on Udemy. Each project is restructured into a self‑contained module
with its own README. Three are deployed live to my Hugging Face account
[`Life1Ok`](https://huggingface.co/Life1Ok); the others run locally per
[`docs/DEPLOY.md`](./docs/DEPLOY.md). **These are study artifacts. CareMatch and
HerPath above are the actual products.**

| # | Project | What it shows | Stack | Live demo |
|---|---|---|---|---|
| 1 | [Career Digital Twin](./01_career_digital_twin) | RAG‑backed agent that role‑plays me on my portfolio site, grounded in a bio I wrote about my actual career | OpenAI · Gradio | **[▶ Live](https://huggingface.co/spaces/Life1Ok/career-digital-twin)** |
| 2 | [SDR Agent](./02_sdr_agent) | Multi‑agent cold‑email pipeline (drafter ↔ critic ↔ sender) — *not deployed publicly because it sends real cold email; runs locally* | OpenAI Agents SDK | Notebook only |
| 3 | [Deep Research Agent](./03_deep_research) | Planner → 5 parallel web‑search agents → writer; produces a sourced report from one query | OpenAI Agents SDK · Gradio | **[▶ Live](https://huggingface.co/spaces/Life1Ok/deep-research-agent)** ⚠️ |
| 4 | [Stock Picker (Crew)](./04_stock_picker) | CrewAI crew with structured output + memory | CrewAI | CLI only |
| 5 | [Engineering Team (Crew)](./05_engineering_team) | A 4‑agent software team that designs + writes Python from a spec | CrewAI | CLI only |
| 6 | [LangGraph Browser Sidekick](./06_langgraph_sidekick) | Stateful assistant with a Playwright‑driven browser | LangGraph · Playwright | Local only |
| 7 | [AutoGen Agent Creator](./07_autogen_creator) | A persona‑prompted AssistantAgent (simplified from the course's dynamic agent‑writer pattern, which requires a writable filesystem unavailable on hosted Spaces) | AutoGen AgentChat | **[▶ Live](https://huggingface.co/spaces/Life1Ok/autogen-agent-creator)** |
| 8 | [Autonomous Trading Floor](./08_autonomous_trading_floor) | Six AI traders, each with their own MCP servers (accounts, market, push, RAG memory). End‑to‑end MCP architecture | MCP · OpenAI Agents SDK | CLI only |

### Honest notes on the live study demos

- **Career Twin** answers as me, grounded in `me/summary.txt` (my actual TPM background,
  March 2024 health event, recovery, CareMatch, HerPath, Stanford Tri‑Valley PFAC, Udemy
  course). It is text‑only — a v1 would add a profile photo card, three starter prompts
  on the CareMatch / HerPath story, and a softer lead‑capture flow.
- **Deep Research** ⚠️ — the underlying `WebSearchTool` is a paid OpenAI add‑on that is
  rate‑limited on usage tier 1, and the upstream code swallows search errors silently.
  It can produce empty reports on a free tier. The fix (swap to Serper) is documented
  in `docs/DEPLOY.md`. **Use CareMatch or HerPath as the primary demo; Deep Research
  is a backup.**
- **AutoGen Creator** — the live Space is a simplified persona‑prompted UI. The
  course's full dynamic agent‑writer pattern (an agent that writes Python files and
  imports them at runtime) requires a writable filesystem that hosted Spaces don't
  provide; that pattern is preserved in the repo for code reading but isn't exposed
  in the live UI.

The 5 study projects without a live demo are deliberate: SDR sends real email
(compliance liability), CrewAI projects (4, 5) write to disk and execute generated
code (sandbox/security issues on hosted Spaces), Browser Sidekick (6) needs a
headful Chromium that HF Spaces don't offer, and the Trading Floor (8) is a
1–2 day deploy with three MCP servers + Polygon market data — and none of those
demos is on‑message for the **healthcare / social‑impact** investors I am
actually pitching CareMatch and HerPath to.

---

## Quick start — try CareMatch or HerPath locally

```bash
git clone https://github.com/sudiptaachakraborty-glitch/agentic-ai-portfolio.git
cd agentic-ai-portfolio/09_carematch_v0     # or 10_herpath_v0
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...
python app.py                                # opens http://127.0.0.1:7860
```

---

## What's a v1 of CareMatch?
- Caregiver onboarding flow + ID/background‑check vendor (Checkr / Sterling)
- Real geolocation radius search (today: exact city‑string match)
- Calendar / scheduling / shift clock
- Stripe Connect for payouts (the Uber‑style breakdown is already on screen)
- Two‑sided reviews + dispute resolution
- Caregiver‑side mobile app (iOS / Android) with the actual swipe‑deck gesture

## What's a v1 of HerPath?
- Resume upload + AI parsing (don't make her retype her career)
- Multilingual UI — Spanish, Hindi, Tagalog, Vietnamese, Mandarin, Arabic, Russian
- Live program availability via partnership APIs to provider intake systems
- Scheduled deadline reminders (most women drop out at the form‑filling step)
- Cohort & peer matching; outcome tracking (enrolled → finished → placed)

---

## Background — about Sudipta Chakraborty

Senior Technical Program Manager / Program Officer with 15+ years across enterprise
platform delivery (Bank of the West / BNP Paribas, May 2019 – Dec 2023), public‑health
programs (WHO Beijing, CBM Germany, Blue Shield of California, via Agama Solutions
2014 – Mar 2019), and Patient & Family Advisory Council work at **Stanford Health Care
Tri‑Valley** since 2024.

In March 2024 I had a serious health event and was on medical disability through May
2025. Recovery was not idle time — I used it to build CareMatch and HerPath (informed
by my own caregiving / patient experience and by the immigrant women I mentor through
my Lean‑In Circle), and to learn the modern AI / agentic toolchain hands‑on. The
Stanford Tri‑Valley PFAC role grew naturally out of that experience.

This repo is the technical proof‑of‑work — both the products and the agent‑pattern
study that informed how I'm building them.

---

## Licensing & attribution

- This repo is MIT‑licensed (see [`LICENSE`](./LICENSE)).
- The 8 study projects (`01_…` through `08_…`) are adapted from Ed Donner's
  MIT‑licensed [course companion repo](https://github.com/ed-donner/agents);
  see [`LICENSE.upstream`](./LICENSE.upstream) and [`NOTICE`](./NOTICE).
- **The two product demos (`09_carematch_v0/` and `10_herpath_v0/`) are original
  work** by Sudipta Chakraborty (©2026, MIT). Caregiver photos are public‑domain
  stock portraits from randomuser.me; caregiver names and bios are fictional.
  HerPath's program data is aggregated from the public websites of the listed
  Bay Area training providers.

---

## Get in touch

- **Email** — see resume; or use the contact flow in the Career Twin Space
- **GitHub** — https://github.com/sudiptaachakraborty-glitch
- **Hugging Face** — https://huggingface.co/Life1Ok

If you're an investor, co‑founder, or partner organisation interested in CareMatch or
HerPath, the live demos above are the fastest way to see what I am building — and the
agent portfolio below is the proof that I can build it.
