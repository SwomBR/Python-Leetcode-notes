"""Tests for 052 Implement Trie (Prefix Tree) (LeetCode 208)."""
import random

TARGET = "Trie"


def _run(ns, ops, args):
    obj = None
    out = []
    for op, arg in zip(ops, args):
        if op == "Trie":
            obj = ns["Trie"]()
            out.append(None)
        else:
            out.append(getattr(obj, op)(*arg))
    return out


def check(ns):
    ops = ["Trie", "insert", "search", "search", "startsWith", "insert", "search"]
    args = [[], ["apple"], ["apple"], ["app"], ["app"], ["app"], ["app"]]
    assert _run(ns, ops, args) == [None, None, True, False, True, None, True]

    t = ns["Trie"]()
    assert t.search("a") is False
    assert t.startsWith("a") is False
    t.insert("a")
    assert t.search("a") is True and t.startsWith("a") is True
    assert t.search("aa") is False and t.startsWith("aa") is False
    t.insert("a")                       # a duplicate insert is harmless
    assert t.search("a") is True
    long_word = "z" * 2000
    t.insert(long_word)
    assert t.search(long_word) is True
    assert t.search("z" * 1999) is False
    assert t.startsWith("z" * 1999) is True
    assert t.startsWith(long_word) is True   # a word is a prefix of itself

    rng = random.Random(52)
    for _ in range(60):
        trie = ns["Trie"]()
        model = set()                    # reference model
        for _ in range(150):
            word = "".join(rng.choice("abc") for _ in range(rng.randint(1, 5)))
            op = rng.choice(["insert", "search", "startsWith"])
            if op == "insert":
                assert trie.insert(word) is None
                model.add(word)
            elif op == "search":
                assert trie.search(word) is (word in model), (op, word)
            else:
                expected = any(w.startswith(word) for w in model)
                assert trie.startsWith(word) is expected, (op, word)
