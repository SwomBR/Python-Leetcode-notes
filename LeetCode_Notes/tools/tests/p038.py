"""Tests for 038 Longest Palindromic Substring.

Several longest palindromes may exist, so we check that the answer is a
palindromic substring of s whose length equals the maximum possible length.
"""
import random


def _max_len(s):
    best = 0
    n = len(s)
    for i in range(n):
        for j in range(i, n):
            sub = s[i:j + 1]
            if sub == sub[::-1]:
                best = max(best, j - i + 1)
    return best


def _ok(s, result):
    return (isinstance(result, str) and result in s and result == result[::-1]
            and len(result) == _max_len(s))


def check(ns):
    solve = ns["Solution"]().longestPalindrome
    # Official examples
    assert solve("babad") in ("bab", "aba")
    assert solve("cbbd") == "bb"
    # Edge cases (unique answers)
    assert solve("a") == "a"
    assert solve("aaaa") == "aaaa"
    assert solve("racecar") == "racecar"
    assert solve("forgeeksskeegfor") == "geeksskeeg"
    assert solve("abacdfgdcaba") in ("aba",)
    for s in ["ac", "abcd", "abb", "bba", "A1b1A", "aAa"]:
        assert _ok(s, solve(s)), s
    rng = random.Random(38)
    for _ in range(400):
        s = "".join(rng.choice("abc") for _ in range(rng.randint(1, 14)))
        assert _ok(s, solve(s)), s
    for _ in range(50):
        s = "".join(rng.choice("ab1Z") for _ in range(rng.randint(1, 30)))
        assert _ok(s, solve(s)), s
