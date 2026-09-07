# Portfolio Output

For every selected concept include:

- **Name / id**
- **Core loop** — one sentence.
- **Why retained** — the structural hypothesis or portfolio role it represents.
- **Key decision / decision contrast** — name the state read and competing alternatives, then give two reachable states where different actions should be preferred for different reasons; if unavailable, write `not yet shown`.
- **Strongest evidence** — trace, simulation, prototype observation, human evidence, or explicitly `none yet`.
- **Primary risk** — strongest known weakness or dependency.
- **Unresolved question** — one falsifiable question that matters before commitment.
- **Smallest next test** — cheapest prototype, paper trace, simulator, telemetry probe, or short human test that can answer it.

Then add:

- **Coverage note** — how the portfolio differs in operation, topology, information, risk coupling, or skill channel.
- **Discarded clusters** — only materially important duplicate or hard-failure groups, with reasons.
- **Prototype order** — if requested, order by expected information gain per implementation cost rather than speculative fun ranking.
- **Human review** — use [human-review.md](human-review.md) before material implementation or publication investment; unattended work may finish with `status: review_pending`.
