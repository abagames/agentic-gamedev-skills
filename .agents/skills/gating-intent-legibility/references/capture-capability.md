# Capture Capability: Engine Routes, Replay Verification, and Fallback

Read this before the first run against a project whose capture path is not already established, when
deciding how C1–C3 will be satisfied on a given engine, or when a replay check has failed and the
fallback must be chosen. `SKILL.md` names C1–C3 and states the fallback rule; this file holds the
per-engine routes and the verification procedure.

## The routes are examples, not a platform list

C1–C3 are capabilities, not tools. Any means of satisfying them is fine, and a project that already
has its own capture path should use it and record how. The routes below are how projects in this
repository's orbit typically satisfy the contract.

**Verify per project rather than inheriting a capability from a citation.** A tool or workflow you
already trust usually covers part of the contract, not all of it, and the gap is exactly where a
confident wrong verdict comes from.

### Browser builds

A headless-browser probing harness that drives a real build — injecting and reading state and taking
screenshots — covers **C1 and C3** directly. **C2 remains the project's to establish**: screenshot
and state-injection tooling does not by itself guarantee that a recorded input track replays to the
same states.

### Godot builds

Headless Godot gives frame-bounded, reproducible runs (`--quit-after <N>`) and log capture, which
serve **C3**, and a seeded policy runner in the project's test tooling can supply the track itself.

**Headless renders nothing, so it cannot provide frame capture.** **C1 must be added by the
project**: run with rendering enabled rather than headless, and save the viewport image at the
chosen ticks.

That is prerequisite work with its own cost, not a step of this gate. It is also the reason
`SKILL.md` steers a *disposable* prototype — one built to be measured and then discarded — toward a
route where C1 and C3 already exist. The gate itself applies unchanged to a finished Godot build.

### Anything else

Satisfy C1–C3 by whatever route the engine offers, and record how in the run manifest.

## Verifying C2 — replaying a searched track into the rendering build

`SKILL.md` states the capability contract and the fallback rule. To check C2:

1. Export the search result as an input track: an ordered sequence of `(tick, input_frame)` using the
   public input schema, plus the seed.
2. Play it back into the rendering build twice, capturing a cheap state fingerprint (score, entity
   count, player position, phase) at each tick you intend to sample.
3. Compare the two playbacks against each other, and against the search run's state at those ticks.

All three must agree at every sampled tick. Two playbacks that agree with each other but not with the
search run mean the rendering build is deterministic but the two models differ — the frames would
show a different run than the one the searcher explored.

Two well-known replay failures are what this check catches. **Replay/attract determinism**: engines
that record inputs for attract replay re-run their update from replayed input, and anything
unguarded on that path — persistence writes, RNG draws, wall-clock reads — diverges. **Boot-frame
race**: start playback on an observed state, never on a fixed timeout, or the first ticks of the
track are silently discarded.

If the check fails, take the fallback in `SKILL.md`. Do not reconstruct frames from simulated state
and do not hand-approximate the track: frames mislabelled with a run they did not come from produce a
confident wrong verdict, which is strictly worse than reporting the verdict as not measurable.

## Fallback rationale

`SKILL.md` states the fallback rule: if C1 is missing or replay does not reproduce the states, do not
bridge the gap inside the gate run — record directly against the rendering build, accept that the run
is a naive-track run, and report `collapse` as not measurable.

The reasoning behind the prohibition is worth keeping explicit, because the improvised bridge always
looks cheap in the moment. Frames that do not correspond to the run they are labelled with are
indistinguishable from correct frames by inspection: nothing about them looks wrong, every grader
answers confidently, and the verdict is wrong for a reason no later reader can recover. A missing
verdict costs a run; a fabricated one costs trust in every verdict the instrument ever produced.

Establishing the replay contract is a legitimate project task with its own value — any telemetry
balance sweep needs the same deterministic forward model — but it is prerequisite work, scheduled and
costed as such, not something to improvise inside a gate run.
