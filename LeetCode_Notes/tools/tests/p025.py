"""Tests for 025 Remove Nth Node From End of List (LeetCode 19)."""
import random


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
    solve = ns["Solution"]().removeNthFromEnd

    def run(values, n):
        return _to_list(solve(_build(ListNode, values), n))

    # Official examples
    assert run([1, 2, 3, 4, 5], 2) == [1, 2, 3, 5]
    assert run([1], 1) == []
    assert run([1, 2], 1) == [1]
    # Edge cases
    assert run([1, 2], 2) == [2]                    # remove the head
    assert run([1, 2, 3, 4, 5], 5) == [2, 3, 4, 5]
    assert run([1, 2, 3, 4, 5], 1) == [1, 2, 3, 4]  # remove the tail
    assert run([7, 7, 7], 2) == [7, 7]
    # Randomized comparison against list slicing
    rng = random.Random(25)
    for _ in range(400):
        sz = rng.randint(1, 30)
        values = [rng.randint(0, 100) for _ in range(sz)]
        n = rng.randint(1, sz)
        expected = values[:sz - n] + values[sz - n + 1:]
        assert run(values, n) == expected, (values, n)
