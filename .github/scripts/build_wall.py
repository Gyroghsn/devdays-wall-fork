"""Collect every participant card into participants.json for the website.

Usage: python3 .github/scripts/build_wall.py [output_dir]
"""
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from wall import USERNAME_RE, parse_card

ROOT = Path(__file__).resolve().parents[2]


def joined_at(path):
    """Date of the commit that first added the card (falls back to now)."""
    try:
        out = subprocess.run(
            ["git", "log", "--diff-filter=A", "--format=%cI", "--", path.relative_to(ROOT).as_posix()],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout.split()
    except (OSError, subprocess.CalledProcessError):
        out = []
    return out[-1] if out else datetime.now(timezone.utc).isoformat(timespec="seconds")


def main():
    out_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT
    participants = []
    for path in sorted((ROOT / "participants").glob("*.json")):
        username = path.stem
        card, errors = parse_card(path.read_text(encoding="utf-8"))
        if not USERNAME_RE.match(username) or errors:
            print(f"skipping {path.name}: {errors or 'invalid username'}")
            continue
        participants.append({"username": username, **card, "joined": joined_at(path)})

    participants.sort(key=lambda p: (p["joined"], p["username"]))
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "participants.json").write_text(
        json.dumps(
            {"generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "participants": participants},
            ensure_ascii=False, indent=2,
        ),
        encoding="utf-8",
    )
    print(f"{len(participants)} participants written to {out_dir / 'participants.json'}")


if __name__ == "__main__":
    main()
