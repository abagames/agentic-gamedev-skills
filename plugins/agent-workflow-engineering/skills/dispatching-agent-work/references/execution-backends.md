# Execution Backends

Read this reference when selecting among multiple backends or adapting the skill to a new host.

## Capability discovery

Determine whether the host provides:

- durable user-visible tasks or threads;
- bounded child agents;
- later or recurring jobs;
- per-worker model and reasoning overrides;
- isolated workspaces or worktrees;
- status, wait, message, cancel, and approval routing;
- destination-specific model availability.

Use only capabilities that are actually exposed. Host policy overrides this reference.

When host policy blocks the required new boundary or model selection, report the capability limit. Do not reinterpret a discontinuous task as a continuation merely to use an available backend.

When persistent dispatch mode is active, capability discovery also selects the host-preferred worker boundary. Prefer durable tasks in Codex Desktop App, subagents on hosts without durable tasks, and the current agent only when no separate worker is exposed or the action is merely coordination or trivial.

## Backend semantics

| Backend | Ownership | Result path | Best fit |
| --- | --- | --- | --- |
| current agent | current conversation | direct response | Small cohesive work |
| durable task | user-visible independent lifecycle | user follows task directly | Long-running work, direct approvals, later follow-up |
| subagent | parent-owned bounded delegation | returns to parent | Independent research or implementation lane for synthesis |
| automation/job | scheduler-owned | notification or stored result | Future, recurring, or monitored work |

A child agent is not a fallback for a durable task when the user needs a visible history, direct steering, or approval prompts. A durable task is not a substitute for an internal subproblem when only the parent needs the result.

## Portable adapter contract

Map host-specific tools to these conceptual operations when available:

```text
capabilities() -> backends, models, efforts, isolation, coordination
dispatch(spec) -> handle
status(handle) -> running | needs-input | complete | failed
message(handle, delta) -> acknowledgement
wait(handle, cursor) -> progress or terminal result
cancel(handle) -> terminal status
```

Do not emulate a missing destructive or externally visible operation with shell commands or undocumented directives.

## Fallback order

1. Preserve user-requested persistence and visibility.
2. Preserve authorization and approval routing.
3. Preserve write isolation.
4. Preserve model role, using the closest available tier.
5. Preserve latency and cost preferences.

If the first three cannot be preserved, stop and request direction rather than silently changing execution semantics.

## Workspace rules

- Shared workspace plus read-only work: parallel is normally safe.
- Shared workspace plus writes: serialize when files or generated artifacts may overlap.
- Isolated workspace plus writes: parallelize only if later integration is defined and repository policy permits isolation.
- Non-repository project without isolation: queue writes; do not simulate a worktree.
- Dirty workspace: state which changes belong to the user or another worker and preserve them.

## Model-role resolution

Discover destination models at dispatch time. Map `efficient`, `balanced`, and `frontier` using the host's own descriptions, not remembered product names or prices. Keep the user's explicit model unchanged when available. If unavailable, report the limitation before substituting unless the user has authorized automatic fallback.
