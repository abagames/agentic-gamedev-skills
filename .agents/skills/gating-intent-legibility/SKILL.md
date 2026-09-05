---
name: gating-intent-legibility
description: "Measures whether a player who was never told the rules can read a game's intent off the screen, by sampling scenes from a recorded run and having an isolated agent that has not seen the design or source name the goal, the options, and the risk. Use when a game runs and its mechanics are verified but it is unknown whether the screen communicates what to aim for without a tutorial or HUD text, or as a cheap early gate that can fail a design for decision collapse before a telemetry sweep. Not for judging fun or difficulty, not for verifying that a mechanic matches its spec, and not for confirming that varied decisions survive continued optimal play."
---

# Gating Intent Legibility

## Purpose

Measure what a game's screen transmits to a player who was never told the rules. Nobody on the
project can judge this — designer, implementer, and any agent that read the source all know the
answer before they look.

The method is blind restoration applied to a new pair of layers: the artifact is a set of sampled
gameplay scenes, the layer to reconstruct is the player's intent, and the withheld key is the
design's stated core loop. Because an agent shown any screen invents a fluent goal, recovery is not
scored alone — each grader must also predict a frame it has not seen, which is then revealed, so
**the game supplies the ground truth**.

One capture set yields **per-scene intent** (goal, options, risk) and **cross-scene divergence** (do
different situations call for different actions). Divergence is a property of the set of verdicts; no
single scene carries it.

## When to Use

- A build runs, its mechanics are verified, and it is unknown whether a first-time player can tell
  what to do.
- A "visually self-explanatory" design claim, or a protagonist/danger/reward legibility claim, has
  only ever been checked by its author.
- Before adding a tutorial or explanatory HUD text.
- As a cheap falsifier before a balance sweep: if every situation calls for the same action,
  telemetry will only confirm it more slowly.

## When Not to Use

- **Confirming that decision variety survives continued play** — no image set supports that claim.
  Use `evaluating-gameplay-balance`.
- **Verifying a mechanic against its spec** — `probing-web-game-mechanics`.
- **Judging fun, taste, difficulty, or beauty** — a blind grader rubber-stamps these, and taste is
  outside what any firewall gate can measure.
- The build produces only title or attract frames.
- No isolated grader can be spawned. Label any such run "self-audit", not a gate verdict.

## Capture Contract

The instrument needs rendered frames; searchers run against models that draw nothing. Any engine,
three capabilities:

- **C1 — frame capture at chosen ticks** (a tick, not a wall-clock moment).
- **C2 — deterministic replay** of an exported input track into the rendering build, same states at
  the same ticks.
- **C3 — state fingerprint** at those ticks (score, entity count, position, phase) to confirm C2 held.

Check C1–C3 against the project; do not assume a tool provides them because it is adjacent. Headless
tooling that renders nothing cannot satisfy C1 however reproducible it is. For a **disposable
prototype built to be measured rather than shipped**, prefer a route where C1 and C3 already exist —
prerequisite capture work is a poor investment in something to be discarded. Route selection, not an
engine endorsement.

**Verify C2 by replaying twice and comparing C3 fingerprints against the search run.** If C1 is
missing or replay diverges: **do not reconstruct frames from simulated state or approximate the
track by hand** — mislabelled frames produce a confident wrong verdict. Record directly against the
rendering build instead, treat the run as naive-track, and report `collapse` as not measurable.

Read `references/capture-capability.md` when the capture path is not established, when deciding how
C1–C3 are satisfied on a given engine, or when a replay check has failed.

## Procedure

1. **Freeze the withheld key** before any capture is graded: intended goal in one sentence, the
   option set per state, the intended risk/reward pairing, and the intended action-class list.

2. **Drive the run with something that is not the judge** — scripted track, separate exploratory
   policy, or human. Record input source, seed, and length. The driver is a **search instrument,
   never an evaluator**: no driver fitness score enters any verdict.

3. **Run a coverage precheck.** Inspect phases, entity-count regimes, resource levels, and
   difficulty band. A run that never left one regime is `inadmissible-sample`, not collapse.

4. **Choose the track and respect what it licenses.**
   - **Skilled** (search-driven or expert human) — widest coverage; the **only track that may carry
     `collapse`**. Says little about first contact.
   - **Naive** (first-contact stand-in that still clears the precheck) — per-scene legibility and the
     entry-point comparison. **Never `collapse`**: low divergence is confounded with the driver's own
     repertoire.
   - **Degenerate** (idle, hold-only, spam) — licenses nothing; `inadmissible-sample` by construction.

   Both tracks on the same build, same Δ, same framing, yields the entry-point verdict.

5. **Sample, do not hand-pick.** Fixed-interval sampling from a recorded run (default: a tick count
   covering ≈30 s of play at normal speed, recorded and expressed **in ticks**), or enumeration of a
   state space declared before results were seen. Reject scene-by-scene curation and any set
   re-picked after a disappointing result. N ≥ 8 scenes per run.

6. **Build each scene as a triplet.** `t-Δback`, `t`, `t+Δfwd`. **Only `t-Δback` and `t` are ever
   shown in stage A; `t+Δfwd` is the withheld oracle.** Two lead-in frames are the minimum that
   recovers motion — displacement, hence direction and speed. **Use three lead-in frames when the
   game's decisions turn on acceleration** — gravity arcs, charge ramps, spring-loaded launches,
   anything where the player reads a curve rather than a line; two frames cannot recover it, and a
   third elsewhere costs grader attention for no information. Tune Δ to the action cycle (input →
   consequence resolved): `Δback ≈ half`, `Δfwd ≈ one full` cycle. Record both and the estimate. If
   the game has two cycles at different timescales (a fast dodge inside a slow build-up), Δ per scene
   family rather than one global pair, and record which family each scene belongs to.

7. **Stage A — one isolated grader per scene**, seeing only its own lead-in frames plus the control
   legend (what each input does physically). Never the design, README, source, repo path, spec,
   telemetry, mechanic names, the title, another scene, `t+Δfwd`, or capture-harness overlays and
   absolute tick/run labels — but **do not crop the game's own HUD or readouts**, which the player is
   entitled to see. Ask **goal**, **options**, **risk**, and an **unconditional prediction**, each
   pointing at supporting evidence in the frames; then the counterfactual — what it would press
   first, and why.

   **Ask sequentially and do not let an answer be revised.** Record the goal answer before showing
   the later questions. No hints, no escalation, no follow-up: the rungs of `weak` come from *where
   in the fixed sequence* the goal first appeared, never from telling the grader more.

8. **Stage B — reveal `t+Δfwd`.** The evaluator scores the prediction `matched` / `partial` /
   `contradicted`. **Only the unconditional prediction is scorable** (the frame followed the recorded
   run's input, not the grader's plan). The prediction **gates the case**: `contradicted` invalidates
   that scene's goal answer; otherwise the goal answer is scored against the withheld key.

   **The gate assumes consequence is inferable from the frames — a design property, not a
   universal.** Score only the deterministic component: gross motion, contacts, and what persists. If
   a mechanic resolves stochastically, the withheld key must declare it, and it is excluded from
   scoring rather than counted against the grader. Distinguish the two failures: predictions wrong
   about *object motion and contact* mean the frames do not transmit consequence; predictions right
   about motion but wrong about *which outcome fired* mean the game is stochastic by design. If more
   than a third of scenes are `contradicted` on motion-independent grounds, the prediction gate is
   uninformative for this game — report `prediction-uninformative`, score intent without the gate,
   and mark those verdicts lower-confidence.

9. **Compare against the key** — evaluator only; never send the key to a grader.

Non-positional state (charge, cooldown, resource, combo) must be drawn as a persistent on-screen
readout. If it is not, any verdict touching that mechanic is **void** and reported as an
implementation gap, because the grader was asked to read state the game never showed.

Read `references/tracks-and-sampling.md` before the first run against a new project, or when the
driving policy, track construction, sampling method, or Δ must be chosen for an unfamiliar action
cycle. Read `references/judging-and-controls.md` before briefing the first grader, when the question
set or prediction scoring changes, or when building the degraded control.

## Controls

At **first use and after any protocol change**, run a **degraded control**: the same build with
intent knowingly destroyed by deliberate presentation-layer defects, captured under identical
protocol and framing, interleaved, never announced. The instrument is trusted only once it
**separates the real build from the control** on both intent and divergence; otherwise report
`instrument-failure` and fix the protocol before reading any verdict. This is the same
instrument-confidence discipline any measurement harness needs before its numbers are read.

## Divergence Metric

Over scenes whose prediction was `matched` or `partial`, assign each counterfactual first action to
a class from the withheld list, flagging any class the design did not anticipate. Report
`distinct_classes`, `dominant_share` (largest class ÷ scored scenes), and per-class scene ids.

**Floor: 6 scored scenes.** Prediction-gating removes scenes from the pool, so N ≥ 8 captured does
not guarantee a usable sample. Below 6 scored, do not compute the metric — report
`collapse-not-measurable` and capture more scenes.

**What the number rests on.** The counterfactual action is not scorable against the oracle; its
quality control is indirect — a scene counts only because a *different* answer, the prediction,
passed. The metric therefore assumes a grader that read the board correctly also chose its action
from that board. That is an attentiveness proxy, not a correctness proof, and it is the metric's
weakest joint.

Scenes within a run are autocorrelated, so scene count is not observation count. Because of that:

- **`collapse` requires n ≥ 3 independent runs**, all skilled-track and differing by seed, each
  showing it. One run is a lead, not a finding.
- Claiming a design **moved** out of collapse needs **n ≥ 5** with no overlap against the recorded
  prior result.
- **Retraction is a valid output.**

`collapse` = `dominant_share ≥ 0.75` or `distinct_classes ≤ 2`, on a skilled track passing the
precheck. `spread` = several classes, none dominant. Calibrate the cut on the degraded control and
record it; a control that does not collapse means the metric is not discriminating.

## Limits

**The instrument is one-sided: it can fail a game, not pass one.** It measures the variety of
situations *presented*, an upper bound on the variety of decisions *exercised* — the sampler chose
the situations, but in play the player's own policy decides which recur. So `collapse` is actionable
alone; `spread` licenses nothing and the balance sweep still runs. Run this **before** that sweep,
never instead of it.

**A prototype verdict covers the design layer only.** Goal legibility, options, risk/reward, and
divergence transfer across engines; legibility at the shipping build's resolution, palette, and
scale does not — that belongs to visual direction on the real build. Re-run when the presentation
layer materially changes.

**Human-review flags** — raise, never score: motor feel and timing tolerance; novelty and surprise
(the grader's genre prior cuts both ways); colour-vision and small-screen accessibility; whether the
recovered goal is worth wanting.

Read `references/scope-and-limits.md` when a verdict is about to be carried into a redesign, a
release call, or a readability claim, or when someone disputes what the gate proved.

## Verdicts

Every verdict names the **artifact measured**: `prototype` or `shipping-build`.

Intent — `legible` (on prediction-passing scenes the intended goal was recovered unprompted, the
counterfactual action is one the design considers sensible, and the control was not read the same
way) / `weak` — any of: the goal was absent from the **goal** answer but present by the **options**
or **risk** answer; it was recovered on pressure-state scenes but not on neutral or early ones; or
the counterfactual action is legal but dominated / `illegible` (not recovered, or recovered equally
well on the control).

Variety — `collapse` / `spread` / `collapse-not-measurable` (naive track), with `distinct_classes`,
`dominant_share`, scene and run counts, track, and sampling method.

Entry point, only when both tracks were sampled on one build — `entry-legible` (naive diverges about
as well as skilled) / `entry-opaque` (skilled diverges, naive collapses: the decisions exist and the
way in is not communicated — repair the opening, not the decision space) / `not-measured`.

`prediction-uninformative` (the gate could not discriminate on this game, per step 8) leaves intent
scored ungated and lower-confidence, and leaves variety unscored.

`instrument-failure` (control not separated) **voids every axis** — the control tests the shared
instrument. `inadmissible-sample` (precheck failed or degenerate track) voids only the run that
produced it. Neither makes a claim about the game.

Per scene, record which of goal / options / risk transmitted, the prediction score, and for each miss
the specific visual element that was absent, ambiguous, or out-competed. **A verdict naming no visual
element is not a finding.**

## Validation

The gate worked if the verdict is backed by concrete recovered/missing structure, not "looks fine":
an `illegible` names the visual element that failed to transmit; a `legible` points at what the
grader actually recovered. Before publishing, confirm the four things whose absence silently
invalidates a verdict rather than degrading it:

- **Key frozen first**, and never revised to match an answer.
- **Firewall intact** — one grader per scene, and no grader saw `t+Δfwd` in stage A, another scene,
  the title, the source, or a repo path.
- **Control separated** the real build from the degraded one, at first use or after a protocol change.
- **Manifest complete** — artifact type, C1–C3 route, track, seed, replay check, precheck, Δ values,
  scene and run counts. A missing field is an unverifiable verdict.

## Output

The three verdicts, the control-separation result, the run manifest, and a per-scene table — goal /
options / risk transmission, prediction score, counterfactual action, assigned class — plus a repair
item per miss naming a visual element, and any human-review flags.

## Rules That Must Survive Editing

The clauses below are **rules**, not commentary. Each is here because its absence produces a
confidently wrong verdict rather than a less-informed one. Compress the prose around them freely; do
not drop them.

- One isolated grader per scene; `t+Δfwd` withheld through stage A.
- Key frozen before grading, never revised to match an answer.
- Degraded control at first use and after any protocol change.
- C1–C3 checked against the project; never reconstruct frames from simulated state.
- The driver is never the judge; driver fitness enters no verdict.
- `collapse` only on a skilled track, and only with n ≥ 3 runs differing by seed.
- Only the unconditional prediction is scorable, and it gates the scene.
- Precheck failure is `inadmissible-sample`, never `collapse`.
- Sampling is fixed-interval or pre-declared; no curation, no re-picking.
- The instrument is one-sided: `spread` licenses nothing and the balance sweep still runs.
- A prototype verdict does not license shipping-build readability.
- A verdict naming no visual element is not a finding.

## References

Each is loaded on its condition, not by default.

- `references/tracks-and-sampling.md` — before the first run against a new project, or when the
  driving policy, track construction, sampling method, or Δ must be chosen for an unfamiliar action
  cycle.
- `references/capture-capability.md` — when the capture path is not established, when deciding how
  C1–C3 are satisfied on a given engine, or when a replay check has failed.
- `references/judging-and-controls.md` — before briefing the first grader, when the question set or
  prediction scoring changes, or when building the degraded control.
- `references/scope-and-limits.md` — when a verdict is about to be carried into a redesign, release
  call, or readability claim, or when someone disputes what the gate proved.
- `references/failure-modes.md` — before publishing a `collapse` or `illegible` verdict, and whenever
  a run returns a surprising result.
