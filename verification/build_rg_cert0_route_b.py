#!/usr/bin/env python3
"""Build the deterministic K=12 Route B RG-CERT-0/v0 bundle.

This is a certificate *producer*, not a verifier and not a Collatz proof.  It
recreates the bounded Route B search from the archival
``verification/round7_affine_coalescence_search.py`` with the fixed parameters

    K = 12, max_back_depth = 16, max_states_per_target = 50_000.

The ordinary-map certificates are translated to the stopped-map, all-positive
``root`` parameterization from ``RG-CERT-0.md``.  If stopped-map safety raises
an edge's lower bound, each excluded positive source is covered by a concrete
singleton-to-1 edge.  Singleton trajectories have the explicit finite safety
limit ``SINGLETON_TRACE_STEP_BOUND``; failure to reach 1 within that limit
aborts bundle construction.

The command line never writes by default.  Choose exactly one of:

    --output PATH   write canonical indented JSON to a new file
    --stdout        write canonical indented JSON to standard output

An existing output file is refused unless ``--force`` is also supplied.
Construction statistics, including stopped-map splits and exact uncovered
residue count, are written to standard error so ``--stdout`` remains valid
JSON.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import Deque, Dict, Iterable, List, Optional, Sequence, Set, Tuple


if not __debug__:
    raise RuntimeError(
        "RG-CERT-0 production is disabled under optimized Python; rerun without -O."
    )


SCHEMA = "RG-CERT-0/v0"
MAP_NAME = "stopped_collatz"
CLAIM = "partial"
ARCHIVE_COMMIT = "2e7eae2bb998b14e5443e6c440154130a0049467"
K = 12
COVERAGE_MODULUS = 1 << K
MAX_BACK_DEPTH = 16
MAX_STATES_PER_TARGET = 50_000
SINGLETON_TRACE_STEP_BOUND = 1_000_000
EDGE_ID_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}\Z")


Affine = Tuple[int, int]
Word = Tuple[int, ...]


@dataclass(frozen=True)
class Certificate:
    """An exact ordinary-map certificate in the archival Route B format."""

    K: int
    R: int
    t: int
    j: int
    A: int
    B: int
    word: Word
    x0: int = 0

    def source_value(self, x: int) -> int:
        return (1 << self.K) * x + self.R

    def target_value(self, x: int) -> int:
        return self.A * x + self.B


@dataclass(frozen=True)
class BuildStats:
    searched_odd_cylinders: int
    ordinary_certificates: int
    ordinary_unresolved: int
    imported_route_edges: int
    stopped_domain_raises: int
    stopped_excluded_instances: int
    stopped_terminal_exclusions: int
    stopped_split_details: Tuple[str, ...]
    singleton_edges: int
    total_edges: int
    exact_uncovered_residues: int


class BuildError(RuntimeError):
    """A fail-closed certificate-production error."""


def ordinary_map(n: int) -> int:
    if n <= 0:
        raise BuildError("ordinary Collatz map received a nonpositive integer")
    return n // 2 if n % 2 == 0 else 3 * n + 1


def iterate_ordinary(n: int, steps: int) -> int:
    if steps < 0:
        raise BuildError("ordinary iteration length must be nonnegative")
    for _ in range(steps):
        n = ordinary_map(n)
    return n


def parity_word(n: int, steps: int) -> Word:
    if steps < 0:
        raise BuildError("parity-word length must be nonnegative")
    out: List[int] = []
    for _ in range(steps):
        out.append(n & 1)
        n = ordinary_map(n)
    return tuple(out)


def minimum_x_for_smaller(
    source_slope: int,
    source_intercept: int,
    target_slope: int,
    target_intercept: int,
) -> Optional[int]:
    """Return the exact least x0 with 0 < target(x) < source(x) for x>=x0."""

    if source_slope < 0:
        raise BuildError("source slope must be nonnegative")
    if target_slope < 0 or target_slope > source_slope:
        return None
    if target_slope == source_slope and target_intercept >= source_intercept:
        return None

    x0 = 0
    if target_slope == 0:
        if target_intercept <= 0:
            return None
    elif target_intercept <= 0:
        x0 = max(x0, (-target_intercept) // target_slope + 1)

    if target_slope < source_slope:
        slope_difference = source_slope - target_slope
        intercept_difference = source_intercept - target_intercept
        if intercept_difference <= 0:
            x0 = max(x0, (-intercept_difference) // slope_difference + 1)

    return x0


def uniform_forward_path(cylinder_k: int, residue: int) -> List[Tuple[int, int, int]]:
    """Recreate the archival exact affine path before its coefficient branches."""

    modulus = 1 << cylinder_k
    if cylinder_k < 0 or not (0 < residue < modulus) or residue % 2 != 1:
        raise BuildError("invalid odd cylinder for uniform forward path")

    slope, intercept = modulus, residue
    path: List[Tuple[int, int, int]] = []
    steps = 0
    while slope % 2 == 0:
        if intercept % 2 == 0:
            slope //= 2
            intercept //= 2
        else:
            slope *= 3
            intercept = 3 * intercept + 1
        steps += 1
        path.append((steps, slope, intercept))
    return path


def source_trace(cylinder_k: int, residue: int, steps: int) -> str:
    """Reconstruct the exact E/O word for a Route B source cylinder."""

    if steps < 0:
        raise BuildError("source trace length must be nonnegative")
    slope, intercept = 1 << cylinder_k, residue
    symbols: List[str] = []
    for _ in range(steps):
        if slope % 2 != 0:
            raise BuildError("requested source trace extends past affine parity uniformity")
        if intercept % 2 == 0:
            symbols.append("E")
            slope //= 2
            intercept //= 2
        else:
            symbols.append("O")
            slope *= 3
            intercept = 3 * intercept + 1
    return "".join(symbols)


def reverse_predecessors(slope: int, intercept: int) -> Iterable[Tuple[int, int, int]]:
    """Yield archival reverse affine predecessors in its deterministic order."""

    yield 2 * slope, 2 * intercept, 0
    if slope % 3 == 0 and (intercept - 1) % 3 == 0:
        previous_slope = slope // 3
        previous_intercept = (intercept - 1) // 3
        if previous_slope % 2 == 0 and previous_intercept % 2 == 1:
            yield previous_slope, previous_intercept, 1


def validate_ordinary_certificate(
    cert: Certificate,
    extra_samples: Sequence[int] = (0, 1, 2, 3, 7, 11, 29),
) -> bool:
    """Validate the archival exact identity without relying on assertions."""

    modulus = 1 << cert.K
    if not (0 < cert.R < modulus and cert.R % 2 == 1):
        return False
    if cert.j != len(cert.word):
        return False

    states = {step: (slope, intercept) for step, slope, intercept in uniform_forward_path(cert.K, cert.R)}
    endpoint = states.get(cert.t)
    if endpoint is None:
        return False

    slope, intercept = cert.A, cert.B
    for parity in cert.word:
        if parity == 0:
            if slope % 2 != 0 or intercept % 2 != 0:
                return False
            slope, intercept = slope // 2, intercept // 2
        elif parity == 1:
            if slope % 2 != 0 or intercept % 2 != 1:
                return False
            slope, intercept = 3 * slope, 3 * intercept + 1
        else:
            return False

    if (slope, intercept) != endpoint:
        return False
    if minimum_x_for_smaller(modulus, cert.R, cert.A, cert.B) != cert.x0:
        return False

    sample_points = sorted(set((cert.x0, cert.x0 + 1, cert.x0 + 2) + tuple(extra_samples)))
    for x in sample_points:
        if x < cert.x0:
            continue
        source = cert.source_value(x)
        target = cert.target_value(x)
        if not (0 < target < source):
            return False
        if parity_word(target, cert.j) != cert.word:
            return False
        if iterate_ordinary(source, cert.t) != iterate_ordinary(target, cert.j):
            return False
    return True


def search_residue(
    cylinder_k: int,
    residue: int,
    max_back_depth: int = MAX_BACK_DEPTH,
    max_states_per_target: int = MAX_STATES_PER_TARGET,
) -> Optional[Certificate]:
    """Recreate the bounded Route B search for one odd residue."""

    modulus = 1 << cylinder_k
    if not (0 < residue < modulus and residue % 2 == 1):
        raise BuildError("search residue must be odd and lie strictly inside its modulus")
    if max_back_depth < 0 or max_states_per_target <= 0:
        raise BuildError("invalid bounded-search limits")

    for step, endpoint_slope, endpoint_intercept in uniform_forward_path(cylinder_k, residue):
        lower = minimum_x_for_smaller(
            modulus, residue, endpoint_slope, endpoint_intercept
        )
        if lower is not None:
            cert = Certificate(
                cylinder_k,
                residue,
                step,
                0,
                endpoint_slope,
                endpoint_intercept,
                (),
                lower,
            )
            if validate_ordinary_certificate(cert):
                return cert

        queue: Deque[Tuple[int, int, int, Word]] = deque(
            [(endpoint_slope, endpoint_intercept, 0, ())]
        )
        seen: Set[Affine] = {(endpoint_slope, endpoint_intercept)}
        visited = 0

        while queue and visited < max_states_per_target:
            slope, intercept, back_steps, word = queue.popleft()
            visited += 1
            if back_steps >= max_back_depth:
                continue

            for previous_slope, previous_intercept, parity in reverse_predecessors(
                slope, intercept
            ):
                key = (previous_slope, previous_intercept)
                if key in seen:
                    continue
                seen.add(key)

                new_word = (parity,) + word
                new_back_steps = back_steps + 1
                lower = minimum_x_for_smaller(
                    modulus, residue, previous_slope, previous_intercept
                )
                if lower is not None:
                    cert = Certificate(
                        cylinder_k,
                        residue,
                        step,
                        new_back_steps,
                        previous_slope,
                        previous_intercept,
                        new_word,
                        lower,
                    )
                    if validate_ordinary_certificate(cert):
                        return cert

                queue.append(
                    (previous_slope, previous_intercept, new_back_steps, new_word)
                )
    return None


def least_x_with_value_above_one(slope: int, intercept: int) -> int:
    """Least nonnegative x for which slope*x+intercept is strictly above 1."""

    if slope < 0:
        raise BuildError("a stopped trace acquired a negative slope")
    if slope == 0:
        if intercept > 1:
            return 0
        raise BuildError(
            "an ordinary E/O pre-step is identically at most 1 and cannot be "
            "made stopped-map safe by raising the domain lower bound"
        )
    return max(0, (1 - intercept) // slope + 1)


def stopped_safe_lower(
    start_slope: int,
    start_intercept: int,
    trace: str,
    initial_lower: int,
) -> int:
    """Return the exact least safe lower bound for every E/O pre-step."""

    if initial_lower < 0:
        raise BuildError("domain lower bound must be nonnegative")
    slope, intercept = start_slope, start_intercept
    required = initial_lower
    for symbol in trace:
        required = max(required, least_x_with_value_above_one(slope, intercept))
        if symbol == "E":
            if slope % 2 != 0 or intercept % 2 != 0:
                raise BuildError("declared E trace is not uniformly even")
            slope, intercept = slope // 2, intercept // 2
        elif symbol == "O":
            if slope % 2 != 0 or intercept % 2 != 1:
                raise BuildError("declared O trace is not uniformly odd")
            slope, intercept = 3 * slope, 3 * intercept + 1
        else:
            raise BuildError("Route B translation accepts only E/O source traces")
    return required


def replay_stopped_affine(
    slope: int, intercept: int, trace: str, lower: int
) -> Affine:
    """Replay one serialized stopped trace exactly over its affine tail."""

    if slope < 0 or lower < 0:
        raise BuildError("invalid affine stopped-trace input")
    for symbol in trace:
        if symbol == "S":
            if (slope, intercept) != (0, 1):
                raise BuildError("S branch is not the identically-one family")
        elif symbol == "E":
            if slope * lower + intercept <= 1:
                raise BuildError("E branch is not above the stopped terminal")
            if slope % 2 != 0 or intercept % 2 != 0:
                raise BuildError("E branch is not uniformly even")
            slope, intercept = slope // 2, intercept // 2
        elif symbol == "O":
            if slope * lower + intercept <= 1:
                raise BuildError("O branch is not above the stopped terminal")
            if slope % 2 != 0 or intercept % 2 != 1:
                raise BuildError("O branch is not uniformly odd")
            slope, intercept = 3 * slope, 3 * intercept + 1
        else:
            raise BuildError("trace contains a symbol outside S/E/O")
    return slope, intercept


def stopped_trace_to_one(n: int) -> str:
    """Return an exact singleton stopped trace to 1 within the fixed bound."""

    if n <= 0:
        raise BuildError("singleton source must decode to a positive integer")
    symbols: List[str] = []
    current = n
    for step in range(SINGLETON_TRACE_STEP_BOUND + 1):
        if current == 1:
            return "".join(symbols)
        if step == SINGLETON_TRACE_STEP_BOUND:
            break
        if current % 2 == 0:
            symbols.append("E")
            current //= 2
        else:
            symbols.append("O")
            current = 3 * current + 1
    raise BuildError(
        "singleton source {} did not reach 1 within {} stopped steps".format(
            n, SINGLETON_TRACE_STEP_BOUND
        )
    )


def make_edge(
    edge_id: str,
    lower: int,
    source: Affine,
    target: Affine,
    source_word: str,
    target_word: str,
    origin: str,
) -> Dict[str, object]:
    return {
        "id": edge_id,
        "domain_lower": lower,
        "source_param": [source[0], source[1]],
        "target_param": [target[0], target[1]],
        "source_trace": source_word,
        "target_trace": target_word,
        "origin": origin,
    }


def validate_built_edge(edge: Dict[str, object]) -> None:
    """Producer-side exact validation; the independent checker remains authoritative."""

    edge_id = edge.get("id")
    lower = edge.get("domain_lower")
    source = edge.get("source_param")
    target = edge.get("target_param")
    source_word = edge.get("source_trace")
    target_word = edge.get("target_trace")
    origin = edge.get("origin")

    if not isinstance(edge_id, str) or EDGE_ID_RE.fullmatch(edge_id) is None:
        raise BuildError("producer created an invalid edge identifier")
    if isinstance(lower, bool) or not isinstance(lower, int) or lower < 0:
        raise BuildError("producer created an invalid domain lower bound")
    if not isinstance(source, list) or len(source) != 2:
        raise BuildError("producer created an invalid source parameter map")
    if not isinstance(target, list) or len(target) != 2:
        raise BuildError("producer created an invalid target parameter map")
    coefficients = source + target
    if any(isinstance(value, bool) or not isinstance(value, int) for value in coefficients):
        raise BuildError("producer created a noninteger affine coefficient")
    source_slope, source_intercept = source
    target_slope, target_intercept = target
    if source_slope < 0 or target_slope < 0:
        raise BuildError("producer created a negative affine slope")
    if source_slope > 0 and COVERAGE_MODULUS % source_slope != 0:
        raise BuildError("producer source slope does not divide the coverage modulus")
    if source_slope * lower + source_intercept < 0:
        raise BuildError("producer source parameter leaves the natural domain")
    if target_slope * lower + target_intercept < 0:
        raise BuildError("producer target parameter leaves the natural domain")
    if not isinstance(source_word, str) or not isinstance(target_word, str):
        raise BuildError("producer created a nonstring trace")
    if not isinstance(origin, str) or not (1 <= len(origin) <= 256):
        raise BuildError("producer created invalid origin metadata")
    if any(ord(character) < 32 or ord(character) > 126 for character in origin):
        raise BuildError("producer origin metadata is not printable ASCII")

    source_endpoint = replay_stopped_affine(
        source_slope, source_intercept + 1, source_word, lower
    )
    target_endpoint = replay_stopped_affine(
        target_slope, target_intercept + 1, target_word, lower
    )
    if source_endpoint != target_endpoint:
        raise BuildError("producer created a false affine coalescence identity")

    rank_slope_difference = source_slope - target_slope
    rank_intercept_difference = source_intercept - target_intercept
    if rank_slope_difference < 0:
        raise BuildError("producer edge does not decrease numerical rank eventually")
    if rank_slope_difference * lower + rank_intercept_difference <= 0:
        raise BuildError("producer edge is not strictly rank decreasing at its lower bound")


def ceil_div(numerator: int, denominator: int) -> int:
    if denominator <= 0:
        raise BuildError("ceil_div denominator must be positive")
    return -((-numerator) // denominator)


def source_membership(parameter: int, edge: Dict[str, object]) -> bool:
    source = edge["source_param"]
    lower = edge["domain_lower"]
    if not isinstance(source, list) or len(source) != 2 or not isinstance(lower, int):
        raise BuildError("internal malformed edge during coverage calculation")
    slope, intercept = source
    if not isinstance(slope, int) or not isinstance(intercept, int):
        raise BuildError("internal noninteger edge during coverage calculation")
    if slope == 0:
        return parameter == intercept
    return parameter % slope == intercept % slope and parameter >= slope * lower + intercept


def compute_uncovered_residues(
    edges: Sequence[Dict[str, object]], modulus: int
) -> List[int]:
    """Implement the exact RG-CERT-0 Section 6 source-coverage decision."""

    if modulus <= 0:
        raise BuildError("coverage modulus must be positive")
    uncovered: List[int] = []
    for residue in range(modulus):
        least_positive = residue if residue > 0 else modulus
        thresholds: List[int] = []
        for edge in edges:
            source = edge["source_param"]
            lower = edge["domain_lower"]
            if not isinstance(source, list) or len(source) != 2 or not isinstance(lower, int):
                raise BuildError("internal malformed edge during coverage calculation")
            slope, intercept = source
            if not isinstance(slope, int) or not isinstance(intercept, int):
                raise BuildError("internal noninteger edge during coverage calculation")
            if slope <= 0:
                continue
            if modulus % slope != 0:
                raise BuildError("positive source slope does not divide coverage modulus")
            if least_positive % slope != intercept % slope:
                continue
            threshold = max(
                0,
                ceil_div(slope * lower + intercept - least_positive, modulus),
            )
            thresholds.append(threshold)

        if not thresholds:
            uncovered.append(residue)
            continue

        first_tail = min(thresholds)
        has_prefix_hole = False
        for k in range(first_tail):
            parameter = least_positive + modulus * k
            if not any(source_membership(parameter, edge) for edge in edges):
                has_prefix_hole = True
                break
        if has_prefix_hole:
            uncovered.append(residue)
    return uncovered


def route_edge(cert: Certificate) -> Tuple[Dict[str, object], int]:
    """Translate one ordinary certificate and return its stopped lower bound."""

    if cert.K != K:
        raise BuildError("Route B importer received the wrong cylinder exponent")
    source_word = source_trace(cert.K, cert.R, cert.t)
    target_symbols: List[str] = []
    for parity in cert.word:
        if parity == 0:
            target_symbols.append("E")
        elif parity == 1:
            target_symbols.append("O")
        else:
            raise BuildError("ordinary certificate contains a nonbinary parity symbol")
    target_word = "".join(target_symbols)
    source_required = stopped_safe_lower(
        1 << cert.K, cert.R, source_word, cert.x0
    )
    target_required = stopped_safe_lower(cert.A, cert.B, target_word, cert.x0)
    lower = max(cert.x0, source_required, target_required)
    edge = make_edge(
        "route-b-k12-r{:04d}".format(cert.R),
        lower,
        (1 << cert.K, cert.R - 1),
        (cert.A, cert.B - 1),
        source_word,
        target_word,
        (
            "Collatz-Conjecture-Work@{} verification/round7_affine_coalescence_search.py; "
            "K=12 R={} x0={} L={} t={} j={}".format(
                ARCHIVE_COMMIT,
                cert.R,
                cert.x0,
                lower,
                cert.t,
                cert.j,
            )
        ),
    )
    return edge, lower


def singleton_edge(source_parameter: int, residue: int, x: int) -> Dict[str, object]:
    if source_parameter <= 0:
        raise BuildError("terminal parameter p=0 must not receive a decreasing edge")
    trace = stopped_trace_to_one(source_parameter + 1)
    return make_edge(
        "stopped-split-p{:010d}".format(source_parameter),
        0,
        (0, source_parameter),
        (0, 0),
        trace,
        "",
        "stopped-map split from Route B K=12 R={} x={}".format(residue, x),
    )


def build_bundle() -> Tuple[Dict[str, object], BuildStats]:
    """Run the fixed search and build an independently checkable partial bundle."""

    certificates: List[Certificate] = []
    unresolved: List[int] = []
    for residue in range(1, COVERAGE_MODULUS, 2):
        cert = search_residue(
            K,
            residue,
            max_back_depth=MAX_BACK_DEPTH,
            max_states_per_target=MAX_STATES_PER_TARGET,
        )
        if cert is None:
            unresolved.append(residue)
        else:
            certificates.append(cert)

    edges: List[Dict[str, object]] = [
        make_edge(
            "structural-even",
            0,
            (2, 1),
            (1, 0),
            "E",
            "",
            "RG-CERT-0 structural even-input edge",
        )
    ]
    excluded_sources: Dict[int, Tuple[int, int]] = {}
    stopped_domain_raises = 0
    stopped_excluded_instances = 0
    stopped_terminal_exclusions = 0
    stopped_split_details: List[str] = []

    for cert in certificates:
        edge, stopped_lower = route_edge(cert)
        edges.append(edge)
        if stopped_lower > cert.x0:
            stopped_domain_raises += 1
            stopped_excluded_instances += stopped_lower - cert.x0
            positive_split_parameters: List[int] = []
            for x in range(cert.x0, stopped_lower):
                parameter = (1 << cert.K) * x + cert.R - 1
                if parameter == 0:
                    stopped_terminal_exclusions += 1
                    continue
                positive_split_parameters.append(parameter)
                prior = excluded_sources.get(parameter)
                source_label = (cert.R, x)
                if prior is not None and prior != source_label:
                    raise BuildError("two stopped splits unexpectedly name one source parameter")
                excluded_sources[parameter] = source_label
            stopped_split_details.append(
                "R={} old_lower={} new_lower={} positive_source_parameters={}".format(
                    cert.R, cert.x0, stopped_lower, positive_split_parameters
                )
            )

    for parameter in sorted(excluded_sources):
        residue, x = excluded_sources[parameter]
        edges.append(singleton_edge(parameter, residue, x))

    identifiers: Set[str] = set()
    for edge in edges:
        edge_id = edge["id"]
        if not isinstance(edge_id, str):
            raise BuildError("internal nonstring edge identifier")
        if edge_id in identifiers:
            raise BuildError("producer created a duplicate edge identifier")
        identifiers.add(edge_id)
        validate_built_edge(edge)

    expected_uncovered = compute_uncovered_residues(edges, COVERAGE_MODULUS)
    if not expected_uncovered:
        raise BuildError("fixed Route B bundle unexpectedly became global; review claim boundary")

    bundle: Dict[str, object] = {
        "schema": SCHEMA,
        "claim": CLAIM,
        "map": MAP_NAME,
        "coverage_modulus": COVERAGE_MODULUS,
        "expected_uncovered": expected_uncovered,
        "edges": edges,
    }
    stats = BuildStats(
        searched_odd_cylinders=1 << (K - 1),
        ordinary_certificates=len(certificates),
        ordinary_unresolved=len(unresolved),
        imported_route_edges=len(certificates),
        stopped_domain_raises=stopped_domain_raises,
        stopped_excluded_instances=stopped_excluded_instances,
        stopped_terminal_exclusions=stopped_terminal_exclusions,
        stopped_split_details=tuple(stopped_split_details),
        singleton_edges=len(excluded_sources),
        total_edges=len(edges),
        exact_uncovered_residues=len(expected_uncovered),
    )
    return bundle, stats


def canonical_json(bundle: Dict[str, object]) -> str:
    return json.dumps(bundle, ensure_ascii=True, indent=2, sort_keys=True) + "\n"


def report_stats(stats: BuildStats) -> None:
    print(
        "Route B search: K={}, max_back_depth={}, max_states_per_target={}".format(
            K, MAX_BACK_DEPTH, MAX_STATES_PER_TARGET
        ),
        file=sys.stderr,
    )
    for detail in stats.stopped_split_details:
        print("stopped-map split detail: {}".format(detail), file=sys.stderr)
    print(
        "ordinary cylinders: searched={}, certified={}, unresolved={}".format(
            stats.searched_odd_cylinders,
            stats.ordinary_certificates,
            stats.ordinary_unresolved,
        ),
        file=sys.stderr,
    )
    print(
        "stopped-map translation: imported={}, raised_domains={}, "
        "excluded_instances={}, terminal_exclusions={}, singleton_edges={}".format(
            stats.imported_route_edges,
            stats.stopped_domain_raises,
            stats.stopped_excluded_instances,
            stats.stopped_terminal_exclusions,
            stats.singleton_edges,
        ),
        file=sys.stderr,
    )
    print(
        "bundle: edges={}, coverage_modulus={}, exact_uncovered_residues={}, claim={}".format(
            stats.total_edges,
            COVERAGE_MODULUS,
            stats.exact_uncovered_residues,
            CLAIM,
        ),
        file=sys.stderr,
    )


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    destination = parser.add_mutually_exclusive_group(required=True)
    destination.add_argument(
        "--output",
        type=Path,
        metavar="PATH",
        help="write canonical indented JSON to PATH",
    )
    destination.add_argument(
        "--stdout",
        action="store_true",
        help="write canonical indented JSON to stdout (statistics go to stderr)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="allow --output to replace an existing regular file",
    )
    args = parser.parse_args(argv)
    if args.force and args.output is None:
        parser.error("--force is valid only with --output")
    return args


def write_output(path: Path, content: str, force: bool) -> None:
    if not path.parent.is_dir():
        raise BuildError("output parent directory does not exist: {}".format(path.parent))
    if path.exists() and not path.is_file():
        raise BuildError("output path exists and is not a regular file: {}".format(path))
    mode = "w" if force else "x"
    try:
        with path.open(mode, encoding="utf-8", newline="\n") as stream:
            stream.write(content)
    except FileExistsError:
        raise BuildError(
            "output already exists; choose another path or pass --force: {}".format(path)
        )
    except OSError as exc:
        raise BuildError("could not write output {}: {}".format(path, exc))


def main(argv: Optional[Sequence[str]] = None) -> int:
    try:
        args = parse_args(argv)
        bundle, stats = build_bundle()
        rendered = canonical_json(bundle)
        if args.stdout:
            sys.stdout.write(rendered)
        else:
            write_output(args.output, rendered, args.force)
        report_stats(stats)
        return 0
    except BuildError as exc:
        print("RG-CERT-0 production failed: {}".format(exc), file=sys.stderr)
        return 1
    except Exception as exc:
        print(
            "RG-CERT-0 production failed with an internal error: {}: {}".format(
                type(exc).__name__, exc
            ),
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
