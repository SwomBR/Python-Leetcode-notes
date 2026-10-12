"""Tests for 015 Reverse Bits."""
import random

MIN_TESTED_BLOCKS = 3


def reference(n):
    bits = [(n >> i) & 1 for i in range(32)]   # bits[i] = bit i of n
    value = 0
    for i, bit in enumerate(bits):
        if bit:
            value |= 1 << (31 - i)
    return value


def check(ns):
    solve = ns["Solution"]().reverseBits
    # Official examples
    assert solve(43261596) == 964176192
    assert solve(2147483644) == 1073741822
    # Edge cases (all even, within 0 <= n <= 2^31 - 2)
    assert solve(0) == 0
    assert solve(2) == 1 << 30
    assert solve(2 ** 31 - 2) == 2 ** 31 - 2
    assert solve(6) == 1610612736
    assert solve(8) == 1 << 28
    assert solve(0b0110 << 14) == 98304
    for k in range(1, 31):
        assert solve(1 << k) == 1 << (31 - k), k
    rng = random.Random(15)
    for _ in range(3000):
        n = rng.randint(0, 2 ** 30 - 1) * 2
        result = solve(n)
        assert result == reference(n), n
        assert 0 <= result <= 2 ** 31 - 1
