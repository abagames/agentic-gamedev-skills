# Revision Log

Keep one log file in the project (for example `REVISION_HISTORY.md` beside the README) and append
to it as the loop runs. It is the memory of the loop: the next session reads it before proposing
anything.

## Opening section

Write once, before the first stage:

- the intent statement and the core interaction;
- the starting state of the build, as a short list of the rules that later entries change;
- where the copy of the first playable build is kept.

## One entry per finding

```markdown
### <short name of the finding>

- **Stage / question:** 1 — Is the whole play space used?
- **Source:** telemetry | frame | play report (build <id>)
- **Observation:** 66–74% of time in the surface band; under 5% below depth 100 (human-limited).
- **Cause:** every action is available only at the surface, and the surface carries no risk.
- **Options:** (a) rising projectile so depth sets range; (b) surface hazard; (c) faster sinking.
- **Decision:** a + b + c in that order; rule 1 (move play toward the core).
- **Change:** <what changed in the rules or presentation>
- **Before → after:** surface band 74% → 16%; below depth 100, 3% → 35% (same seeds).
- **Status:** kept | reverted | unresolved
```

Rules for entries:

- State the observation as a number or a named frame, not as an impression.
- Record options that were not chosen; a later session should not re-derive them.
- A reverted change keeps its entry, with the measurement that caused the revert.
- When a play report is the source, quote it and name the build it refers to.

## Closing sections

- **Not adopted:** a table of ideas tried and removed or proposed and declined, with one line each.
- **Validation notes:** what was measured, what was inspected only in frames, what no one has
  played or heard, and the calibration status.
