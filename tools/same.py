#!/usr/bin/env python3
"""Does every seed carry the one message? Checks the line and the three promises in each seed.

Full seeds must carry each promise with its sentence. Short seeds (card, short, badge) carry the
line and the three promise names. Exit 1 if any seed is missing a piece.   python3 tools/same.py
"""
import html, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LINE = "Your AI, as files you own."
PROMISES = [("Learn it in an hour.", "It thinks the way you do, so you can see how it works."),
            ("Run it on any computer.", "Mac, Windows or Linux. Its memory stays in your own folder."),
            ("Hand it to anyone.", "It is just files. One agent is one file.")]
FULL = ["README.md", "llms.txt", "seeds/hour/index.html", "seeds/paste/README.md",
        "seeds/room/README.md", "seeds/slides/index.html",
        "seeds/agent/first_hour_agent.py"]
SHORT = {"seeds/card/card.svg": ["Learn it", "in an hour", "Run it", "on any computer", "Hand it", "to anyone"],
         "seeds/short/script.md": [p for p, _ in PROMISES],
         "seeds/badge/README.md": []}


def plain(path):
    t = (ROOT / path).read_text(encoding="utf-8")
    t = re.sub(r"<[^>]+>", " ", t)
    t = html.unescape(t).replace("**", "")
    return re.sub(r"\s+", " ", re.sub(r"(?m)^\s*(?:>|\d+\.)\s*", " ", t))


bad = 0
for path in FULL:
    t = plain(path)
    missing = [LINE] * (LINE not in t) + [f"{a} {b}" for a, b in PROMISES if a not in t or b not in t]
    print(("ok   " if not missing else "MISS ") + path + "".join(f"\n       missing: {m}" for m in missing))
    bad += bool(missing)
for path, parts in SHORT.items():
    t = plain(path)
    missing = [LINE] * (LINE not in t) + [p for p in parts if p not in t]
    print(("ok   " if not missing else "MISS ") + path + "".join(f"\n       missing: {m}" for m in missing))
    bad += bool(missing)
sys.exit(1 if bad else 0)
