# Bundled Fixture Manual

Read this file only when using `assets/fixtures/`. It holds a runnable instance of the skill's
structure: a pure reducer, eight event traces an evaluee is given, six more that exist only for
scoring, an invariant checker, and thirteen standalone artifacts: nine defects across five families,
two clean controls, and two equivalent mutants.

## Run the Fixture

```bash
cd assets/fixtures
node check.mjs                  # reference: invariants and complete finals match, exit 0
node check.mjs mutants/m01.mjs  # exit 1 with the first violating step
node check.mjs mutants/m09.mjs traces-scoring.json   # scoring set; needed for the withheld tapes
```

`check.mjs` reports, per trace, the final state and the **first** step at which each invariant fails.
It also compares the complete final state with the bundled clean reducer, so missing effects that
never create an illegal intermediate state still fail. It derives its verdict from executions and
never inspects the candidate reducer source, so it can score a repair it has never seen.

## Withhold the Answer Key

One defect, `m09`, is unreachable from `traces.json` on purpose: an evaluee that only folds the tapes
it was handed cannot see it. Score repairs against `traces-scoring.json`; several other mutants also
gain additional coverage there. The scoring traces, `check.mjs`, and
`references/fixture-manifest.md` are answer key material. Never put any of them in an evaluee's
working copy.

## Measurement Limits

Each mutant is a single roughly 135-line reducer that a capable evaluee can read end to end in one
pass, so localization is nearly free and most arms converge on a repair. This makes the fixture
suitable for **suite detection**—where the subject is a test suite, not a reader—and for the
**over-repair control**, where reading the whole file should prevent a change to healthy code.

It is a weak instrument for **with / without comparison**. When both arms repair everything, a null
result measures the fixture's size rather than the instructions under test. Before claiming an
instruction set makes no difference, confirm that the arms were separated by something other than
reading effort. For that comparison, build mutants whose site is not visible from a single readable
file: defects split across modules, reachable only through a specific tape, or observable only in an
aggregate the evaluee must construct.
