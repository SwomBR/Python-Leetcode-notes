"""Tests for 037 Valid Palindrome."""
import random
import string


def _reference(s):
    cleaned = [c.lower() for c in s if c.isalnum()]
    return cleaned == cleaned[::-1]


def check(ns):
    solve = ns["Solution"]().isPalindrome
    # Official examples
    assert solve("A man, a plan, a canal: Panama") is True
    assert solve("race a car") is False
    assert solve(" ") is True
    # Edge cases
    assert solve("a") is True
    assert solve(".,") is True
    assert solve("0P") is False
    assert solve("ab_a") is True
    assert solve("Aa") is True
    assert solve("1b1") is True
    assert solve("12") is False
    assert solve("No 'x' in Nixon") is True
    rng = random.Random(37)
    alphabet = "aAbB01 ,:!_."
    for _ in range(400):
        s = "".join(rng.choice(alphabet) for _ in range(rng.randint(1, 12)))
        assert solve(s) == _reference(s), s
    for _ in range(200):
        half = "".join(rng.choice(string.printable[:95]) for _ in range(rng.randint(0, 8)))
        s = half + rng.choice(["", "x", " "]) + half[::-1].swapcase()
        if not s:
            s = " "
        assert solve(s) == _reference(s), s
        assert solve(s) is True, s
