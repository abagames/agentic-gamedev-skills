# Template Scope (Invariant Layer Only)

This bundled `godot-base/` template is an infrastructure-only skeleton.
It must not lock gameplay, visual identity, or audio identity.

## Allowed

- Test-hook interfaces in `main.gd`
- Generic telemetry/KPI helpers
- Low-level audio primitives (`sine/square/triangle/noise`, envelope)
- Headless/test/export infrastructure

## Forbidden

- Default gameplay logic (score gain, lose condition, enemy behavior)
- Default visual style (palette, glow profile, HUD language, scripted FX)
- Event-level SFX vocabulary tied to gameplay semantics
- Pre-bundled font assets and font license payloads
- Domain-locked naming in base interfaces (e.g. fixed `left/right/thrust`, `enemy/chaser` semantics)
- Predefined exploratory input choreography that assumes a specific control fantasy

## Implementation Note

When creating a new game from this template, implement mechanics/visual/audio in game-specific files first,
and keep the template itself free of game-specific behavior.
