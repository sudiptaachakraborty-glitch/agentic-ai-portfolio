# SPDX-License-Identifier: MIT
# Part of: agentic-ai-portfolio (https://github.com/sudiptaachakraborty-glitch/agentic-ai-portfolio)
# Copyright (c) 2026 Sudipta Chakraborty.
#
# HerPath v0 — investor-facing product demo.
#
# Concept: an AI matchmaker that helps immigrant women in the SF Bay Area
# find local job training and placement programs aligned to their
# professional level and the type of work they want to do.
#
# The user fills a short profile (country of origin, prior profession,
# English level, preferred work type, location, work auth). The app:
#   1. filters 30 seeded Bay Area programs by level + work type + language
#   2. asks gpt-4o-mini to re-rank the top candidates with a one-paragraph
#      "why this fits you" reasoning grounded in the profile + program data
#   3. shows the top 5 with next-step links the user can act on today
#
# This is deliberately a v0: it proves the matching loop. A v1 would add
# resume upload + parsing, real-time program availability, scheduled
# follow-ups, multilingual UI, and partnership APIs to the program
# providers.

import os
import json
from typing import List, Dict, Optional

import gradio as gr
from openai import OpenAI

from programs import PROGRAMS

WORK_TYPES = [
    "Healthcare (CNA, MA, Patient Care)",
    "Software / Tech (engineering, QA, IT)",
    "Product / Design / UX",
    "Data / Analytics",
    "Office / Administrative",
    "Caregiving / Childcare",
    "Food / Hospitality / Catering",
    "Small business / Entrepreneurship",
    "Logistics / Warehouse / Manufacturing",
    "Trades / Construction / Skilled labor",
    "Open to anything entry-level",
]

LEVELS = [
    "I have professional experience and a degree from my home country",
    "I have some work experience, no degree (or degree not yet evaluated)",
    "Entry-level / first job in the U.S.",
    "Re-entering the workforce after a caregiving or health break",
]

ENGLISH_LEVELS = [
    "Native or fluent",
    "Conversational (work in English daily)",
    "Intermediate (need some support)",
    "Beginner (need ESL-friendly programs)",
]

# Map free-text work-type buttons → program "fields" keywords for filtering.
WORK_TYPE_KEYWORDS = {
    "Healthcare (CNA, MA, Patient Care)": ["healthcare", "cna", "ma", "phlebotomy", "patient", "aide", "medical"],
    "Software / Tech (engineering, QA, IT)": ["software", "engineering", "qa", "it", "cybersecurity", "web", "front", "tech", "code", "computer"],
    "Product / Design / UX": ["ux", "design", "product"],
    "Data / Analytics": ["data", "analytics"],
    "Office / Administrative": ["office", "admin", "administrative", "support"],
    "Caregiving / Childcare": ["caregiving", "childcare", "early childhood", "home health"],
    "Food / Hospitality / Catering": ["food", "hospitality", "catering", "cpg"],
    "Small business / Entrepreneurship": ["small business", "entrepreneurship", "consulting"],
    "Logistics / Warehouse / Manufacturing": ["logistics", "warehouse", "manufacturing"],
    "Trades / Construction / Skilled labor": ["construction", "trades"],
    "Open to anything entry-level": ["any"],
}

LEVEL_KEYWORDS = {
    "I have professional experience and a degree from my home country": ["professional", "career", "mid"],
    "I have some work experience, no degree (or degree not yet evaluated)": ["entry to mid", "mid", "entry"],
    "Entry-level / first job in the U.S.": ["entry", "entry to mid"],
    "Re-entering the workforce after a caregiving or health break": ["any", "career-pivot", "professional", "career"],
}


# ─────────────────────────────────────────────────────────────────────
# Deterministic pre-filter, then LLM re-rank.
# ─────────────────────────────────────────────────────────────────────

def prefilter(profile: Dict, top_k: int = 12) -> List[Dict]:
    """Score every program against the profile; return the top_k."""
    work_type = profile.get("work_type", "")
    level = profile.get("level", "")
    english = profile.get("english", "")
    languages = [l.strip().lower() for l in profile.get("languages", "").split(",") if l.strip()]
    location = profile.get("location", "").lower()

    work_keys = WORK_TYPE_KEYWORDS.get(work_type, [])
    level_keys = LEVEL_KEYWORDS.get(level, [])

    needs_esl = english.startswith("Beginner") or english.startswith("Intermediate")

    scored = []
    for p in PROGRAMS:
        s = 0.0
        # Field match (weight 4 each)
        fields_text = " ".join(p["fields"]).lower()
        for k in work_keys:
            if k in fields_text or k == "any":
                s += 4
                break
        # Level match (weight 3)
        if any(lk in p["level"].lower() for lk in level_keys):
            s += 3
        # Native-language program (weight 3 per match — really matters for newcomers)
        for lang in languages:
            if any(lang == pl.lower() for pl in p["languages"]):
                s += 3
        # ESL-friendly bonus when relevant (weight 3)
        if needs_esl:
            audience_lower = (p["audience"] + " " + p["outcomes"]).lower()
            if "esl" in audience_lower or len(p["languages"]) >= 3:
                s += 3
        # Location proximity (weight 2 if user's city/region appears in program city)
        if location and location in p["city"].lower():
            s += 2
        # Cost — free / paid stipend (weight 1) — most newcomers care
        if "free" in p["cost"].lower() or "paid" in p["cost"].lower() or "stipend" in p["cost"].lower():
            s += 1

        scored.append((s, p))

    scored.sort(key=lambda pair: -pair[0])
    return [p for s, p in scored if s > 0][:top_k]


# ─────────────────────────────────────────────────────────────────────
# LLM re-rank + reasoning. Lazy-init the OpenAI client.
# ─────────────────────────────────────────────────────────────────────

_client: Optional[OpenAI] = None

def _openai() -> Optional[OpenAI]:
    global _client
    if _client is None and os.environ.get("OPENAI_API_KEY"):
        _client = OpenAI()
    return _client


SYSTEM_PROMPT = """You are HerPath's career navigator. You help immigrant women in
the SF Bay Area pick the RIGHT next training program from a curated list.

You will receive:
  • a short profile of the woman (country, prior profession, English level,
    preferred work type, location, work authorization status)
  • 12 candidate programs that already pre-filtered as plausible fits

Your job:
  1. Pick the BEST 5 programs for THIS person, in priority order.
  2. For each, write ONE short paragraph (max 50 words) titled "Why this fits you"
     that is SPECIFIC: reference her actual profession, language, location,
     and what the program literally offers. Do NOT invent program features.
  3. Be warm, concrete, action-oriented. Skip the program if it would clearly
     mismatch (e.g., a software bootcamp for someone who said she wants caregiving work).

Return JSON only, in this exact shape:
{
  "matches": [
    {"id": "p07", "why": "..."},
    {"id": "p10", "why": "..."},
    ...up to 5...
  ]
}
"""


def llm_rerank(profile: Dict, candidates: List[Dict]) -> List[Dict]:
    """Ask the LLM to pick the top 5 with a personalised reason for each.

    Falls back to the pre-filter order with a deterministic reason if the
    LLM is unavailable (no key, rate limit, parse error).
    """
    client = _openai()
    if client is None or not candidates:
        # No-LLM fallback: top 5 from pre-filter, with a deterministic reason.
        return [
            {**p, "why": (
                f"Strong pre-filter match: {p['fields'][0]} aligns with your "
                f"preferred work type, and the program is {p['cost'].lower()}. "
                "(AI personalised reasoning will appear once `OPENAI_API_KEY` is set.)"
            )}
            for p in candidates[:5]
        ]

    user = json.dumps({
        "profile": profile,
        "candidates": [
            {
                "id": p["id"], "name": p["name"], "city": p["city"],
                "level": p["level"], "fields": p["fields"], "audience": p["audience"],
                "outcomes": p["outcomes"], "languages": p["languages"],
                "format": p["format"], "duration": p["duration"], "cost": p["cost"],
            }
            for p in candidates
        ],
    })
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user},
            ],
            temperature=0.4,
            response_format={"type": "json_object"},
            max_tokens=1200,
        )
        data = json.loads(resp.choices[0].message.content)
        by_id = {p["id"]: p for p in candidates}
        out = []
        for m in data.get("matches", [])[:5]:
            pid = m.get("id")
            if pid in by_id:
                out.append({**by_id[pid], "why": m.get("why", "")})
        if not out:
            raise ValueError("LLM returned 0 matches")
        return out
    except Exception as e:
        # Same fallback as the no-key path, but flag the error in the reason.
        return [
            {**p, "why": f"(LLM re-rank unavailable — showing pre-filter top match. {e})"}
            for p in candidates[:5]
        ]


# ─────────────────────────────────────────────────────────────────────
# UI
# ─────────────────────────────────────────────────────────────────────

INTRO = """
# 🌸 HerPath — *AI navigator for immigrant women's careers in the Bay Area*

You are not starting over — you are bringing a whole career with you.

Tell HerPath a little about yourself, and the AI will pick the **5 best free
or paid local training & placement programs** for *you*, with a personalised
"why this fits you" for each.

> **v0 demo** — 30 real Bay Area programs in the seed dataset (Upwardly Global,
> JVS, Year Up, IRC, Maitri, Narika, Code Tenderloin, Hack Bright, Renaissance
> Center, plus 21 more). Built by Sudipta Chakraborty as a founding-stage
> product demo. Inspired by the immigrant women Sudipta mentors through her
> Lean-In Circle.
"""


def search(country, prior_prof, level, english, work_type, location, languages, work_auth, ):
    profile = {
        "country": country or "",
        "prior_profession": prior_prof or "",
        "level": level,
        "english": english,
        "work_type": work_type,
        "location": location or "",
        "languages": languages or "",
        "work_auth": work_auth,
    }
    pre = prefilter(profile, top_k=12)
    if not pre:
        return (
            "### No strong matches yet — try widening your search\n\n"
            "- Lower the work-type specificity (try 'Open to anything entry-level')\n"
            "- Add more spoken languages (those open ESL-supported tracks)\n"
            "- Leave the city blank to search across the whole Bay Area\n\n"
            "_In a production HerPath, we'd auto-broaden the search and suggest adjacent fields._"
        )
    matches = llm_rerank(profile, pre)
    out = ["### Your top 5 matches\n"]
    for i, m in enumerate(matches, 1):
        out.append(f"#### {i}. [{m['name']}]({m['url']})")
        out.append(f"**{m['city']} · {m['format']} · {m['duration']} · {m['cost']}**")
        out.append(f"_Audience:_ {m['audience']}")
        out.append(f"_What you'll get:_ {m['outcomes']}")
        out.append(f"_Languages supported:_ {', '.join(m['languages'])}")
        out.append(f"\n**💡 Why this fits you**\n{m['why']}\n")
        out.append(f"**Next step →** {m['next_step']}")
        out.append("\n---\n")
    out.append(
        "_HerPath is a v0 demo. In production we'd save this list to your account, "
        "schedule check-ins, and send you reminders before deadlines. We'd also "
        "translate the reasoning into your preferred language. — built by Sudipta Chakraborty._"
    )
    return "\n".join(out)


with gr.Blocks(theme=gr.themes.Soft(primary_hue="violet"), title="HerPath v0") as demo:
    gr.Markdown(INTRO)

    with gr.Row():
        with gr.Column(scale=1):
            country = gr.Textbox(label="Country you trained / worked in", placeholder="e.g. India, Mexico, Ukraine, Vietnam")
            prior_prof = gr.Textbox(label="Your profession back home (one line)", placeholder="e.g. high-school math teacher / pharmacist / accountant")
            level = gr.Radio(LEVELS, value=LEVELS[0], label="Where are you in your U.S. journey?")
            english = gr.Radio(ENGLISH_LEVELS, value=ENGLISH_LEVELS[1], label="English comfort level")
            work_type = gr.Dropdown(WORK_TYPES, value=WORK_TYPES[0], label="What kind of work do you want next?")
            location = gr.Textbox(label="City or region in the Bay Area", placeholder="e.g. Fremont, San Francisco, Oakland, Pleasanton")
            languages = gr.Textbox(
                label="Languages you speak (comma-separated)",
                placeholder="e.g. Hindi, English, Bengali",
                value="English",
            )
            work_auth = gr.Radio(
                ["Yes — citizen / green card / EAD", "Pending / asylum / refugee status", "Not yet — exploring options"],
                value="Yes — citizen / green card / EAD",
                label="Do you have U.S. work authorization?",
            )
            search_btn = gr.Button("✨ Find my best 5 programs", variant="primary", size="lg")

        with gr.Column(scale=2):
            results_md = gr.Markdown("_Tell HerPath about yourself on the left and click **Find my best 5 programs**._")

    search_btn.click(
        search,
        inputs=[country, prior_prof, level, english, work_type, location, languages, work_auth],
        outputs=[results_md],
    )

    gr.Markdown(
        """
---
### What's a v1 of HerPath?
- **Resume upload + AI parsing** so the woman doesn't have to retype her career
- **Multilingual UI** — Spanish, Hindi, Tagalog, Vietnamese, Mandarin, Arabic, Russian
- **Live program availability** via partnership APIs to provider intake systems
- **Scheduled follow-ups & deadline reminders** (most women drop out at the form-filling step)
- **Cohort & peer matching** — women in similar transitions can support each other
- **Outcome tracking** — did she enroll, finish, get the job, get the raise

### Why this matters
Roughly **one in three women immigrating to the U.S. as professionals end up
under-employed for years** — a math teacher driving Uber, a pharmacist working
retail. The information about which Bay Area program would actually take her
seriously, in her language, at her level — exists, but is fragmented across
30+ orgs. HerPath is the navigator.
"""
    )


if __name__ == "__main__":
    demo.launch()
