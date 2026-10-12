"""Tests for 075 Find Median from Data Stream (design problem)."""
import random
import statistics

TARGET = "MedianFinder"


def _close(a, b):
    return abs(a - b) <= 1e-5


def check(ns):
    cls = ns["MedianFinder"]
    # Official operation sequence
    mf = cls()
    assert mf.addNum(1) is None
    mf.addNum(2)
    assert _close(mf.findMedian(), 1.5)
    mf.addNum(3)
    assert _close(mf.findMedian(), 2.0)
    # Single element, negatives, duplicates, extremes
    mf = cls()
    mf.addNum(-100000)
    assert _close(mf.findMedian(), -100000)
    mf.addNum(100000)
    assert _close(mf.findMedian(), 0.0)
    mf = cls()
    for x in [5, 5, 5, 5]:
        mf.addNum(x)
        assert _close(mf.findMedian(), 5)
    mf = cls()
    for x, want in zip([6, 10, 2, 6, 5, 0], [6, 8, 6, 6, 6, 5.5]):
        mf.addNum(x)
        assert _close(mf.findMedian(), want), (x, want)
    # Independent instances must not share state
    a, b = cls(), cls()
    a.addNum(1)
    b.addNum(100)
    assert _close(a.findMedian(), 1) and _close(b.findMedian(), 100)
    # Random operation sequences vs statistics.median
    rng = random.Random(75)
    for _ in range(150):
        mf = cls()
        seen = []
        low, high = rng.choice([(-100000, 100000), (0, 100), (-3, 3)])
        for _ in range(rng.randint(1, 120)):
            if seen and rng.random() < 0.4:
                assert _close(mf.findMedian(), statistics.median(seen)), seen
            else:
                x = rng.randint(low, high)
                mf.addNum(x)
                seen.append(x)
        assert _close(mf.findMedian(), statistics.median(seen)), seen
