# 06 · LangGraph Browser Sidekick

> A stateful, persistent personal assistant built on **LangGraph**, with a
> real **Playwright-driven browser**, push notifications, file I/O, Python
> REPL, web search, and an **evaluator–optimizer loop** that grades each
> response against your success criteria and re-tries until they're met.

**Stack:** LangGraph · Playwright · Gradio · Pushover · Serper · OpenAI
**Concepts:** Graph-based agent (nodes/edges/state), checkpointing (SQLite), conditional edges, evaluator-optimizer pattern, browser automation
**Live demo:** [HF Space deploy guide](../docs/DEPLOY.md) — ~15 minutes (needs Playwright system deps).

---

## The graph

```
                         ┌─── tools (browser, search, file, REPL, push) ─┐
                         │                                                │
   user input ──► worker ┴──────────────► evaluator ────────────► END
                  ▲                            │
                  │                            │ (criteria not met)
                  └────────────────────────────┘
```

- **`worker`** — main agent with all the tools.
- **`tools`** — Playwright browser tools (`navigate`, `click`, `extract_text`, `screenshot`), Serper search, Wikipedia, file write, Python REPL, Pushover.
- **`evaluator`** — a separate LLM that compares the worker's reply to the user's success criteria and either approves it or sends specific feedback back to the worker.
- **State** is persisted in `memory.db` (SQLite checkpointer) so a session survives restart.

## Why this matters for CareMatch / HerPath

- **HerPath** is, at its core, an evaluator-optimizer loop: a worker agent finds candidate trainings; an evaluator agent checks them against the user's eligibility/preferences; if not met, refine and retry. This project is the architectural template.
- **CareMatch** uses the browser tooling to scrape state-licensing-board pages for caregiver verification (with the user's consent).

## Run it locally

```bash
cd 06_langgraph_sidekick
cp .env.example .env
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt
playwright install chromium       # one-time, ~150MB
python app.py                     # opens http://127.0.0.1:7860
```

## File map

| File | Purpose |
|---|---|
| `app.py` | Gradio UI |
| `sidekick.py` | LangGraph definition: state, nodes, conditional edges, checkpointer |
| `sidekick_tools.py` | Tool definitions (Playwright + Serper + Wikipedia + REPL + file + push) |
| `01_…04_*.ipynb` | Lab progression — basics → state → tools → full system |

## My additions vs. the course reference

- README written from the angle of *what HerPath actually needs* (an evaluator-optimizer loop over local job trainings).
- Renamed the `1_lab1.ipynb`-style notebooks to descriptive names.

## Risks / things a TPM has to manage

- **Browser automation is fragile.** Site DOMs change weekly. Never deploy without monitoring + a synthetic test that visits the canonical pages every hour.
- **Playwright on serverless** — Hugging Face Spaces' default Gradio image works, but cold starts can exceed the timeout. Pin to CPU-upgrade hardware (free) for production-ish demos.
- **Open-ended REPL is dangerous.** Sandbox it; cap CPU/time; never expose to untrusted users.

---
*Adapted from `4_langgraph/sidekick.py`, `sidekick_tools.py`, `app.py` of [ed-donner/agents](https://github.com/ed-donner/agents) (MIT).*
