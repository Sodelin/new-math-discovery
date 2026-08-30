# RG-RANK-OBS-001: exact cross-label replay-recharge obstruction

## 1. Status and purpose

This note proves a universal obstruction for rank candidates on the exact hard
return map \(F\) of [RG-TRANS-001.md](RG-TRANS-001.md).  For every ordered
pair of distinct hard labels and every prescribed nonnegative replay quotient,
there is an exact \(F\)-edge whose source quotient is zero and whose target
quotient is the prescribed value.

Consequently, no rank that depends only on the hard label and the local replay
quotient can strictly decrease on every \(F\)-edge.  This includes arbitrary
nonlinear and ordinal-valued combinations of those features, not merely the
affine combinations already filtered out in [CONSTRUCTION.md](CONSTRUCTION.md).

The theorem is constructive and uses only congruences modulo powers of two.
It does not use a bounded orbit search.  It also does **not** exhibit a
concrete \(F\)-cycle, rule out ranks that inspect the full hard parameter, or
prove or disprove the Collatz conjecture.  The active progress task `R1`
therefore remains open.

This is a theorem-facing reconstruction of project-specific consequences of
the exact return identities.  No literature-novelty claim is made.

## 2. Hard labels and local replay debt

Let \(\Lambda\) be the set of hard labels

\[
\Lambda
=\{(L,\epsilon):L\ge2,\ \epsilon\in\{0,1\},\
\epsilon\not\equiv L\pmod2\}. \tag{2.1}
\]

For \(\alpha=(L,\epsilon)\in\Lambda\), write

\[
H_\alpha(z)
=N_{L,\epsilon}(z)
=2^L(4z+2\epsilon+1)-1,
\qquad z\in\mathbb N. \tag{2.2}
\]

Define

\[
p_\alpha=3^{L+1},
\qquad
M_\alpha=2^{L+2}, \tag{2.3}
\]

\[
b_\alpha
=\frac{3^{L+1+\epsilon}+3}{4},
\qquad
d_\alpha
=b_\alpha-2^L(2\epsilon+1). \tag{2.4}
\]

Hard parity makes \(L+1+\epsilon\) even, so \(b_\alpha\) is a positive
integer.

The hard-prefix identity (6.4) of RG-TRANS-001 is equivalently

\[
Y_\alpha(z)+1=p_\alpha z+b_\alpha, \tag{2.5}
\]

and the closed hard return is

\[
F(H_\alpha(z))=\rho(Y_\alpha(z)). \tag{2.6}
\]

For later use, put

\[
E_\alpha(z)
=(M_\alpha-p_\alpha)z-d_\alpha, \tag{2.7}
\]

\[
D_\alpha(z)=\nu_2(|E_\alpha(z)|),
\qquad
Q_\alpha(z)=\left\lfloor\frac{D_\alpha(z)}{L+2}\right\rfloor. \tag{2.8}
\]

RG-TRANS-001 proves that \(E_\alpha(z)\ne0\) on every hard state, so
(2.8) is defined.  The quotient \(Q_\alpha\) is the audited local replay
counter whose first recharge was exhibited by \(F(31)=91\).

## 3. Every target label contains an exact successor ray

Fix two hard labels

\[
\alpha=(L,\epsilon),
\qquad
\beta=(h,\eta). \tag{3.1}
\]

### Lemma 3.1: exact cross-label successor cell

There is a unique residue

\[
z_0\pmod{M_\beta} \tag{3.2}
\]

satisfying

\[
p_\alpha z_0+b_\alpha
\equiv2^h(2\eta+1)
\pmod{M_\beta}. \tag{3.3}
\]

Choose \(0\le z_0<M_\beta\), and define

\[
c
=\frac{p_\alpha z_0+b_\alpha-2^h(2\eta+1)}{M_\beta}. \tag{3.4}
\]

Then \(c\in\mathbb N\).  For every \(u\in\mathbb N\), put

\[
z=z_0+M_\beta u,
\qquad
w=p_\alpha u+c. \tag{3.5}
\]

One then has the exact identities

\[
Y_\alpha(z)=H_\beta(w), \tag{3.6}
\]

\[
F(H_\alpha(z))=H_\beta(w). \tag{3.7}
\]

### Proof

The coefficient \(p_\alpha\) is odd, hence invertible modulo the power of two
\(M_\beta=2^{h+2}\).  Thus (3.3) has one and only one residue solution.
The congruence implies that \(p_\alpha z_0+b_\alpha\) has exact two-adic
valuation \(h\), and that its positive odd quotient is
\(2\eta+1\) modulo \(4\).  The least positive integer in that congruence
class is \(2\eta+1\), so (3.4) is a nonnegative integer.

Substitution of (3.5) into (2.5) gives

\[
\begin{aligned}
Y_\alpha(z)+1
&=p_\alpha z_0+b_\alpha+p_\alpha M_\beta u\\
&=2^h\bigl(4c+2\eta+1+4p_\alpha u\bigr)\\
&=2^h(4w+2\eta+1).
\end{aligned} \tag{3.8}
\]

This is (3.6).  Because \(\beta\) is hard, the normalizer \(\rho\) fixes
\(H_\beta(w)\).  Equations (2.6) and (3.6) therefore give (3.7).
\(\square\)

## 4. Arbitrarily prescribed exact recharge

### Theorem 4.1: cross-label exact-recharge theorem

Let \(\alpha=(L,\epsilon)\) and \(\beta=(h,\eta)\) be distinct hard labels.
For every \(q\in\mathbb N\), there are \(z,w\in\mathbb N\) such that

\[
F(H_\alpha(z))=H_\beta(w), \tag{4.1}
\]

\[
Q_\alpha(z)=0, \tag{4.2}
\]

and, in the stronger exact form,

\[
D_\beta(w)=(h+2)q,
\qquad
Q_\beta(w)=q. \tag{4.3}
\]

### Proof

Use Lemma 3.1 and retain its full successor ray

\[
z=z_0+M_\beta u,
\qquad
w=p_\alpha u+c. \tag{4.4}
\]

Along this ray the target debt expression is

\[
\begin{aligned}
E_\beta(w)
&=(M_\beta-p_\beta)(p_\alpha u+c)-d_\beta\\
&=Au+C,
\end{aligned} \tag{4.5}
\]

where

\[
A=(M_\beta-p_\beta)p_\alpha,
\qquad
C=(M_\beta-p_\beta)c-d_\beta. \tag{4.6}
\]

Both \(M_\beta-p_\beta\) and \(p_\alpha\) are odd, so \(A\) is odd.  Set

\[
K=(h+2)q. \tag{4.7}
\]

Because \(A\) is invertible modulo \(2^{K+1}\), the congruence

\[
u\equiv A^{-1}(2^K-C)\pmod{2^{K+1}} \tag{4.8}
\]

has a unique residue solution.  Choose its least nonnegative representative.
Then

\[
E_\beta(w)\equiv2^K\pmod{2^{K+1}}, \tag{4.9}
\]

so \(E_\beta(w)\ne0\) and \(D_\beta(w)=K\).  Equation (4.3) follows.

It remains to calculate the source quotient.  From (2.4) and (2.7),

\[
E_\alpha(z)
=M_\alpha z-
\bigl(p_\alpha z+b_\alpha-2^L(2\epsilon+1)\bigr). \tag{4.10}
\]

Consequently,

\[
M_\alpha\mid E_\alpha(z) \tag{4.11}
\]

holds if and only if

\[
p_\alpha z+b_\alpha
\equiv2^L(2\epsilon+1)
\pmod{M_\alpha}. \tag{4.12}
\]

By the uniqueness of canonical labels, (4.12) says exactly that
\(Y_\alpha(z)\) has label \(\alpha\).  Lemma 3.1 instead makes that label
the distinct label \(\beta\).  Hence (4.11) fails.  In particular,
\(E_\alpha(z)\ne0\) and

\[
D_\alpha(z)<L+2. \tag{4.13}
\]

Equation (4.2) follows from (2.8), while (4.1) already follows from
Lemma 3.1.  All constructed parameters are nonnegative, and every hard
target is positive and nonterminal, so there is no boundary exception.
\(\square\)

## 5. A complete zero-quotient label subgraph

Project each hard state to the feature pair

\[
\Phi(H_\alpha(z))=(\alpha,Q_\alpha(z)). \tag{5.1}
\]

Theorem 4.1 proves that the projected transition relation contains

\[
(\alpha,0)\longrightarrow(\beta,q) \tag{5.2}
\]

for every two distinct hard labels \(\alpha,\beta\) and every
\(q\in\mathbb N\).  In particular, its \(Q=0\) layer contains the complete
loopless directed graph on the infinite label set \(\Lambda\).  This statement
does not exclude additional projected self-loops.

For example, the two exact transitions

\[
F(H_{(2,1)}(9))=H_{(3,0)}(8),
\qquad
155\longrightarrow263, \tag{5.3}
\]

\[
F(H_{(3,0)}(7))=H_{(2,1)}(36),
\qquad
231\longrightarrow587, \tag{5.4}
\]

have quotient zero at both ends.  They form a two-cycle only after projection
by \(\Phi\); they are not a concrete two-cycle of \(F\).
Their exact debt pairs are respectively

\[
(D,Q):(2,0)\longrightarrow(0,0)
\quad\text{and}\quad
(2,0)\longrightarrow(0,0). \tag{5.5}
\]

## 6. Rank-factor obstruction

### Corollary 6.1

Let \((W,\prec)\) be any well-founded relation.  There is no function

\[
\mathcal R:\mathcal H\longrightarrow W \tag{6.1}
\]

for which there is a function

\[
r:\Lambda\times\mathbb N\longrightarrow W \tag{6.2}
\]

satisfying

\[
\mathcal R(H_\alpha(z))=r(\alpha,Q_\alpha(z)) \tag{6.3}
\]

for all \(\alpha\in\Lambda\) and \(z\in\mathbb N\), and such that every
hard-to-hard return satisfies

\[
\mathcal R(F(H_\alpha(z)))
\prec
\mathcal R(H_\alpha(z)). \tag{6.4}
\]

### Proof

Choose distinct hard labels \(\alpha\) and \(\beta\).  Theorem 4.1 with
\(q=0\), first in the order \((\alpha,\beta)\) and then in the order
\((\beta,\alpha)\), forces

\[
r(\beta,0)\prec r(\alpha,0),
\qquad
r(\alpha,0)\prec r(\beta,0). \tag{6.5}
\]

Alternating these two relations gives an infinite descending chain, contrary
to well-foundedness. \(\square\)

The codomain in Corollary 6.1 is arbitrary.  Thus changing a numerical
combination into a nonlinear, lexicographic, multiset, or ordinal expression
does not help if the resulting rank still factors only through
\((\text{label},Q)\).  Immediate special cases include:

- label-only or replay-quotient-only ranks;
- arbitrary functions of the full label and \(Q\);
- ranks using any finite quotient or coarsening of the label together with
  \(Q\); and
- lexicographic ranks whose coordinates contain no information beyond the
  label and \(Q\).

In particular, a finite label quotient cannot hide the obstruction.  Since
\(\Lambda\) is infinite, two distinct labels share a quotient class; the
corresponding exact \(Q=0\) transition projects to a self-loop.

## 7. Exact scope and remaining obligation

Theorem 4.1 strengthens blocker `B3`: recharge is not an isolated numerical
witness.  At the level of hard label plus local replay quotient, every
distinct cross-label transition exists from zero debt, and the target quotient
can be prescribed arbitrarily.

The following conclusions do **not** follow:

- The two directions in (6.5) use different concrete states, so no concrete
  \(F\)-cycle has been proved.
- The theorem does not show that one \(F\)-orbit encounters unbounded replay
  quotients.
- It does not rule out a rank using the full parameter \(z\), the exact debt
  \(D\), additional residues or carries, bounded history, or other augmented
  state.
- It does not rule out a finite quotient of an augmented full state, unless
  that quotient itself factors only through the label and \(Q\).
- It does not rule out a stronger exact coalescence macro.
- It supplies no Collatz convergence or divergence conclusion.

Any future `RG-RANK-001` candidate must therefore distinguish states inside
the same \((\text{label},Q)\) fibre and prove universal decrease using that
additional information.  The exact remaining target is still the one stated
in [CONSTRUCTION.md](CONSTRUCTION.md): a decidable well-founded rank on every
hard return, or a stronger universal coalescence reduction.
