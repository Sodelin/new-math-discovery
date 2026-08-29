# H-FCS-001: finite-center periodic-shadow obstruction

## 1. Definitions

For a nonzero rational number \(x\), let \(\nu_2(x)\) be the exponent of
\(2\) in \(x\), and put \(\nu_2(0)=\infty\). On the positive odd integers,
define the accelerated odd Collatz map

\[
S(n)=\frac{3n+1}{2^{\nu_2(3n+1)}}.
\]

Fix a finite ordered set of rational centers
\(C=(c_1,\ldots,c_s)\), and define the sensor vector

\[
\Sigma_C(n)=
\bigl(\nu_2(n-c_1),\ldots,\nu_2(n-c_s)\bigr).
\]

The correction below is completely arbitrary: no boundedness, continuity,
computability, monotonicity, or locality assumption is imposed beyond its
dependence on this finite sensor vector.

## 2. The theorem

**Theorem (H-FCS-001).** Let \(C\subset\mathbb Q\) be finite, let
\(\alpha>0\), let

\[
R:(\mathbb Z\cup\{\infty\})^s\longrightarrow\mathbb R,
\]

and define

\[
V(n)=\alpha\log_2 n+R(\Sigma_C(n)).
\]

For every \(0<\beta<1\) and every threshold \(N_0\), there is a positive
odd integer \(N\ge N_0\) such that

\[
V(S^\tau(N))>V(N)
\]

for every integer

\[
1\le\tau\le\lfloor\beta\log_2N\rfloor.
\]

Consequently, no potential in this class has a universal non-increase
guarantee within a fixed sub-bitlength fraction of accelerated Collatz steps.

## 3. A disjoint family of repelling rational cycles

For each \(m\ge3\), consider the valuation word

\[
w_m=(2,1^{m-1}).
\]

Its total valuation is

\[
A_m=m+1,
\]

and its real return multiplier is

\[
\lambda_m=\frac{3^m}{2^{m+1}}>1.
\]

For a valuation word \(a_0,\ldots,a_{m-1}\), with
\(A_j=\sum_{t<j}a_t\), the corresponding branch composition is

\[
x\longmapsto
\frac{3^m x+C}{2^A},
\qquad
C=\sum_{j=0}^{m-1}3^{m-1-j}2^{A_j}.
\]

For \(w_m\),

\[
C_m=5\cdot3^{m-1}-2^{m+1},
\]

so the branch fixed point is

\[
q_{m,0}=\frac{C_m}{2^{m+1}-3^m}<0.
\]

Writing \(D_m=3^m-2^{m+1}\), its remaining phases are

\[
q_{m,j}=
\frac{2^{m+1}-3^m-2^{m-j+1}3^{j-1}}{D_m},
\qquad 1\le j<m.
\]

Every displayed numerator and denominator is odd. Direct substitution gives

\[
3q_{m,0}+1=4q_{m,1},
\]

\[
3q_{m,j}+1=2q_{m,j+1}
\quad(1\le j<m-1),
\]

and

\[
3q_{m,m-1}+1=2q_{m,0}.
\]

Thus these identities have exact valuations \(2,1,\ldots,1\), not merely
lower bounds, and they form a negative rational cycle
\(Q_m=\{q_{m,0},\ldots,q_{m,m-1}\}\).

The infinite valuation itinerary has one symbol \(2\) every \(m\) positions,
so its least period is exactly \(m\). Therefore the phases within \(Q_m\)
are distinct. If \(Q_m\) and \(Q_{m'}\) shared a phase, determinism of the
exact valuation itinerary would give the same least period, forcing
\(m=m'\). Hence the cycles \(Q_m\) are pairwise disjoint.

## 4. Choosing a cycle that defeats the proposed horizon

Fix \(0<\beta<1\). Since

\[
\frac{m}{m+1}\longrightarrow1,
\]

there are arbitrarily large \(m\) satisfying

\[
\beta A_m=\beta(m+1)<m. \tag{1}
\]

The cycles \(Q_m\) are pairwise disjoint, while \(C\) is finite. Therefore
only finitely many \(Q_m\) can meet \(C\). Choose an \(m\) satisfying (1)
and

\[
Q_m\cap C=\varnothing. \tag{2}
\]

All sensor contacts are now finite. Choose an integer \(B\ge1\) such that

\[
B>max_{0\le i<m,\ 1\le\ell\le s}
\nu_2(q_{m,i}-c_\ell). \tag{3}
\]

For an empty center set, the maximum condition is vacuous.

## 5. Exact positive shadows of arbitrary depth

Fix a depth \(r\ge1\), and put

\[
M_r=rA_m+B.
\]

Because \(q_{m,0}\) has odd denominator, it has a unique residue
\(u_r\pmod{2^{M_r}}\). Choose its representative
\(0\le u_r<2^{M_r}\), and set

\[
n^{(r)}_0=u_r+2^{M_r}.
\]

This is a positive odd integer with

\[
2^{M_r}\le n^{(r)}_0<2^{M_r+1},
\qquad
\nu_2(n^{(r)}_0-q_{m,0})\ge M_r. \tag{4}
\]

Starting at \(n^{(r)}_0\), apply the accelerated map and write the states as

\[
n^{(r)}_0,n^{(r)}_1,\ldots,n^{(r)}_{rm}.
\]

We claim that the first \(rm\) exact valuations repeat \(w_m\). Suppose the
cumulative prescribed valuation before time \(j\) is \(E_j\). Inductively,

\[
\nu_2\bigl(n^{(r)}_j-q_{m,j\bmod m}\bigr)
\ge M_r-E_j. \tag{5}
\]

Before every one of the first \(rm\) transitions, the right side of (5)
is strictly greater than the next prescribed valuation: after that valuation
is spent, at least the reserve \(B\ge1\) remains. In

\[
3n^{(r)}_j+1=
(3q_{m,j\bmod m}+1)
+3(n^{(r)}_j-q_{m,j\bmod m}),
\]

the second summand consequently has larger \(2\)-adic valuation than the
first. The ultrametric equality makes the valuation of the sum exactly the
prescribed one. Division by that power of two proves the next instance of
(5). This completes the induction, including the final transition, and gives

\[
\nu_2\bigl(n^{(r)}_j-q_{m,j\bmod m}\bigr)\ge B
\quad(0\le j\le rm). \tag{6}
\]

These are genuine positive-integer Collatz prefixes; the negative rational
cycle is used only to prescribe their finite exact itinerary.

## 6. Phasewise sensor freezing

By (2), every \(q_{m,i}-c_\ell\) is nonzero. Equations (3) and (6) give

\[
\nu_2(n^{(r)}_j-q_{m,j\bmod m})
>
\nu_2(q_{m,j\bmod m}-c_\ell).
\]

The ultrametric equality therefore yields

\[
\nu_2(n^{(r)}_j-c_\ell)
=
\nu_2(q_{m,j\bmod m}-c_\ell). \tag{7}
\]

Thus \(\Sigma_C(n^{(r)}_j)\), and hence the correction term \(R\), depends
only on \(j\bmod m\) throughout the entire depth-\(r\) shadow.

## 7. Same-phase growth and the last minimum

The composition over one period is affine with multiplier \(\lambda_m\) and
fixed point \(q_{m,i}\) at phase \(i\). Hence

\[
n^{(r)}_{i+(k+1)m}-q_{m,i}
=
\lambda_m\bigl(n^{(r)}_{i+km}-q_{m,i}\bigr). \tag{8}
\]

Since \(q_{m,i}<0\), \(n^{(r)}_{i+km}>0\), and \(\lambda_m>1\), equation
(8) implies

\[
n^{(r)}_{i+(k+1)m}>n^{(r)}_{i+km}. \tag{9}
\]

The correction is equal at these two states by (7), while \(\alpha>0\).
Therefore \(V\) strictly increases on every same-phase return.

Let \(j_r\) be the last global minimizer of \(V\) on the finite displayed
shadow. Each phase has its minimum at its first occurrence, so

\[
0\le j_r<m. \tag{10}
\]

By the choice of the last global minimizer,

\[
V(n^{(r)}_j)>V(n^{(r)}_{j_r})
\quad(j_r<j\le rm). \tag{11}
\]

## 8. Horizon contradiction

During the first period, every accelerated step satisfies
\(S(n)\le2n\). From (4), for \(0\le j<m\),

\[
\log_2 n^{(r)}_j<rA_m+B+m. \tag{12}
\]

The first-period states also tend to infinity with \(r\); for example, the
single valuation-\(2\) step loses at most a factor \(3/4\), and every later
valuation-\(1\) step grows.

Put

\[
N_r=n^{(r)}_{j_r}.
\]

By (1), \(m-\beta A_m>0\). Equations (10)--(12) show that for all sufficiently
large \(r\), both \(N_r\ge N_0\) and

\[
\lfloor\beta\log_2N_r\rfloor
\le rm-j_r. \tag{13}
\]

Every iterate in the range (13) remains inside the exact displayed shadow.
Equation (11) then gives

\[
V(S^\tau(N_r))>V(N_r)
\]

for every
\(1\le\tau\le\lfloor\beta\log_2N_r\rfloor\), proving the theorem.

## 9. Scope boundary

The theorem rules out exactly the displayed architecture. It does not rule
out:

- horizons with coefficient \(\beta\ge1\) or non-logarithmic horizons;
- infinitely many, adaptive, or input-dependent centers;
- features that do not freeze on these periodic shadows;
- dynamic memory, automata, matrices, or other augmented states;
- ranking architectures not expressible as the displayed corrected-log form.

It neither proves nor disproves the Collatz conjecture.
