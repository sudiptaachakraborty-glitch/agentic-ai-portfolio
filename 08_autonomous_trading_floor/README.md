# 08 · Autonomous Trading Floor — *Capstone*

> The full course capstone. A virtual **trading floor** with **six autonomous
> AI traders**, each with their own personality and strategy, running in
> parallel — all of them talking to a shared set of **MCP servers** for
> accounts, market data, push notifications, and a per-trader RAG memory.
> A Gradio dashboard shows portfolios in real time.

**Stack:** Model Context Protocol (MCP) · OpenAI Agents SDK · Polygon.io · Gradio · SQLite · Pushover · Brave/Serper search · multi-LLM (OpenAI, Anthropic, Gemini, DeepSeek)
**Concepts:** MCP server/client architecture, multi-agent autonomy, distributed scheduler, trader personas via separate model providers, persistent state, real-time dashboard
**Live demo:** [HF Space deploy guide](../docs/DEPLOY.md) — ~20 min. Heavy.

---

## Architecture

```
                ┌───────────────────────── Gradio dashboard ─────────────────────────┐
                │  6 traders · portfolios · holdings · transactions · alerts         │
                └────────────────────────────────────────────────────────────────────┘
                                              ▲
                                              │ reads
                ┌─────────────────────────────┴──────────────────────────────────────┐
                │                       trading_floor.py                             │
                │     scheduler — every N minutes wakes each trader in parallel      │
                └─────────────────────────────────────────────────────────────────────┘
                                              ▲
              ┌───────┬───────┬───────┬───────┴───────┬───────┬───────┐
              │       │       │       │               │       │       │
        ┌─────▼─┐ ┌───▼───┐ ┌─▼─────┐ ┌──▼────┐  ┌────▼──┐ ┌──▼────┐
        │Warren │ │George │ │Ray    │ │Cathie │  │Trader5│ │Trader6│
        │(Buffet│ │(Soros)│ │(Dalio)│ │(Wood) │  │  …    │ │  …    │
        └─────┬─┘ └───┬───┘ └─┬─────┘ └──┬────┘  └────┬──┘ └──┬────┘
              │       │       │           │            │       │
              ▼       ▼       ▼           ▼            ▼       ▼
        ┌──────────────── MCP Servers (each trader gets its own client) ────────────┐
        │ accounts_server   ·  market_server  ·  push_server  ·  RAG memory server  │
        └────────────────────────────────────────────────────────────────────────────┘
              │
              ▼
        SQLite: accounts.db · transactions  ·  Polygon API  ·  Brave/Serper
```

Each trader is built around the OpenAI Agents SDK with a system prompt encoding their investing style. Each trader gets its own `MCPServerStdio` clients so one trader's state can't bleed into another's.

## Why this matters for CareMatch / HerPath

- **MCP is the right boundary** for our multi-tenant future. A "matchmaking server", "payments server", "verification server" each becomes its own MCP, and the same agent code can be re-skinned for CareMatch (matching caregivers ↔ seniors) or HerPath (matching candidates ↔ trainings) just by swapping which MCP servers are mounted.
- This project is the architectural reference for that.

## Run it locally

```bash
cd 08_autonomous_trading_floor
cp .env.example .env
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt

# (optional) reset state to a clean slate:
python reset.py

# start the dashboard (which boots traders + MCP servers in subprocesses):
python app.py
```

The first time you start, each trader is given a fictional $10K and starts trading. The 24/7 loop is governed by `RUN_EVERY_N_MINUTES` in `trading_floor.py`. **Set it high (or don't start the loop) when you're just demoing — this can burn API credits.**

## File map

| File | Role |
|---|---|
| `trading_floor.py` | Scheduler — parallel wake-up of traders |
| `traders.py` | Trader agent class + system prompts |
| `app.py` | Gradio dashboard |
| `accounts.py` / `accounts_server.py` / `accounts_client.py` | MCP server for portfolio state |
| `market.py` / `market_server.py` | MCP server for market data (Polygon) |
| `push_server.py` | MCP server for Pushover notifications |
| `database.py` | SQLite layer for persistent state |
| `templates.py` | System-prompt templates per trader persona |
| `tracers.py` | OpenAI traces wiring |
| `mcp_params.py` | Centralized MCP connection parameters |
| `reset.py` | Wipe state and re-seed with $10K per trader |
| `util.py` | Helpers |
| `01–05_*.ipynb` | Lab progression — MCP basics → servers → tools → traders → trading floor |

## My additions vs. the course reference

- README written from a *system architecture* angle so an investor can read it without watching the course.
- Architecture diagram (above).
- Tied the MCP-as-boundary pattern explicitly to the CareMatch / HerPath multi-server roadmap.

## Risks / things a TPM has to manage

- **This is not real trading.** It uses fictional money. Do not point it at a live brokerage without a regulated broker-dealer.
- **Cost** — six traders × frontier model × 24/7 loop is the most expensive thing in this repo. Default loop is off in the deployed `app.py`.
- **MCP servers are subprocesses** — long-running, can leak. `reset.py` and good lifecycle management matter.
- **Traces can leak prompts** — OpenAI traces include full message history. Keep the trace dashboard private.

---
*Adapted from `6_mcp/` of [ed-donner/agents](https://github.com/ed-donner/agents) (MIT). Per-trader RAG-memory subfolders are templated, not committed, in this repo.*
