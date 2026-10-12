"""Tests for 023 Merge Two Sorted Lists (LeetCode 21)."""
import random


def _build(ListNode, values):
    head = None
    for v in reversed(values):
        head = ListNode(v, head)
    return head


def _nodes(head, limit=100000):
    out = []
    while head is not None:
        out.append(head)
        head = head.next
        assert len(out) <= limit, "result list seems to contain a cycle"
    return out


def check(ns):
    ListNode = ns["ListNode"]
    solve = ns["Solution"]().mergeTwoLists

    def run(a, b):
        l1, l2 = _build(ListNode, a), _build(ListNode, b)
        original_ids = {id(n) for n in _nodes(l1) + _nodes(l2)}
        result = _nodes(solve(l1, l2))
        # Splicing: the merged list must reuse exactly the original nodes.
        assert len(result) == len(original_ids)
        assert {id(n) for n in result} == original_ids
        return [n.val for n in result]

    # Official examples
    assert run([1, 2, 4], [1, 3, 4]) == [1, 1, 2, 3, 4, 4]
    assert run([], []) == []
    assert run([], [0]) == [0]
    assert solve(None, None) is None
    # Edge cases
    assert run([0], []) == [0]
    assert run([1, 2, 3], [4, 5, 6]) == [1, 2, 3, 4, 5, 6]
    assert run([4, 5, 6], [1, 2, 3]) == [1, 2, 3, 4, 5, 6]
    assert run([-100, 100], [-100, 100]) == [-100, -100, 100, 100]
    assert run([2, 2, 2], [2]) == [2, 2, 2, 2]
    # Randomized comparison against sorted()
    rng = random.Random(23)
    for _ in range(400):
        a = sorted(rng.randint(-100, 100) for _ in range(rng.randint(0, 50)))
        b = sorted(rng.randint(-100, 100) for _ in range(rng.randint(0, 50)))
        assert run(a, b) == sorted(a + b), (a, b)
