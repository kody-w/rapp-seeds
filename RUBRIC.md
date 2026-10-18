# Rubric

Every seed is scored 0 to 10 on each line by three independent reviewers who did not write it
(one from a different AI family). The **median** total is the score; one reviewer swings about 4 points
between runs, so a single score is not trusted. A seed ships at a median of **90 or more of 100** with
no reviewer under 80, and the word check passes. Each night pass must raise the median or it is reverted.

| # | Criterion | 10 means |
|---|---|---|
| 1 | **Same message** | It carries the line and the three promises from MESSAGE.md, in those words. |
| 2 | **Simple** | Someone who never met us understands every word in five seconds. No machinery. |
| 3 | **All along** | A first-time person feels an obvious expectation finally met, not a novelty. |
| 4 | **True today** | Every claim works today and can be checked. Nothing planned or promised. |
| 5 | **One action** | One clear next step. Everything technical is behind "Details". |
| 6 | **The hour** | It moves a non-technical person toward running their own Brainstem within an hour. |
| 7 | **Open road** | Free and open for every future AI user. No pricing, no hype, no selling. |
| 8 | **Native** | It feels made for its medium (a page reads like a page, a card fits a pocket). |
| 9 | **Ambitious** | It speaks to everyone who will ever use AI, not a niche of developers. |
| 10 | **Clean** | No private names, no work content, no forbidden words (tools/words.py passes). |

Reviewer output: one score per line, the total, the single weakest line, and one concrete fix.

## How a change is judged (since pass 9)

Absolute scores drift about five points between runs of the same text, so small real improvements were invisible.
Each change is now judged **blind, side by side**: three reviewer families (Sol, Gemini, Claude Sonnet) see the
current and the candidate version in random order as X and Y and pick the one that better meets this rubric.
A change is kept only when **at least 2 of 3** prefer it (`tools/compare.sh`). Absolute scores
(`tools/review.sh`) are still taken now and then to find the weakest line and to decide when a seed ships.
