"""Tests for 056 Coin Change (LeetCode 322)."""
import random
from collections import deque


def _reference(coins, amount):
    # Independent check: breadth-first search over remaining amounts.
    if amount == 0:
        return 0
    seen = {amount}
    queue = deque([(amount, 0)])
    while queue:
        remaining, used = queue.popleft()
        for coin in coins:
            nxt = remaining - coin
            if nxt == 0:
                return used + 1
            if nxt > 0 and nxt not in seen:
                seen.add(nxt)
                queue.append((nxt, used + 1))
    return -1


def check(ns):
    solve = ns["Solution"]().coinChange
    # Official examples
    assert solve([1, 2, 5], 11) == 3
    assert solve([2], 3) == -1
    assert solve([1], 0) == 0
    # Edge cases
    assert solve([1, 3, 4], 6) == 2          # greedy would give 3
    assert solve([5], 3) == -1               # coin larger than amount
    assert solve([2147483647], 2) == -1      # huge coin
    assert solve([2147483647], 0) == 0
    assert solve([3, 7], 14) == 2
    assert solve([2, 5], 1) == -1
    rng = random.Random(56)
    for _ in range(200):
        coins = rng.sample(range(1, 9), rng.randint(1, 3))
        amount = rng.randint(0, 14)
        assert solve(list(coins), amount) == _reference(coins, amount), (coins, amount)
