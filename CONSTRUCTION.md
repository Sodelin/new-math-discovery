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

[RG-TRANS-001.md](RG-TRANS-001.md) supplies the exact global transition
closure.  Every positive integer has a unique parametric label

\[
N_{r,\eta}(w)=2^r(4w+2\eta+1)-1.
\]

Four terminal/soft guard rows either stop at \(1\) or coalesce with a strictly
smaller positive integer.  The one remaining row is the hard family

\[
r\ge2,\qquad \eta\not\equiv r\pmod2.
\]

Strong induction normalizes every input into that family or \(1\), and an
exact return map \(F\) closes the hard family.  Lemma 8.1 of RG-TRANS-001
partitions every one of the 145 affine gap endpoints into these rows.  This
completes `T2` as a finite set of parametric guard schemas.  The parameters
are unbounded, and termination of \(F\) is Collatz-equivalent; transition
closure is not progress.

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
richer state; nonlinearity alone is not enough.

The smaller exact return

\[
F(31)=91
\]

already grows numerically and raises the local replay counter from zero to
one.  It is the first boundary-normalized recharge witness and the minimum
falsification test for any proposed successor rank.

[RG-RANK-OBS-001.md](RG-RANK-OBS-001.md) upgrades those witnesses to a
universal exact obstruction.  For every ordered pair of distinct hard labels
\(\alpha,\beta\) and every \(q\ge0\), it constructs a hard return

\[
(\alpha,Q=0)\longrightarrow(\beta,Q=q).
\]

The \(Q=0\) feature layer therefore contains both directions between every
two distinct labels.  No rank into any well-founded relation can decrease on
all returns if it factors only through \((\text{hard label},Q)\), regardless
of whether its formula is nonlinear, lexicographic, multiset-valued, or
ordinal-valued.  This still leaves ranks that inspect the full hard parameter
or other augmented state, and it does not rule out stronger coalescences.

### B4. Representation without progress

The known finite mixed binary/ternary rewrite system is an exact Collatz
representation, but its universal termination is equivalent to Collatz.
RG-TRANS-001 now compresses every one of the 145 gaps into an exact closed
hard return and proves the same equivalence boundary.  Re-encoding or
iterating that return is useful only if a stronger coalescence macro or
independently checked rank is added.

The detailed blocker proofs remain linked from
[PROVENANCE.md](PROVENANCE.md) and the archive failure ledger. None of these
filters rules out all recursive graphs or all well-founded ranks.

## 4. Active theorem target: RG-RANK-001

RG-TRANS-001 answers state sufficiency, exactness, and global guard coverage.
The sole active mathematical deliverable is now progress on the closed hard
return.

> **RG-RANK-001 target.** Define an explicit decidable well-founded rank
> \(\mathcal R\) on the hard states of RG-TRANS-001 and prove
> \(\mathcal R(F(h))<\mathcal R(h)\) for every nonterminal hard state \(h\);
> or give a stronger exact coalescence macro that sends every hard return to a
> state already smaller in a proved well-founded order.

The theorem must cover arbitrary unbounded \(r,w\), every cross-label return,
the Mersenne high-child chain, and every canonical boundary value including
\(w=0\).  Its definition may not use stopping time, assumed convergence, or
an unbounded future search.  Until this progress theorem exists, there is no
reason to implement RG-CERT-1.

## 5. Ranked candidate policy

A rank candidate is admitted to a full search cycle only if it is:

- defined without stopping time, convergence, or an unbounded future search;
- natural-, ordinal-, or other explicitly well-founded-valued;
- decidable by a small trusted checker or finite proof objects;
- distinguishes states inside a common
  \((\text{hard label},Q)\) fibre, as required by RG-RANK-OBS-001;
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
| `T2` | Finite guarded child/successor transition table | T1 | Completed | RG-TRANS-001 gives a universal guard partition and exact identities |
| `O1` | Exact obstruction to label-and-replay-quotient ranks | T2 | Completed | RG-RANK-OBS-001 constructs every distinct cross-label direction with arbitrary exact recharge |
| `R1` | First rank or smaller-target mechanism for every T2 edge | T2, O1 | Active | Passes B1--B4 and distinguishes states within each \((\text{label},Q)\) fibre |
| `S1` | RG-CERT-1 language and checker correspondence | T2, R1 | Pending | Independent specification audit |
| `G1` | Static globally covering certificate | S1 | Pending | `--require-global` succeeds and F1--F7 audit passes |

Only `R1` may consume exploratory computation now.  Every candidate must act
on the exact RG-TRANS-001 hard return rather than a raw finite-horizon miss
bitmask.  Any candidate factoring through \((\text{hard label},Q)\) is already
closed by RG-RANK-OBS-001.  A richer surviving candidate must then be tested
first on \(31\mapsto91\), the recorded large recharge transition, and the
Mersenne boundary. Schema/checker work starts only after a rank mechanism
survives those tests.

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
