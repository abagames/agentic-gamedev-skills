# Stage Checks

Each row is a question, the evidence that answers it, and the kind of remark a reviewer makes when
the answer is `no`. Skip rows the game cannot reach or its intent does not promise, and say why.
Thresholds are starting points; read every figure against the intent statement.

The evidence column names the strongest form. Weaker forms answer the same question at lower
confidence: an existing log, an input replay, a scripted run, a few minutes of observed play, or a
reading of the rules. Record which was used. A row left `unknown` because only an expensive
measurement could answer it is an acceptable outcome; state it in the report.

A row applies only when its condition holds. The conditions are independent of one another:

- *(goal)* the game has a goal beyond staying alive;
- *(rounds)* play is divided by round, wave, or phase boundaries, whether the run is finite or endless;
- *(respawn)* the player can be taken out of play and return: a respawn, a stun, a recall, any stretch without control;
- *(lives)* failures are counted against a lives or extend economy;
- *(variants)* the game has variations of its base rules;
- *(HUD)* the screen carries counters or notices;
- *(audio)* the game has sound; *(music)* it also has music.

Whether a run is finite is a separate matter, covered by the run-structure row in stage 2. An
endless wave game has *(rounds)* without an end; a game with unlimited respawns has *(respawn)*
without *(lives)*.

A `no` is a finding to weigh against the intent, not an instruction to add something. Where the
design chose the flagged property on purpose, record that and move on. The remarks are symptoms
heard in other projects, phrased generally; they are not features this game should have.

## Contents

- Stage 1: Structure
- Stage 2: Difficulty and progression
- Stage 3: Presentation
- Stage 4: Cleanup

## Stage 1: Structure

| Question | Evidence | A reviewer would say |
|---|---|---|
| Does the core interaction supply most of the score, and a fair share of the actions? | Action share and score share per mechanic, per ladder rung | "The main mechanic hardly ever happens." |
| Is the play space the design intends actually used? | Share of time per named region | "I never go to that part of the screen." |
| Is every threat a real danger? | Fires and hits per threat per minute; any threat with hits near zero | "Nothing ever attacks me." |
| Is the primary threat present when the design says it should be? | Longest stretch with no primary threat, outside designed lulls | "Sometimes the opposition just isn't there." |
| *(goal)* Is stalling an intended trade, or free? | Per-round and whole-run score of stalling against prompt play; whether the gain is capped, what waiting risks, and whether it stays best across skill levels. Stalling that scores more is a defect only when it is uncapped or costs nothing the player cares about | "Waiting until the last moment scores best." |
| *(goal)* Is the goal required? | A survive-only policy must not reach the success state | "You can finish without doing the thing." |
| *(goal)* Does a round end only when everything is resolved? | Goal units still in transit or held by either side at the moment of clear | "It counted that before it was settled." |
| *(variants)* Can each variation be seen? | Effect size in pixels, seconds, or events per round against the baseline; a side-by-side frame pair | "That variant doesn't change how it plays." |
| *(variants)* Is each variation a change of mechanic, not a removal of pressure? | What the variant adds to the decision, stated in one line | "It's the normal game with less going on." |
| Are failures preventable? | For each failure, rewind a short interval and search every reachable input for an escape | "I failed and could do nothing about it." |
| Does simple play lose? | Idle, hold, spam, and nearest-target greed against reading play, on at least two rungs | "Just doing the obvious thing works." |

A variation that fails a *(variants)* row is handled by decision rule 2. A threat that fails its
row is first examined for whether it should exist at all; if it should, make it constrain the core
action with a warning the player can read. Do not answer it by adding another threat.

## Stage 2: Difficulty and progression

| Question | Evidence | A reviewer would say |
|---|---|---|
| Can the difficulty evidence be trusted? | Where simulated players exist: the strong policy's failures are not ones a person would plainly avoid, and results are not saturated for every rung. Close results alone prove nothing | "It's far too easy — are the bots just bad?" |
| Is there a modelled player near the reporter's level? | A rung at or below a reported result, when a play report exists | "I fail far more often than your bot does." |
| Do controls that read hold time work with realistic presses? | Hold-duration probe at 100–150 ms, where a control depends on hold time | "I can't make it move just one step." |
| Does the allowance grow with what is asked? | Time or resource allowance against the amount demanded, where both vary | "It gets faster just when there is more to do." |
| Does the run have the structure the intent names? | Finite: an end placed near where every element has appeared and density has capped. Endless: pressure that keeps rising, or a stated plateau. Timed: the clock, not attrition, ends most skilled runs | "Past a certain point nothing new happens." |
| *(rounds)* Is each round's novelty limited to one element? | Test over the round table | "Everything arrives at once." |
| *(rounds)* Does the weak rung lose gradually? | Clears per round per rung; no round where a quarter of runs end | "There's a wall at that point." |
| Can the best outcome the game advertises be achieved? | At least one such run observed, by a policy or a person | "Is a perfect result even possible?" |
| *(lives)* Do lives and extends suit each rung? | Recorded failure times replayed against candidate settings | "It ends too soon." "You never run out." |
| Do rates hold at double the seed count? | Re-run of the figure being used as a target | (None; this is the check on the other answers.) |

Calibration status goes in the report: `calibrated on <build>` or `uncalibrated`.

## Stage 3: Presentation

| Question | Evidence | A reviewer would say |
|---|---|---|
| *(HUD)* Is every transient element visible where it appears? | Frames at each popup, notice, and banner, including under panels and at screen edges | "That number is hidden behind the panel." |
| *(HUD)* Do coinciding notices stay readable? | Frames with two notices forced onto one frame | "That message overlaps the other one." |
| Is every indicator the game has brighter and larger than decoration? | Contrast and size of existing indicators against the busiest background | "It's too faint to see." |
| Are the actors large enough to carry the action? | Actor and glyph size at the smallest supported scale | "Everything is small; it has no impact." |
| *(HUD)* Can an outsider name every HUD element? | Isolated reader names what each counts and what changes it | "What is that number?" |
| Where a danger cannot be dodged on sight, is it announced where it will land? | For dangers with no readable approach: a warning with the same extent and timing as the hit | "I couldn't tell where it would hit." |
| Does the strongest feedback go to the most important event? | Ordered list of events against effect intensity | "The big moment feels like the small ones." |
| Did the feel pass leave the rules alone? | Seeded simulated results identical before and after, where they exist | (None visible; the symptom is a silent difficulty change.) |
| *(audio)* Is the mix audible, and is the commonest sound above the bed? | Peak level at the final output; most frequent SE against the bed it plays over | "I can barely hear it." |
| *(music)* Do pitched effects fit the music where they are meant to? | Pitch set of SEs against the music's scale, with intended dissonance declared | "That sound is wrong against the music." |
| Is a rule that changes strategy discoverable before it matters? | The rule is readable from play, from the first seconds of a demo, or from the title; whichever the game already has | "I didn't know that was worth doing." |
| *(HUD)* Does a decision depend on each label? | For each text element: which decision uses it | "That label isn't needed." |

## Stage 4: Cleanup

| Question | Evidence | A reviewer would say |
|---|---|---|
| *(rounds)* Are hazards and their effects gone at each boundary? | Live hazard and in-flight effect placed at the next start point at the moment of clear | "Something hit me the instant the next round began." |
| Is each hazard drawn as large as it hits, while it hits? | Drawn extent against active hit extent over the active window | "I was hit with nothing near me." |
| Does a new or revived opponent appear at a fair distance? | Distance and time to first contact at spawn, lowest decile | "It appeared right in front of me." |
| *(respawn)* Is the moment after the player returns fair? | Failures within a few seconds of returning; whether their cause predates the return | "I was hit again the moment I came back." |
| *(respawn)* Do accumulating failure counters pause while the player is out of play? | Counter through the whole time without control | "It kept counting while I was out." |
| *(HUD)* Do coinciding ceremonies all show, and does each counter change match an event? | Two ceremonies forced onto one frame; each counter watched through a failure sequence | "It didn't show the bonus." "The count changed for no reason." |
| Does a collectible just past a transition get collected? | Missed pickups during any slide, turn, or warp the game has | "It leaves one behind after the move." |
| Does each end screen show a finished state? | Frames of every terminal screen | "It still looks like play is going on." |
| Is every sibling handled? | One coverage audit over surfaces changed in this loop | (Various; one member of a family behaves differently.) |
