---
title: CareMatch v0
emoji: 💗
colorFrom: pink
colorTo: red
sdk: gradio
sdk_version: 5.49.0
app_file: app.py
pinned: true
license: mit
short_description: Tinder x Uber for senior caregiving — v0 product demo
---

# CareMatch — v0 product demo

A community-first marketplace where retirees and part-time caregivers can swipe through nearby
senior-care requests with photos, location, transparent Uber-style payouts, and one-tap accept / pass.

This Space is the **family side** of the demo. Fill in what your senior loved one needs, and the app
ranks 12 seeded caregivers in the Tri-Valley, generates an AI "why this match" sentence per card,
and shows the exact payout the caregiver will see.

## What is real here vs. what is mocked

| Real | Mocked (would be production in v1) |
|---|---|
| Matching/scoring algorithm | Caregiver supply (12 seeded profiles vs. real onboarded caregivers) |
| AI "why this match" reasoning (gpt-4o-mini, grounded in form + bio) | Background-check integration (currently a static `True`) |
| Uber-style transparent payout breakdown | Stripe Connect disbursement |
| City / specialty / language / budget / skill matching | Location radius search (currently matches on exact city string) |

## Running locally

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...
python app.py
```

## Built by
Sudipta Chakraborty — founder/builder of CareMatch and HerPath.
Resume + agentic-AI portfolio: https://github.com/sudiptaachakraborty-glitch/agentic-ai-portfolio
