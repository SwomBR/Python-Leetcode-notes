# 017. Merge Intervals

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Merge Intervals |
| **LeetCode number** | 56 |
| **Topic (source list)** | Interval |
| **Also uses** | Array, Sorting |
| **Difficulty** | Medium |
| **LeetCode URL** | <https://leetcode.com/problems/merge-intervals/> |
| **Pattern** | Sort by start, then sweep and merge into the last interval |

---

## 2. Problem Explanation

### What are we given?

`intervals` — a list of intervals, each written as `[start, end]`. They are in **no particular order**, and some of them may overlap.

### What must we return?

A list of **non-overlapping** intervals that covers **exactly the same points** as the input. Every group of overlapping intervals is squashed into one interval stretching from the group's smallest start to its largest end.

### The rules

1. **Touching counts as overlapping.** `[1, 4]` and `[4, 5]` share the point 4, so they become `[1, 5]`.
2. `[1, 2]` and `[3, 4]` share no point, so they stay separate.
3. The input may be unsorted (Example 3 has `[4,7]` before `[1,4]`).
4. An interval may be a single point, like `[3, 3]`.

### Examples

**Example 1**

```text
Input:  intervals = [[1,3],[2,6],[8,10],[15,18]]
Output: [[1,6],[8,10],[15,18]]
```

`[1, 3]` and `[2, 6]` overlap on 2..3, so together they cover 1..6. `[8, 10]` and `[15, 18]` touch nothing else.

**Example 2**

```text
Input:  intervals = [[1,4],[4,5]]
Output: [[1,5]]
```

They meet at the point 4, which counts as overlapping, so they join into `[1, 5]`.

**Example 3**

```text
Input:  intervals = [[4,7],[1,4]]
Output: [[1,7]]
```

Same idea as Example 2, but the input is out of order — a reminder that we must sort (or otherwise handle any order).

### Constraints

- `1 <= intervals.length <= 10^4`
- `intervals[i].length == 2`
- `0 <= start_i <= end_i <= 10^4`

**Follow-up:** none in the official statement.

---

## 3. Everyday Analogy

> **Explain it like I'm five**

You have a pile of paper strips, each one painted on a ruler from some start mark to some end mark. You want to know: *"Which stretches of the ruler are painted?"*

If you grab the strips in random order it's confusing. So first you **line them up by where they start**, leftmost first.

Now take strips one by one:

- If the next strip **starts on or before the end** of the strip you're holding, it overlaps — tape it on. Your taped piece now reaches as far as whichever of the two goes further right.
- If it starts **after** your piece ends, there's a gap. Put your piece down as finished and pick up the new strip.

When you run out of strips, the pieces you put down are the answer.

---

## 4. Step-by-Step Logic

1. **Why sort?** In an unsorted list, two intervals that overlap may be far apart. After sorting by start, any interval that overlaps the "current group" must come right after it — so we only ever need to compare with the **last merged interval**.
2. **Sort by start.**
3. **Walk through the sorted intervals,** keeping a list `merged`.
4. For each `[start, end]`:
   - If `merged` is empty, or `start > merged[-1].end`, there's a gap → start a new group: append `[start, end]`.
   - Otherwise (`start <= merged[-1].end`) it overlaps → extend: `merged[-1].end = max(merged[-1].end, end)`.
5. **Why `max`?** The new interval might be completely inside the last one (e.g. `[1,10]` then `[2,3]`); its end is smaller and must not shrink the group.
6. **Why don't we need to update the start?** Sorting guarantees `start >= merged[-1].start`, so the group's start never moves left.
7. Return `merged`.

---

## 5. Brute-Force Solution

### Algorithm

Without sorting, repeatedly look for **any** two intervals that overlap and replace them with their union. Stop when a full scan finds no overlapping pair. Sort the final list so the output order is tidy.

### Python code

```python
from typing import List


class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        result = [list(iv) for iv in intervals]
        changed = True
        while changed:
            changed = False
            for i in range(len(result)):
                for j in range(i + 1, len(result)):
                    a, b = result[i], result[j]
                    if a[0] <= b[1] and b[0] <= a[1]:          # share a point
                        result[i] = [min(a[0], b[0]), max(a[1], b[1])]
                        result.pop(j)
                        changed = True
                        break
                if changed:
                    break                                      # restart the scan
        result.sort()
        return result
```

### Explanation

- `a[0] <= b[1] and b[0] <= a[1]` is the general overlap test for closed intervals: each one must start no later than the other ends.
- Every successful merge reduces the number of intervals by one, so the `while` loop runs at most `n` times and must stop.
- Replacing two **overlapping** intervals by `[min start, max end]` covers exactly the same points as the two pieces did (because they overlap, there is no gap in between). So when no overlapping pair is left, the list is disjoint and covers exactly the original points.

### Complexity

- **Time:** `O(n³)` in the worst case — up to `n - 1` merges, and each search for an overlapping pair can cost `O(n²)`. For `n = 10^4` that's about `10^12` steps, which **times out**.
- **Auxiliary space:** `O(n)` for the copied list.

---

## 6. Optimized Solution

### Idea

Sort by start once, then a single sweep where each interval is either merged into the last group or starts a new group.

### Algorithm

1. Sort `intervals` by start.
2. `merged = []`.
3. For each `[start, end]`:
   - if `merged` is non-empty and `start <= merged[-1][1]`: `merged[-1][1] = max(merged[-1][1], end)`;
   - else: append `[start, end]`.
4. Return `merged`.

### Python code (LeetCode-ready)

```python
from typing import List


class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        intervals.sort(key=lambda iv: iv[0])        # sort by start
        merged = []

        for start, end in intervals:
            if merged and start <= merged[-1][1]:   # overlaps (or touches) the last group
                merged[-1][1] = max(merged[-1][1], end)
            else:                                   # gap -> new group
                merged.append([start, end])

        return merged
```

> `intervals.sort(...)` reorders the caller's list. That's accepted on LeetCode; use `sorted(intervals, ...)` if you must leave the input untouched. We append **new** lists `[start, end]`, so updating `merged[-1][1]` never edits an input interval.

---

## 7. Line-by-Line Explanation

| Line | What it does | Why |
|---|---|---|
| `intervals.sort(key=lambda iv: iv[0])` | Orders intervals by their start. | Overlapping intervals become neighbours, so we only compare with the last group. |
| `merged = []` | Holds the finished (and the currently growing) groups. | The last element is the group we may still extend. |
| `for start, end in intervals:` | Visits intervals left to right, unpacking each pair. | Readable names instead of `iv[0]`, `iv[1]`. |
| `if merged and start <= merged[-1][1]:` | Checks for overlap with the last group. | `merged` must be non-empty before we look at `merged[-1]`. `<=` because touching intervals merge. |
| `merged[-1][1] = max(merged[-1][1], end)` | Extends the group's end if the new interval reaches further. | `max` protects against intervals nested inside the group. |
| `else: merged.append([start, end])` | Starts a new group. | There's a gap: `start > merged[-1][1]`. Because the list is sorted, no later interval can reach back into an earlier group either. |
| `return merged` | Returns the groups. | They are sorted and disjoint. |

---

## 8. Dry Run

**Input:** `intervals = [[1,3],[2,6],[8,10],[15,18]]`

After sorting by start: `[[1,3],[2,6],[8,10],[15,18]]` (already sorted).

| Step | `[start, end]` | `merged[-1]` before | Check `start <= merged[-1][1]` | Action | `merged` after |
|---|---|---|---|---|---|
| 1 | `[1,3]` | — (empty) | — | append | `[[1,3]]` |
| 2 | `[2,6]` | `[1,3]` | `2 <= 3` ✔ | end = `max(3, 6) = 6` | `[[1,6]]` |
| 3 | `[8,10]` | `[1,6]` | `8 <= 6` ✘ | append | `[[1,6],[8,10]]` |
| 4 | `[15,18]` | `[8,10]` | `15 <= 10` ✘ | append | `[[1,6],[8,10],[15,18]]` |

**Result:** `[[1,6],[8,10],[15,18]]` ✅

**Short dry run — Example 3:** `[[4,7],[1,4]]`

- Sort → `[[1,4],[4,7]]`.
- `[1,4]` → append → `[[1,4]]`.
- `[4,7]` → `4 <= 4` ✔ → end = `max(4, 7) = 7` → `[[1,7]]`.

**Result:** `[[1,7]]` ✅ (without sorting, `[4,7]` would be processed first and `[1,4]` would start a wrong second group.)

---

## 9. Concepts, Data Structures, and Patterns

- **Sorting as preprocessing:** sorting by start turns a "compare everything with everything" problem into "compare with the previous one". This is the most common first move in interval problems.
- **Closed-interval overlap test:** `[a, b]` and `[c, d]` overlap ⇔ `a <= d and c <= b`. After sorting (`a <= c`), it simplifies to `c <= b`.
- **Greedy sweep / "last group" pattern:** keep only the group that can still grow at the end of the result list.
- **`sort(key=...)` and lambdas:** `key=lambda iv: iv[0]` tells Python which value to sort by. (Plain `intervals.sort()` also works, because lists compare element by element.)
- **In-place vs. copy:** `list.sort()` changes the list; `sorted()` makes a new one.
- **Related problems:** Insert Interval ([016_insert_interval.md](016_insert_interval.md)) is this algorithm when only one interval is out of place; Non-overlapping Intervals ([018](018_non_overlapping_intervals.md)) sorts intervals too, but by end; Meeting Rooms ([019](019_meeting_rooms_leetcode_premium.md)) uses the same "sort, then compare neighbours" check.

---

## 10. Complexity Analysis

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Brute force (merge any overlapping pair, repeat) | `O(n³)` | `O(n)` | Up to `n - 1` merges, each found by an `O(n²)` pair scan; the copy uses `O(n)`. |
| Sort + sweep (optimized) | `O(n log n)` | `O(n)` | Sorting costs `O(n log n)`; the sweep is `O(n)`. Python's Timsort may use up to `O(n)` temporary memory. The `merged` output is not counted. |

Sorting is the bottleneck. (Because coordinates here are at most `10^4`, a counting/bucket approach over the coordinate range could avoid comparison sorting, but sort + sweep is the standard, expected answer.)

---

## 11. Edge Cases

| Case | Input | Expected result | Why |
|---|---|---|---|
| Single interval | `[[1,4]]` | `[[1,4]]` | Nothing to merge. |
| Nested interval | `[[1,10],[2,3]]` | `[[1,10]]` | `max` keeps the larger end. |
| Duplicates / single points | `[[1,1],[1,1]]` | `[[1,1]]` | Same point overlaps itself. |
| Separate points | `[[0,0],[1,1]]` | `[[0,0],[1,1]]` | No shared point between 0 and 1. |
| Chain of touching intervals | `[[1,2],[2,3],[3,4]]` | `[[1,4]]` | Each one touches the next. |
| Gap of one | `[[1,2],[3,4]]` | `[[1,2],[3,4]]` | 2 and 3 are different points. |
| Big interval last in input | `[[2,3],[4,5],[6,7],[8,9],[1,10]]` | `[[1,10]]` | Sorting brings `[1,10]` to the front. |

---

## 12. Common Mistakes and Debugging

1. **Forgetting to sort.** Example 3 then gives `[[4,7],[1,4]]` (or worse). Always sort by start first.
2. **Using `<` instead of `<=`.** `[[1,4],[4,5]]` would stay as two intervals, but touching counts as overlap here.
3. **Overwriting the end instead of taking `max`.** `merged[-1][1] = end` turns `[[1,10],[2,3]]` into `[[1,3]]`.
4. **Appending the input list object itself** (`merged.append(interval)`) and then editing `merged[-1][1]` — this silently changes the input. Append a fresh `[start, end]`.
5. **Comparing with the previous *input* interval instead of the last *merged* group.** For `[[1,10],[2,3],[4,5]]`, `[4,5]` doesn't overlap `[2,3]` but does overlap the group `[1,10]`.

**Debugging tip:** print `merged` after each step; it should always be sorted and disjoint.

---

## 13. Practice Questions

**Q1. What does the optimized code return for `[[1,4],[0,4]]`, and what happens without the sort?**

<details><summary>Hint</summary>Sorting puts `[0,4]` first.</summary></details>

**Answer:** Sorted: `[[0,4],[1,4]]` → `1 <= 4` → `[[0,4]]`. Without sorting: `[1,4]` is appended, then `0 <= 4` triggers a merge that only updates the end (`max(4,4) = 4`), giving `[[1,4]]` — the point 0 is lost. The start of a group is only correct because sorting guarantees nothing earlier comes later.

**Q2. Return the total length covered by the union of the intervals (each `[a, b]` has length `b - a`).**

<details><summary>Hint</summary>Merge first, then add up the lengths of the merged groups — overlaps are counted once.</summary></details>

**Answer:**

```python
def covered_length(intervals):
    merged = []
    for start, end in sorted(intervals):
        if merged and start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return sum(end - start for start, end in merged)


assert covered_length([[1, 3], [2, 6], [8, 10], [15, 18]]) == 5 + 2 + 3
assert covered_length([[1, 4], [4, 5]]) == 4
assert covered_length([[1, 10], [2, 3]]) == 9
```

**Q3. "Interval List Intersections" (LeetCode 986): given two lists of sorted, disjoint closed intervals, return their intersection.**

<details><summary>Hint</summary>Two pointers. The overlap of `[a1, a2]` and `[b1, b2]` is `[max(a1, b1), min(a2, b2)]` if that's non-empty. Then advance the pointer whose interval ends first.</summary></details>

**Answer:**

```python
def interval_intersection(first, second):
    i = j = 0
    result = []
    while i < len(first) and j < len(second):
        lo = max(first[i][0], second[j][0])
        hi = min(first[i][1], second[j][1])
        if lo <= hi:
            result.append([lo, hi])
        if first[i][1] < second[j][1]:   # the one that ends first can't meet anything else
            i += 1
        else:
            j += 1
    return result


assert interval_intersection(
    [[0, 2], [5, 10], [13, 23], [24, 25]],
    [[1, 5], [8, 12], [15, 24], [25, 26]],
) == [[1, 2], [5, 5], [8, 10], [15, 23], [24, 24], [25, 25]]
assert interval_intersection([[1, 3], [5, 9]], []) == []
```

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** Sort by start, then sweep, merging into the last group.
- **Key idea:** `if start <= merged[-1][1]: merged[-1][1] = max(merged[-1][1], end) else: append`.
- **Time:** `O(n log n)` (sorting).
- **Auxiliary space:** `O(n)` for sorting in Python (output not counted).
- **One-line memory hook:** *"Line them up, then tape on anything that reaches the last strip."*

### Completion checklist

- [x] Problem requirements verified
- [x] Examples and constraints verified
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force solution written and tested
- [x] Optimized Python solution written and tested (`tools/tests/p017.py`)
- [x] Line-by-line explanation written
- [x] Dry run completed with a real example
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
