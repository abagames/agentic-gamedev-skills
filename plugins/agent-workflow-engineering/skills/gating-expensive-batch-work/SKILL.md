---
name: gating-expensive-batch-work
description: "Splits a batch of expensive per-item agent work into a cheap reversible pass over every item and an expensive irreversible pass, separated by a method-freeze checkpoint. Use when running one costly procedure over many items (evaluations, migrations, audits, labeling, benchmark or fixture construction) and the method — rubric, transform rules, criteria, instrument — could still turn out to be wrong, or when part of the work spends something that cannot be spent twice: fresh seeds, held-out data, one-shot quota, published output, or a reviewer's first impression. Not for single items, cheap items, or a method already validated on the same class of item."
---

# Gating Expensive Batch Work

## Purpose

Stop a batch from being run item-by-item end-to-end when the method might be wrong. Serial execution
guarantees the worst position: a defect found at item 3 forces a choice between finishing with a method known
to be broken and discarding the work already done. Neither is recoverable.

## When to Use

- The same expensive procedure runs over many items, and most of the cost is per-item agent work that cannot
  be scripted.
- The method could still be wrong, and the items are what would reveal it.
- Some step spends an irreversible resource.

## When Not to Use

- One or two items — there is nothing for the checkpoint to amortize over.
- Per-item work is cheap enough that redoing the whole batch is affordable.
- The method is already validated on this class of item; the batch is production, not discovery.
- Nothing irreversible is consumed and nothing expensive is per-item. Just run it.

## Required Inputs

- The item list, fixed before any item is processed.
- The per-item procedure, with its steps in order.
- The method or instrument that all items share.

## Procedure

**1. Name the irreversible resources.** List what the work spends that cannot be un-spent. Typical: fresh
random seeds and held-out data (observing them contaminates later use of the same draw), one-shot API or
compute quota, published or externally visible output, a human reviewer's first read, and any observation that
would condition a later decision. The list may legitimately come out empty: a batch whose only cost is
expensive per-item work still qualifies. Record it as empty rather than inventing an entry, and carry that
into step 2.

**2. Find the split point.** The reversible pass ends at the first step touching anything from step 1 — or,
when that list is empty, at the first step whose per-item cost is what makes redoing the batch expensive.
Everything before it can be redone freely.

**3. Build a mechanical stop, not a rule.** Add a flag, subcommand, or mode that runs the reversible pass and returns
before the first irreversible step. Written discipline is not enough: if the only way to reach the gate is to
run past it, the structure cannot be executed as designed and will not be.

**4. Run the reversible pass for every item.** Not a sample. The checkpoint sees exactly as many ways the method can
break as it has items.

**5. Emit a per-item gate report.** For each item, mechanically: can the irreversible pass produce a usable result,
and if not, which specific requirement failed. Include a field asserting no irreversible resource was touched.
Load `references/gate-report.md` for the minimum record shape; invent a format only if that one cannot carry
the batch's stop reasons.

**6. Take the method-freeze checkpoint once, with all reports in hand.** Record the decision, its basis, and
its **re-freeze scope** — which items must be redone if this decision is later reversed. Different candidate
changes usually have very different scopes; recording one blanket "anything changed here restarts everything"
hides that, and makes a cheap change look as expensive as the costly one.

**7. Adapt per item only before the checkpoint.** This is the one place adaptation is legitimate. Afterwards,
adapting to rescue a particular item conditions the result on the outcome.

**8. Run the irreversible pass** for items that passed the gate.

## Validation

- The gate report carries a machine-checkable assertion, per item, that no irreversible resource was consumed
  (`held_out_accessed: false` or equivalent). When step 1's list came out empty, the equivalent assertion is
  that the expensive pass was never entered. Prose promising it is not a check.
- Every item has a terminal state before the irreversible pass starts: passed, or stopped with a named reason.
- The checkpoint decision is written with its basis before the irreversible pass runs. If the basis cannot be
  stated without citing irreversible-pass results, the checkpoint has not been taken.
- Deliberately run the gate against an item you expect to fail. A gate that reports success on work that is
  actually invalid is worse than no gate, because the report then asserts a check that never happened.

## Common Failure Modes

- **Reading a gate stop as an item failure.** It is a result about the method. Half a batch stopping on one
  requirement is the most informative thing the gate can produce; converting those items to a low score
  destroys the finding.
- **Doing thin work on items expected to stop.** A stop reached through a weak attempt proves nothing. Hold
  every item to the same standard, especially the ones predicted to fail.
- **Sampling instead of covering.** Running the reversible pass on 2 of 7 items yields a checkpoint that has seen 2 of 7
  failure modes, at nearly the same checkpoint cost.
- **Skipping the mechanical stop** because you will be careful. You will run past it.
- **Repairing the method once a stop makes the repair convenient.** The test is whether the defect is arguable
  without referring to the item it rescues. Disclose the ordering either way: a repair made after seeing which
  item it saves is weaker evidence than the same repair made before.
- **Collapsing the checkpoint into the run.** If the decision is taken while the irreversible pass is already in
  flight, its re-freeze scope is unknowable and the freeze is not a freeze.

## Output

- A per-item gate report, one record per item, with the no-irreversible-access assertion.
- One written checkpoint decision carrying its basis and re-freeze scope.
- The irreversible pass executed only for items that passed the gate, with stopped items retained in the record
  under their reason rather than dropped from it.
