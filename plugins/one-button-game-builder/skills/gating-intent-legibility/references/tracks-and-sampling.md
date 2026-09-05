# Tracks, Coverage, and Sampling

Read this when setting up the first run against a new project, when the driving policy or track type
is being chosen, or when Δback / Δfwd must be derived for a game whose action cycle is not already
known. `SKILL.md` carries the rules that decide a verdict; this file carries the derivations, the
alternatives, and the construction guidance.

For the frame-capture and replay capabilities a run depends on, see `capture-capability.md`.

## Driving the run

The input during a sampled run must come from a scripted or replayed input track, a separate
exploratory policy, or a human — never the judging agent.

If the project already has an exploratory policy for balance telemetry, prefer it: it exists, it is
tuned to reach the game's interesting states, and reusing it keeps this gate's sample comparable with
the balance sweep that may follow.

## Tracks

`SKILL.md` fixes which track licenses which verdict. This section covers how to obtain each one.

### The search boundary, and why it is drawn here

A GA or other exploratory searcher is used here strictly as an **input-sequence search instrument**.
It explores input sequences and can detect degenerate play — states where mashing or idling becomes
optimal — and that is the whole of its role. It is **not a working evaluator** and cannot judge
whether a game is legible, interesting, or fun; automatic evaluation of one-button action mini-games
is not currently within reach, and this skill does not quietly assume otherwise. The judgment in this
gate belongs entirely to the blind image-judging agent, whose evidence is frames and nothing else.

Practically, this means a driver's fitness score never appears in a verdict, a driver is never asked
a question about quality, and a high-scoring track is evidence about *coverage*, not about design.

### Obtaining the skilled track

The skilled track needs an **exploratory policy runner**: random, heuristic, replay, or genetic
search over input sequences with fixed seeds, driving the game through a deterministic adapter with a
seeded random source and a public input schema. Reuse the project's existing runner if it has one
rather than building a parallel mechanism; if it has none, standing one up is a prerequisite project
task, not a step of this gate.

Against that runner, the usable policy set is roughly `no_input`, `hold_action`, `spam_action`,
`periodic_action`, `random_action`, and `exploratory`. The first three are the **degenerate track**;
`exploratory` is the **skilled track**; `random_action` is the usual basis for the naive track.

Record the run manifest in whatever fields the project's telemetry already uses for seed set, fixed
timestep, tick budget, and input schema, so a gate run and a balance run describe the same run the
same way rather than two different ways.

### Constructing the naive track

The naive track stands in for a player who has not yet learned the rules. It is **not** the
degenerate track — `no_input` and `hold_action` are learned-nothing *and* explore-nothing, and they
fail the coverage precheck.

Build it from the public input schema as lightly-structured input: seeded random input at a
plausible human cadence, or random input with brief holds, with no state-dependent decision-making.
`random_action` is usually the right starting point. Then **run the coverage precheck on it like any
other track**. A naive track that fails coverage is not evidence that the entry point is opaque — it
is an inadmissible sample, and the two must not be confused, because they recommend opposite repairs.

Both tracks must be sampled on the **same build, at the same Δ values, under the same framing** for
the entry-point comparison to mean anything. A difference produced by a protocol change between the
two runs is not a finding about the game.

## What the coverage precheck inspects

The precheck runs on the recorded run's objective state, not on the frames. Look at least at:

- **Distinct phases visited** — title / play / bonus / boss / game-over, whatever the game's phase
  enum contains. A run that stayed in one phase samples one phase.
- **Entity-count regimes** — the number of simultaneous hazards, targets, or actors, bucketed. A
  run that never saw more than two hazards has not seen the pressure states.
- **Resource / meter levels visited** — charge, ammo, shield, combo depth. A run that never spent a
  resource never presented the decision that spending it creates.
- **Score or difficulty band** — if difficulty scales, a run confined to the opening band has
  sampled the tutorial, not the game.

A run that never left one regime on all of these is an **inadmissible sample**. Report it as such.
It is not evidence of decision collapse, and publishing it as collapse blames the design for the
sampler's behavior.

The degenerate case worth naming explicitly: a run driven by an idle or single-repeated-input
policy presents few situations and will read as decision collapse for reasons that are entirely the
sampler's fault.

## Sampling methods

Two methods are admissible:

- **Fixed-interval sampling from a recorded run.** Default: a tick count covering roughly 30 seconds
  of play at the game's normal speed, scenes taken at a fixed tick interval. Record the interval in
  ticks. Do not budget in wall-clock: a run without rendering advances as fast as the machine allows,
  so the same wall-clock window covers wildly different amounts of game time on different machines.
- **Programmatic enumeration of a declared state space.** Declare the space *before* seeing any
  result — e.g. every combination of hazard-count bucket × player-resource level — and reach each
  combination by state injection into the running build. Record the declaration and its timestamp
  relative to the first result.

Inadmissible, and grounds for rejecting the set outright:

- Screens chosen one at a time by someone who knows the design, "to show the interesting moments".
  Such a set exhibits the intended variety by construction.
- Any set re-picked, re-rolled, or re-seeded after a disappointing divergence result. That converts
  the gate into a demonstration.

### Why scene count is not observation count

Scenes drawn from one such run are **autocorrelated**: consecutive samples share entity layout,
phase, and difficulty band, so eight scenes from one run are worth considerably fewer than eight
independent observations. This is the reason the collapse verdict is gated on independent *runs*
(n ≥ 3) rather than on scene count alone, and why raising N within a single run does not substitute
for a second run.

Alongside that, keep a record-and-compare discipline: record the accepted result and its spread in
the project's notes, so later runs compare against history instead of rediscovering the same
variation each time. A tail that is known and settled should not be re-litigated every time it
reappears.

## Deriving Δback and Δfwd

Define the **action cycle** as the number of frames from a player input to its consequence
resolving. Estimate it once per game and record the estimate.

- `Δback ≈ half the action cycle`. Then adjust: the fastest gameplay-relevant object must visibly
  move between `t-Δback` and `t`, but must not cross the screen or wrap. Too small and the pair
  degenerates into a still, reintroducing exactly the motion blindness the triplet exists to fix.
  Too large and the judge cannot tell which object went where, because correspondence between the
  two frames becomes ambiguous.
- `Δfwd ≈ one full action cycle`, so the consequence has resolved in the revealed frame. A forward
  offset shorter than the cycle reveals nothing scorable — the world has barely moved and any
  prediction "matches".

A game whose action resolves in 8 frames and one that resolves in 90 therefore get very different
spacing. A 30/30 split is the right default only when the cycle is around 30–60 frames; treating 30
as universal is the most common way this instrument is mis-tuned.

### When to add a third lead-in frame

Two lead-in frames are sufficient to recover motion: a pair gives displacement, hence direction and
speed, for every moving object, which is precisely what a single still lacks. A third lead-in frame
buys **acceleration**, and is worth adding only for games whose decisions turn on it — gravity arcs,
charge ramps, spring-loaded launches, anything where the player must read a curve rather than a
line. Adding it elsewhere costs grader attention for no information.
