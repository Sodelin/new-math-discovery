# New Math Discovery

This repository presents a focused obstruction theorem for one proposed
Collatz ranking architecture.

> **Mathematical status:** this is not a proof or disproof of the Collatz
> conjecture. The current result rules out a precisely stated class of
> finite-fixed-center corrected-log potentials with a sub-bitlength descent
> horizon.

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
- [STATUS.md](STATUS.md) states exactly what is and is not claimed.
- [PROVENANCE.md](PROVENANCE.md) maps this reconstruction to its source archive.
- [`verification/check_h_fcs_001.py`](verification/check_h_fcs_001.py) checks
  the finite algebra and representative exact shadows; it does not replace any
  infinite or uniform argument.

The verifier requires Python 3.8 or newer and uses only the standard library.
Run it from the repository root without optimized mode:

```powershell
python -B verification/check_h_fcs_001.py
```

The reviewed transcript is retained in
[`verification/check_h_fcs_001_output.txt`](verification/check_h_fcs_001_output.txt).

The broader exploratory archive remains in
[Sodelin/Collatz-Conjecture-Work](https://github.com/Sodelin/Collatz-Conjecture-Work).
