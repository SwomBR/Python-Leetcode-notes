"""Tests for 033 Minimum Window Substring (LeetCode 76).

Official examples (unique answers) are compared exactly.  Random inputs may
have several minimum windows, so there we check properties instead: the
result is a substring of s, covers t, and has the minimum possible length.
"""
import random
from collections import Counter


def _covers(window, t):
    need = Counter(t)
    have = Counter(window)
    return all(have[c] >= n for c, n in need.items())


def _min_length(s, t):
    best = 0
    for i in range(len(s)):
        for j in range(i, len(s)):
            if _covers(s[i:j + 1], t):
                if best == 0 or j - i + 1 < best:
                    best = j - i + 1
                break
    return best


def check(ns):
    solve = ns["Solution"]().minWindow
    assert solve("ADOBECODEBANC", "ABC") == "BANC"
    assert solve("a", "a") == "a"
    assert solve("a", "aa") == ""
    assert solve("a", "b") == ""
    assert solve("ab", "b") == "b"
    assert solve("aa", "aa") == "aa"
    assert solve("bba", "ab") == "ba"
    assert solve("aA", "A") == "A"           # case-sensitive
    assert solve("abc", "abcd") == ""        # t longer than s
    assert solve("cabwefgewcwaefgcf", "cae") == "cwae"
    rng = random.Random(33)
    for _ in range(400):
        s = "".join(rng.choice("abcA") for _ in range(rng.randint(1, 12)))
        t = "".join(rng.choice("abcA") for _ in range(rng.randint(1, 4)))
        got = solve(s, t)
        length = _min_length(s, t)
        if length == 0:
            assert got == "", (s, t, got)
        else:
            assert len(got) == length, (s, t, got)
            assert got in s and _covers(got, t), (s, t, got)
