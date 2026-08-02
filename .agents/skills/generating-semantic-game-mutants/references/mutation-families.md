# Mutation Families

Operators that produce *semantic* gameplay defects: the build runs, nothing throws, and the game is
wrong. Operator IDs are stable shorthand for manifests.

Spread a mutant set across families. Depth in one family measures that family's tests and reports
the result as a total.

## timing/order

The event happens, at the wrong moment or in the wrong order relative to another.

| ID | Operator | Typical symptom |
| --- | --- | --- |
| `TO-refresh-on-input` | A window/deadline set by one event is also set by an unrelated input | Mashing renews invulnerability, a cooldown, or a grace period forever |
| `TO-order-swap` | Swap two handlers that run in the same tick and *do* share state | Damage applies before the shield it should have been blocked by |
| `TO-off-by-one-window` | `<` becomes `<=` on a deadline comparison | An effect lasts exactly one tick too long; visible only at boundaries |
| `TO-deferred-fires-late` | A completion callback is queued a tick later than the state it reads | Reads a value that has already advanced |

## identity/lifecycle

The wrong object, or a stale flag on the right one. **Includes deferred callbacks whose owner is
already destroyed** — engine tween/timer/signal completions make this ordinary in mini-games.

| ID | Operator | Typical symptom |
| --- | --- | --- |
| `IL-pool-reuse` | Reacquiring a pooled object keeps its previous flags instead of resetting | A fresh enemy is already "scored", already dead, or already invulnerable |
| `IL-identity-by-slot` | Identity keyed by slot/index instead of a stable id | Effects land on whoever occupies the slot after compaction |
| `IL-callback-after-free` | A completion writes to its target without checking the target still exists | Score credited to nothing; a dead entity resurrects; a freed field is written |
| `IL-despawn-soft` | Removal marks dead but leaves the object queryable | Downed entities still absorb hits or count toward a clear condition |

## scoring/resource/economy

The event is right, the amount or the eligibility is wrong.

| ID | Operator | Typical symptom |
| --- | --- | --- |
| `SC-guard-dropped` | Remove the already-credited check | The same target scores repeatedly |
| `SC-per-input` | Credit per input instead of per opportunity | Mashing outscores timed play |
| `SC-multiplier-persist` | A multiplier survives the event that should reset it | Score grows without the risk that was supposed to pay for it |
| `SC-cost-skipped` | An action's resource cost is not deducted on one path | A resource never runs out along that path |

## persistence/save

The snapshot and the restore disagree.

| ID | Operator | Typical symptom |
| --- | --- | --- |
| `PS-field-omitted` | Drop one field from the snapshot; restore leaves it at its default | A meter, cooldown, or streak silently resets on load |
| `PS-absolute-deadline` | Persist a deadline as an absolute time rather than a remaining duration | On restore the deadline is already past, or far in the future |
| `PS-restore-order` | Restore fields in an order where one overwrites another | A derived value clobbers the stored one |
| `PS-save-post-mutation` | Snapshot taken after the tick's mutations instead of before | Reload lands one tick ahead of where the player left |

## RNG/determinism

| ID | Operator | Typical symptom |
| --- | --- | --- |
| `RN-extra-draw` | One additional draw on a conditional path | Every later draw shifts; replays diverge only sometimes |
| `RN-shared-stream` | A cosmetic effect draws from the gameplay stream | Visual settings change gameplay |
| `RN-reseed-on-event` | Reseed mid-run from a non-run-derived value | Replay and attract mode diverge from live play |

## input buffering

| ID | Operator | Typical symptom |
| --- | --- | --- |
| `IB-buffer-not-cleared` | A buffered input survives the transition that should consume it | One press acts twice, e.g. confirms a screen and skips the next |
| `IB-edge-to-level` | Treat a held input as a fresh press each tick | Holding behaves like perfect mashing |
| `IB-window-extended` | Buffer window outlives the action it feeds | An input taken long ago fires at an unrelated moment |

## animation/gameplay synchronization

| ID | Operator | Typical symptom |
| --- | --- | --- |
| `AG-hitbox-from-visual` | Gameplay reads the interpolated visual transform instead of the simulation one | Hits register where the sprite is drawn, not where the entity is |
| `AG-effect-gates-logic` | A rule waits on an animation/tween completion | The rule stops firing when effects are disabled or the frame rate changes |
| `AG-state-on-anim-end` | State advances on animation end rather than on the game event | A skipped or interrupted animation strands the state |

## content/configuration

| ID | Operator | Typical symptom |
| --- | --- | --- |
| `CF-threshold-shift` | Move one tuning threshold past a decision boundary | A branch becomes unreachable while every value still looks plausible |
| `CF-table-row-swap` | Swap two rows in a data table | A wave, level, or drop is subtly wrong and no code changed |
| `CF-default-fallback` | A missing key silently falls back to a default | A typo in content produces playable-but-wrong behavior instead of an error |

## Operators to avoid

- **Crash-producing edits** (null a required reference, delete a `return`). Every suite catches
  these; including them inflates the score and measures nothing.
- **Dead-code edits** on unreachable paths. Undetectable for the right reason, and they read as
  suite failures.
- **Multi-site edits.** Two simultaneous defects make localization unscoreable — a partial repair is
  neither pass nor fail.
- **Anything requiring a scope this repository cannot demonstrate** — network authority,
  reconnection, rollback, asset streaming, distributed builds. Out of scope; do not write operators
  for them.
