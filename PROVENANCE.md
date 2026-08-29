# Provenance

This repository is a clean theorem-facing reconstruction. The broader source
archive is
[Sodelin/Collatz-Conjecture-Work](https://github.com/Sodelin/Collatz-Conjecture-Work).

## Accepted archive baseline

The reconstruction began from archive commit
[`2e7eae2bb998b14e5443e6c440154130a0049467`](https://github.com/Sodelin/Collatz-Conjecture-Work/tree/2e7eae2bb998b14e5443e6c440154130a0049467).

Relevant tracked source notes are:

- [Round 6A public review note](https://github.com/Sodelin/Collatz-Conjecture-Work/blob/2e7eae2bb998b14e5443e6c440154130a0049467/papers/round-6a/Theorem_6A1_Public_Review_Note.md),
  especially its exact rational-period positive-shadow construction and the
  family \(w_m=(2,1^{m-1})\);
- [Round 6B public summary](https://github.com/Sodelin/Collatz-Conjecture-Work/blob/2e7eae2bb998b14e5443e6c440154130a0049467/papers/round-6b/Round6B_Public_Summary.md),
  which identifies phase-frozen finite-sensor surrogates as an obstruction
  target;
- [Failure ledger F004](https://github.com/Sodelin/Collatz-Conjecture-Work/blob/2e7eae2bb998b14e5443e6c440154130a0049467/proof-search/FAILURE_LEDGER.md#f004--finitely-many-fixed-2-adic-proximity-sensors-suffice),
  which records the earlier bounded architecture verdict.

`H-FCS-001` is presented here as a standalone direct theorem. It does not use
the quantitative debt conclusion of Theorem 6A.1; it uses the underlying
periodic-cycle and exact-lift construction and then applies a direct
last-minimum argument.

## Working-tree diagnostic source

The first exact diagnostic program existed as an uncommitted archive working-
tree file on 2026-08-29:

```text
Collatz-Conjecture-Work/verification/finite_center_periodic_shadow_obstruction.py
SHA-256 274300A11A88CFB985C971AFD5B5B4159EDD56883DDFAB707B47EE97299CD3A0
```

Its retained output had checksum:

```text
SHA-256 29E3277EB9A8EB806CE8B4E52738F45F4F0A2089C960DE25E1E59EBB8934F7F8
```

The publication verifier will be tracked directly in this repository and
reviewed independently. These checksums preserve the pre-import lineage
without pretending the uncommitted files belonged to the archive baseline.

## Reviewed publication artifacts

The internal mathematical and reproducibility audits reviewed these exact
artifacts:

```text
THEOREM.md
SHA-256 554C4AAD25F3DB87C9B3D40EE6B595D69072C9C6CD1BE185F854FBFAF7D8C581

verification/check_h_fcs_001.py
SHA-256 0327F7958A0BC246A9BEC5EA89D89947738EAC01E781482CB3188578F65A424A
```

The verifier was run successfully with Python 3.14.7 using the documented
command. A separate optimized-mode run exited before printing any `PASS`, as
required by the fail-closed guard.
