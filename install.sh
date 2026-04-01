#!/usr/bin/env bash
# Install autoresearch skill for Claude Code
set -euo pipefail

SKILL_DIR="${HOME}/.claude/skills/autoresearch"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_SRC="${SCRIPT_DIR}/.claude/skills/autoresearch/SKILL.md"
DASHBOARD_SRC="${SCRIPT_DIR}/dashboard"

# Allow install from GitHub without cloning
if [ ! -f "$SKILL_SRC" ]; then
  echo "Downloading from GitHub..."
  mkdir -p "$SKILL_DIR"
  curl -sfL "https://raw.githubusercontent.com/labclaw/autoresearch-skill/main/.claude/skills/autoresearch/SKILL.md" \
    -o "${SKILL_DIR}/SKILL.md"
  if [ ! -s "${SKILL_DIR}/SKILL.md" ]; then
    echo "ERROR: Download failed or file is empty. Check the URL."
    rm -f "${SKILL_DIR}/SKILL.md"
    exit 1
  fi
  echo "Installed skill to ${SKILL_DIR}/SKILL.md"
  echo ""
  echo "Dashboard: clone the repo and copy dashboard/ to your project:"
  echo "  git clone https://github.com/labclaw/autoresearch-skill.git"
  echo "  cp -r autoresearch-skill/dashboard/ /your/project/dashboard/"
  echo ""
  echo "Use /autoresearch in Claude Code to start."
  exit 0
fi

# Local install — skill + dashboard
mkdir -p "$SKILL_DIR"
cp "$SKILL_SRC" "${SKILL_DIR}/SKILL.md"
echo "Installed skill to ${SKILL_DIR}/SKILL.md"

# Offer to install dashboard to current project
if [ -d "$DASHBOARD_SRC" ] && [ -f "${DASHBOARD_SRC}/server.py" ]; then
  echo ""
  echo "Dashboard files available at: ${DASHBOARD_SRC}/"
  echo "Copy to your project with: cp -r ${DASHBOARD_SRC} /your/project/dashboard/"
  echo ""
  echo "Wandb support (optional): pip install wandb"
fi

echo ""
echo "Use /autoresearch in Claude Code to start."
