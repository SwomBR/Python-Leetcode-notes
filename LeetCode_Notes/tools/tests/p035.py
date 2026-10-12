"""Tests for 035 Group Anagrams (LeetCode 49).

Groups and the words inside each group may come back in any order, so both
levels are sorted before comparing.
"""
import random


def _normalize(groups):
    return sorted(sorted(group) for group in groups)


def _reference(strs):
    groups = []
    for word in strs:
        for group in groups:
            if sorted(group[0]) == sorted(word):
                group.append(word)
                break
        else:
            groups.append([word])
    return groups


def check(ns):
    solve = ns["Solution"]().groupAnagrams
    assert _normalize(solve(["eat", "tea", "tan", "ate", "nat", "bat"])) == \
        _normalize([["bat"], ["nat", "tan"], ["ate", "eat", "tea"]])
    assert _normalize(solve([""])) == [[""]]
    assert _normalize(solve(["a"])) == [["a"]]
    assert _normalize(solve(["", ""])) == [["", ""]]
    assert _normalize(solve(["abc", "abc", "cba"])) == [["abc", "abc", "cba"]]
    assert _normalize(solve(["ab", "abb", "bba", "ba"])) == \
        _normalize([["ab", "ba"], ["abb", "bba"]])
    assert _normalize(solve(["a", "b", "c"])) == [["a"], ["b"], ["c"]]
    rng = random.Random(35)
    for _ in range(300):
        strs = ["".join(rng.choice("abc") for _ in range(rng.randint(0, 4)))
                for _ in range(rng.randint(1, 10))]
        assert _normalize(solve(list(strs))) == _normalize(_reference(strs)), strs
