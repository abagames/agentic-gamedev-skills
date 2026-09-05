import { mkdtempSync, readFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { spawnSync } from "node:child_process";

export function parseArgs(argv) {
  const positional = [];
  const options = {};

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (!arg.startsWith("--")) {
      positional.push(arg);
      continue;
    }

    const key = arg.slice(2);
    if (["trim", "help", "transparent-corners"].includes(key)) {
      options[key] = true;
      continue;
    }

    const value = argv[i + 1];
    if (!value || value.startsWith("--")) {
      throw new Error(`Missing value for --${key}`);
    }
    options[key] = value;
    i += 1;
  }

  return { positional, options };
}

export function requirePaths(input, output) {
  if (!input || !output) {
    throw new Error("Input and output paths are required.");
  }
}

export function run(command, args, context) {
  const result = spawnSync(command, args, { encoding: "utf8" });
  if (result.status !== 0) {
    const stderr = result.stderr?.trim() || `${command} exited with status ${result.status}`;
    throw new Error(`${context}: ${stderr}`);
  }
  return result.stdout?.trim() ?? "";
}

export function runConvert(args, context) {
  return run("convert", args, context);
}

export function runIdentify(args, context) {
  return run("identify", args, context);
}

export function parsePositiveInteger(raw, flag) {
  if (raw == null) {
    return undefined;
  }
  const parsed = Number.parseInt(raw, 10);
  if (!Number.isInteger(parsed) || parsed <= 0) {
    throw new Error(`${flag} must be a positive integer.`);
  }
  return parsed;
}

export function parseSize(raw) {
  const match = /^(\d+)x(\d+)$/i.exec(raw ?? "");
  if (!match) {
    throw new Error("--size must use WxH format, for example 64x64.");
  }
  return {
    width: parsePositiveInteger(match[1], "--size width"),
    height: parsePositiveInteger(match[2], "--size height"),
  };
}

export function parsePercent(raw, flag) {
  if (raw == null) {
    return undefined;
  }
  const parsed = Number.parseFloat(raw);
  if (!Number.isFinite(parsed) || parsed < 0 || parsed > 100) {
    throw new Error(`${flag} must be a number between 0 and 100.`);
  }
  return parsed;
}

export function parseDither(raw) {
  if (raw == null) {
    return true;
  }
  return !["0", "false", "off", "none"].includes(String(raw).trim().toLowerCase());
}

export function normalizeHex(value) {
  const hex = String(value).replace(/^#/, "").trim();
  if (!/^[0-9a-fA-F]{6}$/.test(hex)) {
    throw new Error(`Invalid hex color: ${value}`);
  }
  return `#${hex.toUpperCase()}`;
}

export function getCornerHex(input, corner) {
  const pointByCorner = {
    tl: "0,0",
    tr: "w-1,0",
    bl: "0,h-1",
    br: "w-1,h-1",
  };
  const output = runConvert(
    [input, "-format", `%[hex:p{${pointByCorner[corner]}}]`, "info:"],
    `Failed to sample ${corner} corner`,
  );
  return normalizeHex(output);
}

export function pickBackgroundHex(input, sampleMode = "corners") {
  if (["tl", "tr", "bl", "br"].includes(sampleMode)) {
    return getCornerHex(input, sampleMode);
  }

  const corners = ["tl", "tr", "bl", "br"].map((corner) => getCornerHex(input, corner));
  const counts = new Map();
  for (const hex of corners) {
    counts.set(hex, (counts.get(hex) ?? 0) + 1);
  }

  let winner = corners[0];
  let bestCount = 0;
  for (const [hex, count] of counts.entries()) {
    if (count > bestCount) {
      winner = hex;
      bestCount = count;
    }
  }
  return winner;
}

export function readPaletteHexes(path) {
  const parsed = JSON.parse(readFileSync(path, "utf8"));
  if (!Array.isArray(parsed.colors) || parsed.colors.length === 0) {
    throw new Error(`Palette file must contain a non-empty colors array: ${path}`);
  }
  return parsed.colors.map((value) => normalizeHex(value));
}

export function withTempDir(fn) {
  const dir = mkdtempSync(join(tmpdir(), "dot-asset-generator-"));
  try {
    return fn(dir);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
}

export function buildPaletteImage(tempDir, hexes) {
  const palettePath = join(tempDir, "palette.png");
  const args = hexes.flatMap((hex) => [`xc:${hex}`]);
  runConvert([...args, "+append", palettePath], "Failed to build palette image");
  return palettePath;
}
