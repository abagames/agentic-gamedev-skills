# Simple-Policy Library

Select only policies that make sense for the concept. State what information each policy ignores.

## State-blind baselines

- **Idle**: no voluntary action.
- **Repeat-one-action**: always use the same action or direction.
- **Mash/random**: act at every opportunity without reading state.
- **Fixed interval**: act on a constant cadence.

## Greedy and safety baselines

- **Immediate reward**: choose the action with the largest visible short-term gain.
- **Immediate safety**: minimize current danger or loss regardless of future opportunity.
- **Always hoard**: never spend a resource unless forced.
- **Always spend**: convert a resource immediately whenever possible.
- **Fixed priority**: always target the same class, lane, entity, or objective first.

## What counts as dominance

Do not call a policy dominant from one favorable trace. Prefer one of:

- a reasoning invariant showing no state can reverse the preference;
- exhaustive search on a small discrete state space;
- simulation across varied initial states/seeds;
- repeated prototype telemetry showing the simple policy is no worse than state-reading policies on the target outcome.

If the evidence is only suggestive, classify `weak`.

## Expert-policy contrast

A credible skill claim should identify information that the expert uses and the simple policy ignores. Examples:

- future option count;
- delayed debt;
- opponent intent;
- queue order;
- hazard phase;
- spatial escape routes;
- opportunity cost of recovery;
- information gained by probing actions.
