# Global construction program

## 1. Completion condition

The primary construction target is a finite, human-reviewable certificate
whose exact checker discharges F1--F7 of
[RG-SOUND-001.md](RG-SOUND-001.md). Completion means all of the following,
with no uncovered branch:

1. every positive integer has an entry configuration;
2. every nonterminal configuration has an exact finite stopped-Collatz edge;
3. every edge is source/target closed and symbolically replayable;
4. every edge strictly decreases one fixed well-founded rank; and
5. the static data, checker, proof correspondence, and transcript pass an
   independent hostile audit.

A decreasing percentage of unresolved residues, any fixed computation bound,
or termination of an equivalent rewrite system without a new rank proof does
not meet this condition.

## 2. Current exact frontier

The published baseline is [RG-CERT-0.md](RG-CERT-0.md). Its single `root`
node uses

\[
\delta(p)=p+1,
\qquad
\rho(p)=p.
\]

The retained \(K=12\) bundle has 1,905 universally valid edges:

- one edge for every even decoded input;
- 1,903 exact smaller-target Route B cylinder edges; and
- one stopped-map singleton repair for \(n=3\).

Exact F3 checking leaves 145 source residues modulo 4,096. The complete list
and one witness per residue are retained in
[`verification/rg_cert0_route_b_check_output.txt`](verification/rg_cert0_route_b_check_output.txt).
These are the only active RG-CERT-0 construction gaps.

The archived structural diagnostic partitions the 145 odd cylinders by the
power \(3^s\) in their maximal uniform endpoint slope:

| Endpoint exponent \(s\) | Unresolved cylinders |
|---:|---:|
| 8 | 38 |
| 9 | 60 |
| 10 | 36 |
| 11 | 10 |
| 12 | 1 |

The unique \(s=12\) cylinder is the Mersenne residue \(R=4095\). The table is
an exact classification of this bounded certificate frontier, not a Collatz
invariant.

[RG-MACRO-001.md](RG-MACRO-001.md) now gives an exact symbolic description of
this frontier without invoking the archived breadth-first search.  The 1,903
Route B edges use only empty, `O`, and

\[
w_k=O(EO)^kEEO,
\qquad 1\le k\le6.
\]

The closed inverse formula and its necessary-and-sufficient affine guards
reproduce every selected target and leave exactly the same 145 complementary
cylinders.  The note also proves the universal one-bit child formula: every
maximal endpoint \(3^s x+B\) refines into exactly one exponent-\(s\) child and
one exponent-\(s+1\) child.  This completes the `T1` description gate.  It
does not prove that the refined children form a finite closed state system.

One-bit bounded-search refinement from \(K=12\) to \(K=13\) gives 18
low-resolved/high-unresolved parents, 27 low-unresolved/high-resolved parents,
and 100 parents with both children still unresolved. At longer horizons the
raw survivor bitmask develops substantially more signatures. Therefore the
bitmask itself is not the state language to promote.

Source provenance for these diagnostics remains in the accepted archive:

- [survivor structure](https://github.com/Sodelin/Collatz-Conjecture-Work/blob/2e7eae2bb998b14e5443e6c440154130a0049467/verification/round7_survivor_structure_output_2026-08-23.txt);
- [finite-horizon signatures](https://github.com/Sodelin/Collatz-Conjecture-Work/blob/2e7eae2bb998b14e5443e6c440154130a0049467/verification/round7_survivor_language_signatures_output_2026-08-23.txt).

## 3. Architectures already filtered out

The next search must supply a new mechanism relative to each blocker below.

### B1. More of the same bounded one-shot search

The current search leaves unresolved families at every tested modulus.
Increasing \(K\), inverse depth, or a state cap remains diagnostic only. It
does not establish a finite cover.

### B2. Unrefined whole-family inverse words

For the Mersenne family

\[
M_K(x)=2^K(x+1)-1,
\]

every uniformly admissible one-shot inverse word has leading coefficient at
least \(2^K\). Equality only reconstructs the original family. A reopened
route must refine the parameter or use a genuinely stronger semantic class.

### B3. The audited affine replay-debt rank

Lower-bounded affine combinations of label depth, parameter bitlength, and
the audited replay-debt variables cannot rank every hard successor. The exact
guarded transition

\[
17{,}184{,}927\longrightarrow97{,}873{,}535
\]

recharges all candidates in that class. A successor rank must use genuinely
richer state or a nonlinear well-founded order.

### B4. Representation without progress

The known finite mixed binary/ternary rewrite system is an exact Collatz
representation, but its universal termination is equivalent to Collatz.
Encoding the 145 gaps in that grammar is useful only if a new coalescence
macro or independently checked rank is added.

The detailed blocker proofs remain linked from
[PROVENANCE.md](PROVENANCE.md) and the archive failure ledger. None of these
filters rules out all recursive graphs or all well-founded ranks.

## 4. Active theorem target: RG-TRANS-001

The next mathematical deliverable is not a larger sweep. It is the following
finite transition theorem.

> **RG-TRANS-001 target.** Exhibit finitely many symbolic states and exact
> guarded macros covering every continuation of the 145 RG-CERT-0 gaps, such
> that every macro either coalesces with a uniformly smaller positive start or
> moves to another state while strictly decreasing an explicit well-founded
> rank. Cover every canonical boundary instance, including the Mersenne
> high-child chain and parameter value zero.

The transition theorem must answer four separate questions:

1. **State sufficiency:** which finite carry/mixed-radix data determine the
   next macro and its guards?
2. **Exactness:** what affine or mixed-radix identity proves the macro for the
   entire parameter domain?
3. **Coverage:** why do the guards form an exhaustive partition rather than a
   bounded sample?
4. **Progress:** what smaller target or well-founded rank handles every edge,
   especially cross-label recharge?

Until all four answers exist, there is no reason to implement RG-CERT-1.

## 5. Ranked candidate policy

A rank candidate is admitted to a full search cycle only if it is:

- defined without stopping time, convergence, or an unbounded future search;
- natural-, ordinal-, or other explicitly well-founded-valued;
- decidable by a small trusted checker or finite proof objects;
- tested first on the Mersenne refinement
  \(M_K(2y+1)=M_{K+1}(y)\);
- tested on the canonical boundary \(y=0\); and
- strictly decreasing on the concrete recharge transition above.

Promising classes include nonlinear lexicographic, multiset, or ordinal
measures on a finite mixed-radix state. Their names alone are not mechanisms:
each must come with a universal decrease formula for every guarded successor.

## 6. Canonical backlog

This table is the single active backlog for the construction program.

| ID | Deliverable | Dependency | Status | Promotion test |
|---|---|---|---|---|
| `C0` | RG-CERT-0 schema, checker, and static \(K=12\) boundary | RG-SOUND-001 | Published | Hostile audit passed |
| `T1` | Exact symbolic features for the 145 gaps | C0 | Completed | RG-MACRO-001 formulas reproduce all 145 without using “search miss” as a state invariant |
| `T2` | Finite guarded child/successor transition table | T1 | Active | Universal guard partition and exact identities |
| `R1` | First rank or smaller-target mechanism for every T2 edge | T2 | Pending | Passes B1--B4 kill tests |
| `S1` | RG-CERT-1 language and checker correspondence | T2, R1 | Pending | Independent specification audit |
| `G1` | Static globally covering certificate | S1 | Pending | `--require-global` succeeds and F1--F7 audit passes |

Only `T2` may consume exploratory computation now, and every proposed state
must be a quotient of the exact RG-MACRO-001 coefficient/guard data rather
than a raw finite-horizon miss bitmask. Schema/checker work starts only after
a rank mechanism survives its kill tests.

## 7. Work and review discipline

Each work item has one producer and then one independent reviewer. Parallel
tasks are permitted only when they modify disjoint artifacts and have an
explicit dependency-independent purpose.

Every proposed reopening must record:

- the old blocker;
- the new mechanism;
- why the mechanism lies outside the blocked class;
- the first falsification test; and
- the exact theorem target.

Exploratory programs remain untrusted. Exact outputs promoted into this
repository require a static data artifact, deterministic command, checksum,
scope statement, and hostile checker review. The broader
`Collatz-Conjecture-Work` repository remains a read-only source archive during
publication reconstruction.

## 8. Publication rule

Publish intermediate milestones when they add one of:

- a new human theorem;
- a newly audited exact transition class;
- a stronger rigorously delimited obstruction; or
- a materially smaller exact F3 boundary under a mechanism not already
  blocked above.

Do not publish a larger finite sweep as evidence of eventual closure. The
Collatz conjecture remains unresolved until `G1` passes.
