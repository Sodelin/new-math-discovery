# RG-TRANS-001: exact global hard-boundary return system

## 1. Status and purpose

This note gives a finite parametric transition table for every positive
integer under the once-accelerated Collatz map.  Every state either:

1. is terminal;
2. has an explicit coalescing target that is strictly smaller as an integer;
   or
3. belongs to one precisely defined recurrent hard family.

The soft reductions terminate by ordinary strong induction.  The hard family
has an exact closed return map.  Termination of that return map is equivalent
to the Collatz conjecture.

Thus this theorem completes the transition-closure task `T2` in
[CONSTRUCTION.md](CONSTRUCTION.md), but it does **not** complete the progress
task `R1`.  In particular, the return map can increase both the represented
integer and the currently known replay-debt rank.  No Collatz proof is claimed.

The construction is global and human-checkable: it is a five-row guarded
table with natural-number parameters, not a bounded orbit computation.  Its
specialization to the 145 RG-CERT-0 gaps is given in Section 8.
"Finite" here means finitely many parametric guard schemas; the parameters
\(r\) and \(w\) are unbounded, so this is not a finite-state automaton and no
minimality claim is made.

This is a theorem-facing reconstruction of the accepted archive identities.
No literature-novelty claim is made.

## 2. Accelerated convention

Use the unstopped once-accelerated Collatz map

\[
A(n)=
\begin{cases}
n/2,&n\text{ even},\\
(3n+1)/2,&n\text{ odd}.
\end{cases} \tag{2.1}
\]

Let \(A^j\) denote \(j\)-fold iteration, and let
\(\operatorname{Conv}(n)\) mean that some iterate of \(n\) equals \(1\).
This convergence predicate is equivalent to convergence for the stopped
ordinary map in RG-SOUND-001: an even accelerated step is the ordinary word
`E`, and an odd accelerated step is `OE`.

Write

\[
n\bowtie m
\quad\Longleftrightarrow\quad
\exists i,j\in\mathbb N,\ A^i(n)=A^j(m) \tag{2.2}
\]

for exact orbit coalescence.  This relation is reflexive, symmetric, and
transitive.  For transitivity, if two equalities meet the middle orbit at
different times, iterate the earlier middle endpoint until the later one;
determinism then gives one common endpoint for the outer two orbits.
Moreover, \(A(1)=2\) and \(A(2)=1\), so every point on the post-\(1\) tail is
itself convergent.  Exact coalescence therefore implies convergence
equivalence in both directions.

## 3. Unique canonical labels

For \(r,w\in\mathbb N\) and \(\eta\in\{0,1\}\), define

\[
N_{r,\eta}(w)
=2^r(4w+2\eta+1)-1. \tag{3.1}
\]

### Lemma 3.1

Every positive integer \(n\) has a unique representation

\[
n=N_{r,\eta}(w). \tag{3.2}
\]

Explicitly,

\[
r=\nu_2(n+1),
\qquad
q=\frac{n+1}{2^r}, \tag{3.3}
\]

where \(q\) is positive and odd.  There is one
\(\eta\in\{0,1\}\) with

\[
q\equiv2\eta+1\pmod4, \tag{3.4}
\]

and then

\[
w=\frac{q-(2\eta+1)}4. \tag{3.5}
\]

### Proof

The exact two-adic valuation in (3.3) is unique.  Every positive odd integer
is uniquely \(1\) or \(3\) modulo \(4\), which determines \(\eta\), and then
(3.5) is a unique nonnegative integer.  Substitution gives (3.2). \(\square\)

## 4. The finite boundary table

Call a canonical label **hard** when

\[
r\ge2,
\qquad
\eta\not\equiv r\pmod2. \tag{4.1}
\]

Let \(\mathcal H\) be the set of positive integers with hard labels.  Every
other nonterminal label is **soft**.  Define the soft target

\[
\beta\bigl(N_{r,\eta}(w)\bigr)=
\begin{cases}
2w+\eta,&r=0,\\[1mm]
6w+3\eta+1,&r=1,\\[1mm]
3\,2^{r-2}(4w+2\eta+1)-1,
  &r\ge2\text{ and }\eta\equiv r\pmod2.
\end{cases} \tag{4.2}
\]

The middle row excludes the terminal instance
\((r,\eta,w)=(1,0,0)\), which represents \(1\).

The complete guarded transition table is:

| Row | Exact guard | Outcome |
|---:|---|---|
| 1 | \((r,\eta,w)=(1,0,0)\) | terminal \(1\) |
| 2 | \(r=0\) | smaller target \(2w+\eta\) |
| 3 | \(r=1\), nonterminal | smaller target \(6w+3\eta+1\) |
| 4 | \(r\ge2\), \(\eta\equiv r\pmod2\) | compatible smaller target in (4.2) |
| 5 | \(r\ge2\), \(\eta\not\equiv r\pmod2\) | recurrent hard state |

Lemma 3.1 makes these guards disjoint and exhaustive.

### Theorem 4.1: every soft row is an exact decreasing coalescence

For every nonterminal soft \(n=N_{r,\eta}(w)\),

\[
0<\beta(n)<n, \tag{4.3}
\]

and the following exact identities hold:

\[
\begin{array}{rcll}
A(n)&=&\beta(n),&r=0,\\[1mm]
A^2(n)&=&\beta(n),&r=1,\\[1mm]
A^{r+2}(n)&=&A^r(\beta(n)),
  &r\ge2,\ \eta\equiv r\pmod2.
\end{array} \tag{4.4}
\]

Consequently,

\[
n\bowtie\beta(n), \tag{4.5}
\]

and hence

\[
\operatorname{Conv}(n)
\iff
\operatorname{Conv}(\beta(n)). \tag{4.6}
\]

### Proof

If \(r=0\), then \(n=4w+2\eta\) is even and
\(A(n)=n/2=2w+\eta\).  Positivity follows from the exclusion of
\(n=0\), and division by two is strict for positive \(n>1\).

If \(r=1\), then

\[
n=8w+4\eta+1,
\qquad
\frac{3n+1}{4}=6w+3\eta+1. \tag{4.7}
\]

The first accelerated step uses the odd branch; its output is even because
\(n\equiv1\pmod4\), so the second step gives (4.7).  Moreover,

\[
n-\beta(n)=2w+\eta, \tag{4.8}
\]

which is positive exactly outside the terminal case \(w=\eta=0\).

Now suppose \(r\ge2\), put

\[
a=4w+2\eta+1,
\qquad
n=2^r a-1. \tag{4.9}
\]

For \(0\le j\le r\), direct guarded iteration gives

\[
A^j(n)=2^{r-j}3^j a-1. \tag{4.10}
\]

The branch is odd for every \(j<r\).  Compatibility
\(\eta\equiv r\pmod2\) gives

\[
3^r a\equiv1\pmod4. \tag{4.11}
\]

Therefore the next two branches from \(3^r a-1\) are both even, and

\[
A^{r+2}(n)=\frac{3^r a-1}{4}. \tag{4.12}
\]

On the other side,

\[
\beta(n)=3\,2^{r-2}a-1. \tag{4.13}
\]

Its first \(r-2\) branches are odd.  They lead to
\(3^{r-1}a-1\), which is twice an odd integer by (4.11).  The next
branches are even and then odd, giving

\[
A^r(\beta(n))=\frac{3^r a-1}{4}. \tag{4.14}
\]

Equations (4.12)--(4.14) prove the last coalescence identity.  Finally,

\[
n-\beta(n)=2^{r-2}a>0, \tag{4.15}
\]

and (4.13) is positive.  The three identities witness (4.5), and exact
coalescence transfers convergence in both directions, proving (4.6).
\(\square\)

## 5. Terminating normalization into the hard set

Define \(\rho:\mathbb N_{>0}\to\mathbb N_{>0}\) recursively by

\[
\rho(n)=
\begin{cases}
n,&n=1\text{ or }n\in\mathcal H,\\
\rho(\beta(n)),&\text{otherwise}.
\end{cases} \tag{5.1}
\]

This is well-defined natural-number recursion because every recursive
argument satisfies \(0<\beta(n)<n\).

### Corollary 5.1

For every positive integer \(n\),

\[
\rho(n)\in\mathcal H\cup\{1\}, \tag{5.2}
\]

and

\[
 n\bowtie\rho(n), \tag{5.3}
\]

so in particular

\[
\operatorname{Conv}(n)
\iff
\operatorname{Conv}(\rho(n)). \tag{5.4}
\]

### Proof

Strong induction on \(n\).  Terminal and hard inputs are immediate.  Every
other input reduces to the smaller positive integer \(\beta(n)\); apply the
induction hypothesis and transitivity of \(\bowtie\) to (4.5).  The convergence
equivalence follows. \(\square\)

## 6. Exact return map on the hard family

Write a hard state as

\[
h=N_{L,\epsilon}(z)
=2^L(4z+2\epsilon+1)-1, \tag{6.1}
\]

where

\[
L\ge2,
\qquad
\epsilon\not\equiv L\pmod2. \tag{6.2}
\]

Put \(a=4z+2\epsilon+1\).  The first \(L\) accelerated branches are odd and

\[
A^L(h)=3^L a-1. \tag{6.3}
\]

Hard parity gives \(3^La\equiv3\pmod4\).  Hence the next branch is even and
the following branch is odd.  Direct substitution gives

\[
A^{L+2}(h)
=Y_{L,\epsilon}(z)
=3^{L+1}z+\frac{3^{L+1+\epsilon}-1}{4}. \tag{6.4}
\]

Define the hard return map

\[
F(h)=\rho\bigl(Y_{L,\epsilon}(z)\bigr). \tag{6.5}
\]

By Corollary 5.1,

\[
F(h)\in\mathcal H\cup\{1\}, \tag{6.6}
\]

and equations (6.4)--(6.5) give

\[
h\bowtie F(h), \tag{6.7}
\]

and hence

\[
\operatorname{Conv}(h)
\iff
\operatorname{Conv}(F(h)). \tag{6.8}
\]

Indeed, \(h\) reaches \(Y_{L,\epsilon}(z)\), and Corollary 5.1 coalesces that
endpoint with its finite normal form \(\rho(Y_{L,\epsilon}(z))\).  Thus \(F\)
is a closed exact transition on the sole recurrent state type.

## 7. Exact global reduction theorem

### Theorem 7.1

The following assertions are equivalent:

1. every positive integer has an accelerated Collatz orbit reaching \(1\);
2. every orbit of \(F\) starting in \(\mathcal H\) reaches \(1\).

### Proof

Assume first that every \(F\)-orbit reaches \(1\).  Given any positive
integer \(n\), Corollary 5.1 sends it to \(\rho(n)\in\mathcal H\cup\{1\}\)
without changing convergence.  If the result is hard, repeatedly use (6.8)
along its terminating \(F\)-orbit.  Hence \(n\) converges.

Conversely, assume every positive integer converges and define its stopping
time

\[
\tau(n)=\min\{j\ge0:A^j(n)=1\}. \tag{7.1}
\]

The explicit hard prefix (6.3)--(6.4) contains no \(1\), so

\[
\tau\bigl(Y_{L,\epsilon}(z)\bigr)
=\tau(h)-(L+2). \tag{7.2}
\]

Each nonterminal soft reduction in (4.4) also lowers stopping time.  In the
first two rows it removes respectively one and two initial steps.  In the
compatible row, the explicit source prefix does not reach \(1\) before its
displayed meeting time.  If the smaller target reaches \(1\) before its own
meeting time, its stopping time is already smaller; otherwise the two paths
have the same remaining tail after respectively \(r+2\) and \(r\) steps.
In either case,

\[
\tau(\beta(n))<\tau(n). \tag{7.3}
\]

It follows along the finite recursion (5.1) that

\[
\tau(F(h))
\le\tau\bigl(Y_{L,\epsilon}(z)\bigr)
<\tau(h). \tag{7.4}

Therefore \(\tau\) strictly decreases on every nonterminal \(F\)-transition,
so every \(F\)-orbit reaches \(1\). \(\square\)

The stopping-time rank in this converse direction depends on the assumed
Collatz conclusion.  It is not a construction of the independent rank
required by `R1`.

## 8. Exact entry of every RG-CERT-0 gap

The 145 RG-CERT-0 gaps have maximal accelerated endpoints

\[
A^{12}(4096x+R)=3^s x+B,
\qquad x\ge0. \tag{8.1}
\]

The next lemma gives one uniform transition schema for all of them.

### Lemma 8.1: odd-affine valuation cells

Let

\[
Y(x)=px+b,
\qquad x\ge0, \tag{8.2}
\]

where \(p\) is positive and odd and \(b\ge1\).  For every
\(r\in\mathbb N\) and \(\eta\in\{0,1\}\), there is a unique residue

\[
x_{r,\eta}\pmod{2^{r+2}} \tag{8.3}
\]

satisfying

\[
px_{r,\eta}+b+1
\equiv2^r(2\eta+1)
\pmod{2^{r+2}}. \tag{8.4}
\]

Choose the representative \(0\le x_{r,\eta}<2^{r+2}\), and put

\[
q_{r,\eta}
=\frac{px_{r,\eta}+b+1}{2^r}
=4c_{r,\eta}+2\eta+1. \tag{8.5}
\]

Then \(c_{r,\eta}\) is a nonnegative integer, and on the exact cell

\[
x=x_{r,\eta}+2^{r+2}u,
\qquad u\ge0, \tag{8.6}
\]

one has

\[
Y(x)=N_{r,\eta}(pu+c_{r,\eta}). \tag{8.7}
\]

The cells (8.6), over all \((r,\eta)\), are disjoint and exhaust every
nonnegative integer \(x\).

### Proof

Because \(p\) is odd, it is invertible modulo every power of two, so (8.4)
has exactly one residue solution.  The congruence says that the numerator in
(8.5) has exact valuation \(r\) and that its odd quotient is
\(2\eta+1\) modulo \(4\).  Positivity gives \(c_{r,\eta}\ge0\).  Substituting
(8.6) into (8.2) gives

\[
Y(x)+1
=2^r\bigl(4(pu+c_{r,\eta})+2\eta+1\bigr),
\]

which is (8.7).  Conversely, every \(x\) has a unique exact valuation and
odd quotient by Lemma 3.1, so it lies in exactly one cell. \(\square\)

Apply Lemma 8.1 to (8.1) with \(p=3^s\) and \(b=B\).  Every instance of every
one of the 145 gap cylinders enters exactly one row of the global table in
Section 4.  Soft cells have an explicit decreasing target relative to their
endpoint; hard cells enter \(\mathcal H\), and (5.1) handles any further soft
normalization.  This supplies exhaustive symbolic continuation coverage
without increasing \(K\) or using a future-search miss bitmask.

The decreasing comparison here is with the endpoint \(Y(x)\), not necessarily
with the original cylinder value \(4096x+R\).  Consequently Lemma 8.1 closes
the transition table but does not furnish the rank decrease required by
RG-SOUND-001.

## 9. The first rank-recharge witness

The closed return map is not numerically decreasing.  The smallest hard input
whose boundary-normalized return both grows and recharges the audited local
replay debt is

\[
31=N_{5,0}(0)
\xrightarrow{\ A^7\ }
182=N_{0,1}(45)
\xrightarrow{\ A\ }
91=N_{2,1}(5). \tag{9.1}
\]

Thus

\[
F(31)=91>31. \tag{9.2}
\]

For a hard state, define

\[
d_{L,\epsilon}
=\frac{3^{L+1+\epsilon}+3}{4}-2^L(2\epsilon+1), \tag{9.3}
\]

\[
D_{L,\epsilon}(z)
=\nu_2\!\left(\left|
(2^{L+2}-3^{L+1})z-d_{L,\epsilon}
\right|\right),
\qquad
Q_{L,\epsilon}(z)
=\left\lfloor\frac{D_{L,\epsilon}(z)}{L+2}\right\rfloor. \tag{9.4}
\]

The valuation argument is nonzero on hard states.  Indeed,
\(2^{L+2}-3^{L+1}<0\) for \(L\ge2\), while hard parity forces either
\((L,\epsilon)=(\text{odd},0)\) or
\((L,\epsilon)=(\text{even},1)\).  In the first case \(L\ge3\) and
\(3^{L+1}>4\cdot2^L\); in the second \(L\ge2\) and
\(3^{L+2}>12\cdot2^L\).  Each inequality holds at its least permitted \(L\)
and remains true when \(L\) increases by two.  Thus (9.3) is positive, and
the expression inside the absolute value is strictly negative for every
\(z\ge0\).  Direct calculation gives

\[
(D,Q)(5,0,0)=(0,0),
\qquad
(D,Q)(2,1,5)=(6,1). \tag{9.5}
\]

The known same-label rank therefore recharges from \(0\) to \(1\) across
(9.1), while the represented integer grows.  This does not rule out richer
nonlinear, ordinal, or additional-state ranks.  It does rule out promoting
the local replay counter itself as the missing global rank.

For completeness, the only hard inputs below \(31\) are
\(7=N_{3,0}(0)\), \(11=N_{2,1}(0)\), and
\(27=N_{2,1}(1)\).  Exact use of (6.4) and (5.1) gives

\[
F(7)=F(11)=1,
\qquad
F(27)=47=N_{4,1}(0), \tag{9.6}
\]

and the target in the last transition has \(Q_{4,1}(0)=0\).  Hence (9.1) is
indeed the first hard input exhibiting both numerical growth and a positive
recharge of \(Q\).

## 10. Exact remaining obligation

RG-TRANS-001 gives:

- a unique entry label for every positive integer;
- a finite exhaustive guard table;
- exact coalescence identities on every soft row;
- a terminating strong-induction normalizer into one recurrent hard state
  type;
- an exact closed hard return map; and
- a formula-level entry partition for every RG-CERT-0 gap.

What it does not give is the essential global progress mechanism.  The next
valid theorem must either:

1. assign a well-founded rank that strictly decreases on every \(F\)-edge;
   or
2. add a stronger exact coalescence macro that reduces every hard return to a
   previously ranked state.

Iterating \(F\), extending a finite search horizon, or naming an equivalent
mixed-radix rewrite system does not meet that obligation.  By Theorem 7.1,
proving termination of \(F\) without a new mechanism is exactly as hard as the
Collatz conjecture.
