"""Grandma's telegraph office: one word goes out, nothing else."""
import json
import os
from pathlib import Path

WORD_BUDGET = 30
STEPS = ("collect", "tidy", "audit", "send")


def collect(_):
    return Path("entry.txt").read_text(encoding="utf-8")


def tidy(word):
    return " ".join(word.split())


def audit(word):
    if not word.strip():
        raise SystemExit("telegraph sent an empty word")
    if not (1 <= len(word) <= WORD_BUDGET):
        raise SystemExit("word misses the 1..30 gate")
    return word


def send(word):
    pouch = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    pouch.mkdir(parents=True, exist_ok=True)
    out = pouch / "entry.txt"
    out.write_text(word + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"ok": True, "word": word, "budget": WORD_BUDGET,
                      "out": str(out)}))


HANDS = {"collect": collect, "tidy": tidy, "audit": audit, "send": send}

if __name__ == "__main__":
    payload = None
    for step in STEPS:
        payload = HANDS[step](payload)
