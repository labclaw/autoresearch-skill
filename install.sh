#!/usr/bin/env bash
# Install autoresearch skill for Claude Code
set -euo pipefail

SKILL_DIR="${HOME}/.claude/skills/autoresearch"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_SRC="${SCRIPT_DIR}/.claude/skills/autoresearch/SKILL.md"

# Allow install from GitHub without cloning
if [ ! -f "$SKILL_SRC" ]; then
  echo "Downloading from GitHub..."
  mkdir -p "$SKILL_DIR"
  curl -sL "https://raw.githubusercontent.com/labclaw/autoresearch-skill/main/.claude/skills/autoresearch/SKILL.md" \
    -o "${SKILL_DIR}/SKILL.md"
  echo "Installed to ${SKILL_DIR}/SKILL.md"
  exit 0
fi

mkdir -p "$SKILL_DIR"
cp "$SKILL_SRC" "${SKILL_DIR}/SKILL.md"
echo "Installed to ${SKILL_DIR}/SKILL.md"
echo "Use /autoresearch in Claude Code to start."
