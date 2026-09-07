# Failure Taxonomy

## Reachability and termination

- success/progress state cannot be reached;
- required resources cannot be produced, moved, or consumed as claimed;
- failure is unavoidable before meaningful agency exists;
- state transitions can leave the playable region permanently without a designed terminal condition;
- loops can continue indefinitely while bypassing the intended challenge.

## Dominant simple policy

A policy is dangerous when it succeeds while ignoring state the design claims should matter. A simple policy is not a defect merely because it is viable.

Look for dominance by:

- idle or safe waiting;
- repeat-one-action;
- random/mashing;
- always choose immediate safety;
- always choose largest immediate reward;
- always hoard / always spend;
- fixed target priority;
- fixed timing interval.

## Agency collapse

- best action does not change across reachable states;
- different actions produce equivalent future option sets;
- automatic dynamics overwhelm player influence;
- the player can read state but has no action that meaningfully responds to it;
- decisions exist only because numeric tuning is unspecified;
- a nominal choice merely changes animation, theme, or bookkeeping.

## Reward and resource exploits

- score can be farmed without creating new risk or opportunity;
- one opportunity can be scored repeatedly without a meaningful reset;
- survival or waiting yields uncapped value in a safe state;
- a resource can be produced faster than any intended sink can matter;
- reward and failure systems are causally independent despite a claimed risk/reward loop.

## Rule irrelevance and feature camouflage

- a state variable never changes preferred action;
- a mechanic activates but changes neither progress, risk, information, nor future options;
- a resource has no opportunity cost;
- an exception rule exists mainly to patch another rule's failure;
- upgrades, content, or meta progression add variety without changing the core decision.

## Unsupported appeal

Mark `unknown` or `weak`, not automatically `fails`, when the concept's claimed value depends mainly on:

- audiovisual feel or embodied timing;
- authored content quantity or surprise;
- narrative meaning;
- social dynamics not represented in the model;
- a narrow balance threshold whose viable range is unknown;
- long-horizon mastery not observable from the current rules.
