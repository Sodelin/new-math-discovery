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
no proof holes.

`RG-CERT-0/v0` supplies the first audited concrete checker and static partial
graph. All 1,905 listed edges pass F4--F7: one structural even-input edge,
1,903 Route B odd-cylinder edges, and one exact stopped-map repair for
\(n=3\). Exact F3 checking finds 145 uncovered source residues modulo 4,096.
The bundle therefore fails the global gate and remains proof-construction
infrastructure rather than a Collatz resolution.

`RG-MACRO-001` supplies an exact formula-level description of the same finite
frontier.  Its fixed grammar reconstructs all 1,903 Route B affine targets and
the same 145-cylinder complement without invoking the archived reverse
search.  It also proves an exact binary refinement of each gap into one child
preserving the maximal endpoint exponent and one child incrementing it.  No
finite transition closure or globally decreasing rank follows from that
refinement.

`RG-TRANS-001` supplies the missing transition closure as a global five-row
parametric table.  Four terminal/soft rows stop or coalesce with a smaller
integer; the fifth is one closed hard state type with return map \(F\).
Every positive integer, and in particular every instance of the 145 affine
gaps, enters exactly one row.  The table is not a finite-state automaton:
its natural parameters are unbounded.  Termination of \(F\) is equivalent to
Collatz, so the independent well-founded rank required for progress remains
missing.

`RG-RANK-OBS-001` supplies a universal exact obstruction at that progress
boundary.  Between every ordered pair of distinct hard labels it constructs
hard returns from replay quotient zero to any prescribed target quotient.
The resulting two-way zero-quotient feature transitions rule out every rank
factoring only through \((\text{hard label},Q)\), with any well-founded
codomain.  It does not rule out ranks using the full parameter or augmented
state, so `R1` remains active.

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

For the static RG-CERT-0 graph, every serialized edge is universally valid and
the incompleteness boundary is exact.  RG-TRANS-001 gives global parametric
transition coverage, and RG-RANK-OBS-001 eliminates one broad rank-factor
class.  No globally ranked F1--F7 graph, richer recursive rank, or Collatz
conclusion is claimed.

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
| Concrete F1--F7 checker | Implemented for RG-CERT-0/v0 |
| Concrete globally covering graph | Missing; 145 F3 residue gaps |
| External specialist review | Pending |

## RG-CERT-0 gates

| Gate | Result |
|---|---|
| Schema-to-F1--F7 audit | Passed after three specification repairs |
| Dependency-free checker self-test | Passed |
| Static bundle edge audit | 1,905 edges passed F4--F7 |
| Exact F3 source coverage | Incomplete on 145 residues modulo 4,096 |
| Stopped-map boundary at \(1\) | Repaired explicitly for \(n=3\) |
| Independent deterministic rebuild | Byte-identical |
| Hostile malformed-data mutations | Rejected; no false global PASS |
| Optimized-mode false-PASS test | Passed; fails closed |
| `--require-global` gate | Correctly exits nonzero |
| Global RG-CERT-0 certificate | Missing |

## RG-MACRO-001 gates

| Gate | Result |
|---|---|
| One-bit affine refinement theorem | Proved exactly |
| Closed form for \(O(EO)^kEEO\) | Proved with necessary-and-sufficient parity guards |
| Formula-only reconstruction | Exact match on all 1,903 Route B edges |
| Exact complement | 145 cylinders, matching RG-CERT-0 |
| Stopped-map lower bounds | Reconstructed exactly |
| Gap-child identities | 290/290 passed exact coefficient comparison |
| Independent derivation and hostile-data audit | Passed |
| Optimized-mode false-PASS test | Passed; fails closed |
| Authoritative RG-CERT-0 companion audit | Passed; remains explicitly partial |
| Finite parametric transition closure | Supplied separately by RG-TRANS-001 |
| Rank decrease across all gap successors | Missing |
| Global Collatz consequence | None |

## RG-TRANS-001 gates

| Gate | Result |
|---|---|
| Unique global canonical labels | Proved |
| Terminal/soft guard partition | Exhaustive; exact smaller coalescences |
| Soft normalizer | Terminates by strict numerical decrease |
| Hard-family return | Closed exact coalescence transition |
| Entry of all 145 RG-CERT-0 gaps | Proved by odd-affine valuation cells |
| Collatz-equivalence boundary | Proved in both directions |
| Independent mathematical audit | Passed after two local repairs |
| Bounded exact-integer identity diagnostic | Passed through 10,000 |
| Well-founded rank on every hard return | Missing; sole active construction gate |
| Global Collatz consequence | None |

## RG-RANK-OBS-001 gates

| Gate | Result |
|---|---|
| Exact successor ray for every ordered hard-label pair | Proved |
| Arbitrary target replay quotient | Proved in the exact form \(D=(h+2)q\) |
| Source replay quotient on every distinct-label construction | Exactly zero |
| Rank-factor obstruction | Proved for every codomain with a well-founded relation |
| Boundary cases and two numerical examples | Passed independent exact audit |
| Independent mathematical and scope audit | Passed after one projected-graph wording repair |
| Full-parameter or augmented-state ranks | Not ruled out |
| Global Collatz consequence | None |
