"""Tests for 034 Valid Anagram (LeetCode 242)."""
import random


def _reference(s, t):
    return sorted(s) == sorted(t)


def check(ns):
    solve = ns["Solution"]().isAnagram
    assert solve("anagram", "nagaram") is True
    assert solve("rat", "car") is False
    assert solve("a", "a") is True
    assert solve("a", "b") is False
    assert solve("ab", "a") is False
    assert solve("a", "ab") is False
    assert solve("aacc", "ccac") is False
    assert solve("listen", "silent") is True
    assert solve("aab", "abb") is False
    rng = random.Random(34)
    for _ in range(400):
        s = "".join(rng.choice("abc") for _ in range(rng.randint(1, 8)))
        if rng.random() < 0.5:
            chars = list(s)
            rng.shuffle(chars)
            t = "".join(chars)
        else:
            t = "".join(rng.choice("abc") for _ in range(rng.randint(1, 8)))
        assert solve(s, t) is _reference(s, t), (s, t)
