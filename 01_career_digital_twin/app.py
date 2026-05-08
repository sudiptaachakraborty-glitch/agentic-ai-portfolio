# SPDX-License-Identifier: MIT
# Part of: agentic-ai-portfolio  (https://github.com/sudiptaachakraborty-glitch/agentic-ai-portfolio)
# Adapted from Ed Donner's "AI Engineer Agentic Track" course companion repo
# (https://github.com/ed-donner/agents, MIT, Copyright (c) 2025 Ed Donner).
# Modifications Copyright (c) 2026 Sudipta Chakraborty.
#
# Project 01 — Career Digital Twin
# A persona-grounded chatbot that answers career questions as Sudipta
# Chakraborty, with a profile-card layout (photo + tagline + suggested
# starter prompts on the left, chat on the right). Bio comes from
# `me/summary.txt`; an optional LinkedIn export at `me/linkedin.pdf` is
# included in the system prompt if present. Two tools — record_user_details
# (lead capture) and record_unknown_question (gap logging) — fire Pushover
# notifications only when PUSHOVER_TOKEN/PUSHOVER_USER are set.

import json
import os

import gradio as gr
import requests
from dotenv import load_dotenv
from openai import OpenAI

try:
    from pypdf import PdfReader
except ImportError:  # pypdf is optional; only needed if you provide a PDF
    PdfReader = None


load_dotenv(override=True)


PROFILE_IMAGE_PATH = "me/profile.jpg"
PERSONA_NAME = "Sudipta Chakraborty"
PERSONA_TAGLINE = (
    "Senior Technical Program Manager · Program Officer · "
    "Independent AI Product Builder (CareMatch & HerPath) · "
    "Stanford Health Care Tri-Valley PFAC Advisor"
)
PERSONA_LOCATION = "Dublin, CA · San Francisco Bay Area"

STARTER_PROMPTS = [
    "Tell me about CareMatch and HerPath.",
    "What happened in March 2024 and how did you spend your recovery?",
    "Walk me through the Bank of the West $15M platform migration.",
    "What AI tools have you been learning hands-on?",
    "Why did Stanford Tri-Valley invite you onto their PFAC?",
]


def push(text: str) -> None:
    """Send a Pushover notification if credentials are configured (no-op otherwise).

    Falls back to a printed log line so the Space stays up even when the
    PUSHOVER_TOKEN / PUSHOVER_USER secrets are not set.
    """
    token = os.getenv("PUSHOVER_TOKEN")
    user = os.getenv("PUSHOVER_USER")
    if not (token and user):
        print(f"[pushover-disabled] {text}", flush=True)
        return
    try:
        requests.post(
            "https://api.pushover.net/1/messages.json",
            data={"token": token, "user": user, "message": text},
            timeout=5,
        )
    except Exception as e:
        print(f"[pushover-error] {e}", flush=True)


def record_user_details(email: str, name: str = "Name not provided", notes: str = "not provided") -> dict:
    """Record an interested visitor's email plus optional name/notes."""
    push(f"Recording {name} with email {email} and notes {notes}")
    return {"recorded": "ok"}


def record_unknown_question(question: str) -> dict:
    """Log a question the agent could not confidently answer."""
    push(f"Recording {question}")
    return {"recorded": "ok"}


record_user_details_json = {
    "name": "record_user_details",
    "description": "Use this tool to record that a user is interested in being in touch and provided an email address",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {"type": "string", "description": "The email address of this user"},
            "name": {"type": "string", "description": "The user's name, if they provided it"},
            "notes": {"type": "string", "description": "Any additional context worth recording"},
        },
        "required": ["email"],
        "additionalProperties": False,
    },
}

record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Always use this tool to record any question that couldn't be answered as you didn't know the answer",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {"type": "string", "description": "The question that couldn't be answered"},
        },
        "required": ["question"],
        "additionalProperties": False,
    },
}

tools = [
    {"type": "function", "function": record_user_details_json},
    {"type": "function", "function": record_unknown_question_json},
]


def _load_summary() -> str:
    path = "me/summary.txt"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return "Summary not provided yet."


def _load_linkedin() -> str:
    path = "me/linkedin.pdf"
    if not (os.path.exists(path) and PdfReader is not None):
        return ""
    try:
        reader = PdfReader(path)
        return "".join((page.extract_text() or "") for page in reader.pages)
    except Exception as e:
        print(f"[linkedin-load-error] {e}", flush=True)
        return ""


class Me:
    """Persona-grounded chatbot that answers as Sudipta Chakraborty.

    The OpenAI client is created lazily on the first chat call so the Space
    boots green even before the OPENAI_API_KEY secret is set.
    """

    def __init__(self) -> None:
        self.openai = None
        self.name = os.getenv("PERSONA_NAME", PERSONA_NAME)
        self.summary = _load_summary()
        self.linkedin = _load_linkedin()

    def handle_tool_call(self, tool_calls):
        results = []
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            print(f"Tool called: {tool_name}", flush=True)
            tool = globals().get(tool_name)
            result = tool(**arguments) if tool else {}
            results.append({"role": "tool", "content": json.dumps(result), "tool_call_id": tool_call.id})
        return results

    def system_prompt(self) -> str:
        prompt = (
            f"You are acting as {self.name}. You are answering questions on {self.name}'s portfolio website, "
            f"particularly questions related to {self.name}'s career, background, skills and experience. "
            f"Your responsibility is to represent {self.name} faithfully. "
            "Be warm, professional and concise (2–4 short paragraphs unless asked for detail). "
            "Speak in the first person ('I', 'my'). "
            "If you don't know the answer to any question, use the record_unknown_question tool. "
            "If the user is engaging in discussion, gently steer them towards getting in touch via email; "
            "ask for their email and record it using the record_user_details tool, but only after offering "
            "real value in the conversation first."
        )
        prompt += f"\n\n## Summary:\n{self.summary}\n"
        if self.linkedin:
            prompt += f"\n## LinkedIn Profile:\n{self.linkedin}\n"
        prompt += f"\nWith this context, please chat with the user, always staying in character as {self.name}."
        return prompt

    def chat(self, message, history):
        if not os.environ.get("OPENAI_API_KEY"):
            return (
                "⚠️ `OPENAI_API_KEY` is not set on this Space. "
                "Add it under **Settings → Variables and secrets** "
                "(name: `OPENAI_API_KEY`, value: your `sk-…` key). The Space will restart automatically."
            )
        if self.openai is None:
            self.openai = OpenAI()
        messages = (
            [{"role": "system", "content": self.system_prompt()}]
            + list(history)
            + [{"role": "user", "content": message}]
        )
        while True:
            response = self.openai.chat.completions.create(
                model="gpt-4o-mini", messages=messages, tools=tools
            )
            choice = response.choices[0]
            if choice.finish_reason == "tool_calls":
                tool_calls = choice.message.tool_calls
                results = self.handle_tool_call(tool_calls)
                messages.append(choice.message)
                messages.extend(results)
            else:
                return choice.message.content


me = Me()


CSS = """
#profile-card { padding: 16px 18px; border-radius: 14px;
    background: linear-gradient(180deg, #f8fafc 0%, #eef2ff 100%);
    border: 1px solid #e5e7eb; }
#profile-card h2 { margin: 6px 0 2px 0; font-size: 1.25rem; }
#profile-card p.tagline { color: #4338ca; font-weight: 500; margin: 4px 0 8px 0; font-size: 0.92rem; }
#profile-card p.location { color: #6b7280; margin: 0 0 10px 0; font-size: 0.85rem; }
#profile-image img { border-radius: 12px; object-fit: cover;
    box-shadow: 0 4px 14px rgba(67, 56, 202, 0.18); width: 100%; max-width: 260px; }
.starter-row button { font-size: 0.86rem; }
"""


def _build_profile_card():
    """Render the left-hand profile card (photo + name + tagline + starters)."""
    img_value = PROFILE_IMAGE_PATH if os.path.exists(PROFILE_IMAGE_PATH) else None
    gr.Image(
        value=img_value,
        show_label=False,
        show_download_button=False,
        show_fullscreen_button=False,
        container=False,
        interactive=False,
        elem_id="profile-image",
        height=320,
    )
    gr.HTML(
        f"<div id='profile-card'>"
        f"<h2>{PERSONA_NAME}</h2>"
        f"<p class='tagline'>{PERSONA_TAGLINE}</p>"
        f"<p class='location'>📍 {PERSONA_LOCATION}</p>"
        "<p style='font-size:0.86rem; color:#374151; margin:8px 0 0 0;'>"
        "Ask me about my TPM work, the products I'm building "
        "(<a href='https://huggingface.co/spaces/Life1Ok/carematch-demo' target='_blank'>CareMatch</a>, "
        "<a href='https://huggingface.co/spaces/Life1Ok/herpath-demo' target='_blank'>HerPath</a>), "
        "my Stanford PFAC advisory role, or the AI agentic-AI tools I'm learning right now."
        "</p>"
        "</div>"
    )


with gr.Blocks(theme=gr.themes.Soft(primary_hue="indigo"), css=CSS, title=f"{PERSONA_NAME} — Career Digital Twin") as demo:
    gr.Markdown(
        f"# 👋 Hi, I'm {PERSONA_NAME}\n"
        "*This is my AI-powered digital twin — ask it anything you'd ask me in a coffee chat.*"
    )

    with gr.Row():
        with gr.Column(scale=1, min_width=280):
            _build_profile_card()
        with gr.Column(scale=2):
            chatbot = gr.Chatbot(type="messages", height=460, show_label=False, avatar_images=(None, PROFILE_IMAGE_PATH if os.path.exists(PROFILE_IMAGE_PATH) else None))
            textbox = gr.Textbox(placeholder="Type your question and press Enter…", show_label=False, autofocus=True)
            with gr.Row(elem_classes="starter-row"):
                starter_buttons = [gr.Button(p, size="sm", variant="secondary") for p in STARTER_PROMPTS]

            def _user_submit(user_msg, history):
                history = list(history or [])
                history.append({"role": "user", "content": user_msg})
                return "", history

            def _bot_reply(history):
                history = list(history or [])
                if not history or history[-1].get("role") != "user":
                    return history
                user_msg = history[-1]["content"]
                prior = history[:-1]
                reply = me.chat(user_msg, prior)
                history.append({"role": "assistant", "content": reply})
                return history

            textbox.submit(_user_submit, [textbox, chatbot], [textbox, chatbot]).then(
                _bot_reply, chatbot, chatbot
            )

            for btn, prompt_text in zip(starter_buttons, STARTER_PROMPTS):
                btn.click(_user_submit, [gr.State(prompt_text), chatbot], [textbox, chatbot]).then(
                    _bot_reply, chatbot, chatbot
                )

    gr.Markdown(
        "<sub>Built with OpenAI · Gradio · grounded in `me/summary.txt`. "
        "Source: <a href='https://github.com/sudiptaachakraborty-glitch/agentic-ai-portfolio/tree/main/01_career_digital_twin' target='_blank'>GitHub</a>. "
        "If you leave your email I'll receive a notification and follow up personally.</sub>"
    )


if __name__ == "__main__":
    demo.launch()
