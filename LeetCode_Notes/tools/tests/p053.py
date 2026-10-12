"""Tests for 053 Design Add and Search Words Data Structure (LeetCode 211)."""
import random

TARGET = "WordDictionary"


def _matches(pattern, word):
    if len(pattern) != len(word):
        return False
    return all(p == "." or p == c for p, c in zip(pattern, word))


def check(ns):
    WD = ns["WordDictionary"]
    d = WD()
    assert d.addWord("bad") is None
    d.addWord("dad")
    d.addWord("mad")
    assert d.search("pad") is False
    assert d.search("bad") is True
    assert d.search(".ad") is True
    assert d.search("b..") is True

    d = WD()
    assert d.search("a") is False
    assert d.search(".") is False
    d.addWord("a")
    assert d.search(".") is True
    assert d.search("..") is False      # a dot matches exactly one letter
    assert d.search("a.") is False
    d.addWord("ab")
    assert d.search("a.") is True
    assert d.search(".b") is True
    assert d.search(".c") is False
    assert d.search("..") is True
    d.addWord("x" * 25)
    assert d.search("x" * 23 + "..") is True
    assert d.search("x" * 24) is False

    rng = random.Random(53)
    for _ in range(60):
        wd = WD()
        model = []                       # reference model: plain list of words
        for _ in range(150):
            length = rng.randint(1, 5)
            if rng.random() < 0.4:
                word = "".join(rng.choice("abc") for _ in range(length))
                assert wd.addWord(word) is None
                model.append(word)
            else:
                chars = [rng.choice("abc") for _ in range(length)]
                for i in rng.sample(range(length), min(length, rng.randint(0, 2))):
                    chars[i] = "."
                pattern = "".join(chars)
                expected = any(_matches(pattern, w) for w in model)
                assert wd.search(pattern) is expected, pattern
