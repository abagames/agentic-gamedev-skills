# Codex App Adapter

Read this reference when `durable-task` is the intended boundary in the Codex app.

## Resolve the available operation

Use the first available path:

1. **Host-native creation** — Inspect the exposed task or chat creation tool and its schema. Create a separate task in the same project or local workspace unless the user requested another destination. Pass the complete handoff, then return the created handle or link with `dispatch-status: created`.
2. **User-mediated deep link** — When no creation tool is exposed but Codex deep links are usable, prepare a new-chat link as described below.
3. **Unavailable** — When neither path exists, return `dispatch-status: unavailable` with the handoff text. Do not claim that a task was launched.

Do not open a GUI or activate a deep link automatically unless the user explicitly authorized that externally visible action and host policy permits it.

## Preserve project placement

Use a separate chat for a distinct outcome while preserving the current project or workspace when it remains in scope.

- For a local project, preserve the exact absolute workspace path.
- When only a Git remote identifies the workspace, preserve the exact remote URL.
- For a hosted project, copy the opaque project identifier only from host state or tool output; never invent or derive it.
- Keep the handoff self-contained. Chats may share project files and instructions, but they do not share a transcript.

Do not move the task to another project merely to obtain isolation. Select isolation separately and only through capabilities the host exposes.

## Prepare a Codex deep link

Use one of the documented forms:

```text
codex://threads/new?prompt=<encoded-handoff>&path=<encoded-absolute-path>
codex://new?prompt=<encoded-handoff>&originUrl=<encoded-git-remote-url>
```

Encode each query value as a URI component. Prefer `path` when an exact local workspace is known; Codex resolves it before `originUrl` when both are present. Do not put credentials, secrets, or unnecessary private data in a link.

A deep link opens a new chat and places `prompt` in the composer; it does not submit the prompt or start execution. Report `prepared`, tell the user that submission is required, and do not wait, monitor, claim a worker exists, or fabricate a task handle.

## Reject false substitutes

These operations do not create a durable user-visible task:

| Operation | Why it is not a durable task |
| --- | --- |
| same-thread goal or plan | Changes coordination state inside the current chat |
| internal subagent | Returns to the parent and lacks an independent user-visible lifecycle |
| scheduled automation | Runs later or recurs under scheduler ownership |
| shell or GUI launch alone | May open a composer but does not prove submission or task creation |

If the requested visibility, follow-up path, or approval routing cannot be preserved, follow the fallback stop rule in [execution-backends.md](execution-backends.md).

## Official behavior references

- [Projects and chats](https://learn.chatgpt.com/docs/projects)
- [Commands and Codex deep links](https://learn.chatgpt.com/docs/reference/commands)
