# 075. Find Median from Data Stream

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Find Median from Data Stream |
| **LeetCode number** | 295 |
| **Topic (source list)** | Heap |
| **Also uses** | Design, Sorting, Binary Search (`bisect`), Counting |
| **Difficulty** | Hard |
| **LeetCode URL** | <https://leetcode.com/problems/find-median-from-data-stream/> |
| **Pattern** | Two heaps: a max-heap for the lower half and a min-heap for the upper half |

---

## 2. Problem Explanation

### What is the median?

Sort the numbers. The **median** is the middle one. If there is an even count, there is no single middle, so the median is the **average of the two middle numbers**.

- `[2, 3, 4]` → median `3`.
- `[2, 3]` → median `(2 + 3) / 2 = 2.5`.

### What must we build?

A class `MedianFinder` with:

| Method | What it does |
|---|---|
| `MedianFinder()` | Creates an empty structure. |
| `addNum(num: int) -> None` | Adds one integer from the stream. |
| `findMedian() -> float` | Returns the median of **all** numbers added so far. |

Numbers arrive one at a time ("a stream"), and `findMedian` can be called between additions, so we must be able to answer quickly at any moment. Answers within `10^-5` of the true median are accepted.

### Example

**Example 1**

```text
Input
["MedianFinder", "addNum", "addNum", "findMedian", "addNum", "findMedian"]
[[], [1], [2], [], [3], []]
Output
[null, null, null, 1.5, null, 2.0]
```

- Create an empty `MedianFinder`.
- `addNum(1)` → numbers `[1]`.
- `addNum(2)` → numbers `[1, 2]`.
- `findMedian()` → `(1 + 2) / 2 = 1.5`.
- `addNum(3)` → numbers `[1, 2, 3]`.
- `findMedian()` → `2.0`.

### Constraints

- `-10^5 <= num <= 10^5`
- There will be at least one element in the data structure before calling `findMedian`.
- At most `5 * 10^4` calls will be made to `addNum` and `findMedian`.

### Follow-ups

1. If all integer numbers from the stream are in the range `[0, 100]`, how would you optimize your solution?
2. If 99% of all integer numbers from the stream are in the range `[0, 100]`, how would you optimize your solution?

Both are answered in Section 13 (Q2 and Q3).

---

## 3. Everyday Analogy

> **Explain it like I'm five**

Kids keep arriving at a playground, one by one, and the teacher keeps asking: *"Who is the middle-height kid right now?"*

Lining everyone up again every time is exhausting. Instead, the teacher splits the kids into **two teams**:

- **Team Short** holds the shorter half. Its **tallest** kid stands at the front.
- **Team Tall** holds the taller half. Its **shortest** kid stands at the front.

The two kids at the fronts are standing right in the middle of everyone! The teacher keeps the teams the same size (Team Short may have one extra kid). Then:

- If Team Short has one extra kid, its front kid is the middle one.
- If the teams are equal, the middle is halfway between the two front kids.

When a new kid arrives, they join a team, and if the teams become lopsided, one front kid walks over to the other team. Only the front kids ever matter.

---

## 4. Step-by-Step Logic

1. **The median depends only on the middle one or two values.** We don't need the whole list sorted — just quick access to the middle.
2. **Split the numbers into two halves:**
   - `small` — the lower half; we need its **maximum** quickly → a **max-heap**.
   - `large` — the upper half; we need its **minimum** quickly → a **min-heap**.
3. **Invariant 1 (order):** every number in `small` ≤ every number in `large`.
4. **Invariant 2 (size):** `len(small) == len(large)` or `len(small) == len(large) + 1`.
5. **Median:** if `small` is bigger, it is `max(small)`; otherwise it is `(max(small) + min(large)) / 2`.
6. **Adding a number while keeping both invariants:**
   1. Push it into `small`.
   2. Move `small`'s maximum into `large` (this guarantees the order invariant, whatever the new number was).
   3. If `large` is now bigger than `small`, move `large`'s minimum back into `small`.
7. **Python only has a min-heap** (`heapq`), so store **negated** values in `small` to make it behave as a max-heap.

---

## 5. Brute-Force Solution

### Algorithm

Keep all numbers in a **sorted list**. Insert each new number at its correct position with `bisect.insort`. The median is then read directly from the middle index (or two middle indices).

### Python code

```python
import bisect


class MedianFinder:

    def __init__(self):
        self.data = []                      # always kept sorted

    def addNum(self, num: int) -> None:
        bisect.insort(self.data, num)       # binary search + list insertion

    def findMedian(self) -> float:
        n = len(self.data)
        mid = n // 2
        if n % 2 == 1:
            return float(self.data[mid])
        return (self.data[mid - 1] + self.data[mid]) / 2
```

### Explanation

- `bisect.insort` finds the insertion point with binary search, then inserts there, so the list stays sorted.
- For odd `n` the middle element is at index `n // 2`; for even `n` the two middle elements are at `n // 2 − 1` and `n // 2`.
- `float(...)` makes the return type a float even when the median is a whole number.

### Complexity

- **`addNum`:** `O(n)` time. Finding the position is `O(log n)`, but inserting into a Python list must **shift** every later element one slot right, which is `O(n)` in the worst case (e.g. inserting at the front). Python does this shift with a fast memory move, so it is quick in practice for `5 · 10^4` calls, but it is still linear.
- **`findMedian`:** `O(1)` time (direct indexing).
- **Total over `m` additions:** `O(m²)` worst case.
- **Auxiliary space:** `O(n)` for the stored numbers.

An even simpler brute force — append to an unsorted list and `sort()` on every `findMedian` — makes `addNum` `O(1)` but each `findMedian` at least `O(n)` (and `O(n log n)` in general), which is worse when queries are frequent.

The trade-off: the sorted list is simple and fast to query, but every insertion may move many elements. Two heaps make both operations logarithmic or better.

---

## 6. Optimized Solution

### Idea — two heaps

`small` is a max-heap (negated values) holding the lower half, `large` is a min-heap holding the upper half. `small` may hold one extra element.

### Algorithm

- **`addNum(num)`**
  1. Push `-num` into `small`.
  2. Pop the largest value from `small` and push it into `large`.
  3. If `len(large) > len(small)`, pop the smallest from `large` and push it (negated) into `small`.
- **`findMedian()`**
  - If `len(small) > len(large)`: return `-small[0]`.
  - Else: return `(-small[0] + large[0]) / 2`.

### Python code (LeetCode-ready)

```python
import heapq


class MedianFinder:

    def __init__(self):
        self.small = []   # max-heap (stored as negatives): the lower half
        self.large = []   # min-heap: the upper half

    def addNum(self, num: int) -> None:
        # 1) Put the new number in the lower half
        heapq.heappush(self.small, -num)
        # 2) Move the largest of the lower half to the upper half
        heapq.heappush(self.large, -heapq.heappop(self.small))
        # 3) Keep len(small) == len(large) or len(large) + 1
        if len(self.large) > len(self.small):
            heapq.heappush(self.small, -heapq.heappop(self.large))

    def findMedian(self) -> float:
        if len(self.small) > len(self.large):
            return float(-self.small[0])
        return (-self.small[0] + self.large[0]) / 2
```

---

## 7. Line-by-Line Explanation

| Line | What it does | Why |
|---|---|---|
| `self.small = []` | Lower half, stored as negatives. | `heapq` is a min-heap; the smallest negative is the largest original value, so `-self.small[0]` is the max of the lower half. |
| `self.large = []` | Upper half, a normal min-heap. | `self.large[0]` is the smallest value of the upper half. |
| `heapq.heappush(self.small, -num)` | Adds the new number to the lower half. | A fixed first step keeps the logic uniform. |
| `heapq.heappush(self.large, -heapq.heappop(self.small))` | Moves the lower half's maximum to the upper half. | Whatever `num` was, the biggest value of the lower half now goes up, so every value in `small` ≤ every value in `large`. |
| `if len(self.large) > len(self.small):` | Checks the size invariant. | After step 2, `large` may have one too many. |
| `heapq.heappush(self.small, -heapq.heappop(self.large))` | Moves the upper half's minimum back down. | Restores `len(small) ≥ len(large)` without breaking the order (the moved value is the smallest of `large`). |
| `if len(self.small) > len(self.large):` | Odd total count. | `small` holds the extra (middle) element. |
| `return float(-self.small[0])` | Returns the middle element. | Undo the negation; return a float as the signature says. |
| `return (-self.small[0] + self.large[0]) / 2` | Even total count: average of the two middle values. | `/` is true division in Python 3, so `(1 + 2) / 2 = 1.5`. |

**Why always pass through `small` first?** If we pushed `num` directly into one heap based on a comparison, we would need extra cases. "Push to `small`, move its max to `large`, rebalance" handles every case with the same three heap operations.

---

## 8. Dry Run

**Official example:** `addNum(1)`, `addNum(2)`, `findMedian()`, `addNum(3)`, `findMedian()`

For readability, the heaps are shown as **sets of original values** (the real `small` list stores negatives in heap order).

| Call | After push to `small` | Moved to `large` | Rebalance? | `small` (lower half) | `large` (upper half) | Median |
|---|---|---|---|---|---|---|
| `addNum(1)` | {1} | 1 | `large` 1 > `small` 0 → move 1 back | {1} | {} | — |
| `addNum(2)` | {1, 2} | 2 | No (1 = 1) | {1} | {2} | — |
| `findMedian()` | — | — | — | {1} | {2} | sizes equal → `(1 + 2) / 2 = 1.5` ✅ |
| `addNum(3)` | {1, 3} | 3 | `large` 2 > `small` 1 → move min 2 back | {1, 2} | {3} | — |
| `findMedian()` | — | — | — | {1, 2} | {3} | `small` bigger → `max(small) = 2.0` ✅ |

### Second dry run — a longer stream

Add `6, 10, 2, 6, 5, 0`, calling `findMedian()` after each.

| Add | After push to `small` | Moved up | Rebalance | `small` | `large` | Median | Check (sorted list) |
|---|---|---|---|---|---|---|---|
| 6 | {6} | 6 | move 6 back | {6} | {} | 6 | `[6]` |
| 10 | {6, 10} | 10 | no | {6} | {10} | (6 + 10) / 2 = 8.0 | `[6, 10]` |
| 2 | {2, 6} | 6 | move 6 back | {2, 6} | {10} | 6 | `[2, 6, 10]` |
| 6 | {2, 6, 6} | 6 | no | {2, 6} | {6, 10} | (6 + 6) / 2 = 6.0 | `[2, 6, 6, 10]` |
| 5 | {2, 5, 6} | 6 | move 6 back | {2, 5, 6} | {6, 10} | 6 | `[2, 5, 6, 6, 10]` |
| 0 | {0, 2, 5, 6} | 6 | no | {0, 2, 5} | {6, 6, 10} | (5 + 6) / 2 = 5.5 | `[0, 2, 5, 6, 6, 10]` |

Every median matches the sorted-list check ✅.

---

## 9. Concepts, Data Structures, and Patterns

- **Binary heap (`heapq`):** `heappush` / `heappop` in `O(log n)`, peek at `heap[0]` in `O(1)`.
- **Max-heap by negation:** push `-x`, read `-heap[0]`. This works for integers of any sign.
- **Two-heaps pattern:** split data into "lower half" and "upper half" around a moving boundary. Used for running medians, sliding-window medians (LeetCode 480, with lazy deletion), and IPO-style scheduling problems (LeetCode 502).
- **Invariants:** the solution is correct because two simple rules (order and size) hold after every `addNum`.
- **Design problems:** LeetCode creates the object once and calls its methods in sequence; state lives in `self`.
- **Sorted list + `bisect`:** binary search to find positions, but list insertion still shifts elements.
- **Counting sort idea:** for small value ranges (follow-up 1), counts per value replace storing every number.
- **Related notes:**
  - Top K Frequent Elements ([074_top_k_frequent_elements.md](074_top_k_frequent_elements.md)) — size-`k` heap.
  - Merge K Sorted Lists ([../04_linked_list/024_merge_k_sorted_lists.md](../04_linked_list/024_merge_k_sorted_lists.md)) — heap of the current heads.
  - Kth Smallest Element in a BST ([../07_tree/050_kth_smallest_element_in_a_bst.md](../07_tree/050_kth_smallest_element_in_a_bst.md)) — order statistics in a tree.

---

## 10. Complexity Analysis

`n` = number of values added so far.

| Approach | `addNum` time | `findMedian` time | Auxiliary space | Explanation |
|---|---|---|---|---|
| Unsorted list, sort on query | `O(1)` amortized | `O(n log n)` | `O(n)` | Re-sorting on every query. |
| Sorted list with `bisect.insort` (brute force) | `O(n)` | `O(1)` | `O(n)` | `O(log n)` search but `O(n)` element shifting. |
| Two heaps (optimized) | `O(log n)` | `O(1)` | `O(n)` | At most three heap operations per insert; the median is read from the heap tops. |
| Counting array, values in `[0, 100]` (follow-up 1) | `O(1)` | `O(101)` = `O(1)` | `O(101)` = `O(1)` | One counter per possible value; scan the counters to find the middle. |
| Counts + outlier lists (follow-up 2) | `O(1)` for in-range values; `O(n)` worst case for an outlier (sorted-list insertion) | `O(101)` = `O(1)` (a scan of the counters plus direct indexing into the outlier lists) | `O(101 + outliers)` | Outliers are only ~1% of values; they are stored separately and rarely needed. |

Over the whole run of at most `5 · 10^4` calls, the two-heap design costs `O(m log m)` in total.

---

## 11. Edge Cases

| Case | Operations | Expected result | Why |
|---|---|---|---|
| Single number | `addNum(-100000)`, `findMedian()` | `-100000.0` | One element is its own median. |
| Two extremes | `addNum(-100000)`, `addNum(100000)`, `findMedian()` | `0.0` | `(-100000 + 100000) / 2`. |
| All equal | `addNum(5)` × 4, `findMedian()` after each | `5.0` every time | Duplicates can sit in either heap. |
| Decreasing input | `addNum(3)`, `addNum(2)`, `addNum(1)`, `findMedian()` | `2.0` | The order invariant holds regardless of arrival order. |
| Even count with a `.5` | `addNum(1)`, `addNum(2)`, `findMedian()` | `1.5` | True division, not `//`. |
| Negative even median | `addNum(-1)`, `addNum(-2)`, `findMedian()` | `-1.5` | `//` would wrongly give `-2`. |
| Two separate objects | `a.addNum(1)`, `b.addNum(100)` | `a → 1.0`, `b → 100.0` | State is stored per instance (`self.`), never in class-level lists. |

---

## 12. Common Mistakes and Debugging

1. **Using `//` for the average.** `(1 + 2) // 2 = 1`, and for negatives `(-1 + -2) // 2 = -2` (floor). Use `/`.
2. **Forgetting to negate when reading `small`.** `self.small[0]` is the *negative* of the max; return `-self.small[0]`.
3. **Breaking the order invariant.** Pushing a new number straight into `small` and only balancing sizes can leave a large value in the lower half (e.g. add 1, then 10 into `small` → median wrong). Always move `small`'s max to `large` after pushing.
4. **Letting `large` grow bigger than `small`.** Then `findMedian` on an odd count returns the wrong heap's top. Decide which heap holds the extra element and stick with it.
5. **Class-level mutable attributes.** Writing `small = []` in the class body (not in `__init__`) shares one list between all `MedianFinder` objects; LeetCode creates many objects across test cases.
6. **Sorting on every `findMedian`.** Correct but slow when queries are frequent.

**Debugging tip:** after each `addNum`, assert `len(self.small) - len(self.large) in (0, 1)` and `not self.large or -self.small[0] <= self.large[0]`. Any bug shows up as a failed invariant.

---

## 13. Practice Questions

**Q1. Starting empty, add `5, 15, 1, 3`. What are the halves and the median after each addition?**

<details><summary>Hint</summary>Push to `small`, move its max up, rebalance if `large` is bigger.</summary></details>

**Answer:**
- Add 5: `small = {5}`, `large = {}` → median `5`.
- Add 15: push → `{5, 15}`, move 15 up → `small = {5}`, `large = {15}` → median `10.0`.
- Add 1: push → `{1, 5}`, move 5 up → `large = {5, 15}` is bigger, move 5 back → `small = {1, 5}`, `large = {15}` → median `5`.
- Add 3: push → `{1, 3, 5}`, move 5 up → `small = {1, 3}`, `large = {5, 15}` → median `(3 + 5) / 2 = 4.0`.

**Q2. Follow-up 1: every number is in `[0, 100]`. Design an `O(1)`-per-operation median finder.**

<details><summary>Hint</summary>Keep 101 counters; to find the `i`-th smallest value, walk the counters adding up counts.</summary></details>

**Answer:** `addNum` increments one counter (`O(1)`); `findMedian` scans at most 101 counters (`O(101)`, a constant). Memory is constant too.

```python
import random
import statistics


class BucketMedianFinder:
    def __init__(self):
        self.counts = [0] * 101
        self.n = 0

    def addNum(self, num):
        self.counts[num] += 1
        self.n += 1

    def _kth(self, k):                  # k-th smallest, 0-indexed
        for value, c in enumerate(self.counts):
            if k < c:
                return value
            k -= c

    def findMedian(self):
        if self.n % 2 == 1:
            return float(self._kth(self.n // 2))
        return (self._kth(self.n // 2 - 1) + self._kth(self.n // 2)) / 2


bmf = BucketMedianFinder()
bmf.addNum(1); bmf.addNum(2)
assert bmf.findMedian() == 1.5
bmf.addNum(3)
assert bmf.findMedian() == 2.0

rng = random.Random(0)
bmf, seen = BucketMedianFinder(), []
for _ in range(500):
    x = rng.randint(0, 100)
    bmf.addNum(x)
    seen.append(x)
    assert abs(bmf.findMedian() - statistics.median(seen)) < 1e-9
```

**Q3. Follow-up 2: 99% of the numbers are in `[0, 100]`. How do you adapt?**

<details><summary>Hint</summary>Keep the counters for the common range and store the rare outliers separately (below 0 and above 100).</summary></details>

**Answer:** Keep the 101 counters plus two small sorted lists: `low` (values < 0) and `high` (values > 100). To find the `k`-th smallest: if `k < len(low)` it's `low[k]`; otherwise subtract `len(low)` and walk the counters; if you run past them, it's in `high`. Since outliers are about 1%, the median almost always falls inside the counters, and inserting into the small outlier lists is cheap.

```python
import bisect
import random
import statistics


class RangeMedianFinder:
    def __init__(self):
        self.counts = [0] * 101
        self.low = []        # sorted values < 0
        self.high = []       # sorted values > 100
        self.n = 0

    def addNum(self, num):
        if num < 0:
            bisect.insort(self.low, num)
        elif num > 100:
            bisect.insort(self.high, num)
        else:
            self.counts[num] += 1
        self.n += 1

    def _kth(self, k):
        if k < len(self.low):
            return self.low[k]
        k -= len(self.low)
        for value, c in enumerate(self.counts):
            if k < c:
                return value
            k -= c
        return self.high[k]

    def findMedian(self):
        if self.n % 2 == 1:
            return float(self._kth(self.n // 2))
        return (self._kth(self.n // 2 - 1) + self._kth(self.n // 2)) / 2


rng = random.Random(1)
rmf, seen = RangeMedianFinder(), []
for _ in range(1000):
    x = rng.randint(0, 100) if rng.random() < 0.99 else rng.randint(-100000, 100000)
    rmf.addNum(x)
    seen.append(x)
    assert abs(rmf.findMedian() - statistics.median(seen)) < 1e-9
```

**Q4. Why does the two-heap method need a *max*-heap for the lower half instead of a min-heap?**

<details><summary>Hint</summary>Which element of the lower half touches the middle?</summary></details>

**Answer:** The median sits at the boundary between the halves. The boundary element of the lower half is its **largest** value, and of the upper half its **smallest**. Each heap must expose exactly that boundary element at its top in `O(1)`, so the lower half needs a max-heap and the upper half a min-heap.

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** Two heaps (max-heap lower half via negation, min-heap upper half).
- **Key idea:** Push to `small`, move `small`'s max to `large`, move `large`'s min back if `large` got bigger. Median = top of `small` (odd) or average of both tops (even).
- **Time:** `addNum` `O(log n)`, `findMedian` `O(1)`.
- **Auxiliary space:** `O(n)`.
- **One-line memory hook:** *"Short team, tall team — the two captains stand in the middle."*

### Completion checklist

- [x] Problem requirements verified
- [x] Examples and constraints verified
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force solution written and tested
- [x] Optimized Python solution written and tested (`tools/tests/p075.py`, `TARGET = "MedianFinder"`)
- [x] Line-by-line explanation written
- [x] Dry run completed with a real example
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added (including both follow-ups)
- [x] Final review completed
