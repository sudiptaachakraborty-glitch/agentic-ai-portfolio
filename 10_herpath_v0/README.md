---
title: HerPath v0
emoji: 🌸
colorFrom: pink
colorTo: indigo
sdk: gradio
sdk_version: 5.6.0
app_file: app.py
pinned: true
license: mit
short_description: AI navigator for immigrant women's careers in the Bay Area
---

# HerPath — v0 product demo

An AI matchmaker that helps immigrant women in the SF Bay Area find local job training and
placement programs aligned to their professional level and the type of work they want to do.

The user fills a short profile (country of origin, prior profession, English level, preferred work
type, location, work auth). HerPath then:

1. Pre-filters 30 seeded Bay Area programs by level + work type + language + ESL friendliness
2. Asks gpt-4o-mini to re-rank and pick the top 5 with a *personalised* "why this fits you"
3. Shows next-step links the user can act on today

## Running locally

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...
python app.py
```

## Built by
Sudipta Chakraborty — founder/builder of CareMatch and HerPath. Inspired by the immigrant
women Sudipta mentors through her Lean-In Circle.
Resume + agentic-AI portfolio: https://github.com/sudiptaachakraborty-glitch/agentic-ai-portfolio
