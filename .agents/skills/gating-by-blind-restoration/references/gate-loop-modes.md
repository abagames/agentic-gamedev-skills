# Gate Loop Modes

Load this when integrating blind-restoration gates into a multi-stage generation or
extraction pipeline. For a single standalone check you do not need it.

## The Asymmetry

Upstream (creative generation) and downstream (fidelity) gates use **opposite** loop
philosophies. Confusing them is a common and costly mistake.

### Upstream creative generation → one-shot filter

- The gate has **no feedback loop**. On `fail`, **discard the artifact and regenerate from a
  new seed/prompt**. Never feed the gate's findings back into the generator.
- Why: feeding findings back makes the generator converge toward whatever the gate rewards,
  collapsing diversity and inviting self-justification ("I'll just patch the one thing the
  grader flagged"). A fresh generation preserves variety.
- Stop at the **first** passing artifact. Do not generate many and compare side by side —
  comparison also drives convergence toward known-good patterns.
- Cap attempts (e.g. 5). If nothing passes, stop and classify the cause.

### Downstream fidelity layers → find→fix→re-check loop

- On `fail` / `weak-pass`, **repair the artifact in place** and re-run the gate.
- On re-runs, pass the prior findings as `CLOSED` / `STILL-OPEN`, but the gate makes every new
  judgment from scratch (a closed finding is re-verified, not trusted).
- Cap rounds (e.g. 3). If the same blocker/major is still open at the cap, **abandon** the
  candidate rather than forcing it through.

## Independence Holds in Both Modes

Every gate, upstream or downstream, runs as an independent sub-agent under the input firewall.
Never collapse a gate into an inline self-review by the author of the artifact.

## Abandonment Classification

When a candidate hits the round cap with an open blocker, do not silently drop it — classify
why, so the failure is reusable signal:

- `source-unviable` — the upstream artifact/idea itself cannot support a valid next layer.
- `layer-unresolved` — the layer under repair never reached a passing state within the cap.
- `harness-unrunnable` — the gate itself could not be executed (tooling/firewall broke).

Pick names that fit the domain; the point is that an abandonment carries a recorded cause.

## Jurisdiction Between Stacked Gates

When several layers each have a gate (e.g. spec gate, then implementation gate), keep their
jurisdictions separate: a downstream gate judges only its own layer against the upstream layer
taken as ground truth. If a downstream gate discovers that the **upstream** artifact is at
fault, it does not patch around it — it sends the work back to the upstream gate.
