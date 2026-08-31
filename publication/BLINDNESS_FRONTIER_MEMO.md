# Blindness Frontier: from arbitrary observations to stability margins

**Public research memo, 2026-08-30**
**Status:** two Lean-checked boundary results, one standard linear-algebra
translation, one rejected quantitative proposal, and one deliberately
unclaimed next question.

This memo records what survived an adversarial novelty audit.  It is not a
discovery announcement.  Its purpose is to turn a useful negative result into
a precise map of the next research boundary.

## The question

Let `q` be a target fact about a state and let `r_i` be observations.  A set
`S` of observations is **target-blind** when two states have different targets
but identical readings at every coordinate in `S`.

What patterns of blindness can occur, and which restrictions on observations
force those patterns to have useful structure?

## Result 1: unrestricted Boolean observations permit every pattern

For arbitrary Boolean observations, every downward-closed family of
coalitions can occur.  Given generators `F_j`, the explicit construction has
one target-false base state and one target-true state for each `F_j`, with

```text
S is blind  <->  there exists j with S contained in F_j.
```

For a finite simplicial complex, choose its maximal faces as the generators.
The blind coalitions are exactly its faces.

This is useful as a no-go theorem: topology alone cannot reveal a universal
information law when the observation language is unrestricted.  Any positive
classification must come from additional probabilistic, algebraic,
geometric, causal, or computational structure.

Lean identifiers:

- `NewMathDiscovery.BlindnessRealization.blind_iff_below_generator`
- `NewMathDiscovery.BlindnessRealization.blind_downward`

Historical novelty is not claimed.  The construction is close to standard
Dowker-complex, simple-game, and functional-dependency machinery.

## Result 2: subtraction-preserving observations collapse blindness to kernels

Suppose the state and value types admit subtraction, and every selected
observation and the target preserve it.  Then

```text
two states agree on S but differ on q

        if and only if

there is a direction d with r_i(d) = 0 for every i in S, but q(d) != 0.
```

Equivalently,

```text
S determines q  <->  intersection(kernel r_i, i in S) is contained in kernel q.
```

Lean identifiers:

- `NewMathDiscovery.LinearBlindness.pairBlind_iff_kernelWitness`
- `NewMathDiscovery.LinearBlindness.determinesTarget_iff_kernel_inclusion`
- `NewMathDiscovery.LinearBlindness.pairBlind_downward`

The Lean interface is intentionally weaker than a vector space: it uses only
the subtraction laws needed by the proof.

For finitely many linear functionals over a field, ordinary linear algebra
then gives

```text
S determines q  <->  q belongs to span {r_i : i in S}.
```

That finite linear case is established territory.  It is a representable
matroid port, and its positive coalitions are exactly the accepting sets of a
monotone span program.  The relevant lineage includes
[Karchmer--Wigderson span programs](https://www.math.ias.edu/~avi/PUBLICATIONS/MYPAPERS/KW93/proc.pdf),
[Brickell--Davenport ideal secret sharing](https://doi.org/10.1007/BF00196772),
and [Seymour's secret-sharing matroids](https://doi.org/10.1016/0095-8956(92)90007-K).

This is a successful classification but not new mathematics.  Its value here
is as a translation rule: unrestricted blindness complexes become matroid
closure, circuits, ports, and field-dependent representability as soon as the
observations are linear.

## A proposed next invariant failed

A natural quantitative idea was to score a blind coalition by how large the
target can remain on a unit vector in its common observation kernel.  For a
fixed real inner product this is the distance from `q` to the selected span.
Optimizing that score while preserving only the represented matroid is
ill-posed.

The exact counterexample family uses target row

```text
q = (1, 0)
```

and sensor rows

```text
r_n = (1, n + 1).
```

Every two distinct rows have nonzero determinant.  Thus the target together
with any fixed-size finite block of sensors represents the same uniform
rank-two matroid.  But

```text
d_n = (n + 1, -1)
```

lies in the kernel of `r_n`, while `q(d_n) = n + 1`.  In the projective chart
whose second coordinate is `-1`, these blind directions approach the target
axis.  Choose later and later blocks `r_N, ..., r_(N+k-1)` for any fixed `k`:
all their blind directions degenerate simultaneously while all rows remain
pairwise independent.  Equivalently, after Euclidean normalization every
target value approaches its maximum, even though the sensors approach mutual
parallelism.  The naive minimum-over-coalitions objective therefore rewards
approaching a different matroid.

Lean identifiers for the exact integer core:

- `NewMathDiscovery.LinearBlindness.RankTwoInstability.target_sensor_minor`
- `NewMathDiscovery.LinearBlindness.RankTwoInstability.distinct_sensor_minor`
- `NewMathDiscovery.LinearBlindness.RankTwoInstability.witness_in_sensor_kernel`
- `NewMathDiscovery.LinearBlindness.RankTwoInstability.target_nonzero_on_witness`
- `NewMathDiscovery.LinearBlindness.RankTwoInstability.unbounded_target_on_gauge_fixed_kernel`
- `NewMathDiscovery.LinearBlindness.RankTwoInstability.tail_witnesses_uniformly_large`

The projective-limit interpretation is not formalized in Lean; the
determinants, kernel identities, and unbounded gauge-fixed witnesses are.

This failure also overlaps known quantitative languages.  Distances to spans
occur in [approximate span programs](https://arxiv.org/abs/1507.00432),
matroid realization spaces are encoded by
[slack matrices](https://arxiv.org/abs/1804.05264), and representation
sensitivity is measured by
[circuit imbalance](https://arxiv.org/abs/2108.03616).  No novelty claim
survives for the naive radius.

## The remaining kill-or-repair question

The narrow question worth one bounded trial is whether a **global incidence
margin** gives a useful perturbation theorem for target blindness.

For a normalized real representation `R`, let `alpha_H` be a normal to each
represented hyperplane `H`, and define

```text
Delta(R) = min over H and e not in H of
           |alpha_H dot r_e| / (norm alpha_H * norm r_e).
```

Unlike the rejected target-only score, `Delta` checks every non-incidence and
therefore detects the rank-two degeneration above.  But it is close to the
existing matroid slack-matrix and condition-number literature.  It is a test
target, not a proposed new invariant.

The trial has three acceptance gates:

1. Prove that perturbations smaller than an explicit function of `Delta(R)`
   preserve the blindness/access structure.
2. On one small rank-three representation, show that the bound predicts the
   actual first incidence change rather than merely restating it.
3. Identify a target-specific consequence not already supplied by standard
   slack margins, circuit imbalance, or span-program approximation.

If any gate fails, park the direction.  The next search should then change the
observation class, not rename another known condition number.

## Claim matrix

| Claim | Status | Evidence | Novelty status |
|---|---|---|---|
| Every generated downward-closed Boolean blindness family is realizable | Proved | Lean construction | Useful packaging; historical novelty not established |
| Linear blindness is exactly a common-kernel witness | Proved | Lean theorem | Standard algebraic fact in this formulation |
| Finite linear determinacy is matroid/span-program closure | Established corollary; not separately formalized here | Linear algebra and cited literature | Prior art |
| A target-only robustness optimum is meaningful at fixed matroid | Rejected | Lean-checked rank-two degeneration plus paper-level normalization argument | False as proposed |
| A global slack margin yields a distinct blindness theory | Open trial | No theorem yet | Unproven and not claimed novel |

## A compact interface for future systems

The reusable output is a three-column contract, not a new mathematical
language:

| Observation class | Canonical invariant | Failure certificate |
|---|---|---|
| Arbitrary Boolean | Downward-closed family / relation complex | Opposite-target state pair |
| Linear | Kernel inclusion / matroid closure | Common-kernel direction |
| Quantitative linear | Incidence or conditioning margin | Near-zero non-incidence slack |

This lets either a human or an automated prover route a proposed theorem to
the right mature theory, demand the right witness when it fails, and avoid
mistaking a change of vocabulary for a discovery.

## Reproduction

From the repository root:

```powershell
lake env lean lean\NewMathDiscovery\BlindnessRealization.lean
lake env lean lean\NewMathDiscovery\LinearBlindness.lean
```

The public review route is the draft pull request
[`Sodelin/new-math-discovery#2`](https://github.com/Sodelin/new-math-discovery/pull/2)
and the cross-project audit issue
[`Sodelin/ai-math-discovery#3`](https://github.com/Sodelin/ai-math-discovery/issues/3).
