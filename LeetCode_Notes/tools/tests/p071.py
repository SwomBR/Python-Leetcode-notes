"""Tests for 071 Alien Dictionary (LeetCode 269, Premium).

Several orders can be valid, so outputs are VALIDATED instead of compared:
  * for an invalid input (cycle or "longer word before its own prefix"),
    the answer must be "";
  * otherwise the answer must contain every distinct letter exactly once
    and respect every ordering rule derived from adjacent word pairs.
The independent reference below decides validity by brute-force search
over letter permutations for small alphabets (no topological sort).
"""
import itertools
import random


def _rules(words):
    """Return (letters, edges) or None if a prefix violation exists."""
    letters = set("".join(words))
    edges = set()
    for w1, w2 in zip(words, words[1:]):
        for a, b in zip(w1, w2):
            if a != b:
                edges.add((a, b))
                break
        else:
            if len(w1) > len(w2):
                return None
    return letters, edges


def _has_valid_order(words):
    """Independent reference: does ANY permutation sort the word list?"""
    letters = sorted(set("".join(words)))
    for perm in itertools.permutations(letters):
        rank = {c: i for i, c in enumerate(perm)}
        keys = [[rank[c] for c in w] for w in words]
        if all(keys[i] <= keys[i + 1] for i in range(len(keys) - 1)):
            return True
    return False


def _validate(words, answer):
    expected_valid = _has_valid_order(words)
    if not expected_valid:
        assert answer == "", (words, answer)
        return
    info = _rules(words)
    assert info is not None, words
    letters, edges = info
    assert isinstance(answer, str), (words, answer)
    assert len(answer) == len(letters) and set(answer) == letters, (words, answer)
    pos = {c: i for i, c in enumerate(answer)}
    for a, b in edges:
        assert pos[a] < pos[b], (words, answer, a, b)


def check(ns):
    solve = ns["Solution"]().alienOrder
    # Commonly published examples
    _validate(["wrt", "wrf", "er", "ett", "rftt"], solve(["wrt", "wrf", "er", "ett", "rftt"]))
    assert solve(["wrt", "wrf", "er", "ett", "rftt"]) == "wertf"  # the only valid order
    assert solve(["z", "x"]) == "zx"
    assert solve(["z", "x", "z"]) == ""
    # Prefix violation and its valid counterpart
    assert solve(["abc", "ab"]) == ""
    _validate(["ab", "abc"], solve(["ab", "abc"]))
    # Single word / duplicate words: any order of the letters
    assert solve(["z"]) == "z"
    _validate(["abc", "abc"], solve(["abc", "abc"]))
    _validate(["ab", "adc"], solve(["ab", "adc"]))
    # Letters with no rules must still appear
    _validate(["ac", "ab", "zc", "zb"], solve(["ac", "ab", "zc", "zb"]))
    # Cycle a < b < a
    assert solve(["ab", "ba", "ab"]) == ""
    assert solve(["a", "b", "a"]) == ""
    assert solve(["ba", "bc", "ac", "cab"]) == "bac"  # b<a, a<c: unique
    assert solve(["ab", "bc", "ca", "ab"]) == ""  # a<b, b<c, c<a: cycle
    rng = random.Random(71)
    for trial in range(300):
        alphabet = "abcdefg"[: rng.randint(1, 6)]
        hidden = list(alphabet)
        rng.shuffle(hidden)
        rank = {c: i for i, c in enumerate(hidden)}
        words = ["".join(rng.choice(alphabet) for _ in range(rng.randint(1, 4)))
                 for _ in range(rng.randint(1, 7))]
        if trial % 3 != 0:  # mostly valid: sort by the hidden alien order
            words.sort(key=lambda w: [rank[c] for c in w])
        _validate(words, solve(list(words)))
