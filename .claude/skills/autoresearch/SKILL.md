---
name: autoresearch
description: |
  Autonomous research loop inspired by Andrej Karpathy's autoresearch.
  Propose change → execute → measure → keep/discard → repeat forever.
  Works on any codebase with a measurable objective (test score, benchmark,
  accuracy, loss, performance, LOC, build time, etc.).
  Use when asked to "autoresearch", "auto improve", "run experiments overnight",
  "optimize this autonomously", "improvement loop", or "keep experimenting".
argument-hint: "[objective] [measure-command] [edit-scope]"
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Agent
  - WebSearch
  - WebFetch
---

# Autoresearch: Autonomous Improvement Loop

_Inspired by [Andrej Karpathy's autoresearch](https://github.com/karpathy/autoresearch) — adapted for any codebase._

## Core Principle

You are a completely autonomous researcher. You propose changes, test them,
keep what improves the metric, discard what doesn't, and repeat **forever**
until the human manually stops you. The human may be asleep.

## Preamble

```bash
echo "=== Autoresearch Session ==="
echo "Branch: $(git branch --show-current 2>/dev/null || echo 'no-git')"
echo "Date: $(date '+%Y-%m-%d %H:%M:%S')"
echo "Commit: $(git rev-parse --short HEAD 2>/dev/null || echo 'N/A')"
```

## Phase 0: Setup (interactive — ask the human)

Parse the user's request from `$ARGUMENTS`. If not provided or unclear, ask for:

1. **Objective**: What are we optimizing? (e.g., "minimize val_bpb", "maximize test pass rate", "minimize bundle size", "maximize extraction accuracy")
2. **Measure command**: How do we measure it? A single shell command that outputs the metric. (e.g., `uv run pytest --tb=no -q | tail -1`, `node benchmark.js | grep score`)
3. **Edit scope**: Which files can you modify? (e.g., `src/model.py`, `src/**/*.ts`, `train.py`)
4. **Timeout**: Max time per experiment. Default: 5 minutes.
5. **Branch tag**: Propose a tag based on today's date (e.g., `mar26`). The branch `autoresearch/<tag>` must not already exist.

Then:

1. Create branch: `git checkout -b autoresearch/<tag>`
2. Read all in-scope files for full context
3. Create `results.tsv` with header row:
   ```
   commit	metric	status	description
   ```
4. Run the baseline (no changes) and record it as the first row
5. Confirm setup with the human, then begin the loop

**Once the human confirms, you are autonomous. Do not ask again.**

## Phase 1: The Experiment Loop

**LOOP FOREVER:**

### Step 1 — Propose
Think about what to try next. Draw on:
- Prior experiment results (read `results.tsv`)
- Domain knowledge from your training data
- Patterns from the codebase
- Ideas from related papers/techniques (use WebSearch if stuck)
- Combinations of previous near-misses
- More radical changes if incremental ones stall

Write a 1-line hypothesis: "I expect [change] will [improve/explore] because [reason]."

### Step 2 — Implement
Edit the in-scope files. Keep changes **minimal and focused** — one idea per experiment.

**Simplicity criterion** (from Karpathy): All else being equal, simpler is better.
- A tiny improvement that adds ugly complexity → probably not worth it
- A tiny improvement from *deleting* code → definitely keep
- Equal metric but simpler code → keep

### Step 3 — Commit
```bash
git add -A && git commit -m "experiment: <short description>"
```

### Step 4 — Run
Execute the measure command with output redirected:
```bash
timeout <TIMEOUT> bash -c '<MEASURE_COMMAND>' > run.log 2>&1
```

### Step 5 — Evaluate
Extract the metric from `run.log`. Compare to the current best.

- **Improved** (metric is better): **KEEP**. Log as `keep`. This commit stays. Update the best-known metric.
- **Equal or worse**: **DISCARD**. Log as `discard`. Revert: `git reset --hard HEAD~1`
- **Crashed/timed out**: **CRASH**. Read `tail -50 run.log` for the error.
  - If trivially fixable (typo, import): fix and re-run.
  - If fundamentally broken: log as `crash`, revert, move on.

### Step 6 — Log
Append to `results.tsv` (tab-separated):
```
<commit-hash-7char>	<metric-value>	<keep|discard|crash>	<description>
```

**Do NOT commit results.tsv** — leave it untracked so reverts don't lose the log.

### Step 7 — Repeat
Go back to Step 1. **NEVER STOP.**

## Critical Rules

### NEVER STOP
Once the loop begins, do NOT pause to ask the human if you should continue.
Do NOT ask "should I keep going?" or "is this a good stopping point?".
The human might be asleep, or gone, and expects you to continue **indefinitely**
until manually stopped. You are autonomous.

If you run out of ideas, **use your full power**:

**Research (use Agent tool for parallel deep dives):**
- Dispatch an Agent to WebSearch for SOTA techniques related to the objective
- Dispatch an Agent to explore the codebase for patterns you missed
- Dispatch an Agent to read documentation or API specs that might reveal optimizations
- Run multiple research agents in parallel — you are the coordinator

**Synthesis (combine what you learn):**
- Re-read the in-scope files for new angles
- Cross-reference research findings with the codebase
- Try combining previous near-misses in novel ways
- Apply techniques from adjacent domains (the best ideas cross boundaries)

**Escalation (go bigger):**
- Try more radical architectural changes
- Revisit discarded experiments with a fundamentally different approach
- Challenge assumptions — maybe the bottleneck isn't where you think
- Read papers or docs referenced in the code for deeper understanding
- If a direction shows promise but needs refinement, run 3-5 variations back to back

### Safety
- Only edit files within the declared edit scope
- Never force-push or delete the branch
- Never modify test/evaluation harnesses (that's cheating)
- If something feels destructive, log it and skip
- Keep `results.tsv` as the ground truth audit trail

### Logging discipline
- Every experiment gets a row in `results.tsv`, no exceptions
- Use `0.000000` for crashed experiments
- Descriptions should be short but specific enough to understand the change

### Git hygiene
- One commit per experiment
- Revert cleanly on discard (not a new "revert" commit — use `git reset --hard HEAD~1`)
- The branch should read as a clean sequence of kept improvements

## Power Mode: Multi-Agent Acceleration

When you have access to Agent tools or external CLI agents (ccz, cczt, cxc),
use them to accelerate the loop:

**Parallel research while running experiments:**
While an experiment is running (Step 4), dispatch background agents to:
- Research the next 3 ideas to try (saves think time between experiments)
- Analyze patterns in `results.tsv` to identify promising directions
- Scan the codebase for optimization opportunities you haven't tried
- Fetch documentation or papers relevant to the current approach

**Multi-hypothesis testing:**
If the edit scope allows independent changes in different files, dispatch
multiple agents to prepare different experiments. Queue them and run
sequentially against the metric.

**Post-experiment analysis:**
After every 10 experiments, dispatch an agent to analyze `results.tsv`:
- Which categories of changes tend to work? (architecture, hyperparams, simplification)
- Is there a pattern in what fails?
- What's the diminishing returns curve look like?
- Should you pivot strategy?

This transforms the loop from sequential to **pipelined**: while one
experiment runs, the next is being prepared, and research for the one
after that is happening in parallel.

## Phase 2: Summary (when human returns)

When the human interrupts or you detect they're back, produce a summary:

```
=== Autoresearch Summary ===
Branch: autoresearch/<tag>
Experiments run: <N>
Kept: <K>
Discarded: <D>
Crashed: <C>
Baseline metric: <start>
Best metric: <best> (improvement: <delta>)

Top improvements:
1. <commit> — <description> — <metric>
2. ...

Failed ideas (for reference):
- <description> — <why it didn't work>
```

Display the full `results.tsv` and offer to merge the improvements back to the original branch.

## Adaptation Notes

This skill generalizes Karpathy's autoresearch pattern beyond ML training:

| Karpathy's autoresearch | This skill |
|---|---|
| `train.py` only | User-defined edit scope |
| `val_bpb` metric | Any measurable objective |
| 5-min GPU training | User-defined timeout + command |
| ML architecture changes | Any code changes |
| Single GPU | Any compute environment |

The loop structure is identical: **propose → commit → run → evaluate → keep/discard → repeat**.
