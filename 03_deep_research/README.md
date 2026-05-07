# 03 · Deep Research Agent Team

> Type one research question; get back a **multi-section, source-linked
> report** in a few minutes. The orchestrator plans 5 parallel web searches,
> fans them out to a search agent, hands all results to a writer agent, and
> optionally emails the report.

**Stack:** OpenAI Agents SDK · Gradio · Serper (Google search) · SendGrid (optional)
**Concepts:** Planner / fan-out / writer pattern, structured outputs (Pydantic), agents-as-tools, async orchestration, streaming UI
**Live demo:** [HF Space deploy guide](../docs/DEPLOY.md) — ~10 minutes.

---

## What it does

```
                    ┌─── search_agent (web) ─┐
                    │                        │
   user query ─►  planner ──► [5 queries] ──►├─── search_agent (web) ─┼──► writer ──► report
                    │                        │
                    └─── search_agent (web) ─┘
                                                          (optional: email_agent → SendGrid)
```

Each agent is small and single-purpose:

| File | Role |
|---|---|
| `planner_agent.py` | LLM with structured output: turns the question into 5 specific search queries |
| `search_agent.py` | LLM + WebSearchTool: runs one search, returns a 2–3 paragraph summary |
| `writer_agent.py` | LLM with structured output: takes all 5 summaries → markdown report (`ReportData` schema) |
| `email_agent.py` | LLM + SendGrid tool: sends report as HTML |
| `research_manager.py` | Orchestrator — async fan-out, progress streaming, error handling |
| `deep_research.py` | Gradio chat UI |

## Why this matters for CareMatch / HerPath

- **CareMatch** uses this pattern to research a caregiver candidate's local market: average rates for companion care in their zip, demand signals, payor mix.
- **HerPath** uses it to keep the local-job-training database fresh: scrape new programs and produce a structured row per training (provider, eligibility, cost, format, length).

## Run it locally

```bash
cd 03_deep_research
cp .env.example .env
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt
python deep_research.py    # opens Gradio UI
```

## My additions vs. the course reference

- Pulled the multi-file project out of `2_openai/deep_research/` into a **named, top-level project folder** with its own README and deploy guide.
- Documented the planner→fan-out→writer pattern as a reusable recipe (above) rather than as a code-walk.

## Risks / things a TPM has to manage

- **Source quality** — web search will surface low-quality blogs. Add a domain-allowlist or a quality classifier before the writer step in production.
- **Hallucination in the writer step** — writer should only quote URLs the search agent actually returned. Today there's no enforcement; a guardrail comparing report URLs to seen-URLs would close the loop.
- **Cost / latency** — 5 parallel calls × ~30s each + writer step. Use `gpt-4o-mini` for search summaries and `gpt-4o` only for the writer.

---
*Adapted from `2_openai/deep_research/` of [ed-donner/agents](https://github.com/ed-donner/agents) (MIT).*
