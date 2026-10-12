# 019. Meeting Rooms (LeetCode Premium)

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Meeting Rooms |
| **LeetCode number** | 252 (Premium) |
| **Topic (source list)** | Interval |
| **Also uses** | Array, Sorting |
| **Difficulty** | Easy |
| **LeetCode URL** | <https://leetcode.com/problems/meeting-rooms/> |
| **Free practice** | LintCode 920 — Meeting Rooms (uses an `Interval` object with `.start` / `.end` instead of `[start, end]` lists) |
| **Pattern** | Sort by start, then compare neighbours |

---

## 2. Problem Explanation

> ⚠️ **This is a LeetCode Premium problem. The official statement could not be checked for these notes; the examples and constraints below are the commonly published ones — confirm them on LeetCode if you have Premium access.**

### What are we given?

`intervals` — a list of meetings, each written as `[start, end]`. The meeting occupies the time from `start` up to (but not including) `end`.

### What must we return?

`True` if **one person** could attend **every** meeting — that is, no two meetings overlap in time. Otherwise `False`.

### The rules

1. **Times are half-open: `[start, end)`.** A meeting that ends at time `t` does **not** clash with one that starts at time `t` — you can walk straight from one to the other. So `[1, 5]` and `[5, 10]` are fine together.
2. Two meetings clash if one starts **strictly before** the other ends (and vice versa).
3. The meetings are given in **any order**.
4. The signature is `def canAttendMeetings(self, intervals: List[List[int]]) -> bool`.

### Examples (commonly published)

**Example 1**

```text
Input:  intervals = [[0,30],[5,10],[15,20]]
Output: false
```

The meeting `[0, 30]` lasts the whole time, and both `[5, 10]` and `[15, 20]` happen during it. One person can't be in two places at once.

**Example 2**

```text
Input:  intervals = [[7,10],[2,4]]
Output: true
```

In time order, `[2, 4]` finishes at 4, well before `[7, 10]` starts at 7. No clash.

### Constraints (commonly published — see the warning above)

- `0 <= intervals.length <= 10^4`
- `intervals[i].length == 2`
- `0 <= start_i < end_i <= 10^6`

Note that the list **can be empty** — with no meetings, the answer is `True`.

**Follow-up:** none known. The natural next question is "how many rooms would we need?" — that's Meeting Rooms II ([020_meeting_rooms_ii_leetcode_premium.md](020_meeting_rooms_ii_leetcode_premium.md)).

**Where to practice for free:** LintCode 920 "Meeting Rooms" is the same task. There, each meeting is an `Interval` object, so you write `iv.start` / `iv.end` instead of `iv[0]` / `iv[1]`.

---

## 3. Everyday Analogy

> **Explain it like I'm five**

Your mum gives you a stack of party invitations, each with a start time and an end time, all shuffled. Can you go to **all** of them?

Easy way to check: put the invitations **in order of start time**. Now look at each pair of neighbours:

- Does the next party start **before** the previous one finishes? Then you'd have to leave a party early — you **can't** go to all of them.
- If every party starts when or after the previous one ended, you can go to every single one.

You never need to compare parties that aren't neighbours, because in time order the closest "threat" to each party is the one right before it.

---

## 4. Step-by-Step Logic

1. **Half-open overlap test:** meetings `[a, b)` and `[c, d)` clash ⇔ `a < d and c < b`.
2. **Brute force idea:** test every pair with that rule. Correct but `O(n²)`.
3. **Sort by start.** After sorting, if meeting `i` doesn't clash with meeting `i - 1`, it can't clash with any earlier meeting either:
   - Suppose no neighbour pair clashes, so `end[k-1] <= start[k]` for every `k`. Since every meeting has `start < end`, this gives `start[0] < end[0] <= start[1] < end[1] <= start[2] < ...` — the meetings march strictly forward in time and nothing overlaps.
   - Conversely, if some neighbour pair has `start[i] < end[i-1]`, those two clash (and `start[i-1] <= start[i] < end[i]` gives the other half of the test).
4. So: sort, then check each neighbour pair. If any `start[i] < end[i-1]`, return `False`. Otherwise `True`.
5. Empty list and single meeting: the loop doesn't run → `True`.

---

## 5. Brute-Force Solution

### Algorithm

Compare every pair of meetings. If any pair overlaps, return `False`; if none do, return `True`.

### Python code

```python
from typing import List


class Solution:
    def canAttendMeetings(self, intervals: List[List[int]]) -> bool:
        n = len(intervals)
        for i in range(n):
            for j in range(i + 1, n):
                a_start, a_end = intervals[i]
                b_start, b_end = intervals[j]
                if a_start < b_end and b_start < a_end:   # they share some time
                    return False
        return True
```

### Explanation

- The double loop visits each unordered pair `(i, j)` once.
- `a_start < b_end and b_start < a_end` is the overlap test for half-open intervals. Strict `<` means `[1, 5]` and `[5, 10]` are **not** a clash.
- The input order doesn't matter, so no sorting is needed.

### Complexity

- **Time:** `O(n²)` — about `5 · 10^7` pair checks for `n = 10^4`. That is very slow in Python and likely to **time out**.
- **Auxiliary space:** `O(1)`.

---

## 6. Optimized Solution

### Idea

Sort meetings by start time, then only compare each meeting with the one just before it.

### Algorithm

1. Sort `intervals` by start.
2. For `i` from 1 to `n - 1`: if `intervals[i][0] < intervals[i - 1][1]`, return `False`.
3. Return `True`.

### Python code (LeetCode-ready)

```python
from typing import List


class Solution:
    def canAttendMeetings(self, intervals: List[List[int]]) -> bool:
        intervals.sort(key=lambda iv: iv[0])            # by start time

        for i in range(1, len(intervals)):
            if intervals[i][0] < intervals[i - 1][1]:   # starts before the previous one ends
                return False

        return True
```

> **LintCode 920 version:** replace `iv[0]` with `iv.start` and `intervals[i][0]` / `intervals[i - 1][1]` with `intervals[i].start` / `intervals[i - 1].end`.

---

## 7. Line-by-Line Explanation

| Line | What it does | Why |
|---|---|---|
| `intervals.sort(key=lambda iv: iv[0])` | Orders meetings by start time. | After sorting, any clash shows up between neighbours. (This reorders the caller's list; use `sorted(...)` to avoid that.) |
| `for i in range(1, len(intervals)):` | Looks at every meeting except the first, paired with the one before it. | Pairs `(0,1), (1,2), ...`. With 0 or 1 meetings the loop never runs. |
| `if intervals[i][0] < intervals[i - 1][1]:` | Does this meeting start before the previous one ends? | Strict `<`: starting exactly when the previous ends is allowed (half-open). |
| `return False` | Stops at the first clash. | One clash is enough to make attending all impossible. |
| `return True` | No neighbour pair clashed. | By the argument in Step 3 of the logic, no pair at all clashes. |

---

## 8. Dry Run

**Input:** `intervals = [[0,30],[5,10],[15,20]]` (Example 1)

After sorting by start: `[[0,30],[5,10],[15,20]]` (unchanged).

| `i` | Previous meeting | Current meeting | Check `start_i < end_{i-1}` | Result |
|---|---|---|---|---|
| 1 | `[0,30]` | `[5,10]` | `5 < 30` ✔ | clash → return `False` |

**Result:** `False` ✅ (the loop stops at the first clash; `[15,20]` is never examined)

**Second dry run — Example 2:** `intervals = [[7,10],[2,4]]`

Sorted: `[[2,4],[7,10]]`

| `i` | Previous meeting | Current meeting | Check `start_i < end_{i-1}` | Result |
|---|---|---|---|---|
| 1 | `[2,4]` | `[7,10]` | `7 < 4` ✘ | no clash |

Loop ends → **Result:** `True` ✅

**Touching meetings:** `[[5,8],[1,3],[3,5]]` → sorted `[[1,3],[3,5],[5,8]]` → `3 < 3`? No. `5 < 5`? No. → `True`.

---

## 9. Concepts, Data Structures, and Patterns

- **Half-open intervals `[start, end)`:** the natural model for time slots. Two meetings clash iff `a < d and c < b`. Compare with the **closed** intervals of Merge Intervals ([017_merge_intervals.md](017_merge_intervals.md)), where touching counts as overlap.
- **Sort, then check neighbours:** sorting turns an all-pairs check into a single pass. The same idea appears in Contains Duplicate ([003_contains_duplicate.md](../01_array/003_contains_duplicate.md)), where sorting puts equal values next to each other.
- **Early exit:** return as soon as the answer is known.
- **Relation to other interval problems:** this asks "does Non-overlapping Intervals ([018](018_non_overlapping_intervals.md)) need **zero** removals?" and "does Meeting Rooms II ([020](020_meeting_rooms_ii_leetcode_premium.md)) need at most **one** room?"
- **LintCode `Interval` objects:** the same algorithm, accessed through attributes instead of list indices.

---

## 10. Complexity Analysis

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Brute force (all pairs) | `O(n²)` | `O(1)` | `n(n-1)/2` pair checks, constant memory. |
| Sort + neighbour check (optimized) | `O(n log n)` | `O(n)` | Sorting dominates; the scan is `O(n)`. Our code uses `O(1)` extra variables, but Python's Timsort can use up to `O(n)` temporary memory. |

---

## 11. Edge Cases

| Case | Input | Expected result | Why |
|---|---|---|---|
| No meetings | `[]` | `True` | Nothing can clash. |
| One meeting | `[[1,5]]` | `True` | Nothing to clash with. |
| Back-to-back | `[[1,5],[5,10]]` | `True` | Ending at 5 and starting at 5 is allowed. |
| Identical meetings | `[[1,5],[1,5]]` | `False` | Same time slot twice. |
| Nested meeting | `[[1,10],[2,3]]` | `False` | `[2,3]` happens inside `[1,10]`. |
| Unsorted but fine | `[[5,8],[1,3],[3,5]]` | `True` | Sorted, they touch end to start. |

---

## 12. Common Mistakes and Debugging

1. **Using `<=` instead of `<`.** Then back-to-back meetings like `[[1,5],[5,10]]` wrongly return `False`.
2. **Forgetting to sort.** For `[[7,10],[2,4]]` without sorting, the check `2 < 10` reports a false clash.
3. **Comparing with the wrong neighbour field** (e.g. `intervals[i][1] < intervals[i-1][0]`). Write the rule in words first: *"current start is before previous end"*.
4. **Crashing on an empty list** by reading `intervals[0]` before the loop. `range(1, 0)` is empty, so the code above is safe.
5. **Assuming the published constraints are official.** This is a Premium problem; keep your solution robust (handle an empty list, any order).

**Debugging tip:** print the sorted list and each `(previous end, current start)` pair.

---

## 13. Practice Questions

**Q1. Without running code, what does the optimized solution return for `[[9,12],[1,4],[4,9]]`?**

<details><summary>Hint</summary>Sort first, then check each start against the previous end with strict `<`.</summary></details>

**Answer:** Sorted: `[[1,4],[4,9],[9,12]]`. Checks: `4 < 4`? No. `9 < 9`? No. → `True`. All three meetings are back to back.

**Q2. Instead of `True`/`False`, return the first clashing pair in time order (or `None`).**

<details><summary>Hint</summary>Same loop — just return the two meetings instead of `False`.</summary></details>

**Answer:**

```python
def first_conflict(intervals):
    ordered = sorted(intervals)
    for i in range(1, len(ordered)):
        if ordered[i][0] < ordered[i - 1][1]:
            return ordered[i - 1], ordered[i]
    return None


assert first_conflict([[0, 30], [5, 10], [15, 20]]) == ([0, 30], [5, 10])
assert first_conflict([[7, 10], [2, 4]]) is None
assert first_conflict([]) is None
```

**Q3. Suppose meetings were closed intervals `[start, end]` (a meeting ending at 5 *does* clash with one starting at 5). What changes?**

<details><summary>Hint</summary>Only the comparison operator.</summary></details>

**Answer:** Change `<` to `<=`: a clash happens when `start_i <= end_{i-1}`.

```python
def can_attend_closed(intervals):
    ordered = sorted(intervals)
    for i in range(1, len(ordered)):
        if ordered[i][0] <= ordered[i - 1][1]:
            return False
    return True


assert can_attend_closed([[1, 5], [5, 10]]) is False
assert can_attend_closed([[1, 4], [5, 10]]) is True
assert can_attend_closed([[7, 10], [2, 4]]) is True
```

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** Sort by start, compare neighbours.
- **Key idea:** after sorting, a clash exists iff some `start_i < end_{i-1}` (half-open times, so touching is fine).
- **Time:** `O(n log n)`.
- **Auxiliary space:** `O(1)` beyond sorting (`O(n)` worst case for Python's sort).
- **One-line memory hook:** *"Line up the invitations; does anyone start before the last one ends?"*

### Completion checklist

- [x] Problem requirements written from the well-known signature and commonly published description
- [ ] Examples and constraints verified against official statement — **not done**: this is a LeetCode Premium problem and the official statement could not be fetched; the examples and constraints are the commonly published ones
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force solution written and tested
- [x] Optimized Python solution written and tested (`tools/tests/p019.py`)
- [x] Line-by-line explanation written
- [x] Dry run completed with the commonly published examples
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
