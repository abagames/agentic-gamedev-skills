# Bundled Fixture — Withheld Manifest

**Answer key.** Never include this file, or a path from which it is reachable, in an evaluee's
working copy.

## Navigation

- `Contents` defines the visible and withheld fixture parts and reference outcomes.
- `Entries` contains the answer-key record for m01 through m13.
- `Scoring Protocol` separates defects, clean controls, and equivalent mutants.

## Contents

```
assets/fixtures/
  reducer.mjs           reference implementation (also the diff key)
  traces.json           the eight tapes an evaluee is given
  traces-scoring.json   those eight plus six withheld tapes; scoring only
  check.mjs             invariant and reference-outcome checker; never reads candidate source
  mutants/m01..m13      standalone reducers, presentationally identical to each other
```

`traces.json` is the evaluee-visible tape set. `traces-scoring.json` adds six tapes that exist
only to score repairs; **it is answer key alongside `check.mjs` and never goes into a working
copy.** One of the nine defects, `m09`, is not reachable from `traces.json` at all, which is
deliberate: an evaluee that only folds the tapes it was handed cannot reach it. The withheld tapes
also add observations for several defects that are already reachable on the visible set.

Selected reference finals (`node check.mjs reducer.mjs traces-scoring.json`, exit 0).
`charging` is `false` and `chargeStart` is `-1` at the end of every tape.

| trace | given | tick | score | hp | energy | iframesUntil |
| --- | --- | --- | --- | --- | --- | --- |
| basic | yes | 6 | 30 | 2 | 5 | 34 |
| mash | yes | 33 | 0 | 1 | 4 | 62 |
| pool | yes | 4 | 30 | 3 | 5 | -1 |
| save | yes | 2 | 10 | 3 | 3 | -1 |
| save2 | yes | 2 | 0 | 3 | 5 | -1 |
| hold | yes | 12 | 25 | 3 | 3 | -1 |
| hold2 | yes | 8 | 25 | 3 | 3 | -1 |
| long | yes | 107 | 115 | 3 | 2 | -1 |
| hold_double_release | no | 13 | 25 | 3 | 3 | -1 |
| hold_miss_then_hit | no | 13 | 0 | 3 | 5 | -1 |
| hold_short | no | 7 | 0 | 3 | 5 | -1 |
| hold_boundary | no | 7 | 25 | 3 | 3 | -1 |
| release_bare | no | 9 | 0 | 3 | 5 | -1 |
| drain | no | 10 | 0 | 3 | 0 | -1 |

Oracles in `check.mjs`: `INV-SCORE-ONCE`, `INV-IFRAME-SOURCE`, `INV-POOL-FRESH`,
`INV-SAVE-ROUNDTRIP`, `INV-ENERGY-RANGE`, `INV-ENERGY-SOURCE`, `INV-CHARGE-ONE-SHOT`,
`INV-CHARGE-CONSUMED`, `INV-CHARGE-THRESHOLD`. The last five hold their ground-truth constants
locally rather than importing them, so a reducer that retunes `ENERGY_MAX`, `ENERGY_REGEN_EVERY`,
or `CHARGE_MIN` cannot move the bar it is scored against. `check.mjs` also compares the complete
final state with `reducer.mjs`; this catches missing effects such as m10 that do not create an
illegal intermediate state.

`save2` is the round-trip regression guard. It requires `save` and `load` to preserve `nextUid`,
`slots`, `charging`, and `chargeStart` as well as the scalar meters. `SNAPSHOT_FIELDS` uses an
order-insensitive structural comparison so object-key order does not count as divergence.

This bundled set is a reproducible demonstration, not a fresh workflow benchmark: its manifest is
distributed beside the artifacts. For a measured workflow comparison, create unused mutants and
keep their manifests outside every evaluee-accessible working copy.

## Entries

### m01

```yaml
mutant_id: m01
operator_id: SC-guard-dropped
family: scoring/resource/economy
site: mutants/m01.mjs, reduce() case "strike"
defect_mechanism: >
  The eligibility guard drops its already-dead and already-credited terms, keeping only the
  existence check, so every repeated strike on the same entity credits score again.
precondition: two or more strike events against one entity between its spawn and despawn
reachability: trace "basic" (slots a and b are struck twice each); not reached by mash/pool/save
expected_symptom: attacking an enemy that is already down keeps adding points
violated_invariant: no entity uid is credited STRIKE_SCORE more than once
hidden_oracle: INV-SCORE-ONCE fails at basic step 3; basic final score 50 instead of 30
affected_scope: scoring only; no lifetime, persistence, or timing field changes
equivalent_risk: none — observed divergence on trace basic
restoration: a strike credits score at most once per entity identity, and a downed entity is not
  re-credited. Any implementation with that behavior is correct.
clean_control: m05
symptom_report: >
  Players report that if they keep attacking an enemy that is already down, the score keeps going
  up. A recorded session is attached as the trace set.
```

### m02

```yaml
mutant_id: m02
operator_id: TO-refresh-on-input
family: timing/order
site: mutants/m02.mjs, reduce() case "tap"
defect_mechanism: >
  The tap handler also writes the invulnerability deadline, so any input renews a window that
  should only be renewed by taking a hit.
precondition: an input event inside IFRAME_TICKS of a subsequent hazard
reachability: traces "mash" (hp 3 instead of 1) and "save" (iframesUntil 31 instead of -1)
expected_symptom: you can button-mash your way out of taking damage; HP stops going down
violated_invariant: iframesUntil changes only on a hazard that lands, or on a restore
hidden_oracle: INV-IFRAME-SOURCE fails at mash step 1 and save step 3; mash final hp 3 instead of 1
affected_scope: damage timing; scoring and persistence untouched
equivalent_risk: none — observed divergence on traces mash and save
restoration: input alone never extends invulnerability; only a landed hazard does.
clean_control: m05
symptom_report: >
  A tester found that if you just keep tapping, hazards stop hurting you — HP never drops after
  the first hit. A recorded session is attached as the trace set.
```

### m03

```yaml
mutant_id: m03
operator_id: IL-pool-reuse / IL-identity-by-slot
family: identity/lifecycle
site: mutants/m03.mjs, reduce() cases "spawn" and "despawn"
defect_mechanism: >
  Despawn marks the entity not-alive instead of removing it, and spawn revives the pooled record
  rather than allocating a fresh identity, so the scored flag survives into the next occupant.
precondition: a slot despawned and respawned at least once
reachability: trace "pool" (score 10 instead of 30)
expected_symptom: after the first enemy at a spot, later enemies at that same spot give no points
violated_invariant: a spawn produces an identity never seen before, with no carried flags
hidden_oracle: INV-POOL-FRESH fails at pool step 5; pool final score 10 instead of 30
affected_scope: entity identity and scoring eligibility
equivalent_risk: none
restoration: each spawn yields a fresh identity that is independently eligible to score.
clean_control: m05
symptom_report: >
  Someone noticed that only the first enemy in a given position is worth points. The ones that
  appear there afterwards score nothing. A recorded session is attached as the trace set.
```

### m04

```yaml
mutant_id: m04
operator_id: PS-field-omitted
family: persistence/save
site: mutants/m04.mjs, reduce() case "load"
defect_mechanism: restore writes ENERGY_MAX instead of the snapshot's energy value
precondition: a save taken while energy is below maximum, followed by a load
reachability: trace "save" (energy 5 instead of 3)
expected_symptom: loading a save gives back a full energy meter regardless of what was spent
violated_invariant: every persisted field restores to the value captured at the matching save
hidden_oracle: INV-SAVE-ROUNDTRIP fails at save step 10; save final energy 5 instead of 3
affected_scope: persistence only
equivalent_risk: none
restoration: load restores energy to the saved value.
clean_control: m05
symptom_report: >
  A player reported that saving and reloading refills the energy meter, so you can top up for free
  by reloading. A recorded session is attached as the trace set.
```

### m05 — clean control

```yaml
mutant_id: m05
operator_id: none
family: control
site: none — behaviorally identical to reducer.mjs
defect_mechanism: none
precondition: n/a
reachability: n/a
expected_symptom: none; the reported symptom does not exist in this build
violated_invariant: none
hidden_oracle: all nine invariants and all reference-final comparisons pass on all fourteen tapes
affected_scope: n/a
equivalent_risk: n/a
restoration: no change is correct
clean_control: self
symptom_report: >
  A player reported that the invulnerability window sometimes does not protect them after a hit.
  A recorded session is attached as the trace set.
```

### m06 — equivalent

```yaml
mutant_id: m06
operator_id: TO-order-swap (on statements that do not share state)
family: timing/order
site: mutants/m06.mjs, reduce() case "strike"
defect_mechanism: >
  The score credit is moved ahead of the two flag writes. None of the three reads what the others
  write, so the resulting state is identical at every step.
precondition: none
reachability: every trace; no observable difference on any of them
expected_symptom: none observable
violated_invariant: none
hidden_oracle: full state sequence, finals, and invariants match the reference on all fourteen traces
affected_scope: none
equivalent_risk: high — confirmed by full-observation-set comparison
restoration: none exists; there is no defect to restore
clean_control: m05
symptom_report: >
  QA logged "scoring feels wrong on enemy kills" against this build without further detail. A
  recorded session is attached as the trace set.
```

### m07

```yaml
mutant_id: m07
operator_id: SC-per-input
family: scoring/resource/economy
site: mutants/m07.mjs, reduce() case "tap"
defect_mechanism: the tap handler credits STRIKE_SCORE, so score is paid per input rather than
  per scoring opportunity
precondition: any successful tap (energy >= TAP_COST)
reachability: traces "mash" (score 20 instead of 0) and "save" (score 30 instead of 10)
expected_symptom: you gain points just for pressing the button, without hitting anything
violated_invariant: score changes only on a strike that credits an eligible entity, or on a restore
hidden_oracle: INV-SCORE-ONCE fails at mash step 1 and save step 3
affected_scope: scoring only
equivalent_risk: none
restoration: input alone never awards score; only crediting an eligible entity does.
clean_control: m05
symptom_report: >
  A tester says the score goes up just from pressing the action button, even with nothing on
  screen to hit. A recorded session is attached as the trace set.
```

### m08

```yaml
mutant_id: m08
operator_id: IL-identity-by-slot
family: identity/lifecycle
site: mutants/m08.mjs, reduce() case "spawn"
defect_mechanism: >
  Entity identity is derived from the slot name instead of the monotonic counter, so every
  occupant of a slot shares one identity across its whole lifetime history.
precondition: two or more spawns into the same slot
reachability: trace "pool"
expected_symptom: >
  none in the totals — the score is right. Only per-entity accounting is wrong.
violated_invariant: a spawn produces an identity never seen before
hidden_oracle: >
  INV-POOL-FRESH fails at pool step 5 and INV-SCORE-ONCE at pool step 6, while every final-state
  field matches the reference. This is the case that separates aggregate checking from per-event
  checking: a suite that only compares finals passes it.
affected_scope: identity accounting; totals unaffected
equivalent_risk: low — no final-state divergence, but per-event divergence is observable
restoration: each spawn yields an identity distinct from every previous one.
clean_control: m05
symptom_report: >
  Our per-enemy kill statistics look wrong — the same enemy appears to be credited more than once
  in the breakdown, even though the total score looks right. A recorded session is attached as
  the trace set.
```

### m09

```yaml
mutant_id: m09
operator_id: SC-cost-skipped
family: scoring/resource/economy
site: mutants/m09.mjs, reduce() case "release"
defect_mechanism: >
  The hold is disarmed only on the path that actually fires the shot. A release that finds no live,
  uncredited target, or that cannot pay POWER_COST, returns with charging still true and chargeStart
  still pointing at the original press, so the charge is never spent.
precondition: a release that does not fire, followed by a later release, with no charge between them
reachability: >
  none of the eight supplied tapes. Every release in hold, hold2 and long finds a live, affordable
  target, so the arm is consumed and the mutant is byte-identical to the reference on all eight.
  Withheld tape hold_miss_then_hit reaches it.
expected_symptom: a charged shot that misses is not spent; the next release fires at full power
violated_invariant: a release ends the hold, whether or not the shot landed
hidden_oracle: >
  INV-CHARGE-CONSUMED fails at hold_miss_then_hit step 13 and INV-CHARGE-ONE-SHOT at step 16;
  hold_miss_then_hit final score 25 instead of 0 and energy 3 instead of 5
affected_scope: the charged-shot economy only; ordinary strikes, hazards and persistence untouched
equivalent_risk: none — divergence observed on hold_miss_then_hit over the fourteen-tape set
restoration: one hold pays for at most one release, hit or miss.
clean_control: m12
symptom_report: >
  A tester reports that if you charge up and let go at nothing — the enemy is already gone, or you
  just aimed at empty space — the charge is not used up. You can let go again at the next enemy and
  it still comes out at full power without holding the button again. A recorded session is attached
  as the trace set.
```

### m10

```yaml
mutant_id: m10
operator_id: IB-edge-to-level
family: input buffering
site: mutants/m10.mjs, reduce() case "charge"
defect_mechanism: >
  The "already holding" guard is gone, so a press arriving during an existing hold restarts it,
  moving chargeStart forward to the current tick. The release then measures a hold shorter than the
  one the player performed.
precondition: two charge events with no release between them
reachability: supplied tape hold2 (final score 0 instead of 25, energy 5 instead of 3)
expected_symptom: a shot held plenty long does not come out
violated_invariant: >
  a shot credits score only when the hold that armed it lasted at least CHARGE_MIN ticks, and every
  hold that did last that long and had a valid target fires
hidden_oracle: >
  no state invariant fires because a missing effect is not an illegal state.
  OBS-REFERENCE-FINAL fails on hold2: score 0 instead of 25 and energy 5 instead of 3.
  The hold_short and hold_boundary finals reject a constant-only repair: lowering CHARGE_MIN fires
  a four-tick hold, while raising it suppresses the exact-boundary shot.
affected_scope: charged shots only
equivalent_risk: none — divergence observed on hold2
restoration: a press during a hold changes nothing; the hold is measured from the press that began it.
clean_control: m12
symptom_report: >
  A player says the charged shot sometimes just does not come out. They held the button well past
  the point where it normally fires, and nothing happened. It seems to happen when they adjust their
  grip and press again part-way through the hold. A recorded session is attached as the trace set.
```

### m11

```yaml
mutant_id: m11
operator_id: TO-deferred-fires-late
family: timing/order
site: mutants/m11.mjs, reduce() case "tick"
defect_mechanism: >
  The regeneration test is evaluated against the tick counter before it advances, so the meter
  refills on the tick preceding each intended one, and picks up one extra refill at the very first
  tick of a session in which the meter is already below full.
precondition: a session long enough for the offset to survive without the meter saturating
reachability: >
  supplied tape long — first divergence at state 3 of 149, final energy 3 instead of 2. Also
  diverges per-event on mash and drain with identical finals. Not reachable on the other tapes.
expected_symptom: a long session ends with more in the meter than the session paid for
violated_invariant: the meter refills only on a tick whose resulting tick count is a multiple of the regen period
hidden_oracle: INV-ENERGY-SOURCE fails at long step 2 and mash step 12; long final energy 3 instead of 2
affected_scope: the meter only; scoring, damage and persistence untouched
equivalent_risk: none — divergence observed on long
restoration: the meter gains one unit on exactly the ticks the regen period selects, and no others.
clean_control: m12
symptom_report: >
  On long stages the meter ends the run one notch fuller than the session should have left it.
  Short sessions add up correctly. A recorded long session is attached as the trace set.
```

### m12 — clean control

```yaml
mutant_id: m12
operator_id: none
family: control
site: none — behaviorally identical to reducer.mjs
defect_mechanism: none
precondition: n/a
reachability: n/a
expected_symptom: none; the reported symptom does not exist in this build
violated_invariant: none
hidden_oracle: all nine invariants and all reference-final comparisons pass on all fourteen tapes
affected_scope: n/a
equivalent_risk: n/a
restoration: no change is correct
clean_control: self
symptom_report: >
  A player says the charged shot sometimes fires weaker than it should — as if part of the charge
  had leaked away while they were holding. A recorded session is attached as the trace set.
```

### m13 — equivalent

```yaml
mutant_id: m13
operator_id: CF-threshold-shift (moved to a point that is not a decision boundary)
family: content/configuration
site: mutants/m13.mjs, reduce() case "tap"
defect_mechanism: >
  The affordability guard is rewritten from "at least TAP_COST left" to "more than zero left".
  TAP_COST is 1, so the two admit exactly the same taps.
precondition: none
reachability: every tape; no observable difference on any of them
expected_symptom: none observable
violated_invariant: none
hidden_oracle: >
  finals and all nine invariants identical to the reference on all fourteen tapes — equivalent,
  confirmed by full-observation-set comparison
affected_scope: none
equivalent_risk: high
restoration: none exists; there is no defect to restore
clean_control: m12
symptom_report: >
  QA filed "the meter sometimes lets you act when it should not" against this build with no further
  detail and no repro steps. A recorded session is attached as the trace set.
```

## Scoring Protocol

- Score m01–m04, m07–m11 as defects. A repair passes when
  `node check.mjs <patched> traces-scoring.json` exits 0 and the reported localization reaches the
  manifest's `site`. Judge behavior, not textual equality with `reducer.mjs`.
- Score m05 and m12 as clean controls. A semantic change is a failure; comment-only or formatting
  changes may be recorded but do not fail the control.
- Keep m06 and m13 outside the pass/fail pool as equivalent mutants. Record whether the evaluee
  reports observational equivalence or invents a repair.
- Use `traces-scoring.json` for final scoring. The visible set does not reach m09, so a run against
  `traces.json` alone cannot distinguish repairing it from doing nothing.
