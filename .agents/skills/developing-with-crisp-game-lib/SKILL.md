---
name: developing-with-crisp-game-lib
description: "Creates or repairs browser mini-games specifically using crisp-game-lib. Use only when the user explicitly asks for crisp-game-lib or the existing project already uses it; skip for Godot, Unity, Phaser, canvas-only, or unspecified engine requests."
---

# Developing with crisp-game-lib

Creates browser-based mini-games using crisp-game-lib, a JavaScript library for rapid arcade game development.

## 1. Purpose and Scope

Use this skill when asked to create or repair a mini-game with crisp-game-lib. If the user asks for Godot or another engine, or leaves the engine unspecified, do not use this skill unless the existing project is already a crisp-game-lib project.

This guide separates:

- ordered implementation steps (what to do in sequence)
- mandatory constraints (rules that always apply)
- reusable patterns and references (optional support)

## 2. Pre-Implementation Decisions

### Choose Project Setup

Choose the appropriate setup based on the project context.

#### Option A: CDN (Simplest — single HTML file)

Create a project directory with `index.html` and `main.js`. CDN is acceptable for final projects when the script URL is pinned to a verified version. For quick prototypes only, a clearly labeled draft may use `crisp-game-lib@latest`.

For reproducible assignments or committed projects:

- CDN is fine; the reproducibility issue is an unpinned moving version such as `@latest`.
- Pin only a version that is already specified by the project or that you have verified from package metadata/CDN access.
- Do not invent a crisp-game-lib version number.
- If using `algo-chip` helpers, the verified `crisp-game-lib` version must be `1.5.0` or later.
- If no verified version is available, treat version selection as a blocker for a final committed skeleton: ask for the existing project version or permission to check package/CDN metadata. You may show `@latest` only in a clearly labeled draft, not as the final committed form.

**index.html:**

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>My Game</title>
    <meta
      name="viewport"
      content="width=device-width, height=device-height, user-scalable=no, initial-scale=1, maximum-scale=1"
    />
    <!-- REQUIRED for any sound: crisp-game-lib 1.5.0+ built-in audio (play()/BGM)
         silently no-ops without the AlgoChip/AlgoChipUtil globals (no console error) -->
    <script src="https://unpkg.com/algo-chip@1.1.0/packages/core/dist/algo-chip.umd.js"></script>
    <script src="https://unpkg.com/algo-chip@1.1.0/packages/util/dist/algo-chip-util.umd.js"></script>
    <script src="https://unpkg.com/crisp-game-lib@<verified-version>/docs/bundle.js"></script>
    <script src="./main.js"></script>
    <script>
      window.addEventListener("load", onLoad);
    </script>
  </head>
  <body style="background: #ddd"></body>
</html>
```

Other optional script tags (add before `bundle.js` if needed):

```html
<!-- GIF capture: add if options.isCapturing is true -->
<script src="https://unpkg.com/gif-capture-canvas@1.1.0/build/index.js"></script>
<!-- WebGL themes (pixel, shape, shapeDark, crt): add if using these themes -->
<script src="https://unpkg.com/pixi.js@5.3.0/dist/pixi.min.js"></script>
<script src="https://unpkg.com/pixi-filters@3.1.1/dist/pixi-filters.js"></script>
```

#### Option B: npm + Bundler (Vite, Webpack, etc.)

Assumes a bundler is already configured (e.g. project has `package.json` and a Vite/Webpack/etc. dev-server entry). If not, bootstrap the bundler first (e.g. `npm create vite@latest`) before adding crisp-game-lib.

The other CDN-only optional tags (`gif-capture-canvas`, `pixi.js` + `pixi-filters`) have no documented npm replacement — keep them as `<script>` tags in `index.html` if used.

```bash
npm install crisp-game-lib
```

If this project also uses `algo-chip` helpers, install or pin `crisp-game-lib` at `1.5.0` or later.

**index.html:**

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>My Game</title>
    <meta
      name="viewport"
      content="width=device-width, height=device-height, user-scalable=no, initial-scale=1, maximum-scale=1"
    />
    <!-- REQUIRED for any sound: crisp-game-lib 1.5.0+ built-in audio (play()/BGM)
         silently no-ops without the AlgoChip/AlgoChipUtil globals (no console error) -->
    <script src="https://unpkg.com/algo-chip@1.1.0/packages/core/dist/algo-chip.umd.js"></script>
    <script src="https://unpkg.com/algo-chip@1.1.0/packages/util/dist/algo-chip-util.umd.js"></script>
    <script type="module" src="./main.js"></script>
  </head>
  <body style="background: #ddd"></body>
</html>
```

**main.js** (bundler version uses `const`, `import`, and `init()`):

```javascript
import "crisp-game-lib";

const title = "MY GAME";
const description = `[Control instructions]`;
const characters = [];
const options = {};

function update() {
  if (!ticks) {
    /* init */
  }
}

init({ update, title, description, characters, options });
```

## 3. Implementation Flow

### Step 1: Create `main.js`

Write `main.js` following the structure below.

Before and during implementation:

- Read `references/api.md` when you need exact function behavior, argument shapes, collision semantics, or available colors/sounds.
- Read `references/examples.md` when the requested game resembles one of the listed patterns, or when you need a complete working loop to adapt.
- For one-button games, state the exact input interpretation before coding (for example tap toggles state, tap applies impulse, hold charges, or release fires).

#### Required Structure (CDN / Repository)

```javascript
title = "GAME NAME";

description = `
[Control instructions]
`;

characters = []; // Optional pixel art (6x6 grid, use letters a-z)

options = {
  viewSize: { x: 100, y: 100 }, // Default screen size
  theme: "simple", // simple | dark | shape | shapeDark | pixel | crt
};

// Game state variables
let player, enemies;

function update() {
  if (!ticks) {
    // Initialize on first frame
    player = { pos: vec(50, 50) };
    enemies = [];
  }

  // Input → Physics → Spawn → Draw (with collision) → Score → Game Over
}
```

### Step 2: Implement Core Game Loop

Fill `update()` with a clear per-frame order:

- Input handling
- Physics/state updates
- Spawning
- Drawing (with collision checks)
- Score updates
- Game-over conditions

Use `if (!ticks) { ... }` for one-time initialization.

**Emergence review**: after the first working loop, watch for unintentional but interesting behaviors arising from crisp-game-lib idioms (collision artifacts, misordered draw calls, unexpected physics). If one looks more interesting than the original spec, record it and flag it for design reconsideration rather than silently fixing it.

### Step 3: Apply Mandatory Rules and Validate

Apply section 4 (Mandatory Rules) as required validation criteria. Scope the section 6 checklist to the change: run it in full for a new game or a change that reaches the runtime broadly (loop structure, input wiring, audio setup, entry point), and for a localized fix check only the items covering the behavior you changed, plus a short runtime check that the game still starts. Audio, mobile input, collision, and scoring do not need re-verification when the change cannot reach them.

For this repository's automated testers:

- In generated test fixtures for this repository, keep game-specific helper logic inside `update()`; tester execution can miss helpers defined outside it. In normal user projects, small top-level helpers are acceptable if the target build/test harness runs them correctly.
- Name moving hazard arrays with detectable terms such as `obstacles`, `enemies`, or `hazards` when useful. Verbose GA logs use those names to populate spawn analysis.
- Prefer `addScore(points, x, y)` over `addScore(points, pos)` when you need accurate score-event positions in tester logs.
- The headless simulator cannot detect collisions for shapes drawn only with `line`, `bar`, or `arc`. Give collision-critical entities a `box` or `rect` representation (visible or as the collision carrier) so automated collision checks can see them; keep `line`/`bar`/`arc` for decoration.

## 4. Mandatory Rules (Always Apply)

Follow these rules strictly. Violations cause silent bugs.

**Drawing order determines collision detection.** Objects can ONLY detect collision with shapes drawn BEFORE them in the same frame:

```javascript
// ✅ CORRECT: Draw targets first, then detectors
color("red");
enemies.forEach((e) => box(e.pos, 10)); // Draw enemies FIRST
color("blue");
if (box(player.pos, 8).isColliding.rect.red) {
  end();
} // Player detects enemies

// ❌ WRONG: Checking collision with something not yet drawn
color("blue");
if (box(player.pos, 8).isColliding.rect.red) {
  end();
} // red not drawn yet!
color("red");
enemies.forEach((e) => box(e.pos, 10));
```

**Call only documented API functions.** A test mock or simulator may expose helper globals (such as `sign`) that do not exist in the browser bundle, so code can pass every automated test and still crash on the first real frame or input. If a helper is not in `references/api.md` or standard JavaScript, define it yourself or use the standard equivalent (`Math.sign`, etc.).

**Do NOT manually draw the score** — *unless you have taken ownership of the arcade cycle* (see below). In the default mode the library displays it automatically; calling `text()` for score display then duplicates it.

**White color is invisible** on all themes (matches background). Use `light_` variants or other colors instead.

**Use `particle()` with object format:**

```javascript
particle(pos, { count: 5, speed: 2, angle: PI }); // ✅ Preferred
particle(pos, 5, 2, PI, PI); // ❌ Legacy format
```

**Sound requires algo-chip (1.5.0+).** At init the bundle enables audio only if the `AlgoChip` and `AlgoChipUtil` globals exist (legacy projects may instead rely on the `sss` global); with neither, `isSoundEnabled` stays false and every `play()`/BGM call silently no-ops — no console error, so smoke tests pass on a silent game. Load both algo-chip scripts before `bundle.js` and verify `algoChipSession != null` after the first input.

**`input.isJustPressed` merges ALL keyboard keys plus pointer.** In a game with key movement plus an action button, reading `input.isJustPressed` for the action fires on every arrow-key press. Read specific keys via `keyboard.code[...]`, and detect pointer-only clicks with `pointer.isJustPressed` (deriving it as `input.isJustPressed && !keyboard.isJustPressed` misses a click landing on the same frame as a key press). `input.isJustPressed` remains correct for exactly one thing: "any input starts the game".

**Bind keys once per named action, never per screen.** Define each action as a **set of synonym keys** in one place, and have every phase — play, ceremony screens, name entry, menus — read that set. Inlining key codes per screen is how one screen ends up accepting a binding the others do not: observed case, a name-entry cursor wired to arrows only in a game whose movement also accepted WASD, so WASD players could not enter their initials, and neither the probe suite nor the screenshot harness noticed because both press arrows.

Default assignment:

```javascript
// movement (held)
const moveLeft  = () => keyboard.code.ArrowLeft.isPressed  || keyboard.code.KeyA.isPressed;
// action (edge) — Space plus both cabinet button positions, for either handedness
const actionPressed = () =>
  keyboard.code.Space.isJustPressed || keyboard.code.KeyZ.isJustPressed ||
  keyboard.code.KeyX.isJustPressed  || keyboard.code.KeyJ.isJustPressed ||
  keyboard.code.KeyK.isJustPressed;
// confirm = the action set ∪ Enter
const confirmPressed = () => actionPressed() || keyboard.code.Enter.isJustPressed;
```

Rationale, in order of importance: the two synonym pairs (`Z`/`X` with arrows, `J`/`K` with WASD) cover both handedness layouts; confirm is a **superset** of action, so a hand that learned the action button always works on ceremony screens; `Enter` is confirm-only, so a ceremony key never leaks into play.

**Physical button count ≠ action count.** Binding both cabinet button positions (`Z`/`X`, `J`/`K`) to a single action is a synonym set, not a second action, and does not relax a one-button design constraint. Say so explicitly in the spec, or a later reader will treat the second key as evidence that a second action is available.

**Owning the arcade cycle.** The default flow — library title screen, `end()` for game over, library-drawn score — is one mode. A game that wants its own attract loop, ceremony screens, name entry and score table takes the other, and the contract is all-or-nothing:

- Leave `title` and `description` **undefined**. That keeps the bundle's `isNoTitle` true so `update()` runs from frame 0 and your code owns every phase. Defining either one hands control back to the library and breaks a custom attract mode.
- **Never call `end()`.** Game over, name entry and the score table become your own phases.
- Set `options.isShowingScore` **off** and draw score yourself — the library refreshes its own display only inside `initInGame()`, so in this mode a library-drawn score silently stops updating.
- Queue frame-scheduled jingles while the update loop is still running; anything scheduled past the point where the loop stops never fires.

Mixing the two modes is the failure: a self-owned cycle that still relies on the library's score display, or a default-mode game that defines its own game-over phase, produces bugs that look like rendering faults.

## 5. Common Implementation Patterns (Optional)

#### One-Button / Tap Game (Best for Mobile)

```javascript
if (input.isJustPressed) {
  /* jump, shoot, or change direction */
}
```

#### Slide Control

```javascript
player.pos.x = input.pos.x;
player.pos.clamp(5, 95, 5, 95);
```

#### Spawning with Difficulty Scaling

```javascript
// Declare at game state level
let nextEnemyTicks;

// In update(), initialize on first frame
if (!ticks) {
  nextEnemyTicks = 0;
}

// Countdown and spawn
nextEnemyTicks--;
if (nextEnemyTicks < 0) {
  enemies.push({ pos: vec(110, rnd(90) + 5) });
  nextEnemyTicks = rnd(60, 120) / difficulty;
}
```

#### Entity Update with remove()

```javascript
remove(enemies, (e) => {
  e.pos.x -= difficulty * 0.5;
  color("red");
  box(e.pos, 8);
  return e.pos.x < -10; // Remove when off-screen
});
```

#### Physics (Gravity + Jump)

```javascript
player.vy += 0.15; // Gravity
player.pos.y += player.vy;
if (player.pos.y >= ground) {
  // Ground collision
  player.pos.y = ground;
  player.vy = 0;
  player.onGround = true;
}
if (input.isJustPressed && player.onGround) {
  player.vy = -4;
  play("jump");
}
```

## 6. Verification Checklist

Open the game in a browser and check the items the change can reach — all of them for a new game or a broad runtime change (see Step 3):

- Game initializes without errors
- Controls respond correctly
- Collision detection works (drawing order is correct)
- Score increases appropriately
- `end()` triggers game over correctly
- Sound actually plays: `algoChipSession != null` after first input (silent no-op is the failure mode, not an error)
- Mobile: touch controls work if applicable

## 7. Key API Quick Reference

| Category | Functions                                                                                                                                                                                                              |
| -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Drawing  | `rect(x,y,w,h)` `box(pos,w,h)` `line(p1,p2,t)` `bar(pos,len,t,angle)` `arc(pos,r,t,start,end)`                                                                                                                         |
| Text     | `text(str,x,y)` `char(ch,x,y)` `addWithCharCode(ch,offset)`                                                                                                                                                            |
| Color    | `color("red")` — red, green, blue, yellow, purple, cyan, black, light\_\* variants, transparent                                                                                                                        |
| Input    | `input.pos` `input.isPressed` `input.isJustPressed` `keyboard.code["Space"].isJustPressed`                                                                                                                             |
| Audio    | `play("coin")` — listed names: coin, powerUp, hit, jump, select, lucky. **Treat this list as illustrative; consult `references/api.md` for the complete enumeration before invoking other names.**                     |
| Vector   | `vec(x,y)` `.add()` `.sub()` `.mul()` `.clamp(xMin,xMax,yMin,yMax)` `.wrap()` `.addWithAngle()` `.distanceTo()`                                                                                                        |
| Utility  | `times(n,fn)` `range(n)` `remove(arr,fn)` `rnd(max)` `rndi(max)` `clamp(v,min,max)` `wrap(v,min,max)` — note the free-function `clamp` / `wrap` take a scalar; the Vector method on the same name takes 4 axis bounds. |
| State    | `ticks` `score` `difficulty` `addScore(points)` `addScore(points,pos)` `addScore(points,x,y)` `end()`                                                                                                                  |
| Effects  | `particle(pos, {count, speed, angle, angleWidth})`                                                                                                                                                                     |
