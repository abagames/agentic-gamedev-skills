# Moment Catalogue

Use this to enumerate what to capture. Take only rows the game has. Each row names the defect that
moment tends to hide.

## Transient text

| Moment | Typical defect |
|---|---|
| Score popup at each source (kill, pickup, delivery, bonus) | Drifts under a HUD panel; several stack into an unreadable pile |
| Popup anchored to an object at each screen edge | Clipped or off-screen |
| Popup during the busiest effect stack | Lost among particles of the same colour |
| Notice for each rare event (extend, loss, rule change) | Overwritten by a banner on the same frame |
| Countdown in its last seconds | Same size and colour as when nothing is urgent |

## Coincidences to force

| Pair | How it arises |
|---|---|
| Round clear + extend | The clear bonus itself crosses the extend threshold |
| Round clear + miss | The last target and the player are destroyed on one frame |
| Extend + death sequence | Score from an already-launched shot arrives after the miss |
| Two notices from independent systems | A loss notice and a reward notice in the same second |
| New high score + end-of-run banner | Both drawn on the terminal screen |

## Indicators

| Moment | Typical defect |
|---|---|
| Warning or prediction line at its dimmest frame | Dimmer than decorative dots or the starfield |
| Indicator over the most crowded part of the field | Same colour as the things it crosses |
| Aim or landing marker while the player's finger or sprite covers it | Hidden by the thing it describes |
| Indicator in a mode where it should be absent (attract, pause, end screen) | Left over from the last run |

## HUD

| Moment | Typical defect |
|---|---|
| Each counter at the instant it changes | Changes with nothing connecting it to its cause |
| Lives display through a death sequence | Count changes with no matching grant or loss event |
| Counter at its maximum width (largest score, most lives) | Overflows into its neighbour; icons plus a multiplier read as a larger number |
| Multiplier or bonus that persists between phases | Shown only inside the phase, so its persistence is unknown |
| A draining value the player is meant to race | Not shown at all until it is paid out |

## Screens

| Moment | Typical defect |
|---|---|
| Title | Explains controls but not the one rule a player cannot guess |
| Attract demo | Shows title text or a table over the play it is meant to show |
| Every terminal screen | Player still blinking as invulnerable; play state still animating |
| Name entry at each cursor extreme | Cursor or DEL/END cells overlap or leave the frame |
| Smallest supported display scale, portrait and landscape | Text below a readable size; playfield under the thumb |
