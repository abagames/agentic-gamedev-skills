#!/usr/bin/env node
// Folds every trace through a reducer and reports, per trace, the final state,
// the first step at which each invariant is violated, and any mismatch from the
// bundled reference reducer's complete final state.
//
//   node check.mjs [reducerPath] [tracesPath]
//
// Exit 0 when no invariant or reference outcome is violated, 1 when any is, and
// 2 on a harness problem.
// The invariants are derived from the observed state sequence only; the checker
// never inspects the reducer's source.

import { readFileSync } from "node:fs";
import { pathToFileURL } from "node:url";
import { resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const reducerPath = resolve(process.argv[2] ?? resolve(here, "reducer.mjs"));
const tracesPath = resolve(process.argv[3] ?? resolve(here, "traces.json"));
const referencePath = resolve(here, "reducer.mjs");

let mod;
let reference;
try {
  mod = await import(pathToFileURL(reducerPath).href);
  reference = await import(pathToFileURL(referencePath).href);
} catch (err) {
  console.error(`cannot load reducer or bundled reference: ${err.message}`);
  process.exit(2);
}
if (
  typeof mod.run !== "function" ||
  typeof mod.initialState !== "function" ||
  typeof reference.run !== "function" ||
  typeof reference.initialState !== "function"
) {
  console.error("reducer must export initialState() and run(trace, init)");
  process.exit(2);
}

const traces = JSON.parse(readFileSync(tracesPath, "utf8"));

// --- invariants over the observed state sequence -----------------------------

function invScoreOnce(trace, states) {
  const credited = new Map(); // uid -> step index that credited it
  const out = [];
  for (let i = 0; i < trace.length; i++) {
    const ev = trace[i];
    const before = states[i];
    const after = states[i + 1];
    const delta = after.score - before.score;
    if (delta === 0) continue;
    if (ev.type === "load") continue; // restoring a snapshot is not a fresh credit
    if (ev.type !== "strike" && ev.type !== "release") {
      out.push({ step: i, event: ev, detail: `score changed by ${delta} on a "${ev.type}" event` });
      continue;
    }
    const uid = before.slots[ev.slot]?.uid;
    if (uid === undefined) {
      out.push({ step: i, event: ev, detail: `score changed by ${delta} with no entity in slot ${ev.slot}` });
      continue;
    }
    if (credited.has(uid)) {
      out.push({ step: i, event: ev, detail: `uid ${uid} scored again (first credited at step ${credited.get(uid)})` });
      continue;
    }
    credited.set(uid, i);
  }
  return out;
}

function invIframeSource(trace, states) {
  const out = [];
  for (let i = 0; i < trace.length; i++) {
    const ev = trace[i];
    if (states[i].iframesUntil === states[i + 1].iframesUntil) continue;
    if (ev.type === "hazard" || ev.type === "load") continue;
    out.push({
      step: i,
      event: ev,
      detail: `iframesUntil ${states[i].iframesUntil} -> ${states[i + 1].iframesUntil} on a "${ev.type}" event`,
    });
  }
  return out;
}

function invPoolFresh(trace, states) {
  const seen = new Set();
  const out = [];
  for (let i = 0; i < trace.length; i++) {
    for (const e of Object.values(states[i].slots)) seen.add(e.uid);
    if (trace[i].type !== "spawn") continue;
    const e = states[i + 1].slots[trace[i].slot];
    if (!e) {
      out.push({ step: i, event: trace[i], detail: `spawn produced no entity in slot ${trace[i].slot}` });
      continue;
    }
    if (seen.has(e.uid)) {
      out.push({ step: i, event: trace[i], detail: `spawn reused uid ${e.uid} in slot ${trace[i].slot}` });
    }
    if (e.scored) {
      out.push({ step: i, event: trace[i], detail: `spawn produced uid ${e.uid} already marked scored` });
    }
  }
  return out;
}

// Every field a save must capture and a load must restore, including the entity
// table: rewinding the score without rewinding the entities it was earned from
// leaves a state no play sequence can produce.
const SNAPSHOT_FIELDS = [
  "tick",
  "score",
  "hp",
  "energy",
  "iframesUntil",
  "nextUid",
  "slots",
  "charging",
  "chargeStart",
];

// Order-insensitive structural equality, so a differently ordered slots object
// is not reported as a divergence.
function stable(v) {
  if (v === null || typeof v !== "object") return JSON.stringify(v) ?? "undefined";
  if (Array.isArray(v)) return `[${v.map(stable).join(",")}]`;
  return `{${Object.keys(v).sort().map((k) => `${JSON.stringify(k)}:${stable(v[k])}`).join(",")}}`;
}

function firstDifference(expected, actual, path = "state") {
  if (stable(expected) === stable(actual)) return null;
  if (
    expected === null ||
    actual === null ||
    typeof expected !== "object" ||
    typeof actual !== "object"
  ) {
    return { path, expected, actual };
  }
  const keys = [...new Set([...Object.keys(expected), ...Object.keys(actual)])].sort();
  for (const key of keys) {
    const difference = firstDifference(expected[key], actual[key], `${path}.${key}`);
    if (difference) return difference;
  }
  return { path, expected, actual };
}

function invSaveRoundtrip(trace, states) {
  const out = [];
  let snapshot = null;
  for (let i = 0; i < trace.length; i++) {
    const ev = trace[i];
    if (ev.type === "save") {
      snapshot = Object.fromEntries(SNAPSHOT_FIELDS.map((f) => [f, states[i + 1][f]]));
      continue;
    }
    if (ev.type !== "load" || snapshot === null) continue;
    for (const f of SNAPSHOT_FIELDS) {
      const got = states[i + 1][f];
      if (stable(got) !== stable(snapshot[f])) {
        out.push({ step: i, event: ev, detail: `load restored ${f}=${stable(got)}, saved value was ${stable(snapshot[f])}` });
      }
    }
  }
  return out;
}

// Ground-truth constants, held here rather than imported, so a reducer that
// retunes them cannot move the bar it is being scored against.
const ENERGY_CAP = 5;
const REGEN_PERIOD = 10;
const HOLD_MIN = 5;

function invEnergyRange(trace, states) {
  const out = [];
  for (let i = 0; i < trace.length; i++) {
    const e = states[i + 1].energy;
    if (e >= 0 && e <= ENERGY_CAP) continue;
    out.push({ step: i, event: trace[i], detail: `energy ${e} outside 0..${ENERGY_CAP}` });
  }
  return out;
}

function invEnergySource(trace, states) {
  const out = [];
  for (let i = 0; i < trace.length; i++) {
    const ev = trace[i];
    if (states[i + 1].energy <= states[i].energy) continue;
    if (ev.type === "load") continue;
    if (ev.type === "tick" && states[i + 1].tick % REGEN_PERIOD === 0) continue;
    out.push({
      step: i,
      event: ev,
      detail: `energy ${states[i].energy} -> ${states[i + 1].energy} on a "${ev.type}" event at tick ${states[i + 1].tick}`,
    });
  }
  return out;
}

// One hold arms one shot. A release that credits score must consume an arming
// charge; a second credited release with no charge between them is a violation.
function invChargeOneShot(trace, states) {
  const out = [];
  let armed = false;
  for (let i = 0; i < trace.length; i++) {
    const ev = trace[i];
    if (ev.type === "charge") armed = true;
    if (ev.type !== "release") continue;
    const credited = states[i + 1].score !== states[i].score;
    if (credited && !armed) {
      out.push({ step: i, event: ev, detail: "release credited score with no charge held for it" });
    }
    armed = false; // a release ends the hold whether or not the shot landed
  }
  return out;
}

// A release always ends the hold. Leaving it armed lets one charge pay for a
// second shot later.
function invChargeConsumed(trace, states) {
  const out = [];
  for (let i = 0; i < trace.length; i++) {
    if (trace[i].type !== "release") continue;
    if (states[i + 1].charging === false) continue;
    out.push({ step: i, event: trace[i], detail: "release left the hold still armed" });
  }
  return out;
}

function invChargeThreshold(trace, states) {
  const out = [];
  for (let i = 0; i < trace.length; i++) {
    const ev = trace[i];
    if (ev.type !== "release") continue;
    if (states[i + 1].score === states[i].score) continue;
    const held = states[i].tick - states[i].chargeStart;
    if (held >= HOLD_MIN) continue;
    out.push({ step: i, event: ev, detail: `release credited score after a hold of ${held} ticks` });
  }
  return out;
}

const INVARIANTS = {
  "INV-SCORE-ONCE": invScoreOnce,
  "INV-IFRAME-SOURCE": invIframeSource,
  "INV-POOL-FRESH": invPoolFresh,
  "INV-SAVE-ROUNDTRIP": invSaveRoundtrip,
  "INV-ENERGY-RANGE": invEnergyRange,
  "INV-ENERGY-SOURCE": invEnergySource,
  "INV-CHARGE-ONE-SHOT": invChargeOneShot,
  "INV-CHARGE-CONSUMED": invChargeConsumed,
  "INV-CHARGE-THRESHOLD": invChargeThreshold,
};

// --- run ---------------------------------------------------------------------

const report = {};
let failed = false;

for (const [name, trace] of Object.entries(traces)) {
  const { final, states } = mod.run(trace, mod.initialState());
  const expectedFinal = reference.run(trace, reference.initialState()).final;
  const violations = {};
  for (const [inv, fn] of Object.entries(INVARIANTS)) {
    const hits = fn(trace, states);
    if (hits.length > 0) {
      violations[inv] = hits[0]; // first divergence only
      failed = true;
    }
  }
  const difference = firstDifference(expectedFinal, final);
  if (difference) {
    violations["OBS-REFERENCE-FINAL"] = {
      step: trace.length,
      event: { type: "end-of-trace" },
      detail: `${difference.path} was ${stable(difference.actual)}, expected ${stable(difference.expected)}`,
    };
    failed = true;
  }
  report[name] = {
    final: {
      tick: final.tick,
      score: final.score,
      hp: final.hp,
      energy: final.energy,
      iframesUntil: final.iframesUntil,
      charging: final.charging,
      chargeStart: final.chargeStart,
    },
    violations,
  };
}

for (const [name, r] of Object.entries(report)) {
  const f = r.final;
  console.log(
    `${name.padEnd(20)} tick=${f.tick} score=${f.score} hp=${f.hp} energy=${f.energy} ` +
      `iframesUntil=${f.iframesUntil} charging=${f.charging} chargeStart=${f.chargeStart}`
  );
  for (const [inv, v] of Object.entries(r.violations)) {
    console.log(`  VIOLATION ${inv} at step ${v.step} (${JSON.stringify(v.event)}): ${v.detail}`);
  }
}
console.log(
  failed
    ? "\nRESULT: invariant violations or reference mismatches found"
    : "\nRESULT: all invariants and reference finals match"
);
process.exit(failed ? 1 : 0);
