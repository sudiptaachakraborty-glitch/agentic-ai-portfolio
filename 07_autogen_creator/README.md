# 07 · AutoGen Agent Creator

> An **AutoGen agent that writes other AutoGen agents** and runs them in a
> shared "world" of agents that talk to each other. The meta-agent pattern.

**Stack:** AutoGen AgentChat · AutoGen Core · OpenAI
**Concepts:** AgentChat conversations, AutoGen Core message passing, agent factories, distributed agents
**Demo:** Python script — best demoed as a screencast that shows the Creator emitting source code for a new agent, then that new agent joining the conversation.

---

## What it does

| File | Purpose |
|---|---|
| `creator.py` | The **Creator** agent. Given a one-line description, it generates a complete `agent.py`-shaped Python file for a new agent with a particular trading-style backstory and message handlers. |
| `agent.py` | A template agent the Creator riffs on. |
| `messages.py` | Shared message types so generated agents can talk to each other. |
| `world.py` | The "world" — instantiates a population of generated agents, registers them with a runtime, and lets them converse. |

The lab notebooks build up to this:

| Notebook | Topic |
|---|---|
| `01_agentchat.ipynb` | First multi-agent conversation in AgentChat |
| `02_agentchat_advanced.ipynb` | Tools, structured outputs, termination |
| `03_autogen_core.ipynb` | Lower-level Core: message passing, runtimes |
| `04_distributed.ipynb` | Distributed agents across processes |

## Why this matters for CareMatch / HerPath

- **HerPath** has a long-tail problem: every immigrant cohort (Bangladeshi nurses, Ukrainian welders, Filipino caregivers) needs a slightly specialized recommender. A meta-agent that *generates* a per-cohort recommender from a one-line spec is a force-multiplier.
- For prototype-stage products like ours, this pattern lets one PM spin up many small agents quickly without hand-coding each.

## Run it locally

```bash
cd 07_autogen_creator
cp .env.example .env
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt
python creator.py            # creates a new agent, then runs world.py
```

## My additions vs. the course reference

- README ties the meta-agent pattern to a concrete HerPath product need.
- Notebooks renamed for scannability.

## Risks / things a TPM has to manage

- **Generated agents are not safe by default.** They can `eval` arbitrary code from each other's messages. Sandbox the runtime; don't let generated agents touch your filesystem unless they've passed review.
- **Cost** — N²-ish in agents-talking-to-agents. Cap turns hard; set a budget alert.
- **Debugging** — distributed conversations are notoriously hard to trace. Wire OpenAI traces in early.

---
*Adapted from `5_autogen/` of [ed-donner/agents](https://github.com/ed-donner/agents) (MIT).*
