"""Tests for 074 Top K Frequent Elements. Order is free, so compare sorted."""
import random


def _reference(nums, k):
    freq = {}
    for x in nums:
        freq[x] = freq.get(x, 0) + 1
    ranked = sorted(freq, key=lambda v: -freq[v])
    return sorted(ranked[:k])


def _unique(nums, k):
    freq = {}
    for x in nums:
        freq[x] = freq.get(x, 0) + 1
    counts = sorted(freq.values(), reverse=True)
    return k == len(counts) or counts[k - 1] != counts[k]


def check(ns):
    solve = ns["Solution"]().topKFrequent
    assert sorted(solve([1, 1, 1, 2, 2, 3], 2)) == [1, 2]
    assert sorted(solve([1], 1)) == [1]
    assert sorted(solve([1, 2, 1, 2, 1, 2, 3, 1, 3, 2], 2)) == [1, 2]
    assert sorted(solve([4, 4, 5, 5, 6], 3)) == [4, 5, 6]          # k = all unique values
    assert sorted(solve([-1, -1, 3], 1)) == [-1]                   # negatives
    assert sorted(solve([7] * 5, 1)) == [7]
    assert sorted(solve([-10000, 10000, 10000], 1)) == [10000]
    rng = random.Random(74)
    tested = 0
    while tested < 300:
        nums = [rng.randint(-6, 6) for _ in range(rng.randint(1, 30))]
        k = rng.randint(1, len(set(nums)))
        if not _unique(nums, k):
            continue
        tested += 1
        assert sorted(solve(list(nums), k)) == _reference(nums, k), (nums, k)
