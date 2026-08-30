#!/usr/bin/env python3
"""Check the RG-MACRO-001 closed-form classification of RG-CERT-0.

This program does not import or execute the bounded Route B search.  It
reconstructs every K=12 odd source cylinder from elementary affine formulas
and tests only the finite target-word grammar

    empty, O, and w_k = O(EO)^kEEO for 0 <= k <= 6.

It then compares the resulting certificates and the exact 145-cylinder
complement with the retained RG-CERT-0 bundle.  The calculation supports the
human derivation in RG-MACRO-001.md; it is not a global Collatz certificate.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple


if not __debug__:
    raise RuntimeError(
        "RG-MACRO-001 checking is disabled under optimized Python; "
        "rerun without -O."
    )


K = 12
MODULUS = 1 << K
MAX_MACRO_INDEX = 6
EXPECTED_CYLINDERS = 1 << (K - 1)
EXPECTED_CERTIFIED = 1903
EXPECTED_GAPS = 145
EXPECTED_ROUTE_TEMPLATES = {
    "": 1184,
    "O": 638,
    "OEOEEO": 5,
    "OEOEOEEO": 40,
    "OEOEOEOEEO": 20,
    "OEOEOEOEOEEO": 10,
    "OEOEOEOEOEOEEO": 4,
    "OEOEOEOEOEOEOEEO": 2,
}
EXPECTED_TOP_LEVEL_KEYS = {
    "schema",
    "claim",
    "map",
    "coverage_modulus",
    "expected_uncovered",
    "edges",
}
EXPECTED_NON_ROUTE_EDGES = [
    {
        "domain_lower": 0,
        "id": "structural-even",
        "origin": "RG-CERT-0 structural even-input edge",
        "source_param": [2, 1],
        "source_trace": "E",
        "target_param": [1, 0],
        "target_trace": "",
    },
    {
        "domain_lower": 0,
        "id": "stopped-split-p0000000002",
        "origin": "stopped-map split from Route B K=12 R=3 x=0",
        "source_param": [0, 2],
        "source_trace": "OEOEEEE",
        "target_param": [0, 0],
        "target_trace": "",
    },
]


Affine = Tuple[int, int]


class CheckError(RuntimeError):
    """A fail-closed formula-classification error."""


@dataclass(frozen=True)
class FormulaCertificate:
    residue: int
    source_steps: int
    endpoint: Affine
    target: Affine
    source_word: str
    target_word: str
    lower: int


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckError(message)


def ordinary_affine_step(slope: int, intercept: int, symbol: str) -> Affine:
    if symbol == "E":
        require(slope % 2 == 0 and intercept % 2 == 0, "invalid affine E step")
        return slope // 2, intercept // 2
    if symbol == "O":
        require(slope % 2 == 0 and intercept % 2 == 1, "invalid affine O step")
        return 3 * slope, 3 * intercept + 1
    raise CheckError("trace contains a symbol outside E/O")


def replay_affine(start: Affine, word: str) -> Affine:
    slope, intercept = start
    for symbol in word:
        slope, intercept = ordinary_affine_step(slope, intercept, symbol)
    return slope, intercept


def uniform_forward_path(k: int, residue: int) -> List[Tuple[int, int, int, str]]:
    """Return every ordinary affine prefix through k accelerated decisions."""

    modulus = 1 << k
    require(k >= 1, "cylinder exponent must be positive")
    require(0 < residue < modulus and residue % 2 == 1, "invalid odd cylinder")
    slope, intercept = modulus, residue
    word: List[str] = []
    path: List[Tuple[int, int, int, str]] = []
    steps = 0
    while slope % 2 == 0:
        symbol = "E" if intercept % 2 == 0 else "O"
        word.append(symbol)
        slope, intercept = ordinary_affine_step(slope, intercept, symbol)
        steps += 1
        path.append((steps, slope, intercept, "".join(word)))
    return path


def minimum_x_for_smaller(source: Affine, target: Affine) -> Optional[int]:
    """Least x >= 0 for which 0 < target(x) < source(x) thereafter."""

    source_slope, source_intercept = source
    target_slope, target_intercept = target
    require(source_slope >= 0, "negative source slope")
    if target_slope < 0 or target_slope > source_slope:
        return None
    if target_slope == source_slope and target_intercept >= source_intercept:
        return None

    lower = 0
    if target_slope == 0:
        if target_intercept <= 0:
            return None
    elif target_intercept <= 0:
        lower = max(lower, (-target_intercept) // target_slope + 1)

    if target_slope < source_slope:
        slope_difference = source_slope - target_slope
        intercept_difference = source_intercept - target_intercept
        if intercept_difference <= 0:
            lower = max(lower, (-intercept_difference) // slope_difference + 1)
    return lower


def o_predecessor(endpoint: Affine) -> Optional[Affine]:
    """Exact uniformly odd predecessor for the one-letter target word O."""

    slope, intercept = endpoint
    if slope % 3 != 0 or (intercept - 1) % 3 != 0:
        return None
    previous = slope // 3, (intercept - 1) // 3
    if previous[0] % 2 != 0 or previous[1] % 2 != 1:
        return None
    return previous


def macro_word(k: int) -> str:
    require(0 <= k <= MAX_MACRO_INDEX, "macro index outside fixed grammar")
    return "O" + "EO" * k + "EEO"


def macro_predecessor(endpoint: Affine, k: int) -> Optional[Affine]:
    """Return P_k(Y) exactly when w_k is uniformly parity-admissible."""

    slope, intercept = endpoint
    denominator = 3 ** (k + 2)

    # For Y(x)=slope*x+intercept, q=(2Y+1)/3^(k+2) must be an
    # integer affine family with one fixed residue (-1)^k modulo 4.
    if slope % (2 * denominator) != 0:
        return None
    if (2 * intercept + 1) % denominator != 0:
        return None
    q_intercept = (2 * intercept + 1) // denominator
    if q_intercept % 4 != ((-1) ** k) % 4:
        return None

    target = (
        (2 ** (k + 2)) * (slope // denominator),
        (2 ** (k + 1)) * q_intercept - 1,
    )
    if replay_affine(target, macro_word(k)) != endpoint:
        raise CheckError("closed-form macro failed its affine endpoint identity")
    return target


def endpoint_candidates(endpoint: Affine) -> Iterable[Tuple[Affine, str]]:
    """Yield the fixed grammar in increasing target-word length."""

    yield endpoint, ""
    previous = o_predecessor(endpoint)
    if previous is not None:
        yield previous, "O"
    for k in range(MAX_MACRO_INDEX + 1):
        previous = macro_predecessor(endpoint, k)
        if previous is not None:
            yield previous, macro_word(k)


def classify_residue(residue: int) -> Optional[FormulaCertificate]:
    source = MODULUS, residue
    for steps, endpoint_slope, endpoint_intercept, source_word in uniform_forward_path(
        K, residue
    ):
        endpoint = endpoint_slope, endpoint_intercept
        for target, target_word in endpoint_candidates(endpoint):
            lower = minimum_x_for_smaller(source, target)
            if lower is None:
                continue
            require(
                replay_affine(target, target_word) == endpoint,
                "candidate target does not reach the source endpoint",
            )
            return FormulaCertificate(
                residue=residue,
                source_steps=steps,
                endpoint=endpoint,
                target=target,
                source_word=source_word,
                target_word=target_word,
                lower=lower,
            )
    return None


def least_x_above_one(slope: int, intercept: int) -> int:
    if slope < 0:
        raise CheckError("negative slope in stopped-map trace")
    if slope == 0:
        if intercept > 1:
            return 0
        raise CheckError("constant E/O pre-step cannot be made greater than 1")
    return max(0, (1 - intercept) // slope + 1)


def stopped_safe_lower(start: Affine, word: str, initial_lower: int) -> int:
    slope, intercept = start
    lower = initial_lower
    for symbol in word:
        lower = max(lower, least_x_above_one(slope, intercept))
        slope, intercept = ordinary_affine_step(slope, intercept, symbol)
    return lower


def no_duplicate_pairs(pairs: Sequence[Tuple[str, object]]) -> Dict[str, object]:
    out: Dict[str, object] = {}
    for key, value in pairs:
        if key in out:
            raise CheckError("duplicate JSON member: {}".format(key))
        out[key] = value
    return out


def reject_json_constant(token: str) -> object:
    raise CheckError("nonstandard JSON constant: {}".format(token))


def load_bundle(path: Path) -> Dict[str, object]:
    try:
        with path.open("r", encoding="utf-8") as stream:
            value = json.load(
                stream,
                object_pairs_hook=no_duplicate_pairs,
                parse_constant=reject_json_constant,
            )
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise CheckError("could not read bundle: {}".format(exc))
    require(isinstance(value, dict), "bundle root must be an object")
    return value


def exact_int(value: object, label: str) -> int:
    require(isinstance(value, int) and not isinstance(value, bool), label)
    return value


def exact_affine(value: object, label: str) -> Affine:
    require(isinstance(value, list) and len(value) == 2, label)
    return exact_int(value[0], label), exact_int(value[1], label)


def route_edges(bundle: Dict[str, object]) -> Dict[int, Dict[str, object]]:
    edges = bundle.get("edges")
    require(isinstance(edges, list), "bundle edges must be a list")
    out: Dict[int, Dict[str, object]] = {}
    prefix = "route-b-k12-r"
    for raw_edge in edges:
        require(isinstance(raw_edge, dict), "bundle edge must be an object")
        edge_id = raw_edge.get("id")
        require(isinstance(edge_id, str), "bundle edge id must be a string")
        if not edge_id.startswith(prefix):
            continue
        suffix = edge_id[len(prefix) :]
        require(len(suffix) == 4 and suffix.isdigit(), "malformed Route B edge id")
        residue = int(suffix)
        require(residue not in out, "duplicate Route B residue")
        out[residue] = raw_edge
    return out


def validate_static_bundle_boundary(bundle: Dict[str, object]) -> None:
    """Freeze non-Route-B data; the full RG-CERT checker remains authoritative."""

    require(set(bundle) == EXPECTED_TOP_LEVEL_KEYS, "unexpected top-level bundle fields")
    require(bundle.get("schema") == "RG-CERT-0/v0", "wrong bundle schema")
    require(bundle.get("claim") == "partial", "macro audit requires the partial bundle")
    require(bundle.get("map") == "stopped_collatz", "wrong bundle map")
    require(bundle.get("coverage_modulus") == MODULUS, "wrong coverage modulus")
    edges = bundle.get("edges")
    require(isinstance(edges, list), "bundle edges must be a list")
    require(len(edges) == EXPECTED_CERTIFIED + 2, "unexpected total edge count")
    non_route: List[Dict[str, object]] = []
    for edge in edges:
        require(isinstance(edge, dict), "bundle edge must be an object")
        edge_id = edge.get("id")
        require(isinstance(edge_id, str), "bundle edge id must be a string")
        if not edge_id.startswith("route-b-k12-r"):
            non_route.append(edge)
    require(non_route == EXPECTED_NON_ROUTE_EDGES, "non-Route-B static edge mismatch")


def compare_certificate(cert: FormulaCertificate, edge: Dict[str, object]) -> None:
    source_param = exact_affine(edge.get("source_param"), "bad source_param")
    target_param = exact_affine(edge.get("target_param"), "bad target_param")
    lower = exact_int(edge.get("domain_lower"), "bad domain_lower")
    source_word = edge.get("source_trace")
    target_word = edge.get("target_trace")
    require(isinstance(source_word, str), "bad source_trace")
    require(isinstance(target_word, str), "bad target_trace")

    require(source_param == (MODULUS, cert.residue - 1), "source map mismatch")
    require(target_param == (cert.target[0], cert.target[1] - 1), "target map mismatch")
    require(source_word == cert.source_word, "source word mismatch")
    require(target_word == cert.target_word, "target word mismatch")

    expected_lower = max(
        cert.lower,
        stopped_safe_lower((MODULUS, cert.residue), cert.source_word, cert.lower),
        stopped_safe_lower(cert.target, cert.target_word, cert.lower),
    )
    require(lower == expected_lower, "stopped-map lower bound mismatch")


def final_power_of_three(path: Sequence[Tuple[int, int, int, str]]) -> int:
    require(bool(path), "empty forward path")
    slope = path[-1][1]
    exponent = 0
    while slope % 3 == 0:
        slope //= 3
        exponent += 1
    require(slope == 1, "maximal endpoint slope is not a power of three")
    return exponent


def check_one_bit_refinement(residues: Sequence[int]) -> Counter:
    exponents: Counter = Counter()
    for residue in residues:
        parent_path = uniform_forward_path(K, residue)
        parent_slope, parent_intercept = parent_path[-1][1:3]
        child_exponents: List[int] = []
        for epsilon in (0, 1):
            child_residue = residue + epsilon * MODULUS
            constant = parent_intercept + epsilon * parent_slope
            if constant % 2 == 0:
                predicted = parent_slope, constant // 2
            else:
                predicted = 3 * parent_slope, (3 * constant + 1) // 2
            child_path = uniform_forward_path(K + 1, child_residue)
            actual = child_path[-1][1], child_path[-1][2]
            require(predicted == actual, "one-bit refinement identity mismatch")
            child_exponents.append(final_power_of_three(child_path))
        parent_exponent = final_power_of_three(parent_path)
        require(
            sorted(child_exponents) == [parent_exponent, parent_exponent + 1],
            "one-bit refinement exponent partition mismatch",
        )
        exponents[parent_exponent] += 1
    return exponents


def self_test() -> None:
    for k in range(MAX_MACRO_INDEX + 1):
        expected_mod_four = ((-1) ** k) % 4
        for q in range(1, 40, 2):
            endpoint = (3 ** (k + 2) * q - 1) // 2
            candidate = macro_predecessor((0, endpoint), k)
            if q % 4 == expected_mod_four:
                require(candidate == (0, 2 ** (k + 1) * q - 1), "macro test failed")
            else:
                require(candidate is None, "wrong-parity macro was accepted")

    require(o_predecessor((6, 4)) == (2, 1), "O predecessor test failed")
    require(o_predecessor((3, 4)) is None, "nonuniform O predecessor was accepted")
    require(
        minimum_x_for_smaller((8, 7), (4, 9)) == 1,
        "strict-smaller threshold test failed",
    )


def format_histogram(histogram: Counter) -> List[str]:
    lines: List[str] = []
    for word, expected in EXPECTED_ROUTE_TEMPLATES.items():
        label = "<empty>" if word == "" else word
        lines.append("  {}: {}".format(label, histogram[word]))
        require(histogram[word] == expected, "target-template count mismatch")
    require(set(histogram) == set(EXPECTED_ROUTE_TEMPLATES), "unexpected target template")
    return lines


def run(bundle_path: Path) -> None:
    self_test()

    certificates: Dict[int, FormulaCertificate] = {}
    gaps: List[int] = []
    for residue in range(1, MODULUS, 2):
        cert = classify_residue(residue)
        if cert is None:
            gaps.append(residue)
        else:
            certificates[residue] = cert

    require(len(certificates) == EXPECTED_CERTIFIED, "formula-certified count mismatch")
    require(len(gaps) == EXPECTED_GAPS, "formula-gap count mismatch")
    require(len(certificates) + len(gaps) == EXPECTED_CYLINDERS, "partition mismatch")

    bundle = load_bundle(bundle_path)
    validate_static_bundle_boundary(bundle)
    edges = route_edges(bundle)
    require(set(edges) == set(certificates), "formula/bundle Route B set mismatch")
    for residue, cert in certificates.items():
        compare_certificate(cert, edges[residue])

    expected_uncovered = bundle.get("expected_uncovered")
    require(isinstance(expected_uncovered, list), "bad expected_uncovered")
    uncovered = [exact_int(value, "bad uncovered residue") for value in expected_uncovered]
    require(uncovered == [residue - 1 for residue in gaps], "formula/bundle gap mismatch")

    histogram = Counter(cert.target_word for cert in certificates.values())
    gap_exponents = check_one_bit_refinement(gaps)
    require(gap_exponents == Counter({8: 38, 9: 60, 10: 36, 11: 10, 12: 1}),
            "gap endpoint-exponent distribution mismatch")

    print("RG-MACRO-001 exact formula classification")
    print("K={} odd_cylinders={}".format(K, EXPECTED_CYLINDERS))
    print(
        "fixed grammar: <empty>, O, O(EO)^kEEO for 0<=k<={}".format(
            MAX_MACRO_INDEX
        )
    )
    print("formula-certified={}".format(len(certificates)))
    print("formula-gaps={}".format(len(gaps)))
    print("bundle Route B edge set and selected affine data: exact match")
    print("target trace templates:")
    for line in format_histogram(histogram):
        print(line)
    print("gap maximal-endpoint exponents:")
    for exponent in sorted(gap_exponents):
        print("  s={}: {}".format(exponent, gap_exponents[exponent]))
    print("one-bit refinement: 290 children, exact identities and exponent split PASS")
    print("gap decoded residues R:")
    print("  " + " ".join(str(residue) for residue in gaps))
    print("gap RG-CERT-0 source-parameter residues p=R-1:")
    print("  " + " ".join(str(residue - 1) for residue in gaps))
    print("RG-MACRO-001 PASS (partial symbolic classification; not global)")


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "bundle",
        nargs="?",
        type=Path,
        default=Path(__file__).with_name("rg_cert0_route_b_k12.json"),
        help="retained RG-CERT-0 bundle (default: adjacent static bundle)",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="run formula unit tests only",
    )
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    try:
        args = parse_args(argv)
        if args.self_test:
            self_test()
            print("RG-MACRO-001 self-test PASS")
        else:
            run(args.bundle)
        return 0
    except CheckError as exc:
        print("RG-MACRO-001 check failed: {}".format(exc), file=sys.stderr)
        return 1
    except Exception as exc:
        print(
            "RG-MACRO-001 check failed with an internal error: {}: {}".format(
                type(exc).__name__, exc
            ),
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
