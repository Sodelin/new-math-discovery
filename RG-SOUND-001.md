# RG-SOUND-001: soundness of ranked coalescence graphs

## 1. Status and purpose

This note freezes the mathematical interface for a finite recursive
residue/coalescence certificate.

It proves a general soundness theorem:

> if finitely described symbolic configurations cover every positive
> integer, every nonterminal configuration has an exact finite Collatz
> coalescence edge to a strictly lower-ranked configuration, and the declared
> rank is genuinely well-founded, then the Collatz conjecture follows.

This is a certificate-semantics theorem, not an exhibited global certificate.
The remaining construction problem is to supply finite graph data satisfying
all validity conditions below.

## 2. Stopped ordinary Collatz map

Use the stopped ordinary Collatz map

\[
T(n)=
\begin{cases}
1,&n=1,\\
n/2,&n>1\text{ and }n\text{ is even},\\
3n+1,&n>1\text{ and }n\text{ is odd}.
\end{cases}
\]

This agrees with the ordinary Collatz map until the first visit to \(1\), and
then fixes \(1\). Define

\[
\operatorname{Conv}(n)
\quad\Longleftrightarrow\quad
\exists k\ge0\;T^k(n)=1.
\]

Two elementary facts will be used.

**Tail lemma.** If \(\operatorname{Conv}(n)\), then
\(\operatorname{Conv}(T^b(n))\) for every \(b\ge0\).

Indeed, if \(T^k(n)=1\), then \(T^b(n)\) reaches \(1\) after \(k-b\) steps
when \(b\le k\), and already equals \(1\) when \(b>k\).

**Coalescence lemma.** If

\[
T^a(n)=T^b(m)
\]

for some \(a,b\ge0\), and \(\operatorname{Conv}(m)\), then
\(\operatorname{Conv}(n)\).

By the tail lemma, \(T^b(m)\) reaches \(1\). The displayed equality then
places the same convergent tail after \(a\) steps of the orbit of \(n\).

## 3. Abstract ranked coalescence system

An abstract ranked coalescence system consists of:

1. a type \(\mathcal C\) of symbolic configurations;
2. a decoder

   \[
   \delta:\mathcal C\longrightarrow\mathbb N_{>0}
   \]

   whose values are positive integers;
3. a fixed rank dimension \(d\ge1\) and rank

   \[
   \rho:\mathcal C\longrightarrow\mathbb N^d,
   \]

   ordered lexicographically;
4. an entry predicate \(E\subseteq\mathcal C\);
5. a directed macro-edge relation. An edge

   \[
   c\xrightarrow{a,b}c'
   \]

   carries fixed natural numbers \(a,b\) and certifies

   \[
   T^a(\delta(c))=T^b(\delta(c')). \tag{1}
   \]

The system is **valid** when it satisfies all three semantic conditions:

### V1. Entry coverage

Every positive integer has an entry representation:

\[
\forall n\in\mathbb N_{>0}\;\exists c\in E,
\qquad \delta(c)=n. \tag{2}
\]

Injectivity and disjointness are not required for soundness.

### V2. Total nonterminal progress

Every configuration not decoding to \(1\) has at least one outgoing exact
macro edge:

\[
\delta(c)>1
\Longrightarrow
\exists c',a,b\ge0,
\qquad c\xrightarrow{a,b}c'. \tag{3}
\]

### V3. Strict rank decrease

Every macro edge strictly decreases the declared lexicographic rank:

\[
c\xrightarrow{a,b}c'
\Longrightarrow
\rho(c')<_{\mathrm{lex}}\rho(c). \tag{4}
\]

There is deliberately no requirement that
\(\delta(c')<\delta(c)\). Temporary numerical growth is permitted; all
recursive progress is carried by the independently checked rank.

## 4. Soundness theorem

**Theorem (RG-SOUND-001).** Every valid abstract ranked coalescence system
proves convergence of every positive integer under \(T\). Consequently it
proves the ordinary Collatz conjecture and the equivalent accelerated global
descent property.

### Proof

Lexicographic order on \(\mathbb N^d\) is well-founded for every fixed finite
\(d\). We prove

\[
\operatorname{Conv}(\delta(c))
\]

for every configuration \(c\), by well-founded induction on \(\rho(c)\).

Fix \(c\), and assume as induction hypothesis that

\[
\forall c'\in\mathcal C,\qquad
\rho(c')<_{\mathrm{lex}}\rho(c)
\Longrightarrow
\operatorname{Conv}(\delta(c')). \tag{5}
\]

If \(\delta(c)=1\), convergence is immediate. Otherwise
\(\delta(c)>1\), so V2 supplies an edge

\[
c\xrightarrow{a,b}c'.
\]

By V3, \(\rho(c')<_{\mathrm{lex}}\rho(c)\), and (5) gives
\(\operatorname{Conv}(\delta(c'))\). Edge validity supplies the exact
coalescence identity (1), so the coalescence lemma gives
\(\operatorname{Conv}(\delta(c))\). This completes the well-founded
induction.

Now let \(n\) be any positive integer. V1 supplies an entry configuration
\(c\) with \(\delta(c)=n\), and the result just proved gives
\(\operatorname{Conv}(n)\). Thus every positive integer converges.

Finally, the stopped map agrees with the ordinary Collatz map up to the first
visit to \(1\). Hence this is exactly the ordinary Collatz conjecture. Since
every odd \(n>1\) then reaches \(1<n\), it also implies accelerated global
descent. \(\square\)

## 5. Finite guarded graph certificate

The abstract theorem separates soundness from representation. A finite
machine-checkable certificate instantiates \(\mathcal C\) as finitely many
node types with possibly infinite parameter domains.

### 5.1 Finite data

A finite guarded graph certificate contains:

1. a finite node set \(Q\);
2. for each node \(q\), an explicitly decidable parameter domain
   \(D_q\subseteq\mathbb N^{r_q}\);
3. for each node, a decoder

   \[
   \delta_q:D_q\longrightarrow\mathbb N_{>0};
   \]

4. for each designated entry node \(q\), an entry-domain predicate
   \(I_q\subseteq D_q\);
5. a fixed rank dimension \(d\) and explicit rank expressions

   \[
   \rho_q:D_q\longrightarrow\mathbb N^d;
   \]

6. finitely many edges. An edge \(e:q\to q'\) contains:

   - an explicitly described edge-parameter domain \(P_e\);
   - a raw source refinement map
     \(\sigma_e:P_e\to\mathbb N^{r_q}\);
   - a raw target parameter map
     \(\phi_e:P_e\to\mathbb N^{r_{q'}}\);
   - fixed macro lengths \(a_e,b_e\ge0\);
   - a source trace containing exactly \(a_e\) stopped-map steps and a target
     trace containing exactly \(b_e\) stopped-map steps;
   - an exact symbolic identity equating the two trace endpoints.

Its configurations are pairs \((q,p)\) with \(p\in D_q\). The decoder and
rank are \(\delta(q,p)=\delta_q(p)\) and
\(\rho(q,p)=\rho_q(p)\). The abstract entry set is

\[
E=\{(q,p):q\text{ is designated entry},\ p\in D_q,
\text{ and }I_q(p)\}. \tag{6}
\]

Once source and target closure are verified, each \(y\in P_e\) instantiates
the abstract edge

\[
(q,\sigma_e(y))\xrightarrow{a_e,b_e}(q',\phi_e(y)). \tag{7}
\]

### 5.2 Semantic validity obligations and proof evidence

The certificate is accepted only after checking all of the following.

The node and edge tables are finite, but their parameter domains may be
infinite. Finiteness of the tables alone does **not** make the quantified
conditions below decidable. A concrete certificate format must therefore
either restrict all domains and expressions to a theory with a proved decision
procedure, or carry finite proof objects that a trusted checker validates.

**F1. Domain safety.** Every decoder value is a positive integer, and
every rank coordinate is a natural number, throughout its whole declared
domain.

**F2. Exact entry coverage.** The entry families satisfy

\[
\forall n\in\mathbb N_{>0}\;\exists(q,p)\in E,
\qquad \delta_q(p)=n. \tag{8}
\]

Coverage is a proved arithmetic identity or finite congruence partition, not
a bounded sample.

**F3. Source coverage.** For every \(p\in D_q\) with
\(\delta_q(p)>1\), there are an outgoing edge \(e:q\to q'\) and a parameter
\(y\in P_e\) such that

\[
\sigma_e(y)=p. \tag{9}
\]

Source images may overlap for soundness, although a checker may require a
disjoint partition for deterministic replay.

**F4. Source and target closure.** For every \(y\in P_e\),

\[
\sigma_e(y)\in D_q,
\qquad
\phi_e(y)\in D_{q'}. \tag{10}
\]

**F5. Uniform trace validity and length.** The source trace replays exactly
\(a_e\) applications of \(T\), and the target trace replays exactly \(b_e\)
applications. Every stopped, even, or odd branch decision in those traces is
correct for every \(y\in P_e\), when started respectively from
\(\delta_q(\sigma_e(y))\) and \(\delta_{q'}(\phi_e(y))\). The trace semantics
uses the stopped rule at \(1\); a domain containing an exceptional value that
reaches \(1\) during a nominal affine trace must be split or checked explicitly.

**F6. Exact coalescence.** For every \(y\in P_e\),

\[
T^{a_e}(\delta_q(\sigma_e(y)))
=
T^{b_e}(\delta_{q'}(\phi_e(y))). \tag{11}
\]

This must be a symbolic integer identity after replaying the certified traces.

**F7. Uniform strict rank decrease.** For every \(y\in P_e\),

\[
\rho_{q'}(\phi_e(y))
<_{\mathrm{lex}}
\rho_q(\sigma_e(y)). \tag{12}
\]

The decrease is proved over the whole edge domain. Checking representative
parameters or showing decrease on average is invalid.

Conditions F1--F7 imply V1--V3: F2 gives entry coverage; F3 chooses an
instantiated outgoing edge for every nonterminal configuration; F4 makes that
edge well-typed; F5--F6 prove its stopped-map coalescence semantics; and F7
gives strict rank decrease. Thus RG-SOUND-001 applies immediately. Neither
nonunique decoders nor overlapping source images affect this implication.

## 6. Affine residue specialization

One possible exact checker language uses one natural parameter per node and
affine decoders

\[
\delta_q(x)=A_qx+B_q,
\qquad x\in D_q\subseteq\mathbb N,
\]

where \(D_q\) is a finite union of congruence classes with lower bounds. An
edge likewise uses a one-dimensional domain \(P_e\) and explicit maps

\[
\sigma_e(y)=M_ey+r_e,
\qquad 0\le r_e<M_e,
\]

and

\[
\phi_e(y)=P_ey+Q_e.
\]

The images of the source maps must prove F3; merely listing residue refinements
does not establish totality.

After splitting the edge domain so that every step has uniform
stopped/even/odd status as required by F5, every iterate of an affine family
remains affine (with the stopped branch represented by the constant affine
family \(1\)).
If the rank coordinates are affine, piecewise affine, or otherwise definable
in a chosen decidable arithmetic language, F1--F7 reduce to finitely many
formulas in that language plus exact affine endpoint identities. A trusted
decision procedure or replayable proof objects must discharge those formulas;
bounded enumeration is insufficient.

Affine ranks are only a reference specialization, not an assertion that this
rank class can solve the remaining Collatz graph. The abstract semantics allow
nonlinear rank expressions into \(\mathbb N^d\), provided domain safety and
strict edge decrease have independently checkable proofs.

This specialization contains ordinary direct descent and the existing
coalescence examples:

- direct descent uses a target decoder equal to a smaller iterate;
- a coalescence identity such as

  \[
  T^9(64x+15)=T(54x+13)
  \]

  becomes an edge once its target family is represented and the chosen global
  rank decreases;
- an abstract back-edge is permitted only when its parameter transformation
  makes (12) hold.

## 7. Anti-circularity requirements

A purported certificate is rejected if any of the following is used inside
its validation:

- an assumption that the source or target orbit eventually reaches \(1\);
- an unbounded existential search for a future good iterate;
- a rank defined using stopping time, convergence, or another unknown orbit
  property;
- sampled rather than universal parity, coverage, identity, or decrease
  checks;
- an uncovered parameter branch, or a symbolic strongly connected component
  for which source coverage or strict instantiated-edge decrease has not been
  discharged (node-level cycles are allowed when every traversal satisfies
  F7);
- a rank whose codomain or order has not been proved well-founded;
- a target map that silently leaves its declared domain;
- a modulus- or depth-bounded cover promoted to all positive integers.

The macro lengths and traces are finite certificate data. The checker verifies
only exact arithmetic and the general soundness theorem; it does not trust the
program that generated the graph.

## 8. Exact remaining construction target

RG-SOUND-001 closes the semantic question but does not provide the graph.
The next constructive milestone is a concrete finite certificate satisfying
F1--F7.

A candidate must therefore provide, in one reviewable bundle:

1. the finite node, domain, decoder, guard, and target tables;
2. exact entry coverage of all positive integers;
3. exact parity traces and coalescence identities for every edge;
4. a fixed-dimensional natural-valued rank with strict decrease on every
   guarded edge;
5. a dependency-free checker that replays F1--F7;
6. an independent proof that the checker implements this document's semantics.

Until such data exist, the Collatz conjecture remains unresolved.

## 9. Formal verification boundary

The core theorem is compiled in
[`lean/NewMathDiscovery/RankedCoalescenceSound.lean`](lean/NewMathDiscovery/RankedCoalescenceSound.lean).
Lean currently verifies:

- finite iteration and iteration composition;
- persistence of a fixed terminal state;
- the tail and exact coalescence-transfer lemmas;
- well-founded induction for an arbitrary pulled-back configuration rank;
- progress, exact-edge, and strict-decrease semantics;
- lifting configuration soundness through an entry-coverage predicate.

The dependency report contains only Lean's standard `propext`,
`Classical.choice`, and `Quot.sound`; it contains no `sorryAx` and no
Collatz-specific axiom.

The current Lean module does **not** yet formalize:

- the stopped ordinary Collatz function or its equivalence to the standard and
  accelerated formulations;
- positive decoder safety;
- lexicographic well-foundedness for a concrete \(\mathbb N^d\) rank;
- finite guarded tables, parity-trace replay, or the F1--F7 checker.

Accordingly, the formal result is the abstract soundness kernel, not a formal
proof of Collatz and not yet a formal checker for a concrete graph.
