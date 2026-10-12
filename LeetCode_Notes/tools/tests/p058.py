"""Tests for 058 Longest Common Subsequence (LeetCode 1143)."""
import random


def _is_subsequence(small, big):
    it = iter(big)
    return all(ch in it for ch in small)


def _reference(a, b):
    # Independent check: every subsequence of `a`, tested against `b`.
    best = 0
    n = len(a)
    for mask in range(1 << n):
        sub = "".join(a[i] for i in range(n) if mask >> i & 1)
        if len(sub) > best and _is_subsequence(sub, b):
            best = len(sub)
    return best


def check(ns):
    solve = ns["Solution"]().longestCommonSubsequence
    # Official examples
    assert solve("abcde", "ace") == 3
    assert solve("abc", "abc") == 3
    assert solve("abc", "def") == 0
    # Edge cases
    assert solve("a", "a") == 1
    assert solve("a", "b") == 0
    assert solve("ace", "abcde") == 3
    assert solve("abc", "cba") == 1
    assert solve("bsbininm", "jmjkbkjkv") == 1
    assert solve("aaaa", "aa") == 2
    rng = random.Random(58)
    for _ in range(200):
        a = "".join(rng.choice("abc") for _ in range(rng.randint(1, 7)))
        b = "".join(rng.choice("abc") for _ in range(rng.randint(1, 7)))
        assert solve(a, b) == _reference(a, b), (a, b)
