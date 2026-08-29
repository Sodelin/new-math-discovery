# Status

## Current verdict

`H-FCS-001` is a reconstructed theorem candidate with a complete human proof
in [THEOREM.md](THEOREM.md). Its cycle/lift and freezing/horizon halves passed
separate internal adversarial reconstructions. The exact verifier passed an
independent reproducibility review, including a fail-closed optimized-mode
test. The theorem has not received external specialist review and has not been
formalized in a proof assistant.

The Collatz conjecture remains unresolved.

`RG-SOUND-001` now supplies the audited human certificate semantics for a
ranked coalescence graph. Its abstract soundness kernel compiles in Lean with
no proof holes. No finite graph satisfying F1--F7 has been constructed, so
this is proof infrastructure rather than a Collatz resolution.

## Claim classification

- **Claim type:** class-wide method obstruction.
- **Positive content:** arbitrarily deep positive-integer shadows of an
  infinite, pairwise-disjoint family of repelling rational cycles defeat every
  finite-fixed-center corrected-log potential at every fixed horizon fraction
  \(0<\beta<1\).
- **Not claimed:** Collatz convergence, Collatz divergence, a positive cycle,
  a divergent positive orbit, or impossibility of all ranking functions.
- **Software role:** exact diagnostics only; the infinite theorem must stand
  on the written proof.
- **Review status:** internal mathematical and reproducibility gates passed;
  external specialist review pending.

## Promotion gates

Internal package gates:

| Gate | Result |
|---|---|
| Rational-cycle algebra and pairwise disjointness | Passed |
| Endpoint-exact arbitrary-depth positive lift | Passed |
| Sensor-freezing and horizon uniformity | Passed |
| Dependency-free exact diagnostic run | Passed |
| Optimized-mode false-PASS test | Passed; fails closed |
| Collatz-resolution scope boundary | Passed internally |
| External specialist review | Pending |
| Proof-assistant formalization | Not attempted |

## RG-SOUND-001 gates

| Gate | Result |
|---|---|
| Stopped-map tail and coalescence lemmas | Passed independent audit |
| Well-founded ranked soundness proof | Passed independent audit |
| F1--F7 finite-interface typing/checkability | Passed after repair |
| Core Lean build | Passed on pinned Lean 4.33.1 |
| Lean axiom audit | Standard axioms only; no `sorryAx` |
| Concrete globally covering graph | Missing |
| Concrete F1--F7 checker | Not yet implemented |
| External specialist review | Pending |
