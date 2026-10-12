# 016. Insert Interval

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Insert Interval |
| **LeetCode number** | 57 |
| **Topic (source list)** | Interval |
| **Also uses** | Array, linear scan (optionally binary search) |
| **Difficulty** | Medium |
| **LeetCode URL** | <https://leetcode.com/problems/insert-interval/> |
| **Pattern** | Three-phase sweep: before / overlapping / after |

---

## 2. Problem Explanation

### What are we given?

- `intervals` — a list of intervals, each written as `[start, end]`. The list is already **sorted by `start`**, and no two intervals in it overlap.
- `newInterval` — one more interval `[start, end]`.

### What must we return?

The list of intervals you get after adding `newInterval`, with two promises kept:

1. The result is still **sorted by start**.
2. The result still has **no overlapping intervals** — anything the new interval overlaps gets **merged** with it into one bigger interval.

### The rules

1. **"Overlap" means sharing at least one point.** The intervals are closed on both ends, so `[1, 2]` and `[2, 3]` **do** overlap (they share the point `2`) and must be merged into `[1, 3]`.
2. `[1, 2]` and `[3, 4]` do **not** overlap: no number belongs to both.
3. You don't have to modify `intervals` in place — building and returning a new list is fine.
4. An interval may have `start == end` (a single point such as `[5, 5]`).

### Examples

**Example 1**

```text
Input:  intervals = [[1,3],[6,9]], newInterval = [2,5]
Output: [[1,5],[6,9]]
```

`[2, 5]` overlaps `[1, 3]` (they share 2 and 3), so the two become `[1, 5]`. It ends at 5, before 6, so `[6, 9]` is untouched.

**Example 2**

```text
Input:  intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]], newInterval = [4,8]
Output: [[1,2],[3,10],[12,16]]
```

`[4, 8]` touches three existing intervals: `[3, 5]`, `[6, 7]` and `[8, 10]` (it shares the point 8 with the last one). All four collapse into `[3, 10]`. `[1, 2]` ends before 4 and `[12, 16]` starts after 10, so both stay as they are.

### Constraints

- `0 <= intervals.length <= 10^4`
- `intervals[i].length == 2`
- `0 <= start_i <= end_i <= 10^5`
- `intervals` is sorted by `start_i` in ascending order.
- `newInterval.length == 2`
- `0 <= start <= end <= 10^5`

Note that `intervals` **can be empty** — then the answer is just `[newInterval]`.

**Follow-up:** none in the official statement.

---

## 3. Everyday Analogy

> **Explain it like I'm five**

Imagine a long shelf where books are lined up in order, and some books are tied together with string into bundles. No two bundles touch.

Now someone hands you a new bundle and says: *"Put this on the shelf. If it touches any bundles, tie them all together into one."*

You walk along the shelf from the left:

1. **Bundles that end before the new one starts** — they're safely to the left. Leave them alone.
2. **Bundles that touch the new one** — untie nothing, just tie them **into** the new bundle. The new bundle grows each time.
3. Once you reach a bundle that **starts after** your (grown) new bundle ends, you place your bundle down. Everything from here on is safely to the right — leave it alone.

One walk down the shelf and you're done.

---

## 4. Step-by-Step Logic

1. **The list is already sorted and clean.** That's a big gift: every existing interval falls into exactly one of three groups relative to `newInterval`:
   - **Completely left:** it ends before the new one starts → `end_i < new_start`.
   - **Overlapping:** it shares at least one point with the new one.
   - **Completely right:** it starts after the new one ends → `start_i > new_end`.
2. Because the list is sorted, these groups appear **in that order**: first all the "left" ones, then the "overlapping" ones, then the "right" ones.
3. **Phase 1:** copy every "left" interval to the result.
4. **Phase 2:** while the current interval starts at or before `new_end`, it overlaps. Grow the new interval to cover it:
   - `new_start = min(new_start, start_i)`
   - `new_end = max(new_end, end_i)`
5. After phase 2, add the (possibly grown) new interval to the result.
6. **Phase 3:** copy all remaining intervals — they're all to the right.
7. **Why is the phase 2 test only `start_i <= new_end`?** Phase 1 already removed every interval with `end_i < new_start`, so anything left has `end_i >= new_start`. Two closed intervals overlap exactly when *each one starts no later than the other ends*, so the only remaining check is `start_i <= new_end`.

---

## 5. Brute-Force Solution

### Algorithm

Ignore the fact that the list is sorted:

1. Put all intervals plus `newInterval` into one list.
2. Sort it by start.
3. Merge overlapping intervals with the standard "Merge Intervals" sweep (see [017_merge_intervals.md](017_merge_intervals.md)).

### Python code

```python
from typing import List


class Solution:
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        everything = [list(iv) for iv in intervals] + [list(newInterval)]
        everything.sort(key=lambda iv: iv[0])

        merged = []
        for start, end in everything:
            if merged and start <= merged[-1][1]:      # shares a point with the last one
                merged[-1][1] = max(merged[-1][1], end)
            else:
                merged.append([start, end])
        return merged
```

### Explanation

- We copy every interval (`list(iv)`) so the merge step never edits the caller's lists.
- After sorting, overlapping intervals sit next to each other, so a single pass that compares each interval with the **last merged one** is enough.
- `start <= merged[-1][1]` uses `<=` because touching intervals count as overlapping here.

### Complexity

- **Time:** `O(n log n)` because of the sort. This actually **passes** on LeetCode (`n <= 10^4`), but it throws away the free information that the input is already sorted.
- **Auxiliary space:** `O(n)` for the copied list (and the sort's own buffer).

---

## 6. Optimized Solution

### Idea

Use the sortedness: one left-to-right walk with three phases (left / overlapping / right). No sorting needed.

### Algorithm

1. `result = []`, `i = 0`, and unpack `new_start, new_end = newInterval`.
2. **Phase 1:** while `intervals[i][1] < new_start`, append `intervals[i]` and move on.
3. **Phase 2:** while `intervals[i][0] <= new_end`, absorb it: `new_start = min(...)`, `new_end = max(...)`, move on.
4. Append `[new_start, new_end]`.
5. **Phase 3:** append everything that's left.
6. Return `result`.

### Python code (LeetCode-ready)

```python
from typing import List


class Solution:
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        result = []
        i, n = 0, len(intervals)
        new_start, new_end = newInterval

        # Phase 1: intervals that end before the new one starts.
        while i < n and intervals[i][1] < new_start:
            result.append(intervals[i])
            i += 1

        # Phase 2: intervals that overlap the new one -> merge them in.
        while i < n and intervals[i][0] <= new_end:
            new_start = min(new_start, intervals[i][0])
            new_end = max(new_end, intervals[i][1])
            i += 1
        result.append([new_start, new_end])

        # Phase 3: intervals that start after the merged one ends.
        while i < n:
            result.append(intervals[i])
            i += 1

        return result
```

---

## 7. Line-by-Line Explanation

| Line | What it does | Why |
|---|---|---|
| `result = []` | The answer list we build. | The statement allows returning a new list. |
| `i, n = 0, len(intervals)` | `i` is our position in `intervals`; `n` is its length. | All three phases share the same pointer `i`, so the walk never goes backwards. |
| `new_start, new_end = newInterval` | Copies the new interval's ends into two variables. | We will grow these numbers; we don't want to edit the caller's `newInterval` list. |
| `while i < n and intervals[i][1] < new_start:` | Phase 1 condition: the current interval ends **strictly before** the new one begins. | Strict `<`: if `end_i == new_start`, they share a point and must merge instead. |
| `result.append(intervals[i])` | Keeps it unchanged. | It cannot touch the new interval. |
| `while i < n and intervals[i][0] <= new_end:` | Phase 2 condition: the current interval starts at or before the new one ends. | Together with phase 1 having finished, this means they share a point. `<=` handles touching ends like `[4, 8]` and `[8, 10]`. |
| `new_start = min(new_start, intervals[i][0])` | Stretches the left edge if needed. | Only the **first** overlapping interval can start earlier, but `min` is simplest and always right. |
| `new_end = max(new_end, intervals[i][1])` | Stretches the right edge if needed. | An overlapping interval may stick out to the right (like `[8, 10]` in Example 2). Using `max` also handles the case where it's fully inside. |
| `result.append([new_start, new_end])` | Places the merged interval. | Runs even if phase 2 absorbed nothing — then the new interval is just inserted as-is. |
| `while i < n: result.append(intervals[i])` | Phase 3: copies the rest. | Every remaining interval starts after `new_end`, so none overlap. |
| `return result` | Returns the sorted, overlap-free list. | Phases produce left, merged, right — already in order. |

---

## 8. Dry Run

**Input:** `intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]]`, `newInterval = [4,8]`

Start: `new_start = 4`, `new_end = 8`, `result = []`.

| Step | Phase | `i` | `intervals[i]` | Check | Action | `new_start, new_end` | `result` |
|---|---|---|---|---|---|---|---|
| 1 | 1 | 0 | `[1,2]` | `2 < 4` ✔ | keep it | 4, 8 | `[[1,2]]` |
| 2 | 1 | 1 | `[3,5]` | `5 < 4` ✘ | leave phase 1 | 4, 8 | `[[1,2]]` |
| 3 | 2 | 1 | `[3,5]` | `3 <= 8` ✔ | merge: `min(4,3)=3`, `max(8,5)=8` | 3, 8 | `[[1,2]]` |
| 4 | 2 | 2 | `[6,7]` | `6 <= 8` ✔ | merge: `min(3,6)=3`, `max(8,7)=8` | 3, 8 | `[[1,2]]` |
| 5 | 2 | 3 | `[8,10]` | `8 <= 8` ✔ | merge: `min(3,8)=3`, `max(8,10)=10` | 3, 10 | `[[1,2]]` |
| 6 | 2 | 4 | `[12,16]` | `12 <= 10` ✘ | leave phase 2, append `[3,10]` | 3, 10 | `[[1,2],[3,10]]` |
| 7 | 3 | 4 | `[12,16]` | — | copy | 3, 10 | `[[1,2],[3,10],[12,16]]` |

**Result:** `[[1,2],[3,10],[12,16]]` ✅

**Short dry run — Example 1:** `intervals = [[1,3],[6,9]]`, `newInterval = [2,5]`

- Phase 1: `[1,3]` → `3 < 2`? No → phase 1 ends immediately.
- Phase 2: `[1,3]` → `1 <= 5` ✔ → `new = [min(2,1), max(5,3)] = [1,5]`. Next `[6,9]` → `6 <= 5`? No. Append `[1,5]`.
- Phase 3: copy `[6,9]`.

**Result:** `[[1,5],[6,9]]` ✅

---

## 9. Concepts, Data Structures, and Patterns

- **Intervals as pairs `[start, end]`:** here they are *closed* — both ends belong to the interval — so touching intervals overlap. Compare with meeting times in [019_meeting_rooms_leetcode_premium.md](019_meeting_rooms_leetcode_premium.md), where a meeting ending at 10 does **not** clash with one starting at 10.
- **Overlap test for closed intervals:** `[a, b]` and `[c, d]` overlap ⇔ `a <= d and c <= b`. The phases split this test into two halves.
- **Exploiting sorted input:** because the list is sorted and disjoint, the three groups are contiguous, so one pointer and three `while` loops cover everything in `O(n)`.
- **Merge sweep:** the brute-force is exactly the algorithm of [017_merge_intervals.md](017_merge_intervals.md). Insert Interval is "Merge Intervals when only one interval is out of place".
- **Binary search (optional):** the boundaries of phase 1 and phase 3 can be found with `bisect` in `O(log n)`, but building the output list is still `O(n)`, so the total doesn't improve (see Practice Q2).
- **Related problems:** Merge Intervals ([017](017_merge_intervals.md)), Non-overlapping Intervals ([018](018_non_overlapping_intervals.md)), Meeting Rooms II ([020](020_meeting_rooms_ii_leetcode_premium.md)).

---

## 10. Complexity Analysis

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Brute force (add, sort, merge) | `O(n log n)` | `O(n)` | Sorting `n + 1` intervals dominates; we also copy the list. |
| Optimized three-phase sweep | `O(n)` | `O(1)` | Each interval is looked at once by exactly one of the three loops. Besides the output list we only keep `i`, `new_start`, `new_end`. |
| Binary search for boundaries | `O(n)` | `O(1)` | Finding the boundaries is `O(log n)`, but copying the output is still `O(n)`. |

The output itself has up to `n + 1` intervals and is not counted as auxiliary space.

---

## 11. Edge Cases

| Case | `intervals` | `newInterval` | Expected result | Why |
|---|---|---|---|---|
| Empty list | `[]` | `[5,7]` | `[[5,7]]` | Nothing to merge with. |
| New goes first | `[[3,5]]` | `[1,2]` | `[[1,2],[3,5]]` | `2 < 3`, no shared point. |
| New goes last | `[[1,2]]` | `[5,6]` | `[[1,2],[5,6]]` | Phase 1 takes `[1,2]`, phase 2 takes nothing. |
| Touching ends | `[[1,2]]` | `[2,3]` | `[[1,3]]` | They share the point 2. |
| New swallows everything | `[[1,2],[3,4]]` | `[0,10]` | `[[0,10]]` | Every interval overlaps. |
| New fully inside one | `[[1,5]]` | `[3,3]` | `[[1,5]]` | `max`/`min` keep the bigger interval. |
| Point interval in a gap | `[[0,0],[2,2]]` | `[1,1]` | `[[0,0],[1,1],[2,2]]` | Neighbours at distance 1 share no point. |

---

## 12. Common Mistakes and Debugging

1. **Using `<=` in phase 1.** `intervals[i][1] <= new_start` would treat `[1,2]` and `[2,3]` as separate. Touching closed intervals must merge, so phase 1 needs strict `<`.
2. **Using `<` in phase 2.** `intervals[i][0] < new_end` misses `[8,10]` in Example 2 and returns `[[1,2],[3,8],[8,10],[12,16]]` — overlapping output.
3. **Forgetting `max` on the end.** Writing `new_end = intervals[i][1]` breaks when the existing interval sits fully inside the new one (e.g. `[6,7]` inside `[3,8]` would shrink the end to 7).
4. **Forgetting to append the new interval** when phase 2 absorbed nothing (or when the list is empty). The `append` must sit *after* phase 2, unconditionally.
5. **Dropping `i < n` from a `while`.** Leads to `IndexError` when the new interval belongs at the end.
6. **Editing `newInterval` in place** (`newInterval[0] = ...`). It works, but it changes the caller's data — use local variables.

**Debugging tip:** print `phase, i, new_start, new_end` at each step and compare with the dry-run table.

---

## 13. Practice Questions

**Q1. Trace the optimized solution on `intervals = [[1,5],[10,15]]`, `newInterval = [5,10]`. What is returned?**

<details><summary>Hint</summary>Phase 1 uses strict `<`; phase 2 uses `<=`. The new interval touches both neighbours.</summary></details>

**Answer:** Phase 1: `5 < 5`? No. Phase 2: `[1,5]` → `1 <= 10` ✔ → `[1,10]`; `[10,15]` → `10 <= 10` ✔ → `[1,15]`. Result `[[1,15]]` — one interval, because `[5,10]` shares a point with each neighbour.

**Q2. Find the phase boundaries with binary search (`bisect`) instead of scanning.**

<details><summary>Hint</summary>The ends are sorted too (the intervals are disjoint and sorted). Phase 1 = intervals with `end < new_start`; phase 3 = intervals with `start > new_end`.</summary></details>

**Answer:**

```python
import bisect


def insert_with_bisect(intervals, new_interval):
    starts = [s for s, _ in intervals]
    ends = [e for _, e in intervals]
    new_start, new_end = new_interval
    left = bisect.bisect_left(ends, new_start)      # first interval with end >= new_start
    right = bisect.bisect_right(starts, new_end)    # first interval with start > new_end
    if left < right:                                # some intervals overlap
        new_start = min(new_start, intervals[left][0])
        new_end = max(new_end, intervals[right - 1][1])
    return intervals[:left] + [[new_start, new_end]] + intervals[right:]


assert insert_with_bisect([[1, 3], [6, 9]], [2, 5]) == [[1, 5], [6, 9]]
assert insert_with_bisect([[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8]) == [[1, 2], [3, 10], [12, 16]]
assert insert_with_bisect([], [5, 7]) == [[5, 7]]
assert insert_with_bisect([[1, 5]], [3, 3]) == [[1, 5]]
```

The searches are `O(log n)`, but building the lists `starts`, `ends` and the slices is still `O(n)`.

**Q3. "Remove Interval" (LeetCode 1272): given sorted disjoint half-open intervals `[a, b)` and one half-open interval `toBeRemoved`, return what remains after cutting it out.**

<details><summary>Hint</summary>For each interval, keep the piece left of the cut (if any) and the piece right of the cut (if any). With half-open intervals, `[a, b)` and `[b, c)` share no point.</summary></details>

**Answer:**

```python
def remove_interval(intervals, to_be_removed):
    cut_start, cut_end = to_be_removed
    result = []
    for a, b in intervals:
        if b <= cut_start or a >= cut_end:   # no overlap: keep whole
            result.append([a, b])
            continue
        if a < cut_start:                    # piece sticking out on the left
            result.append([a, cut_start])
        if b > cut_end:                      # piece sticking out on the right
            result.append([cut_end, b])
    return result


assert remove_interval([[0, 2], [3, 4], [5, 7]], [1, 6]) == [[0, 1], [6, 7]]
assert remove_interval([[0, 5]], [2, 3]) == [[0, 2], [3, 5]]
assert remove_interval([[0, 1]], [1, 2]) == [[0, 1]]
```

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** Three-phase sweep over a sorted, disjoint interval list.
- **Key idea:** copy intervals with `end < new_start`; merge intervals with `start <= new_end` into the new one (`min` start, `max` end); append it; copy the rest.
- **Time:** `O(n)`.
- **Auxiliary space:** `O(1)` (output not counted).
- **One-line memory hook:** *"Left alone, tie together, right alone."*

### Completion checklist

- [x] Problem requirements verified
- [x] Examples and constraints verified
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force solution written and tested
- [x] Optimized Python solution written and tested (`tools/tests/p016.py`)
- [x] Line-by-line explanation written
- [x] Dry run completed with a real example
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
