# Adversarial Condition Catalog

Use this as a routing catalog. Start from the diff and restored invariant, identify which state
surfaces the patch can reach, and select conditions only from those surfaces. Do not inventory
unreachable rows. If a reachable condition has high failure cost but cannot be run, record it in
`untested_scope` with the reason.

Each selected condition names what to set up and what the *break* looks like, so a run can be
scored without knowing the patch author's intent.

## Input and randomness

| Condition | Setup | Break looks like |
| --- | --- | --- |
| **Another seed** | Re-run the repro tape under 3+ seeds other than the reported one | Symptom returns, or the invariant fails on a seed where the tape reaches different entities |
| **Idle policy** | No input at all, run to natural end | Score accrues, safety persists, or the patched path never runs and nothing notices |
| **Mashing policy** | Maximum-rate repeated input | A window, cooldown, or timer is refreshed faster than it drains; score per opportunity exceeds the cap |
| **Hold policy** | Hold the primary input for the whole run | A state entered on press is never exited; a drain that assumes release never runs |
| **Alternating policy** | Strict A/B alternation at high rate | Two mutually exclusive states are both entered, or a toggle desynchronizes from what it toggles |
| **Input at boundaries** | Input on the exact tick of a transition (spawn, death, phase change, restore) | The event is processed by both the old and the new state, or by neither |

## Time

| Condition | Setup | Break looks like |
| --- | --- | --- |
| **Different tick rate** | Run the same tape at 30 / 60 / 144 Hz, or at half and double fixed timestep | Outcome depends on frame count rather than elapsed time; a per-frame decrement drains at a rate the design did not choose |
| **Variable / spiked frames** | Inject a long frame (a 250 ms stall) inside the affected window | A window is skipped entirely, or a `while` catch-up loop runs the effect several times |
| **Pause / resume** | Pause inside the affected window, resume after a real-time delay | A deadline stored as an absolute time expires during the pause; a tween resumes from a stale base |
| **Multiple events in one tick** | Two hits, two pickups, two deaths on the same tick | Both are credited against one opportunity; ordering decides the result and the order is not defined |

## Identity and lifetime

| Condition | Setup | Break looks like |
| --- | --- | --- |
| **Pooled identity reuse** | Force an object back to the pool and re-acquire it | Flags set by the previous occupant are still set: the new entity cannot score, is already invulnerable, or is already dead |
| **Deferred callback after owner destruction** | Start a tween / timer / signal-connected effect, destroy the target before it completes | The completion writes into a freed or recycled object, resurrects a dead entity, or credits a score to nothing. **Engine-provided completions are the common case in mini-games; this is not an exotic async scenario** |
| **Destruction during iteration** | Remove an entity from inside a loop over the collection holding it | One element is skipped, or the same one is processed twice |
| **Identity vs. position** | Refer to the affected entity by index/slot after the collection has been compacted | Effects land on the wrong entity while every count stays plausible |

## Persistence and transitions

| Condition | Setup | Break looks like |
| --- | --- | --- |
| **Save / load mid-window** | Save inside the affected window, reload, continue | A field is absent from the snapshot and silently resets; a deadline restores as an absolute value that is now in the past |
| **Scene / level transition** | Trigger the defect, transition out and back | State the transition should clear survives; state it should keep is rebuilt to a default |
| **Restart without process restart** | Finish a run, start another in the same session | The second run starts with the first run's residue — the single most common way a fix passes in isolation and fails in play |
| **Restore of an older save** | Load a snapshot written by the pre-patch build | The patch assumes a field the old snapshot lacks |

## Semantics of the healthy case

| Condition | Setup | Break looks like |
| --- | --- | --- |
| **Normal-case diff** | Run a healthy tape that never triggers the defect, pre- and post-patch | Any observable difference. The patch was supposed to change only the broken path; a difference here means it changed more |
| **Inverse test** | Construct a case where the patched branch must not fire | It fires, i.e. the fix suppresses the mechanic rather than the defect |
| **Boundary values** | Zero, one, and maximum of whatever the patch counts | Off-by-one at the cap, or the guard excludes the first legitimate case |

## Budgets

Run these only when the project already has a recorded budget; without a prior number there is
nothing to regress against, and inventing one during validation produces a false regression.

| Condition | Setup | Break looks like |
| --- | --- | --- |
| **Frame time** | Compare against the recorded budget on the affected scene | Per-frame cost added inside a hot loop by a guard that could be checked once |
| **Memory / entity count** | Long run, sample active object counts | A lifetime the patch extended stops being reclaimed |
| **Build time** | Compare against the recorded baseline | Only relevant if the patch touched build inputs |

## Out of scope

Do not write conditions for these; this repository cannot demonstrate them, so any procedure here
would be untested advice:

- network authority, reconnection, rollback, lag compensation
- asset streaming, distributed builds, build farms
- production-scale architecture doctrine
- cross-repository build/test selection
