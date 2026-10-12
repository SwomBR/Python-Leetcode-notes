"""Tests for 026 Reorder List (in place, returns None)."""
import random


def _build(ns, values):
    ListNode = ns["ListNode"]
    head = None
    for v in reversed(values):
        head = ListNode(v, head)
    return head


def _nodes(head, limit):
    out = []
    while head is not None:
        out.append(head)
        assert len(out) <= limit, "cycle or extra nodes after reorder"
        head = head.next
    return out


def _reference(values):
    out = []
    i, j = 0, len(values) - 1
    while i <= j:
        out.append(values[i])
        if i != j:
            out.append(values[j])
        i += 1
        j -= 1
    return out


def _run(ns, values):
    head = _build(ns, values)
    original = _nodes(head, len(values))
    original_vals = {id(node): node.val for node in original}
    result = ns["Solution"]().reorderList(head)
    assert result is None, "reorderList must return None"
    after = _nodes(head, len(values))
    assert len(after) == len(values), "nodes were lost"
    assert sorted(map(id, after)) == sorted(map(id, original)), "nodes must be reused"
    for node in after:
        assert node.val == original_vals[id(node)], "node values must not be modified"
    return [node.val for node in after]


def check(ns):
    assert _run(ns, [1, 2, 3, 4]) == [1, 4, 2, 3]
    assert _run(ns, [1, 2, 3, 4, 5]) == [1, 5, 2, 4, 3]
    assert _run(ns, [7]) == [7]
    assert _run(ns, [1, 2]) == [1, 2]
    assert _run(ns, [1, 2, 3]) == [1, 3, 2]
    assert _run(ns, [5, 5, 5, 5]) == [5, 5, 5, 5]
    rng = random.Random(26)
    for _ in range(300):
        values = [rng.randint(1, 1000) for _ in range(rng.randint(1, 40))]
        assert _run(ns, values) == _reference(values), values
    big = [rng.randint(1, 1000) for _ in range(5000)]
    assert _run(ns, big) == _reference(big)
