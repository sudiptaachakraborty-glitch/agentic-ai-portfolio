# SPDX-License-Identifier: MIT
# Part of: agentic-ai-portfolio (https://github.com/sudiptaachakraborty-glitch/agentic-ai-portfolio)
# Copyright (c) 2026 Sudipta Chakraborty.
#
# CareMatch v0 — investor-facing product demo.
#
# Concept: Tinder × Uber for senior caregiving. A family describes the
# senior's needs once. The app ranks 12 seeded caregiver profiles (the same
# matching logic that would run against a real supply-side database) and
# presents them one card at a time. For each card the app:
#   • shows the caregiver's photo, location, rate, languages, specialty
#   • generates a short AI "Why this match" sentence grounded in the form
#   • shows a transparent Uber-style payout estimate
#   • offers Accept / Pass / Skip buttons (the "swipe" gesture in mobile)
#
# Stack: Gradio Blocks + OpenAI Chat Completions (gpt-4o-mini) for match
# reasoning. No external DB — caregivers.py holds the seed.
#
# This is deliberately a v0: it proves the matching loop and the family-side
# UX. A v1 would add: caregiver onboarding flow, location radius search,
# scheduling/calendar, Stripe Connect for payouts, ID verification, and
# review history.

import os
import json
from typing import List, Dict, Tuple, Optional

import gradio as gr
from openai import OpenAI

from caregivers import CAREGIVERS

PLATFORM_FEE_PCT = 15  # CareMatch keeps 15%, caregiver keeps 85% — shown explicitly.

CITIES = sorted({c["city"] for c in CAREGIVERS})
SPECIALTIES = ["companion", "clinical", "either"]

# ─────────────────────────────────────────────────────────────────────
# Matching logic — pure Python, deterministic, runs without OpenAI.
# (The LLM only writes the human-readable "why this match" sentence.)
# ─────────────────────────────────────────────────────────────────────

def score(caregiver: Dict, request: Dict) -> float:
    """Score a caregiver against the senior/family request. Higher = better match.

    Heuristic: city match (3) + specialty match (3) + language overlap (2 each)
    + within-budget (2) + has-needed-skill keyword overlap (1 each).
    """
    s = 0.0
    if caregiver["city"] == request["city"]:
        s += 3
    if request["specialty"] == "either" or caregiver["specialty"] == request["specialty"]:
        s += 3
    for lang in request.get("languages", []):
        if lang and lang in caregiver["languages"]:
            s += 2
    if caregiver["hourly_rate"] <= request["max_hourly_rate"]:
        s += 2
    needs_text = " ".join([request.get("needs", ""), request.get("notes", "")]).lower()
    for skill in caregiver["skills"]:
        if any(token in needs_text for token in skill.lower().split()):
            s += 1
    return s


def rank(request: Dict) -> List[Dict]:
    scored = [(score(c, request), c) for c in CAREGIVERS]
    scored.sort(key=lambda pair: (-pair[0], pair[1]["hourly_rate"]))
    # Drop zero-score caregivers — they're irrelevant to this request.
    return [c for s, c in scored if s > 0]


def payout_breakdown(rate: float, hours_per_week: float, weeks: float) -> Dict:
    gross = rate * hours_per_week * weeks
    fee = gross * (PLATFORM_FEE_PCT / 100)
    net_to_caregiver = gross - fee
    return {
        "gross": round(gross, 2),
        "platform_fee_pct": PLATFORM_FEE_PCT,
        "platform_fee": round(fee, 2),
        "net_to_caregiver": round(net_to_caregiver, 2),
        "rate": rate,
        "hours_per_week": hours_per_week,
        "weeks": weeks,
    }


# ─────────────────────────────────────────────────────────────────────
# AI match-reason — one sentence, grounded in the form + the caregiver bio.
# Lazy OpenAI client so the Space boots without a key.
# ─────────────────────────────────────────────────────────────────────

_client: Optional[OpenAI] = None

def _openai() -> Optional[OpenAI]:
    global _client
    if _client is not None:
        return _client
    if not os.environ.get("OPENAI_API_KEY"):
        return None
    _client = OpenAI()
    return _client


def ai_match_reason(caregiver: Dict, request: Dict) -> str:
    client = _openai()
    if client is None:
        return (
            "_(AI reasoning will appear here once `OPENAI_API_KEY` is set on this "
            "Space — meanwhile, this caregiver scored highest on the deterministic "
            "match score: city, specialty, language and budget alignment.)_"
        )
    system = (
        "You are CareMatch's matching assistant. In ONE sentence (max 35 words), "
        "explain to a family why this caregiver is a strong fit for their senior "
        "loved one. Be specific. Reference what's actually in the caregiver's bio "
        "or skills AND what the family asked for. Warm but not gushing. No hedging."
    )
    user = json.dumps({
        "family_request": request,
        "caregiver": {
            "name": caregiver["name"],
            "city": caregiver["city"],
            "specialty": caregiver["specialty"],
            "languages": caregiver["languages"],
            "skills": caregiver["skills"],
            "bio": caregiver["bio"],
            "years_experience": caregiver["years_experience"],
        },
    })
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
            temperature=0.4,
            max_tokens=120,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"_(AI match reason unavailable: {e})_"


# ─────────────────────────────────────────────────────────────────────
# UI — Gradio Blocks. State holds the ranked list + the current index.
# ─────────────────────────────────────────────────────────────────────

EMPTY_CARD = (
    "### No more matches in your area\n\n"
    "Try widening the city radius, raising your max hourly rate, or relaxing "
    "the specialty filter. (In a production CareMatch, we would also expand "
    "the search to the next city ring automatically.)"
)


def render_card(caregiver: Dict, reason: str, request: Dict) -> Tuple[str, str, str]:
    """Return (photo_url, markdown_card, payout_markdown)."""
    payout = payout_breakdown(
        caregiver["hourly_rate"], request["hours_per_week"], request["weeks"]
    )
    badges = []
    if caregiver["background_checked"]:
        badges.append("✅ Background-checked")
    badges.append(f"⭐ {caregiver['years_experience']} yrs experience")
    badges.append(f"🗣 {', '.join(caregiver['languages'])}")
    badge_line = " · ".join(badges)

    card_md = f"""
### {caregiver['name']}, {caregiver['age']}
**{caregiver['city']} · ${caregiver['hourly_rate']}/hr · {caregiver['specialty'].title()} care**
{badge_line}

> {caregiver['bio']}

**Skills:** {', '.join(caregiver['skills'])}
**Availability:** {caregiver['availability']}

#### 💡 Why this match
{reason}
"""

    payout_md = f"""
#### 💵 Transparent payout (Uber-style)
| Item | Amount |
|---|---|
| Hourly rate | ${payout['rate']:.2f}/hr |
| Hours / week | {payout['hours_per_week']:.0f} |
| Weeks | {payout['weeks']:.0f} |
| **Gross to engagement** | **${payout['gross']:.2f}** |
| CareMatch platform fee ({payout['platform_fee_pct']}%) | −${payout['platform_fee']:.2f} |
| **Net to caregiver** | **${payout['net_to_caregiver']:.2f}** |

_The caregiver sees this exact breakdown before they accept._
"""
    return caregiver["photo"], card_md, payout_md


def start_search(city, specialty, languages_str, max_rate, hours, weeks, needs, notes):
    request = {
        "city": city,
        "specialty": specialty,
        "languages": [l.strip() for l in (languages_str or "").split(",") if l.strip()],
        "max_hourly_rate": float(max_rate),
        "hours_per_week": float(hours),
        "weeks": float(weeks),
        "needs": needs or "",
        "notes": notes or "",
    }
    matches = rank(request)
    if not matches:
        return (
            request, [], 0, [],   # state
            None, EMPTY_CARD, "", "", # photo, card_md, payout_md, status
        )
    first = matches[0]
    reason = ai_match_reason(first, request)
    photo, card_md, payout_md = render_card(first, reason, request)
    accepted: List[str] = []
    status = f"Showing match **1 of {len(matches)}** · {len(matches)} caregivers ranked for you"
    return request, matches, 0, accepted, photo, card_md + status_md(status), payout_md, render_history(accepted)


def status_md(text: str) -> str:
    return f"\n\n---\n_{text}_\n"


def render_history(accepted: List[str]) -> str:
    if not accepted:
        return "_No caregivers accepted yet._"
    lines = ["### Your shortlist (Accepted)"] + [f"- {name}" for name in accepted]
    lines.append("\n_In a production CareMatch, accepting opens the chat thread + "
                 "sends the caregiver a push notification with the same payout breakdown they just saw._")
    return "\n".join(lines)


def advance(direction: str, request, matches, idx, accepted):
    """direction in {'accept', 'pass', 'skip'}."""
    if not matches:
        return request, matches, idx, accepted, None, EMPTY_CARD, "", render_history(accepted)
    current = matches[idx]
    if direction == "accept":
        accepted = list(accepted) + [f"{current['name']} ({current['city']}, ${current['hourly_rate']}/hr)"]
    new_idx = idx + 1
    if new_idx >= len(matches):
        done_msg = (
            f"### 🎉 You've reviewed all {len(matches)} matches.\n\n"
            f"Accepted: **{len(accepted)}** caregivers (see shortlist below)."
        )
        return request, matches, new_idx, accepted, None, done_msg, "", render_history(accepted)
    nxt = matches[new_idx]
    reason = ai_match_reason(nxt, request)
    photo, card_md, payout_md = render_card(nxt, reason, request)
    status = f"Showing match **{new_idx+1} of {len(matches)}** · accepted so far: {len(accepted)}"
    return request, matches, new_idx, accepted, photo, card_md + status_md(status), payout_md, render_history(accepted)


# ─────────────────────────────────────────────────────────────────────
# Layout
# ─────────────────────────────────────────────────────────────────────

with gr.Blocks(theme=gr.themes.Soft(primary_hue="rose"), title="CareMatch v0") as demo:
    gr.Markdown(
        """
# 💗 CareMatch — *Tinder × Uber for senior caregiving*

A community-first marketplace where retirees and part-time caregivers in your
neighborhood can swipe through nearby companion-care or clinical-care requests,
see a transparent payout, and accept with one tap.

> **v0 demo** — 12 seeded caregiver profiles in the Tri-Valley (Pleasanton,
> Dublin, San Ramon, Livermore, Fremont, Hayward, Tracy). The matching logic,
> the AI "why this match" sentence, and the Uber-style payout breakdown
> are all real and ready to be wired to a production database. Built by
> Sudipta Chakraborty as a founding-stage product demo.
"""
    )

    request_state = gr.State(value={})
    matches_state = gr.State(value=[])
    idx_state = gr.State(value=0)
    accepted_state = gr.State(value=[])

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### Tell us about your loved one")
            city = gr.Dropdown(CITIES, value=CITIES[0] if CITIES else None, label="City")
            specialty = gr.Radio(SPECIALTIES, value="either", label="Care type")
            languages_str = gr.Textbox(
                value="English",
                label="Preferred languages (comma-separated)",
                placeholder="English, Spanish",
            )
            max_rate = gr.Slider(15, 60, value=35, step=1, label="Max hourly rate ($/hr)")
            hours = gr.Slider(2, 60, value=20, step=1, label="Hours per week")
            weeks = gr.Slider(1, 52, value=4, step=1, label="Engagement length (weeks)")
            needs = gr.Textbox(
                label="What does your loved one need help with?",
                lines=2,
                placeholder="e.g. companionship, medication reminders, light meals, walks",
            )
            notes = gr.Textbox(
                label="Anything else? (health conditions, preferences)",
                lines=2,
                placeholder="e.g. early-stage dementia, vegetarian, prefers female caregiver",
            )
            search_btn = gr.Button("🔍 Find caregivers", variant="primary", size="lg")

        with gr.Column(scale=2):
            gr.Markdown("### Your match")
            photo = gr.Image(label="", show_label=False, height=280, width=280, interactive=False)
            card_md = gr.Markdown(
                "_Fill the form on the left and click **Find caregivers** to see your first match._"
            )
            with gr.Row():
                pass_btn = gr.Button("👎  Pass", scale=1)
                skip_btn = gr.Button("⏭  Skip for now", scale=1)
                accept_btn = gr.Button("👍  Accept", scale=1, variant="primary")
            payout_md = gr.Markdown("")
            shortlist_md = gr.Markdown("_No caregivers accepted yet._")

    search_btn.click(
        start_search,
        inputs=[city, specialty, languages_str, max_rate, hours, weeks, needs, notes],
        outputs=[request_state, matches_state, idx_state, accepted_state,
                 photo, card_md, payout_md, shortlist_md],
    )
    accept_btn.click(
        lambda r, m, i, a: advance("accept", r, m, i, a),
        inputs=[request_state, matches_state, idx_state, accepted_state],
        outputs=[request_state, matches_state, idx_state, accepted_state,
                 photo, card_md, payout_md, shortlist_md],
    )
    pass_btn.click(
        lambda r, m, i, a: advance("pass", r, m, i, a),
        inputs=[request_state, matches_state, idx_state, accepted_state],
        outputs=[request_state, matches_state, idx_state, accepted_state,
                 photo, card_md, payout_md, shortlist_md],
    )
    skip_btn.click(
        lambda r, m, i, a: advance("skip", r, m, i, a),
        inputs=[request_state, matches_state, idx_state, accepted_state],
        outputs=[request_state, matches_state, idx_state, accepted_state,
                 photo, card_md, payout_md, shortlist_md],
    )

    gr.Markdown(
        """
---
### What's a v1 of CareMatch?
- Caregiver onboarding flow (ID + background-check vendor integration: Checkr / Sterling)
- Location radius search with reverse-geocoding (we currently match on exact city)
- Calendar + scheduling, recurring shifts, and a shift-clock for time tracking
- Stripe Connect for payout disbursement (the Uber-style breakdown is already on this screen)
- Two-sided reviews + dispute resolution
- Caregiver-side mobile app (iOS / Android) with the actual swipe-deck gesture

### Why this matters
Family caregivers in the U.S. spend an average of **24+ hours/week** on unpaid
care and most can't afford traditional 24-hr home care. CareMatch unlocks the
**retirement-age workforce** that wants flexible, dignified, locally-bounded
work — and matches them to families who need exactly a few hours, not a full
shift. The transparent payout (no hidden agency fees) is the trust layer.
"""
    )

if __name__ == "__main__":
    demo.launch()
