---
name: dispatching-agent-work
description: "Routes a user's request to a separate task, subagent, automation, or current agent with an appropriate model role, reasoning effort, and workspace isolation. Use when the user or an authoritative instruction asks to dispatch, delegate, orchestrate, enter dispatch mode, run work in another session, select an execution backend, or schedule work. While dispatch mode is active, proactively send substantive execution to the host's preferred worker boundary: a new user-visible task in Codex Desktop App and a subagent on hosts without durable tasks. Do not invoke merely because ordinary work is complex, long-running, or parallelizable, or when this skill is only being mentioned, reviewed, or edited."
---

# Dispatching Agent Work

Route work without coupling the decision to one vendor's model names or agent APIs. When dispatch mode is active, keep the current conversation as the coordinator and prefer a separate worker for substantive execution. Otherwise prefer the smallest execution unit and lowest sufficient model role that can meet the success criteria reliably.

## Workflow

### 0. Confirm activation and duration

Proceed only when the current request or an authoritative host or repository instruction explicitly asks for dispatch or execution-boundary selection, or when a previously and explicitly established dispatch mode remains active in the conversation. Mentioning, reviewing, or editing this skill does not activate dispatch. Complexity, duration, cost, or possible parallelism alone does not activate it. When the current request provides no activation and no established dispatch mode is active, continue with the current agent under normal host policy.

Distinguish one-request activation from **dispatch mode**. A request to dispatch or delegate one objective applies only to that objective. A request such as "enter dispatch mode," "act as an orchestrator," or an authoritative instruction establishing that role activates dispatch mode for later objectives in the same conversation. Keep that mode active until the user asks to leave it or an authoritative instruction changes the role. Do not mistake a request to inspect, review, or edit this skill for activation.

In dispatch mode, treat the current agent primarily as a coordinator. Proactively dispatch every substantive objective that has a self-contained handoff and success criterion; the user does not need to repeat "dispatch" on each turn. Keep only clarification, routing, coordination, synthesis, and genuinely trivial one-step actions in the current conversation. Do not create an empty worker merely to await an objective: collect enough task content for a lean handoff first.

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

Classify the instruction before selecting a boundary. Reuse a worker only when the instruction is affirmatively a continuation of that worker's objective and has the same artifact surface, authority, lifecycle, required model role, and required reasoning effort. Assess the required model role and effort fresh for the instruction before comparing them with the worker. If any dimension differs, is unknown, or has not been checked, treat the instruction as a new objective. A shared project, repository, conversation, chronology, or available worker is not continuity.

When dispatch mode is active, first select the host-preferred worker boundary:

- **Codex Desktop App:** create a new durable user-visible task for each new substantive objective. Prefer the current project and an isolated worktree for repository writes when host policy supports it. Use a new task even when the parent will later synthesize the result; task visibility is the mode's default, not a special case requiring the user to ask again.
- **Other hosts with subagents but no durable tasks:** create a subagent for each bounded substantive objective and return or synthesize its result in the parent.
- **Hosts with neither:** perform the work in the current agent and report the capability limit.
- **Scheduled or recurring work:** use an automation or queued job instead of either default.

Outside dispatch mode, or after classifying a continuation or exception within it, use the first matching boundary:

1. **Existing worker** — the continuation gate above passes and the user did not request a new boundary. Send a concise delta, not the original prompt again.
2. **Automation or queued job** — work must run later or recur.
3. **Durable task** — the user requested a separate user-visible task, needs direct follow-up or approvals, or the work has an independent lifecycle.
4. **Subagent** — a bounded independent subproblem whose result should return to the parent for synthesis.
5. **Current agent** — clarification, routing, synthesis, or one trivial action for which creating a worker would provide no useful separation. Outside dispatch mode, it may also handle one small cohesive action when its model role and effort meet the requirement. When either falls short and an override is available, dispatch instead.

Do not treat a subagent as equivalent to a user-visible task. Do not append a trivial follow-up to an expensive worker solely because it is already open; account for both separation cost and capability mismatch.

When a durable task is the first match, keep it as the intended boundary even if creation is unavailable. Report the limitation or prepare a user-mediated handoff according to the host adapter; do not silently demote it to a current-agent goal or subagent.

### 4. Select a model role and reasoning effort

Resolve these semantic roles to models actually available on the destination host:

| Role | Starting effort | Use for |
| --- | --- | --- |
| efficient | low | Narrow, well-specified work with a strong oracle and cheap validation |
| balanced | medium | Multi-condition audits, data analysis, or moderate cross-file synthesis |
| frontier | high | Ambiguous, cross-cutting, long-horizon, architectural, creative, or weak-oracle work |

Role and effort are independent axes; the starting-effort column is a default, not a binding. A frontier-role model running at low effort satisfies the frontier role but not a high-effort requirement.

Raise the role or effort for high consequence, broad coupling, unclear specifications, large evidence sets, or judgment that tools cannot verify. Lower it when deterministic tools, focused tests, or a precise specification carry most of the work. Reserve maximum effort for demonstrated quality gains on genuinely hard work.

Apply this to the orchestrator itself: when the required role or effort exceeds the current agent's own, dispatch instead of working locally. The orchestrator's own effort is normally fixed for the session, so raising effort means dispatching a worker. Trigger on conditions that are cheap to evaluate — scope breadth, a missing test, specification, or deterministic checker, unresolved ambiguity in the request — not on a sense of difficulty, and not on an analysis that itself needs the higher effort. If no higher tier or effort override is available, proceed and report the capability limit.

Never infer quality needs from line count alone. Verify current model availability before naming a concrete model; otherwise report only the semantic role.

### 5. Enforce concurrency safety

Inspect active work when the host exposes it.

- Run read-only tasks in parallel when their observations will remain valid.
- Serialize writes to the same workspace or overlapping artifact surface.
- Use isolated workspaces for independent writes only when the host and repository policy support them.
- If isolation is unavailable, queue separate work; merge it into an existing worker only when the continuation gate passes.
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

- Dispatch promptly once the handoff has an objective and success evidence. Do not ask the user to choose a backend that host policy and this workflow already determine.
- In Codex Desktop App dispatch mode, use the host-native task-creation operation rather than an internal subagent. On other hosts, use the exposed subagent operation unless the task requires a different boundary.
- Treat a durable task as created only when a host-native operation confirms creation and returns its task or chat handle or link. A prepared composer or deep link is not a successful dispatch.
- Wait or monitor only when the parent must synthesize the result.
- Route an instruction to an existing worker only after the continuation gate passes.
- Start a separate worker for every discontinuous substantive task. Select its model role and reasoning effort independently; do not inherit either merely because another worker is open.
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

Report `model-role` and `reasoning` as the levels the work requires. When the current agent runs below them and no escalation is available, say so in `reason`.

For `durable-task`, also report:

```text
dispatch-status: created | prepared | unavailable
```

Use `created` only after host-native creation succeeds, `prepared` when user action is still required, and `unavailable` when neither creation nor a faithful user-mediated handoff is possible. Do not expose internal routing analysis unless the user asks.
