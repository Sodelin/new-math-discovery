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

The ranked-coalescence soundness reconstruction also uses:

- [Route B: recursive residue/coalescence certificate graph](https://github.com/Sodelin/Collatz-Conjecture-Work/blob/2e7eae2bb998b14e5443e6c440154130a0049467/proof-search/routes/B_recursive_residue_graph.md),
  which proposed `ValidCoalescenceGraph cert -> Collatz` without previously
  freezing its semantics;
- [L0: global descent equivalence](https://github.com/Sodelin/Collatz-Conjecture-Work/blob/2e7eae2bb998b14e5443e6c440154130a0049467/proof-search/lemmas/L0_Global_Descent_Equivalence.md),
  which supplies the exact Collatz endpoint;
- [Lean verification policy](https://github.com/Sodelin/Collatz-Conjecture-Work/blob/2e7eae2bb998b14e5443e6c440154130a0049467/lean/VERIFICATION_POLICY.md),
  which requires general certificate soundness before untrusted search.
- [Round 7 affine coalescence search](https://github.com/Sodelin/Collatz-Conjecture-Work/blob/2e7eae2bb998b14e5443e6c440154130a0049467/verification/round7_affine_coalescence_search.py),
  which supplies the bounded ordinary-map Route B certificates imported by
  RG-CERT-0.
- [L13 refined Mersenne child macros](https://github.com/Sodelin/Collatz-Conjecture-Work/blob/2e7eae2bb998b14e5443e6c440154130a0049467/proof-search/lemmas/L13_Refined_Mersenne_Child_Macros.md),
  which proves the compatible smaller-target identity and hard-child affine
  normalization used by RG-TRANS-001.
- [Hard-boundary return system](https://github.com/Sodelin/Collatz-Conjecture-Work/blob/2e7eae2bb998b14e5443e6c440154130a0049467/proof-search/routes/AB_hard_boundary_return_system.md),
  which records the total soft normalizer, closed hard return, exact
  Collatz-equivalence boundary, and first replay-rank recharge witness.

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

The RG-SOUND-001 paper and Lean artifact were reconstructed in this repository
from the cited archive interfaces. They do not copy or claim completion of a
pre-existing graph certificate.

```text
RG-SOUND-001.md
SHA-256 65713EEFA86916EF4514BBF9513B113FA7499D4E148CEC18593A1B67079424D3

lean/NewMathDiscovery/RankedCoalescenceSound.lean
SHA-256 2F6B8B6DC0BA491A17ED1C4B31A8C8ECF56D3F9EDE3E91DE595379A007E97EAF

verification/lean_rg_sound_build_output.txt
SHA-256 A390D38FD77B09ED1258C5F43F0535AC6E86D5A6703AC4B08C6598673FE0A2AE
```

The RG-SOUND paper checksum changed when the decoder and entry coverage were
generalized consistently from positive odd integers to all positive integers.
The abstract Lean kernel was already carrier-generic, so its source and build
transcript did not change.

## RG-CERT-0 Route B reconstruction

The imported archive source had this working-copy checksum on 2026-08-29; it
was tracked and unmodified relative to the accepted archive baseline:

```text
Collatz-Conjecture-Work/verification/round7_affine_coalescence_search.py
SHA-256 36CF236477063D915B470343713DCEE2A4F0D53A9FCA80C9DAD5F1226655D8A1
```

That archive program checks the unstopped ordinary map, for which \(U(1)=4\).
The publication producer reconstructs the search, translates its data to the
stopped map required by RG-SOUND-001, and emits static JSON. This translation
found one boundary exception: the \(R=3\) family had to start at \(x=1\), and
the excluded input \(n=3\) received the explicit stopped trace `OEOEEEE` to
\(1\).

The schema, independent checker, untrusted producer, and exact data reviewed
for this milestone are:

```text
RG-CERT-0.md
SHA-256 53AC5DBE8A3FB1A17A3879863C050BAAB818999601E151948CD387DCBBBA86FA

verification/check_rg_cert0.py
SHA-256 7D6F5A61FB5D718C4F45265E30A0B9715472911FC5D2A9F607DDF928B8B2FA6A

verification/build_rg_cert0_route_b.py
SHA-256 00AFE86AD0EC5F8BF6ABF4F279297E859B50E6AEFA9F93A5E475FE8416BE7B5E

verification/rg_cert0_route_b_k12.json
SHA-256 5599F8C39449D944543E52377DA6E20C2FA941902B0403E9EC17BF3BBA25812B

verification/rg_cert0_route_b_build_output.txt
SHA-256 2B6A142F21FBBA724905A79096A243E3361F10124AB383F23DAB1337E51D2A46

verification/rg_cert0_route_b_check_output.txt
SHA-256 6DB64CD87860DF1052BA960A931EB007E02E2C4DBC0150EBC2A0BBC41C1D44E7
```

An independent audit rebuilt the JSON byte-for-byte and attacked the checker
with a false global claim, an empty coverage report, corrupted traces and
endpoints, removal of the \(n=3\) repair, duplicate JSON keys, nonstandard
constants, boolean numerics, and optimized Python mode. Every hostile case
exited nonzero without printing `GLOBAL RG-CERT-0 PASS`.

The accepted partial bundle has 1,905 universally valid edges and exactly 145
uncovered source residues modulo 4,096. It does not satisfy F3 and is not a
Collatz proof.

## RG-MACRO-001 symbolic reconstruction

RG-MACRO-001 was derived in the publication repository from the already
reviewed static RG-CERT-0 bundle and the elementary affine trace convention.
It does not claim that the archive stated the resulting closed macro theorem,
and no literature-novelty claim is made.  The archive remains the provenance
source for the original Route B search and its bounded K=12 boundary.

The new classifier does not import or execute that search.  It reconstructs
every uniform source prefix and tests only empty, `O`, and the proved family
\(O(EO)^kEEO\) for \(0\le k\le6\).  Its exact selected affine maps, traces,
stopped lower bounds, and 145-cylinder complement match the static bundle.

The independently reviewed artifacts are:

```text
RG-MACRO-001.md
SHA-256 951E995EB3274E451BA447857EDE5B2EC33F304F5A36D83C36186D68C9C8FFF3

verification/check_rg_macro_001.py
SHA-256 3975A24103EC504B7FE62F9A5962A44027F10F0D0656A40D2D0A8F0FE85185AE

verification/check_rg_macro_001_output.txt
SHA-256 1A0E05C2CAC882CD69017B376F3FA3364E0341154C61B6BA88E2B7A44D678401
```

Independent review rederived the one-bit and target-word formulas, checked
440 pointwise macro cases and 510 affine child refinements, reproduced the
full transcript, and confirmed fail-closed optimized mode.  Hostile mutations
to Route B coefficients and traces, the uncovered set, JSON numeric types and
constants, top-level claim and map labels, non-Route-B records, duplicate
keys, missing edges, and extra edges were all rejected.  The authoritative
RG-CERT-0 checker remains a mandatory companion because RG-MACRO-001 is a
symbolic-classification audit, not a second F1--F7 semantics checker.

## RG-TRANS-001 global transition reconstruction

RG-TRANS-001 reconstructs the accepted archive's L13 and hard-boundary return
identities as one self-contained human theorem.  It adds the explicit
odd-affine valuation-cell lemma that sends every instance of every
RG-CERT-0 gap into the same global parametric table.  This is transition
closure only: the theorem proves that termination of the closed hard return is
Collatz-equivalent and does not claim an independent rank.

```text
RG-TRANS-001.md
SHA-256 8F8D11B5F84653B255AB5DA889E9BC0A207C2630F3AF45B8EA36A0E4059C0F0B
```

Independent review rederived the canonical labels, all three soft
coalescences, hard endpoint, well-founded normalizer, both directions of the
return-map equivalence, affine valuation partition, and the \(31\mapsto91\)
rank-recharge witness.  Review found and repaired one malformed formula token
and one zero-boundary overreach before acceptance, then separately confirmed
the strengthened exact-coalescence statements.  A non-retained exact-integer
diagnostic checked every guard and identity for all positive inputs through
10,000.  The written universal proof, not that bounded diagnostic, is the
artifact.

The construction is a clean publication reconstruction of archived
project-specific consequences of standard parity-affine identities.  No
literature-novelty claim is made.
