# autoresearch-skill

A Claude Code skill that runs autonomous improvement loops on any codebase. Inspired by [Andrej Karpathy's autoresearch](https://github.com/karpathy/autoresearch).

**The idea:** give Claude a measurable objective, point it at your code, and let it experiment autonomously — proposing changes, testing them, keeping what works, discarding what doesn't, and repeating forever until you stop it.

```
/autoresearch "maximize pytest pass rate" "pytest -q 2>&1 | tail -1" "src/"
```

## How it works

```
┌─────────────────────────────────────────────────────┐
│                AUTORESEARCH LOOP                     │
│                                                      │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐        │
│  │ Propose  │──→│ Implement│──→│  Commit  │        │
│  │ (think)  │   │ (edit)   │   │  (git)   │        │
│  └──────────┘   └──────────┘   └──────────┘        │
│       ↑                              │               │
│       │                              ↓               │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐        │
│  │  Log to  │←──│ Evaluate │←──│   Run    │        │
│  │results.tsv   │(compare) │   │(measure) │        │
│  └──────────┘   └──────────┘   └──────────┘        │
│       │                                              │
│       ↓                                              │
│  keep? → advance branch                             │
│  worse? → git reset --hard HEAD~1                   │
│  crash? → fix or skip                               │
│                                                      │
│  REPEAT FOREVER (never ask, never stop)             │
└─────────────────────────────────────────────────────┘
```

## Dashboard & Observability

### Local Web Dashboard

A built-in web dashboard (zero Python dependencies, stdlib only) shows live experiment
progress — metric trends, keep/discard/crash stats, and a full experiment table.

```bash
python dashboard/server.py --port 8420 --results results.tsv
```

Open `http://localhost:8420` in any browser. Auto-refreshes every 3 seconds.

The skill automatically launches this during setup. No manual action needed.

### Remote Logging with Wandb

Optional integration with [Weights & Biases](https://wandb.ai) for remote experiment tracking:

```bash
# Install wandb (optional)
pip install wandb

# During autoresearch, the skill can log to wandb
python dashboard/wandb_logger.py --init --project my-experiment --config '{"objective":"minimize loss"}'

# Replay all results.tsv data to wandb after the fact
python dashboard/wandb_logger.py --replay --project my-experiment
```

Wandb is fully optional. All data is always available locally via `results.tsv` and the dashboard.

## Install

Copy the skill to your Claude Code skills directory:

```bash
# User-level (all projects) — skill only
mkdir -p ~/.claude/skills/autoresearch
cp .claude/skills/autoresearch/SKILL.md ~/.claude/skills/autoresearch/SKILL.md

# Or project-level (current project only, after cloning this repo)
mkdir -p /path/to/your/project/.claude/skills/autoresearch
cp .claude/skills/autoresearch/SKILL.md /path/to/your/project/.claude/skills/autoresearch/

# For dashboard + wandb support, copy the dashboard/ directory into your project:
cp -r dashboard/ /path/to/your/project/dashboard/
```

Or one-liner from GitHub:

```bash
mkdir -p ~/.claude/skills/autoresearch && \
curl -sL https://raw.githubusercontent.com/labclaw/autoresearch-skill/main/.claude/skills/autoresearch/SKILL.md \
  -o ~/.claude/skills/autoresearch/SKILL.md
```

Or use the install script:

```bash
./install.sh
```

## Usage

### Interactive setup

```
/autoresearch
```

Claude will ask you for:
1. **Objective** — what to optimize (e.g., "minimize val_bpb", "maximize test pass rate")
2. **Measure command** — how to measure it (e.g., `pytest -q | tail -1`)
3. **Edit scope** — which files Claude can modify (e.g., `src/model.py`)
4. **Timeout** — max time per experiment (default: 5 min)

### One-shot

```
/autoresearch "minimize bundle size" "npm run build 2>&1 | grep 'Total size'" "src/**/*.ts"
```

### What happens

1. Claude creates a `autoresearch/<tag>` branch
2. Runs the baseline and records the starting metric
3. Asks for confirmation once, then goes fully autonomous
4. Experiments indefinitely — you can leave, sleep, come back

When you return, you get:

```
=== Autoresearch Summary ===
Branch: autoresearch/mar26
Experiments run: 47
Kept: 12
Discarded: 31
Crashed: 4
Baseline metric: 0.998
Best metric: 0.871 (improvement: -12.7%)

Top improvements:
1. a1b2c3d — increase LR to 0.04 — 0.993
2. b2c3d4e — add cosine schedule — 0.961
...
```

## Examples

### ML training (Karpathy-style)

```
/autoresearch "minimize val_bpb" "uv run train.py > run.log 2>&1 && grep '^val_bpb:' run.log" "train.py"
```

### Test coverage

```
/autoresearch "maximize test pass count" "pytest --tb=no -q 2>&1 | tail -1" "src/ tests/"
```

### Build size

```
/autoresearch "minimize bundle size bytes" "npm run build 2>&1 | grep -oP 'Total: \K[\d.]+'" "webpack.config.js src/"
```

### Code quality

```
/autoresearch "minimize ruff warnings" "ruff check src/ 2>&1 | tail -1" "src/"
```

### API accuracy

```
/autoresearch "maximize extraction accuracy" "python benchmark.py 2>&1 | grep accuracy" "src/pipeline/"
```

## Design principles

Directly from [Karpathy's autoresearch](https://github.com/karpathy/autoresearch):

| Principle | Rule |
|-----------|------|
| **Autonomy** | Never stop. Never ask. The human may be asleep. |
| **Simplicity** | Simpler code at equal metric = keep. Complexity for tiny gain = discard. |
| **Git safety** | One commit per experiment. Revert cleanly. Branch never corrupted. |
| **Audit trail** | Every experiment logged to `results.tsv`. No exceptions. |
| **Scope** | Only edit declared files. Never touch evaluation harness. |

## How this differs from Karpathy's autoresearch

| Karpathy's autoresearch | This skill |
|---|---|
| Python script + `program.md` | Claude Code skill (SKILL.md) |
| Only edits `train.py` | User-defined edit scope |
| Only `val_bpb` metric | Any measurable objective |
| 5-min GPU training | User-defined timeout + command |
| ML architecture only | Any code changes |
| Single GPU required | Any compute environment |
| Claude Code / Cursor required | Claude Code only |
| No UI | Local web dashboard + wandb integration |

The loop structure is identical: **propose -> commit -> run -> evaluate -> keep/discard -> repeat**.

## Creating your own skill (template)

This repo serves as a template for creating Claude Code skills. The key file is `.claude/skills/autoresearch/SKILL.md`:

```yaml
---
name: your-skill-name
description: |
  What it does and when to trigger it.
argument-hint: "[arg1] [arg2]"
allowed-tools:
  - Bash
  - Read
  - Edit
---

# Your skill instructions here

Claude follows these instructions when the skill is invoked.
Use $ARGUMENTS for user input.
Use ```bash blocks for dynamic context injection.
```

See the [Claude Code docs](https://docs.anthropic.com/en/docs/claude-code) for the full skill specification.

## License

MIT
