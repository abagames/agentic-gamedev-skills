#!/usr/bin/env node

import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const CLASSIFICATIONS = new Set(["sfx", "jingle", "bgm", "none"]);
const PROGRAM_KINDS = new Set(["sfx", "jingle"]);

function finiteNumber(value) {
  return typeof value === "number" && Number.isFinite(value);
}

function recordOrEmpty(value, label, errors) {
  if (!value || typeof value !== "object" || Array.isArray(value)) {
    errors.push(`${label} must be an object`);
    return {};
  }
  return value;
}

function requirePositive(value, label, errors) {
  if (!finiteNumber(value) || value <= 0) errors.push(`${label} must be a positive finite number`);
}

function requireNonNegative(value, label, errors) {
  if (!finiteNumber(value) || value < 0) errors.push(`${label} must be a non-negative finite number`);
}

function requirePositiveInteger(value, label, errors) {
  if (!Number.isInteger(value) || value <= 0) errors.push(`${label} must be a positive integer`);
}

function validateSteps(steps, label, voiceLimit, maxSteps, errors) {
  if (!Array.isArray(steps) || steps.length === 0) {
    errors.push(`${label}.steps must be a non-empty array`);
    return { duration: 0, maxConcurrency: 0 };
  }
  if (steps.length > maxSteps) errors.push(`${label}.steps has ${steps.length} entries; budget is ${maxSteps}`);

  const boundaries = [];
  let duration = 0;
  steps.forEach((step, index) => {
    const prefix = `${label}.steps[${index}]`;
    if (!step || typeof step !== "object") {
      errors.push(`${prefix} must be an object`);
      return;
    }
    requireNonNegative(step.offset, `${prefix}.offset`, errors);
    requirePositive(step.duration, `${prefix}.duration`, errors);
    if (typeof step.voice !== "string" || step.voice.length === 0) errors.push(`${prefix}.voice must be a non-empty string`);
    if (finiteNumber(step.offset) && finiteNumber(step.duration) && step.duration > 0) {
      const end = step.offset + step.duration;
      duration = Math.max(duration, end);
      boundaries.push({ time: step.offset, delta: 1, voice: step.voice });
      boundaries.push({ time: end, delta: -1, voice: step.voice });
    }
  });

  boundaries.sort((a, b) => a.time - b.time || a.delta - b.delta);
  let active = 0;
  let maxConcurrency = 0;
  const activeByVoice = new Map();
  for (const boundary of boundaries) {
    const voiceActive = activeByVoice.get(boundary.voice) ?? 0;
    if (boundary.delta > 0 && voiceActive > 0) {
      errors.push(`${label} overlaps voice ${boundary.voice} at ${boundary.time}s`);
    }
    activeByVoice.set(boundary.voice, voiceActive + boundary.delta);
    active += boundary.delta;
    maxConcurrency = Math.max(maxConcurrency, active);
  }
  if (maxConcurrency > voiceLimit) errors.push(`${label} reaches ${maxConcurrency} simultaneous voices; limit is ${voiceLimit}`);
  return { duration, maxConcurrency };
}

export function validateManifestDetailed(manifest) {
  const errors = [];
  const warnings = [];
  if (!manifest || typeof manifest !== "object" || Array.isArray(manifest)) {
    return { errors: ["manifest must be an object"], warnings };
  }
  if (manifest.version !== 1) errors.push("version must be 1");
  if (!new Set(["active", "silent"]).has(manifest.audioMode)) {
    errors.push("audioMode must be active or silent");
  }

  const profile = recordOrEmpty(manifest.hardwareProfile, "hardwareProfile", errors);
  if (typeof profile.id !== "string" || !profile.id) errors.push("hardwareProfile.id must be a non-empty string");
  if (!new Set(["era-inspired", "hardware-faithful"]).has(profile.fidelity)) {
    errors.push("hardwareProfile.fidelity must be era-inspired or hardware-faithful");
  }
  if (profile.fidelity === "hardware-faithful" &&
      (typeof profile.targetHardware !== "string" || !profile.targetHardware.trim())) {
    errors.push("hardwareProfile.targetHardware must name the target for hardware-faithful fidelity");
  }
  requirePositiveInteger(profile.voiceLimit, "hardwareProfile.voiceLimit", errors);
  if (!Array.isArray(profile.primitives) || profile.primitives.length === 0) {
    errors.push("hardwareProfile.primitives must be a non-empty array");
  } else {
    profile.primitives.forEach((primitive, index) => {
      if (typeof primitive !== "string" || !primitive.trim()) {
        errors.push(`hardwareProfile.primitives[${index}] must be a non-empty string`);
      }
    });
  }

  const budgets = recordOrEmpty(manifest.budgets, "budgets", errors);
  requirePositive(budgets.sfxMaxDurationSeconds, "budgets.sfxMaxDurationSeconds", errors);
  requirePositive(budgets.jingleMaxDurationSeconds, "budgets.jingleMaxDurationSeconds", errors);
  requirePositiveInteger(budgets.maxStepsPerProgram, "budgets.maxStepsPerProgram", errors);
  requirePositive(budgets.bgmLoopMaxDurationSeconds, "budgets.bgmLoopMaxDurationSeconds", errors);
  requireNonNegative(budgets.bgmLoopMaxTailSeconds, "budgets.bgmLoopMaxTailSeconds", errors);
  const voiceLimit = finiteNumber(profile.voiceLimit) && profile.voiceLimit > 0 ? profile.voiceLimit : 1;
  const maxSteps = finiteNumber(budgets.maxStepsPerProgram) && budgets.maxStepsPerProgram > 0
    ? Math.floor(budgets.maxStepsPerProgram)
    : 24;

  const programs = recordOrEmpty(manifest.programs, "programs", errors);
  for (const [key, program] of Object.entries(programs)) {
    const label = `programs.${key}`;
    if (!program || typeof program !== "object" || Array.isArray(program)) {
      errors.push(`${label} must be an object`);
      continue;
    }
    if (program.id !== key) errors.push(`${label}.id must match registry key`);
    if (!PROGRAM_KINDS.has(program.kind)) errors.push(`${label}.kind must be sfx or jingle`);
    const result = validateSteps(program.steps, label, voiceLimit, maxSteps, errors);
    const durationBudget = program.kind === "jingle"
      ? budgets.jingleMaxDurationSeconds
      : budgets.sfxMaxDurationSeconds;
    if (finiteNumber(durationBudget) && result.duration > durationBudget + 1e-9) {
      errors.push(`${label} duration ${result.duration.toFixed(6)}s exceeds ${durationBudget}s budget`);
    }
  }

  const cues = recordOrEmpty(manifest.bgmCues, "bgmCues", errors);
  for (const [key, cue] of Object.entries(cues)) {
    const label = `bgmCues.${key}`;
    if (!cue || typeof cue !== "object" || Array.isArray(cue)) {
      errors.push(`${label} must be an object`);
      continue;
    }
    if (cue.id !== key) errors.push(`${label}.id must match registry key`);
    requirePositive(cue.durationSeconds, `${label}.durationSeconds`, errors);
    requireNonNegative(cue.loopStartSeconds, `${label}.loopStartSeconds`, errors);
    requirePositive(cue.loopEndSeconds, `${label}.loopEndSeconds`, errors);
    if (finiteNumber(cue.loopStartSeconds) && finiteNumber(cue.loopEndSeconds) && cue.loopEndSeconds <= cue.loopStartSeconds) {
      errors.push(`${label} loop end must be greater than loop start`);
    }
    if (finiteNumber(cue.durationSeconds) && finiteNumber(cue.loopEndSeconds) && cue.loopEndSeconds > cue.durationSeconds + 1e-9) {
      errors.push(`${label} loop end exceeds cue duration`);
    }
    const loopDuration = finiteNumber(cue.loopStartSeconds) && finiteNumber(cue.loopEndSeconds)
      ? cue.loopEndSeconds - cue.loopStartSeconds
      : 0;
    if (finiteNumber(budgets.bgmLoopMaxDurationSeconds) && loopDuration > budgets.bgmLoopMaxDurationSeconds + 1e-9) {
      errors.push(`${label} loop duration ${loopDuration.toFixed(6)}s exceeds ${budgets.bgmLoopMaxDurationSeconds}s budget`);
    }
    const result = validateSteps(cue.steps, label, voiceLimit, Number.MAX_SAFE_INTEGER, errors);
    const maxTail = budgets.bgmLoopMaxTailSeconds;
    if (finiteNumber(cue.loopEndSeconds) && finiteNumber(maxTail)) {
      const tail = Math.max(0, result.duration - cue.loopEndSeconds);
      if (tail > maxTail + 1e-9) {
        errors.push(`${label} loop tail ${tail.toFixed(6)}s exceeds ${maxTail}s budget`);
      }
    }
  }

  const aliases = recordOrEmpty(manifest.aliases, "aliases", errors);
  const normalizedAliases = new Map();
  for (const [name, target] of Object.entries(aliases)) {
    let normalized;
    if (typeof target === "string") {
      normalized = { kind: "program", id: target };
    } else if (target && typeof target === "object" && !Array.isArray(target) &&
               new Set(["program", "cue"]).has(target.kind) &&
               typeof target.id === "string" && target.id) {
      normalized = { kind: target.kind, id: target.id };
    } else {
      errors.push(`aliases.${name} must be a program ID string or { kind: program|cue, id }`);
      continue;
    }
    normalizedAliases.set(name, normalized);
    if (normalized.kind === "program" && !programs[normalized.id]) {
      errors.push(`aliases.${name} targets missing program ${normalized.id}`);
    }
    if (normalized.kind === "cue" && !cues[normalized.id]) {
      errors.push(`aliases.${name} targets missing cue ${normalized.id}`);
    }
  }

  const reachablePrograms = new Set();
  const reachableCues = new Set();
  let audibleEventCount = 0;

  if (!Array.isArray(manifest.events)) {
    errors.push("events must be an array");
  } else {
    const names = new Set();
    manifest.events.forEach((event, index) => {
      const label = `events[${index}]`;
      if (!event || typeof event !== "object" || Array.isArray(event)) {
        errors.push(`${label} must be an object`);
        return;
      }
      if (typeof event.name !== "string" || !event.name) errors.push(`${label}.name must be a non-empty string`);
      if (names.has(event.name)) errors.push(`${label}.name duplicates ${event.name}`);
      names.add(event.name);
      if (!CLASSIFICATIONS.has(event.classification)) errors.push(`${label}.classification is invalid`);
      requireNonNegative(event.priority, `${label}.priority`, errors);
      if (event.classification === "none" && event.priority !== 0) {
        errors.push(`${label} none event priority must be 0`);
      }

      let direct;
      if ((event.classification === "sfx" || event.classification === "jingle") && programs[event.name]) {
        direct = { kind: "program", id: event.name };
      } else if (event.classification === "bgm" && cues[event.name]) {
        direct = { kind: "cue", id: event.name };
      } else if (event.classification === "none" && programs[event.name]) {
        direct = { kind: "program", id: event.name };
      } else if (event.classification === "none" && cues[event.name]) {
        direct = { kind: "cue", id: event.name };
      }
      const resolved = direct ?? normalizedAliases.get(event.name);
      if (event.classification !== "none" && CLASSIFICATIONS.has(event.classification)) audibleEventCount += 1;
      if (event.classification === "none" && resolved) {
        errors.push(`${label} is classified none but resolves to ${resolved.kind} ${resolved.id}`);
      }
      if (event.classification === "sfx" || event.classification === "jingle") {
        if (!resolved || resolved.kind !== "program" || !programs[resolved.id]) {
          errors.push(`${label} does not resolve to a program`);
        } else if (programs[resolved.id].kind !== event.classification) {
          errors.push(`${label} resolves to ${programs[resolved.id].kind}, expected ${event.classification}`);
        } else {
          reachablePrograms.add(resolved.id);
        }
      }
      if (event.classification === "bgm") {
        if (!resolved || resolved.kind !== "cue" || !cues[resolved.id]) {
          errors.push(`${label} does not resolve to a BGM cue`);
        } else {
          reachableCues.add(resolved.id);
        }
      }
    });
  }

  if (manifest.audioMode === "active" && audibleEventCount === 0) {
    errors.push("audioMode active requires at least one audible event");
  }
  if (manifest.audioMode === "silent") {
    if (Object.keys(programs).length || Object.keys(cues).length || Object.keys(aliases).length) {
      errors.push("audioMode silent must not define programs, cues, or aliases");
    }
    if (audibleEventCount > 0) errors.push("audioMode silent must not declare audible events");
  }

  for (const id of Object.keys(programs)) {
    if (!reachablePrograms.has(id)) warnings.push(`programs.${id} is unreachable from events`);
  }
  for (const id of Object.keys(cues)) {
    if (!reachableCues.has(id)) warnings.push(`bgmCues.${id} is unreachable from events`);
  }
  return { errors, warnings };
}

export function validateManifest(manifest) {
  return validateManifestDetailed(manifest).errors;
}

export function summarize(manifest) {
  const count = (value) => (value && typeof value === "object" && !Array.isArray(value) ? Object.keys(value).length : 0);
  const events = Array.isArray(manifest?.events) ? manifest.events : [];
  const byClass = {};
  for (const event of events) {
    const key = CLASSIFICATIONS.has(event?.classification) ? event.classification : "invalid";
    byClass[key] = (byClass[key] ?? 0) + 1;
  }
  return {
    mode: manifest?.audioMode ?? "?",
    profile: manifest?.hardwareProfile?.id ?? "?",
    fidelity: manifest?.hardwareProfile?.fidelity ?? "?",
    programs: count(manifest?.programs),
    cues: count(manifest?.bgmCues),
    events: events.length,
    byClass,
  };
}

/* Whether this file is being run as a command rather than imported. Both sides
 * are resolved through realpath first: an ESM module URL is symlink-resolved by
 * the loader while `process.argv[1]` is not, so comparing them raw makes the
 * script silently do nothing when it is invoked through a symlinked directory
 * -- a validator that exits 0 without validating, which is worse than one that
 * crashes. */
export function isDirectInvocation(argvPath, moduleUrl) {
  if (!argvPath || !moduleUrl) return false;
  const real = (p) => {
    try {
      return fs.realpathSync(p);
    } catch {
      return path.resolve(p);
    }
  };
  return real(argvPath) === real(fileURLToPath(moduleUrl));
}

function validFixture() {
  return {
    version: 1,
    audioMode: "active",
    hardwareProfile: { id: "test-four", fidelity: "era-inspired", voiceLimit: 4, primitives: ["pulse", "noise"] },
    budgets: { sfxMaxDurationSeconds: 0.6, jingleMaxDurationSeconds: 1.6, maxStepsPerProgram: 24, bgmLoopMaxDurationSeconds: 32, bgmLoopMaxTailSeconds: 0 },
    programs: {
      fire: { id: "fire", kind: "sfx", steps: [{ offset: 0, duration: 0.08, voice: "pulse1" }] },
      "jingle:start": { id: "jingle:start", kind: "jingle", steps: [{ offset: 0, duration: 0.2, voice: "pulse1" }] }
    },
    aliases: { "player:fire": "fire", start: "jingle:start", stage: { kind: "cue", id: "main" } },
    events: [
      { name: "player:fire", classification: "sfx", priority: 100 },
      { name: "start", classification: "jingle", priority: 60 },
      { name: "ui:focus", classification: "none", priority: 0 },
      { name: "stage", classification: "bgm", priority: 20 }
    ],
    bgmCues: {
      main: { id: "main", durationSeconds: 8, loopStartSeconds: 0, loopEndSeconds: 8, steps: [{ offset: 0, duration: 0.25, voice: "pulse1" }] }
    }
  };
}

function runSelfTest() {
  const validErrors = validateManifest(validFixture());
  if (validErrors.length) throw new Error(`valid fixture failed:\n${validErrors.join("\n")}`);
  const invalid = validFixture();
  invalid.programs.fire.steps[0].duration = 0.8;
  invalid.programs.fire.steps.push({ offset: 0.1, duration: 0.1, voice: "pulse1" });
  invalid.events.push({ name: "player:fire", classification: "sfx", priority: 100 });
  const invalidErrors = validateManifest(invalid);
  if (!invalidErrors.some((error) => error.includes("exceeds"))) throw new Error("self-test missed duration budget violation");
  if (!invalidErrors.some((error) => error.includes("duplicates"))) throw new Error("self-test missed duplicate event violation");
  if (!invalidErrors.some((error) => error.includes("overlaps voice"))) throw new Error("self-test missed per-voice overlap violation");

  const faithful = validFixture();
  faithful.hardwareProfile.fidelity = "hardware-faithful";
  if (!validateManifest(faithful).some((error) => error.includes("targetHardware"))) {
    throw new Error("self-test missed unnamed hardware-faithful target");
  }

  const tail = validFixture();
  tail.bgmCues.main.durationSeconds = 8.2;
  tail.bgmCues.main.steps.push({ offset: 7.9, duration: 0.2, voice: "pulse2" });
  if (!validateManifest(tail).some((error) => error.includes("loop tail"))) {
    throw new Error("self-test missed loop-tail budget violation");
  }

  const silent = validFixture();
  silent.audioMode = "silent";
  silent.programs = {};
  silent.aliases = {};
  silent.events = [{ name: "ui:focus", classification: "none", priority: 0 }];
  silent.bgmCues = {};
  if (validateManifest(silent).length) throw new Error("self-test rejected intentional silent kit");

  const emptyActive = validFixture();
  emptyActive.programs = {};
  emptyActive.aliases = {};
  emptyActive.events = [];
  emptyActive.bgmCues = {};
  if (!validateManifest(emptyActive).some((error) => error.includes("at least one audible event"))) {
    throw new Error("self-test accepted empty active kit");
  }

  const orphan = validFixture();
  orphan.programs.orphan = { id: "orphan", kind: "sfx", steps: [{ offset: 0, duration: 0.1, voice: "pulse2" }] };
  if (!validateManifestDetailed(orphan).warnings.some((warning) => warning.includes("orphan"))) {
    throw new Error("self-test missed unreachable program warning");
  }

  const malformedRegistries = validFixture();
  malformedRegistries.programs = [];
  malformedRegistries.bgmCues = [];
  malformedRegistries.aliases = [];
  const malformedRegistryErrors = validateManifest(malformedRegistries);
  for (const field of ["programs", "bgmCues", "aliases"]) {
    if (!malformedRegistryErrors.some((error) => error.includes(`${field} must be an object`))) {
      throw new Error(`self-test accepted a non-object ${field} registry`);
    }
  }

  const malformedProfile = validFixture();
  malformedProfile.hardwareProfile.voiceLimit = 1.5;
  malformedProfile.hardwareProfile.primitives = [7];
  const malformedProfileErrors = validateManifest(malformedProfile);
  if (!malformedProfileErrors.some((error) => error.includes("voiceLimit must be a positive integer"))) {
    throw new Error("self-test accepted a fractional voice limit");
  }
  if (!malformedProfileErrors.some((error) => error.includes("primitives[0]"))) {
    throw new Error("self-test accepted a non-string primitive");
  }

  const nonzeroNonePriority = validFixture();
  nonzeroNonePriority.events.find((event) => event.classification === "none").priority = 1;
  if (!validateManifest(nonzeroNonePriority).some((error) => error.includes("none event priority must be 0"))) {
    throw new Error("self-test accepted a nonzero priority for a none event");
  }

  const summary = summarize(validFixture());
  if (summary.programs !== 2 || summary.cues !== 1 || summary.events !== 4) {
    throw new Error("self-test found a summary that does not describe the fixture");
  }

  // The CLI guard. This file is commonly reached through a symlinked skills
  // directory, and a guard that fails there turns every run into a silent
  // exit 0 -- the one failure mode a validator must not have.
  const here = fileURLToPath(import.meta.url);
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "validate-audio-kit-"));
  try {
    const link = path.join(tmp, "linked.mjs");
    fs.symlinkSync(here, link);
    if (!isDirectInvocation(here, import.meta.url)) {
      throw new Error("self-test: direct invocation by real path was not recognised");
    }
    if (!isDirectInvocation(link, import.meta.url)) {
      throw new Error("self-test: invocation through a symlink was not recognised");
    }
    if (isDirectInvocation(path.join(tmp, "other.mjs"), import.meta.url)) {
      throw new Error("self-test: an unrelated path was treated as direct invocation");
    }
    if (isDirectInvocation(undefined, import.meta.url)) {
      throw new Error("self-test: a missing argv path was treated as direct invocation");
    }
  } finally {
    fs.rmSync(tmp, { recursive: true, force: true });
  }
  console.log("validate-audio-kit self-test passed");
}

function main(argv) {
  if (argv.includes("--self-test")) {
    runSelfTest();
    return;
  }
  const input = argv[0];
  if (!input || input === "--help" || input === "-h") {
    console.log("Usage: validate-audio-kit.mjs <manifest.json>\n       validate-audio-kit.mjs --self-test");
    process.exitCode = input ? 0 : 2;
    return;
  }
  const resolved = path.resolve(input);
  let manifest;
  try {
    manifest = JSON.parse(fs.readFileSync(resolved, "utf8"));
  } catch (error) {
    console.error(`Unable to read ${resolved}: ${error.message}`);
    process.exitCode = 2;
    return;
  }
  const { errors, warnings } = validateManifestDetailed(manifest);
  warnings.forEach((warning) => console.warn(`Audio kit warning: ${warning}`));
  if (errors.length) {
    console.error(`Audio kit validation failed (${errors.length}):`);
    errors.forEach((error) => console.error(`- ${error}`));
    process.exitCode = 1;
    return;
  }
  // Report what was actually checked. A bare "passed", or silence, cannot be
  // told apart from a run that validated nothing.
  const s = summarize(manifest);
  const classes = Object.entries(s.byClass)
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([k, n]) => `${k} ${n}`)
    .join(", ");
  console.log(
    `Audio kit validation passed: ${resolved}\n` +
      `  profile ${s.profile} (${s.fidelity}), mode ${s.mode}\n` +
      `  ${s.programs} programs, ${s.cues} cues, ${s.events} events [${classes || "none"}]` +
      (warnings.length ? `, ${warnings.length} warning(s)` : "")
  );
}

if (isDirectInvocation(process.argv[1], import.meta.url)) {
  main(process.argv.slice(2));
}
