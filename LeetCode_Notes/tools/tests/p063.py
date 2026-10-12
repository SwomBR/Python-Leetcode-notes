"""Tests for 063 Decode Ways."""
import random


def _reference(s):
    """Try every way of cutting s into pieces of length 1 or 2 (bitmask of cuts)."""
    n = len(s)
    total = 0
    for mask in range(1 << (n - 1)):  # bit i set -> cut after position i
        pieces, start = [], 0
        for i in range(n - 1):
            if mask >> i & 1:
                pieces.append(s[start:i + 1])
                start = i + 1
        pieces.append(s[start:])
        if all(p[0] != "0" and len(p) <= 2 and 1 <= int(p) <= 26 for p in pieces):
            total += 1
    return total


def check(ns):
    solve = ns["Solution"]().numDecodings
    assert solve("12") == 2
    assert solve("226") == 3
    assert solve("06") == 0
    assert solve("11106") == 2
    for s, want in [("0", 0), ("1", 1), ("10", 1), ("20", 1), ("30", 0),
                    ("27", 1), ("26", 2), ("100", 0), ("101", 1), ("2101", 1),
                    ("1111", 5), ("00", 0), ("110", 1), ("1201234", 3)]:
        assert solve(s) == want, (s, want)
    rng = random.Random(63)
    digits = "0111222333456789"
    for _ in range(400):
        s = "".join(rng.choice(digits) for _ in range(rng.randint(1, 13)))
        assert solve(s) == _reference(s), s
