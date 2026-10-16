# Play Input

What to do when a person has played a build and handed back what they saw. The loop never waits
for this; it uses it when it arrives.

## Inputs

Take whatever the session produced:

- **Replays**, when the game records them. Where it does not, the run summaries the game prints or
  logs at the end of a run.
- **Flagged moments**: points in a run the person marked, each with a category and a note.
- **Notes** per run and per session.
- **Proposals**: new content, rule ideas, other games offered as references.
- **Which session this was** for that person: a first play and a practised play are different
  evidence.
- **Who the person is**: the game's owner or designer, or another player.

## Procedure

1. **Find the build that was played** and work on its copy. Every observation below is about that
   build. A replay is read-only evidence about the rules it was played under: never regenerate,
   migrate, or re-record it after a rule change.
2. **Open each flagged moment.** From the replay, or the nearest evidence the session left, extract
   the state and the events in the seconds around it.
3. **Turn each note into a question** answered on the played build, whatever stage it belongs to.
   - It matches a row in [stage-checks.md](stage-checks.md): answer that row.
   - It matches no row and is not taste: write it as a new question in the project's own check
     list, not in this skill, and answer it the same way.
   - It is taste (style, genre, how something feels): keep it for the questions in step 6.

   An answer of `no` is an ordinary finding for the loop.
4. **Route each proposal to design**, as a separate entry from the findings. The decision rules
   choose among repairs for a finding; they do not admit or reject proposals. Weigh the proposal
   against the intent statement, then do one of:
   - adopt it as named content;
   - try it as one element at a time — one new element per round where the game has rounds,
     otherwise one change under step 4 of the loop — and keep or revert it by its evidence;
   - decline it with a reason.

   Record the outcome in the revision log. Never discard a proposal because it does not map to a
   stage check. When the proposer is the game's owner, do not decline on your own judgment: try it,
   or send the reason for declining back as one of the questions in step 6.
5. **Calibrate.** Fitting the simulated players to the person — comparing how they play with how
   the human-limited policy plays, placing them on the ladder, keeping a rung per person and
   session — belongs to the measurement procedure. Hand it the replays or summaries, the played
   build, and the session. When no such procedure is available, place the person on the existing
   ladder by the outcome of their runs on the played build and label the difficulty verdict as
   fitted on outcome only.
6. **Ask back.** Send taste items and unresolved points as three to five specific questions, each
   tied to a moment in one of the person's runs ("at 1:42 in your second run, when the boss
   appeared, ..."). Do not ask general questions such as "was it fun?".
7. **Revisit the stages the findings belong to**, in stage order. A finding in stage 1 reopens
   stage 1, and the rule change that answers it reopens what it can affect, as in the loop.

## Record

For each session, the log names: the person and the session, the build played, the replays or
summaries received, each flagged moment with the question it became, each proposal with its
outcome, the calibration result, and the questions sent back.
