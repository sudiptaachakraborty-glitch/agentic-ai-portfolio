# Handoff — finishing the GitHub publish

Everything is built and committed in your **local repo at**
`/Users/sudee/projects/agentic-ai-portfolio` — 130 files, ~13 MB.

```
$ git -C /Users/sudee/projects/agentic-ai-portfolio log --oneline
4b98a9e Initial commit: 8-project agentic AI portfolio
```

I cannot push from inside the assistant because there's no GitHub CLI
installed and no SSH key configured on this machine. There are 3 ways to
finish — pick the easiest.

---

## Step 1 (required for all options) — create the empty GitHub repo

Open https://github.com/new in a browser (you're already logged in) and
fill in:

- **Repository name:** `agentic-ai-portfolio`
- **Description:** `Eight hands-on AI-agent projects — OpenAI Agents SDK, CrewAI, LangGraph, AutoGen, MCP. Portfolio for CareMatch & HerPath.`
- **Visibility:** **Public**
- ⚠️ **Do NOT** check "Add a README", "Add .gitignore", or "Choose a license" — I already wrote those, and ticking them will create a merge conflict.
- Click **Create repository**.

You'll land on an "empty repo, push your code" page. Leave that page open.

---

## Step 2 — authenticate & push (pick ONE)

### Option A — GitHub CLI *(easiest, recommended)*

```bash
brew install gh                 # if not already installed
gh auth login                   # follow the browser flow; pick HTTPS
cd /Users/sudee/projects/agentic-ai-portfolio
git push -u origin main
```

### Option B — Personal Access Token *(no install needed)*

1. Open https://github.com/settings/personal-access-tokens/new
2. **Token name:** `agentic-ai-portfolio-push` · **Expiration:** 7 days · **Resource owner:** sudiptaachakraborty-glitch
3. **Repository access:** *Only select repositories* → `agentic-ai-portfolio`
4. **Permissions → Repository permissions:**
   - Contents: **Read and write**
   - Metadata: **Read** (auto-included)
5. **Generate token**, copy the `github_pat_…` string.
6. Push:
   ```bash
   cd /Users/sudee/projects/agentic-ai-portfolio
   git push -u origin main
   # Username: sudiptaachakraborty-glitch
   # Password: <paste the token>
   ```
   macOS Keychain will offer to save it; choose Yes for next time.

### Option C — SSH

```bash
ssh-keygen -t ed25519 -C "you@example.com"          # press Enter at prompts
cat ~/.ssh/id_ed25519.pub                            # copy the printed key
# Paste it at https://github.com/settings/ssh/new (title: "MacBook")
cd /Users/sudee/projects/agentic-ai-portfolio
git remote set-url origin git@github.com:sudiptaachakraborty-glitch/agentic-ai-portfolio.git
git push -u origin main
```

---

## Step 3 — verify

Open https://github.com/sudiptaachakraborty-glitch/agentic-ai-portfolio in
the browser. The README should render with the project table. Click into
any of the 8 project folders to confirm their READMEs are there.

---

## Step 4 (optional, recommended) — deploy live demos

Five of the eight projects can become live URLs in 5–20 minutes each.
See [`docs/DEPLOY.md`](./docs/DEPLOY.md). The demo URLs go right back
into the table in the top-level [`README.md`](./README.md).

| # | Project | Demo deploy time | Required keys |
|---|---|---|---|
| 1 | Career Digital Twin | 5 min | OpenAI |
| 3 | Deep Research | 10 min | OpenAI, Serper |
| 6 | LangGraph Sidekick | 15 min | OpenAI, Serper |
| 7 | AutoGen Creator | 10 min (optional) | OpenAI |
| 8 | Trading Floor | 20 min | OpenAI, Polygon |

Recommend deploying **#1** and **#3** first — they're the most "click and
be impressed" demos for an investor. #8 is the most architecturally
impressive but takes the longest and burns the most credits.

---

## What I built (high level)

- 8 self-contained projects under `01_…/` … `08_…/`, each with a `README.md`, `.env.example`, `requirements.txt`
- Top-level `README.md` (portfolio narrative tying everything to CareMatch & HerPath)
- `LICENSE` (MIT) + `LICENSE.upstream` (Ed Donner's MIT) + `NOTICE` (attribution)
- `docs/ARCHITECTURE.md` (single-page system diagram + TPM risk-frame)
- `docs/DEPLOY.md` (Hugging Face Spaces guide)
- `.gitignore` (no secrets, no DBs, no PDFs leak in)
- SPDX-License-Identifier headers on all 52 .py files with attribution to upstream
- `push.sh` helper script

## Questions / changes you may want to make before pushing

- **Replace** `01_career_digital_twin/me/README.md` by dropping in your real
  bio (`me/summary.txt`) and LinkedIn export PDF (`me/linkedin.pdf`) — but
  these are *gitignored* so they stay private. Without them, the Digital
  Twin will work but answer "I don't have that info."
- **Edit** the email in the top-level README (currently
  `sudipta.chakraborty@example.com` placeholder).
- **Rename the repo** if `agentic-ai-portfolio` isn't your preferred name —
  just make sure the same name is used in `git remote add` and on GitHub.
