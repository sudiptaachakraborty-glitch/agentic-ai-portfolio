# 04 · Stock Picker (CrewAI)

> A four-agent crew that scans the news for trending companies, deep-researches
> each, and recommends one — with **structured outputs** for every step,
> **persistent memory** across runs (short-term, long-term, and entity), and
> a Pushover alert when the pick is finalized.

**Stack:** CrewAI · OpenAI · Pushover · Pydantic
**Concepts:** Multi-agent crew (hierarchical process), role/goal/task DSL, structured outputs (Pydantic), CrewAI memory (short / long / entity), tools, manager LLM
**Demo:** CLI — best demoed via screencast.

---

## The crew

| Agent | Goal |
|---|---|
| Trending Company Finder | Scrape news / search to find 2–3 companies trending today, return a `TrendingCompanyList` |
| Financial Researcher | For each trending company, produce a structured `TrendingCompanyResearch` (market position, future outlook, investment potential) |
| Stock Picker | Compare the researched companies, pick the best, justify, and explain why the others were not picked |
| **Manager** (LLM) | Hierarchical-process coordinator that delegates to the three above |

After the run, `output/decision.md` contains the recommendation and the system fires a Pushover alert.

## Why this matters for CareMatch / HerPath

- **CareMatch** uses the same crew shape to score caregiver candidates against an opening: scout → research → rank.
- **HerPath** uses it to recommend the single best training program for a new user given her professional level and goals.

## Run it locally

```bash
cd 04_stock_picker
cp .env.example .env
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt
crewai run                    # CrewAI's standard entrypoint
# Output → output/decision.md  (also pushed to your Pushover device)
```

## File map

```
src/stock_picker/
├── main.py                  # entrypoint / inputs
├── crew.py                  # crew + agents + tasks wiring
├── config/
│   ├── agents.yaml          # agent role/goal/backstory definitions
│   └── tasks.yaml           # task descriptions + structured-output schemas
└── tools/push_tool.py       # Pushover notification tool
```

## My additions vs. the course reference

- Project README written from a *product* angle.
- Companion `_companion_financial_researcher/` retained as a reference for the simpler "single-task crew" pattern that informs CareMatch's caregiver-scoring crew.

## Risks / things a TPM has to manage

- **Memory bloat** — long-term memory grows without bound. Set TTLs.
- **Source rot / paywalls** — the trending-company step is brittle to which news sources work today. Use a real news API in production.
- **This is not investment advice.** Documented as such in the system prompt.

---
*Adapted from `3_crew/stock_picker/` of [ed-donner/agents](https://github.com/ed-donner/agents) (MIT).*
