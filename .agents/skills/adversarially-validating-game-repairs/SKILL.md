---
name: adversarially-validating-game-repairs
description: "Stress-tests an already-written game bug fix with adversarial cases selected from the state, timing, identity, lifecycle, persistence, and input surfaces the patch can actually reach, then returns a PatchEvidence record covering fail-to-pass, relevant pass-to-pass, inverse-case, invariant, and untested-scope evidence. Use when a fix makes the reported symptom go away and it is still unknown whether the fix is the real one or an overfit, coincidental, or plausible-but-wrong one. Not for finding unknown defects in a build (that is runtime smoke testing), checking one mechanic against its written spec, or judging difficulty, fun, or balance."
---

# Adversarially Validating Game Repairs

## Purpose

A fix that makes the symptom disappear has proven one thing: the symptom disappears under the one
condition that was tried. That is compatible with the fix being correct, and equally compatible with
it being a guard at the reader, a clamp on the output, a special case that happens to cover the
reported input, or a change that works only at 60 fps on seed 2001.

This procedure attacks the fix with conditions its author did not have in mind, and produces a
record an independent reader can check without re-deriving the author's reasoning.

## When to Use

- A patch exists, the reported symptom is gone, and confidence in *why* is low.
- The fix touches lifecycle, identity, timing, ordering, persistence, or a shared/pooled resource —
  the areas where a locally correct change is most often globally wrong.
- Before shipping a repair to a mechanic that players can grind, repeat, or abuse.

## When Not to Use

- No patch yet. There is nothing to attack.
- The build crashes or throws — establish runtime health first; adversarial conditions on a build
  that does not run produce noise.
- The question is whether a mechanic matches its written spec, or whether the game is well
  balanced. Both are different questions with different instruments.
- The change is cosmetic and cannot reach game state.

## Required Inputs

- The patch, as a diff.
- The `ReproCase` the patch was written against — minimal contract, inlined so this skill needs
  nothing else:

  ```yaml
  id:            # stable name for this defect
  seed:          # RNG seed, or "none"
  build:         # commit / build identifier
  setup:         # starting state or save slot
  inputs:        # ordered input events with tick indices — the input tape
  observe:       # the wrong observable, as a value
  expected:      # the healthy value
  determinism:   # always | intermittent(n/m runs)
  ```

- The invariant the patch claims to restore, stated as a checkable predicate.
- Whatever passing checks existed before the patch, so pass-to-pass has a baseline.

## Procedure

1. **Restate the claim without the author's explanation.** Write, from the diff alone, what the
   patch changes and what would have to be true for that to fix the reported symptom. Do not read
   the author's rationale first, and do not treat it as evidence when you do. An explanation is a
   hypothesis with a motive; the diff is the artifact.

2. **Establish fail-to-pass and relevant pass-to-pass.** Run the `ReproCase` on the pre-patch build (must
   fail) and the post-patch build (must pass). A repro that does not fail before the patch
   invalidates everything downstream — stop and fix the repro. Then run the existing healthy checks
   whose paths the patch can reach and confirm they still pass. State what those checks exercise;
   an unrelated green suite is not evidence. Record counts, not adjectives.

3. **Select adversarial cases by reachability and failure cost.** Use
   `references/adversarial-conditions.md` as a routing catalog, not a universal checklist. Map the
   diff and restored invariant to the state surfaces they can reach, then run the cheapest cases
   that cover those surfaces:
   - vary seeds only when the patched path consumes or depends on RNG;
   - vary frame/tick rate only when it reaches elapsed time, frame counts, deadlines, or ordering;
   - exercise pause/resume, scene transitions, or save/load only when it reaches that lifecycle;
   - exercise pooling, identity reuse, same-tick events, or deferred completions only when it
     reaches identity, ordering, or lifetime;
   - measure performance, memory, or build time only when a prior budget exists and the patch can
     affect it.

   Do not enumerate catalog rows the patch cannot reach. Record a reachable, high-cost condition in
   `untested_scope` when it matters but cannot be run.

4. **Attack the fix's shape, not only its inputs.** For each of these, decide yes/no with evidence:
   - Does the patch change the **first divergent write**, or add a check downstream of it? A guard
     at the reader leaves the bad write in place and fails the moment a second reader appears.
   - Does it **clamp an output** (`max(0, hp)`, `min(cap, score)`) rather than prevent the bad
     value? Clamping converts a visible defect into a silent one.
   - Does it **special-case the reported input** — a condition mentioning the exact entity, level,
     seed, or count from the bug report?
   - Does it change **only a constant** where the report describes wrong logic? Retuning a number is
     not a logic repair, and the two are routinely confused because both make the symptom go away.
   - Does it introduce state that a **pool, restore, or scene reload** can carry across a lifetime
     boundary?

5. **Test the inverse.** Construct a case where the patched code path *should not* trigger and
   confirm it does not. A fix that suppresses the symptom by suppressing the whole mechanic passes
   every test aimed at the bug.

6. **Judge by outcome, never by diff similarity.** If a reference or "correct" patch exists, do not
   compare against it. A different change that restores the invariant is correct; an identical
   change that does not is not.

7. **Do not let the fix's author supply the verdict.** The evidence must be reconstructable from the
   diff, the `ReproCase`, and the recorded runs alone. If a claim in the record can only be checked
   by asking the author what they meant, it is not evidence — rewrite it or drop it.

## Stop Conditions

- **The repro does not fail pre-patch.** Stop at step 2. Nothing after it means anything.
- **Any adversarial case reproduces the original symptom.** Stop and report; the patch is
  incomplete. Do not extend the patch and re-run in the same pass — a fix shaped around the case
  that caught it is a bigger overfit than the one you started with.
- **The invariant cannot be written as a predicate.** Report that the patch is unvalidatable by this
  method and say what a human has to judge instead.
- **Behavior is indistinguishable with and without the patch across every case.** Report
  `undecidable`. Do not resolve it by preferring the patched version.

## Output

A `PatchEvidence` record. Field list and a worked example are in `references/patch-evidence.md`;
the required fields are:

```yaml
patch_id:
root_cause_hypothesis:
violated_invariant:
fail_to_pass:
pass_to_pass:
adversarial_cases:
cross_configuration:
performance_impact:
fix_shape:
inverse_test:
untested_scope:
confidence:            # high | medium | low | undecidable
human_decisions_required:
```

`human_decisions_required` may not be empty. `untested_scope` contains important conditions the
patch plausibly reaches but this pass did not run; use `none identified from patch reachability`
when there are none. That phrase is scoped to the patch, not a claim of exhaustive game-state
coverage.

## Validation

- `fail_to_pass` names a run that actually failed before the patch.
- `pass_to_pass` reaches the patched subsystem, and an inverse case confirms the patched path does
  not fire when it should not.
- The restored invariant is evaluated directly on the post-patch repro.
- Every selected adversarial case names the patch surface that made it relevant.
- `confidence` is justified by the recorded runs and downgraded to `low` when `untested_scope`
  covers a condition the patch plausibly reaches.
- No field cites the author's explanation as its support.
- Steps 4 and 5 are answered explicitly, not implied by the other results.

## Common Failure Modes

- **Grading the explanation.** The rationale is coherent, so the patch is accepted. Coherent
  rationales accompany wrong patches at roughly the rate they accompany right ones.
- **Reporting the pre-existing suite as pass-to-pass.** A suite that never covered the mechanic
  passes before and after and proves nothing. Say what the passing checks actually reach.
- **Skipping a reached source of variation.** If the patched path consumes RNG, crosses a lifetime
  boundary, or depends on event timing, the corresponding condition is relevant even when the diff
  looks locally deterministic.
- **Confusing "symptom gone" with "invariant restored".** These come apart exactly when the patch
  is wrong, which is the case worth detecting.
- **Extending the patch mid-run.** Each extension invalidates the evidence collected so far, and the
  record ends up describing a patch that no longer exists.

## References

- `references/adversarial-conditions.md` — the condition catalog, with the setup and the observable
  break for each.
- `references/patch-evidence.md` — full `PatchEvidence` schema and a worked example.
