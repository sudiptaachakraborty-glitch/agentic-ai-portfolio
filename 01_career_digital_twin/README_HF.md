---
title: Career Digital Twin
emoji: 🧑‍💼
colorFrom: indigo
colorTo: blue
sdk: gradio
sdk_version: 5.49.0
app_file: app.py
pinned: false
license: mit
short_description: Chat as Sudipta Chakraborty — TPM / AI product builder.
---

# Career Digital Twin — Sudipta Chakraborty

A persona-grounded chatbot that answers career questions as **Sudipta
Chakraborty** (Senior TPM / Program Officer, AI product builder), with a
profile-card layout (photo + tagline + suggested starter prompts) on the
left and the chat on the right.

Project **01** of the [agentic-ai-portfolio](https://github.com/sudiptaachakraborty-glitch/agentic-ai-portfolio)
— hands-on capstones from Ed Donner's *AI Engineer Agentic Track: The
Complete Agent & MCP Course* on Udemy.

## How it works
- Loads `me/summary.txt` (and optionally `me/linkedin.pdf`) as grounding context.
- Uses **OpenAI** `gpt-4o-mini` with two tools: `record_user_details` (capture leads) and `record_unknown_question` (log gaps in the bot's knowledge).
- Renders a profile card with `me/profile.jpg` + name + tagline + 5 suggested starter prompts.
- Pushover notifications fire only if `PUSHOVER_TOKEN` and `PUSHOVER_USER` are set as Space secrets — otherwise the call is a no-op.

## Required secrets
Set these in **Space → Settings → Variables and secrets**:

| Name | Required | Notes |
|---|---|---|
| `OPENAI_API_KEY` | ✅ | https://platform.openai.com/api-keys |
| `PUSHOVER_TOKEN` | optional | Mobile push for new leads |
| `PUSHOVER_USER`  | optional | Mobile push for new leads |
