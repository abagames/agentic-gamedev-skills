---
name: auditing-game-screen-readability
description: "Audits what a running game's screen shows at the moments that matter, by capturing frames at gameplay events and at forced coincidences and checking them for overlapping or occluded text, indicators too faint, too small, or too brief to read, HUD elements whose meaning an isolated reader cannot name, and labels no decision depends on. Use when a game plays correctly but a display may be hidden, clipped, crowded, unexplained, or unnecessary, after adding HUD elements, notices, warnings, or score popups, or before release. Not for whether the goal, options, and risk can be read (use gating-intent-legibility), for choosing a visual direction (use directing-game-visuals), or for font selection and licensing (use styling-web-game-typography)."
---

# Auditing Game Screen Readability

## Purpose

Find display defects that tests of game state cannot see. A score popup is emitted with the right
value and drawn under a HUD panel. Two notices are each correct and land on the same line. A
warning line exists and is dimmer than the background dots. A counter is accurate and nobody can
say what it counts. Each passes every state assertion and fails the player.

These defects appear only at particular moments, so the audit is organised around moments, not
around screens.

## When to Use

- HUD elements, notices, warnings, indicators, or score popups were added or moved.
- A reviewer asked what a number or symbol means, or said something was hidden, faint, or small.
- Two events that each show a message can happen on the same frame.
- Before release, once, over the whole display.

## When Not to Use

- The question is whether a newcomer can tell what to aim for: `gating-intent-legibility`.
- No visual direction exists yet: `directing-game-visuals`.
- The build cannot be captured at chosen states. Report that, and fall back to reading the draw
  code for the checks in step 3 that need no pixels.

## Procedure

### 1. List the moments

Enumerate from the code, not from memory. Read [moments.md](references/moments.md) for the
catalogue. At minimum:

- every source of transient text: score popups, notices, banners, countdowns;
- every warning or prediction indicator, at its faintest and against the busiest background;
- every HUD counter at the instant it changes;
- the busiest effect stack the game can produce;
- every ceremony screen, including each terminal screen;
- **coincidences**: each pair of notices that can share a frame, forced to do so;
- **extremes**: each world-anchored element at every screen edge and under every HUD panel.

### 2. Capture

Arrange each moment by state injection or a scripted run, and capture at the game's native
resolution and at the smallest display scale it supports. For transient elements capture the first
frame, a middle frame, and the last. Record how each frame was produced so it can be re-captured.

### 3. Run the mechanical checks

Have the game report, per captured frame, the rectangle and draw order of every text draw,
indicator, and HUD panel — from the same data the renderer uses, never from a hand-kept list. Write them to a manifest
and run:

```bash
node <skill-dir>/scripts/check-screen-frames.mjs <manifest.json>
```

The manifest format and thresholds are in
[frame-manifest.md](references/frame-manifest.md). The script reports:

- `overlap` — two readable elements intersect;
- `occluded` — a readable element is drawn before an opaque panel that covers it. This needs a
  distinct draw order for both; when it is missing or tied, including for a panel's own children,
  the script lists the intersection as a `REVIEW` line to inspect in the frame instead of failing;
- `offscreen` — any part of a readable element is outside the viewport;
- `small` — glyph height at the smallest display scale is below the floor;
- `faint` — contrast between an element and what is behind it is below the floor;
- `brief` — a transient element is visible for less time than its length needs.

A passing run prints the manifest it read and the counts it checked. **If it prints nothing, it did
not run.** Run `--self-test` once per environment; it must report every defect class on its
built-in bad manifest.

When the project cannot emit rectangles, apply the same six checks by inspecting the frames, and
label the result `inspected`, not `checked`.

Two checks need pixels and are done on the frames themselves:

- **Stale elements.** Nothing from a previous run, phase, or mode is still drawn: an indicator left
  over in the attract demo, a notice surviving a restart, a blinking invulnerable player on an end
  screen.
- **Extent agreement.** A hazard's drawn extent is at least its active hit extent for the whole
  time it can hit, and a warning covers the area the hit will cover.

### 4. Ask an isolated reader what the HUD means

Give an agent that has seen neither the design nor the source two or three ordinary play frames
with each HUD element numbered. For each, ask: what does it count, what makes it change, and is
more of it good or bad? Compare with the design.

An element the reader cannot name is a finding even if its value is correct. If no isolated reader
can be spawned, answer the questions yourself and label the result `self-audit`; it is weaker
evidence, because you already know the answers.

### 5. Ask whether each element is needed

For every label, number, and symbol, name the decision that depends on it. If there is none, it is
a candidate for removal: a mode name that never changes, a marker repeating what an animation
already shows, a count the player cannot act on.

### 6. Repair in this order

1. **Remove** the element.
2. **Move** it to where the player is looking, or out from under what covers it. World-anchored
   text that drifts toward a HUD panel should drift the other way.
3. **Strengthen** it: size, contrast, duration, or motion that follows the direction of play.
4. **Connect** it to its cause: an animation from the in-world event to the counter it changes
   explains a counter better than a caption does.
5. **Label** it, last.

Give coinciding notices separate lines, and fold a rapid series of popups into one running total.

### 7. Re-capture

Re-run steps 2 and 3 on the changed moments only, and repeat step 4 only for elements whose
meaning was the finding.

## Validation

- Every moment listed in step 1 has a frame, or a stated reason it cannot occur.
- Each coincidence was produced on purpose; none is assumed not to happen.
- The script's self-test passed in this environment, and the real run printed its counts.
- Every `REVIEW` line was resolved by looking at the frame; none is reported as a pass unseen.
- Each finding names the element, the frame, and the check that failed. A finding that names no
  element is not a finding.
- Findings from an isolated reader are marked as such, separately from `self-audit` results.

## Output

A table of findings (element, moment, check, repair, status), the manifest or frames behind it, and
a list of moments that could not be captured.

## Limits

This audit says an element can be seen and named. It does not say the game is understood, that the
layout is attractive, or that the display reads well on hardware the capture did not use. Colour
vision deficiency and very small physical screens need a person or a dedicated simulation.
