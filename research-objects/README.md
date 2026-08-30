# Research-bank exports

This directory is the source-side export boundary for immutable research-bank
snapshots from `Sodelin/new-math-discovery`.

The repository remains authoritative for the current theorem wording, status,
Lean source, checker code, exact certificate boundary, and corrections. The
bank may store pinned snapshots and annotations; it may not promote or rewrite
source-repository status.

Each exported object must bind:

- repository, commit, path, and content digest;
- exact statement or finite scope;
- status at the snapshot time;
- verification methods and their non-implications;
- source/provenance bindings;
- toolchain or interpreter details when executable;
- license and human-review metadata;
- invalidation triggers and any superseding object.

Lean and checker files copied into the bank are immutable replay bundles, not a
second mutable proof tree. A bank annotation is untrusted input until a scoped
source-side review accepts it. A changed dependency taints affected verdicts
until replayed or narrowed.

The initial [`BANK_EXPORT_MANIFEST.json`](BANK_EXPORT_MANIFEST.json) includes
H-FCS-001, RG-SOUND-001, the abstract Lean kernel, the RG-CERT-0 specification
and checker, and the K=12 partial bundle. The manifest preserves the decisive
boundary: 145 source residues remain uncovered, so the bundle is not a global
certificate and the Collatz conjecture remains unresolved.
