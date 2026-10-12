"""Tests for 021 Reverse Linked List (LeetCode 206)."""
import random

MIN_TESTED_BLOCKS = 3  # brute force, iterative, recursive


def _build(ListNode, values):
    head = None
    for v in reversed(values):
        head = ListNode(v, head)
    return head


def _to_list(head, limit=100000):
    out = []
    while head is not None:
        out.append(head.val)
        head = head.next
        assert len(out) <= limit, "result list seems to contain a cycle"
    return out


def check(ns):
    ListNode = ns["ListNode"]
    solve = ns["Solution"]().reverseList

    def run(values):
        return _to_list(solve(_build(ListNode, values)))

    # Official examples
    assert run([1, 2, 3, 4, 5]) == [5, 4, 3, 2, 1]
    assert run([1, 2]) == [2, 1]
    assert run([]) == []
    assert solve(None) is None
    # Edge cases
    assert run([7]) == [7]
    assert run([-5000, 5000]) == [5000, -5000]
    assert run([3, 3, 3]) == [3, 3, 3]
    # Reversing twice gives back the original order
    head = _build(ListNode, [1, 2, 3])
    assert _to_list(solve(solve(head))) == [1, 2, 3]
    # The new head holds the old last value and the list ends properly
    head = _build(ListNode, [1, 2, 3])
    new_head = solve(head)
    assert new_head.val == 3 and _to_list(new_head) == [3, 2, 1]
    # Randomized comparison against slicing-based reversal
    rng = random.Random(21)
    for _ in range(300):
        values = [rng.randint(-5000, 5000) for _ in range(rng.randint(0, 60))]
        assert run(values) == values[::-1], values
