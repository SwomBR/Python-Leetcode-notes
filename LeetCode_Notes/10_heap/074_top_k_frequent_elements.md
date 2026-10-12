# 074. Top K Frequent Elements

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Top K Frequent Elements |
| **LeetCode number** | 347 |
| **Topic (source list)** | Heap |
| **Also uses** | Hash Table (counting), Bucket Sort, Quickselect |
| **Difficulty** | Medium |
| **LeetCode URL** | <https://leetcode.com/problems/top-k-frequent-elements/> |
| **Pattern** | Count with a hash map, then select the top `k` with a size-`k` min-heap or frequency buckets |

---

## 2. Problem Explanation

### What are we given?

- `nums` — a list of integers (values may repeat).
- `k` — how many values we want.

### What must we return?

The `k` values that appear **most often** in `nums`. The values can be returned in **any order**.

### The rules

1. We return **values**, not indices and not counts.
2. Each value appears in the answer at most once.
3. The problem guarantees that the answer is **unique**: there is never a tie at the cut-off between the `k`-th and the `(k+1)`-th most frequent value, so we never have to choose between equally frequent candidates.

### Examples

**Example 1**

```text
Input:  nums = [1,1,1,2,2,3], k = 2
Output: [1,2]
```

`1` appears 3 times, `2` appears 2 times, `3` appears once. The top two are `1` and `2`.

**Example 2**

```text
Input:  nums = [1], k = 1
Output: [1]
```

**Example 3**

```text
Input:  nums = [1,2,1,2,1,2,3,1,3,2], k = 2
Output: [1,2]
```

`1` and `2` each appear 4 times, `3` appears 2 times. (The tie between `1` and `2` is fine because both are in the answer.)

### Constraints

- `1 <= nums.length <= 10^5`
- `-10^4 <= nums[i] <= 10^4`
- `k` is in the range `[1, the number of unique elements in the array]`.
- It is guaranteed that the answer is unique.

**Follow-up:** Your algorithm's time complexity must be better than `O(n log n)`, where `n` is the array's size.

---

## 3. Everyday Analogy

> **Explain it like I'm five**

Your class votes for their favourite fruit, and the teacher wants the **two most popular** fruits.

**Step 1 — tally.** Walk past every vote and put a tally mark next to that fruit on the board. Now you know how many votes each fruit got.

**Step 2 — pick the winners.** Two fun ways:

- **The small podium (heap).** You keep a podium with only `k` spots. Each fruit tries to climb on. If the podium is overfull, the **weakest** fruit on it gets kicked off. At the end, the podium holds the `k` strongest fruits.
- **The shelves (buckets).** Build shelves numbered 1, 2, 3, … up to the number of votes. Put each fruit on the shelf equal to its vote count. Then read shelves from the top down and grab fruits until you have `k`.

---

## 4. Step-by-Step Logic

1. **We need frequencies first.** A dictionary `value -> count` built in one pass (`collections.Counter`) gives them in `O(n)`.
2. **Now it's a "top `k` by count" selection problem** over `u` distinct values (`u ≤ n`).
3. **Sorting all `u` values by count** works but costs `O(u log u)`, which can be `O(n log n)` — exactly what the follow-up asks us to beat.
4. **Size-`k` min-heap:** keep only the best `k` seen so far; the smallest of them sits on top, so it's cheap to evict. Each push/pop costs `O(log k)` → `O(n + u log k)`.
5. **Bucket sort:** a count is always between `1` and `n`. Use `n + 1` buckets indexed by count and read them from high to low → `O(n)`.
6. **Stop as soon as `k` values are collected.** The uniqueness guarantee means no tie is split at the boundary.

---

## 5. Brute-Force Solution

### Algorithm

1. For every distinct value, count its occurrences by scanning the whole list (`nums.count(value)`).
2. Sort the distinct values by count, largest first.
3. Return the first `k`.

### Python code

```python
from typing import List


class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        distinct = list(set(nums))
        counts = {value: nums.count(value) for value in distinct}   # O(n) per value
        distinct.sort(key=lambda value: counts[value], reverse=True)
        return distinct[:k]
```

### Explanation

- `set(nums)` removes duplicates, so each value is counted once.
- `nums.count(value)` scans the full list each time.
- Sorting by count (descending) puts the most frequent values first; slicing keeps `k` of them.
- Because the answer is unique, values tied at the cut-off never occur, so the slice is always correct.

### Complexity

- **Time:** `O(n · u + u log u)`, where `u` is the number of distinct values. Here `u` can reach `min(n, 20001)` (values lie in `[-10^4, 10^4]`), so the counting step can be about `10^5 × 2 × 10^4 = 2 × 10^9` operations — far too slow.
- **Auxiliary space:** `O(u)` for the distinct list and the counts.

The trade-off: very short and obviously correct, but it re-scans the whole list for every distinct value and sorts, failing both the time limit and the follow-up.

---

## 6. Optimized Solution

### Idea — count once, then keep a min-heap of size `k`

Count with a hash map in `O(n)`. Then push `(count, value)` pairs into a min-heap, popping whenever it grows beyond `k`. The heap always holds the `k` most frequent values seen so far, with the least frequent of them at the top, ready to be evicted.

### Algorithm

1. `count = Counter(nums)`.
2. `heap = []`.
3. For each `(value, freq)` in `count`: push `(freq, value)`; if `len(heap) > k`, pop the smallest.
4. Return the values left in the heap.

### Python code (LeetCode-ready)

```python
from typing import List
from collections import Counter
import heapq


class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        count = Counter(nums)                    # value -> frequency

        heap = []                                # min-heap of (frequency, value)
        for value, freq in count.items():
            heapq.heappush(heap, (freq, value))
            if len(heap) > k:
                heapq.heappop(heap)              # drop the least frequent

        return [value for freq, value in heap]
```

Python's one-liner `heapq.nlargest(k, count.keys(), key=count.get)` does the same job internally in `O(u log k)`.

### Even faster: bucket sort, `O(n)`

A frequency is between `1` and `n`, so use those frequencies as list indices.

```python
from typing import List
from collections import Counter


class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        count = Counter(nums)

        buckets = [[] for _ in range(len(nums) + 1)]   # buckets[f] = values seen f times
        for value, freq in count.items():
            buckets[freq].append(value)

        result = []
        for freq in range(len(buckets) - 1, 0, -1):    # highest frequency first
            for value in buckets[freq]:
                result.append(value)
                if len(result) == k:
                    return result
        return result
```

### Library one-liner (same complexity as the heap)

```python
from typing import List
from collections import Counter
import heapq


class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        count = Counter(nums)
        return heapq.nlargest(k, count.keys(), key=count.get)
```

---

## 7. Line-by-Line Explanation

(Min-heap version)

| Line | What it does | Why |
|---|---|---|
| `count = Counter(nums)` | Builds `value -> frequency` in one pass. | Every later step needs frequencies. |
| `heap = []` | An empty list used as a min-heap by `heapq`. | `heap[0]` is always the smallest tuple. |
| `for value, freq in count.items():` | Visits each distinct value once. | `u` iterations, not `n`. |
| `heapq.heappush(heap, (freq, value))` | Inserts the pair, ordered by frequency first. | Tuples compare element by element, so `freq` decides the order. |
| `if len(heap) > k:` | The heap has one too many candidates. | We only keep `k`. |
| `heapq.heappop(heap)` | Removes the pair with the **smallest** frequency. | It can never be in the top `k`: at least `k` values beat it. |
| `return [value for freq, value in heap]` | Extracts the values. | Any order is accepted. |

**Why a *min*-heap for the *largest* items?** We need to evict the weakest candidate quickly. A min-heap keeps the weakest at the top, so eviction is a single `heappop`. A max-heap of all `u` items would also work but costs `O(u)` memory and `O(u + k log u)` time.

(Bucket version, key lines)

| Line | What it does | Why |
|---|---|---|
| `buckets = [[] for _ in range(len(nums) + 1)]` | One bucket per possible frequency `0..n`. | No value appears more than `n` times. Use a comprehension — `[[]] * (n + 1)` would share one list. |
| `buckets[freq].append(value)` | Files each value under its frequency. | Grouping replaces sorting. |
| `for freq in range(len(buckets) - 1, 0, -1):` | Reads from the highest frequency down to 1. | The most frequent values come out first. |
| `if len(result) == k: return result` | Stops once `k` values are collected. | Uniqueness guarantees we never split a tie. |

---

## 8. Dry Run

**Input:** `nums = [1, 1, 1, 2, 2, 3]`, `k = 2`

`count = {1: 3, 2: 2, 3: 1}`

### Min-heap

| Step | Pair pushed | Heap after push (list form) | `len > k`? | Popped | Heap after |
|---|---|---|---|---|---|
| 1 | `(3, 1)` | `[(3, 1)]` | No | — | `[(3, 1)]` |
| 2 | `(2, 2)` | `[(2, 2), (3, 1)]` | No | — | `[(2, 2), (3, 1)]` |
| 3 | `(1, 3)` | `[(1, 3), (3, 1), (2, 2)]` | Yes (3 > 2) | `(1, 3)` | `[(2, 2), (3, 1)]` |

Return `[2, 1]` — the same set as `[1, 2]` ✅ (order does not matter).

### Bucket sort

`len(nums) = 6`, so buckets are indexed `0..6`:

| Frequency | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| Values | — | `[3]` | `[2]` | `[1]` | — | — | — |

Scan from 6 down: 6, 5, 4 are empty; 3 → take `1` (`result = [1]`); 2 → take `2` (`result = [1, 2]`, length = `k`) → return `[1, 2]` ✅.

### Second dry run — Example 3 (tie inside the answer)

`nums = [1,2,1,2,1,2,3,1,3,2]`, `k = 2` → `count = {1: 4, 2: 4, 3: 2}`.

Bucket 4 holds `[1, 2]`, bucket 2 holds `[3]`. Scanning from 10 down, bucket 4 gives `1` then `2` → `[1, 2]` ✅. The tie is between two values that are **both** in the answer, so it is harmless.

---

## 9. Concepts, Data Structures, and Patterns

- **Frequency counting with a hash map** (`Counter`): the first step of countless problems — see Contains Duplicate ([../01_array/003_contains_duplicate.md](../01_array/003_contains_duplicate.md)), Valid Anagram ([../06_string/034_valid_anagram.md](../06_string/034_valid_anagram.md)), Group Anagrams ([../06_string/035_group_anagrams.md](../06_string/035_group_anagrams.md)).
- **Binary heap (`heapq`):** a list arranged so `heap[0]` is the minimum; push/pop are `O(log size)`. Python only provides a min-heap; negate keys for a max-heap.
- **"Top `k`" pattern:** keep a **min-heap of size `k`** to find the `k` largest (and a max-heap of size `k` for the `k` smallest). Cost `O(m log k)` for `m` items.
- **Bucket sort:** when the keys are small integers in a known range (here `1..n`), index directly by key instead of comparing.
- **Quickselect:** average `O(u)` selection of the `k`-th largest count (see Q3) — another way to beat `O(n log n)`.
- **Related notes:**
  - Find Median from Data Stream ([075_find_median_from_data_stream.md](075_find_median_from_data_stream.md)) — two heaps.
  - Merge K Sorted Lists ([../04_linked_list/024_merge_k_sorted_lists.md](../04_linked_list/024_merge_k_sorted_lists.md)) — a heap of size `k` over list heads.
  - Kth Smallest Element in a BST ([../07_tree/050_kth_smallest_element_in_a_bst.md](../07_tree/050_kth_smallest_element_in_a_bst.md)) — another "k-th" selection.

---

## 10. Complexity Analysis

`n` = length of `nums`, `u` = number of distinct values (`u ≤ n`).

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Brute force (`count` per value + sort) | `O(n · u + u log u)` | `O(u)` | A full scan per distinct value, then a sort. |
| Counter + full sort | `O(n + u log u)` | `O(u)` | Fine in practice, but `O(n log n)` when most values are distinct — does not meet the follow-up. |
| Counter + size-`k` min-heap | `O(n + u log k)` | `O(u + k)` | Counting `O(n)`; each of `u` pushes/pops costs `O(log k)`. Better than `O(n log n)` whenever `k` is small relative to `n`; in the worst case `k = u = n` it degrades to `O(n log n)`. |
| Counter + bucket sort | `O(n)` | `O(n)` | Counting `O(n)`; `n + 1` buckets hold `u` values in total; one scan over buckets. Always better than `O(n log n)`. |
| `heapq.nlargest` | `O(n + u log k)` | `O(u + k)` | Same as the hand-written heap. |

The `O(u)` term in auxiliary space is the `Counter` itself, which every approach needs.

---

## 11. Edge Cases

| Case | Example | Expected result | Why |
|---|---|---|---|
| Single element | `nums = [1]`, `k = 1` | `[1]` | Only one value. |
| `k` equals the number of distinct values | `nums = [4, 4, 5, 5, 6]`, `k = 3` | `[4, 5, 6]` (any order) | Every distinct value is returned. |
| All elements equal | `nums = [7, 7, 7, 7, 7]`, `k = 1` | `[7]` | One distinct value. |
| Negative values | `nums = [-1, -1, 3]`, `k = 1` | `[-1]` | Values are just dictionary keys; sign does not matter. |
| Extreme values | `nums = [-10000, 10000, 10000]`, `k = 1` | `[10000]` | Count 2 beats count 1. |
| Tie inside the answer | `nums = [1,2,1,2,1,2,3,1,3,2]`, `k = 2` | `[1, 2]` | Both tied values are included. |

---

## 12. Common Mistakes and Debugging

1. **Returning counts or `(count, value)` pairs** instead of plain values.
2. **Using a max-heap of all values** when a size-`k` min-heap is enough — it works, but uses more memory and time.
3. **Popping from the wrong end.** With a min-heap of size `k`, pop when `len(heap) > k`; popping the *largest* would throw away the answer.
4. **`buckets = [[]] * (n + 1)`** creates `n + 1` references to **the same list**, so every value lands in every bucket. Use a list comprehension.
5. **Bucket list too short.** A value can appear `n` times, so you need index `n` → size `n + 1`.
6. **Comparing the answer's order in tests.** Any order is valid; compare sorted lists or sets.
7. **Forgetting to stop at `k`** in the bucket scan, returning too many values.

**Debugging tip:** print `count` first. If the counts are right, the remaining bug is in the selection step.

---

## 13. Practice Questions

**Q1. For `nums = [5, 3, 5, 2, 3, 5, 9]` and `k = 2`, what do the buckets look like and what is the answer?**

<details><summary>Hint</summary>Count first: 5 appears three times.</summary></details>

**Answer:** `count = {5: 3, 3: 2, 2: 1, 9: 1}`. Buckets (indices 0..7): bucket 1 = `[2, 9]`, bucket 2 = `[3]`, bucket 3 = `[5]`. Scanning down from 7: bucket 3 gives `5`, bucket 2 gives `3` → `[5, 3]`.

**Q2. (LeetCode 215, Kth Largest Element in an Array) Return the `k`-th largest element using a size-`k` min-heap.**

<details><summary>Hint</summary>After processing all elements, the heap holds the `k` largest; its top is the smallest of them.</summary></details>

**Answer:**

```python
import heapq


def kth_largest(nums, k):
    heap = []
    for x in nums:
        heapq.heappush(heap, x)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0]


assert kth_largest([3, 2, 1, 5, 6, 4], 2) == 5
assert kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == 4
```

Time `O(n log k)`, space `O(k)`.

**Q3. Solve Top K Frequent with quickselect (average `O(n)`).**

<details><summary>Hint</summary>Partition the distinct values by frequency so the `k` most frequent end up at the end of the list.</summary></details>

**Answer:** Quickselect places the value that would sit at position `u − k` (in ascending-frequency order) correctly; everything to its right is at least as frequent.

```python
import random
from collections import Counter


def top_k_quickselect(nums, k):
    count = Counter(nums)
    values = list(count)
    target = len(values) - k          # final index of the k-th most frequent

    lo, hi = 0, len(values) - 1
    while True:
        pivot_index = random.randint(lo, hi)
        values[pivot_index], values[hi] = values[hi], values[pivot_index]
        pivot_freq = count[values[hi]]
        store = lo
        for i in range(lo, hi):        # Lomuto partition by frequency
            if count[values[i]] < pivot_freq:
                values[store], values[i] = values[i], values[store]
                store += 1
        values[store], values[hi] = values[hi], values[store]
        if store == target:
            return values[target:]
        if store < target:
            lo = store + 1
        else:
            hi = store - 1


assert sorted(top_k_quickselect([1, 1, 1, 2, 2, 3], 2)) == [1, 2]
assert sorted(top_k_quickselect([1, 2, 1, 2, 1, 2, 3, 1, 3, 2], 2)) == [1, 2]
assert top_k_quickselect([1], 1) == [1]
```

Average `O(n)`, worst case `O(n + u²)` with consistently unlucky pivots.

**Q4. (LeetCode 692, Top K Frequent Words) Return the `k` most frequent words, sorted by frequency (high to low), breaking ties alphabetically.**

<details><summary>Hint</summary>Sort by the key `(-count, word)`.</summary></details>

**Answer:**

```python
from collections import Counter
import heapq


def top_k_words(words, k):
    count = Counter(words)
    return heapq.nsmallest(k, count, key=lambda w: (-count[w], w))


assert top_k_words(["i", "love", "leetcode", "i", "love", "coding"], 2) == ["i", "love"]
assert top_k_words(["the", "day", "is", "sunny", "the", "the", "the",
                    "sunny", "is", "is"], 4) == ["the", "is", "sunny", "day"]
```

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** Count with a hash map → select top `k` (size-`k` min-heap or frequency buckets).
- **Key idea:** Frequencies are integers in `1..n`, so bucket them by frequency and read from the top; or keep a min-heap of size `k` and evict the weakest.
- **Time:** `O(n)` (buckets) / `O(n + u log k)` (heap).
- **Auxiliary space:** `O(n)` (buckets) / `O(u + k)` (heap).
- **One-line memory hook:** *"Tally the votes, then read the shelves from the top."*

### Completion checklist

- [x] Problem requirements verified
- [x] Examples and constraints verified
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force solution written and tested
- [x] Optimized Python solution written and tested (`tools/tests/p074.py`): heap, bucket sort and `heapq.nlargest` versions
- [x] Line-by-line explanation written
- [x] Dry run completed with a real example
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
