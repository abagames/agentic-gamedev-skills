#!/usr/bin/env node
// Checks a frame manifest (see references/frame-manifest.md) for display defects:
// overlap, occluded, offscreen, small, faint, brief.
// Occlusion needs draw order (z). Without it, intersections are listed as REVIEW lines
// to inspect in the frame and do not fail the run.
// Usage: node check-screen-frames.mjs <manifest.json> | --self-test
import { readFileSync } from "node:fs";

const DEFAULTS = { glyphPx: 12, contrast: 3, briefBaseMs: 400, briefPerCharMs: 50 };
const READABLE = new Set(["text", "indicator"]);

function intersects(a, b) {
  return a[0] < b[0] + b[2] && b[0] < a[0] + a[2] && a[1] < b[1] + b[3] && b[1] < a[1] + a[3];
}

function luminance([r, g, b]) {
  const f = (v) => {
    const s = v / 255;
    return s <= 0.03928 ? s / 12.92 : ((s + 0.055) / 1.055) ** 2.4;
  };
  return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b);
}

function contrastRatio(fg, bg) {
  const a = luminance(fg);
  const b = luminance(bg);
  return (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05);
}

export function checkManifest(manifest) {
  if (!manifest || !manifest.viewport || !Array.isArray(manifest.frames)) {
    throw new Error("manifest needs viewport and frames[]");
  }
  const t = { ...DEFAULTS, ...(manifest.thresholds || {}) };
  const scale = manifest.minScale || 1;
  const view = [0, 0, manifest.viewport.w, manifest.viewport.h];
  const findings = [];
  const reviews = [];
  const counts = { frames: 0, elements: 0, pairs: 0, skipped: { small: 0, faint: 0, brief: 0 } };

  for (const frame of manifest.frames) {
    counts.frames++;
    const elements = frame.elements || [];
    const readable = elements.filter((e) => READABLE.has(e.kind));
    const panels = elements.filter((e) => e.kind === "panel" && e.opaque);
    const add = (check, element, detail) => findings.push({ frame: frame.id, check, element, detail });

    for (const e of readable) {
      counts.elements++;
      if (!Array.isArray(e.rect) || e.rect.length !== 4) {
        throw new Error(`frame ${frame.id}: element ${e.id} has no rect`);
      }
      const [x, y, w, h] = e.rect;
      if (x < view[0] || y < view[1] || x + w > view[2] || y + h > view[3]) {
        add("offscreen", e.id, `rect ${e.rect.join(",")} outside ${view[2]}x${view[3]}`);
      }
      for (const p of panels) {
        if (!intersects(e.rect, p.rect)) continue;
        const ordered = typeof e.z === "number" && typeof p.z === "number";
        if (ordered && p.z > e.z) {
          // Draw order is known: the later-drawn (higher z) one is on top.
          add("occluded", e.id, `under ${p.id} (z ${e.z} < ${p.z})`);
        } else if (!ordered || p.z === e.z) {
          // Draw order unknown or tied: rectangles alone cannot tell which is on top,
          // and being a panel's child does not guarantee being drawn after it.
          const why = ordered ? `same z ${e.z}` : "no z on both";
          const child = e.parent === p.id ? " (its parent)" : "";
          reviews.push({ frame: frame.id, check: "occlusion-candidate", element: e.id, detail: `intersects ${p.id}${child}; ${why}, inspect the frame` });
        }
      }
      if (typeof e.glyphH === "number") {
        const px = e.glyphH * scale;
        if (px < t.glyphPx) add("small", e.id, `${px}px glyph at scale ${scale}, floor ${t.glyphPx}px`);
      } else counts.skipped.small++;
      if (e.fg && e.bg) {
        const ratio = contrastRatio(e.fg, e.bg);
        if (ratio < t.contrast) add("faint", e.id, `contrast ${ratio.toFixed(2)}, floor ${t.contrast}`);
      } else counts.skipped.faint++;
      if (typeof e.visibleMs === "number") {
        const need = t.briefBaseMs + t.briefPerCharMs * (e.chars || 0);
        if (e.visibleMs < need) add("brief", e.id, `${e.visibleMs}ms visible, needs ${need}ms`);
      } else counts.skipped.brief++;
    }

    for (let i = 0; i < readable.length; i++) {
      for (let j = i + 1; j < readable.length; j++) {
        const a = readable[i];
        const b = readable[j];
        counts.pairs++;
        if (a.group && a.group === b.group) continue;
        if (intersects(a.rect, b.rect)) add("overlap", a.id, `with ${b.id}`);
      }
    }
  }
  return { findings, reviews, counts };
}

function report(source, { findings, reviews, counts }) {
  console.log(`read ${source}`);
  console.log(
    `checked ${counts.frames} frames, ${counts.elements} readable elements, ${counts.pairs} pairs; ` +
      `skipped small ${counts.skipped.small}, faint ${counts.skipped.faint}, brief ${counts.skipped.brief}`,
  );
  for (const f of findings) console.log(`FAIL ${f.check} | ${f.frame} | ${f.element} | ${f.detail}`);
  for (const r of reviews) console.log(`REVIEW ${r.check} | ${r.frame} | ${r.element} | ${r.detail}`);
  console.log(
    `${findings.length ? `${findings.length} finding(s)` : "no findings"}` +
      (reviews.length ? `; ${reviews.length} to inspect by eye` : ""),
  );
}

function selfTest() {
  const bad = {
    viewport: { w: 224, h: 256 },
    minScale: 2,
    frames: [
      {
        id: "bad",
        elements: [
          { id: "banner", kind: "text", rect: [60, 100, 104, 7], glyphH: 7 },
          { id: "notice", kind: "text", rect: [80, 102, 64, 7], glyphH: 7 },
          { id: "hud", kind: "panel", rect: [0, 0, 224, 24], opaque: true, z: 10 },
          { id: "popup", kind: "text", rect: [40, 18, 20, 7], glyphH: 7, z: 5 },
          { id: "buried-child", kind: "text", rect: [150, 4, 30, 7], glyphH: 7, z: 5, parent: "hud" },
          { id: "edge", kind: "text", rect: [215, 200, 20, 7], glyphH: 7 },
          { id: "tiny", kind: "text", rect: [10, 60, 20, 5], glyphH: 5 },
          { id: "line", kind: "indicator", rect: [10, 80, 40, 1], fg: [70, 70, 0], bg: [0, 0, 0] },
          { id: "flash", kind: "text", rect: [10, 120, 60, 7], glyphH: 7, visibleMs: 300, chars: 8 },
        ],
      },
    ],
  };
  const good = {
    viewport: { w: 224, h: 256 },
    minScale: 2,
    frames: [
      {
        id: "good",
        elements: [
          { id: "hud", kind: "panel", rect: [0, 0, 224, 24], opaque: true, z: 10 },
          { id: "hud:label", kind: "text", rect: [4, 4, 30, 7], glyphH: 7, parent: "hud", z: 11 },
          { id: "popup-on-top", kind: "text", rect: [100, 18, 20, 7], glyphH: 7, z: 20 },
          { id: "log", kind: "panel", rect: [0, 230, 224, 26], opaque: true },
          { id: "log:line", kind: "text", rect: [4, 234, 60, 7], glyphH: 7, parent: "log" },
          { id: "unordered", kind: "text", rect: [100, 236, 40, 7], glyphH: 7 },
          { id: "tied", kind: "text", rect: [180, 4, 30, 7], glyphH: 7, z: 10 },
          { id: "score:label", kind: "text", rect: [10, 40, 30, 7], glyphH: 7, group: "score" },
          { id: "score:value", kind: "text", rect: [10, 40, 60, 7], glyphH: 7, group: "score" },
          { id: "line", kind: "indicator", rect: [10, 80, 40, 2], fg: [255, 255, 0], bg: [0, 0, 0] },
          { id: "notice", kind: "text", rect: [10, 120, 60, 7], glyphH: 7, visibleMs: 2000, chars: 8 },
        ],
      },
    ],
  };
  const want = ["overlap", "occluded", "offscreen", "small", "faint", "brief"];
  const badResult = checkManifest(bad);
  const got = new Set(badResult.findings.map((f) => f.check));
  const missing = want.filter((c) => !got.has(c));
  const occluded = badResult.findings.filter((f) => f.check === "occluded").map((f) => f.element);
  const goodResult = checkManifest(good);
  const clean = goodResult.findings;
  const candidates = goodResult.reviews.map((r) => r.element);
  const problems = [];
  if (missing.length) problems.push(`missing ${missing.join(",")}`);
  if (clean.length) problems.push(`false positives ${clean.map((f) => `${f.check}:${f.element}`).join(",")}`);
  // Draw order: an element under a later-drawn panel is occluded even when it is that panel's child.
  if (!occluded.includes("popup") || !occluded.includes("buried-child")) problems.push("z-order occlusion not detected");
  // Whenever draw order is missing or tied the script must defer to inspection, children included.
  const expected = "log:line,tied,unordered";
  if ([...candidates].sort().join(",") !== expected) problems.push(`occlusion candidates were [${candidates.join(",")}], expected [${expected}]`);
  if (problems.length) {
    console.log(`self-test FAILED: ${problems.join("; ")}`);
    process.exit(1);
  }
  console.log(
    `self-test passed: detected ${want.join(", ")}; z-order respected in both directions; ` +
      "missing or tied order deferred to inspection, children included; clean manifest produced no findings",
  );
}

const arg = process.argv[2];
if (!arg) {
  console.error("usage: check-screen-frames.mjs <manifest.json> | --self-test");
  process.exit(2);
} else if (arg === "--self-test") {
  selfTest();
} else {
  const result = checkManifest(JSON.parse(readFileSync(arg, "utf8")));
  report(arg, result);
  process.exit(result.findings.length ? 1 : 0);
}
