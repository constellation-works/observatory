---
title: "I002 Crew Tier Routing Audit"
summary: "Audit Constellation's own model-tier routing policy against accumulated run outcomes, rather than benchmarking vendors against each other."
tags: [parallax, idea, constellation, model-routing, tiering, evaluation]
related: ["docs/ideas/README.md", "docs/research/README.md", "docs/sessions/2026-08-03-r04-attention-elasticity-instrument-check.md"]
created_on: 2026-08-03
updated_on: 2026-08-03
status: draft
idea_id: I002
---

# I002: Crew tier routing audit

## Idea

Stop comparing vendors and audit the routing policy instead.

Constellation already assigns work to model tiers — medium and hard tasks to the heavyweight crews,
low-complexity tasks to the cheaper ones, right-sized per task at the orchestrator's discretion.
That policy is load-bearing, it was set by judgment, and it has never been checked against what
actually happened afterwards.

Two questions, both with money or rework attached:

1. **Which tasks routed to the expensive tier would have landed fine on the cheap one?** Every one
   of those is margin, and Constellation is running near breakeven against its self-sufficiency
   target.
2. **Which tasks routed cheap came back needing rework, or produced plausible-but-wrong work a
   reviewer had to catch?** This is the expensive direction and it is invisible unless someone goes
   looking, because a cheap model that produces confident wrong output costs more than it saves.

The first pass needs no new evaluation runs. Orbit already records task complexity, assigned crew,
outcome, review findings, and self-reported frictions across months of operation. That is an
observational dataset the project owns outright.

## Why it might matter

It came out of rejecting a worse idea. The obvious version — benchmark Opus against Sol against
Gemini, tier by tier — was considered and dropped on 2026-08-03 for two reasons:

- **It reveals nothing that is acted on.** Daniel already routes by tier and the routing broadly
  works. A ranking is not a decision.
- **It rots.** Anthropic shipped eleven flagship releases in the fourteen months to 2026-08, and
  Google's Pro line sat frozen at 3.1 while Flash moved twice. A tier map built in August is stale
  by October, and maintaining it is a standing cost for a standing non-answer.

The routing audit inverts both problems. It measures where *our* boundary should sit rather than who
is ahead this month, so it stays valid as models churn. And its output is a policy change, not a
league table.

## What is unknown

- **Is the existing record rich enough?** The audit needs complexity, assigned crew, outcome, and
  rework signal joined per task. Whether that join is clean across months of schema drift is the
  first thing to check, and it may be the blocker.
- **Confounding by assignment.** Tier is assigned *because* of expected difficulty, so cheap-tier
  tasks succeeding does not by itself show the tier was sufficient — they were the easy ones. The
  usable comparison is at the boundary: tasks of similar complexity that were routed differently,
  or tasks re-run after a failure. Without that overlap there is no identification, only selection.
- **Sample size at the boundary** is probably small, since most tasks are routed unambiguously.

## Measuring rework when nothing is ever rejected

Task status cannot carry this signal. Work is merged and marked done for expediency, and fixes
arrive afterwards as separate tasks, so `outcome` is very close to a constant. The signal is not
missing though — it moved.

**Primary, retrospective: line survival in git.** For each commit attributed to a task, take the
lines it introduced, then blame the same files 14 and 30 days later and count how many survive. Low
survival means the work was rewritten. This is standard code-churn measurement, needs no process
change, and is derived entirely from history that already exists.

Line-level blame rather than file-touch counting, because it is what separates the two kinds of
churn: a later commit that **modifies the lines the earlier one introduced** is corrective, while
one that **adds new lines on the same surface** is the next feature. Counting file touches conflates
them and would make every hot file look defective. Weight by the size of the corrective diff — a
one-line follow-up and a rewrite are both rework but are not the same evidence.

**Secondary, contemporaneous: defects found at review.** Reviews happen before merge, so the
merge-anyway policy does not touch them. Whether the adversarial cross-provider reviewer found real
defects is recorded regardless of the disposition that followed. No settling window needed.

**Forward instrument: a `fixes` relation.** Fixes arrive as later tasks and the orchestrator already
sets dependencies and relations at creation, so a `fixes: T-xxx` relation costs the human nothing at
the moment they would otherwise be impatient. Git covers history retroactively; this covers new work
cleanly from the day it lands.

## Differential scrutiny, and why it helps

The obvious worry is that review intensity correlates with tier. It does, and **inversely**:
heavyweight-crew output is trusted and merged with light inspection, while weaker-model output is
scrutinised precisely because it is not trusted. The human reviewer has also said he cannot
outperform the heavyweight crews' writing, so his inspection of their work is a weak detector even
when he does look.

That biases the two measures in *opposite* directions:

- **Review findings are biased against the cheap tier.** More looking finds more defects, and many
  of those defects are then fixed before the code ever lands.
- **Line survival is biased against the heavyweight tier.** Its defects are the ones that get waved
  through, land, and are corrected later — exactly the churn this measure sees. Meanwhile cheap-tier
  defects caught pre-merge never appear in it at all.

So the pair brackets the truth. **If both measures agree on a tier ordering, the ordering survives
the scrutiny confound.** If they disagree, the disagreement localises where scrutiny is doing the
work, which is itself worth knowing. Neither measure alone should be reported.

**The cheap fix is randomisation.** If adversarial reviews are going to be added anyway to generate
signal, assign them to a *random* subset of tasks regardless of tier rather than where they feel
needed. Ad-hoc addition reproduces the same confound by hand. Random assignment breaks the
correlation between scrutiny and tier by construction and converts this from an observational study
into a randomised one — the difference between "we think" and "we know", for the price of the review
budget alone.

Note that this reframes the audit's second question. It is not only "is the cheap tier good enough";
it is also **"is the trust in the heavyweight tier calibrated?"** Merging without inspection is a
bet, and line survival is the only thing currently in a position to settle it.

## The judgment measure that already exists

The most interesting quantity is one nobody designed an eval for. Constellation's adversarial
cross-provider review policy means a reviewer from a different provider family inspects each piece
of work — so every review is a natural test of whether the reviewer *exercised judgment*: did it
find a real defect, or rubber-stamp the diff?

**Reviewer catch rate by tier** is therefore about as close to a direct measure of critical thinking
as this system can produce, and it accumulates for free as a byproduct of normal operation. It also
speaks to the property that matters most in practice and appears on no leaderboard: does the model
tell you when you are wrong. The 2026-07 Gemini 3.6 Flash reports of increased "laziness" — shorter,
more agreeable answers, less pushback on a wrong premise — describe exactly the failure this metric
would catch, and exactly the one coding benchmarks miss.

Caveat: catch rate confounds reviewer capability with executor quality. A low catch rate can mean a
weak reviewer or strong work. Pairing matters, and the cross-provider policy at least keeps the
pairs from being degenerate.

## Possible destination

A numbered research program — `R05`, on the constellation's own operations — is the likely home,
since the unit of study is a task rather than a market and the data contract is Orbit's records
rather than an external source. It could instead stay an ops analysis if the retrospective turns
out to be a one-off answer rather than a repeatable measurement.

Do not start it as a prospective eval. Prospective runs are only justified for the boundary cases
the retrospective leaves ambiguous, and designing them before knowing where those are would be the
same mistake R03's E01 made — building an experiment before checking the instrument.

## Next step

Smallest useful investigation, in order:

1. Join existing Orbit records into one table of
   `task → complexity → assigned crew → landed commits → review findings → frictions`, and report
   **coverage and boundary overlap only**. No modelling, no tier verdict. If similar-complexity
   tasks were never routed differently, the audit is not identifiable from existing data and the
   idea stops there, cheaply.
2. If there is overlap, compute 14-day line survival for the landed commits and check it is
   computable at all — attribution from task to commit is the likely failure point, not the blame.
3. Only then decide whether to start randomised review assignment, which is the point at which this
   stops being retrospective and starts costing budget.

## Graduation history

- 2026-08-03: Captured after rejecting a vendor tier-comparison benchmark as unactionable and
  fast-rotting. No destination assigned yet.
- 2026-08-03: Added rework measurement after establishing that task status carries no signal —
  work is merged and marked done, with fixes following as separate tasks. Recorded the inverse
  scrutiny gradient (heavyweight trusted, weak models inspected), the opposite-direction biases it
  induces in the two measures, and randomised review assignment as the fix.
