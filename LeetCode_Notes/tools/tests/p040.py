"""Tests for 040 Encode and Decode Strings (LeetCode 271, Premium).

The official statement could not be fetched; these tests check the
well-known contract: decode(encode(strs)) == strs for any list of strings
over the 256 ASCII characters chr(0)..chr(255).
"""
import random

TARGET = "Codec"

BACKSLASH = chr(92)


def _round_trip(ns, strs):
    # LeetCode uses separate Codec objects for encode and decode.
    encoded = ns["Codec"]().encode(list(strs))
    assert isinstance(encoded, str)
    decoded = ns["Codec"]().decode(encoded)
    assert decoded == strs, (strs, encoded, decoded)


def check(ns):
    # Commonly published examples
    _round_trip(ns, ["Hello", "World"])
    _round_trip(ns, [""])
    # Tricky contents
    for strs in [
        ["", ""], ["", "", ""], ["#"], ["##", "#"], ["3#abc"], ["5#", "#5"],
        ["12#hello", "0#"], ["a" * 200],
        [BACKSLASH, BACKSLASH * 2, BACKSLASH + "#", BACKSLASH + ","],
        [",", ";", "|", ",,", ""],
        [chr(0), chr(255), "\n"], ["10", "#", "", "x#y#z"], [" ", "  "],
        ["Hello", "", "World", ""], [chr(i) for i in range(256)],
        ["".join(chr(i) for i in range(256))],
        [],
    ]:
        _round_trip(ns, strs)
    rng = random.Random(40)
    alphabet = [chr(i) for i in range(256)]
    tricky = list("#0123456789:,") + [BACKSLASH, chr(0), chr(255)]
    for _ in range(400):
        pool = tricky if rng.random() < 0.5 else alphabet
        strs = ["".join(rng.choice(pool) for _ in range(rng.randint(0, 12)))
                for _ in range(rng.randint(1, 8))]
        _round_trip(ns, strs)
    big = ["".join(rng.choice(alphabet) for _ in range(200)) for _ in range(200)]
    _round_trip(ns, big)
