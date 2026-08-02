# ObservationEvent

The per-event trace record used to localize a divergence. One record per state transition.

This is a **different layer** from run-aggregate telemetry. Aggregate telemetry answers "how did
this run go" — final score, elapsed time, death counts, per-policy comparisons. It is scored once
per run and is the right shape for judging balance. It cannot answer "at which step did the state
first become wrong", because by construction it has already collapsed the step axis. Keep both;
do not try to widen an aggregate schema into this one, and do not emit this volume for every
routine run.

## Record

```json
{
  "i": 12,
  "tick": 6,
  "event": { "type": "strike", "slot": "a" },
  "actor": "player",
  "subject_id": "uid:1",
  "reads": { "slots.a.scored": false, "slots.a.alive": true },
  "writes": { "score": [30, 40], "slots.a.scored": [false, true] },
  "oracles": { "INV-SCORE-ONCE": true, "INV-IFRAME-SOURCE": true }
}
```

| Field | Required | Meaning |
| --- | --- | --- |
| `i` | yes | Monotone index in the trace. The unit of localization. Never reuse or reorder. |
| `tick` | yes | Simulation tick. Several records can share a tick; `i` breaks the tie. |
| `event` | yes | The input or system event that drove the transition. |
| `actor` | no | Who caused it: `player`, `system`, `ai`, `restore`. Separates player-caused from engine-caused divergence without reading code. |
| `subject_id` | when an entity is involved | **Stable identity**, not slot, index, or pool position. The single most important field: identity reuse is invisible without it, and pooled objects are where it bites. |
| `reads` | recommended | State the handler consulted, at its pre-transition value. Makes "the guard was checked and passed" distinguishable from "the guard was never reached". |
| `writes` | yes | Fields written by the handler as `[before, after]`. Include a same-value write as `[value, value]`; omit fields the handler did not write. |
| `oracles` | yes | Each predicate evaluated at the post-state. `false` marks a violation. |

## Rules

- **Emit from replay, not from the live session.** A trace captured live and a trace captured on
  replay that disagree mean the replay is not faithful; that is a bigger problem than the defect
  being chased.
- **`writes` records both values, including same-value writes.** After-only values force a second
  pass to reconstruct deltas. A refresh that writes a timer's current value is still a real write,
  so record it as `[value, value]` rather than making it indistinguishable from no write at all.
- **Identity is not position.** `slot: "a"` is a position. `uid: 1` is an identity. A pool that
  hands slot `a` to a fresh entity produces a correct-looking trace under positional keys and an
  obviously wrong one under identity keys.
- **Same-tick ordering is load-bearing.** Two events at one tick that commute in the healthy build
  may not commute in the broken one. Preserve emission order and never sort a trace by `tick`.
- **Do not sample.** Dropping records to control volume removes exactly the step you need. Bound
  the *tape*, not the trace: shorten the repro case instead.

## Cost

A full trace is large and slow. It is a debugging instrument, not a shipping feature. Gate it
behind a flag, emit only for a `ReproCase` replay, and restrict `reads`/`writes` to the fields the
declared oracles actually touch — that projection is usually a small fraction of game state and
keeps the trace readable by a person as well as a checker.
