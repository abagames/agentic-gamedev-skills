# Mutant Manifest

The withheld ground truth for one mutant. Written **before** the operator is applied.

## Schema

```yaml
mutant_id:              # stable, opaque. Not descriptive — the id may leak into a filename
operator_id:            # from mutation-families.md
family:                 # timing/order | identity/lifecycle | scoring/resource/economy |
                        # persistence/save | RNG/determinism | input buffering |
                        # animation/gameplay sync | content/configuration
site:                   # file + symbol. Answer key
defect_mechanism:       # what the edit makes the program do differently, mechanically
precondition:           # state required for the defect to be reachable at all
reachability:           # which of the available traces/inputs actually reach it
expected_symptom:       # the observable a player or tester would report — player language
violated_invariant:     # the predicate that becomes false
hidden_oracle:          # how a grader detects it without seeing the site. Never shown to an evaluee
affected_scope:         # what else the edit could plausibly change
equivalent_risk:        # none | low | high — and on what observation set that was judged
restoration:            # the reference behavior, as behavior, not as a diff
clean_control:          # optional; required only for an over-repair-control protocol
symptom_report:         # the text handed to the evaluee. Must contain no code-level terms
```

## Rules

- **`mutant_id` is opaque.** `m03` is fine; `m03-pool-reuse` names the answer in the filename.
- **`expected_symptom` is in player language.** "Killing an enemy that already died gives points
  again", not "the `scored` guard is missing". `symptom_report` is stricter still: it is what the
  evaluee reads, so it must not name a function, field, file, or the defect class. Writing it in
  code terms is the most common way an evaluation is quietly given the answer.
- **`hidden_oracle` never leaves the manifest.** Not into the symptom report, not into the working
  copy, not into the instructions under test. An oracle the evaluee can read is a specification of
  the fix.
- **`restoration` describes behavior, not a diff.** "Each entity identity is credited at most once"
  — not "re-add `|| e.scored`". Judging by diff equality rejects correct alternative repairs and is
  the single most common scoring error.
- **`equivalent_risk` is measured, not guessed.** Run reference and mutant over the whole
  observation set. Identical everywhere means `high`, and the mutant leaves the pass/fail pool.
- **`clean_control` is goal-specific.** Require it when measuring over-repair and present it under
  the same protocol as defect cases. It is optional for direct suite detection and for workflow
  repair measurements that do not claim to measure over-repair.

## What may reach the evaluee

| Item | Pass to evaluee |
| --- | --- |
| `symptom_report` | yes |
| Mutated source | yes |
| Traces / inputs | yes |
| Instructions under test | yes |
| `site`, `operator_id`, `defect_mechanism` | **no** |
| `hidden_oracle`, `restoration`, `violated_invariant` | **no** |
| Reference source or its diff | **no** |
| That the artifact is a mutant at all | **no** |
| Any other mutant's result | **no** |

The last two matter most and are the easiest to leak by accident — in the framing of the request,
or by pointing the evaluee at a directory from which the reference is reachable.

## Freeze

Once evaluation starts, the manifest is immutable. Editing `expected_symptom` or a pass criterion
after seeing a result converts the measurement into a demonstration. If a mutant turns out to be
badly constructed, discard it and record why; do not repair it mid-run.
