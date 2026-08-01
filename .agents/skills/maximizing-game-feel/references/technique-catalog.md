# Game-Feel Technique Catalog

Load the relevant technique sections after identifying weak gameplay moments and the game's expressive register.

## Contents

- Squash and stretch
- Tilt and rotation
- Eyes and focal direction
- Particles and trails
- Easing and secondary motion
- Hit flash and hit stop
- Camera response
- Knockback and recoil
- Engine notes

## Squash and stretch

- Stretch vertically at jump start and squash horizontally on landing; use restrained idle breathing only in a register that supports it.
- Squash movable enemies or obstacles on impact and return them to rest.
- Do not deform fixed walls or rooted spikes as though they landed. Use a flash or particle response instead.
- Never let presentation deformation silently change or misrepresent authoritative collision geometry.

## Tilt and rotation

- Lean moving objects from velocity or acceleration and return them to neutral.
- Spin or tilt mobile enemies and rolling hazards in proportion to motion.
- Use rotation to telegraph charging, aiming, alert, or defeat even when an object does not translate.
- Fixed scenery without an active state needs no motion merely for liveliness.

## Eyes and focal direction

- Add eyes only in a character/playful register and only when readable at actual screen size.
- Aim pupils toward movement, input direction, or the current target.
- Consider any agentive player, enemy, companion, collectible, or projectile; omit faces from inert obstacles unless the fiction intentionally gives them agency.
- In abstract or serious games, express direction through orientation, a leading edge, or a focal highlight.

## Particles and trails

- Use dust for jump, landing, dash, and stop; sparks or fragments for hits, wall bounces, destruction, and spawn; glints for rewards.
- Use color and density to distinguish gentle motion, danger, and reward.
- Give afterimages only to fast movement where the trail clarifies a trajectory. Trails on slow objects read as smears.
- Cap simultaneous particles and trail samples, especially on mobile or Web export.

## Easing and secondary motion

- Use ease-out for arrivals, ease-in for departures, and bounded overshoot for snap.
- Add readable anticipation before important actions and follow-through afterward.
- Let dependent visual parts lag slightly to imply connected mass.
- Telegraph enemy attacks before they become dangerous; let defeats settle instead of snapping.
- For an activating fixed hazard, animate the activation wind-up rather than inventing locomotion.

## Hit flash and hit stop

- Flash a damaged visual to a bright tint for roughly 1–3 frames and restore it fully.
- Keep flashes short enough to preserve the hazard silhouette; prevent repeated hits from producing unreadable strobing.
- Use hit stop only for meaningful impact. Scale it from one or two frames for light impact to several for rare heavy or finishing events.
- Freeze presentation or the involved objects while retaining queued input. Calm or flow-focused games may omit hit stop.

## Camera response

- Prefer a directional kick opposite impact or along firing direction over random jitter.
- Decay displacement to zero quickly; reserve the largest response for rare events.
- Use a small zoom punch when shake would reduce readability.
- Cap displacement so the player and hazards remain spatially legible during precision play.

## Knockback and recoil

- Push a struck visual along the hit direction and give the attacker a smaller opposite recoil.
- Add a short weapon kick when firing when it supports the register.
- Keep gameplay displacement authoritative and intentional. Do not push the player into danger solely for feel.
- Use less knockback for heavier movable objects; fixed obstacles should answer through flash, particles, or camera response.

## Engine notes

### crisp-game-lib

Drawing is collision geometry, so render-only deformation is not generally available. Prefer color/flash, particles, sound, and camera-style feedback that leave gameplay shapes intact. If a gameplay shape is deformed, keep its collision silhouette honest.

- Use `bar(..., angle)` or `line()` for rotated forms; there is no general transform stack. Rotation `0` points right and positive angles rotate clockwise. For an upward-facing object, use `-PI / 2` as the base angle and add the tilt offset.
- Call `color(...)` before `particle(...)`; particle color comes from current draw color.
- Use the current object-form particle arguments.

### General 2D engines

Apply squash and tilt to a visual child or presentation component while leaving collision state authoritative. Use engine-native particles, pooled sprites, or ghost images according to the project's performance budget.

### Godot

Keep `CollisionShape2D` authoritative and apply deformation, flash, and trails under a visual child such as `VisualRoot`. Prefer small local scripts (`player_feel`, `hazard_feel`, `reward_feel`) for mini-games. For Web export, cap trails and particles and prefer light or pooled effects when needed.
