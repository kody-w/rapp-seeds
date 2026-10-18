#!/bin/zsh
# Three-family review panel: Sol, Gemini, Claude Sonnet score one seed against RUBRIC.md.
# Usage: tools/review.sh <seed-path> <tag>   -> reviews/<tag>.json with every score and the median.
cd "${0:A:h}/.." || exit 2
seed=$1; tag=$2; mkdir -p reviews/raw
prompt="$(cat tools/REVIEW-PROMPT.md)

Seed file: $seed"
for m in gpt-5.6-sol gemini-4-argon claude-sonnet-5.5; do
  ( copilot -p "$prompt" --model $m --allow-all-tools --log-level none > "reviews/raw/$tag.$m.txt" 2>&1 ) &
done
wait
python3 - "$tag" "$seed" <<'PY'
import json, re, sys, statistics, pathlib
tag, seed = sys.argv[1], sys.argv[2]
rows = []
for m in ["gpt-5.6-sol", "gemini-4-argon", "claude-sonnet-5.5"]:
    t = pathlib.Path(f"reviews/raw/{tag}.{m}.txt").read_text(errors="replace")
    found = None
    for cand in re.findall(r'\{"seed".*?\}\s*\}?\s*(?=\n|$)', t, flags=re.S) + re.findall(r'\{\s*"seed".*\}', t, flags=re.S):
        try:
            found = json.loads(cand.strip()); break
        except Exception:
            continue
    if found is None:
        rows.append({"model": m, "error": "no JSON in reply"}); continue
    found["model"] = m
    found["total"] = sum(int(v) for v in found["scores"].values())
    rows.append(found)
totals = [r["total"] for r in rows if "total" in r]
out = {"seed": seed, "tag": tag, "reviews": rows,
       "median": statistics.median(totals) if totals else None,
       "min": min(totals) if totals else None, "n": len(totals)}
pathlib.Path(f"reviews/{tag}.json").write_text(json.dumps(out, indent=1))
print(f"{tag}: median {out['median']} min {out['min']} n={out['n']} totals={totals}")
for r in rows:
    print(f"  {r['model']}: {r.get('total', r.get('error'))} | weakest: {str(r.get('weakest',''))[:160]}")
PY
