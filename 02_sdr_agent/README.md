# 02 · SDR (Sales Development Rep) Agent

> A multi-agent cold-email pipeline: three "writer" personas draft emails, a
> "sales manager" agent picks the strongest one, a formatter rewrites it as
> HTML with a subject line, and SendGrid actually sends it.
> Demonstrates **handoffs**, **tools**, and **input/output guardrails** in
> the OpenAI Agents SDK.

**Stack:** OpenAI Agents SDK · SendGrid
**Concepts:** Agent handoffs, agents-as-tools, structured outputs, input & output guardrails, traces
**Live demo:** notebook walkthrough (this one writes & sends real email — best demoed via screencast or a controlled run with a no-op email tool).

---

## What it does (lab progression)

The four notebooks build the SDR system layer by layer:

| Notebook | Adds |
|---|---|
| `01_first_agent.ipynb` | One `Agent` + `Runner` + traces |
| `02_sdr_handoffs.ipynb` | Three writer agents + a sales manager that picks the best draft |
| `03_sdr_with_tools.ipynb` | `send_email` tool (SendGrid) + a formatter sub-agent |
| `04_sdr_guardrails.ipynb` | **Input guardrail**: rejects PII in the lead's name. **Output guardrail**: rejects emails that mention the wrong company name |

## Why this matters for CareMatch / HerPath

- **CareMatch** will need outbound to caregivers as new openings appear in their zip code (consent-gated). This is the pipeline.
- **HerPath** will need warm intros to local employer partners — same pattern, different tone.

## Run it

```bash
cd 02_sdr_agent
cp .env.example .env
uv venv && source .venv/bin/activate
uv pip install openai-agents sendgrid python-dotenv jupyter pydantic
jupyter notebook
```

> Open `04_sdr_guardrails.ipynb` for the most complete version. **Comment out the `send_email` tool call** during demos unless you want to actually email.

## My additions vs. the course reference

- Renamed labs from `1_lab1.ipynb` style → descriptive filenames so a recruiter scanning the repo immediately sees the progression.
- README framed around how the pattern feeds into CareMatch / HerPath outbound, not just as course exercises.

## Risks / things a TPM has to manage

- **Spam-law compliance** (CAN-SPAM, GDPR, CASL) — there must be a verified opt-in, a physical address, and a working unsubscribe link before this goes anywhere near a real list.
- **Output guardrails are not foolproof** — they catch the named risk but won't catch novel ones. Always log + sample human review.
- **Sender reputation** — warm-up domains gradually; don't ramp from 0 to 1,000/day.

---
*Adapted from `2_openai/` of [ed-donner/agents](https://github.com/ed-donner/agents) (MIT).*
