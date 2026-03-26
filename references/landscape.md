# Autoresearch Ecosystem Landscape

> Last updated: 2026-03-26

## Origin

| Repo | Stars | Description |
|------|-------|-------------|
| [karpathy/autoresearch](https://github.com/karpathy/autoresearch) | 57K+ | The original. 630 lines, single GPU, `program.md` as meta-program. 20 improvements overnight. |

## Claude Code Skills (direct competitors)

| Repo | Stars | Key Differentiator |
|------|-------|--------------------|
| [Orchestra-Research/AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs) | 5,670 | 86 skills, two-loop architecture, supports 8 agents |
| [wanshuiyin/ARIS](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) | 4,249 | Cross-model adversarial review, full research lifecycle |
| [uditgoenka/autoresearch](https://github.com/uditgoenka/autoresearch) | 2,421 | 9 subcommands, guard clauses, domain auto-detection |
| [krzysztofdudek/ResearcherSkill](https://github.com/krzysztofdudek/ResearcherSkill) | 118 | `.lab/` dir, non-linear branching, 10 hypothesis strategies |
| [proyecto26/autoresearch-ai-plugin](https://github.com/proyecto26/autoresearch-ai-plugin) | 5 | MAD-based confidence scoring, `autoresearch.jsonl` persistence |

## Other Agent Ports

| Repo | Stars | Agent |
|------|-------|-------|
| [leo-lilinxiao/codex-autoresearch](https://github.com/leo-lilinxiao/codex-autoresearch) | 750 | Codex CLI, resume support, persistent lessons |
| [davebcn87/pi-autoresearch](https://github.com/davebcn87/pi-autoresearch) | 2,944 | Pi terminal, live dashboard, confidence scoring |
| [jmilinovich/goal-md](https://github.com/jmilinovich/goal-md) | 95 | Agent-agnostic, dual scoring (metric + trustworthiness) |
| [greyhaven-ai/autocontext](https://github.com/greyhaven-ai/autocontext) | 667 | 5 specialized agents, persistent knowledge across runs |

## Domain-Specific

| Repo | Stars | Domain |
|------|-------|--------|
| [RightNow-AI/autokernel](https://github.com/RightNow-AI/autokernel) | 845 | GPU kernel optimization (18→187 TFLOPS) |
| [jsegov/autoresearch-win-rtx](https://github.com/jsegov/autoresearch-win-rtx) | 394 | Windows + consumer RTX GPUs |
| [mutable-state-inc/autoresearch-at-home](https://github.com/mutable-state-inc/autoresearch-at-home) | 452 | Distributed swarm, SETI@home style |

## Research-Grade Systems

| Repo | Stars | Scope |
|------|-------|-------|
| [SakanaAI/AI-Scientist](https://github.com/SakanaAI/AI-Scientist) | 12,715 | Fully automatic scientific discovery |
| [aiming-lab/AutoResearchClaw](https://github.com/aiming-lab/AutoResearchClaw) | 8,902 | 23-stage pipeline, idea→paper, multi-agent debate |
| [HKUDS/AI-Researcher](https://github.com/HKUDS/AI-Researcher) | 4,967 | NeurIPS 2025, hypothesis→experiments→manuscript |
| [SamuelSchmidgall/AgentLaboratory](https://github.com/SamuelSchmidgall/AgentLaboratory) | 5,419 | End-to-end research, autonomous + co-pilot modes |

## Self-Improvement Systems

| Repo | Stars | Innovation |
|------|-------|------------|
| [gepa-ai/gepa](https://github.com/gepa-ai/gepa) | 2,991 | ICLR 2026 Oral, genetic-Pareto prompt evolution |
| [ShengranHu/ADAS](https://github.com/ShengranHu/ADAS) | 1,544 | ICLR 2025, meta-agents that invent agent architectures |
| [MaximeRobeyns/SICA](https://github.com/MaximeRobeyns/self_improving_coding_agent) | 294 | Agent edits its own codebase (17%→53% SWE-Bench) |
| [WecoAI/aideml](https://github.com/WecoAI/aideml) | 1,184 | Tree-search agent, 4x medal rate on Kaggle |

## Awesome Lists

| List | Stars |
|------|-------|
| [alvinunreal/awesome-autoresearch](https://github.com/alvinunreal/awesome-autoresearch) | 685 |
| [WecoAI/awesome-autoresearch](https://github.com/WecoAI/awesome-autoresearch) | 292 |

## Top 10 Design Patterns to Learn From

1. **Dual scoring** (goal-md) — separate metric quality from measurement trustworthiness
2. **`.lab/` directory** (ResearcherSkill) — gitignored experiment state survives all git ops
3. **Confidence scoring** (pi-autoresearch) — MAD-based stats after 3+ experiments to filter noise
4. **Cross-model adversarial review** (ARIS) — different LLM as reviewer catches blind spots
5. **Non-linear branching** (ResearcherSkill) — fork from any prior `keep`, not just HEAD
6. **Persistent lessons** (codex-autoresearch) — extract and persist what worked across sessions
7. **Tree search** (AIDE/weco) — explore multiple branches simultaneously
8. **10 hypothesis strategies** (ResearcherSkill) — ablation, amplification, inversion, decomposition, sweep, analogy, scaling, simplification, combination, isolation
9. **Guard clauses** (uditgoenka) — optimize one metric while protecting another
10. **Constructed metrics** (goal-md) — agent builds measurement system before optimizing
