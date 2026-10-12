# 018. Non-overlapping Intervals

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Non-overlapping Intervals |
| **LeetCode number** | 435 |
| **Topic (source list)** | Interval |
| **Also uses** | Greedy, Sorting (Dynamic Programming as a slower alternative) |
| **Difficulty** | Medium |
| **LeetCode URL** | <https://leetcode.com/problems/non-overlapping-intervals/> |
| **Pattern** | Greedy interval scheduling: sort by end, keep the earliest-finishing interval |

---

## 2. Problem Explanation

### What are we given?

`intervals` — a list of intervals `[start, end]`, in any order. Every interval has `start < end` (no zero-length intervals).

### What must we return?

The **smallest number of intervals to delete** so that the intervals that remain do not overlap each other.

### The rules

1. **Touching is allowed.** Intervals that only meet at a single point — like `[1, 2]` and `[2, 3]` — are **not** considered overlapping. (This is the opposite convention from Merge Intervals!)
2. So two intervals clash only if one starts **strictly before** the other ends: `[1, 3]` and `[2, 4]` clash; `[1, 2]` and `[2, 4]` don't.
3. Only the **count** of removals is returned, not which ones.
4. Coordinates can be negative.

### Examples

**Example 1**

```text
Input:  intervals = [[1,2],[2,3],[3,4],[1,3]]
Output: 1
```

`[1, 3]` clashes with both `[1, 2]` and `[2, 3]`. Throw it away and `[1,2]`, `[2,3]`, `[3,4]` sit end to end with no clashes. One removal is the minimum.

**Example 2**

```text
Input:  intervals = [[1,2],[1,2],[1,2]]
Output: 2
```

All three are the same interval, so they all clash with each other. At most one can stay; two must go.

**Example 3**

```text
Input:  intervals = [[1,2],[2,3]]
Output: 0
```

They only touch at the point 2, which is allowed. Nothing needs removing.

### Constraints

- `1 <= intervals.length <= 10^5`
- `intervals[i].length == 2`
- `-5 * 10^4 <= start_i < end_i <= 5 * 10^4`

**Follow-up:** none in the official statement.

---

## 3. Everyday Analogy

> **Explain it like I'm five**

You have one TV and a list of shows you'd like to watch. Each show has a start time and an end time. Shows that overlap can't both be watched. You want to watch **as many shows as possible** (then the shows you skip is as small as possible).

Here's a smart rule: **always pick the show that finishes first.**

Why? Finishing early leaves the TV free for the longest time afterwards, so it can never hurt your chances of fitting in more shows later. So:

1. Sort the shows by when they **end**.
2. Watch the first one.
3. Go down the list: if a show starts **after (or exactly when)** your last watched show ended, watch it too. Otherwise, skip it.

Count the skipped shows — that's the answer.

---

## 4. Step-by-Step Logic

1. **Flip the question.** "Fewest removals" = `n` − "most intervals we can keep with no overlaps". So find the largest set of non-overlapping intervals.
2. **Greedy choice:** among all intervals, the one with the **smallest end** can always be part of some best set.
   - Take any best set. Its earliest-ending interval `X` ends at or after our interval `E` (because `E` has the smallest end of all).
   - Swap `X` for `E`: everything else in the set started at or after `X` ended, so it also starts at or after `E` ended. The set is still valid and the same size.
3. After choosing `E`, throw away everything that clashes with it, and repeat on what's left. That's the same as walking the list **sorted by end**.
4. **Walking the sorted list:** keep `prev_end` = end of the last kept interval.
   - If `start >= prev_end` → no clash (touching allowed) → keep it, `prev_end = end`.
   - Otherwise → it clashes → remove it (count it). We don't update `prev_end`, because the kept interval ends earlier (we sorted by end), which is better for the future.
5. Start with `prev_end = -infinity`, so the first interval is always kept.

---

## 5. Brute-Force Solution

### Algorithm

Try **every subset** of intervals. For each subset, check if it's non-overlapping. The answer is `n` minus the size of the largest valid subset.

To check a subset quickly: sort the intervals by start once, and for a chosen subset make sure every chosen interval ends no later than the next chosen one starts.

### Python code

```python
from typing import List


class Solution:
    def eraseOverlapIntervals(self, intervals: List[List[int]]) -> int:
        ordered = sorted(intervals)                   # by start (then end)
        n = len(ordered)
        best_keep = 0
        for mask in range(1 << n):                    # every subset as a bitmask
            chosen = [ordered[i] for i in range(n) if mask >> i & 1]
            if all(chosen[k][1] <= chosen[k + 1][0] for k in range(len(chosen) - 1)):
                best_keep = max(best_keep, len(chosen))
        return n - best_keep
```

### Explanation

- A number `mask` from `0` to `2^n - 1` has `n` bits; bit `i` set means "keep interval `i`". So the loop visits all `2^n` subsets.
- Within a subset (kept in start order), checking **neighbours** is enough: if each chosen interval ends no later than the next one starts, then (since `start < end`) the chosen intervals march strictly to the right and no pair can overlap.
- `<=` allows touching, as the problem requires.

### Complexity

- **Time:** `O(2^n · n)` — hopeless for `n = 10^5` (and already slow around `n = 25`). It **times out**; it's only useful to check answers on tiny inputs.
- **Auxiliary space:** `O(n)` for the sorted copy and the chosen list.

A middle ground is an `O(n²)` dynamic program (like Longest Increasing Subsequence) — see Practice Q3. It is still too slow for `n = 10^5`.

---

## 6. Optimized Solution

### Idea

Greedy: sort by end, keep every interval that starts at or after the last kept end, and count the rest.

### Algorithm

1. Sort `intervals` by end.
2. `removed = 0`, `prev_end = -inf`.
3. For each `[start, end]`:
   - if `start >= prev_end`: keep it → `prev_end = end`;
   - else: `removed += 1`.
4. Return `removed`.

### Python code (LeetCode-ready)

```python
from typing import List


class Solution:
    def eraseOverlapIntervals(self, intervals: List[List[int]]) -> int:
        intervals.sort(key=lambda iv: iv[1])     # earliest end first
        removed = 0
        prev_end = float("-inf")                 # end of the last interval we kept

        for start, end in intervals:
            if start >= prev_end:                # no clash (touching is fine)
                prev_end = end                   # keep it
            else:
                removed += 1                     # clash -> drop this one

        return removed
```

---

## 7. Line-by-Line Explanation

| Line | What it does | Why |
|---|---|---|
| `intervals.sort(key=lambda iv: iv[1])` | Sorts by end time. | The greedy rule "keep whatever finishes first" needs intervals in end order. |
| `removed = 0` | Counts dropped intervals. | That's the answer. |
| `prev_end = float("-inf")` | End of the last kept interval; starts at minus infinity. | Guarantees the first interval is kept, even with negative coordinates. |
| `for start, end in intervals:` | Visits intervals in order of end. | One pass. |
| `if start >= prev_end:` | Checks whether this interval starts after the last kept one ends. | `>=` because touching (`start == prev_end`) is allowed. |
| `prev_end = end` | Keeps this interval. | It ends no earlier than the previous kept one (sorted), so it becomes the new boundary. |
| `else: removed += 1` | Drops the clashing interval. | Its end is `>= prev_end`, so keeping the earlier-ending one is never worse. |
| `return removed` | Returns the minimum number of removals. | Equal to `n` minus the size of the greedy (maximum) kept set. |

---

## 8. Dry Run

**Input:** `intervals = [[1,2],[2,3],[3,4],[1,3]]`

Sorted by end (Python's sort is stable, so `[2,3]` stays ahead of `[1,3]`, both ending at 3):
`[[1,2],[2,3],[1,3],[3,4]]`

| Step | `[start, end]` | `prev_end` before | Check `start >= prev_end` | Action | `prev_end` after | `removed` |
|---|---|---|---|---|---|---|
| 1 | `[1,2]` | -inf | `1 >= -inf` ✔ | keep | 2 | 0 |
| 2 | `[2,3]` | 2 | `2 >= 2` ✔ | keep (touching) | 3 | 0 |
| 3 | `[1,3]` | 3 | `1 >= 3` ✘ | remove | 3 | 1 |
| 4 | `[3,4]` | 3 | `3 >= 3` ✔ | keep | 4 | 1 |

**Result:** `1` ✅ (kept `[1,2]`, `[2,3]`, `[3,4]`)

**Short dry run — Example 2:** `[[1,2],[1,2],[1,2]]` → first `[1,2]` kept (`prev_end = 2`); second: `1 >= 2`? No → removed = 1; third: same → removed = 2. **Result:** `2` ✅

**What if two intervals tie on end?** It doesn't matter which one we meet first: whichever is kept sets `prev_end` to the same value, so the rest of the run is identical.

---

## 9. Concepts, Data Structures, and Patterns

- **Interval scheduling (activity selection):** the classic greedy problem "choose the maximum number of non-overlapping intervals". Sort by **end** and take greedily. This problem is its complement.
- **Exchange argument:** the proof technique in Step-by-Step Logic — show the greedy choice can be swapped into any optimal solution without making it worse.
- **Half-open thinking:** because touching is allowed here, it helps to think of intervals as `[start, end)`. Merge Intervals ([017_merge_intervals.md](017_merge_intervals.md)) and Insert Interval ([016](016_insert_interval.md)) use the closed convention instead — read each statement carefully.
- **Sort by end vs. sort by start:** sorting by start also works if, on a clash, you keep the interval with the **smaller end** (Practice Q2).
- **Bitmask enumeration:** `for mask in range(1 << n)` lists all subsets; useful for brute-force checks on tiny inputs.
- **Related problems:** Meeting Rooms ([019](019_meeting_rooms_leetcode_premium.md)) asks whether zero removals are needed; Minimum Number of Arrows to Burst Balloons (LeetCode 452) is the same greedy with closed intervals (Practice Q1).

---

## 10. Complexity Analysis

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Brute force (all subsets) | `O(2^n · n)` | `O(n)` | `2^n` subsets, each checked in `O(n)`. |
| DP (LIS-style, Practice Q3) | `O(n²)` | `O(n)` | For each interval, look at every earlier-ending one. |
| Greedy, sort by end (optimized) | `O(n log n)` | `O(n)` | Sorting dominates; the sweep is `O(n)` with two variables. The `O(n)` space is Python's Timsort buffer in the worst case — our own code uses `O(1)`. |

---

## 11. Edge Cases

| Case | Input | Expected result | Why |
|---|---|---|---|
| Single interval | `[[1,5]]` | `0` | Nothing to clash with. |
| All identical | `[[1,2],[1,2],[1,2]]` | `2` | Only one copy can stay. |
| Touching chain | `[[1,2],[2,3],[3,4],[4,5]]` | `0` | Touching is allowed. |
| One long interval covers short ones | `[[1,10],[2,3],[4,5]]` | `1` | Drop `[1,10]`, keep two short ones. |
| Negative coordinates | `[[-3,-1],[-2,0]]` | `1` | They overlap on `(-2, -1)`. |
| Mixed | `[[1,100],[11,22],[1,11],[2,12]]` | `2` | Keep `[1,11]` and `[11,22]`. |

---

## 12. Common Mistakes and Debugging

1. **Using `>` instead of `>=`.** Then `[1,2]` and `[2,3]` count as a clash and Example 3 returns 1 instead of 0.
2. **Sorting by start and always keeping the first interval.** For `[[1,10],[2,3],[4,5]]`, keeping `[1,10]` forces two removals; the right answer is 1. If you sort by start, on a clash you must keep the one with the smaller end.
3. **Initializing `prev_end` to 0.** Coordinates can be negative (`-5 * 10^4`), so an interval like `[-3,-1]` would wrongly look like a clash. Use `float("-inf")` (or the first interval's end).
4. **Updating `prev_end` when removing.** The removed interval is gone; `prev_end` must stay the end of the last **kept** interval.
5. **Confusing this with Merge Intervals.** Here touching is *allowed*; in Merge Intervals touching *merges*.

**Debugging tip:** also collect the kept intervals in a list and print it; check by eye that each one starts at or after the previous one ends.

---

## 13. Practice Questions

**Q1. "Minimum Number of Arrows to Burst Balloons" (LeetCode 452): each balloon spans `[x_start, x_end]`; an arrow shot at `x` bursts every balloon with `x_start <= x <= x_end`. Find the minimum number of arrows.**

<details><summary>Hint</summary>Same greedy: sort by end, shoot at the end of the first unburst balloon. Here touching balloons **can** share an arrow, so a new arrow is needed only when `start > arrow_x`.</summary></details>

**Answer:**

```python
def find_min_arrow_shots(points):
    points = sorted(points, key=lambda p: p[1])
    arrows = 0
    arrow_x = float("-inf")
    for start, end in points:
        if start > arrow_x:          # this balloon isn't hit by the last arrow
            arrows += 1
            arrow_x = end            # shoot as far right as possible
    return arrows


assert find_min_arrow_shots([[10, 16], [2, 8], [1, 6], [7, 12]]) == 2
assert find_min_arrow_shots([[1, 2], [3, 4], [5, 6], [7, 8]]) == 4
assert find_min_arrow_shots([[1, 2], [2, 3], [3, 4], [4, 5]]) == 2
```

**Q2. Solve the original problem by sorting by start instead of by end.**

<details><summary>Hint</summary>When the current interval clashes with the last kept one, remove the one that ends later — i.e. keep `prev_end = min(prev_end, end)`.</summary></details>

**Answer:**

```python
def erase_overlap_sort_by_start(intervals):
    intervals = sorted(intervals)
    removed = 0
    prev_end = float("-inf")
    for start, end in intervals:
        if start >= prev_end:
            prev_end = end
        else:
            removed += 1
            prev_end = min(prev_end, end)   # keep whichever ends first
    return removed


assert erase_overlap_sort_by_start([[1, 2], [2, 3], [3, 4], [1, 3]]) == 1
assert erase_overlap_sort_by_start([[1, 2], [1, 2], [1, 2]]) == 2
assert erase_overlap_sort_by_start([[1, 10], [2, 3], [4, 5]]) == 1
```

**Q3. Write the `O(n²)` dynamic-programming version: `best[i]` = most intervals you can keep if interval `i` (in end order) is the last kept one.**

<details><summary>Hint</summary>`best[i] = 1 + max(best[j])` over earlier `j` with `end_j <= start_i` (or `1` if none). Answer: `n - max(best)`.</summary></details>

**Answer:**

```python
def erase_overlap_dp(intervals):
    ordered = sorted(intervals, key=lambda iv: iv[1])
    n = len(ordered)
    best = [1] * n
    for i in range(n):
        for j in range(i):
            if ordered[j][1] <= ordered[i][0]:
                best[i] = max(best[i], best[j] + 1)
    return n - max(best)


assert erase_overlap_dp([[1, 2], [2, 3], [3, 4], [1, 3]]) == 1
assert erase_overlap_dp([[1, 2], [1, 2], [1, 2]]) == 2
assert erase_overlap_dp([[1, 2], [2, 3]]) == 0
```

This is correct but `O(n²)` — about `10^10` steps for `n = 10^5`, so it times out. The greedy replaces the inner loop with a single variable.

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** Greedy interval scheduling.
- **Key idea:** sort by end; keep an interval if `start >= prev_end` (then `prev_end = end`), otherwise count a removal.
- **Time:** `O(n log n)`.
- **Auxiliary space:** `O(1)` beyond sorting (`O(n)` worst case for Python's sort).
- **One-line memory hook:** *"Always watch the show that ends first."*

### Completion checklist

- [x] Problem requirements verified
- [x] Examples and constraints verified
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force solution written and tested
- [x] Optimized Python solution written and tested (`tools/tests/p018.py`)
- [x] Line-by-line explanation written
- [x] Dry run completed with a real example
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
