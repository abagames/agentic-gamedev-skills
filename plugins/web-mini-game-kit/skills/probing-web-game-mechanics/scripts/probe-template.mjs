// Probe template — COPY and ADAPT per game; not a generic runner.
// Usage: node probe.mjs [path/to/index.html] (run from the game project dir so
// Playwright resolves from its node_modules).
import { createRequire } from "node:module";
const require = createRequire(process.cwd() + "/");
const { chromium } = require("playwright");
const path = require("path");

const target = process.argv[2] || "index.html";
const url = /^https?:/.test(target) ? target : "file://" + path.resolve(target);

const errors = [];
const failures = [];
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 500, height: 500 } });
page.on("pageerror", (e) => errors.push("pageerror: " + e.message));
page.on("console", (m) => {
  if (m.type() === "error") errors.push("console: " + m.text());
});

// assert helper: name, actual, predicate (or expected value)
const check = (name, actual, expected) => {
  const ok = typeof expected === "function" ? expected(actual) : actual === expected;
  console.log(`${ok ? "PASS" : "FAIL"} ${name}: ${JSON.stringify(actual)}`);
  if (!ok) failures.push(name);
};

await page.goto(url, { waitUntil: "load" });
await page.waitForTimeout(800);
// Leave the title screen for real before injecting anything.
await page.keyboard.press("Space");
await page.waitForTimeout(400);

// ---- Scenario: <name it after the spec line it verifies> ----
// 1. Inject minimal state; neutralize confounders (park timers, clear other
//    entities, make player invulnerable) and record baselines as deltas.
await page.evaluate(`
  // EXAMPLE for a crisp-game-lib game — replace with the target game's globals:
  // enemies = []; hawkTimer = 99999; invuln = 99999;
  // window.__s0 = score;
`);
// 2. Let the game loop process the injected state.
await page.waitForTimeout(300);
// 3. Read back and assert concrete expected values from the spec.
// const r = await page.evaluate(`({ gained: score - window.__s0 })`);
// check("bank n=3 at mult 2 adds 180", r.gained, 180);

// Repeat scenarios; reset shared state (storage, lives, phase) between them.

console.log("ERRORS:", errors.length ? errors : "none");
await browser.close();
process.exit(errors.length || failures.length ? 1 : 0);
