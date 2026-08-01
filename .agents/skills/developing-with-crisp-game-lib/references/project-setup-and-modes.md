# crisp-game-lib Project Setup and Runtime Modes

Use only the sections relevant to the project. Exact API behavior remains in [api.md](api.md).

## Contents

- Project setup
- Named input bindings
- Arcade-cycle ownership
- Repository tester contract

## Project setup

Preserve an existing project's setup. For a new project, choose one of these modes.

### CDN / classic script

Use `index.html` plus `main.js`. Pin a version already specified by the project or verified from package/CDN metadata. Do not invent a version. A clearly labeled throwaway draft may use `@latest`; a committed or reproducible project may not. Algo-chip helpers require crisp-game-lib 1.5.0 or later.

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, height=device-height, user-scalable=no, initial-scale=1, maximum-scale=1" />
    <!-- Include these two scripts only when using built-in sound. -->
    <script src="https://unpkg.com/algo-chip@1.1.0/packages/core/dist/algo-chip.umd.js"></script>
    <script src="https://unpkg.com/algo-chip@1.1.0/packages/util/dist/algo-chip-util.umd.js"></script>
    <script src="https://unpkg.com/crisp-game-lib@<verified-version>/docs/bundle.js"></script>
    <script src="./main.js"></script>
    <script>window.addEventListener("load", onLoad);</script>
  </head>
  <body style="background: #ddd"></body>
</html>
```

Optional CDN scripts must precede `bundle.js`: `gif-capture-canvas` for capture, and `pixi.js` plus `pixi-filters` for WebGL themes.

```javascript
title = "GAME NAME";
description = `[Control instructions]`;
characters = [];
options = { viewSize: { x: 100, y: 100 }, theme: "simple" };

let player, enemies;
function update() {
  if (!ticks) {
    player = { pos: vec(50, 50) };
    enemies = [];
  }
  // Input → state/physics → spawn → draw/collision → score → game over
}
```

### npm / bundler

Use this only when a bundler is already configured or the task includes bootstrapping one. Install `crisp-game-lib`; keep CDN-only optional libraries as script tags when needed.

```javascript
import "crisp-game-lib";

const title = "GAME NAME";
const description = `[Control instructions]`;
const characters = [];
const options = {};

function update() {
  if (!ticks) {
    // Initialize.
  }
}

init({ update, title, description, characters, options });
```

## Named input bindings

Create one binding function per named action and reuse it in play, ceremonies, menus, and name entry. A practical keyboard default is:

```javascript
const moveLeft = () =>
  keyboard.code.ArrowLeft.isPressed || keyboard.code.KeyA.isPressed;
const actionPressed = () =>
  keyboard.code.Space.isJustPressed || keyboard.code.KeyZ.isJustPressed ||
  keyboard.code.KeyX.isJustPressed || keyboard.code.KeyJ.isJustPressed ||
  keyboard.code.KeyK.isJustPressed;
const confirmPressed = () =>
  actionPressed() || keyboard.code.Enter.isJustPressed;
```

The synonym pairs support arrow-key and WASD hand layouts. `confirm` is a superset of `action`, while Enter remains ceremony-only. Adapt bindings to the project, but keep one source of truth.

## Arcade-cycle ownership

Choose one complete contract; mixing them causes score, title, and game-over failures.

### Library-owned cycle

- Define `title` and `description`.
- Let the library render score; do not draw it again with `text()`, or the score appears twice.
- Call `end()` for game over.
- Insert any custom pre-game-over phase before `end()` while `update()` still runs.

### Game-owned cycle

- Leave `title` and `description` undefined so `update()` owns frame zero onward.
- Never call `end()`; represent game over, name entry, table, and attract mode as game phases.
- Disable `options.isShowingScore` and draw score explicitly.
- Process frame-scheduled jingles before any point that stops the update loop.

When library replay is enabled, guard persistence with `isReplaying`, keep custom phases input-deterministic, and prevent a just-pressed input from bleeding through multiple same-frame phase transitions.

## Repository tester contract

Apply these only to fixtures exercised by this repository's automated game harness:

- Keep game-specific helper logic inside `update()` when the tester cannot execute top-level helpers.
- Prefer detectable moving-hazard names such as `obstacles`, `enemies`, or `hazards` when spawn analysis depends on them.
- Prefer `addScore(points, x, y)` when score-event positions must be logged accurately.
- Give collision-critical `line`, `bar`, or `arc` entities a `box` or `rect` collision carrier because the headless simulator cannot detect those primitives alone.

Confirm the actual harness limitation before changing a normal user project to satisfy this contract.
