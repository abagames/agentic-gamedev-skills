#!/usr/bin/env node
import {
  parseArgs,
  pickBackgroundHex,
  requirePaths,
  runConvert,
} from "./common.mjs";

function printHelp() {
  console.log(`Usage:
  node cutout.mjs <input> <output> [--sample corners] [--fuzz 8%] [--trim]

Options:
  --sample   Background sample point: corners | tl | tr | bl | br
  --fuzz     ImageMagick fuzz threshold. Default: 8%
  --trim     Trim transparent margins after cutout
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

  const backgroundHex = pickBackgroundHex(input, options.sample ?? "corners");
  const args = [
    input,
    "-alpha",
    "set",
    "-fuzz",
    options.fuzz ?? "8%",
    "-transparent",
    backgroundHex,
  ];

  if (options.trim) {
    args.push("-trim", "+repage");
  }

  args.push(output);
  runConvert(args, "Cutout conversion failed");

  console.log(JSON.stringify({ input, output, backgroundHex, fuzz: options.fuzz ?? "8%", trimmed: options.trim === true }, null, 2));
}

main();
