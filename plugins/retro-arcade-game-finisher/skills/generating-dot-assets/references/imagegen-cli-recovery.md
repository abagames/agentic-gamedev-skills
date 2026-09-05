# Recovering built-in image_gen output in Codex CLI

## Summary

In Codex CLI, the built-in `image_gen` tool may not write a visible image file under
`$CODEX_HOME/generated_images`, and the terminal UI may not display the generated
image. In the observed run, the generated PNG was stored inside the Codex session
JSONL log as base64 text.

The relevant event is:

- `type`: `event_msg`
- `payload.type`: `image_generation_end`
- `payload.result`: base64-encoded PNG bytes
- `payload.call_id`: image generation call id
- `payload.revised_prompt`: final prompt used by the image tool

## Observed Example

Session log:

```text
/home/cs8k/.codex/sessions/2026/06/22/rollout-2026-06-22T09-21-26-019eecb4-185f-7bf3-a356-f188a43fa73d.jsonl
```

Image generation call id:

```text
ig_0e06ecc00f9d1ef2016a38801b5cb88191a715c8d67edf5887
```

Recovered file:

```text
/home/cs8k/tmp/flip-walker/pelican-from-imagegen.png
```

Validation:

```text
PNG image data, 1024 x 1536, 8-bit/color RGB, non-interlaced
```

## Recovery Steps

1. Find the current session log.

   Codex CLI session logs are usually under:

   ```text
   $CODEX_HOME/sessions/YYYY/MM/DD/rollout-*.jsonl
   ```

   If `CODEX_HOME` is not set, it is commonly:

   ```text
   ~/.codex
   ```

2. Search the session log for image generation events.

   ```bash
   rg -n '"image_generation_end"|'"'"'call_id'"'"'|'"'"'revised_prompt'"'"' ~/.codex/sessions
   ```

3. Decode `payload.result` from the matching `image_generation_end` event.

   Use this script, replacing `session` and `out` as needed:

   ```bash
   python3 - <<'PY'
   import base64
   import json
   from pathlib import Path

   session = Path("/home/cs8k/.codex/sessions/2026/06/22/rollout-2026-06-22T09-21-26-019eecb4-185f-7bf3-a356-f188a43fa73d.jsonl")
   out = Path("/home/cs8k/tmp/flip-walker/recovered-imagegen.png")

   for line in session.read_text().splitlines():
       obj = json.loads(line)
       payload = obj.get("payload", {})
       if payload.get("type") == "image_generation_end":
           result = payload.get("result")
           if not result:
               continue
           out.write_bytes(base64.b64decode(result))
           print(out)
           break
   else:
       raise SystemExit("No image_generation_end result found")
   PY
   ```

4. Validate the recovered file.

   ```bash
   file /home/cs8k/tmp/flip-walker/recovered-imagegen.png
   ```

## Recovering a Specific Call ID

If a session has multiple image generations, filter by `payload.call_id`:

```bash
python3 - <<'PY'
import base64
import json
from pathlib import Path

session = Path("/path/to/rollout.jsonl")
call_id = "ig_..."
out = Path("/path/to/output.png")

for line in session.read_text().splitlines():
    obj = json.loads(line)
    payload = obj.get("payload", {})
    if (
        payload.get("type") == "image_generation_end"
        and payload.get("call_id") == call_id
    ):
        out.write_bytes(base64.b64decode(payload["result"]))
        print(out)
        break
else:
    raise SystemExit(f"No image result found for {call_id}")
PY
```

## Notes

- The built-in `image_gen` tool schema currently exposes only `prompt`; there is no
  `output_path`, `save_path`, or destination argument.
- Asking for a save path inside the prompt does not make the built-in tool write to
  that filesystem path.
- For deterministic file output, use either:
  - built-in `image_gen`, then decode `image_generation_end.result` from the session log
  - CLI/API fallback with an explicit output path, when that path is appropriate for the task
- Do not assume files under `$CODEX_HOME/generated_images` are from the current run.
  Check timestamps and the session log first.
