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

1. Pick the gate direction:
   - **Restoration** — can the adjacent layer be recovered from this artifact alone?
   - **Degeneration** — does this generated artifact avoid a dominant exploit / collapse
     that a blind reconstructor would immediately find?
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
   likely matches, and likely mismatches versus the (unseen) original.
5. Return a verdict:
   - `pass` — sufficient for the target restoration level.
   - `weak-pass` — core structure recoverable, exact details expected-missing.
   - `fail` — not enough recoverable structure; the artifact must be revised.

To wire gates into a multi-round generation/extraction pipeline (one-shot vs.
find→fix→re-check, round caps, abandonment classification), load
`references/gate-loop-modes.md`. For a single standalone check, steps 1–5 are enough.

## Validation

The gate worked if the verdict is backed by **concrete recovered/missing structure**, not
"looks fine": a `fail` must name a specific unrecoverable element or a specific dominant
exploit; a `pass` must point at the structure it actually recovered.

## Common Failure Modes

- **Firewall leak** — source or sibling artifact slips into the gate input; the verdict no
  longer measures the artifact.
- **Self-grading** — the author runs the gate; bias toward pass.
- **Gating taste** — trying to firewall-test subjective quality instead of recoverability.
- **Verdict without evidence** — a bare pass/fail with no recovered/missing structure named.

## Output

A verdict (`pass` / `weak-pass` / `fail`) plus a short report: recovered structure,
ambiguities, likely matches, and likely mismatches.
