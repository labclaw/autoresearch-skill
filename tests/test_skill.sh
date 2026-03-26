#!/usr/bin/env bash
# Test suite for autoresearch skill
# Validates SKILL.md structure, frontmatter, and content quality
set -euo pipefail

SKILL_FILE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/.claude/skills/autoresearch/SKILL.md"
PASS=0
FAIL=0

pass() { ((PASS++)); echo "  PASS: $1"; }
fail() { ((FAIL++)); echo "  FAIL: $1"; }

echo "=== Autoresearch Skill Tests ==="
echo "Testing: ${SKILL_FILE}"
echo ""

# --- File existence ---
echo "[1] File structure"
[ -f "$SKILL_FILE" ] && pass "SKILL.md exists" || fail "SKILL.md not found"

# --- Frontmatter validation ---
echo ""
echo "[2] YAML frontmatter"

# Check frontmatter delimiters
head -1 "$SKILL_FILE" | grep -q "^---$" && pass "starts with ---" || fail "missing opening ---"
awk 'NR>1 && /^---$/{found=1; exit} END{exit !found}' "$SKILL_FILE" && pass "has closing ---" || fail "missing closing ---"

# Required fields
grep -q "^name:" "$SKILL_FILE" && pass "has name field" || fail "missing name field"
grep -q "^description:" "$SKILL_FILE" && pass "has description field" || fail "missing description field"

# Name format (kebab-case, max 64 chars)
NAME=$(grep "^name:" "$SKILL_FILE" | head -1 | sed 's/^name: *//')
echo "$NAME" | grep -qE '^[a-z0-9-]{1,64}$' && pass "name is valid kebab-case ($NAME)" || fail "name not kebab-case: $NAME"

# Description is multi-line or meaningful (handles YAML | syntax)
DESC_LINES=$(awk '/^description:/{found=1; next} found && /^[a-z]/{exit} found{print}' "$SKILL_FILE" | wc -l)
[ "$DESC_LINES" -ge 2 ] && pass "description is substantive (${DESC_LINES} lines)" || fail "description too short"

# --- Content validation ---
echo ""
echo "[3] Skill content"

CONTENT=$(awk '/^---$/{n++} n==2{print}' "$SKILL_FILE")
WORD_COUNT=$(echo "$CONTENT" | wc -w)

[ "$WORD_COUNT" -ge 200 ] && pass "content has ${WORD_COUNT} words (min 200)" || fail "content too short: ${WORD_COUNT} words"
[ "$WORD_COUNT" -le 5000 ] && pass "content under 5000 words" || fail "content too long: ${WORD_COUNT} words"

# Key sections
grep -q "## Phase 0" "$SKILL_FILE" && pass "has setup phase" || fail "missing setup phase"
grep -q "## Phase 1" "$SKILL_FILE" && pass "has experiment loop" || fail "missing experiment loop"
grep -q "## Phase 2" "$SKILL_FILE" && pass "has summary phase" || fail "missing summary phase"
grep -q "NEVER STOP" "$SKILL_FILE" && pass "has autonomy directive" || fail "missing NEVER STOP"
grep -q "results.tsv" "$SKILL_FILE" && pass "references results.tsv" || fail "missing results.tsv"
grep -q "git reset" "$SKILL_FILE" && pass "has revert mechanism" || fail "missing revert mechanism"

# --- Loop structure ---
echo ""
echo "[4] Loop completeness"

grep -q "Propose" "$SKILL_FILE" && pass "step: propose" || fail "missing propose step"
grep -q "Implement" "$SKILL_FILE" && pass "step: implement" || fail "missing implement step"
grep -q "Commit" "$SKILL_FILE" && pass "step: commit" || fail "missing commit step"
grep -q "Run" "$SKILL_FILE" && pass "step: run" || fail "missing run step"
grep -q "Evaluate" "$SKILL_FILE" && pass "step: evaluate" || fail "missing evaluate step"
grep -q "Log" "$SKILL_FILE" && pass "step: log" || fail "missing log step"
grep -q "Repeat" "$SKILL_FILE" && pass "step: repeat" || fail "missing repeat step"

# --- Safety checks ---
echo ""
echo "[5] Safety guards"

grep -q "edit scope" "$SKILL_FILE" && pass "mentions edit scope" || fail "missing edit scope guard"
grep -q "force-push" "$SKILL_FILE" && pass "warns against force-push" || fail "missing force-push warning"
grep -q "evaluation harness" "$SKILL_FILE" && pass "protects eval harness" || fail "missing eval harness protection"
grep -q "audit trail" "$SKILL_FILE" && pass "mentions audit trail" || fail "missing audit trail"

# --- Allowed tools ---
echo ""
echo "[6] Tool configuration"

grep -q "allowed-tools:" "$SKILL_FILE" && pass "has allowed-tools" || fail "missing allowed-tools"
grep -q "Bash" "$SKILL_FILE" && pass "allows Bash" || fail "missing Bash tool"
grep -q "Edit" "$SKILL_FILE" && pass "allows Edit" || fail "missing Edit tool"

# --- Summary ---
echo ""
echo "=== Results ==="
TOTAL=$((PASS + FAIL))
echo "Passed: ${PASS}/${TOTAL}"
echo "Failed: ${FAIL}/${TOTAL}"

if [ "$FAIL" -eq 0 ]; then
  echo "ALL TESTS PASSED"
  exit 0
else
  echo "SOME TESTS FAILED"
  exit 1
fi
