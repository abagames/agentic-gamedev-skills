# Judging Protocol and Control Construction

Read this before briefing the first grader, when the question set or the prediction scoring is being
changed, or when building the degraded control. `SKILL.md` carries the stage split, the firewall, the
scoring constraint, and the control requirement; this file carries the wording to send, the rubric to
score with, and the degraded-control catalog.

## What each grader receives

Its own scene's lead-in frames, plus a **control legend**: what each input does physically. A player
standing at a cabinet knows there is a button and what pressing it does mechanically; withholding
that models nothing real and only measures whether the grader guesses the input scheme.

Nothing else. Not the design doc, README, source, repository path, spec, telemetry, mechanic names,
the game's title, any other scene, or the withheld follow-up frame.

## Stage A — verbatim questions

Send these four, in order, with the instruction that every answer must point at what in the frames
supports it:

1. **Goal** — "What is the player trying to make happen? What tells you?"
2. **Options** — "List every distinct thing the player could sensibly do from here."
3. **Risk** — "What would go wrong, and what does the screen show that warns of it?"
4. **Prediction** — "Ignoring what the player might choose, describe what these objects will be
   doing a moment from now: positions, contacts, what disappears, what the score does."

Then the counterfactual:

> "What would you actually press first, and why?"

The counterfactual is the highest-value single answer in the protocol. A grader that recites the
intended goal but would take a dominated action has not received the intent — the recovery question
alone cannot surface that divergence, because a grader can quote a goal it would not act on.

### Questions never to ask

Do not ask whether the game is fun, balanced, well paced, or varied over time. They are outside what
frames can support, and asking them reliably produces confident invention that then contaminates the
answers to the questions that *are* answerable. Question 4's "ignoring what the player might choose"
clause is load-bearing for the same reason: without it graders volunteer conditional predictions that
cannot be scored.

## Stage B — prediction rubric

Reveal `t+Δfwd`. The **evaluator** scores the stage-A prediction; the grader is not asked to grade
itself and is not shown the withheld key at any point.

- `matched` — the named objects are where the prediction put them, the named contacts happened, and
  nothing the prediction called out went the other way. Minor detail differences (exact pixel
  position, exact score increment) do not demote a match.
- `partial` — the gross motion was right but a called-out consequence did not resolve as stated, or
  the prediction was correct about some objects and silent or wrong about others that mattered.
- `contradicted` — an object the prediction placed went somewhere else, a predicted contact did not
  occur, or a predicted disappearance did not happen. The grader's model of the board was wrong.

### Scope constraints on scoring

- **Only the unconditional prediction (question 4) is scorable.** The revealed frame is the
  consequence of whatever the *recorded run's* input was, not of the action the judge said it would
  take. Scoring the judge's plan against it punishes correct reasoning about a branch that was
  never taken.
- Any prediction the grader volunteers that is conditioned on its own chosen action is **recorded,
  never scored**.
- What the prediction test measures is **situational readability** — whether the judge's model of
  what is on the screen is the real one. That is necessary for intent legibility, not identical to
  it: a judge can correctly predict a falling block without knowing what the game wants. So a
  `contradicted` prediction **invalidates that scene's goal answer** (the goal was read off a
  misunderstood board) and a `matched` or `partial` prediction **licenses the goal answer to be
  scored against the withheld key**. It gates the case; it is not the intent verdict.

## Assigning action classes

For the divergence metric, the evaluator assigns each scene's counterfactual first action to a class
from the withheld intended-class list. Add a class only when the grader named an action the design
did not anticipate, and flag such additions — an unanticipated action class is itself a design
finding, whether it indicates an unnoticed option or a misread board.

Do not let one grader's phrasing create a class. Two graders saying "dodge left" and "move away from
the red thing" are one class. Cluster on the action, not the words.

## Constructing the degraded control

The control is a variant of the same build whose intent is knowingly destroyed by deliberately
planted presentation-layer defects. Pick degradations that attack intent transmission without
touching the simulation:

- **Palette collapse** — assign every gameplay role the same or near-indistinguishable color, so
  role-by-color reading is unavailable.
- **Uniform sprites** — replace player, hazard, target, and pickup with one identical shape, so
  role-by-silhouette reading is unavailable.
- **Readout removal** — delete the persistent gauges and meters, so non-positional state is
  unreadable.
- **Reward concealment** — hide or move off-screen the object the player is meant to want, so the
  goal has no on-screen referent.

Capture the control under **identical protocol and framing**, interleaved with real scenes. The
grader must not be able to tell which build it is looking at, and must never be told that some
scenes are degraded — saying "this one might be fine" on a control run is telling it the answer.

### The control still predicts correctly, and that is the point

A degraded build usually permits perfectly correct *predictions*: the physics is unchanged, objects
still move where they were going to move. Only the intent reading collapses. This asymmetry is the
running demonstration that prediction score and intent legibility are different axes, and it is why
a `matched` prediction licenses the goal answer to be scored rather than constituting the pass.

If the control does not separate — if the grader names the intended goal as readily on the degraded
build as on the real one — the instrument has measured the grader's fluency, not the game. Report
`instrument-failure` and fix the protocol before reading any verdict: harsher degradation,
forced-choice answers instead of free prose, or more graders per scene.
