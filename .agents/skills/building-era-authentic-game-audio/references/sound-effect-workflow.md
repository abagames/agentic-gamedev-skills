# Sound-Effect and Jingle Workflow

Use this when the integrated audio system includes SEs or jingles. Design the set around game
meaning and collision behavior rather than filling a fixed preset catalogue.

## 1. Define the event target

For each audible event, record its function, expected repetition rate, priority, competing
sounds, and one-line sonic target. Keep `none` explicit when silence communicates the event
better. Distinguish immediate control feedback, causal consequences, warnings, rewards, and
rare state changes before choosing timbre.

## 2. Choose a contour and texture

Select the smallest contour that communicates the event: impulse, gated tone, pitch sweep,
short sequence, noise burst, layered impact, warning pulse, or compact phrase. These are
non-exhaustive functional families, not mandatory templates. Combine or omit them when the
game and hardware profile justify it.

Assign each sibling sound a distinct region in at least two useful dimensions such as onset,
duration, pitch/register, contour, noise content, rhythm, or repetition pattern. Preserve a
shared cabinet identity through the fixed primitive set, master chain, and bounded parameter
ranges.

## 3. Author deterministic program data

Encode occupied voice intervals, envelopes, pitch/noise motion, and optional variation in data
when the host permits it. Own seeds at the kit or session boundary. Vary features that are
audible but non-semantic; keep warning direction, success/failure contour, timing, and event
identity stable unless gameplay explicitly changes their meaning.

Treat duration and step caps as starting budgets, not creative ceilings. Override a cap in the
frozen profile when a longer alarm, speech-like cadence, sustained state sound, or elaborate
jingle is necessary, then test its repetition and arbitration cost.

## 4. Tune the sibling kit under load

Audition repeated actions and dense collisions, not only isolated sounds. Shorten, retrigger,
coalesce, duck, or drop according to the bus policy. Keep essential control and danger feedback
readable before reward, ambience, and BGM ornament. Verify that rare jingles remain state
punctuation rather than accidental background music.

## 5. Validate identity and variation

Check representative seeds and gameplay states for duration, voice use, deterministic replay,
repeat caps, sibling confusion, painful stacking, and loss of event identity. Reject both
inaudible randomization and variations that reverse or obscure semantic cues.
