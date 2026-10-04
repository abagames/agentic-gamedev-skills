# Frame Manifest

`scripts/check-screen-frames.mjs` reads one JSON file describing captured frames. Generate it from
the running game — the rectangles the renderer actually used — never by hand.

```json
{
  "viewport": { "w": 224, "h": 256 },
  "minScale": 2,
  "thresholds": { "glyphPx": 12, "contrast": 3, "briefBaseMs": 400, "briefPerCharMs": 50 },
  "frames": [
    {
      "id": "extend-on-clear",
      "elements": [
        { "id": "banner:clear", "kind": "text", "rect": [60, 100, 104, 7],
          "glyphH": 7, "fg": [255, 255, 255], "bg": [0, 0, 0] },
        { "id": "notice:extend", "kind": "text", "rect": [80, 112, 64, 7],
          "glyphH": 7, "visibleMs": 2000, "chars": 6 },
        { "id": "hud:panel", "kind": "panel", "rect": [0, 0, 224, 24], "opaque": true, "z": 10 },
        { "id": "popup:score", "kind": "text", "rect": [40, 18, 20, 7], "glyphH": 7, "z": 5 }
      ]
    }
  ]
}
```

This example contains one defect on purpose: `popup:score` is drawn before the opaque `hud:panel`
panel that covers it, so the script reports `occluded` and exits 1.

## Fields

| Field | Meaning |
|---|---|
| `viewport` | Logical size of the game screen |
| `minScale` | Device pixels per logical pixel at the smallest supported display; default 1 |
| `thresholds` | Optional overrides; defaults are shown above |
| `frames[].id` | Name of the moment, matching the capture |
| `elements[].kind` | `text` or `indicator` (readable; all checks apply) or `panel` (may occlude) |
| `elements[].rect` | `[x, y, w, h]` in logical pixels |
| `elements[].opaque` | For a panel: it hides what is drawn before it |
| `elements[].z` | Draw order within the frame; a higher value is drawn later, on top. Emit the renderer's own order (a draw-call index is enough); equal values establish no order |
| `elements[].parent` | Id of the panel an element belongs to. Informational: it labels the `REVIEW` line and does not exempt the element from the occlusion check |
| `elements[].group` | Elements sharing a group may overlap (a label and its own value) |
| `elements[].glyphH` | Glyph height in logical pixels, for `small` |
| `elements[].fg`, `bg` | Element colour and the dominant colour behind it, for `faint` |
| `elements[].visibleMs`, `chars` | Lifetime and length of a transient element, for `brief` |

Checks whose fields are absent are skipped for that element and counted as skipped in the output,
so missing data is visible.

## Occlusion and draw order

Rectangles cannot say which of two intersecting things is on top. The script therefore decides
occlusion only when both the element and the panel carry `z`: the element is `occluded` when the
panel is drawn later, whether or not it is that panel's child.

When `z` is missing on either side, or the two values are equal, the order is not established and
the intersection is printed as `REVIEW occlusion-candidate`; it does not fail the run. This
includes an element and its own `parent` panel, because belonging to a panel does not guarantee
being drawn after it. Open the captured frame and judge it by eye, or supply distinct `z` values
and re-run. A manifest without `z` therefore produces one `REVIEW` line per label on a panel;
emitting the draw order removes them.

## Thresholds

The defaults are starting points for low-resolution pixel displays, not standards.

- `glyphPx` 12: glyph height in device pixels. A 3×5 font at 2× fails; a 5×7 font at 2× passes.
- `contrast` 3: WCAG-style contrast ratio between `fg` and `bg`. For an indicator, also compare by
  eye against decorative elements; it should not be the dimmest thing on screen.
- `briefBaseMs` 400 and `briefPerCharMs` 50: a transient element must stay at least
  `base + perChar × chars`.

Record any threshold you change, and why, beside the manifest.
