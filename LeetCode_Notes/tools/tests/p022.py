"""Tests for 022 Linked List Cycle (LeetCode 141)."""
import random


def _build_with_cycle(ListNode, values, pos):
    """Build a list; if pos != -1, link the tail back to the node at index pos."""
    nodes = [ListNode(v) for v in values]
    for a, b in zip(nodes, nodes[1:]):
        a.next = b
    if pos != -1:
        nodes[-1].next = nodes[pos]
    return nodes[0] if nodes else None


def _reference(values, pos):
    # By construction a cycle exists exactly when the list is non-empty and pos != -1.
    return len(values) > 0 and pos != -1


def check(ns):
    ListNode = ns["ListNode"]
    solve = ns["Solution"]().hasCycle

    def run(values, pos):
        return solve(_build_with_cycle(ListNode, values, pos))

    # Official examples
    assert run([3, 2, 0, -4], 1) is True
    assert run([1, 2], 0) is True
    assert run([1], -1) is False
    # Edge cases
    assert run([], -1) is False
    assert solve(None) is False
    assert run([1], 0) is True              # a node pointing to itself
    assert run([1, 2], -1) is False
    assert run([1, 2, 3], 2) is True        # tail points to itself
    assert run([5, 5, 5, 5], -1) is False   # equal values but no cycle
    assert run([5, 5, 5, 5], 3) is True
    # Randomized comparison
    rng = random.Random(22)
    for _ in range(400):
        n = rng.randint(0, 40)
        values = [rng.randint(-10, 10) for _ in range(n)]
        pos = -1 if n == 0 or rng.random() < 0.5 else rng.randrange(n)
        assert run(values, pos) is _reference(values, pos), (values, pos)
    # Upper constraint size (10^4 nodes), with and without a cycle
    assert run(list(range(10 ** 4)), -1) is False
    assert run(list(range(10 ** 4)), 0) is True
    assert run(list(range(10 ** 4)), 10 ** 4 - 1) is True
