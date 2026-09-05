#!/usr/bin/env node
import {
  buildPaletteImage,
  parseArgs,
  parseDither,
  parsePercent,
  parsePositiveInteger,
  readPaletteHexes,
  requirePaths,
  runConvert,
  withTempDir,
} from "./common.mjs";
import { join } from "node:path";

function printHelp() {
  console.log(`Usage:
  node pixelize.mjs <input> <output> [--width 96] [--height 64] [--colors 24] [--palette palette.json] [--dither off] [--dither-strength 25]

Options:
  --width     Output width before final canvas fitting
  --height    Output height before final canvas fitting
  --colors    Color limit when palette is not specified. Default: 24
  --palette   Palette JSON with a colors array
  --dither    Use Floyd-Steinberg dithering unless set to off/false/0
  --dither-strength  Blend amount for dithering, 0 to 100
  --help      Show this message
`);
}

function resizeSpec(width, height) {
  if (width && height) {
    return `${width}x${height}`;
  }
  if (width) {
    return `${width}x`;
  }
  if (height) {
    return `x${height}`;
  }
  return undefined;
}

function main() {
  const { positional, options } = parseArgs(process.argv.slice(2));
  if (options.help) {
    printHelp();
    return;
  }

  const [input, output] = positional;
  requirePaths(input, output);

  const width = parsePositiveInteger(options.width, "--width");
  const height = parsePositiveInteger(options.height, "--height");
  const colors = parsePositiveInteger(options.colors ?? "24", "--colors") ?? 24;
  const useDither = parseDither(options.dither);
  const requestedStrength = parsePercent(options["dither-strength"], "--dither-strength");
  const ditherStrength = useDither ? requestedStrength ?? 100 : 0;

  withTempDir((tempDir) => {
    const resizedPath = join(tempDir, "resized.png");
    const resizeArgs = [input];
    const requestedResize = resizeSpec(width, height);
    if (requestedResize) {
      resizeArgs.push("-filter", "point", "-resize", requestedResize);
    }
    resizeArgs.push(resizedPath);
    runConvert(resizeArgs, "Resize step failed");

    const noDitherPath = join(tempDir, "quantized-no-dither.png");
    const fullDitherPath = join(tempDir, "quantized-full-dither.png");
    const blendedPath = join(tempDir, "quantized-blended.png");
    const quantizedPath = join(tempDir, "quantized-final.png");

    let paletteImage;
    if (options.palette) {
      paletteImage = buildPaletteImage(tempDir, readPaletteHexes(options.palette));
      runConvert([resizedPath, "+dither", "-remap", paletteImage, noDitherPath], "Non-dithered palette remap failed");
      runConvert([resizedPath, "-dither", "FloydSteinberg", "-remap", paletteImage, fullDitherPath], "Dithered palette remap failed");
    } else {
      runConvert([resizedPath, "+dither", "-colors", String(colors), noDitherPath], "Non-dithered quantization failed");
      runConvert([resizedPath, "-dither", "FloydSteinberg", "-colors", String(colors), fullDitherPath], "Dithered quantization failed");
    }

    if (ditherStrength <= 0) {
      runConvert([noDitherPath, blendedPath], "Failed to keep non-dithered image");
    } else if (ditherStrength >= 100) {
      runConvert([fullDitherPath, blendedPath], "Failed to keep dithered image");
    } else {
      runConvert([noDitherPath, fullDitherPath, "-compose", "blend", "-define", `compose:args=${ditherStrength}`, "-composite", blendedPath], "Failed to blend dither strength");
    }

    const finalArgs = [blendedPath];
    if (paletteImage) {
      finalArgs.push("+dither", "-remap", paletteImage);
    } else {
      finalArgs.push("+dither", "-colors", String(colors));
    }
    finalArgs.push(quantizedPath);
    runConvert(finalArgs, "Pixelize conversion failed");

    runConvert([
      quantizedPath,
      "(",
      resizedPath,
      "-alpha",
      "extract",
      ")",
      "-compose",
      "copyopacity",
      "-composite",
      output,
    ], "Failed to restore source alpha");
  });

  console.log(JSON.stringify({ input, output, width: width ?? null, height: height ?? null, colors: options.palette ? null : colors, palette: options.palette ?? null, dither: useDither, ditherStrength }, null, 2));
}

main();
