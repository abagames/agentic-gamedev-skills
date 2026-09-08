---
name: smoke-testing-web-games
description: "Smoke-tests a browser game build in a headless browser through load, idle, and input phases, failing on console errors, uncaught exceptions, or crashes. Use after changes that can reach browser runtime, especially game-loop, input, dependency, entry-point, or build-output changes. Skip changes the running build cannot reach. This checks runtime health, not gameplay quality, balance, visuals, or mechanic correctness. Requires Node 18+ and Playwright with Chromium in the target project."
---

# Smoke-Testing Web Games

Run this real-browser gate once per completed change unit that can reach the game runtime. It catches environment and input-handler failures that mocks or idle-only tests can miss.

## Requirements and Usage

- Node 18+ and Playwright with Chromium installed in the project under test. The script resolves `playwright` from the directory where it runs.
- Network access when the page loads CDN resources; failed loads surface as console errors.
- Run from the game project directory:

```bash
node <skill-dir>/scripts/smoke-test.mjs path/to/index.html            # 3s idle, 6s input
node <skill-dir>/scripts/smoke-test.mjs http://localhost:5173 --idle 5 --input 10
```

Serve over HTTP when the game uses ES modules, `fetch`, or other origin-restricted features.

The harness runs these phases in order:

1. **load** — navigate through the `load` event; navigation failure is immediate failure.
2. **idle** — wait untouched for startup and frame-loop errors.
3. **input** — send scattered pointer taps, Space and arrow-key taps, plus a short arrow-key hold, with pauses for timers and spawns.

It prints each error with its phase. Exit `0` means PASS, `1` means a runtime error or load failure, and `2` means a harness problem such as missing Playwright or bad arguments.

## Boundaries

- A PASS means only that the page loaded and survived the exercised idle/input paths without reported errors. It does not prove that the loop started or that mechanics, audio, visuals, performance, difficulty, or balance are correct.
- For state transitions or scoring formulas, use `probing-web-game-mechanics`; test silent no-op behavior with a dedicated runtime check.
- The generic input schedule does not cover custom keys. Extend it or report those controls as untested.
- Treat CDN/network errors as failures, but rerun before attributing a flaky external load to game code.

## Harness Self-Test

```bash
node scripts/smoke-test.mjs assets/fixtures/fixture-ok.html                    # PASS, exit 0
node scripts/smoke-test.mjs assets/fixtures/fixture-input-crash.html           # FAIL, exit 1
node scripts/smoke-test.mjs assets/fixtures/fixture-input-crash.html --input 0 # PASS: idle misses the bug
```
