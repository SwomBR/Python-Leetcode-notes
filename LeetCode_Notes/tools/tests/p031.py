"""Tests for 031 Longest Substring Without Repeating Characters (LeetCode 3)."""
import random


def _reference(s):
    best = 0
    for i in range(len(s)):
        for j in range(i, len(s)):
            if len(set(s[i:j + 1])) == j - i + 1:
                best = max(best, j - i + 1)
    return best


def check(ns):
    solve = ns["Solution"]().lengthOfLongestSubstring
    assert solve("abcabcbb") == 3
    assert solve("bbbbb") == 1
    assert solve("pwwkew") == 3
    assert solve("") == 0
    assert solve(" ") == 1
    assert solve("au") == 2
    assert solve("dvdf") == 3
    assert solve("abba") == 2
    assert solve("tmmzuxt") == 5
    assert solve("a b!a") == 4
    assert solve("abcdefghijklmnopqrstuvwxyz") == 26
    rng = random.Random(31)
    for _ in range(400):
        alphabet = rng.choice(["ab", "abc", "abcde", "aB1 !"])
        s = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 14)))
        assert solve(s) == _reference(s), s
