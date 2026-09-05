---
name: localizing-game-state-divergence
description: "Localizes a reproducible gameplay defect to the first tick at which game state violates an invariant, by replaying a deterministic repro case and scanning a per-event observation trace (or bisecting only when replay is costly and the oracle is monotone), then reporting the first divergent event together with the state before and after it. Use when a game produces a wrong value, a duplicated or missing effect, or an impossible state, the defect can already be reproduced, and nothing throws — so there is no stack trace or error message to follow back. Not for crashes, exceptions, build failures, or test errors that already name a line; not for deciding whether a value is well balanced; and not for writing the fix itself."
---

# Localizing Game State Divergence

## Purpose

Find *when* a gameplay defect happens, in tick order, before anyone argues about *where* in the
code it lives. A semantic game defect — score credited twice, a cooldown that never expires, a
resource that refills across a save — throws nothing. There is no stack trace, so backward tracing
from an error has no starting point. The starting point has to be constructed: a per-event trace
plus a predicate that is true of every healthy state, scanned for the first index where the
predicate fails.

The output is a tick index and two states, not a diagnosis and not a patch.

## When to Use

- The defect reproduces deterministically, and the wrong observable is a value, a count, a
  duplicated or missing effect, or a state that should be unreachable.
- The symptom appears far from its cause: a HUD reads a wrong number, a run ends with impossible
  totals, a save restores something it should not.
- A log or telemetry dump exists and nobody knows which line in it is the first bad one.

## When Not to Use

- **The defect does not reproduce yet.** Stop. Everything below replays a fixed input; without one
  there is nothing to replay and any conclusion is a guess.
- An exception, crash, assertion, or failing test already names a file and line — follow that
  instead; this procedure is strictly more expensive.
- The value is correct but feels too strong, too weak, or unfun. That is a balance question, not a
  divergence.
- You already know the divergent tick and only need to choose the repair.

## Required Inputs

A `ReproCase` — the minimal contract, inlined here so this skill needs nothing else:

```yaml
id:            # stable name for this defect
seed:          # RNG seed, or "none" if the run is seedless
build:         # commit / build identifier
setup:         # starting state or save slot, if not a fresh run
inputs:        # ordered input events with their tick indices — the input tape
observe:       # the wrong observable, as a value: "score == 50 at tick 6, expected 30"
expected:      # the value a healthy run produces at that point
determinism:   # always | intermittent(n/m runs) — intermittent blocks this procedure
```

Also required:

- A **replayable core**: the game logic must be steppable from `(state, event) -> state` with no
  wall clock, unseeded RNG, or I/O in the path. If it is not, extracting one for the affected
  subsystem is prerequisite work and outside this procedure. A subsystem harness may be enough,
  but extracting one from a non-replayable real project has not yet been validated by this skill;
  report that gap instead of treating the harness as routine or proven.
- At least one **oracle predicate** (below).

## Procedure

1. **Write the oracle before looking at the trace.** State the property as a predicate over
   observed state, in a form that is true at every healthy step and mechanically checkable:

   - `INV-SCORE-ONCE`: no entity identity is credited score more than once.
   - `INV-<field>-SOURCE`: `<field>` changes only on the event types allowed to change it.
   - `INV-<x>-ROUNDTRIP`: after a restore, `<x>` equals the value captured at the matching save.

   A predicate that can only be evaluated by a human reading the log is not an oracle. If the
   property cannot be written this way, say so and stop — the defect is not localizable by this
   method, and a guessed fix is the alternative you are declining.

2. **Emit an observation trace.** One record per state transition, not per run. The field list is
   in `references/observation-event.md`. Emit from the replay, not from the live game, so the trace
   is reproducible.

3. **Replay and scan.** Fold the input tape through the core, keeping every intermediate state.
   Evaluate every oracle at every index. Record the **lowest** index at which any oracle first
   fails. Scan linearly when the trace fits in memory; bisect only when replay is expensive, and
   only if the oracle is monotone (once false, stays false) — a non-monotone oracle bisects to the
   wrong index.

4. **Stop conditions, applied in this order:**

   - **No oracle fails anywhere, but the final state is wrong.** The observation layer is too
     coarse: some state that changed is not in the trace. Add the missing field and re-run. Do not
     proceed to a fix. This is the most common outcome on the first attempt and it is a finding
     about instrumentation, not about the game.
   - **An oracle fails at index 0.** The setup is already invalid; the `ReproCase` starting state
     is wrong, not the game.
   - **Two oracles fail at the same index.** Report both. Do not pick the one that looks easier.

5. **Separate first violation from first cause.** The index where the predicate breaks is where the
   state became *observably* wrong. The write that made it possible is often earlier and silent —
   a flag set, an identity reused, a field left out of a snapshot. Walk backward from the divergent
   index over the fields the violated oracle reads, and report the earliest event that wrote any of
   them. Name both indices. Fixing at the violation index without doing this produces a guard that
   hides the symptom and leaves the bad write in place.

6. **Confirm the localization is causal.** Re-run the same tape with the single divergent event
   removed or its inputs changed. If the oracle still fails at the same index, the localization is
   wrong — the reported event is a bystander. Report this as a failed localization rather than
   handing off an unverified index.

## Output

A `DivergenceReport`:

```yaml
repro:                 # ReproCase id
oracle:                # the predicate that failed, verbatim
first_violation_index: # tick / event index
first_violation_event: # the event at that index
state_before:          # observed fields the oracle reads, immediately before
state_after:           # the same fields immediately after
earliest_writer_index: # earliest event writing any field the oracle reads
causal_check:          # confirmed | failed — result of step 6
unobserved:            # state deliberately not in the trace, and why
```

`unobserved` is required. A trace that claims full coverage is claiming the defect cannot be
anywhere else, which is almost never true and is the assumption that makes the next bug expensive.

## Validation

- The oracle is stated as a predicate and evaluated mechanically, not read by eye.
- `first_violation_index` is the lowest failing index, not the first one noticed.
- `causal_check` is `confirmed`, or the report says the localization failed.
- `earliest_writer_index` is present and is `<=` `first_violation_index`.
- The report contains no proposed patch. Choosing the repair is a separate decision, and mixing it
  in here is how a localization becomes an argument for a fix that was picked first.

## Common Failure Modes

- **Aggregate-only telemetry.** Run totals ("final score 50, expected 30") cannot localize
  anything; they are the symptom restated. Per-event records are the whole method.
- **Oracle written after reading the trace.** It will be shaped to accept whatever the trace shows
  and will pass. Write it in step 1 and do not edit it during step 3.
- **Non-determinism smuggled into replay.** An unseeded shuffle, a wall-clock read, or iteration
  over an unordered map moves the divergent index between runs. If the index is not stable across
  two replays, fix that before believing any index.
- **Stopping at the reader.** The HUD showing a wrong number is where you noticed it, never where
  it happened. Step 5 exists because this is the default mistake.
- **Bisecting a non-monotone oracle.** "Energy is within range" can fail, recover, and fail again;
  bisection lands on an arbitrary failure. Scan linearly unless the oracle is monotone.

## References

- `references/observation-event.md` — the per-event trace record, and how it differs from
  run-aggregate telemetry.
