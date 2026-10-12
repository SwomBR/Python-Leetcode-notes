"""Tests for 002 Best Time to Buy and Sell Stock."""
import random


def _reference(prices):
    best = 0
    for i in range(len(prices)):
        for j in range(i + 1, len(prices)):
            best = max(best, prices[j] - prices[i])
    return best


def check(ns):
    solve = ns["Solution"]().maxProfit
    assert solve([7, 1, 5, 3, 6, 4]) == 5
    assert solve([7, 6, 4, 3, 1]) == 0
    assert solve([5]) == 0
    assert solve([1, 2]) == 1
    assert solve([2, 4, 1]) == 2
    assert solve([3, 3, 3]) == 0
    rng = random.Random(2)
    for _ in range(300):
        prices = [rng.randint(0, 50) for _ in range(rng.randint(1, 25))]
        assert solve(list(prices)) == _reference(prices), prices
