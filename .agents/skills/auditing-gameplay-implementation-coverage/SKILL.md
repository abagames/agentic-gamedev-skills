---
name: auditing-gameplay-implementation-coverage
description: "Audits a stateful game's specification, phase/state machine, implementation, presentation, and tests for scenario-specific omissions such as one phase missing an input alias, one actor skipping a rule, a state change lacking HUD feedback, an event lacking audio, or a lifecycle boundary failing to reset or freeze state. Use when a game mostly works but may contain unimplemented sibling cases, inconsistent behavior across phases or actors, or important rules with no concrete probe; scope the audit to behavior surfaces changed or plausibly reached by a cross-cutting mechanic, to named high-risk surfaces before release, or to a family implicated by repeated forgotten-case bugs. Do not use for a small isolated change already covered by a direct distinguishing assertion, and do not expand into unrelated behavior surfaces. Not for localizing an already-reproduced semantic divergence, validating an existing patch, measuring balance, or proving exhaustive correctness."
---

# Auditing Gameplay Implementation Coverage

## Purpose

Find missing members of behavior families. A game rarely omits a whole feature; it omits one member
of a set the code already declares — one phase that never got the second input alias, one actor
variant the freeze path skips, one saved field nobody restores. Each omission looks like working
code, because every branch present is correct.

This procedure builds an evidence-backed coverage ledger across intent, code, observable output, and
tests, then verifies the high-risk gaps without changing the audited behavior. The output is a
ledger of obligations and their status, not a repair.

## When to Use

- A change or a cross-cutting mechanic plausibly reaches several behavior surfaces, and only some
  of them were updated.
- Named high-risk families need inspection before a release.
- Repeated forgotten-case bugs point at one family — input aliases, actor variants, save fields —
  and the question is how many more members are missing.

## When Not to Use

- A small isolated change already covered by a direct distinguishing assertion. The ledger costs
  more than the assertion.
- A semantic divergence is already reproduced and needs a tick index; that is localization.
- A patch exists and the question is whether it is the real fix; that is repair validation.
- The question is balance, difficulty, or fun.
- Exhaustive correctness is wanted. This procedure finds gaps; a clean result is
  `no confirmed gap found` and never proof of completeness.

## Preserve Audit Integrity

1. Record the build or snapshot under audit.
2. List defects and inconsistencies already known to the auditor. Exclude them from novel-finding
   counts, though they may remain in the report as `known`.
3. Freeze the audit method and coverage axes before investigating individual candidates.
4. Do not repair production code during the audit. A repair changes the subject and contaminates
   later findings.
5. Treat a clean result as `no confirmed gap found`, never as proof of completeness.

## Build the Behavior Inventory

Freeze a bounded audit scope before building the inventory. For a change-triggered audit, include
only surfaces the change can plausibly reach and their structurally coupled siblings. For a release
or recurring-defect audit, name the high-risk families being inspected. Record the rest in
`unexamined_scope`; do not turn either trigger into a whole-project audit by default.

Read repository instructions first, then the design/intent documents, as-built specification,
entrypoints, state/phase machine, debug/test handles, and existing tests. Resolve the project's
declared authority order before comparing them.

Inventory only values evidenced by the project:

- phases, modes, screens, rounds, and transition boundaries;
- player actions, input aliases, press/hold/release semantics, and input locks;
- actors, effects, sources/owners, identities, and lifecycle states;
- state producers and consumers, including HUD, animation, audio, persistence, and telemetry;
- reset, freeze, save/restore, death, retry, and scene/round transition behavior.

Use `references/coverage-surfaces.md` to route the inventory. Do not form the full Cartesian product;
most combinations are meaningless.

## Derive Coverage Obligations

Assign every obligation a stable `OBL-<surface>-<number>` identifier. Derive obligations from one of
these evidence classes and record which class applies:

1. **Explicit:** a specification or repository rule directly requires the behavior.
2. **Structural sibling:** code or data declares a family whose members should receive the same
   treatment, such as input aliases, actor variants, phase handlers, registry entries, or save
   fields.
3. **Metamorphic:** two routes are declared equivalent and should produce the same observed result.
4. **Producer-consumer:** a produced state/event must have every required consumer, or a consumer
   must have a producer.
5. **Boundary:** entering, leaving, pausing, restoring, dying, or restarting creates a reset/freeze/
   persistence obligation.

Do not silently convert visual similarity or naming similarity into intent. If sibling equivalence
is plausible but not authoritative, create an `intent-unknown` question instead of a defect claim.

Prefer relational obligations over isolated examples:

```text
observe(run(phase, alias_a)) == observe(run(phase, alias_b))
all scoring producers preserve an allowed source tag
every decision-changing state has a pre-decision presentation consumer
every declared event is emitted or explicitly declared silent
```

## Map the Coverage Ledger

For each obligation, map all four links:

```text
authority -> implementation path -> player/debug observable -> concrete test
```

Record `none found` rather than leaving a cell blank. Classify the row:

- `covered`: all required links exist and the test checks a concrete outcome;
- `confirmed-defect`: authoritative behavior fails in a reproducible run;
- `implementation-gap`: authority is explicit but no implementation path exists;
- `probe-gap`: behavior exists but no test directly distinguishes it from the omitted case;
- `presentation-gap`: behavior changes a player decision but required feedback is absent;
- `spec-conflict`: authoritative artifacts or spec and implementation disagree;
- `intent-unknown`: a plausible sibling relation lacks authority;
- `unverified`: evidence is insufficient or the required path cannot be exercised.

A smoke test is not mechanic coverage. A test counts only when its expected value or relation would
fail if the member under audit were omitted.

## Search the Negative Space

Compare family membership rather than reading only implemented branches. Use fast textual and
structural searches to census both sides of each relation:

- phase declarations versus phase update/draw/input/audio/reset branches;
- input aliases versus every phase that accepts the action;
- actor/effect types versus collision, scoring, freeze, draw, audio, and cleanup paths;
- event registries versus emitters and explicit silence declarations;
- saved fields versus initialization, serialization, restoration, and migration;
- decision-changing state versus persistent pre-decision display;
- debug state versus every rule state needed for a mechanical check;
- spec rules versus concrete test assertions.

Prioritize separately implemented siblings, negative branches, boundary ticks, and cross-system
consumers. Use pairwise coverage when more than two independent axes interact; escalate to a larger
combination only when causality or the code path requires it.

## Verify Candidates

Verify in this order without editing audited behavior:

1. Confirm the obligation's authority and quote or cite its exact source.
2. Confirm the suspected path is reachable in the current build.
3. Create the smallest state setup and input/event sequence using the existing debug handle or
   harness.
4. State the expected concrete value or relation before running it.
5. Capture the observed value, phase, event, screenshot, or persisted record.
6. Run an inverse case where the obligation should not apply.
7. Downgrade to `unverified` or `intent-unknown` when any required evidence is missing.

For a visual obligation, inspect the reached screen; state-only telemetry cannot prove presentation.
For a test gap, provide the proposed assertion and the omission it would distinguish, but do not add
the test unless the user also requests implementation.

## Report

Return the `CoverageGapReport` defined in `references/coverage-gap-report.md`. Lead with confirmed
novel defects, then implementation/presentation/probe gaps, conflicts, questions, and covered
high-risk obligations. Include known exclusions and unexamined scope.

Do not report a coverage percentage unless the obligation set was frozen before candidate review and
the denominator is included. On a live build with no known defect denominator, report precision of
adjudicated findings and coverage deltas, not recall.

## Validation

- Every reported defect has authority, reachability, expected outcome, observed outcome, and an
  inverse or reason it is impossible.
- Every `probe-gap` names a specific omission that the proposed assertion would detect.
- Every obligation is derived from evidence rather than an imagined feature.
- The frozen scope follows the trigger, and unrelated surfaces are recorded rather than audited.
- Known findings are excluded from novel-effect claims.
- Important unexamined combinations appear in `unexamined_scope`.
- The audit makes no production behavior change.
