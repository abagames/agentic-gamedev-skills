# Scope: What the Verdict Licenses, and Why

Read this when a verdict is about to be carried into another decision — a redesign, a release call,
a claim that the game is readable — or when someone disputes what the gate proved. `SKILL.md` states
the limits as rules; this file gives the mechanisms behind them, which is what settles an argument.

## Why the instrument is one-sided

The gate measures the variety of **situations presented**, which is an upper bound on the variety of
decisions actually **exercised**. It can fail a game; it cannot pass one.

The bias has a specific mechanism: the sampler chose the situations, but in real play the *player's
own policy* determines which situations recur. A game can present eight genuinely different states
while a monotonous policy drives it into one basin and never sees seven of them. No sampling protocol
fixes this, because the sampler is not the player.

Hence the asymmetry in what the two variety outcomes are worth:

- `collapse` is decisive on its own. If situations deliberately spread across the state space still
  resolve to one action class, real play cannot be more varied than that. Revise the design.
- `spread` licenses nothing about long-run play. It says the situation space is not degenerate,
  which is a precondition for varied play and not evidence of it.

Confirming that varied situations are actually reached, and that varied decisions beat monotonous
ones, requires played-input instruments instead of frames: a telemetry comparison of monotonous
versus exploratory policies, and runtime idle-bot versus active-bot invariant checks.

**Ladder placement.** Run this gate *before* the balance sweep — it is cheaper and a `collapse` ends
the question early. Never run it *instead of* the sweep.

## Why a prototype verdict does not cover the shipped build

What the gate concludes divides by layer.

**Transfers across engines and builds** — goal legibility, presence of options, risk/reward
structure, and cross-scene divergence. These are properties of the rules and the screen composition,
not of the renderer that drew them. A prototype that establishes them establishes them for the
design.

**Does not transfer** — legibility at the shipping build's actual resolution, palette, scale, and
effect density. That is a visual-direction question about the real build. A prototype says nothing
about it, and nothing in the procedure could make it say anything: the frames were drawn by a
different renderer at a different size.

So a verdict earned on a disposable prototype licenses the design-layer conclusions only. Re-run on
the real build whenever the presentation layer materially changes. Recording the artifact type in
every verdict exists precisely so a later reader can tell which question was asked; a `prototype`
verdict quoted as evidence of shipped readability is the central misuse this gate creates.

## Why these four questions go to a human

The gate returns flags rather than scores on these, because an agent asked to score them will produce
a confident number with nothing behind it.

- **Motor feel and timing tolerance.** Whether the intent is *executable* at the speed the game
  demands is a property of hands, not of frames. A perfectly legible intent can be unreachable.
- **Novelty and surprise.** A grader carries a large prior over existing games. It may name the goal
  from genre convention rather than from this screen — inflating legibility for a conventional design
  — and it may find an unfamiliar-to-humans mechanic obvious, or a human-obvious one opaque. The
  direction of the error is not predictable, so it cannot be corrected for.
- **Colour-vision and small-screen accessibility.** The grader is one reader under one set of
  conditions, not a proxy population.
- **Whether the recovered goal is worth wanting.** Legible and boring passes this gate, correctly.
  Desirability is taste, and taste is outside what a blind firewall gate can measure.
