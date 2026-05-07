# Validation

Check every final asset:

- dimensions exactly match requested `WxH`
- PNG has an alpha channel
- all four corners are transparent when `--transparent-corners` is requested
- subject is not cropped
- no visible chroma-key fringe
- color count is within the intended range when a color limit or palette is used

If validation fails, fix the pipeline step rather than accepting the file.
