# RG-MACRO-001: exact affine refinement and target-macro compression

## 1. Status and purpose

This note replaces the phrase "the bounded search missed 145 cylinders" by
an exact symbolic statement.  It proves two elementary affine theorems and
uses their explicit guards to classify the retained \(K=12\) boundary:

1. every odd cylinder has an exact binary one-bit refinement; and
2. all 1,903 ordinary Route B certificates retained in RG-CERT-0 use only
   eight target traces: empty and `O`, plus six instances of one closed-form
   macro family.

The dependency-free classifier
[`verification/check_rg_macro_001.py`](verification/check_rg_macro_001.py)
does not import or run the archived breadth-first search.  From the formulas
below it reconstructs exactly the same 1,903 certified cylinders, the same
affine targets and traces, and the same 145-cylinder complement.

This is a symbolic compression of an exact finite frontier, not a proof of the
Collatz conjecture.  It supplies no finite cover of the 145 continuations and
no decreasing rank for them.  Those remain the separate `T2` and `R1` gates in
[CONSTRUCTION.md](CONSTRUCTION.md).

## 2. Three maps and the trace convention

Let \(U\) be the unstopped ordinary Collatz map

\[
U(n)=
\begin{cases}
n/2,&n\text{ even},\\
3n+1,&n\text{ odd},
\end{cases}
\]

and let \(A\) be its once-accelerated form

\[
A(n)=
\begin{cases}
n/2,&n\text{ even},\\
(3n+1)/2,&n\text{ odd}.
\end{cases}
\]

The stopped map \(T\) used by RG-CERT-0 has \(T(1)=1\) and agrees with \(U\)
above \(1\).  Ordinary trace letters are read from left to right:

\[
E:n\mapsto n/2,
\qquad
O:n\mapsto3n+1.
\]

Thus an even \(A\)-step expands to `E`, while an odd \(A\)-step expands to
`OE`.  Every stopped-map use of an `E` or `O` letter additionally requires
that its input be strictly greater than \(1\).

## 3. Universal one-bit affine refinement

### Theorem 3.1

Fix \(K\ge1\), an odd residue \(0<R<2^K\), and a nonnegative integer
\(L\).  On the parameter tail \(x\in\mathbb Z\), \(x\ge L\), suppose the
first \(K\) accelerated decisions have the exact affine endpoint

\[
A^K(2^Kx+R)=3^s x+B. \tag{3.1}
\]

For \(\epsilon\in\{0,1\}\), define

\[
R_\epsilon=R+\epsilon2^K,
\qquad
c_\epsilon=B+\epsilon3^s,
\]

and

\[
L_\epsilon=
\max\!\left(0,
\left\lceil\frac{L-\epsilon}{2}\right\rceil\right).
\]

Then, for every integer \(y\ge L_\epsilon\),

\[
A^{K+1}(2^{K+1}y+R_\epsilon)=
\begin{cases}
3^s y+c_\epsilon/2,
  &c_\epsilon\equiv0\pmod2,\\[1mm]
3^{s+1}y+(3c_\epsilon+1)/2,
  &c_\epsilon\equiv1\pmod2.
\end{cases} \tag{3.2}
\]

Exactly one child preserves endpoint exponent \(s\), and exactly one child
increments it to \(s+1\).  More precisely,

\[
\epsilon_{\rm preserve}\equiv B\pmod2,
\qquad
\epsilon_{\rm increment}=1-\epsilon_{\rm preserve}. \tag{3.3}
\]

The two substitutions \(x=2y+\epsilon\), with their stated domains, partition
the parent tail exactly.

### Proof

Substitute \(x=2y+\epsilon\) in (3.1):

\[
2^K(2y+\epsilon)+R=2^{K+1}y+R_\epsilon
\]

and

\[
A^K(2^{K+1}y+R_\epsilon)
=2\cdot3^s y+c_\epsilon. \tag{3.4}
\]

The coefficient of \(y\) is even, so the parity in (3.4) is the fixed parity
of \(c_\epsilon\).  Applying the corresponding branch of \(A\) gives (3.2).
Because

\[
c_1-c_0=3^s
\]

is odd, the two constants have opposite parity, which proves (3.3).  Finally,
\(2y+\epsilon\ge L\) is equivalent to \(y\ge L_\epsilon\), proving the exact
domain partition. \(\square\)

### Stopped-map boundary

Equation (3.2) is an unstopped identity.  In ordinary letters the newly
appended step is `E` on the preserving child and `OE` on the incrementing
child.  For the stopped map, every declared pre-step value must be greater
than \(1\).  At the new step the possible exceptional set is

\[
\left\{y\ge L_\epsilon:
2\cdot3^s y+c_\epsilon=1\right\}, \tag{3.5}
\]

which contains at most one integer unless the family is identically one.
Earlier trace prefixes require the same check.  Such boundary points must be
split into stopped terminal cases; they cannot be passed through using the
unstopped rule \(U(1)=4\).

The theorem proves an exact next source step.  It does not prove that a child
has a smaller coalescing target or that repeated refinement terminates.

## 4. A closed target-word family

For every \(k\ge0\), define

\[
w_k=O(EO)^kEEO=(OE)^{k+1}EO. \tag{4.1}
\]

### Theorem 4.1: forward formula and exact inverse guard

Whenever every letter of \(w_k\) has the declared parity,

\[
U^{|w_k|}(n)
=\frac{3^{k+2}(n+1)-2^{k+1}}{2^{k+2}}. \tag{4.2}
\]

Consequently, \(w_k\) maps a positive integer \(n\) to \(Y\) if and only if

\[
q=\frac{2Y+1}{3^{k+2}}\in\mathbb N_{>0},
\qquad
q\equiv(-1)^k\pmod4, \tag{4.3}
\]

in which case the unique predecessor is

\[
n=P_k(Y)
=\frac{2^{k+1}(2Y+1)}{3^{k+2}}-1
=2^{k+1}q-1. \tag{4.4}
\]

### Proof

One `OE` pair sends \(z+1\) to \(3(z+1)/2\).  After the first \(k+1\)
pairs in (4.1), the value is

\[
\frac{3^{k+1}(n+1)}{2^{k+1}}-1.
\]

Applying the final `EO` gives (4.2), and solving (4.2) for \(n\) gives
(4.4).

It remains to characterize the parity word.  Put
\(n=2^{k+1}q-1\).  After \(j\) of the first \(k+1\) `OE` pairs, the value is

\[
n_j=3^j2^{k+1-j}q-1. \tag{4.5}
\]

For \(0\le j\le k\), this is odd, and its `O` image is even.  The value
\(n_{k+1}=3^{k+1}q-1\) is even, as required by the next `E`.  The input to
the final `O` is

\[
\frac{3^{k+1}q-1}{2},
\]

which is odd exactly when

\[
3^{k+1}q\equiv3\pmod4.
\]

Since \(3^{-1}\equiv3\pmod4\), this is precisely
\(q\equiv3^{k+2}\equiv(-1)^k\pmod4\).  Positivity is exactly \(q>0\).
This proves necessity and sufficiency. \(\square\)

### Corollary 4.2: exact affine-tail guard

Let

\[
Y(x)=ax+b,
\qquad x\ge L,
\qquad a\ge0,
\]

where \(L\in\mathbb Z_{\ge0}\) and \(x\) ranges over consecutive integers.
Put \(d=3^{k+2}\).  The inverse (4.4) is one affine positive-integer
family with trace \(w_k\) on every consecutive integer \(x\ge L\) exactly
when

\[
2d\mid a, \tag{4.6}
\]

\[
d\mid 2b+1, \tag{4.7}
\]

\[
\frac{2b+1}{d}\equiv(-1)^k\pmod4, \tag{4.8}
\]

and

\[
q(L)=\frac{2aL+2b+1}{d}>0. \tag{4.9}
\]

Under these guards,

\[
P_k(Y(x))
=\frac{2^{k+2}a}{d}x
+\left(\frac{2^{k+1}(2b+1)}{d}-1\right). \tag{4.10}
\]

Indeed, the affine family

\[
q(x)=\frac{2a}{d}x+\frac{2b+1}{d}
\]

must have one fixed residue \((-1)^k\) modulo \(4\).  Conditions (4.6)--(4.8)
say exactly that its slope is divisible by \(4\) and its intercept has that
residue.  Since its slope is nonnegative, (4.9) is equivalent to positivity
on the whole tail.

For the stopped map, the sole positive pointwise parity-admissible exception
is

\[
(k,q,n,Y)=(0,1,1,4), \tag{4.11}
\]

because the first `O` would be taken from \(1\).  If (4.11) occurs only at a
lower endpoint, that point must be split or the lower bound raised.  For
\(k\ge1\), (4.4) and \(q\ge1\) give \(n\ge3\), and the displayed intermediate
values show that every declared `E` or `O` input is above \(1\).

## 5. Exact finite \(K=12\) classification

For every odd \(R\) with \(0<R<4096\), start from

\[
N_R(x)=4096x+R,
\qquad x\ge0. \tag{5.1}
\]

Beginning with \((a_0,b_0)=(4096,R)\), form every uniform ordinary prefix by
the exact recurrence

\[
(a_{i+1},b_{i+1})=
\begin{cases}
(a_i/2,b_i/2),&b_i\text{ even},\\
(3a_i,3b_i+1),&b_i\text{ odd},
\end{cases} \tag{5.2}
\]

while \(a_i\) is even.  The parity is uniform because the slope is even.
The recurrence stops immediately after the twelfth `E`, when the slope is a
power \(3^s\).

At each prefix endpoint \(Y_i(x)=a_ix+b_i\), test only the finite grammar

\[
\mathcal G_{16}=
\{\varnothing,O\}
\cup\{w_k:0\le k\le6\}. \tag{5.3}
\]

The empty word has target \(Y_i\).  The one-letter word `O` has target

\[
\frac{Y_i-1}{3}
\]

exactly when its affine coefficients are integral and uniformly odd.  The
remaining targets and their necessary-and-sufficient parity guards are
(4.6)--(4.10).

For any candidate target \(m(x)=Ax+B\), the existence of a tail on which

\[
0<m(x)<4096x+R \tag{5.4}
\]

is decided exactly from the two affine coefficients.  It is impossible if
\(A>4096\), or if \(A=4096\) and \(B\ge R\).  Otherwise positivity and strict
inequality each give one explicit lower bound, and their maximum is the least
valid \(L\).  This is the numerical-rank test proved in RG-CERT-0, not an
orbit sample.

### Proposition 5.1

Applying (5.2)--(5.4) to all 2,048 odd residues gives:

- 1,903 cylinders with an exact uniformly smaller target;
- 145 cylinders with no target in \(\mathcal G_{16}\) at any uniform prefix;
- exact equality with the Route B edge set and selected affine data retained
  in `rg_cert0_route_b_k12.json`; and
- the following complete selected-trace histogram.

| Target trace | Cylinders |
|---|---:|
| empty | 1,184 |
| `O` | 638 |
| \(w_1=\)`OEOEEO` | 5 |
| \(w_2=\)`OEOEOEEO` | 40 |
| \(w_3=\)`OEOEOEOEEO` | 20 |
| \(w_4=\)`OEOEOEOEOEEO` | 10 |
| \(w_5=\)`OEOEOEOEOEOEEO` | 4 |
| \(w_6=\)`OEOEOEOEOEOEOEEO` | 2 |

### Proof of Proposition 5.1

Recurrence (5.2) uniquely lists every uniform prefix, and Theorem 4.1 plus
Corollary 4.2 are necessary and sufficient for every nontrivial word in the
finite grammar (5.3).  The two affine inequalities in (5.4) are monotone, so
their coefficient test is also necessary and sufficient on an infinite tail.
It therefore remains only to evaluate finitely many integer predicates for
the 2,048 possible residues.

The classifier performs exactly that evaluation with arbitrary-precision
integers.  It then compares residue keys, source and target coefficients,
both trace words, stopped-safe lower bounds, and the ordered 145-element
complement against the static RG-CERT-0 bundle.  Every comparison succeeds,
and the displayed histogram sums to \(1{,}903\).  The source and checker are
retained with the deterministic transcript, so this finite last step is
directly reproducible and inspectable. \(\square\)

No selected certificate uses \(w_0\).  It is included in
\(\mathcal G_{16}\) because its length is within the same exact formula
family and its guard is needed to state the finite classifier without an
ad-hoc gap.

The exact 145 decoded residues \(R\), together with their RG-CERT-0 source
parameter residues \(p=R-1\), are printed in the retained transcript
[`verification/check_rg_macro_001_output.txt`](verification/check_rg_macro_001_output.txt).
They are now characterized by failure of the explicit finite predicates
(4.6)--(4.10) and (5.4) over the exact prefix recurrence (5.2), rather than by
the operational fact that a breadth-first search stopped.

For these 145 residues, the final slopes in (5.2) have the exact distribution

| Final exponent \(s\) | Cylinders |
|---:|---:|
| 8 | 38 |
| 9 | 60 |
| 10 | 36 |
| 11 | 10 |
| 12 | 1 |

The unique \(s=12\) residue is \(R=4095\).  Applying Theorem 3.1 to every gap
produces 290 exact children; in every pair one child preserves \(s\) and the
other increments it.  That binary refinement identity is structural.  It
does not say that either child is certified by \(\mathcal G_{16}\).

## 6. Verification boundary

The classifier independently implements only:

- the affine prefix recurrence (5.2);
- the three closed target forms: empty, `O`, and (4.10);
- universal parity and positivity guards;
- the exact affine smaller-target inequality;
- stopped-map lower-bound adjustment; and
- the one-bit identities (3.2) for all 290 children of the gaps.

It then compares its result with the static bundle.  It neither imports the
producer nor enumerates reverse-search states.  The exact match therefore
shows that the retained bounded search output has a much smaller symbolic
description; it does not turn a bounded description into a global one.

This classifier freezes the expected partial claim, stopped-map label, and
two non-Route-B edges so unrelated bundle mutations cannot inherit its PASS
marker.  It is still not a replacement for the full F1--F7 checker:
`check_rg_cert0.py` is a mandatory companion publication gate.

The next valid promotion is `T2`: a finite guarded successor table covering
every continuation of these 145 symbolic states.  A larger value of \(K\), a
larger inverse depth, or repeated use of Theorem 3.1 without a new finite-state
closure proof remains outside the promotion gate.
