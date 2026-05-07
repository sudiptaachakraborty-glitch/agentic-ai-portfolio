# 05 · Multi-Agent Engineering Team (CrewAI)

> A four-role engineering crew — **Engineering Lead, Backend Engineer,
> Frontend Engineer, QA Engineer** — that takes a one-paragraph spec and
> produces a working Python module + a Gradio UI + tests.
> Three example outputs are included so you can see what 4o, 4o-mini, and
> a newer model produce from the same spec.

**Stack:** CrewAI (sequential process) · OpenAI · Gradio
**Concepts:** Sequential multi-agent crew, role specialization, code-as-output, generated UI, simple test scaffold
**Demo:** CLI — runs `crewai run`, then opens the generated Gradio app.

---

## The crew

| Agent | Output |
|---|---|
| Engineering Lead | A design doc with the module API |
| Backend Engineer | The Python module (a single `.py`) |
| Frontend Engineer | A Gradio UI that calls the module |
| QA Engineer | A pytest test file |

The default spec in `main.py` builds a small **Account Management** module (open account, deposit/withdraw, buy/sell shares with current price, calculate holdings/PnL/portfolio value, prevent invalid transactions).

## Why this matters for CareMatch / HerPath

- This is exactly the loop I want for **CareMatch's micro-features**: I describe a tiny new screen ("show caregivers within 5 mi sorted by rating"), the crew scaffolds the backend + UI + a smoke test, and a human reviews. AI as a force-multiplier for a small product team, not as a replacement for one.

## Run it locally

```bash
cd 05_engineering_team
cp .env.example .env
uv pip install -r requirements.txt   # or: uv sync (uses pyproject.toml)
crewai run
# generated app → output/app.py     (run: python output/app.py)
# generated tests → output/test_accounts.py
```

## See three example outputs without running

- `example_output_4o/` — output when the crew runs on `gpt-4o`
- `example_output_mini/` — output on `gpt-4o-mini`
- `example_output_new/` — output on a newer frontier model

Compare their generated `accounts.py` / `app.py` to see how model choice changes the design and the bug surface.

## My additions vs. the course reference

- README framed as "AI as a force-multiplier for a tiny product team," which is the actual investor pitch for CareMatch.

## Risks / things a TPM has to manage

- **Generated code quality varies massively** by model. Pin the model and freeze prompts before any user-facing run.
- **No real CI** — the QA agent generates tests but doesn't run them. A real version pipes through `pytest -q` and feeds failures back to the backend agent (evaluator-optimizer).
- **License of generated code** — depends on the model provider's terms. Document.

---
*Adapted from `3_crew/engineering_team/` of [ed-donner/agents](https://github.com/ed-donner/agents) (MIT).*
