---
name: generating-semantic-game-mutants
description: "Injects controlled, game-specific semantic defects — timing/order, identity and lifecycle, scoring and economy, persistence/save, RNG/determinism, input buffering, animation-gameplay sync, content/configuration — into a game or its trace reducer, and records a withheld manifest of intended defect mechanism, precondition, expected symptom, violated invariant, hidden oracle, equivalent-mutant risk, and a clean-control counterpart, so the detection power of a test suite or of an agent repair workflow can be measured against known-planted defects. Use when measuring whether tests or an agent workflow actually catch gameplay defects, when building known-bad fixtures for a with-skill / without-skill comparison, or when checking that a workflow does not \"fix\" a healthy build. Not for finding unknown defects in a real build, not for repairing defects, and not for balance tuning."
---

# Generating Semantic Game Mutants

## Purpose

Measure what a test suite or an agent workflow actually catches, by planting defects whose ground
truth you hold. Without planted defects, a suite's detection rate is unknown: green means "no
defect was found", which is indistinguishable from "no defect was looked for".

The defects here are **semantic and game-specific** — a scoring guard removed, an identity reused
across a pool boundary, a field dropped from a save. Generic syntactic mutation (flip `<` to `<=`,
delete a statement) mostly produces crashes and dead code, which any suite catches, inflating the
score without measuring anything about gameplay.

## What This Measures — Pick One Before Starting

These are different experiments with different setups. Running one and reporting another is the
main way this instrument produces a wrong number.

| Goal | Subject | Passing means | Additional setup |
| --- | --- | --- | --- |
| **Suite detection** | An existing test suite | The suite goes red on the mutant | Run the suite directly; no subagent or clean control is required |
| **Workflow repair** | An agent + a workflow | The agent localizes and restores the invariant | Withhold the manifest and use an isolated working copy |
| **With / without comparison** | The same agent, two instruction sets | Repair-rate difference across matched task sets | Keep agent conditions and prompts matched; use enough independent tasks to support the claim |
| **Over-repair control** | An agent, on a healthy build | The agent changes nothing semantically | Present a clean control exactly like a defect case |

## When to Use

- Before trusting a suite or a workflow that has never been measured against known-bad input.
- When comparing two instruction sets and a real difference has to be separated from noise.
- When building an evaluation fixture set for repeated use.

## When Not to Use

- Hunting unknown defects in a real build. Opposite direction.
- Repairing anything. This skill only plants and records.
- Balance or difficulty tuning.
- As a quality metric on its own. A mutation score is a property of the mutant set as much as of the
  suite; a set built from operators your code cannot express produces a flattering number.

## Procedure

1. **Choose the measurement goal** from the table above and write it down. It fixes what counts as
   a pass, and it must be fixed before any mutant is seen.

2. **Pick operators across families.** The catalog is in `references/mutation-families.md`. Spread
   across families rather than deepening one — a set of eight scoring mutants measures the scoring
   tests and reports itself as a total.

3. **Write the manifest entry before applying the operator.** Fields and rules are in
   `references/mutant-manifest.md`. Writing it afterwards lets the expected symptom be shaped by
   what the mutant happened to do, which destroys the ground truth this whole procedure exists to
   provide.

4. **Emit each mutant as a standalone artifact.** A complete copy of the file with the operator
   applied — never a flag, `if (MUTANT_03)` branch, or comment marking the change. Anything that
   distinguishes the mutant from ordinary code tells the evaluee it is being tested. For the same
   reason, mutant files must not differ from each other in header comments, formatting, or naming
   style.

5. **Screen for equivalent mutants and keep them separate.** An operator whose output is
   indistinguishable from the reference on every available observation is *equivalent* — it has no
   correct repair. Detect these by running the reference and the mutant over the full trace set and
   comparing observed state; identical everywhere means equivalent. **Do not put equivalent mutants
   in the pass/fail pool.** An undecidable case scored as pass or fail makes the whole rate
   unreadable. Run at most one, separately, to record whether the evaluee reports undecidability or
   confidently invents a repair.

6. **Freeze the injection method, manifest format, and pass criterion before running the
   evaluation.** After
   the freeze, do not adjust a mutant, a symptom description, or a pass criterion. Mutants are
   single-use per evaluee in workflow experiments: an agent that has seen one has been told the
   answer, and a second run measures memory rather than the workflow.

7. **Apply the setup for the selected goal.**
   - **Suite detection:** run the existing suite on each non-equivalent mutant. A subprocess or
     isolated agent adds no evidence unless the suite itself requires one.
   - **Workflow repair:** hide the manifest and reference diff, and investigate in an isolated
     working environment.
   - **With / without comparison:** keep the agent, model/settings, prompt, tools, and task
     presentation the same across arms. Use comparable task sets and do not keep, revise, or delete
     a skill on the strength of one case.
   - **Over-repair control:** build a behaviorally clean copy with the same neutral presentation as
     defect cases, and score only whether the evaluee makes a semantic change.
   - **Workflow revision followed by remeasurement:** prepare unused reserve mutants before the
     revision. Never present a spent case as a fresh measurement after changing the workflow.

## Information Isolation

For workflow repair, with/without comparison, and over-repair control, the manifest is the answer
key. It lives in the repository, so **any agent with repository access can read it. File placement
is not a firewall.** Isolation is procedural:

- Run each evaluation in a separate isolated agent/session or equivalent fresh environment. One
  mutant per environment — the first case's findings contaminate the second's localization.
- Give the evaluee a **working copy outside the fixture directory**, containing only the mutated
  source, the traces, and any instructions under test. Do not hand it a repository path from which
  the reference, the other mutants, or the manifest is reachable.
- Never pass: the manifest, the mutation site, the operator name, the reference diff, the fact that
  this is a mutant at all, or any other case's result.
- **Say nothing different on the clean control run.** Telling the evaluee "this one might be fine"
  is telling it the answer; the control only works when it is indistinguishable from a defect run.
- Ask for investigation, not repair: "investigate this symptom, fix it if a fix is warranted, and
  report your evidence." An instruction to fix removes the "nothing is wrong" answer, which is the
  only output the over-repair control can measure.

## Judging

- **Judge by restored behavior and invariants, never by diff equality with the reference.** A
  different correct repair is a pass. An identical-looking repair that leaves an oracle failing is
  not.
- Score the clean control as pass **only if nothing changed semantically**. A plausible-sounding
  change to healthy code is the failure this control exists to catch, and it is more serious than a
  missed defect: a workflow that misses a bug wastes a run, one that damages healthy code costs
  trust in every green result it ever produced.
- Record per case: whether localization reached the right site, which layer it stopped at, whether a
  change was made, how complete the returned evidence was, and how many round trips it took.
- Report failures as observations. Do not soften a fixture, add hints to a symptom description, or
  relax a criterion after seeing a result — each of those converts a measurement into a
  demonstration.

## Bundled Fixture

`assets/fixtures/` holds a runnable instance of this whole structure: a pure reducer, eight event
traces an evaluee is given, six more that exist only for scoring, an invariant checker, and thirteen
standalone artifacts: nine defects across five families, two clean controls, and two equivalent
mutants.

```bash
cd assets/fixtures
node check.mjs                  # reference: invariants and complete finals match, exit 0
node check.mjs mutants/m01.mjs  # exit 1 with the first violating step
node check.mjs mutants/m09.mjs traces-scoring.json   # scoring set; needed for the withheld tapes
```

`check.mjs` reports, per trace, the final state and the **first** step at which each invariant
fails. It also compares the complete final state with the bundled clean reducer, so missing effects
that never create an illegal intermediate state still fail. It derives its verdict from executions
and never inspects the candidate reducer source, so it scores a repair it has never seen.

One defect, `m09`, is unreachable from `traces.json` on purpose: an evaluee that only folds the
tapes it was handed cannot see it. Score repairs against `traces-scoring.json`; several other
mutants also gain additional coverage there. Both it and `check.mjs` are answer key
alongside `references/fixture-manifest.md`; none of the three goes into a working copy.

**What this fixture can and cannot measure.** Each mutant is a single ~135-line reducer that a
capable evaluee reads end to end in one pass, so localization is nearly free and most arms converge
on a repair. That makes the fixture suitable for **suite detection** — where the subject is a test
suite, not a reader — and for the **over-repair control**, where reading the whole file is exactly
what should stop a change to healthy code. It is a weak instrument for **with / without
comparison**: when both arms repair everything, a null result measures the fixture's size, not the
instructions under test. Before claiming an instruction set makes no difference, confirm the arms
were separated by something other than reading effort. To measure that comparison, build mutants
whose site is not visible from a single readable file — defects split across modules, reachable
only through a specific tape, or observable only in an aggregate the evaluee must construct.

## Validation

- The measurement goal and pass criterion were fixed before injection.
- Every mutant has a manifest entry written before injection.
- No mutant is distinguishable from ordinary code by inspection of the file alone.
- Equivalent mutants are identified and excluded from the pass/fail pool.
- **Suite detection:** the suite was run directly on each scored mutant; no agent isolation, clean
  control, or reserve pool is required.
- **Workflow repair:** each evaluee lacked manifest and reference access and worked in isolation.
- **With / without comparison:** arms used matched agent conditions, prompts, tools, and comparable
  task sets; conclusions reflect repeated cases rather than one result.
- **Over-repair control:** a behaviorally clean artifact was presented under the identical protocol
  and remained semantically unchanged.
- **Remeasurement after workflow revision:** only unused reserve mutants count as fresh evidence.

## References

- `references/mutation-families.md` — operator catalog by family.
- `references/mutant-manifest.md` — manifest schema and the rules that keep it usable as ground truth.
- `references/fixture-manifest.md` — the bundled fixture's answer key. Withhold from evaluees.
