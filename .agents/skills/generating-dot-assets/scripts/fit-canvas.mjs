#!/usr/bin/env node
import {
  parseArgs,
  parseSize,
  requirePaths,
  runConvert,
} from "./common.mjs";

function printHelp() {
  console.log(`Usage:
  node fit-canvas.mjs <input> <output> --size WxH [--fit contain|stretch|none] [--gravity center]

Options:
  --size     Required final canvas size, for example 64x64
  --fit      contain (default), stretch, or none
  --gravity  ImageMagick gravity. Default: center
  --help     Show this message
`);
}

function main() {
  const { positional, options } = parseArgs(process.argv.slice(2));
  if (options.help) {
    printHelp();
    return;
  }

  const [input, output] = positional;
  requirePaths(input, output);
  const { width, height } = parseSize(options.size);
  const fit = options.fit ?? "contain";
  const gravity = options.gravity ?? "center";
  const size = `${width}x${height}`;

  const args = [input, "-background", "none"];
  if (fit === "contain") {
    args.push("-filter", "point", "-resize", `${size}>`);
  } else if (fit === "stretch") {
    args.push("-filter", "point", "-resize", `${size}!`);
  } else if (fit !== "none") {
    throw new Error("--fit must be contain, stretch, or none.");
  }

  args.push("-gravity", gravity, "-extent", size, output);
  runConvert(args, "Fit canvas failed");

  console.log(JSON.stringify({ input, output, size, fit, gravity }, null, 2));
}

main();
