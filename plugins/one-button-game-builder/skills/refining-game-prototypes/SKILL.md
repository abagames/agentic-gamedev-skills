---
name: refining-game-prototypes
description: "Drives a first playable game build through a staged refinement loop — structure, difficulty and progression, presentation, cleanup — by answering a fixed set of measurable questions about what play actually consists of, choosing and applying one fix at a time without waiting for a reviewer, and keeping a revision log. Use when a game runs and passes its own tests but has only ever been judged by its author, when asked to polish, tune, or finish a prototype autonomously, or when a human reviewer keeps supplying the same kinds of observation (monotonous, too easy, a mechanic that changes nothing, an unfair death, an unreadable display). Not for inventing the concept, for a single reported bug, or for taste decisions such as art style or musical genre."
---

# Refining Game Prototypes

## Purpose

A first build that works is not yet the game it was meant to be. The distance is usually closed by
a reviewer who plays it and reports what is wrong, one observation at a time. Most of those
observations are confirmed by a measurement taken only after the reviewer asks. This skill asks
first: it turns the recurring observations into questions, answers them from telemetry and
captured frames, and acts on the answers.

It supplies the order, the questions, the decision rule, and the record. The measurement and repair
methods belong to companion skills, used when their own trigger conditions are met.

## When to Use

- A build is playable end to end and its author has run out of failing tests.
- The request is to finish, polish, or tune a prototype with little or no review in between.
- Review rounds keep producing observations the project could have measured itself.

## When Not to Use

- No playable loop exists, or the concept itself is in question: design it first.
- One specific defect was reported: fix it directly.
- The open question is taste. Record it for the reviewer; do not loop on it.

## Preconditions

Establish these before the first stage, and state any that cannot be met:

- **Intent statement.** One sentence for the intended moment-to-moment experience, and the name of
  the core interaction. Every stage compares measurements against it.
- **Run structure.** What a run is meant to be: a finite campaign, a timed attack, an endless
  score attack, a single puzzle. Success conditions come from this, not from a default.
- **Evidence the project already has.** Logs, telemetry, input replays, a scripted run, captured
  frames, simulated players, play reports. Use what exists. Do not build a simulator or a bot
  ladder because this skill mentions one; build one only when a question central to the intent
  statement cannot be answered any cheaper and the answer would change what gets built.
- **Scope.** Match the stages entered to the request. A request to polish presentation starts at
  stage 3 and takes stages 1 and 2 as given unless something observed contradicts them.
- **Build copies.** Keep a copy of the first playable build and of every build handed to a person.
  Play reports are evidence about the build that was played.
- **A revision log** in the project, started now. See
  [revision-log.md](references/revision-log.md).

## The Loop

Run the stages in order. Within a stage:

1. **Ask.** Answer the stage's questions in [stage-checks.md](references/stage-checks.md) that apply
   to this game's intent and run structure, cheapest evidence first: an existing log, a replay, one
   scripted run, a captured frame, a few minutes of observed play. Mark each `yes`, `no`, or
   `unknown`, with the evidence behind it and how strong that evidence is.
2. **Pick one finding.** Take the `no` with the largest effect on the intent statement. An
   `unknown` is not a finding by itself. Measure it only when it concerns the core interaction, a
   cheap measurement exists, and either answer would change the build; otherwise leave it
   `unknown`, record why, and carry it into the final report.
3. **Decide.** Write two or three candidate changes with expected effect and risk, choose with the
   decision rules below, and proceed. Do not stop to ask which one.
4. **Change one thing**, then re-measure with the same seeds, policies, and budgets.
5. **Keep or revert.** Keep the change only if the observed quantity moved the intended way and the
   guardrails the project can check still hold: simple play does not win, and failures remain ones
   a person would recognise. Otherwise revert. Re-check with the same evidence that raised the
   finding; a finding seen in one replay is re-checked with that replay.
6. **Log** the observation, cause, options, change, and before/after evidence, including reverted
   attempts.
7. Repeat until the stage's exit condition holds: every applicable question is `yes`, or is an
   accepted limitation or an `unknown` recorded with its reason.

A change in a later stage that reaches the rules reopens only the earlier questions it can affect.

## Stages

| Stage | Settles |
|---|---|
| 1. Structure | The core interaction is what play consists of; no unintended stall or bypass; every variation is perceptible |
| 2. Difficulty and progression | Difficulty evidence can be trusted; the run structure the intent names is in place; pressure scales with what is asked |
| 3. Presentation | The screen and sound report what the rules do |
| 4. Cleanup | Nothing fails for a reason the player cannot see |

Each stage exits as in step 7. Questions are conditional on the game: those about rounds, a
defined end, and one new element per round apply to finite, round-based runs only; an intended
endless score attack is checked for what it promises instead (pressure that keeps rising, or a
stated plateau).

Stage 1 comes first because presentation spent on a mechanic that is later removed is wasted, and
because a difficulty curve tuned on the wrong core has to be redone.

## Decision Rules

Use these to choose among candidates without a reviewer.

1. **Move play toward the core before adding anything.** Prefer changing where an action is
   possible, what a position costs, or what a round starts with over adding an enemy, a meter, or a
   mode.
2. **Remove what cannot be seen.** A variation whose effect is below what a player can perceive is
   removed, not tuned up, unless a one-rule change makes its effect unmistakable.
3. **Keep the reward the player already feels.** When closing an exploit, prefer raising the cost
   of the exploit over withdrawing a reward that ordinary play enjoys.
4. **One rule for both sides.** When the player and the opposition do the same kind of thing, give
   them the same rule; asymmetric exceptions are where loopholes live.
5. **Fairness before difficulty.** Fix failures the player could not have prevented before
   adjusting how hard the game is.
6. **Subtract from the screen.** For a display nobody can interpret: remove it, else tie it to a
   visible in-world event, else label it.
7. **Stop after three attempts** on one finding. Record it as unresolved with what was tried.

Ask a person only for an irreversible or outward-facing action, or for calibration input. A request
for calibration never blocks the loop.

## Calibration Input

The loop runs without a play report and labels its difficulty verdict uncalibrated. When a report
arrives — ideally the one-line run summary the game prints at the end of a run — fit it on the
build that was played, then revisit stage 2 only. A report is the only evidence that fixes the
*direction* of the simulated players' error.

## Companion Skills

Use each when its own trigger matches a finding. A stage naming a skill is not a reason to run it.

| Finding | Skill |
|---|---|
| Usage, stall, bypass, ladder, calibration | `evaluating-gameplay-balance` |
| A design claim that may not survive attack; an imperceptible variation | `stress-testing-game-concepts` |
| A promise that needs enforcing in code | `implementing-gameplay-invariants` |
| No end, no lives economy, no ceremony, no attract loop | `arcadifying-mini-games` |
| Goal, options, or risk not readable from the screen | `gating-intent-legibility` |
| Overlap, occlusion, faint or tiny indicators, unexplained HUD | `auditing-game-screen-readability` |
| Correct but lifeless response | `maximizing-game-feel` |
| Inaudible, clashing, or missing sound | `designing-retro-arcade-sound-kits`, `building-era-authentic-game-audio` |
| A family of siblings where one member may be missing | `auditing-gameplay-implementation-coverage` |
| A rare state that organic play reaches too slowly | `probing-web-game-mechanics` or the engine's equivalent |

When a companion skill is not installed, apply the question from `stage-checks.md` directly and say
so in the log.

## Validation

- Every question in the stages reached has an answer with evidence, a stated reason it does not
  apply to this game, or an `unknown` with the reason it was left unmeasured.
- Every kept change has before/after evidence of the same kind: the same seeds and policies when
  simulated, the same replay or scripted run otherwise.
- No `unknown` is reported as confirmed. Unknowns about the core interaction are listed first.
- Every reverted or rejected candidate is in the log; a later session must be able to see what was
  already tried.
- The final report separates what was measured, what was only inspected in frames, and what no one
  has played or heard.

## Output

The revised build, the revision log, and a short report: stages completed, findings fixed, findings
unresolved, calibration status, and the open questions that need a person.

## Failure Modes

- **Polishing first.** When the request covers the whole refinement, presentation work begun
  before stage 1 exits. This does not apply to a request scoped to presentation, which starts at
  stage 3 by design.
- **Proposing and waiting.** A list of options ending in a question, when the decision rules pick.
- **Metric without effect.** A variation kept because simulated players changed targets, though
  nothing on screen differs.
- **Tuning on a weak ladder.** Difficulty set from a strong policy shown to fail in ways a person
  would avoid.
- **Several changes at once.** The before/after comparison then attributes nothing.
- **Running every gate.** Entering an expensive check because a stage lists it or because evidence
  is merely absent, instead of because a question came back `no`.
- **Imposing a structure.** Adding rounds, an ending, or a lives economy to a game whose intent is
  an endless or single-screen experience, because the checks mention them.
- **Silent reverts.** A tried-and-removed feature left out of the log, then proposed again.
