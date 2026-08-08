---
name: dispatching-agent-work
description: "Routes a user's request to the appropriate execution boundary, model role, reasoning effort, and workspace isolation. Use only when the current user request or an authoritative host or repository instruction explicitly asks for dispatch, delegation, separate-task execution, scheduling, or execution-backend selection. Do not invoke merely because ordinary work is complex, long-running, or parallelizable, or when this skill is only being mentioned, reviewed, or edited."
---

# Dispatching Agent Work

Route work without coupling the decision to one vendor's model names or agent APIs. Prefer the smallest execution unit and lowest sufficient model role that can meet the success criteria reliably.

## Workflow

### 0. Confirm activation and duration

Proceed only when the current request or an authoritative host or repository instruction explicitly asks for dispatch or execution-boundary selection. Mentioning, reviewing, or editing this skill does not activate dispatch. Complexity, duration, cost, or possible parallelism alone does not activate it. Without activation, continue with the current agent under normal host policy.

Treat activation as scoped to the current request by default. Keep coordinating workers created for that request, including in-scope follow-ups, until their results are returned or the request ends. Require fresh activation for a new objective or later request. Continue dispatching across requests only when the user or authoritative instruction explicitly establishes a persistent orchestration role; honor an instruction to leave that role.

Activation permits routing analysis but does not override host policy or broaden authority. Before considering a boundary, remove any backend that the host forbids or that requires authorization not present in the current request.

### 1. Capture the dispatch contract

Extract only:

- objective and success evidence;
- answer, diagnose, change, monitor, or schedule intent;
- files, systems, and people in scope;
- approval and destructive-action boundaries;
- persistence, follow-up, deadline, and isolation needs;
- any explicitly requested model, backend, or skill.

Do not broaden authority while delegating. Preserve an explicitly requested model or execution boundary when the host supports it.

### 2. Discover host capabilities

Inspect available tools and policies instead of assuming that the host supports tasks, subagents, worktrees, model overrides, waits, or approval forwarding. Read [execution-backends.md](references/execution-backends.md) when more than one backend is available or a fallback is required.

When the destination is the Codex app and a separate user-visible task may match, read [codex-app.md](references/codex-app.md) before dispatching.

### 3. Choose the execution boundary

Use the first matching boundary:

1. **Existing worker** — the new instruction has the same objective, artifact surface, authority, lifecycle, and suitable model role, and the user did not request a new boundary. Send a concise delta, not the original prompt again.
2. **Automation or queued job** — work must run later or recur.
3. **Durable task** — the user requested a separate user-visible task, needs direct follow-up or approvals, or the work has an independent lifecycle.
4. **Current agent** — one small cohesive action with no suitable existing worker or separate lifecycle.
5. **Subagent** — a bounded independent subproblem whose result should return to the parent for synthesis.

Do not treat a subagent as equivalent to a user-visible task. Do not append a trivial follow-up to an expensive worker solely because it is already open; account for both separation cost and capability mismatch.

When a durable task is the first match, keep it as the intended boundary even if creation is unavailable. Report the limitation or prepare a user-mediated handoff according to the host adapter; do not silently demote it to a current-agent goal or subagent.

### 4. Select a model role and reasoning effort

Resolve these semantic roles to models actually available on the destination host:

| Role | Starting effort | Use for |
| --- | --- | --- |
| efficient | low | Narrow, well-specified work with a strong oracle and cheap validation |
| balanced | medium | Multi-condition audits, data analysis, or moderate cross-file synthesis |
| frontier | high | Ambiguous, cross-cutting, long-horizon, architectural, creative, or weak-oracle work |

Raise the role or effort for high consequence, broad coupling, unclear specifications, large evidence sets, or judgment that tools cannot verify. Lower it when deterministic tools, focused tests, or a precise specification carry most of the work. Reserve maximum effort for demonstrated quality gains on genuinely hard work.

Never infer quality needs from line count alone. Verify current model availability before naming a concrete model; otherwise report only the semantic role.

### 5. Enforce concurrency safety

Inspect active work when the host exposes it.

- Run read-only tasks in parallel when their observations will remain valid.
- Serialize writes to the same workspace or overlapping artifact surface.
- Use isolated workspaces for independent writes only when the host and repository policy support them.
- If isolation is unavailable, queue the work or merge it into a suitable existing worker.
- Avoid launching a read-only audit against files that another worker is actively rewriting unless the audit explicitly accepts a point-in-time snapshot.

### 6. Build a lean handoff

Pass:

```text
Objective:
Scope and preserved state:
Required skills:
Success evidence:
Authority and prohibited actions:
Final report fields:
```

Reference applicable skills by name; do not copy their full procedures. Include repository policy and uncommitted-change ownership only when relevant. State whether the worker should implement or only diagnose.

### 7. Dispatch and coordinate

- Treat a durable task as created only when a host-native operation confirms creation and returns its task or chat handle or link. A prepared composer or deep link is not a successful dispatch.
- Wait or monitor only when the parent must synthesize the result.
- Route follow-up instructions to the responsible worker when they remain in scope.
- Start a separate worker when the objective, artifact surface, authority, lifecycle, or appropriate model role changes materially.
- Do not duplicate work already in progress.

## Output

Report the decision concisely:

```text
backend: current | existing | durable-task | subagent | automation
model-role: efficient | balanced | frontier
reasoning: low | medium | high | host-default
isolation: shared-read | serialized-write | isolated-write
reason: one sentence
```

For `durable-task`, also report:

```text
dispatch-status: created | prepared | unavailable
```

Use `created` only after host-native creation succeeds, `prepared` when user action is still required, and `unavailable` when neither creation nor a faithful user-mediated handoff is possible. Do not expose internal routing analysis unless the user asks.
