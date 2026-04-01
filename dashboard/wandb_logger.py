#!/usr/bin/env python3
"""Wandb logger for autoresearch experiments.

Optional remote logging to Weights & Biases. Logs each experiment's
metric, status, and description as a wandb run entry.

Usage (standalone):
    python dashboard/wandb_logger.py --init --project my-autoresearch --objective "minimize loss"
    python dashboard/wandb_logger.py --log --metric 0.42 --status keep --desc "simplified layer norm"
    python dashboard/wandb_logger.py --finish

Usage (as module):
    from dashboard.wandb_logger import WandbLogger
    logger = WandbLogger(project="my-autoresearch", config={"objective": "minimize loss"})
    logger.log(metric=0.42, status="keep", description="simplified layer norm")
    logger.finish()
"""

import argparse
import json
import sys
from pathlib import Path

# Lazy import — wandb is optional
_wandb = None


def _get_wandb():
    global _wandb
    if _wandb is None:
        try:
            import wandb

            _wandb = wandb
        except ImportError:
            print("wandb not installed. Run: pip install wandb", file=sys.stderr)
            sys.exit(1)
    return _wandb


class WandbLogger:
    """Logs autoresearch experiments to wandb."""

    def __init__(
        self,
        project: str = "autoresearch",
        name: str | None = None,
        config: dict | None = None,
        dir: str | None = None,
    ):
        wandb = _get_wandb()
        self.run = wandb.init(
            project=project,
            name=name,
            config=config or {},
            dir=dir,
            reinit=True,
        )

    def log(
        self,
        metric: float | None = None,
        status: str = "keep",
        description: str = "",
        commit_hash: str = "",
        step: int | None = None,
    ):
        """Log a single experiment result."""
        wandb = _get_wandb()
        data = {
            "metric": metric if metric is not None else float("nan"),
            "status_keep": 1 if status == "keep" else 0,
            "status_discard": 1 if status == "discard" else 0,
            "status_crash": 1 if status == "crash" else 0,
        }
        wandb.log(data, step=step)

    def finish(self):
        """End the wandb run."""
        wandb = _get_wandb()
        wandb.finish()


def _parse_results_for_replay(path: Path, project: str):
    """Replay all experiments from results.tsv into wandb."""
    if not path.exists():
        print(f"No results.tsv found at {path}", file=sys.stderr)
        return
    lines = path.read_text().strip().split("\n")
    if len(lines) < 2:
        print("No experiments to replay.", file=sys.stderr)
        return

    header = lines[0].split("\t")
    rows = []
    for line in lines[1:]:
        parts = line.split("\t")
        row = {}
        for i, col in enumerate(header):
            row[col] = parts[i] if i < len(parts) else ""
        rows.append(row)

    logger = WandbLogger(
        project=project,
        config={"source": "results.tsv", "total_experiments": len(rows)},
    )
    for i, row in enumerate(rows):
        metric = None
        if row.get("metric") and row["metric"] != "ERR":
            try:
                metric = float(row["metric"])
            except ValueError:
                pass
        logger.log(
            metric=metric,
            status=row.get("status", "unknown"),
            description=row.get("description", ""),
            commit_hash=row.get("commit", ""),
            step=i,
        )
    logger.finish()
    print(f"Replayed {len(rows)} experiments to wandb project '{project}'")


def main():
    parser = argparse.ArgumentParser(description="Autoresearch Wandb Logger")
    parser.add_argument(
        "--init", action="store_true", help="Initialize a new wandb run"
    )
    parser.add_argument("--log", action="store_true", help="Log a single experiment")
    parser.add_argument("--finish", action="store_true", help="Finish the current run")
    parser.add_argument(
        "--replay", action="store_true", help="Replay all from results.tsv"
    )
    parser.add_argument(
        "--project", "-p", default="autoresearch", help="Wandb project name"
    )
    parser.add_argument("--name", "-n", default=None, help="Run name")
    parser.add_argument("--metric", "-m", type=float, default=None, help="Metric value")
    parser.add_argument(
        "--status", "-s", default="keep", help="Status: keep/discard/crash"
    )
    parser.add_argument("--desc", "-d", default="", help="Experiment description")
    parser.add_argument(
        "--results",
        "-r",
        default="results.tsv",
        help="Path to results.tsv (for replay)",
    )
    parser.add_argument("--config", "-c", default=None, help="JSON config string")
    args = parser.parse_args()

    if args.replay:
        _parse_results_for_replay(Path(args.results), args.project)
        return

    if args.init:
        config = json.loads(args.config) if args.config else {}
        logger = WandbLogger(project=args.project, name=args.name, config=config)
        # Save run info for subsequent --log calls
        run_file = Path(".autoresearch_wandb.json")
        run_file.write_text(
            json.dumps(
                {
                    "project": args.project,
                    "run_id": logger.run.id,
                    "entity": logger.run.entity,
                }
            )
        )
        print(f"Wandb run initialized: {logger.run.url}")

    elif args.log:
        run_file = Path(".autoresearch_wandb.json")
        if not run_file.exists():
            print("No active wandb run. Use --init first.", file=sys.stderr)
            sys.exit(1)
        info = json.loads(run_file.read_text())
        wandb = _get_wandb()
        run = wandb.init(
            project=info["project"],
            id=info["run_id"],
            entity=info["entity"],
            resume="must",
        )
        data = {
            "metric": args.metric if args.metric is not None else float("nan"),
            "status_keep": 1 if args.status == "keep" else 0,
            "status_discard": 1 if args.status == "discard" else 0,
            "status_crash": 1 if args.status == "crash" else 0,
        }
        wandb.log(data)
        wandb.finish()
        print(f"Logged: metric={args.metric} status={args.status}")

    elif args.finish:
        run_file = Path(".autoresearch_wandb.json")
        if run_file.exists():
            info = json.loads(run_file.read_text())
            wandb = _get_wandb()
            run = wandb.init(
                project=info["project"],
                id=info["run_id"],
                entity=info["entity"],
                resume="must",
            )
            wandb.finish()
            run_file.unlink(missing_ok=True)
            print("Wandb run finished.")
        else:
            print("No active run to finish.", file=sys.stderr)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
