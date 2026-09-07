# Stress-Test Report Contract

For each concept or ruleset report:

- **Concept id** — preserve a supplied stable ID or assign one that does not depend on rank.
- **Mechanism signature** — preserve compatible normalized fields when supplied; use equal-format records when comparing concepts.
- **Core causal model** — actions, relevant state, automatic dynamics, progress, risk/failure.
- **Claim id / claim under test** — a stable claim ID and one falsifiable design claim at a time.
- **Attack / policy** — what adversarial or simple strategy was applied.
- **Evidence** — reasoning trace, state transition, simulation result, telemetry, or explicitly missing information.
- **Classification** — `fails`, `weak`, `unknown`, or `survives`.
- **Severity** — `core`, `major`, or `minor`.
- **Next discriminator** — smallest test that could change the conclusion.
- **Provenance** — source artifact and method for each observation, imported classification, or derived verdict.

At concept level, optionally add:

- **Overall status** — `hard_reject`, `weak`, `survives_with_unknowns`, or `survives_applied_tests`.
- **Primary failure mode** — strongest demonstrated problem, if any.
- **Strongest surviving hypothesis** — specific structural behavior that remains plausible.

`survives_applied_tests` does not mean `fun` or production-ready.

These classifications may be carried into curation with provenance, but none automatically becomes `hard_reject` or an evidence score. Include a `human_review` record using [human-review.md](human-review.md) when a named human test or investment checkpoint is relevant.
