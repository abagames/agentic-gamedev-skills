// Game core reducer.
// Pure: reduce(prev, event) returns a new state and never mutates prev.
// Deterministic: no clock, no RNG, no I/O.

export const HP_MAX = 3;
export const ENERGY_MAX = 5;
export const IFRAME_TICKS = 30;
export const TAP_COST = 1;
export const STRIKE_SCORE = 10;
export const ENERGY_REGEN_EVERY = 10;
export const CHARGE_MIN = 5;
export const POWER_COST = 2;
export const POWER_SCORE = 25;

export function initialState() {
  return {
    tick: 0,
    score: 0,
    hp: HP_MAX,
    energy: ENERGY_MAX,
    iframesUntil: -1,
    nextUid: 1,
    slots: {},
    charging: false,
    chargeStart: -1,
    saved: null,
  };
}

const copy = (s) => JSON.parse(JSON.stringify(s));

export function reduce(prev, ev) {
  const s = copy(prev);
  switch (ev.type) {
    case "tick":
      s.tick += 1;
      if (s.energy < ENERGY_MAX && s.tick % ENERGY_REGEN_EVERY === 0) s.energy += 1;
      break;

    case "spawn":
      s.slots[ev.slot] = { uid: s.nextUid, alive: true, scored: false };
      s.nextUid += 1;
      break;

    case "despawn":
      delete s.slots[ev.slot];
      break;

    case "tap":
      if (s.energy < TAP_COST) break;
      s.energy -= TAP_COST;
      s.iframesUntil = s.tick + IFRAME_TICKS;
      break;

    case "strike": {
      const e = s.slots[ev.slot];
      if (!e || !e.alive || e.scored) break;
      e.alive = false;
      e.scored = true;
      s.score += STRIKE_SCORE;
      break;
    }

    case "charge":
      if (s.charging) break;
      s.charging = true;
      s.chargeStart = s.tick;
      break;

    case "release": {
      if (!s.charging) break;
      const held = s.tick - s.chargeStart;
      s.charging = false;
      s.chargeStart = -1;
      if (held < CHARGE_MIN) break;
      const target = s.slots[ev.slot];
      if (!target || !target.alive || target.scored) break;
      if (s.energy < POWER_COST) break;
      s.energy -= POWER_COST;
      target.alive = false;
      target.scored = true;
      s.score += POWER_SCORE;
      break;
    }

    case "hazard":
      if (s.tick < s.iframesUntil) break;
      s.hp -= 1;
      s.iframesUntil = s.tick + IFRAME_TICKS;
      break;

    case "save":
      s.saved = {
        tick: s.tick,
        score: s.score,
        hp: s.hp,
        energy: s.energy,
        iframesUntil: s.iframesUntil,
        nextUid: s.nextUid,
        slots: copy(s.slots),
        charging: s.charging,
        chargeStart: s.chargeStart,
      };
      break;

    case "load": {
      if (!s.saved) break;
      const d = s.saved;
      s.tick = d.tick;
      s.score = d.score;
      s.hp = d.hp;
      s.energy = d.energy;
      s.iframesUntil = d.iframesUntil;
      s.nextUid = d.nextUid;
      s.slots = copy(d.slots);
      s.charging = d.charging;
      s.chargeStart = d.chargeStart;
      break;
    }

    default:
      break;
  }
  return s;
}

export function run(trace, init) {
  let cur = init === undefined ? initialState() : init;
  const states = [cur];
  for (const ev of trace) {
    cur = reduce(cur, ev);
    states.push(cur);
  }
  return { final: cur, states };
}
