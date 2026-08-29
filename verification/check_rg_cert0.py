#!/usr/bin/env python3
"""Fail-closed checker for the RG-CERT-0/v0 certificate language.

This checker validates exact infinite affine families.  It does not search for
edges and it never treats a partial bundle as a Collatz proof.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, NoReturn, Sequence


if not __debug__:
    raise RuntimeError(
        "RG-CERT-0 verification refuses optimized Python mode; do not use -O."
    )


SCHEMA = "RG-CERT-0/v0"
MAP_NAME = "stopped_collatz"
TOP_KEYS = {
    "schema",
    "claim",
    "map",
    "coverage_modulus",
    "expected_uncovered",
    "edges",
}
EDGE_KEYS = {
    "id",
    "domain_lower",
    "source_param",
    "target_param",
    "source_trace",
    "target_trace",
    "origin",
}
EDGE_ID_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}\Z")


class CertificateError(ValueError):
    """A fail-closed schema or mathematical validation failure."""


@dataclass(frozen=True)
class Affine:
    slope: int
    intercept: int


@dataclass(frozen=True)
class Edge:
    edge_id: str
    lower: int
    source: Affine
    target: Affine
    source_trace: str
    target_trace: str
    origin: str


@dataclass(frozen=True)
class CoverageHole:
    residue: int
    kind: str
    witness: int


def fail(message: str) -> NoReturn:
    raise CertificateError(message)


def exact_keys(value: Any, required: set[str], context: str) -> dict[str, Any]:
    if type(value) is not dict:
        fail(f"{context}: expected an object")
    actual = set(value)
    if actual != required:
        missing = sorted(required - actual)
        unknown = sorted(actual - required)
        fail(f"{context}: key mismatch; missing={missing}, unknown={unknown}")
    return value


def integer(value: Any, context: str) -> int:
    if type(value) is not int:
        fail(f"{context}: expected a JSON integer (booleans are forbidden)")
    return value


def affine_pair(value: Any, context: str) -> Affine:
    if type(value) is not list or len(value) != 2:
        fail(f"{context}: expected an exact two-element array")
    slope = integer(value[0], f"{context}[0]")
    intercept = integer(value[1], f"{context}[1]")
    if slope < 0:
        fail(f"{context}[0]: slope must be nonnegative")
    return Affine(slope, intercept)


def trace_string(value: Any, context: str) -> str:
    if type(value) is not str:
        fail(f"{context}: expected a string")
    bad = sorted(set(value) - {"S", "E", "O"})
    if bad:
        fail(f"{context}: unknown trace symbols {bad}")
    return value


def printable_ascii(value: Any, context: str) -> str:
    if type(value) is not str:
        fail(f"{context}: expected a string")
    if not (1 <= len(value) <= 256):
        fail(f"{context}: length must be between 1 and 256 characters")
    if any(ord(char) < 32 or ord(char) > 126 for char in value):
        fail(f"{context}: only printable ASCII characters are permitted")
    return value


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            fail(f"JSON object: duplicate member name {key!r}")
        result[key] = value
    return result


def reject_constant(token: str) -> NoReturn:
    fail(f"JSON: nonstandard constant {token!r} is forbidden")


def reject_float(token: str) -> NoReturn:
    fail(f"JSON: floating-point number {token!r} is forbidden")


def load_json(path: Path) -> Any:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        fail(f"cannot read UTF-8 certificate {path}: {exc}")
    try:
        return json.loads(
            text,
            object_pairs_hook=unique_object,
            parse_constant=reject_constant,
            parse_float=reject_float,
        )
    except CertificateError:
        raise
    except (json.JSONDecodeError, RecursionError, ValueError) as exc:
        fail(f"invalid JSON in {path}: {exc}")


def replay(start: Affine, trace: str, lower: int, context: str) -> Affine:
    current = start
    for index, branch in enumerate(trace):
        u, v = current.slope, current.intercept
        step = f"{context}[{index}]"
        if branch == "S":
            if (u, v) != (0, 1):
                fail(f"{step}: S requires the identically-one family, got {u}*x+{v}")
        elif branch == "E":
            if u * lower + v <= 1:
                fail(f"{step}: E pre-step family is not uniformly greater than 1")
            if u % 2 != 0 or v % 2 != 0:
                fail(f"{step}: E pre-step family is not uniformly even")
            current = Affine(u // 2, v // 2)
        elif branch == "O":
            if u * lower + v <= 1:
                fail(f"{step}: O pre-step family is not uniformly greater than 1")
            if u % 2 != 0 or v % 2 != 1:
                fail(f"{step}: O pre-step family is not uniformly odd")
            current = Affine(3 * u, 3 * v + 1)
        else:
            fail(f"{step}: internal unknown trace symbol {branch!r}")
    return current


def parse_edge(raw: Any, index: int, modulus: int, seen_ids: set[str]) -> Edge:
    context = f"edges[{index}]"
    obj = exact_keys(raw, EDGE_KEYS, context)

    edge_id = obj["id"]
    if type(edge_id) is not str or EDGE_ID_RE.fullmatch(edge_id) is None:
        fail(f"{context}.id: does not match the frozen ASCII identifier grammar")
    if edge_id in seen_ids:
        fail(f"{context}.id: duplicate identifier {edge_id!r}")
    seen_ids.add(edge_id)

    lower = integer(obj["domain_lower"], f"{context}.domain_lower")
    if lower < 0:
        fail(f"{context}.domain_lower: must be nonnegative")
    source = affine_pair(obj["source_param"], f"{context}.source_param")
    target = affine_pair(obj["target_param"], f"{context}.target_param")
    source_trace = trace_string(obj["source_trace"], f"{context}.source_trace")
    target_trace = trace_string(obj["target_trace"], f"{context}.target_trace")
    origin = printable_ascii(obj["origin"], f"{context}.origin")

    if source.slope > 0 and modulus % source.slope != 0:
        fail(
            f"{context}: positive source slope {source.slope} "
            f"does not divide coverage modulus {modulus}"
        )

    source_at_lower = source.slope * lower + source.intercept
    target_at_lower = target.slope * lower + target.intercept
    if source_at_lower < 0:
        fail(f"{context}: source map leaves D=N at the lower endpoint")
    if target_at_lower < 0:
        fail(f"{context}: target map leaves D=N at the lower endpoint")

    source_endpoint = replay(
        Affine(source.slope, source.intercept + 1),
        source_trace,
        lower,
        f"{context}.source_trace",
    )
    target_endpoint = replay(
        Affine(target.slope, target.intercept + 1),
        target_trace,
        lower,
        f"{context}.target_trace",
    )
    if source_endpoint != target_endpoint:
        fail(
            f"{context}: F6 endpoint mismatch: "
            f"source={source_endpoint}, target={target_endpoint}"
        )

    slope_difference = source.slope - target.slope
    lower_difference = (
        slope_difference * lower + source.intercept - target.intercept
    )
    if slope_difference < 0 or lower_difference <= 0:
        fail(f"{context}: F7 rank decrease does not hold on the whole tail")

    return Edge(
        edge_id=edge_id,
        lower=lower,
        source=source,
        target=target,
        source_trace=source_trace,
        target_trace=target_trace,
        origin=origin,
    )


def ceil_div(numerator: int, denominator: int) -> int:
    return -((-numerator) // denominator)


def singleton_indices(edges: Sequence[Edge], q: int, modulus: int) -> set[int]:
    indices: set[int] = set()
    for edge in edges:
        if edge.source.slope != 0:
            continue
        parameter = edge.source.intercept
        if parameter >= q and (parameter - q) % modulus == 0:
            indices.add((parameter - q) // modulus)
    return indices


def first_missing_index(covered: set[int], limit: int | None = None) -> int | None:
    """Least nonnegative index absent from covered, optionally below limit."""
    candidate = 0
    for index in sorted(covered):
        if index < candidate:
            continue
        if limit is not None and candidate >= limit:
            return None
        if index != candidate:
            return candidate
        candidate += 1
    if limit is not None and candidate >= limit:
        return None
    return candidate


def coverage_holes(edges: Sequence[Edge], modulus: int) -> list[CoverageHole]:
    holes: list[CoverageHole] = []
    for residue in range(modulus):
        q = residue if residue > 0 else modulus
        eligible: list[int] = []
        for edge in edges:
            m = edge.source.slope
            r = edge.source.intercept
            if m > 0 and (q - r) % m == 0:
                threshold_numerator = m * edge.lower + r - q
                eligible.append(max(0, ceil_div(threshold_numerator, modulus)))

        covered_singletons = singleton_indices(edges, q, modulus)
        if not eligible:
            missing_k = first_missing_index(covered_singletons)
            if missing_k is None:
                fail("internal coverage error: a finite set covered an infinite sequence")
            holes.append(
                CoverageHole(
                    residue=residue,
                    kind="no_eventual_tail",
                    witness=q + modulus * missing_k,
                )
            )
            continue

        first_tail = min(eligible)
        missing_k = first_missing_index(covered_singletons, first_tail)
        if missing_k is not None:
            holes.append(
                CoverageHole(
                    residue=residue,
                    kind="finite_prefix_hole",
                    witness=q + modulus * missing_k,
                )
            )
    return holes


def parse_bundle(raw: Any) -> tuple[str, int, list[int], list[Edge]]:
    obj = exact_keys(raw, TOP_KEYS, "bundle")
    if obj["schema"] != SCHEMA:
        fail(f"bundle.schema: expected {SCHEMA!r}")
    if obj["map"] != MAP_NAME:
        fail(f"bundle.map: expected {MAP_NAME!r}")

    claim = obj["claim"]
    if type(claim) is not str or claim not in {"partial", "global"}:
        fail("bundle.claim: expected exactly 'partial' or 'global'")

    modulus = integer(obj["coverage_modulus"], "bundle.coverage_modulus")
    if modulus <= 0:
        fail("bundle.coverage_modulus: must be positive")

    expected_raw = obj["expected_uncovered"]
    if type(expected_raw) is not list:
        fail("bundle.expected_uncovered: expected an array")
    expected: list[int] = []
    previous = -1
    for index, item in enumerate(expected_raw):
        residue = integer(item, f"bundle.expected_uncovered[{index}]")
        if not (0 <= residue < modulus):
            fail(f"bundle.expected_uncovered[{index}]: residue is outside [0,C)")
        if residue <= previous:
            fail("bundle.expected_uncovered: entries must be strictly increasing")
        expected.append(residue)
        previous = residue

    edges_raw = obj["edges"]
    if type(edges_raw) is not list:
        fail("bundle.edges: expected an array")
    seen_ids: set[str] = set()
    edges = [
        parse_edge(edge_raw, index, modulus, seen_ids)
        for index, edge_raw in enumerate(edges_raw)
    ]
    return claim, modulus, expected, edges


def validate_bundle(raw: Any) -> tuple[str, int, list[Edge], list[CoverageHole]]:
    claim, modulus, expected, edges = parse_bundle(raw)
    holes = coverage_holes(edges, modulus)
    actual = [hole.residue for hole in holes]
    if actual != expected:
        fail(
            "bundle.expected_uncovered: mismatch; "
            f"declared={expected}, computed={actual}"
        )
    if claim == "partial" and not holes:
        fail("bundle.claim: a complete cover must declare 'global', not 'partial'")
    if claim == "global" and holes:
        fail("bundle.claim: 'global' is forbidden when F3 has uncovered residues")
    return claim, modulus, edges, holes


def format_pairs(holes: Sequence[CoverageHole], kind: str) -> str:
    return ", ".join(
        f"{hole.residue}->{hole.witness}" for hole in holes if hole.kind == kind
    )


def report(
    claim: str,
    modulus: int,
    edges: Sequence[Edge],
    holes: Sequence[CoverageHole],
) -> None:
    print("RG-CERT-0/v0 exact certificate audit")
    print(f"  declared claim: {claim}")
    print(f"  coverage modulus: {modulus}")
    print(f"  validated edges: {len(edges)}")
    print("  F1 domain safety: PASS (fixed root decoder/rank)")
    print("  F2 entry coverage: PASS (delta(p)=p+1)")
    print("  F4-F7 listed-edge audit: PASS")
    print("LOCAL EDGE AUDIT PASS")

    if holes:
        residues = ",".join(str(hole.residue) for hole in holes)
        no_tail = [hole for hole in holes if hole.kind == "no_eventual_tail"]
        prefix = [hole for hole in holes if hole.kind == "finite_prefix_hole"]
        print(f"  F3 source coverage: INCOMPLETE ({len(holes)} residues)")
        print(f"  exact uncovered residues modulo {modulus}: [{residues}]")
        if no_tail:
            print(
                "  no-eventual-tail witnesses (residue->parameter): "
                + format_pairs(no_tail, "no_eventual_tail")
            )
        if prefix:
            print(
                "  finite-prefix-hole witnesses (residue->parameter): "
                + format_pairs(prefix, "finite_prefix_hole")
            )
        print("PARTIAL CONSTRUCTION VERIFIED; GLOBAL F3 INCOMPLETE")
    else:
        print("  F3 source coverage: PASS")
        print("GLOBAL RG-CERT-0 PASS")


def self_test() -> None:
    # The coverage test uses only source images.  Both residue tails are exact.
    cover = [
        Edge("even", 0, Affine(2, 1), Affine(1, 0), "E", "", "self-test"),
        Edge("even-parameter", 1, Affine(2, 0), Affine(0, 0), "", "", "self-test"),
    ]
    if coverage_holes(cover, 2):
        fail("self-test: exact two-residue cover was rejected")

    prefix_gap = [
        Edge("odd", 0, Affine(2, 1), Affine(0, 0), "", "", "self-test"),
        Edge("late-even", 2, Affine(2, 0), Affine(0, 0), "", "", "self-test"),
    ]
    holes = coverage_holes(prefix_gap, 2)
    if holes != [CoverageHole(0, "finite_prefix_hole", 2)]:
        fail(f"self-test: wrong prefix-hole result {holes}")

    singleton_repair = prefix_gap + [
        Edge("base-2", 0, Affine(0, 2), Affine(0, 0), "", "", "self-test")
    ]
    holes = coverage_holes(singleton_repair, 2)
    if holes:
        fail(f"self-test: singleton prefix repair failed {holes}")

    no_tail = [
        Edge("odd", 0, Affine(2, 1), Affine(0, 0), "", "", "self-test")
    ]
    holes = coverage_holes(no_tail, 2)
    if holes != [CoverageHole(0, "no_eventual_tail", 2)]:
        fail(f"self-test: wrong no-tail result {holes}")

    if replay(Affine(2, 2), "E", 0, "self-test") != Affine(1, 1):
        fail("self-test: even affine replay failed")
    if replay(Affine(2, 3), "O", 0, "self-test") != Affine(6, 10):
        fail("self-test: odd affine replay failed")
    if replay(Affine(0, 1), "SS", 0, "self-test") != Affine(0, 1):
        fail("self-test: stopped affine replay failed")

    try:
        json.loads('{"x": 1, "x": 2}', object_pairs_hook=unique_object)
    except CertificateError:
        pass
    else:
        fail("self-test: duplicate JSON key was accepted")
    try:
        json.loads("NaN", parse_constant=reject_constant)
    except CertificateError:
        pass
    else:
        fail("self-test: nonstandard JSON constant was accepted")

    print("RG-CERT-0 CHECKER SELF-TEST PASS")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate", nargs="?", type=Path)
    parser.add_argument(
        "--require-global",
        action="store_true",
        help="exit nonzero unless the checked bundle is globally complete",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="run checker-internal exact arithmetic and parser regressions",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.self_test:
            if args.certificate is not None or args.require_global:
                fail("--self-test cannot be combined with a certificate or --require-global")
            self_test()
            return 0
        if args.certificate is None:
            fail("a certificate path is required unless --self-test is used")

        raw = load_json(args.certificate)
        claim, modulus, edges, holes = validate_bundle(raw)
        report(claim, modulus, edges, holes)
        if args.require_global and holes:
            print("--require-global: rejected incomplete certificate", file=sys.stderr)
            return 2
        return 0
    except CertificateError as exc:
        print(f"RG-CERT-0 CHECK FAILED: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:  # fail closed on unforeseen checker errors
        print(
            f"RG-CERT-0 CHECK FAILED: internal {type(exc).__name__}: {exc}",
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
