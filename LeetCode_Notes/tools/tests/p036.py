"""Tests for 036 Valid Parentheses."""
import random


def _reference(s):
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in s:
        if ch in "([{":
            stack.append(ch)
        elif not stack or stack.pop() != pairs[ch]:
            return False
    return not stack


def _random_valid(rng, depth=0):
    if depth > 4 or rng.random() < 0.3:
        return ""
    o, c = rng.choice(["()", "[]", "{}"])
    return o + _random_valid(rng, depth + 1) + c + _random_valid(rng, depth + 1)


def check(ns):
    solve = ns["Solution"]().isValid
    # Official examples
    assert solve("()") is True
    assert solve("()[]{}") is True
    assert solve("(]") is False
    assert solve("([])") is True
    assert solve("([)]") is False
    # Edge cases
    assert solve("(") is False
    assert solve(")") is False
    assert solve("((") is False
    assert solve("))") is False
    assert solve("){") is False
    assert solve("{[]}") is True
    assert solve("(((())))") is True
    assert solve("(()") is False
    assert solve("())") is False
    assert solve("]") is False
    rng = random.Random(36)
    for _ in range(400):
        s = "".join(rng.choice("()[]{}") for _ in range(rng.randint(1, 10)))
        assert solve(s) == _reference(s), s
    for _ in range(200):
        s = _random_valid(rng) or "()"
        assert solve(s) is True, s
