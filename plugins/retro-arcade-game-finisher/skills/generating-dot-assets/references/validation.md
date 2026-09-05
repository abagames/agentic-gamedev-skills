# Validation

Run `scripts/validate-pixel-asset.mjs` for checks the tool can decide:

- dimensions exactly match requested `WxH`
- PNG has an alpha channel
- all four corners are transparent when `--transparent-corners` is requested
- color count does not exceed `--max-colors` when supplied

Then inspect every final asset for checks that require visual judgment:

- subject is not cropped
- no visible chroma-key fringe
- silhouette and important details remain readable at final size

If the design asks for a color range such as 16–24 colors, enforce the upper bound with
`--max-colors` and treat the lower bound as a visual acceptance check for sufficient detail.

If validation fails, fix the pipeline step rather than accepting the file.
