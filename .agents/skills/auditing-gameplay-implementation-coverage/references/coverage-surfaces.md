# Coverage Surfaces

Use this catalog to select project-relevant axes. Do not audit rows unsupported by the game.

| Surface | Family census | Common omission | Useful relation |
|---|---|---|---|
| Phase/mode | declared phases, entry/exit paths | one phase lacks input, draw, reset, or audio handling | every reachable phase has required update and presentation paths |
| Input | actions, aliases, edges, locks | one alias or one screen is missing | declared aliases produce the same transition |
| Actor/effect | types, owners, states | new type omitted from cleanup, freeze, collision, or draw | every family member participates in required systems |
| Causality | source, owner, instigator | tag lost through a secondary effect | downstream consequence preserves allowed provenance |
| Lifecycle | spawn, arm, die, retry, round/scene change | stale or missing state across a boundary | boundary establishes the documented postcondition |
| Timing/order | same-tick events, deadlines, deferred work | branch runs once too early/late or after invalidation | boundary tick and adjacent tick satisfy distinct expectations |
| Presentation | HUD, marker, animation, warning | implemented rule is invisible before a decision | decision-changing state has a timely visible consumer |
| Audio/events | registry, emitters, silence, arbitration | one event undeclared, un-emitted, or unmeasured | registry and emit/silence sets reconcile |
| Scoring/economy | score producers, multipliers, costs, caps | one producer bypasses cause or cap | all producers satisfy the same economy invariant |
| Persistence | defaults, schema, write/read/migration | field written but not restored or ranked differently | save/restore or write/read round trip preserves required fields |
| Debug/testing | observable state, injectors, assertions | rule state inaccessible or only smoke-tested | each important rule has a distinguishing mechanical assertion |
| Content/config | IDs, tables, unlocks, assets | declared member absent from one lookup or consumer | referenced and consumed identifier sets reconcile |

## Pruning Rules

1. Remove impossible combinations using reachability evidence.
2. Collapse truly shared implementation paths, but keep separate data/config members.
3. Keep separately coded siblings separate even when names match.
4. Cover each pair of interacting axes before considering triples.
5. Add a triple only when the implementation condition reads all three axes or a documented bug
   requires them.
6. Prioritize omissions with silent outcomes over crashes; runtime gates already favor crashes.

## High-Yield Queries

Adapt these patterns to the repository rather than copying them literally:

```text
phase|mode|state
Arrow|Key[A-Z]|isPressed|isJustPressed|isJustReleased
type|kind|owner|source|src
emit|event|sound|silent
draw|render|hud|marker|warning
save|load|storage|serialize|restore|migrate
reset|clear|splice|remove|freeze|pause|resume
score|bonus|multiplier|cost|reward
debug|window\.|inject|setState|probe|assert|check\(
```

