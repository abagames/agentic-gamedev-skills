---
name: extracting-spec-design-ladders
description: "Reverse-engineer existing source code into a two-layer artifact ladder — a concrete reproduction spec (preserves behavior-affecting constants, same-tick ordering, input edges, collision/threshold semantics; drops cosmetics) and an abstract design doc (intentionally omits reproduction detail and records what is unspecified vs. safe-to-assume). Use to document or recover a program's intent and reproducible behavior without leaking implementation-only detail into the design layer."
---

# Extracting Spec / Design Ladders

## Purpose

Turn read-only source into two separated layers with non-overlapping responsibilities: a
faithful **reproduction spec** (enough to rebuild observable behavior) and an abstract
**design doc** (intent and experience, deliberately stripped of reproduction detail).

## When to Use

- Recovering intent and reproducible behavior from an existing program.
- Producing documentation that must let someone REBUILD behavior (spec) and, separately,
  understand DESIGN intent (design doc) without the two contaminating each other.

## When Not to Use

- Pure summary or README work where reproduction fidelity is not required.
- When a maintained spec already exists and only needs editing.

## Required Inputs

- Read-only source (treat as input only; never edit it).
- Any engine/runtime convention doc, so shared helper behavior is referenced once, not
  re-specified in every artifact.

## Procedure

1. **Spec layer.** Preserve only what changes observable play/behavior: goal, core loop,
   required state & resources, input behavior, scoring/failure, balance-critical constants and
   formulas. Drop cosmetics. The detailed preserve-vs-drop rules — same-tick ordering,
   collision/hitbox/threshold semantics, spawn/target/random/input-edge behavior, reusable
   scoring/safety pulses — are a checklist; load `references/spec-preservation-checklist.md`
   while writing the spec.
2. **Design layer.** Working **from the spec only**, write the abstract doc: experience core,
   decisions asked of the user, risk/reward, how tension is built, learning curve, room for
   reinterpretation, and the invariant structure. Convert numeric balance into qualitative
   intent. Never leak exact constants, formulas, random ranges, tick counts, or source names.
   Add explicit recovery guidance: what to **treat as unspecified**, what is **safe to assume**,
   and the **restoration priority** order.
3. **Log** what was abstracted, preserved, omitted, and added as recovery guidance, so the
   abstraction is auditable. Keep it as a short section inside the design doc, OR — if the log
   needs to cite specific abstracted constants or source names — in a sibling log file, since
   putting those specifics inside the design doc would violate its no-leak rule.

## Validation

Validation is **not** run by you, the extractor — you have read the source and cannot judge
the artifacts blind. It is run by an **independent** party (the orchestrator spawns a fresh
agent that sees only the artifact text). Hand the artifacts off and apply the
`gating-by-blind-restoration` skill, under firewall:

- spec-only → can an implementable structure be recovered? (`pass` / `weak-pass` / `fail`)
- design-only → can a reproduction spec hypothesis be recovered?

A `fail` on either means that layer lost required structure (spec dropped a behavior-affecting
detail, or design omitted something unrecoverable). Revise and re-gate. A `weak-pass` on the
design layer is expected and acceptable — abstract docs intentionally drop reproduction detail.

If no isolated gate can be spawned, degrade explicitly: run the checklist's Self-Check section
against each layer and **record that validation was self-audit, not a blind gate** — do not
present it as gated.

## Common Failure Modes

- **Reproduction detail leaking into the design doc** (constants, tick counts, source names) —
  the two layers stop having distinct jobs.
- **Dropping ordering/edge behavior** that silently changes the dominant strategy.
- **Over-specifying cosmetics, under-specifying timing/collision.**
- Writing the design doc from the source instead of from the spec, which re-imports detail the
  spec was meant to filter.

## Output

Two artifacts — a reproduction spec and an abstract design doc — plus an extraction log, each
validated by the restoration gate.
