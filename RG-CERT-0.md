# RG-CERT-0: exact bootstrap certificate language

## 1. Status and purpose

`RG-CERT-0` is the first concrete, dependency-free certificate language for
the ranked-coalescence interface in [RG-SOUND-001.md](RG-SOUND-001.md).
It has two deliberately separate outcomes:

1. validate exact Collatz coalescence edges over whole infinite affine
   families; and
2. decide whether the source images of those edges cover every nonterminal
   configuration.

The initial Route B import is expected to pass every listed-edge check and
fail global source coverage on a finite, explicitly reported set of residue
families.  A successful audit of that partial object is **not** a proof of the
Collatz conjecture.  Only a bundle for which the checker reports all F1--F7
obligations as globally satisfied may be combined with RG-SOUND-001.

Version 0 uses one node and the ordinary numerical order.  This makes the
existing exact smaller-target coalescences directly importable.  It is a
bootstrap format, not a claim that numerical descent or affine ranks suffice
for the final construction.  A later format may add multiple node types and a
fixed-dimensional nonlinear well-founded rank without changing the soundness
theorem.

## 2. Map, configuration, decoder, and rank

The map is the stopped ordinary Collatz map

\[
T(n)=
\begin{cases}
1,&n=1,\\
n/2,&n>1\text{ and }n\text{ is even},\\
3n+1,&n>1\text{ and }n\text{ is odd}.
\end{cases}
\]

There is one node, `root`, with parameter domain

\[
D=\mathbb N.
\]

Its decoder and one-dimensional rank are

\[
\delta(p)=p+1,
\qquad
\rho(p)=p.
\]

Every parameter is an entry parameter.  Therefore F1 and F2 are immediate:
the decoder is positive, the rank is natural-valued, and every positive
integer \(n\) has the unique entry parameter \(p=n-1\).

The terminal configuration is \(p=0\), which decodes to \(1\).  Every
\(p\ge1\) must occur in at least one edge source image for F3 to hold.

## 3. Exact data grammar

A version-0 bundle is one UTF-8 JSON object with these top-level fields:

```text
schema                    exactly "RG-CERT-0/v0"
claim                     either "partial" or "global"
map                       exactly "stopped_collatz"
coverage_modulus          a positive integer C
expected_uncovered        a sorted list of source residues modulo C
edges                     a finite list of edge objects
```

Unknown fields are rejected at every object depth.  Duplicate object-member
names are rejected at every depth rather than resolved by first- or last-key
wins behavior.  The parser accepts standard JSON only: `NaN`, positive or
negative `Infinity`, and every other nonstandard constant are rejected.
Integers are JSON integers, not floating-point numbers or numeric strings;
booleans are not accepted as integers.  `expected_uncovered` must be a
strictly increasing list of unique integers in the half-open interval
\([0,C)\).

Each edge has exactly these fields:

```text
id                        [A-Za-z0-9][A-Za-z0-9._:-]{0,127}
domain_lower              an integer L >= 0
source_param              [M, R]
target_param              [A, B]
source_trace              a finite string over {S,E,O}
target_trace              a finite string over {S,E,O}
origin                    1--256 printable ASCII characters
```

The edge parameter is every integer \(x\ge L\).  Its raw source and target
maps are

\[
\sigma(x)=Mx+R,
\qquad
\phi(x)=Ax+B.
\]

Each parameter array has exactly two elements.  Both slopes are required to
be nonnegative.  A zero source slope represents
an exact singleton source family; the redundant infinite edge-parameter
domain is harmless.  Positive source slopes are required to divide the
declared coverage modulus \(C\).  This restriction is only for the exact F3
decision procedure in Section 6.

The decoded source and target families are therefore

\[
N(x)=Mx+R+1,
\qquad
m(x)=Ax+B+1.
\]

The trace symbols mean:

- `S`: the current value is identically \(1\), so the stopped branch fixes it;
- `E`: every current value is greater than \(1\) and even, so divide by \(2\);
- `O`: every current value is greater than \(1\) and odd, so replace it by
  \(3n+1\).

The macro lengths \(a_e,b_e\) are not stored redundantly: they are exactly
the lengths of `source_trace` and `target_trace`.

`origin` is a scalar metadata string only and is never used to establish an
arithmetic obligation.  Its permitted characters are ASCII code points 32
through 126 inclusive.  This closed grammar prevents provenance metadata from
silently carrying nested or executable semantics; the repository-level
lineage and checksums remain in [PROVENANCE.md](PROVENANCE.md).

## 4. Exact affine trace replay

At every point in a trace the current decoded family has the form

\[
f(x)=ux+v,
\qquad x\ge L,
\]

with integer coefficients and \(u\ge0\).  The following rules are necessary
and sufficient for the declared branch to hold over the whole infinite tail.

### Stopped branch

`S` is accepted exactly when \((u,v)=(0,1)\).  The next family is again
\((0,1)\).

### Even branch

`E` is accepted exactly when

\[
uL+v>1,
\qquad
u\equiv0\pmod2,
\qquad
v\equiv0\pmod2.
\]

The next family is \((u/2,v/2)\).

### Odd branch

`O` is accepted exactly when

\[
uL+v>1,
\qquad
u\equiv0\pmod2,
\qquad
v\equiv1\pmod2.
\]

The next family is \((3u,3v+1)\).

Because \(u\ge0\), the value at \(L\) is the minimum on the edge domain.
Because the domain contains every consecutive integer from \(L\) onward, an
affine family has uniform parity exactly when its slope is even and its
intercept has the declared parity.  Thus these are universal arithmetic
checks, not samples.

Replaying both traces produces endpoint pairs
\((u_s,v_s)\) and \((u_t,v_t)\).  F5 and F6 hold exactly when every branch
check succeeds and

\[
(u_s,v_s)=(u_t,v_t).
\]

This coefficient identity is equivalent to endpoint equality for every
\(x\ge L\).

## 5. Closure and strict decrease

F4 requires both raw parameters to remain in \(D=\mathbb N\).  For an affine
map with nonnegative slope on \(x\ge L\), this is equivalent to

\[
ML+R\ge0,
\qquad
AL+B\ge0.
\]

F7 is strict decrease in the declared numeric rank:

\[
Ax+B<Mx+R
\qquad\text{for every }x\ge L. \tag{1}
\]

Let \(d=M-A\).  The checker accepts (1) exactly when

\[
d\ge0
\qquad\text{and}\qquad
dL+(R-B)>0. \tag{2}
\]

If \(d<0\), the target eventually exceeds the source.  If \(d\ge0\), the
left side of the desired difference is nondecreasing, so positivity at the
lower endpoint is necessary and sufficient.  This includes the valid
equal-slope case \(M=A\) with \(B<R\).

## 6. Exact source-coverage decision

The source image of a positive-slope edge is the arithmetic tail

\[
\{Mx+R:x\ge L\}.
\]

The source image of a zero-slope edge is the singleton \(\{R\}\).  The
checker first requires every positive source slope \(M\) to divide the
declared modulus \(C\).

For each residue \(c\in\{0,\ldots,C-1\}\), define its least positive member

\[
q_c=\begin{cases}c,&c>0,\\C,&c=0,\end{cases}
\]

and consider the sequence of positive source parameters

\[
p=q_c+Ck,
\qquad k\ge0.
\]

A positive-slope edge \((M,R,L)\) can cover this sequence only if

\[
q_c\equiv R\pmod M.
\]

When that congruence holds, put

\[
k_e=\max\!\left(0,
\left\lceil\frac{ML+R-q_c}{C}\right\rceil\right). \tag{3}
\]

The edge covers every \(q_c+Ck\) with \(k\ge k_e\): the quotient
\((q_c+Ck-R)/M\) is integral, is at least \(L\), and increases by the integer
\(C/M\).  If one or more positive-slope edges have the required congruence,
let \(k_*\) be the least of their thresholds (3).  The checker tests every
\(0\le k<k_*\) by exact source-image membership against every edge:

\[
\begin{aligned}
M>0:&\quad p\equiv R\pmod M\ \text{ and }\ p\ge ML+R,\\
M=0:&\quad p=R.
\end{aligned} \tag{4}
\]

If there is no eligible positive-slope edge, finitely many singleton images
cannot cover the infinite sequence, so the residue is uncovered.

Formally, with \(\Sigma\) the union of all edge source images, define

\[
\mathcal U=
\left\{c\in\{0,\ldots,C-1\}:
\exists k\ge0,\ q_c+Ck\notin\Sigma\right\}. \tag{5}
\]

The threshold calculation and finite prefix test above decide membership in
\(\mathcal U\) exactly.

This proves one of two exact outcomes for each residue:

1. every positive \(p\equiv c\pmod C\) is covered; or
2. no positive-slope edge supplies an eventual tail, or a specific positive
   prefix parameter is uncovered.

The choice \(q_0=C\) explicitly excludes the terminal parameter \(p=0\)
from F3.  No bounded orbit sample is used.  F3 holds globally exactly when
\(\mathcal U=\varnothing\).

`expected_uncovered` must equal the strictly increasing enumeration of
\(\mathcal U\).  A mismatch rejects the bundle.  A `partial` bundle must have
\(\mathcal U\ne\varnothing\); a `global` bundle must declare an empty list
and have \(\mathcal U=\varnothing\).  The checker reports for each member of
\(\mathcal U\) whether it lacks any eventual tail edge or instead has a
specific finite-prefix hole, together with one exact uncovered parameter as a
witness.  Thus a residue with only one lower-bound hole is not silently
treated as covered, while a residue lacking a tail is not misleadingly
described as only one missing integer.

## 7. Import of the existing Route B certificates

The archived bounded search uses the unstopped ordinary map

\[
U(n)=\begin{cases}n/2,&n\text{ even},\\3n+1,&n\text{ odd},\end{cases}
\]

for which \(U(1)=4\), and an odd cylinder

\[
N(x)=2^Kx+R
\]

and an exact coalescing target

\[
m(x)=Ax+B,
\qquad 0<m(x)<N(x),
\]

with an ordinary-map identity

\[
U^t(N(x))=U^j(m(x))
\]

over a tail \(x\ge x_0\).  Its v0 translation is the `root` edge

\[
\sigma(x)=2^Kx+(R-1),
\qquad
\phi(x)=Ax+(B-1),
\qquad
L=x_0.
\]

The source trace is reconstructed symbolically from the archived cylinder;
the target trace is the archived parity word.  The archive's `validate()`
therefore proves an ordinary-\(U\) identity only.  Before import, every
pre-step affine family for a declared `E` or `O` step must be greater than
\(1\) on the new domain.  Reaching \(1\) only at the final endpoint is valid;
the mismatch occurs when another ordinary step would be taken from \(1\).

For a nonconstant positive-slope pre-step family, equality to \(1\) can occur
only at a finite lower-endpoint exception.  The importer may raise \(L\) past
all such exceptions, after which the recorded \(U\) and stopped-\(T\) traces
agree.  Every positive source instance excluded between the old and new lower
bounds must receive its own exact edge or is detected by (5).  If a required
pre-step family is identically \(1\), raising \(L\) cannot repair it: the
candidate must be discarded or its suffix recomputed with `S` branches.

The universal smaller-target inequality is exactly the v0 rank decrease,
since subtracting one from source and target does not change strict order.
The checker does not trust the search or importer: it replays both stopped-map
traces, the affine identity, closure, rank decrease, and source coverage from
the serialized edge data.

Even decoded inputs have the single exact edge

\[
\sigma(x)=2x+1,
\qquad
\phi(x)=x,
\qquad
T(2x+2)=x+1.
\]

At \(K=12\), the archived bounded search reports ordinary-map exact
smaller-target edges
for 1903 of the 2048 odd residue cylinders and leaves 145 unresolved.  The
1903 count is not yet a v0-valid result.  The first v0 artifact must
independently pass stopped-map replay, every required lower-bound split, and
the post-split F3 calculation before the imported-edge count and exact
uncovered residue set are treated as reviewed publication data.

## 8. Checker outcomes and fail-closed behavior

The command-line checker has three distinct outcomes.

- `LOCAL EDGE AUDIT PASS`: every serialized edge satisfies its schema, F4,
  F5, F6, and F7 obligations.  This says nothing by itself about F3.
- `PARTIAL CONSTRUCTION VERIFIED; GLOBAL F3 INCOMPLETE`: the local audit
  passed and the exact uncovered report equals the partial bundle's declared
  report.  This is a successful audit of an incomplete research artifact,
  not a global certificate.
- `GLOBAL RG-CERT-0 PASS`: the bundle declares `global`, all local checks
  pass, and exact source coverage is complete.  Only this outcome satisfies
  F1--F7 for the v0 specialization.

Any malformed field, duplicate JSON member name, nonstandard JSON constant,
duplicate identifier, unknown trace symbol, failed universal check,
coverage-report mismatch, or internal exception exits nonzero before printing
either success outcome.  Optimized Python mode is rejected before validation.
Assertions may be retained as developer guardrails but are never the sole
enforcement of a certificate obligation.

The checker also provides `--require-global`.  Under that flag a correct
partial bundle exits nonzero after reporting its incompleteness.  This is the
mode for any workflow whose success condition is a Collatz-complete
certificate.

## 9. Version boundary and next construction gate

`RG-CERT-0/v0` can certify exact direct descent and smaller-target
coalescence.  Because its rank is the source integer minus one, it cannot
represent an edge whose recursive target is numerically larger.  That is a
format limitation, not a mathematical obstruction theorem.

The next research fork is therefore explicit:

1. close the remaining v0 residue families with exact smaller targets; or
2. introduce a reviewed successor schema with genuinely richer finite state
   and a fixed-dimensional well-founded rank, then prove that checker's
   F1--F7 correspondence before using its search results.

In either branch, publication requires the data bundle, deterministic
transcript, exact checksum, independent checker audit, and an unambiguous
statement of whether global F3 passed.  Until `GLOBAL RG-CERT-0 PASS` or an
equally audited successor certificate exists, the Collatz conjecture remains
unresolved.
