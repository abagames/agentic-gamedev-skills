---
name: developing-with-crisp-game-lib
description: "Creates or repairs browser mini-games specifically using crisp-game-lib. Use only when the user explicitly asks for crisp-game-lib or the existing project already uses it; skip for Godot, Unity, Phaser, canvas-only, or unspecified engine requests."
---

# Developing with crisp-game-lib

## Workflow

1. Inspect the existing project before choosing a setup. Preserve its pinned library version, entry style, helpers, and test harness.
2. For a new project, choose CDN/classic-script or npm/bundler setup. Read [project-setup-and-modes.md](references/project-setup-and-modes.md) before creating entry files or selecting a version.
3. State each named action and its physical bindings before coding. For a one-button game, state whether press, hold, or release acts and which phases are intentionally unused.
4. Implement one clear frame order: input → state/physics → spawning → drawing/collision → scoring → game over.
5. Apply the runtime contracts below and validate only behavior the change can reach. A new game or entry-point/input/audio/loop change needs a real-browser runtime check; a localized fix needs the affected check plus startup smoke.
6. After the first working loop, record any interesting emergent behavior before deciding whether a collision artifact, draw-order effect, or physics interaction is a bug or a better mechanic.

Use `if (!ticks) { ... }` for first-frame initialization in classic-script projects. In a bundler project, follow the existing `init({ update, title, description, characters, options })` entry style.

## Runtime contracts

- **Use documented APIs only.** Test mocks may expose globals absent from the browser bundle. Consult [api.md](references/api.md) for exact signatures, colors, sounds, collision properties, and options; use standard JavaScript or define any missing helper yourself.
- **Drawing order is collision order.** A shape detects only shapes drawn earlier in the same frame. Draw targets first and detectors second.
- **Treat `input.isJustPressed` as unified input.** It merges keyboard keys and pointer input. Use `keyboard.code[...]` for a named keyboard action and `pointer.isJustPressed` for pointer-only input. Unified input is appropriate for “any input starts.”
- **Define bindings once per named action.** Every phase must read the same synonym set. Multiple physical keys bound to one named action do not create additional game actions.
- **Keep library-owned and game-owned arcade cycles separate.** The normal cycle uses `title`, `description`, library score rendering, and `end()`. A custom attract/ceremony/name-entry cycle owns all of those. Read [project-setup-and-modes.md](references/project-setup-and-modes.md) before implementing or changing a custom cycle.
- **Verify audio audibly.** For built-in audio on crisp-game-lib 1.5.0+, load both algo-chip globals before the bundle and verify `algoChipSession != null` after first input. Missing globals silently disable `play()` and BGM.
- **Use current particle syntax.** Call `particle(pos, { count, speed, angle, angleWidth })`; do not introduce the legacy positional form.
- **Avoid `white` for visible art.** It matches the background across bundled themes. Use another color or a `light_*` variant.

Minimal collision pattern:

```javascript
color("red");
enemies.forEach((enemy) => box(enemy.pos, 10));

color("blue");
if (box(player.pos, 8).isColliding.rect.red) {
  end();
}
```

## Conditional references

- Read [api.md](references/api.md) whenever exact library behavior matters. Its API enumeration is canonical; do not reconstruct it from memory.
- Read [examples.md](references/examples.md) only when a complete loop matching the requested control or game pattern would reduce implementation risk.
- Read [project-setup-and-modes.md](references/project-setup-and-modes.md) for CDN/npm skeletons, version pinning, default input bindings, custom arcade ownership, or this repository's simulator/tester constraints.

## Validation

Check the applicable items in a real browser:

- startup has no console error or uncaught exception;
- controls map only to their named actions in every reachable phase;
- collision direction and draw order match the intended rule;
- score and game-over behavior match the chosen ownership mode;
- audio produces sound after user activation when audio changed;
- pointer/touch input works when the game claims mobile support.

For this repository's automated harness, also apply the tester contract in [project-setup-and-modes.md](references/project-setup-and-modes.md). Do not impose that contract on unrelated user projects.
