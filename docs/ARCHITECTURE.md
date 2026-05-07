# Architecture overview

How the eight projects map to the modern agentic-AI stack — and why a TPM
should care about each layer.

```
              ┌──────────────────────────────────────────────────────────┐
              │                  USER-FACING SURFACE                     │
              │   Gradio · Streamlit · CLI · Slack/email · Push notif.   │
              └──────────────────────────────────────────────────────────┘
                                       ▲
                                       │
   ┌───────────────────────────────────┴──────────────────────────────────┐
   │                       AGENT ORCHESTRATION                            │
   │                                                                      │
   │   Single-agent loop  ─── 02 SDR (handoffs, guardrails)              │
   │                       ─── 06 LangGraph Sidekick (graph + memory)    │
   │                                                                      │
   │   Multi-agent crew   ─── 04 Stock Picker  (CrewAI hierarchical)     │
   │                       ─── 05 Engineering Team (CrewAI sequential)   │
   │                       ─── 03 Deep Research (Agents SDK fan-out)     │
   │                                                                      │
   │   Meta-agents        ─── 07 AutoGen Creator (agents that build      │
   │                                              other agents)          │
   │                                                                      │
   │   Distributed agents ─── 08 Trading Floor (6 traders × MCP servers, │
   │                                            scheduler, RAG memory)   │
   └──────────────────────────────────────────────────────────────────────┘
                                       ▲
                                       │
   ┌───────────────────────────────────┴──────────────────────────────────┐
   │                    TOOLS / KNOWLEDGE / I/O                           │
   │                                                                      │
   │   RAG & vector store ── 01 Career Digital Twin (over your bio/CV)   │
   │   Web search          ── Serper / Brave  (3, 4, 6, 8)               │
   │   Browser automation  ── Playwright       (6 Sidekick)              │
   │   Email               ── SendGrid         (2 SDR, 3 Deep Research)  │
   │   Push notifications  ── Pushover         (1, 4, 6, 8)              │
   │   Persistent state    ── SQLite memory.db (6, 8)                    │
   │   Market data         ── Polygon          (8)                       │
   │                                                                      │
   │   ─── exposed to agents via ──>   MCP (Model Context Protocol)      │
   │                                   demonstrated end-to-end in 08    │
   └──────────────────────────────────────────────────────────────────────┘
                                       ▲
                                       │
   ┌───────────────────────────────────┴──────────────────────────────────┐
   │                     FOUNDATION MODELS                                │
   │   OpenAI gpt-4o / gpt-4o-mini · Anthropic Claude · Google Gemini    │
   │   DeepSeek · Groq · (any OpenAI-compatible endpoint)                │
   └──────────────────────────────────────────────────────────────────────┘
```

## What each framework brings

| Framework | Strength | Project |
|---|---|---|
| **OpenAI Agents SDK** | Cleanest agent loop + handoffs + guardrails + tracing | 02, 03 |
| **CrewAI** | Declarative multi-agent crews with roles, goals, tasks | 04, 05 |
| **LangGraph** | Stateful graphs with checkpointing, evaluator-optimizer loops | 06 |
| **AutoGen** | Conversational multi-agent + agents-that-create-agents | 07 |
| **MCP** | Standard tool-server protocol — agents and tools become independently versioned | 08 |

## Why a TPM should care

For each layer there is a **risk you have to manage** as a Technical Program Manager — these are exactly the hooks I drove during the 2019–2023 Bank of the West platform-modernization program and now apply to my own products:

- **Foundation-model layer** — model-update risk, eval regressions, cost variance. Pin model versions; budget on usage; nightly evals as part of CI.
- **Tools layer** — flaky 3rd-party APIs, rate limits, secret rotation. MCP gives you a standard contract that lets you swap providers without touching agent code.
- **Orchestration layer** — non-determinism, runaway loops, cascading failures. Need timeouts, max-turn limits, structured outputs, observability (LangSmith / OpenAI traces).
- **User-facing layer** — guardrails, audit trails, model-card disclosures, EU AI Act readiness.

These eight projects exercise each of those failure modes; the README of each project calls out the specific risk(s) it surfaces.
