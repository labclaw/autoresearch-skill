#!/usr/bin/env python3
"""Lightweight web dashboard for autoresearch experiment tracking.

Serves a live-updating HTML page that reads results.tsv and displays
metric trends, experiment status, and run details. Uses only Python
stdlib — no external dependencies required.

Usage:
    python dashboard/server.py [--port 8420] [--results results.tsv]
"""

import argparse
import json
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from typing import Any

HERE = Path(__file__).parent
TEMPLATES = HERE / "templates"
STATIC = HERE / "static"


def parse_results_tsv(path: Path) -> list[dict[str, Any]]:
    """Parse results.tsv into a list of dicts."""
    rows = []
    if not path.exists():
        return rows
    try:
        text = path.read_text().strip()
        if not text:
            return rows
        lines = text.split("\n")
        if not lines:
            return rows
        header = lines[0].split("\t")
        for line in lines[1:]:
            parts = line.split("\t")
            row = {}
            for i, col in enumerate(header):
                row[col] = parts[i] if i < len(parts) else ""
            rows.append(row)
    except Exception:
        pass
    return rows


class DashboardHandler(SimpleHTTPRequestHandler):
    """HTTP handler that serves the autoresearch dashboard."""

    results_path: Path = Path("results.tsv")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(STATIC), **kwargs)

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self._serve_template()
        elif self.path == "/api/results":
            self._serve_results()
        elif self.path == "/api/status":
            self._serve_status()
        else:
            super().do_GET()

    def _serve_template(self):
        """Serve the main dashboard HTML."""
        template = TEMPLATES / "index.html"
        if template.exists():
            content = template.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_error(404, "Template not found")

    def _serve_results(self):
        """Serve parsed results.tsv as JSON."""
        rows = parse_results_tsv(self.results_path)
        payload = json.dumps({"experiments": rows}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def _serve_status(self):
        """Serve a lightweight status endpoint."""
        rows = parse_results_tsv(self.results_path)
        kept = sum(1 for r in rows if r.get("status") == "keep")
        discarded = sum(1 for r in rows if r.get("status") == "discard")
        crashed = sum(1 for r in rows if r.get("status") == "crash")
        metrics = [
            float(r["metric"])
            for r in rows
            if r.get("metric") and r["metric"] != "ERR" and r.get("status") == "keep"
        ]
        payload = json.dumps(
            {
                "total": len(rows),
                "kept": kept,
                "discarded": discarded,
                "crashed": crashed,
                "best_metric": max(metrics) if metrics else None,
                "worst_metric": min(metrics) if metrics else None,
                "results_modified": os.path.getmtime(self.results_path)
                if self.results_path.exists()
                else 0,
            }
        ).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, format, *args):
        """Quiet logging — only errors."""
        if args and "404" not in str(args[0]):
            pass  # suppress noisy access logs


def main():
    parser = argparse.ArgumentParser(description="Autoresearch Dashboard")
    parser.add_argument(
        "--port",
        "-p",
        type=int,
        default=8420,
        help="Port to serve on (default: 8420)",
    )
    parser.add_argument(
        "--results",
        "-r",
        type=str,
        default="results.tsv",
        help="Path to results.tsv (default: ./results.tsv)",
    )
    args = parser.parse_args()

    results_path = Path(args.results).resolve()
    DashboardHandler.results_path = results_path

    # Serve from the autoresearch working directory for results.tsv access
    os.chdir(results_path.parent)

    server = HTTPServer(("0.0.0.0", args.port), DashboardHandler)
    url = f"http://localhost:{args.port}"
    print(f"Autoresearch Dashboard: {url}")
    print(f"Watching: {results_path}")
    print("Press Ctrl+C to stop")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nDashboard stopped.")
        server.server_close()


if __name__ == "__main__":
    main()
