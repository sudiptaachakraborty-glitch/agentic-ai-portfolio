# 01 · Career Digital Twin

> A small RAG-backed agent that role-plays *you* on your own website — answers
> visitor questions about your background using your bio and LinkedIn export
> as the knowledge base, captures lead emails, and pushes a notification when
> it can't answer something.

**Stack:** OpenAI · Gradio · Pushover
**Concepts:** simple RAG, structured outputs, tool calls, evaluator-pattern, push notifications, lead capture
**Live demo:** see [`docs/DEPLOY.md`](../docs/DEPLOY.md) — deploy to Hugging Face Space in ~5 minutes.

---

## What it does

1. Loads your bio (`me/summary.txt`) and LinkedIn-export PDF (`me/linkedin.pdf`) into the system prompt.
2. A Gradio chat UI lets visitors ask anything about your career.
3. The agent has two tools:
   - `record_user_details(email, name, notes)` — push notification + saved lead.
   - `record_unknown_question(question)` — push notification when the agent doesn't know the answer (so you can improve the bio).
4. A second LLM acts as an **evaluator** that checks each reply for accuracy & tone before it's sent back. If the evaluator rejects the reply, the agent re-tries with the evaluator's feedback.

## Why this matters for CareMatch / HerPath

Both products will need an "ambassador" agent on the landing page that can answer policy/eligibility questions before a real human is in the loop, and capture qualified leads. This pattern is the prototype.

## Run it locally

```bash
cd 01_career_digital_twin
cp .env.example .env          # then edit .env with your keys
echo "Replace this with your bio in plain text." > me/summary.txt
# drop your LinkedIn export PDF as: me/linkedin.pdf

uv venv && source .venv/bin/activate
uv pip install -r requirements.txt
python app.py                 # opens http://127.0.0.1:7860
```

## My additions vs. the course reference

- Pulled `me/` content out of the repo and into a template (so anyone can fork and personalize).
- README written from a *product* angle (what it would do for CareMatch / HerPath) rather than a course-exercise angle.
- `.env.example` enumerates every secret with where to get it.

## Deploying as a live demo

See [`../docs/DEPLOY.md`](../docs/DEPLOY.md) — uses Hugging Face Spaces (Gradio SDK), free tier.

## Risks / things a TPM has to manage

- **Hallucination on personal facts** → the evaluator agent + a tightly scoped system prompt + the `record_unknown_question` tool together keep this bounded.
- **PII capture** → the lead form must show a privacy notice in production. Not done here.
- **Cost** → every page-view-with-chat is one or more LLM calls. Cache the system prompt and use `gpt-4o-mini` for the evaluator.

---
*Adapted from `1_foundations/app.py` of [ed-donner/agents](https://github.com/ed-donner/agents) (MIT). See [NOTICE](../NOTICE).*
