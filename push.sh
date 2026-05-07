#!/usr/bin/env bash
# push.sh — one-shot helper to publish this repo to GitHub.
#
# Usage:
#   1. Create the empty repo on GitHub first (UI: https://github.com/new)
#      Recommended name: agentic-ai-portfolio
#      Visibility: Public
#      DO NOT initialize with README / LICENSE / .gitignore
#   2. From this directory, run one of:
#
#      A) HTTPS + Personal Access Token / browser auth:
#         GITHUB_USER=sudiptaachakraborty-glitch ./push.sh
#
#      B) gh CLI (after `brew install gh && gh auth login`):
#         GITHUB_USER=sudiptaachakraborty-glitch USE_GH=1 ./push.sh
#
#      C) SSH (after adding an SSH key in GitHub settings):
#         GITHUB_USER=sudiptaachakraborty-glitch USE_SSH=1 ./push.sh

set -euo pipefail

GITHUB_USER="${GITHUB_USER:-sudiptaachakraborty-glitch}"
REPO_NAME="${REPO_NAME:-agentic-ai-portfolio}"

if [ -n "${USE_GH:-}" ]; then
  if ! command -v gh >/dev/null 2>&1; then
    echo "gh not found. Install with: brew install gh" >&2; exit 1
  fi
  gh repo create "$GITHUB_USER/$REPO_NAME" --public --source=. --remote=origin --push
  exit 0
fi

REMOTE_URL="https://github.com/$GITHUB_USER/$REPO_NAME.git"
[ -n "${USE_SSH:-}" ] && REMOTE_URL="git@github.com:$GITHUB_USER/$REPO_NAME.git"

if [ ! -d .git ]; then
  git init -b main
fi
git add -A
git diff --cached --quiet || git commit -m "Initial commit: 8-project agentic AI portfolio"
git remote remove origin 2>/dev/null || true
git remote add origin "$REMOTE_URL"
git branch -M main
git push -u origin main
echo "✓ Pushed to $REMOTE_URL"
