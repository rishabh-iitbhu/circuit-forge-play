#!/usr/bin/env python3
"""Append a single-line update entry to the implementation-status change log."""

import argparse
from datetime import datetime
from pathlib import Path


def update_change_tracker(message: str, log_path: Path | None = None) -> str:
    if log_path is None:
        log_path = Path(__file__).resolve().parent.parent / "assets" / "implementation_status" / "update_log.txt"

    log_path.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {message.strip()}"
    with open(log_path, "a", encoding="utf-8") as handle:
        handle.write(entry + "\n")
    return entry


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Append a one-line entry to the change tracker log")
    parser.add_argument("message", help="Single-line summary of the latest change")
    args = parser.parse_args()
    print(update_change_tracker(args.message))
