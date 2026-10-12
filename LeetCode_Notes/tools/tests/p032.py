"""Tests for 032 Longest Repeating Character Replacement (LeetCode 424)."""
import random


def _reference(s, k):
    best = 0
    for i in range(len(s)):
        for j in range(i, len(s)):
            window = s[i:j + 1]
            most = max(window.count(c) for c in set(window))
            if len(window) - most <= k:
                best = max(best, len(window))
    return best


def check(ns):
    solve = ns["Solution"]().characterReplacement
    assert solve("ABAB", 2) == 4
    assert solve("AABABBA", 1) == 4
    assert solve("A", 0) == 1
    assert solve("A", 1) == 1
    assert solve("AAAA", 0) == 4
    assert solve("ABCD", 0) == 1
    assert solve("ABCD", 4) == 4
    assert solve("ABBB", 2) == 4
    assert solve("AAABBC", 0) == 3
    assert solve("BAAAB", 2) == 5
    rng = random.Random(32)
    for _ in range(400):
        s = "".join(rng.choice(rng.choice(["AB", "ABC", "ABCD"]))
                    for _ in range(rng.randint(1, 12)))
        k = rng.randint(0, len(s))
        assert solve(s, k) == _reference(s, k), (s, k)
