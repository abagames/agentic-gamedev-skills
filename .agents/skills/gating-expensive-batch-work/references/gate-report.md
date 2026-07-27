# Gate Report Record Shape

Minimum machine-checkable shape for the per-item gate report (step 5) and the checkpoint decision (step 6).
Use YAML, JSON, or a table — the field set is what matters, not the syntax.

## Per-Item Record

One record per item in the batch, including items that stopped. Stopped items stay in the report under their
reason; dropping them destroys the finding the gate exists to produce.

```yaml
- item_id: <stable identifier from the fixed item list>
  gate: pass | stopped
  stop_reason: <null when pass; otherwise the specific requirement that failed>
  irreversible_touched: false
  evidence: <what the reversible pass actually produced for this item>
```

Field notes:

- `gate` has exactly two terminal values. There is no `partial`, no `deferred`, and no numeric score — a score
  invites converting a method-level stop into an item-level failure.
- `stop_reason` names a requirement, not a symptom. `"needs manual step the procedure does not define"` is a
  reason; `"did not work"` is not. Two items sharing a reason string is the signal the checkpoint most needs.
- `irreversible_touched` must be produced by the run itself — a counter, a log assertion, an access flag — not
  written by hand afterwards. When step 1's resource list was empty, assert instead that the expensive pass was
  never entered (`expensive_pass_entered: false`).
- `evidence` is what makes a stop auditable. A stop with no evidence is indistinguishable from a thin attempt.

## Checkpoint Decision Record

One record for the whole batch, written before the irreversible pass starts.

```yaml
decision: <the frozen method, stated so it can be executed without re-reading this file>
basis: <which gate records support it, by item_id>
re_freeze_scope:
  - change: <a candidate change to the method>
    redo: <the item_ids that would need their reversible pass redone if it is made>
items_entering_irreversible_pass: [<item_id>, ...]
```

`re_freeze_scope` lists candidate changes separately. A single blanket "any change restarts everything" hides
that a cheap change and a costly one have different scopes, and makes the cheap one look unaffordable.

## Self-Check

- Every item on the fixed list appears exactly once.
- No record has `gate: pass` together with a non-null `stop_reason`.
- `basis` cites only gate records — if it cites an irreversible-pass result, the checkpoint was taken too late.
- At least one item was run expecting a stop, and its record shows the same depth of work as the others.
