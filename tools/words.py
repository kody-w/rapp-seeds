#!/usr/bin/env python3
"""Word check for every seed: the brand stays simple and the same everywhere.

Fails on internal words a stranger would not understand, on retired names, and on
claims the rubric forbids. Prints each hit with file and line. Exit 1 on any hit.

    python3 tools/words.py seeds/
"""
import re
import sys
from pathlib import Path

# word -> what to say instead
BANNED = {
    r"\bRAPP/1\b": "say RAPP (the version tag lives only in the spec and code)",
    r"\bPrototyping Platform\b": "the acronym is Rapid Agent Prototype Platform, or just RAPP",
    r"\batoms?\b": "say 'your Brainstem'",
    r"\bLegion\b": "private tool, never public",
    r"\bgrail\b": "say 'the Brainstem core'",
    r"\bkernel\b": "say 'the Brainstem core'",
    r"\bdistros?\b": "describe it plainly",
    r"\borganisms?\b": "describe it plainly",
    r"\beggs?\b": "describe what it does",
    r"\bsoul\b(?!\.md)": "say 'the one page that tells it who it is' (the file name soul.md is fine)",
    r"\bframes?\b": "describe what it does",
    r"\btwins?\b": "describe what it does",
    r"\bholos?\b": "describe what it does",
    r"\bchants?\b": "describe what it does",
    r"\bDOGG\b": "internal",
    r"\bhives?\b": "describe what it does",
    r"\bVAI\b": "say 'your computer' or the device's name",
    r"\bminds\b": "say 'your computers'",
    r"\bAI estate\b": "say 'every computer you own'",
    r"\bRaptr\b|\bAiraptr\b|\bRapterBox\b": "retired names",
    r"\bzero[- ]meter\b|\bno usage\b": "it uses your Copilot sign-in; never claim zero usage",
    r"\bdisab(led|ility)\b": "never mention",
    r"\bcoming soon\b|\bplanned\b|\broadmap\b": "show only what works today",
    r"\$\s?\d|\bpricing\b|\bsubscribe\b|\bbuy now\b": "open road, no selling",
}

def scan(paths):
    hits = 0
    for root in paths:
        root = Path(root)
        files = [root] if root.is_file() else [p for p in root.rglob("*")
                 if p.suffix in {".md", ".html", ".txt", ".json", ".svg"} and p.is_file()]
        for f in sorted(files):
            for n, line in enumerate(f.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
                if "words-ok" in line:
                    continue
                # links are addresses, not words people read
                line = re.sub(r'https?://\S+|href="[^"]*"', " ", line)
                for pat, fix in BANNED.items():
                    for m in re.finditer(pat, line, flags=re.I):
                        hits += 1
                        print(f"{f}:{n}: '{m.group(0)}' -> {fix}")
    return hits

if __name__ == "__main__":
    targets = sys.argv[1:] or ["seeds"]
    h = scan(targets)
    print(f"words: {h} hit(s) in {', '.join(targets)}")
    sys.exit(1 if h else 0)
