"""Tests for 039 Palindromic Substrings."""
import random


def _reference(s):
    n = len(s)
    return sum(1 for i in range(n) for j in range(i + 1, n + 1) if s[i:j] == s[i:j][::-1])


def check(ns):
    solve = ns["Solution"]().countSubstrings
    # Official examples
    assert solve("abc") == 3
    assert solve("aaa") == 6
    # Edge cases
    assert solve("a") == 1
    assert solve("aa") == 3
    assert solve("ab") == 2
    assert solve("aba") == 4
    assert solve("abba") == 6
    assert solve("aaaa") == 10
    rng = random.Random(39)
    for _ in range(400):
        s = "".join(rng.choice("abc") for _ in range(rng.randint(1, 15)))
        assert solve(s) == _reference(s), s
    s = "a" * 60
    assert solve(s) == 60 * 61 // 2
