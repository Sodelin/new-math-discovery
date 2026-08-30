# New Math Discovery

This repository presents a focused obstruction theorem, an audited global
certificate semantics, and a concrete exact partial construction for the
Collatz problem.

> **Mathematical status:** this is not a proof or disproof of the Collatz
> conjecture. The obstruction rules out a precisely stated method class. The
> current graph bundle validates 1,905 exact edges but still fails global
> source coverage on 145 residue classes.

## Main result

Let

\[
S(n)=\frac{3n+1}{2^{\nu_2(3n+1)}}
\]

be the accelerated odd Collatz map. Fix finitely many rational centers
\(c_1,\ldots,c_s\). For any \(\alpha>0\), any correction function \(R\),
and any \(0<\beta<1\), a potential of the form

\[
V(n)=\alpha\log_2 n+
R\!\left(\nu_2(n-c_1),\ldots,\nu_2(n-c_s)\right)
\]

cannot guarantee a non-increase within
\(\lfloor\beta\log_2 n\rfloor\) accelerated steps for every sufficiently
large positive odd \(n\).

The stronger quantified statement and proof are in [THEOREM.md](THEOREM.md).

## Global construction interface

[RG-SOUND-001.md](RG-SOUND-001.md) defines a finite guarded
residue/coalescence graph certificate and proves the general soundness theorem:
exact coverage of all positive integers, total finite coalescence progress,
and strict decrease in a well-founded rank imply Collatz convergence. The
theorem permits temporary numerical growth.

[RG-CERT-0.md](RG-CERT-0.md) freezes the first concrete checker language. Its
one-node bootstrap specialization uses the exact numerical rank. The retained
\(K=12\) bundle contains:

- one uniform edge covering every even decoded input;
- 1,903 exact smaller-target edges for odd residue cylinders;
- one stopped-map singleton repair for \(n=3\); and
- 145 explicitly reported uncovered source residues modulo 4,096.

All 1,905 serialized edges pass exact stopped-map trace, closure,
coalescence-identity, and rank-decrease checks. F3 source coverage is
incomplete, so the bundle is a precise construction boundary rather than a
global Collatz certificate.

[RG-MACRO-001.md](RG-MACRO-001.md) replaces the operational description of
that boundary by exact formulas.  It proves a universal one-bit affine
refinement theorem and shows that all 1,903 Route B targets use only empty,
`O`, or the family

\[
O(EO)^kEEO,
\qquad 1\le k\le6.
\]

A separate formula classifier reconstructs the selected affine data and the
exact 145-cylinder complement without importing or executing the archived
breadth-first search.  This completes the symbolic-description gate; finite
transition closure is supplied separately below.

[RG-TRANS-001.md](RG-TRANS-001.md) now closes the transition side globally.
Every positive integer has a unique label

\[
N_{r,\eta}(w)=2^r(4w+2\eta+1)-1.
\]

A five-row parametric table sends every soft label to an exact smaller
coalescing target and closes the remaining hard labels under one return map
\(F\).  An odd-affine valuation theorem places every instance of all 145 gaps
into that table.  This is a global transition construction, but not a Collatz
proof: termination of \(F\) is Collatz-equivalent, and no independent
well-founded rank for all \(F\)-edges is known.

The abstract kernel is compiled in
[`lean/NewMathDiscovery/RankedCoalescenceSound.lean`](lean/NewMathDiscovery/RankedCoalescenceSound.lean).
No globally ranked graph satisfying all obligations F1--F7 is claimed.
Transition coverage is now global, but constructing an independent rank that
decreases on every hard return is the remaining research target.
[CONSTRUCTION.md](CONSTRUCTION.md) is the canonical dependency-gated backlog
for that target.

## Why the obstruction works

An infinite family of pairwise-disjoint negative rational periodic orbits has
valuation words

\[
w_m=(2,1,\ldots,1).
\]

For any finite center set, one can choose a sufficiently long orbit avoiding
every center. Positive odd integers can shadow that orbit exactly for an
arbitrary number of periods. Along the shadow, all fixed-center valuation
sensors freeze phase by phase, while the real orbit grows on every same-phase
return. A last-minimum argument then produces arbitrarily large inputs with no
potential non-increase inside the claimed sub-bitlength horizon.

## Repository contract

- [THEOREM.md](THEOREM.md) is the human-checkable mathematical artifact.
- [RG-SOUND-001.md](RG-SOUND-001.md) is the audited global-certificate
  semantics and construction specification.
- [RG-CERT-0.md](RG-CERT-0.md) is the audited exact bootstrap data language.
- [RG-MACRO-001.md](RG-MACRO-001.md) is the closed-form symbolic compression
  of the current partial-certificate frontier.
- [RG-TRANS-001.md](RG-TRANS-001.md) is the exact global parametric transition
  table and hard-return reduction.
- [CONSTRUCTION.md](CONSTRUCTION.md) is the single active global-construction
  backlog and architecture filter.
- [STATUS.md](STATUS.md) states exactly what is and is not claimed.
- [PROVENANCE.md](PROVENANCE.md) maps this reconstruction to its source archive.
- [`verification/check_h_fcs_001.py`](verification/check_h_fcs_001.py) checks
  the finite algebra and representative exact shadows; it does not replace any
  infinite or uniform argument.
- [`verification/check_rg_cert0.py`](verification/check_rg_cert0.py) is the
  fail-closed independent checker; the producer is deliberately separate.
- [`verification/check_rg_macro_001.py`](verification/check_rg_macro_001.py)
  independently reconstructs the finite macro classification from formulas.
- [`verification/rg_cert0_route_b_k12.json`](verification/rg_cert0_route_b_k12.json)
  is the static partial certificate data.
- [`verification/README.md`](verification/README.md) explains the trusted
  checker/untrusted producer boundary and all reproduction commands.
- [`research-objects/README.md`](research-objects/README.md) defines the
  source-versus-bank ownership boundary.
- [`research-objects/BANK_EXPORT_MANIFEST.json`](research-objects/BANK_EXPORT_MANIFEST.json)
  pins immutable source-side export candidates and their exact non-implications.

The shared research bank may index or annotate pinned snapshots. This
repository remains authoritative for mutable theorem wording, status, Lean
source, checker code, certificate coverage, and corrections. Bank annotations
cannot promote a claim here.

The verifier requires Python 3.8 or newer and uses only the standard library.
Run it from the repository root without optimized mode:

```powershell
python -B verification/check_h_fcs_001.py
```

The reviewed transcript is retained in
[`verification/check_h_fcs_001_output.txt`](verification/check_h_fcs_001_output.txt).

Compile and axiom-audit the abstract ranked-coalescence soundness theorem with
the pinned Lean 4.33.1 toolchain:

```powershell
lake build
```

The reviewed transcript is retained in
[`verification/lean_rg_sound_build_output.txt`](verification/lean_rg_sound_build_output.txt).

Audit the static partial construction:

```powershell
python -B verification/check_rg_cert0.py --self-test
python -B verification/check_rg_cert0.py verification/rg_cert0_route_b_k12.json
```

Require a genuinely global result with the stricter gate below. It currently
exits nonzero because 145 residue classes remain uncovered:

```powershell
python -B verification/check_rg_cert0.py --require-global verification/rg_cert0_route_b_k12.json
```

The deterministic, untrusted producer can rebuild the static data at a new
path:

```powershell
python -B verification/build_rg_cert0_route_b.py --output <new-json-path>
```

Reviewed build and check transcripts are retained in
[`verification/rg_cert0_route_b_build_output.txt`](verification/rg_cert0_route_b_build_output.txt)
and
[`verification/rg_cert0_route_b_check_output.txt`](verification/rg_cert0_route_b_check_output.txt).

Reproduce the symbolic macro classification:

```powershell
python -B verification/check_rg_macro_001.py --self-test
python -B verification/check_rg_macro_001.py
```

The retained transcript is
[`verification/check_rg_macro_001_output.txt`](verification/check_rg_macro_001_output.txt).

The broader exploratory archive remains in
[Sodelin/Collatz-Conjecture-Work](https://github.com/Sodelin/Collatz-Conjecture-Work).
