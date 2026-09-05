# Failure Modes

Read this before publishing a `collapse` or `illegible` verdict, and whenever a run returns a
surprising result — the majority of surprising results from this instrument are protocol artifacts,
not design findings. Also worth a pass when adapting the protocol to a new genre.

Each entry names the artifact and the control that neutralizes it.

## Protocol errors that invert the result

- **Outcome leak.** Showing `t+Δfwd` during stage A. The judge then reads the answer off the future
  and the whole gate becomes a description exercise — it will pass almost any build. This is the
  single most damaging error available, which is why the withholding rule is stated in `SKILL.md`
  rather than here. Control: the follow-up frame is never in the stage-A payload.

- **Scoring an unconditional oracle against a conditional prediction.** The revealed frame followed
  the recorded run's input, not the judge's plan. Scoring the judge's plan against it marks correct
  reasoning as wrong and can push a legible game to `illegible`. Control: score question 4 only.

- **Δ mismatched to the action cycle.** Δback too small makes the lead-in pair a still and
  reintroduces the motion blindness the triplet exists to fix; Δfwd shorter than one cycle reveals
  nothing scorable, so every prediction "matches" and the oracle stops discriminating. Control:
  derive both from a recorded action-cycle estimate.

## Sampling artifacts

- **Sampler-caused collapse.** An idle or one-key run visits one regime, every scene looks alike,
  and the design is blamed for the driver's behavior. Control: the coverage precheck, and
  `inadmissible-sample` as a first-class verdict.

- **Capability assumed rather than checked.** A tool covers part of the capture contract and is read
  as covering all of it — most commonly, a project assuming headless tooling can produce frames when
  it renders nothing. Control: C1–C3 are checked and their route recorded per project, never
  inherited from a citation.

- **Skilled track read as first contact.** A GA-driven sample is optimized play; treating its
  legibility result as what a new player sees overstates the game. Control: the naive track and the
  entry-point verdict.

- **Naive-track collapse reported as design collapse.** The naive driver has a limited repertoire of
  its own, so low divergence there is confounded. Control: only a skilled track may carry `collapse`;
  a naive run reports `collapse-not-measurable`.

- **Assumed replay contract.** The searched track is played into the rendered build without checking
  that it reproduces the search-run states, so the frames show a different run than the one searched —
  and nothing about them looks wrong. Control: fingerprint comparison at every sampled tick before
  any frame is graded.

- **Missing frame capture worked around inside the gate run.** Reconstructing frames from simulated state,
  or hand-approximating the GA track, to avoid losing the skilled track. Control: the documented
  fallback — record directly against the rendered build and report `collapse` as not measurable.

- **Driver fitness leaking into a verdict.** A GA's score is used as evidence that the design is good.
  It is a search signal about coverage and nothing else. Control: the search boundary is stated in
  `SKILL.md` and the validation list checks for it.

- **Judge-driven run.** The judging agent chose the situations it then grades, so the divergence
  number measures its own policy rather than the game's situation space. Control: the driver is a
  scripted track, a separate exploratory policy, or a human, and the source is recorded.

- **Curated sample.** Screens hand-picked by someone who knows the design show the intended variety
  by construction. Control: only fixed-interval or pre-declared-enumeration sampling is admissible.

- **Sample re-rolled after a bad result.** Re-seeding until the number improves converts the gate
  into a demonstration. Control: sampling method and seed fixed and recorded before results are
  seen; a disappointing result is a finding, not a reason to re-sample.

- **Scene count mistaken for observation count.** Eight autocorrelated scenes from one run read as
  eight independent observations. Control: collapse requires n ≥ 3 independent runs.

## Grader-side artifacts

- **Shared grader across scenes.** One session judging all scenes anchors on its first answer and
  reports false agreement — or, noticing it is repeating itself, deliberately varies its answers and
  reports false variety. Both directions destroy the divergence metric. Control: one isolated
  grader per scene.

- **Author grading.** Anyone who has read the design, source, or spec knows the answer and cannot
  produce a blind reading. Disqualification is permanent, not per case. Control: graders are freshly
  spawned and the orchestrator never forwards project context.

- **Firewall leak by convenience.** Handing the grader a repository path "so it can see the build"
  hands it the source. Control: copy frames into a bare directory with neutral case ids.

- **Title leak.** A game's name very often states its goal outright, and titles hide in filenames,
  the window title bar or host-page title, the launcher or shell wrapper, and any visible attract or
  title frame. Control: strip all of these before capture, and check one captured frame by eye.

- **Uncontrolled pass.** No degraded control has ever been run, so fluent grader prose is mistaken
  for a legible screen. Control: the degraded control at first use and after any protocol change.

## Interpretation errors

- **Prototype pass carried forward as shipping-build readability.** The design-layer conclusions
  transfer; legibility at the shipped resolution, palette, and scale does not. Control: the artifact
  type is recorded in every verdict, and a material presentation change requires a re-run.

- **Conflating the instruments.** "Does variety emerge over continued play" answered from pictures
  as if it were the question a balance harness answers. This instrument yields an upper bound on
  situation variety only. Control: `spread` is documented as licensing nothing, and the balance
  sweep still runs.

- **Fixing the key after the fact.** Rewriting the intended goal, or adding an action class to the
  intended list, so that it matches what the graders said. This destroys the ground truth the whole
  procedure exists to provide. Control: the key is frozen before any answer is read, and
  unanticipated action classes are flagged as findings rather than absorbed.

- **Verdict without a named visual element.** "The goal did not read" with nothing pointed at is not
  actionable and usually means the miss was not analyzed. Control: every miss cites the specific
  element that was absent, ambiguous, or out-competed by something louder.

- **Folding an implementation gap into a legibility verdict.** Non-positional state that was never
  drawn makes the game illegible in a trivial sense that says nothing about visual direction.
  Control: report it as an implementation gap and void the affected scene's verdict.
