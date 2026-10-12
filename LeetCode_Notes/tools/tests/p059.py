"""Tests for 059 Word Break (LeetCode 139)."""
import random
import re


def _reference(s, words):
    # Independent check: a regular expression "(w1|w2|...)+" must match all of s.
    pattern = "(?:" + "|".join(map(re.escape, words)) + ")+"
    return re.fullmatch(pattern, s) is not None


def check(ns):
    solve = ns["Solution"]().wordBreak
    # Official examples
    assert solve("leetcode", ["leet", "code"]) is True
    assert solve("applepenapple", ["apple", "pen"]) is True
    assert solve("catsandog", ["cats", "dog", "sand", "and", "cat"]) is False
    # Edge cases
    assert solve("a", ["a"]) is True
    assert solve("a", ["b"]) is False
    assert solve("goalspecial", ["go", "goal", "goals", "special"]) is True
    assert solve("aaaaaaa", ["aaaa", "aaa"]) is True
    assert solve("ab", ["abc"]) is False
    assert solve("aaaaaaaaaaab", ["a", "aa", "aaa"]) is False
    rng = random.Random(59)
    for _ in range(200):
        s = "".join(rng.choice("ab") for _ in range(rng.randint(1, 10)))
        pool = sorted({"".join(rng.choice("ab") for _ in range(rng.randint(1, 3)))
                       for _ in range(rng.randint(1, 4))})
        assert solve(s, list(pool)) == _reference(s, pool), (s, pool)
