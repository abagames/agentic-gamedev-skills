# Revision Log

Keep one log file in the project (for example `REVISION_HISTORY.md` beside the README) and append
to it as the loop runs. It is the memory of the loop: the next session reads it before proposing
anything.

## Opening section

Write once, before the first stage:

- the intent statement, the core interaction, and the intended run structure;
- the starting state of the build, as a short list of the rules that later entries change;
- where the copy of the first playable build is kept.

## One entry per finding

The fields matter; the wording is the project's own. Angle brackets mark what to fill in.

```markdown
### <short name of the finding>

- **Stage / question:** <stage number> — <the question from stage-checks.md>
- **Source:** <telemetry | replay | frame | observed play | play report on build <id>>
- **Observation:** <a number or a named frame, with the policy or run it came from>
- **Cause:** <the rule or presentation fact that produces it>
- **Options:** <two or three candidate changes, one line each>
- **Decision:** <the option taken, and the decision rule or reason>
- **Change:** <what changed in the rules or presentation>
- **Before → after:** <the same evidence, re-taken; same seeds or the same replay>
- **Status:** <kept | reverted | unresolved | left unknown, with the reason>
```

Rules for entries:

- State the observation as a number or a named frame, not as an impression.
- Record options that were not chosen; a later session should not re-derive them.
- A reverted change keeps its entry, with the evidence that caused the revert.
- When a play report is the source, quote it and name the build it refers to.
- When the finding was that the design intends what a question flagged, record that and close it.

## Closing sections

- **Not adopted:** a table of ideas tried and removed or proposed and declined, with one line each.
- **Validation notes:** what was measured, what was inspected only in frames, what no one has
  played or heard, what was left unknown and why, and the calibration status.
