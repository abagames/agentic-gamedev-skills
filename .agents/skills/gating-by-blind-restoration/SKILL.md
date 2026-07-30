---
name: gating-by-blind-restoration
description: "Validate that one abstraction layer (a spec, design doc, schema, contract, or generated artifact) is self-sufficient by spawning an ISOLATED sub-agent that sees only that layer and must reconstruct the adjacent layer, returning pass / weak-pass / fail. Use when checking whether an extracted or generated artifact preserves enough structure to be rebuilt or used without the original source, and to prevent an author from grading their own output."
---

# Gating by Blind Restoration

## Purpose

Check that an abstraction layer carries enough recoverable structure by testing
reconstruction under a strict information firewall — not by self-review. The gate's
authority comes from two things: the grader never saw the source, and the author never
grades their own work.

## When to Use

- After generating or extracting a spec, design doc, schema, API contract, or refactor plan.
- Whenever you need to answer "is this artifact enough to rebuild the next layer from?"
- Whenever the author of an artifact would otherwise judge their own work.

## When Not to Use

- Subjective quality (taste, "is it fun / elegant / well-written"). A firewall cannot decide
  that, and a confident-sounding grader will rubber-stamp it. Do not gate it.
- When the original source is the intended input anyway, so no abstraction is being trusted.

## Required Inputs

- The single artifact text under test.
- A definition of the adjacent layer to reconstruct (e.g. "an implementable structure",
  "a reproduction spec hypothesis", "the upstream requirements").

## Procedure

1. Pick the gate direction and prepare a **withheld evaluation key**:
   - **Restoration** — can the adjacent layer be recovered from this artifact alone?
   - **Degeneration** — does this generated artifact avoid a dominant exploit / collapse
     that a blind reconstructor would immediately find?
   List the load-bearing rules or exploit conditions that the restored result must preserve.
   The orchestrator keeps this key; the blind grader never sees it.
2. Spawn an **independent** sub-agent, run by the orchestrator — never by the artifact's
   author, who has already seen the source and cannot judge blind. A freshly spawned grader
   that sees only the artifact text **is a real, independent gate**; its verdict is a true
   gate verdict — do not downgrade it to "self-audit." The degraded path applies only when no
   separate grader can be spawned at all and you must judge from the same context that produced
   or read the source: in that case fall back to an explicit self-audit and **label the result
   as self-audit, not a gate verdict**.
3. Enforce the **input firewall**: pass ONLY the artifact text. Do NOT pass the source, the
   sibling artifact, runtime traces, observations, screenshots, or repository paths. A single
   leak makes the verdict worthless.
4. Task it to reconstruct the adjacent layer and report: recovered structure, ambiguities,
   and the rules it treated as load-bearing. Do not ask it to speculate about matches versus
   an original it cannot see.
5. **Ask the counterfactual question.** For each rule the grader recovered, ask what it
   **would actually have implemented**, not only what it believes the artifact says. A rule
   the grader can quote but would have implemented differently **has not transmitted**. This
   divergence is the gate's highest-value signal and a recoverability question alone cannot
   produce it.
6. After the blind grader returns, have an evaluator compare its reconstruction and
   counterfactual implementation against the withheld key. This comparison happens **after**
   the firewall measurement; never send the key back to the grader. The evaluator may inspect
   the artifact to count occurrences and placement, but must not replace the grader's reported
   reconstruction with its own reading.
7. Return **two** verdicts.

   Whole artifact:
   - `pass` — sufficient for the target restoration level.
   - `weak-pass` — core structure recoverable, exact details expected-missing.
   - `fail` — not enough recoverable structure; the artifact must be revised.

   Per load-bearing rule, assigned by the evaluator from blind evidence:
   - `unmissable` — the grader recovered it without prompting and its counterfactual
     implementation matches the withheld key.
   - `findable` — relevant text exists, but the grader missed it, reported ambiguity, or would
     have implemented the opposite.
   - `absent` — the grader did not recover it and the evaluator cannot locate an equivalent
     rule in the artifact.

   For `findable`, cite the misleading placement or emphasis that explains the transmission
   failure. For `absent`, cite the withheld-key item that was not recovered; do not pretend the
   blind grader could identify omitted content. Both are repair items even when the
   whole-artifact verdict is `pass`.

To wire gates into a multi-round generation/extraction pipeline (one-shot vs.
find→fix→re-check, round caps, abandonment classification), load
`references/gate-loop-modes.md`. For a single standalone check, steps 1–7 are enough.

## Validation

The gate worked if the verdict is backed by **concrete recovered/missing structure**, not
"looks fine": a `fail` must name a specific unrecoverable element or a specific dominant
exploit; a `pass` must point at the structure it actually recovered. A per-rule verdict must
trace the withheld-key item to the blind reconstruction and counterfactual answer.

## Common Failure Modes

- **Firewall leak** — source or sibling artifact slips into the gate input; the verdict no
  longer measures the artifact.
- **Self-grading** — the author runs the gate; bias toward pass.
- **Gating taste** — trying to firewall-test subjective quality instead of recoverability.
- **Verdict without evidence** — a bare pass/fail with no recovered/missing structure named.
- **Stated but not transmitted** — the artifact contains a rule, correctly and with its
  rationale, and the grader still would have built the opposite. Observed: a rule present once,
  in a subordinate clause following a more emphatic unconditional half, and absent from every
  section the document designated as a rule summary; the grader quoted it as recovered and
  named the opposite as what it would have implemented. Only step 5 surfaces this.

## Output

Two verdicts — whole-artifact (`pass` / `weak-pass` / `fail`) and per-load-bearing-rule
(`unmissable` / `findable` / `absent`) — plus a short report: recovered structure, ambiguities,
the evaluator's key comparison, and the counterfactual answers from step 5.

When an artifact passes after repair, have it carry an explicit note naming **which clauses are
rules and must survive editing**. The strongest reinforcements a repair produces tend to be
commentary *about* the gate, which is the first thing a later editor strips as scaffolding —
losing the repair without touching a single rule statement.
