# 070. Longest Consecutive Sequence

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Longest Consecutive Sequence |
| **LeetCode number** | 128 |
| **Topic (source list)** | Graph |
| **Also uses** | Hash Set, Array, Union-Find |
| **Difficulty** | Medium |
| **LeetCode URL** | <https://leetcode.com/problems/longest-consecutive-sequence/> |
| **Pattern** | Hash set + "only start counting at the beginning of a run" |

---

## 2. Problem Explanation

### What are we given?

`nums` — an **unsorted** list of integers. It may contain duplicates, negatives, and may even be empty.

### What must we return?

The length of the longest run of **consecutive integer values** (`x, x+1, x+2, ...`) that can be built from the numbers in `nums`.

- The numbers do **not** need to be next to each other in the list — position doesn't matter, only which values are present.
- Duplicates don't help: `[1, 2, 2, 3]` still gives the run `1, 2, 3` of length 3.
- An empty list has answer `0`.

### The rule that makes it hard

The algorithm must run in **`O(n)` time**. Sorting takes `O(n log n)`, so a sorting solution, while accepted in practice, does not meet the stated requirement.

### Why is this in the Graph section?

Picture every distinct value as a **node**, and draw an **edge** between `x` and `x + 1` whenever both are present. The graph breaks into simple chains (paths), and the answer is the **size of the largest connected component**:

```text
nums = [100, 4, 200, 1, 3, 2]

   1 — 2 — 3 — 4        100        200
   (component of size 4) (size 1)  (size 1)
```

The hash-set solution below walks each chain once from its left end; a Union-Find solution (Q3) merges neighbouring values into components. For the general graph vocabulary see [066_clone_graph.md](066_clone_graph.md).

### Examples

**Example 1**

```text
Input:  nums = [100,4,200,1,3,2]
Output: 4
```

The longest run is `1, 2, 3, 4`.

**Example 2**

```text
Input:  nums = [0,3,7,2,5,8,4,6,0,1]
Output: 9
```

The values `0` through `8` are all present (0 appears twice), giving a run of length 9.

**Example 3**

```text
Input:  nums = [1,0,1,2]
Output: 3
```

The run is `0, 1, 2`; the extra `1` does not add anything.

### Constraints

- `0 <= nums.length <= 10^5`
- `-10^9 <= nums[i] <= 10^9`

The `O(n)` time requirement is part of the statement itself (there is no separate follow-up).

---

## 3. Everyday Analogy

> **Explain it like I'm five**

You have a bag of numbered tickets, all mixed up. You want the longest "staircase" of tickets: 1, 2, 3, 4, …

First, spread the tickets on a table so you can instantly see whether any ticket is there (that's the **set**).

Now, pick up a ticket, say **3**. Before counting, ask: *"Is there a 2?"* If yes, then 3 is **not the bottom step** — someone else's staircase will include it, so skip it. Only when there is **no smaller neighbour** (like ticket **1**, because there's no 0) do you start climbing: is there a 2? yes. A 3? yes. A 4? yes. A 5? no. Staircase length 4.

Because you only climb from the bottom step, every step of every staircase gets climbed just once.

---

## 4. Step-by-Step Logic

1. **We need fast "is value `v` present?" questions.** Put all numbers in a hash set: membership checks are `O(1)` on average, and duplicates disappear automatically.
2. **A run has a unique starting value** `x`: the one where `x - 1` is **not** in the set.
3. **Only start counting at a start.** For a start `x`, count `x, x+1, x+2, ...` while they are in the set.
4. **Skip non-starts.** If `x - 1` is in the set, `x` belongs to a longer run counted from further left — counting from `x` would only repeat work.
5. **Track the best length.** Return 0 if there are no numbers.
6. **Why `O(n)`:** every distinct value is visited by the outer loop once and by an inner "climb" at most once (only the climb from its own run's start passes over it).

---

## 5. Brute-Force Solution

### Algorithm (truly simple)

For every number `x` in `nums`, count upward: is `x + 1` in the list? `x + 2`? … Keep the longest count. Membership is checked directly in the **list**, which scans it each time.

### Python code

```python
from typing import List


class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        best = 0
        for num in nums:
            length = 1
            current = num
            while current + 1 in nums:      # list membership: O(n) scan
                current += 1
                length += 1
            best = max(best, length)
        return best
```

### Explanation

- Every number is tried as a possible start, so the true longest run is always found.
- An empty list skips the loop and returns `0`.
- Duplicates are harmless; they just repeat work.

### Complexity

- **Time:** `O(n³)` in the worst case. For `nums = [0, 1, ..., n-1]`, starting from value `v` climbs `n - 1 - v` steps, each `in nums` check scans up to `n` elements: about `n²/2` checks × `n` per check. At `n = 10^5` that is far beyond any time limit.
- **Auxiliary space:** `O(1)`.

### Middle step 1 — same idea with a set: `O(n²)`

Changing `in nums` to `in num_set` (where `num_set = set(nums)`) makes each check `O(1)` on average, so the worst case drops to `O(n²)` — but climbing from every number, including the middle of runs, still repeats work. The optimized solution fixes exactly that.

### Middle step 2 — sorting: `O(n log n)`

Sort, then walk once: equal neighbours are skipped, a `+1` step extends the current run, anything else restarts it. This is a perfectly good, simple solution — it is just not the required `O(n)`.

```python
from typing import List


class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        if not nums:
            return 0
        nums = sorted(nums)
        best = current = 1
        for i in range(1, len(nums)):
            if nums[i] == nums[i - 1]:        # duplicate: run neither grows nor breaks
                continue
            if nums[i] == nums[i - 1] + 1:    # next consecutive value
                current += 1
            else:                             # gap: start a new run
                current = 1
            best = max(best, current)
        return best
```

- **Time:** `O(n log n)` for sorting, then `O(n)` for the walk.
- **Auxiliary space:** `O(n)` — `sorted` makes a new list (Python's Timsort may also use up to `O(n)` temporary memory).

---

## 6. Optimized Solution

### Idea

Hash set + start-of-sequence check: only numbers with no left neighbour (`num - 1` absent) start a climb.

### Algorithm

1. `num_set = set(nums)`.
2. `best = 0`.
3. For each `num` in `num_set`:
   1. If `num - 1` is in the set, skip it.
   2. Otherwise climb: `length = 1`; while `num + length` is in the set, `length += 1`.
   3. `best = max(best, length)`.
4. Return `best`.

### Python code (LeetCode-ready)

```python
from typing import List


class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        num_set = set(nums)
        best = 0

        for num in num_set:                  # iterate the SET: each value once
            if num - 1 in num_set:           # not the start of a run
                continue
            length = 1
            while num + length in num_set:   # climb to the end of this run
                length += 1
            best = max(best, length)

        return best
```

---

## 7. Line-by-Line Explanation

| Line | What it does | Why |
|---|---|---|
| `num_set = set(nums)` | Builds a hash set of the values. | `O(1)` average membership; removes duplicates. |
| `best = 0` | Longest run found so far. | Correct answer for an empty list. |
| `for num in num_set:` | Loops over **distinct** values. | Looping over `nums` would repeat a climb for every duplicate start (see mistake 3). |
| `if num - 1 in num_set: continue` | Skips values that are not the start of a run. | Their run is counted from its real start; this is what makes the total work linear. |
| `length = 1` | The run contains `num` itself. | |
| `while num + length in num_set:` | Checks the next value up. | `num + length` is the next value we need. |
| `length += 1` | Extends the run. | |
| `best = max(best, length)` | Updates the answer. | |
| `return best` | Returns the longest run. | |

**Why is the nested loop still `O(n)`?** The `while` loop's body runs once for each value that is *not* a start, and only from the start of that value's own run. Runs don't overlap, so across the whole program the body runs at most `(number of distinct values) - (number of runs)` times. Add the outer loop's `n` iterations and the total is `O(n)`.

---

## 8. Dry Run

**Input:** `nums = [100, 4, 200, 1, 3, 2]` (Example 1) → `num_set = {100, 4, 200, 1, 3, 2}`.

A set's iteration order is not guaranteed, but every decision below depends only on the set's contents, so the result is the same in any order. Here we follow the order of `nums`:

| `num` | `num - 1` in set? | Start? | Climb checks | `length` | `best` |
|---|---|---|---|---|---|
| 100 | 99: No | Yes | 101? No | 1 | 1 |
| 4 | 3: **Yes** | No — skip | — | — | 1 |
| 200 | 199: No | Yes | 201? No | 1 | 1 |
| 1 | 0: No | Yes | 2? Yes → 3? Yes → 4? Yes → 5? No | 4 | **4** |
| 3 | 2: **Yes** | No — skip | — | — | 4 |
| 2 | 1: **Yes** | No — skip | — | — | 4 |

**Result:** `4` ✅. Total climb steps: 3 (for 2, 3, 4) — each non-start value was climbed over exactly once.

**Second dry run:** `nums = [0, 3, 7, 2, 5, 8, 4, 6, 0, 1]` (Example 2) → `num_set = {0, 1, 2, 3, 4, 5, 6, 7, 8}`. Only `0` is a start (`-1` is absent); every other value has its left neighbour. The climb from 0 checks 1, 2, …, 8 (all present) and stops at 9 → `length = 9` ✅.

**Third:** `nums = [1, 0, 1, 2]` (Example 3) → `{0, 1, 2}`; start `0` climbs to 2 → `3` ✅.

---

## 9. Concepts, Data Structures, and Patterns

- **Hash set:** average `O(1)` `in` checks; also deduplicates.
- **"Start of sequence" trick:** do the expensive work only from a canonical starting point (`x - 1` absent) so each element is processed once. The same idea of "only count from a unique representative" appears in Number of Islands (each island counted at its first cell).
- **Amortized analysis:** a nested loop can still be linear when the inner loop's total work over the whole run is bounded by `n`.
- **Graph view / Union-Find:** values are nodes, `x — x+1` are edges, and the answer is the largest connected component. Union-Find with component sizes solves it in near-linear time (Q3).
- **Sorting as a baseline:** `O(n log n)` and very easy — a good fallback when `O(n)` isn't required.
- **Related problems in this project:**
  - Contains Duplicate — the basic set-membership pattern: [../01_array/003_contains_duplicate.md](../01_array/003_contains_duplicate.md)
  - Two Sum — hash lookups instead of scanning: [../01_array/001_two_sum.md](../01_array/001_two_sum.md)
  - Number of Islands — counting/measuring connected components: [069_number_of_islands.md](069_number_of_islands.md)
  - Number of Connected Components in an Undirected Graph — Union-Find on an edge list: [073_number_of_connected_components_in_an_undirected_graph_leetcode_premium.md](073_number_of_connected_components_in_an_undirected_graph_leetcode_premium.md)

---

## 10. Complexity Analysis

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Brute force (list membership) | `O(n³)` | `O(1)` | Up to `n` starts × up to `n` climb steps × `O(n)` per list scan. |
| Brute force with a set | `O(n²)` average | `O(n)` | Same climbs, but each check is `O(1)`; climbs from the middle of runs repeat work. |
| Sorting | `O(n log n)` | `O(n)` | Sorting dominates; the walk is `O(n)`. |
| Hash set + start check (optimized) | `O(n)` average | `O(n)` | Building the set is `O(n)`; the outer loop is `O(n)`; all climbs together take `O(n)`. |
| Union-Find (Q3) | `O(n · α(n))` average | `O(n)` | Up to `n` unions with path compression + union by size. |

"Average" refers to hash-table operations, which are `O(1)` on average.

---

## 11. Edge Cases

| Case | Input | Expected | Why |
|---|---|---|---|
| Empty list | `[]` | `0` | No numbers, no run (`best` starts at 0). |
| Single element | `[5]` | `1` | A run of one. |
| All duplicates | `[7, 7, 7]` | `1` | The set is `{7}`. |
| Duplicates inside a run | `[1, 0, 1, 2]` | `3` | Example 3. |
| Negative numbers | `[-1, -2, -3, 10]` | `3` | `-3, -2, -1`; consecutive works the same below zero. |
| Extreme values | `[10^9, -10^9, 10^9 - 1]` | `2` | `999999999, 1000000000`; Python ints don't overflow. |
| Whole list is one run | `[0,3,7,2,5,8,4,6,0,1]` | `9` | Example 2. |

All of these and 400 random lists (compared with an independent sort-based reference) are in `tools/tests/p070.py`.

---

## 12. Common Mistakes and Debugging

1. **Climbing from every number** (no `num - 1` check). Correct, but `O(n²)` — it fails the `O(n)` requirement and can time out.
2. **Using the list for membership** (`x in nums`) — each check is `O(n)`.
3. **Looping over `nums` instead of `num_set`.** If a run's start value appears many times (e.g. fifty thousand copies of `1` followed by `2, 3, …`), the climb is repeated for each copy, which is `O(n²)` again. Looping over the set visits each value once.
4. **Returning 1 for an empty list.** Start `best` at 0 (or handle `[]` explicitly, as the sorting version does).
5. **Sorting version: treating duplicates as a gap.** `[1, 2, 2, 3]` must give 3; skip equal neighbours instead of resetting the run.
6. **Thinking order in the input matters.** It doesn't — only which values exist.

**Debugging tip:** print each value the loop treats as a start and the length it climbs to. There should be exactly one start per run, and the lengths should add up to the number of distinct values.

---

## 13. Practice Questions

**Q1. For `nums = [9, 1, 4, 7, 3, -1, 0, 5, 8, -1, 6]`, which values are starts and what is the answer?**

<details><summary>Hint</summary>Write down the distinct values in sorted order first and look for gaps.</summary></details>

**Answer:** Distinct values: `-1, 0, 1, 3, 4, 5, 6, 7, 8, 9`. Starts (left neighbour missing): `-1` (no `-2`) and `3` (no `2`). Runs: `-1, 0, 1` (length 3) and `3, 4, 5, 6, 7, 8, 9` (length 7). **Answer: 7.**

**Q2. Return the longest run itself (the smallest-starting one if there is a tie).**

<details><summary>Hint</summary>Remember the start value when you update `best`.</summary></details>

**Answer:**

```python
def longest_run(nums):
    num_set = set(nums)
    best_len, best_start = 0, None
    for num in num_set:
        if num - 1 in num_set:
            continue
        length = 1
        while num + length in num_set:
            length += 1
        if length > best_len or (length == best_len and num < best_start):
            best_len, best_start = length, num
    if best_start is None:
        return []
    return list(range(best_start, best_start + best_len))


assert longest_run([100, 4, 200, 1, 3, 2]) == [1, 2, 3, 4]
assert longest_run([]) == []
assert longest_run([5, 1]) == [1]          # tie of length 1: smallest start wins
```

**Q3. Solve it with Union-Find (the graph view).**

<details><summary>Hint</summary>Make each distinct value a node; union `x` with `x + 1` when both exist; track component sizes.</summary></details>

**Answer:**

```python
def longest_consecutive_union_find(nums):
    parent = {x: x for x in nums}         # duplicates collapse into one key
    size = {x: 1 for x in parent}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra == rb:
            return
        if size[ra] < size[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        size[ra] += size[rb]

    for x in parent:
        if x + 1 in parent:
            union(x, x + 1)
    return max((size[find(x)] for x in parent), default=0)


assert longest_consecutive_union_find([100, 4, 200, 1, 3, 2]) == 4
assert longest_consecutive_union_find([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]) == 9
assert longest_consecutive_union_find([]) == 0
```

**Q4. Explain in one or two sentences why the optimized solution is `O(n)` even though it has a `while` loop inside a `for` loop.**

<details><summary>Hint</summary>Count how many times, over the whole program, the `while` body can run for a single value.</summary></details>

**Answer:** A value is passed over by a `while` climb only from the start of its own run, and every run is climbed exactly once, so the `while` body runs at most once per distinct value in total. That adds `O(n)` to the `O(n)` outer loop, giving `O(n)` overall.

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** Hash set + start-of-sequence check.
- **Key idea:** Put the values in a set. Only when `x - 1` is missing is `x` the start of a run; climb `x+1, x+2, …` from there. Loop over the set, not the list.
- **Time:** `O(n)` average.
- **Auxiliary space:** `O(n)`.
- **Graph view:** largest connected component of the "x — x+1" graph (Union-Find works too).
- **One-line memory hook:** *"Only climb the staircase from the bottom step."*

### Completion checklist

- [x] Problem requirements verified against the official statement
- [x] Examples and constraints verified
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force (`O(n³)`) solution written and tested, with set and sorting middle steps
- [x] Optimized Python solution written and tested (`tools/tests/p070.py`)
- [x] Line-by-line explanation written
- [x] Dry run completed with Example 1 (plus Examples 2 and 3)
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
