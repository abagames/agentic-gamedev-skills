# Stage Checks

Each row is a question, the evidence that answers it, and the observation a reviewer would make if
the answer were `no`. Skip rows the game cannot reach or its intent does not promise, and say why.
Thresholds are starting points; read every figure against the intent statement.

The evidence column names the strongest form. Weaker forms answer the same question at lower
confidence: an existing log, an input replay, a scripted run, a few minutes of observed play, or a
reading of the rules. Record which was used. A row left `unknown` because only an expensive
measurement could answer it is an acceptable outcome; state it in the report.

Rows marked *(rounds)* apply to finite, round-based runs. Rows marked *(goal)* apply when the game
has a goal beyond staying alive.

## Contents

- Stage 1: Structure
- Stage 2: Difficulty and progression
- Stage 3: Presentation
- Stage 4: Cleanup

## Stage 1: Structure

| Question | Evidence | What a reviewer would say |
|---|---|---|
| Does the core interaction supply most of the actions and most of the score? | Action share and score share per mechanic, per ladder rung | "The main mechanic hardly ever happens." |
| Is the whole play space used? | Share of time per named region | "I never go to that part of the screen." |
| Is every threat a real danger? | Fires and hits per threat per minute; any threat with hits near zero | "Nothing ever attacks me." "That gun never hits." |
| Is the primary threat present? | Longest stretch with no primary threat, outside designed lulls | "Sometimes the enemy just doesn't show up." |
| *(goal)* Is stalling an intended trade, or free? | Per-round and whole-run score of stalling against prompt play; whether the gain is capped, what waiting risks, and whether it stays best across skill levels. Stalling that scores more is a defect only when it is uncapped or costs nothing the player cares about | "Waiting until the last moment scores best." |
| *(goal)* Is the goal required? | A survive-only policy must not reach the success state | "You can finish without doing the thing." |
| *(goal)* Does a round end only when everything is resolved? | Goal units carried, in transit, or held by an opponent at the moment of clear | "It counted them as saved before I got home." |
| Can each variation be seen? | Effect size in pixels, seconds, or events per round against the baseline; a side-by-side frame pair | "That variant doesn't change how it plays." |
| Is each variation a change of mechanic, not a removal of pressure? | What the variant adds to the decision, stated in one line | "It's the normal stage with less going on." |
| Are failures preventable? | For each death, rewind a short interval and search every reachable input for an escape | "I died and could do nothing about it." |
| Does simple play lose? | Idle, hold, spam, nearest-target greedy against reading play, on at least two rungs | "Just shooting the nearest thing works." |

A variation that fails either variation row is removed under decision rule 2. A threat that fails
its row is strengthened so that it constrains the core action, with a warning the player can read
(see stage 3), not replaced by an additional threat.

## Stage 2: Difficulty and progression

| Question | Evidence | What a reviewer would say |
|---|---|---|
| Can the difficulty evidence be trusted? | Where simulated players exist: the strong policy's failures are not ones a person would plainly avoid, and results are not saturated for every rung. Close results alone prove nothing | "It's far too easy — are the bots just bad?" |
| Is there a rung below the human-limited policy? | A novice model, plus an ignore-the-threats baseline | "I fail far more often than your bot does." |
| Do controls that read hold time work with realistic presses? | Hold-duration probe at 100–150 ms | "I can't make it move just one step." |
| Does the allowance grow with what is asked? | Time or resource allowance per round against target count | "It gets faster just when there is more to do." |
| Does the run have the structure the intent names? | Finite: an end placed near where every element has appeared and density has capped. Endless: pressure that keeps rising, or a stated plateau. Timed: the clock, not attrition, ends most skilled runs | "Past a certain point nothing new happens." |
| *(rounds)* Is each round's novelty limited to one element? | Test over the round table | "Everything arrives at once on that wave." |
| *(rounds)* Does the weak rung lose gradually? | Clears per round per rung; no round where a quarter of runs end | "There's a wall at that wave." |
| Can the best outcome the game advertises be achieved? | At least one such run observed, by a policy or a person | "Is a perfect clear even possible?" |
| Do lives and extends suit each rung? | Recorded failure times replayed against candidate settings | "It ends too soon." "You never run out." |
| Do rates hold at double the seed count? | Re-run of the figure being used as a target | (None; this is the check on the other answers.) |

Calibration status goes in the report: `calibrated on <build>` or `uncalibrated`.

## Stage 3: Presentation

| Question | Evidence | What a reviewer would say |
|---|---|---|
| Is every transient element visible where it appears? | Frames at each popup, notice, and banner, including under HUD panels and at screen edges | "The score is hidden behind the radar." |
| Do coinciding notices stay readable? | Frames with two notices forced onto one frame | "That message overlaps the clear text." |
| Is every indicator brighter and larger than decoration? | Contrast and size of indicators against the busiest background | "The line is too faint to see." |
| Are the actors large enough to carry the action? | Actor and glyph size at the smallest supported scale | "Everything is small; it has no impact." |
| Can an outsider name every HUD element? | Isolated reader names what each counts and what changes it | "What is that number?" |
| Is each danger announced where it will land? | A warning with the same extent and timing as the hit, visible for its whole duration | "Show me where it is going to hit." |
| Does the strongest feedback go to the most important event? | Ordered list of events against effect intensity | "The big moment feels like the small ones." |
| Did the feel pass leave the rules alone? | Seeded simulated results identical before and after | (None visible; the symptom is a silent difficulty change.) |
| Is the mix audible, and is the commonest sound above the bed? | Peak level at the final output; most frequent SE against BGM | "I can barely hear it." |
| Do pitched effects fit the music where they are meant to? | Pitch set of SEs against the BGM's scale, with intended dissonance declared | "That sound is wrong against the music." |
| Does the title show what a player cannot guess? | Each rule that changes strategy appears on the title or in the first seconds of the demo | "I didn't know that enemy was worth eating." |
| Is every label needed? | For each text element: which decision depends on it | "That label isn't needed." |

## Stage 4: Cleanup

| Question | Evidence | What a reviewer would say |
|---|---|---|
| Are hazards and their effects gone at each boundary? | Live hazard and in-flight effect placed at the next spawn point at the moment of clear | "Something exploded the instant the wave began." |
| Is each hazard drawn as large as it hits, while it hits? | Drawn extent against active hit extent over the active window | "I was destroyed with nothing near me." |
| Does a new or revived opponent appear at a fair distance? | Distance and time to first contact at spawn, lowest decile | "It appeared right in front of me." |
| Is the moment after a respawn fair? | Failures within a few seconds of respawn; whether their cause predates the respawn | "I lost another life the moment I came back." |
| Do failure counters pause while the player is down? | Counter through a death sequence | "It kept counting while I was dead." |
| Do coinciding ceremonies all show, and does each counter change match an event? | Extend on the clear bonus; miss on the frame of a clear; lives display through a death sequence | "It didn't show the extend." "The ship count went up when I died." |
| Does a collectible just past a transition get collected? | Missed pickups during any slide, turn, or warp | "It leaves one behind after the lane change." |
| Does each end screen show a finished state? | Frames of every terminal screen | "The player is still blinking on the clear screen." |
| Is every sibling handled? | One coverage audit over surfaces changed in this loop | (Various; one member of a family behaves differently.) |
