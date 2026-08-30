# Verification artifacts

All programs in this directory use only the Python standard library. Run them
from the repository root without optimized mode.

## Artifact roles

| Artifact | Role |
|---|---|
| `check_h_fcs_001.py` | Exact finite diagnostics supporting H-FCS-001 |
| `check_rg_cert0.py` | Independent, fail-closed RG-CERT-0/v0 checker |
| `build_rg_cert0_route_b.py` | Deterministic but untrusted Route B producer |
| `rg_cert0_route_b_k12.json` | Static partial certificate data |
| `check_rg_macro_001.py` | Formula-only reconstruction of the K=12 macro classification |
| `*_output.txt` | Retained reviewed transcripts |

The producer is not part of the trusted proof path. The checker validates the
serialized data from scratch: schema, stopped-map traces, source/target
closure, affine endpoint identities, uniform rank decrease, and exact source
coverage.

## Commands

```powershell
python -B verification/check_h_fcs_001.py
python -B verification/check_rg_cert0.py --self-test
python -B verification/check_rg_cert0.py verification/rg_cert0_route_b_k12.json
python -B verification/check_rg_cert0.py --require-global verification/rg_cert0_route_b_k12.json
python -B verification/check_rg_macro_001.py --self-test
python -B verification/check_rg_macro_001.py
```

The ordinary audit exits zero because it verifies an explicitly partial
artifact. The `--require-global` command exits nonzero: 145 source residues
modulo 4,096 remain uncovered, so F3 is incomplete.

To reproduce the bundle without overwriting the reviewed file, choose a new
output path:

```powershell
python -B verification/build_rg_cert0_route_b.py --output <new-json-path>
```

The reviewed rebuild was byte-identical to the retained JSON. Checksums and
archive lineage are recorded in [PROVENANCE.md](../PROVENANCE.md).

`check_rg_macro_001.py` does not import or execute the producer.  It applies
the closed formulas in [RG-MACRO-001.md](../RG-MACRO-001.md) to every odd
\(K=12\) cylinder, reconstructs the exact selected affine target, trace, and
stopped lower bound for all 1,903 Route B edges, and compares the resulting
145-cylinder complement with the static bundle.  Its success is an exact
finite symbolic classification, not global source coverage.

The macro classifier also freezes the static partial claim, map name, and two
non-Route-B records, but it does not re-prove their F1--F7 semantics.  Always
run `check_rg_cert0.py` as the authoritative companion bundle gate.
