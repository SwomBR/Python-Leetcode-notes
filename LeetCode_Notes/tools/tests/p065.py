"""Tests for 065 Jump Game."""
import random
from collections import deque


def _reference(nums):
    """Breadth-first search over indices."""
    n = len(nums)
    seen = {0}
    queue = deque([0])
    while queue:
        i = queue.popleft()
        for j in range(i + 1, min(n, i + nums[i] + 1)):
            if j not in seen:
                seen.add(j)
                queue.append(j)
    return n - 1 in seen


def check(ns):
    solve = ns["Solution"]().canJump
    assert solve([2, 3, 1, 1, 4]) is True
    assert solve([3, 2, 1, 0, 4]) is False
    assert solve([0]) is True
    assert solve([0, 1]) is False
    assert solve([1, 0]) is True
    assert solve([2, 0, 0]) is True
    assert solve([1, 0, 1]) is False
    assert solve([5, 0, 0, 0, 0, 0]) is True
    assert solve([1, 1, 0, 1]) is False
    rng = random.Random(65)
    for _ in range(400):
        nums = [rng.randint(0, 3) for _ in range(rng.randint(1, 11))]
        assert solve(list(nums)) == _reference(nums), nums
