# PatchEvidence

The record an adversarial validation returns. Written so a reader who has never seen the patch's
author can decide whether to ship it.

## Schema

```yaml
patch_id:                 # commit / branch / diff identifier
root_cause_hypothesis:    # what the diff implies must have been wrong, derived from the diff
violated_invariant:       # the predicate the patch claims to restore, checkable form

fail_to_pass:
  repro_id:               # ReproCase id
  pre_patch:              # observed value + FAIL
  post_patch:             # observed value + PASS
pass_to_pass:
  checks_run:             # count
  checks_passed:          # count
  reach:                  # what those checks actually exercise; "" is not acceptable

adversarial_cases:        # selected by patch reachability and failure cost
  - condition:
    reached_surface:      # RNG | time/order | lifecycle | identity | persistence | budget | other
    status:               # run-pass | run-fail | run-fail-then-pass | untested
    evidence:             # observed values, or the reason it is untested
cross_configuration:      # relevant tick rates, seeds, platforms exercised; "not reached" is valid
performance_impact:       # measured against a prior budget, or "not reached / no prior budget"

fix_shape:                # step 4 of the procedure, answered explicitly
  changes_first_divergent_write:   # yes | no | unknown
  clamps_output:                   # yes | no
  special_cases_reported_input:    # yes | no
  constant_only:                   # yes | no
  crosses_lifetime_boundary:       # yes | no
inverse_test:             # the case where the patched branch must not fire, and what happened

untested_scope:           # important reachable conditions omitted, or "none identified..."
confidence:               # high | medium | low | undecidable
human_decisions_required: # required, non-empty
```

## Rules

- **`root_cause_hypothesis` is derived from the diff, not quoted from the author.** If it can only
  be written by reading their explanation, write "cannot be derived from the diff" — that is itself
  a finding about the patch.
- **`pass_to_pass.reach` is mandatory.** "All 84 tests pass" is worthless when none of the 84 touch
  the mechanic. State what they cover, and say when the answer is "nothing in this area".
- **`untested_scope` is reachability-scoped.** Record important conditions the patch can reach but
  that were not run. If none were identified, say so explicitly; do not list every catalog row as
  not applicable.
- **`human_decisions_required` non-empty.** At minimum, whether the restored behavior is the
  intended design. A passing check is not a design approval, and this field is where that
  distinction is kept from quietly disappearing.
- **`confidence: undecidable`** when patched and unpatched builds behave identically everywhere
  tested. It is a real outcome, not a failure to try harder — and it must not be resolved by
  preferring the patched build.

## Worked example

A pickup's collect animation is a tween on the pickup node. Its completion callback credits the
player and frees the node. When the player dies mid-animation the level despawns everything, and the
tween completion still arrives.

```yaml
patch_id: fix/pickup-tween-after-despawn @ 4a91c2e
root_cause_hypothesis: >
  The tween completion callback credits the run total and then frees its node. Level despawn frees
  the node without cancelling the tween, so a completion arriving after despawn credits a run that
  has already ended and then frees an already-freed node.
violated_invariant: "no credit is applied to a run whose end-of-run total has already been read"

fail_to_pass:
  repro_id: pickup-collect-during-death
  pre_patch: "collect a pickup, die within the tween duration -> results screen total is 1 higher than the sum shown in play; second free logs an error — FAIL"
  post_patch: "same tape -> totals agree, no second free — PASS"
pass_to_pass:
  checks_run: 11
  checks_passed: 11
  reach: >
    Nine checks cover pickup spawn, normal collect, and score accumulation; two cover the death
    transition. None covered a collect overlapping a death before this patch, which is why the
    defect survived a green suite.

adversarial_cases:
  - condition: another seed
    status: run-pass
    evidence: "5 seeds; pickup placement varies, totals agree on all 5"
  - condition: mashing policy
    status: run-pass
    evidence: "collect input spammed through the death frame produces one credit, not several"
  - condition: deferred callback after owner destruction
    status: run-fail-then-pass
    evidence: >
      The defect itself. Post-patch, forcing despawn at 50% tween progress cancels the tween and
      credits nothing; at 99% progress the completion is likewise cancelled. This is the condition
      that produced the bug and it needed its own case, not just the original repro.
  - condition: scene transition
    status: run-pass
    evidence: "collect, then transition before completion: no credit leaks into the next scene's total"
  - condition: restart without process restart
    status: run-pass
    evidence: "three consecutive runs in one session; run 2 and 3 totals start at 0"
  - condition: pause / resume
    status: run-fail
    evidence: >
      Pausing mid-tween and resuming after 5 s credits correctly, but the tween restarts its
      easing from the paused value, so the pickup visibly jumps. Not the reported defect and not
      introduced by this patch — filed separately rather than folded into this one.
  - condition: tick rate 30 / 60 / 144
    status: run-pass
    evidence: "totals identical at all three; the tween is time-driven, not frame-driven"
  - condition: normal-case diff
    status: run-pass
    evidence: "a run with no death during a collect is observably identical pre- and post-patch"
  - condition: save / load
    status: untested
    evidence: "this game has no mid-run save"
cross_configuration: "30/60/144 Hz, 5 seeds, desktop build only; no mobile or web export exercised"
performance_impact: "frame time unchanged within the recorded 2.1 ms budget for this scene"

fix_shape:
  changes_first_divergent_write: yes
  clamps_output: no
  special_cases_reported_input: no
  constant_only: no
  crosses_lifetime_boundary: yes
inverse_test: >
  A pickup collected with no death must still credit exactly once and still free its node.
  Confirmed over 20 collects; total 20, no leaked nodes.

untested_scope: >
  Web and mobile exports. Two pickups completing on the same frame as a death. Any path where a
  tween is owned by a node other than the pickup itself.
confidence: medium
human_decisions_required: >
  Whether a pickup collected during the death frame should count for the run at all. The patch
  drops it; crediting it before the results screen reads the total is equally consistent with the
  invariant, and which one players will consider fair is a design call.
```

Note what the example does *not* do: it does not claim the untested conditions passed, it keeps a
`run-fail` that the patch did not cause rather than quietly dropping it, and it does not raise
`confidence` to `high` on the strength of eleven green checks.
