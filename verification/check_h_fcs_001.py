"""Exact finite diagnostics for H-FCS-001.

The human proof is in THEOREM.md.  This dependency-free program checks its
finite algebra and representative positive-shadow constructions using only
integers and fractions.  A passing run is not a proof of the infinite theorem
and is not a proof or disproof of Collatz.
"""

from __future__ import annotations

from fractions import Fraction


def v2_int(n: int) -> int:
    """Return the exponent of 2 in a nonzero integer."""

    n = abs(n)
    if n == 0:
        raise ValueError("v2(0)")
    out = 0
    while n % 2 == 0:
        n //= 2
        out += 1
    return out


def v2_frac(x: Fraction) -> int:
    """Return the exponent of 2 in a nonzero rational."""

    if x == 0:
        raise ValueError("v2(0)")
    return v2_int(x.numerator) - v2_int(x.denominator)


def accelerated_odd(n: int) -> int:
    assert n > 0 and n % 2 == 1
    z = 3 * n + 1
    return z // (2 ** v2_int(z))


def valuation_word(m: int) -> tuple[int, ...]:
    assert m >= 3
    return (2,) + (1,) * (m - 1)


def word_constant(word: tuple[int, ...]) -> tuple[int, int]:
    """Return A and C for x |-> (3^m x + C) / 2^A."""

    total = 0
    constant = 0
    m = len(word)
    for j, valuation in enumerate(word):
        constant += (3 ** (m - 1 - j)) * (2**total)
        total += valuation
    return total, constant


def rational_cycle(m: int) -> tuple[Fraction, ...]:
    """Construct the exact negative rational cycle for (2, 1^(m-1))."""

    word = valuation_word(m)
    total, constant = word_constant(word)
    assert total == m + 1
    assert constant == 5 * (3 ** (m - 1)) - 2 ** (m + 1)
    assert 3**m > 2**total

    first = Fraction(constant, 2**total - 3**m)
    cycle = [first]
    x = first
    for j, expected in enumerate(word):
        z = 3 * x + 1
        assert v2_frac(z) == expected
        x = z / (2**expected)
        if j < m - 1:
            cycle.append(x)

    assert x == first
    assert len(cycle) == m
    assert all(x < 0 and v2_frac(x) == 0 for x in cycle)

    # Check the closed phase formulas displayed in THEOREM.md.
    denominator = 3**m - 2 ** (m + 1)
    displayed = [
        Fraction(2 ** (m + 1) - 5 * (3 ** (m - 1)), denominator)
    ]
    displayed.extend(
        Fraction(
            2 ** (m + 1) - 3**m - (2 ** (m - j + 1)) * (3 ** (j - 1)),
            denominator,
        )
        for j in range(1, m)
    )
    assert tuple(displayed) == tuple(cycle)
    return tuple(cycle)


def normalized_lift(
    m: int, periods: int, reserve: int
) -> tuple[tuple[int, ...], tuple[Fraction, ...]]:
    """Return the canonical positive lift in [2^M, 2^(M+1))."""

    assert periods >= 1 and reserve >= 1
    word = valuation_word(m)
    total, _ = word_constant(word)
    cycle = rational_cycle(m)
    precision = periods * total + reserve
    modulus = 2**precision
    first = cycle[0]
    residue = (first.numerator * pow(first.denominator, -1, modulus)) % modulus
    n = residue + modulus
    assert modulus <= n < 2 * modulus and n % 2 == 1

    values = [n]
    for j in range(periods * m):
        expected = word[j % m]
        assert v2_int(3 * n + 1) == expected
        n = accelerated_odd(n)
        values.append(n)

    return tuple(values), cycle


def feature(x: Fraction, centers: tuple[Fraction, ...]) -> tuple[int, ...]:
    return tuple(v2_frac(x - center) for center in centers)


def choose_avoiding_m(beta: Fraction, centers: tuple[Fraction, ...]) -> int:
    """Find a diagnostic m with m-beta(m+1)>=1 and Q_m disjoint from C."""

    for m in range(3, 2000):
        if Fraction(m) - beta * (m + 1) < 1:
            continue
        if all(phase not in centers for phase in rational_cycle(m)):
            return m
    raise AssertionError("diagnostic search bound exhausted")


def test_cycles() -> tuple[int, int]:
    owner: dict[Fraction, int] = {}
    phases = 0
    for m in range(3, 81):
        cycle = rational_cycle(m)
        assert len(set(cycle)) == m
        for phase in cycle:
            assert phase not in owner
            owner[phase] = m
            phases += 1
    return 78, phases


def test_lifts() -> int:
    cases = 0
    for m in (3, 4, 7, 12, 25):
        word = valuation_word(m)
        total, _ = word_constant(word)
        for periods in (1, 2, 5, 11):
            for reserve in (1, 3, 9):
                values, cycle = normalized_lift(m, periods, reserve)
                assert len(values) == periods * m + 1
                for j, n in enumerate(values):
                    spent = (j // m) * total + sum(word[: j % m])
                    assert v2_frac(Fraction(n) - cycle[j % m]) >= (
                        periods * total + reserve - spent
                    )
                assert v2_frac(Fraction(values[-1]) - cycle[0]) >= reserve
                cases += 1
    return cases


def test_freezing_and_horizon() -> tuple[int, tuple[tuple[int, int, int], ...]]:
    collision_cycles = {m: rational_cycle(m) for m in (3, 5, 8, 13)}
    centers = (
        Fraction(-1),
        Fraction(1, 3),
        collision_cycles[3][0],
        collision_cycles[5][2],
        collision_cycles[8][4],
        Fraction(-103, 17),
    )
    records: list[tuple[int, int, int]] = []

    for beta in (Fraction(1, 2), Fraction(3, 4), Fraction(9, 10)):
        m = choose_avoiding_m(beta, centers)
        cycle = rational_cycle(m)
        contact = max(
            v2_frac(phase - center) for phase in cycle for center in centers
        )
        reserve = max(1, contact + 1)
        phase_features = tuple(feature(phase, centers) for phase in cycle)
        feature_classes = sorted(set(phase_features))
        weights = {
            item: Fraction(index + 1, index + 2)
            for index, item in enumerate(feature_classes)
        }

        found = False
        for periods in (8, 16, 32, 64, 128):
            values, _ = normalized_lift(m, periods, reserve)
            value_features = tuple(feature(Fraction(n), centers) for n in values)
            assert all(
                item == phase_features[j % m]
                for j, item in enumerate(value_features)
            )

            # For V(n)=log_2(n)+log_2(weight(feature)), minimizing V is
            # exactly minimizing the positive rational score below.
            scores = tuple(
                Fraction(n) * weights[item]
                for n, item in zip(values, value_features)
            )
            minimum = min(scores)
            jstar = max(j for j, score in enumerate(scores) if score == minimum)
            assert jstar < m
            assert all(score > scores[jstar] for score in scores[jstar + 1 :])

            remaining = periods * m - jstar
            p, q = beta.numerator, beta.denominator
            if values[jstar] ** p < 2 ** (q * remaining):
                records.append((m, periods, jstar))
                found = True
                break
        assert found

    return len(records), tuple(records)


def main() -> None:
    if not __debug__:
        raise RuntimeError(
            "H-FCS-001 diagnostics require assertions; rerun without -O "
            "and with PYTHONOPTIMIZE unset"
        )

    print("H-FCS-001 EXACT DIAGNOSTICS")
    print("Scope: finite algebra checks; not an infinite proof and not Collatz.\n")

    cycle_count, phase_count = test_cycles()
    print(f"PASS A: {cycle_count} cycles and {phase_count} distinct phases checked.")

    lift_count = test_lifts()
    print(f"PASS B: {lift_count} exact lifts checked through their endpoints.")

    horizon_count, records = test_freezing_and_horizon()
    print(f"PASS C: {horizon_count} finite-center horizon contradictions: {records}.")
    print("\nH-FCS-001 DIAGNOSTICS = PASS")


if __name__ == "__main__":
    main()
