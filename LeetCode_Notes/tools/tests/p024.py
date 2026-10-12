"""Tests for 024 Merge K Sorted Lists (LeetCode 23)."""
import random

MIN_TESTED_BLOCKS = 3  # brute force, min-heap, divide and conquer


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


def _reference(lists):
    """Independent k-way merge: repeatedly take the smallest front value."""
    fronts = [0] * len(lists)
    out = []
    while True:
        best = -1
        for i, lst in enumerate(lists):
            if fronts[i] < len(lst) and (
                best == -1 or lst[fronts[i]] < lists[best][fronts[best]]
            ):
                best = i
        if best == -1:
            return out
        out.append(lists[best][fronts[best]])
        fronts[best] += 1


def check(ns):
    ListNode = ns["ListNode"]
    solve = ns["Solution"]().mergeKLists

    def run(lists):
        return _to_list(solve([_build(ListNode, lst) for lst in lists]))

    # Official examples
    assert run([[1, 4, 5], [1, 3, 4], [2, 6]]) == [1, 1, 2, 3, 4, 4, 5, 6]
    assert run([]) == []
    assert run([[]]) == []
    # Edge cases
    assert solve([]) is None
    assert solve([None]) is None
    assert run([[], [], []]) == []
    assert run([[1]]) == [1]
    assert run([[], [1], []]) == [1]
    assert run([[5, 5], [5], [5, 5, 5]]) == [5] * 6   # ties between nodes
    assert run([[-10000], [10000], [0]]) == [-10000, 0, 10000]
    assert run([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == list(range(1, 10))
    # Randomized comparison
    rng = random.Random(24)
    for _ in range(300):
        k = rng.randint(0, 8)
        lists = [sorted(rng.randint(-20, 20) for _ in range(rng.randint(0, 8)))
                 for _ in range(k)]
        assert run(lists) == _reference(lists), lists
    # Many lists (large k) with few nodes each
    lists = [sorted(rng.randint(-10 ** 4, 10 ** 4) for _ in range(rng.randint(0, 2)))
             for _ in range(2000)]
    assert run(lists) == sorted(v for lst in lists for v in lst)
