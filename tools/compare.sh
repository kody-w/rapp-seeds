#!/bin/zsh
# Blind side-by-side: is the working-tree version of a seed better than the committed one?
# Each of three reviewer families sees both versions as X and Y in random order and picks one against RUBRIC.md.
# Keep the change only when at least 2 of 3 prefer it.   Usage: tools/compare.sh <seed-path> <tag>
cd "${0:A:h}/.." || exit 2
seed=$1; tag=$2; d=reviews/pairs/$tag; mkdir -p $d
git show HEAD:$seed > $d/old.txt || exit 2
cp $seed $d/new.txt
for m in gpt-5.6-sol gemini-4-argon claude-sonnet-5.5; do
  if (( RANDOM % 2 )); then x=old; y=new; else x=new; y=old; fi
  echo "$x $y" > $d/$m.order
  cp $d/$x.txt $d/X.$m.txt; cp $d/$y.txt $d/Y.$m.txt
  ( copilot -p "You are an adversarial reviewer. Read RUBRIC.md and MESSAGE.md in this repository. Then read two versions of the same seed: $d/X.$m.txt and $d/Y.$m.txt. Neither is known to be newer. Judge which version better meets the rubric as a whole for a non-technical first-time reader and a skeptical expert who checks every claim against the public sources (https://github.com/kody-w/rapp-installer, the installers at https://kody-w.github.io/rapp-installer/install.sh and install.ps1). Reply with ONLY this JSON: {\"better\": \"X\" or \"Y\", \"margin\": \"slight\" or \"clear\", \"why\": \"one sentence\"}" --model $m --allow-all-tools --log-level none > $d/$m.reply 2>&1 ) &
done
wait
python3 - "$d" "$tag" <<'PY'
import json, re, sys, pathlib
d, tag = pathlib.Path(sys.argv[1]), sys.argv[2]
votes = []
for m in ["gpt-5.6-sol", "gemini-4-argon", "claude-sonnet-5.5"]:
    x, y = (d / f"{m}.order").read_text().split()
    t = (d / f"{m}.reply").read_text(errors="replace")
    j = None
    for c in re.findall(r'\{[^{}]*"better"[^{}]*\}', t):
        try: j = json.loads(c); break
        except Exception: pass
    if not j: votes.append((m, None, "no JSON")); continue
    pick = x if j["better"].strip().upper() == "X" else y
    votes.append((m, pick, f'{j.get("margin")}: {j.get("why")}'))
new = sum(1 for _, p, _ in votes if p == "new")
counted = sum(1 for _, p, _ in votes if p)
verdict = "KEEP" if new >= 2 else "REVERT"
(d / "verdict.json").write_text(json.dumps({"tag": tag, "new_votes": new, "counted": counted, "verdict": verdict, "votes": votes}, indent=1))
print(f"{tag}: {verdict} ({new} of {counted} prefer the new version)")
for m, p, w in votes: print(f"  {m}: {p} | {str(w)[:170]}")
PY
