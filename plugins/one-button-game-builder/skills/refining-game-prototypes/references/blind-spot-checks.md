# Blind-Spot Checks

A schedule of stage-check rows that run at fixed points whether or not a finding calls for them.
Every check named here is a row in [stage-checks.md](stage-checks.md), quoted by its question; this
file says only when each runs and at what cost. A check that comes back `no` is an ordinary finding
for the loop.

## Why these run unconditionally

The loop otherwise enters a check only when a question comes back `no`. The rows below are the ones
earlier projects skipped on exactly that ground, and a person then found the problem by playing:
an unreadable rule and unreadable words on the screen, a threat that never threatened, variants too
small to see, something from the previous run still running after game over, a mix that clipped
because sounds were measured one at a time. Missing them costs a person's play session. That is
negative evidence about these specific checks, not an absence of evidence, which is why they are an
exception to the rule against entering expensive checks.

## Cost tiers

- **Rule change or presentation change.** A change is a rule change when seeded simulated results
  differ. Where the project has no seeded simulated players, it is a rule change when it touches
  code or data the rules read; decide by reading the diff. Any other change is presentation, and
  only the presentation checks apply.
- **Light.** Answered by re-running probes that already exist — the project's simulated players,
  ablation switches, exploit policies — and reading their telemetry. Run after every rule change.
  Where no simulated players exist, answer from a scripted run and a reading of the rules at lower
  confidence, and say so. Do not build a simulator to make a check light.
- **Setup.** Work that makes a light check possible: a switch to disable each mechanic, an exploit
  policy for each source of score or progress. It is heavy. Do it once at loop entry, and again when
  a new mechanic or score source appears; afterwards the check is light.
- **Heavy.** Needs real input, sweeps, captures, a search or lookup, an outside reader, or audio
  rendering. Run at each of the host's handover points and once before the final report.

A handover point is a moment the build goes to a person to play or review. When the host names no
handover points, the only one is the final report.

## Coverage of each run

The first run of a check covers every element once. Later runs cover the elements the changes
since then can reach, judged from the diff, plus the one or two cases most likely to fail: the
busiest screen, the fastest actor, the element nearest a panel or an edge. Widen only within a
family that comes back `no`.

Cost decides only *when* a heavy check runs — now, or at the next handover point — never *whether*
it runs. Record every deferral with its reason. The absence of a finding is never a reason to defer.
Before the final report nothing remains deferred. A check this environment cannot perform (no
network, no way to run an independent reader, no audio rendering) is logged as not run, with the
reason, and listed in the report.

## At loop entry (heavy, once)

These belong before building; this loop starts from a playable build, so do them on it, and again
for any element added later.

- *(reference)* "Is what the design borrows from each named reference game what that game actually
  does?"
- "Do the events the intent promises happen often enough, and never stop for too long?" — at entry,
  list the events and fix how each is counted and the longest gap allowed.
- *(variants)* "Can each variation be seen?"
- Setup for "Does every mechanic earn its place?" and *(goal)* "Can any source of score or progress
  be repeated without advancing?"

## After every rule change (light)

- "Do the events the intent promises happen often enough, and never stop for too long?"
- "Does every mechanic earn its place?"
- *(goal)* "Can any source of score or progress be repeated without advancing?"
- *(variants)* "Can each variation be seen?" — the effect size, from telemetry.
- "Do constants derived from another quantity still fit it?"
- Any other stage 1 question the change can affect that the existing probes answer. Those needing a
  lookup, an input search, or captures (*(reference)*, preventability, the variant frame pair) wait
  for the next handover point.

## At each handover point and before the final report (heavy)

- "Does the game respond to real presses and touches as it does to simulated input?"
- "Does any result depend heavily on a value no play supports?"
- "Are collisions tested over the whole step?"
- *(end)* "Does each run start clean?"
- "Does every player-facing text match the current rules?"
- The stage 1 questions deferred from rule changes since the last handover point.

## In the presentation pass (heavy)

Run once when stage 3 is entered and again at each handover point after a presentation change.

- "Is each hazard drawn as large as it hits, while it hits?" (a stage 4 row)
- *(HUD)* "Is every transient element visible where it appears?" and "Do coinciding notices stay
  readable?"
- "Can an outsider name every screen element?" — the reader is an agent or person that has seen
  neither the design nor the source. Where the host cannot run one, log the check as not run.
- *(audio)* "Is the mix audible, and is the commonest sound above the bed?" and *(music)* "Do
  pitched effects fit the music where they are meant to?"

## What these checks cannot answer

None of them says whether the game is fun for a person, or how it feels and sounds. Ask the person
about those in the report, with specific questions tied to moments in a run.
