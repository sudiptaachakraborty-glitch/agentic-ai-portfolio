# SPDX-License-Identifier: MIT
# Part of: agentic-ai-portfolio  (https://github.com/sudiptaachakraborty-glitch/agentic-ai-portfolio)
# Adapted from Ed Donner's "AI Engineer Agentic Track" course companion repo
# (https://github.com/ed-donner/agents, MIT, Copyright (c) 2025 Ed Donner).
# Modifications Copyright (c) 2026 Sudipta Chakraborty.

import gradio as gr
from dotenv import load_dotenv
from research_manager import ResearchManager

load_dotenv(override=True)


async def run(query: str):
    async for chunk in ResearchManager().run(query):
        yield chunk


with gr.Blocks(theme=gr.themes.Default(primary_hue="sky")) as ui:
    gr.Markdown("# Deep Research")
    query_textbox = gr.Textbox(label="What topic would you like to research?")
    run_button = gr.Button("Run", variant="primary")
    report = gr.Markdown(label="Report")
    
    run_button.click(fn=run, inputs=query_textbox, outputs=report)
    query_textbox.submit(fn=run, inputs=query_textbox, outputs=report)

ui.launch(inbrowser=True)

