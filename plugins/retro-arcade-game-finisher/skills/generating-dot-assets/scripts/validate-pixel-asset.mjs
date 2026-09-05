#!/usr/bin/env node
import {
  parseArgs,
  parsePositiveInteger,
  parseSize,
  runConvert,
  runIdentify,
} from "./common.mjs";

function printHelp() {
  console.log(`Usage:
  node validate-pixel-asset.mjs <input> --size WxH [--max-colors 32] [--transparent-corners]

Options:
  --size     Required final image size, for example 64x64
  --max-colors  Optional maximum color count
  --transparent-corners  Require all four corners to have alpha 0
  --help     Show this message
`);
}

function getCornerAlpha(input, corner) {
  const pointByCorner = {
    tl: "0,0",
    tr: "w-1,0",
    bl: "0,h-1",
    br: "w-1,h-1",
  };
  const raw = runConvert(
    [
      input,
      "-alpha",
      "extract",
      "-format",
      `%[fx:int(255*p{${pointByCorner[corner]}}.r)]`,
      "info:",
    ],
    `Failed to sample ${corner} alpha`,
  );
  return Number.parseInt(raw, 10);
}

function main() {
  const { positional, options } = parseArgs(process.argv.slice(2));
  if (options.help) {
    printHelp();
    return;
  }

  const input = positional[0];
  if (!input) {
    throw new Error("Input path is required.");
  }
  const expected = parseSize(options.size);
  const maxColors = parsePositiveInteger(options["max-colors"], "--max-colors");

  const raw = runIdentify(["-format", "%w %h %[channels] %k", input], "Failed to identify image");
  const [widthRaw, heightRaw, channelsRaw, colorsRaw] = raw.split(/\s+/);
  const width = Number.parseInt(widthRaw, 10);
  const height = Number.parseInt(heightRaw, 10);
  const colors = Number.parseInt(colorsRaw, 10);
  const channels = channelsRaw;
  const errors = [];

  if (width !== expected.width || height !== expected.height) {
    errors.push(`Expected ${expected.width}x${expected.height}, got ${width}x${height}`);
  }
  if (!/a/i.test(channels)) {
    errors.push(`Expected alpha channel, got channels: ${channels}`);
  }
  if (maxColors != null && colors > maxColors) {
    errors.push(`Expected at most ${maxColors} colors, got ${colors}`);
  }

  if (options["transparent-corners"]) {
    const corners = ["tl", "tr", "bl", "br"].map((corner) => getCornerAlpha(input, corner));
    const transparent = corners.every((alpha) => alpha === 0);
    if (!transparent) {
      errors.push(`Expected transparent corners; alpha-corner samples were ${corners.join(", ")}`);
    }
  }

  if (errors.length > 0) {
    console.error(JSON.stringify({ input, ok: false, width, height, channels, colors, errors }, null, 2));
    process.exit(1);
  }

  console.log(JSON.stringify({ input, ok: true, width, height, channels, colors }, null, 2));
}

main();
