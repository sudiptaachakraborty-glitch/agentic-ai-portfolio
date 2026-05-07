# Deploy Guide — Live demos on Hugging Face Spaces

You can host **5 of the 8 projects** as free, public live demos on Hugging Face Spaces (Gradio SDK). The other 3 (SDR Agent, Stock Picker, Engineering Team) are best demoed via notebooks or recorded screencasts because they email / write files / run multi-minute crews.

| # | Project | Recommended host | Time to deploy |
|---|---|---|---|
| 1 | Career Digital Twin | HF Space (Gradio) | 5 min |
| 3 | Deep Research | HF Space (Gradio) | 10 min |
| 6 | LangGraph Sidekick | HF Space (Gradio + Playwright) | 15 min |
| 7 | AutoGen Creator | HF Space (Gradio) — optional | 10 min |
| 8 | Autonomous Trading Floor | HF Space (Gradio) | 20 min |

## One-time setup

1. Create a free Hugging Face account → https://huggingface.co/join
2. Create a **write token** → https://huggingface.co/settings/tokens → "New token" → Type: **Write**.
3. Install the HF CLI:
   ```bash
   pip install -U "huggingface_hub[cli]"
   huggingface-cli login   # paste your write token
   ```

## Per-project deploy (uses project 03 as example)

```bash
# 1. Create a new Space (Gradio SDK, Public)
huggingface-cli repo create deep-research-agent --type space --space_sdk gradio

# 2. Push the project folder
cd 03_deep_research
git init -b main
git remote add origin https://huggingface.co/spaces/<your-hf-username>/deep-research-agent
git add .
git commit -m "Initial deploy"
git push origin main
```

After the first push, go to **Space → Settings → Variables and secrets** and add (as **Secrets**, not Variables):

- `OPENAI_API_KEY`
- `SERPER_API_KEY`
- `SENDGRID_API_KEY` (for project 3 email step — optional, you can comment out the email_agent call if you don't want it)

The Space will rebuild automatically and your live demo URL will be:

```
https://huggingface.co/spaces/<your-hf-username>/deep-research-agent
```

Paste that URL back into the table in the **top-level [README.md](../README.md)**.

## Secrets each project needs

| Project | Required secrets |
|---|---|
| 01 Career Digital Twin | `OPENAI_API_KEY`, `PUSHOVER_USER`, `PUSHOVER_TOKEN` |
| 03 Deep Research | `OPENAI_API_KEY`, `SERPER_API_KEY` (`SENDGRID_API_KEY` optional) |
| 06 Sidekick | `OPENAI_API_KEY`, `SERPER_API_KEY`, `PUSHOVER_USER`, `PUSHOVER_TOKEN` |
| 07 AutoGen Creator | `OPENAI_API_KEY` |
| 08 Trading Floor | `OPENAI_API_KEY`, `POLYGON_API_KEY`, `BRAVE_API_KEY` (or `SERPER_API_KEY`), `PUSHOVER_USER`, `PUSHOVER_TOKEN` |

## Tips

- **Free Spaces auto-sleep** after ~48 hrs of no traffic; first hit after sleep takes ~30 sec to wake. That's fine for an investor link.
- For project **06 Sidekick** the Space needs Playwright. Add a `packages.txt` containing one line `chromium` if Gradio's default image misses a system dep, and set the Space hardware to **CPU upgrade (free)** if cold-start exceeds the timeout.
- For project **08 Trading Floor** the 24/7 loop is *off* by default in the deployed `app.py` — the demo shows the most recent run. Trigger a manual run from the UI.
- **Cost discipline.** Set monthly limits on every paid API. OpenAI: https://platform.openai.com/usage → Limits.
- **Never commit `.env`.** Every project ships a `.env.example`; copy locally to `.env` and let `.gitignore` keep it out of git.

## Streamlit Cloud alternative

For projects that don't have a Gradio UI, [Streamlit Cloud](https://streamlit.io/cloud) is a fine free alternative. The deploy flow is the same: push to GitHub, connect the repo, add secrets in the Streamlit dashboard.

## Recording screencasts (for the 3 non-UI projects)

For SDR (02), Stock Picker (04), and Engineering Team (05), the most credible "demo" for an investor is a 60–90 second screencast of the actual run:

```bash
# macOS built-in:  ⌘+Shift+5  → Record selected portion → save .mov
# upload to YouTube unlisted, paste link into the project README
```
