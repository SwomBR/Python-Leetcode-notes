# 020. Meeting Rooms II (LeetCode Premium)

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Meeting Rooms II |
| **LeetCode number** | 253 (Premium) |
| **Topic (source list)** | Interval |
| **Also uses** | Heap (Priority Queue), Sorting, Sweep line / Two pointers |
| **Difficulty** | Medium |
| **LeetCode URL** | <https://leetcode.com/problems/meeting-rooms-ii/> |
| **Free practice** | LintCode 919 — Meeting Rooms II (uses an `Interval` object with `.start` / `.end` instead of `[start, end]` lists) |
| **Pattern** | Sort by start + min-heap of end times (or: sweep over sorted starts and ends) |

---

## 2. Problem Explanation

> ⚠️ **This is a LeetCode Premium problem. The official statement could not be checked for these notes; the examples and constraints below are the commonly published ones — confirm them on LeetCode if you have Premium access.**

### What are we given?

`intervals` — a list of meetings, each written as `[start, end]`. A meeting occupies the time from `start` up to (but not including) `end`.

### What must we return?

The **minimum number of conference rooms** needed so that every meeting can take place, with no two meetings sharing a room at the same time.

### The rules

1. **Times are half-open: `[start, end)`.** If one meeting ends at time `t` and another starts at `t`, the second can use the same room.
2. The meetings are given in **any order**.
3. The signature is `def minMeetingRooms(self, intervals: List[List[int]]) -> int`.

An equivalent way to say it: the answer is the **largest number of meetings happening at the same moment**.

### Examples (commonly published)

**Example 1**

```text
Input:  intervals = [[0,30],[5,10],[15,20]]
Output: 2
```

`[0, 30]` needs a room the whole time. `[5, 10]` happens during it, so it needs a second room. By the time `[15, 20]` starts, `[5, 10]` has finished and its room is free again. Two rooms are enough, and at time 5 two meetings really are running together, so fewer won't do.

**Example 2**

```text
Input:  intervals = [[7,10],[2,4]]
Output: 1
```

`[2, 4]` is over long before `[7, 10]` starts, so one room serves both.

### Constraints (commonly published — see the warning above)

- `1 <= intervals.length <= 10^4`
- `0 <= start_i < end_i <= 10^6`

**Follow-up:** none known.

**Where to practice for free:** LintCode 919 "Meeting Rooms II" is the same task. There, each meeting is an `Interval` object, so you write `iv.start` / `iv.end` instead of `iv[0]` / `iv[1]`.

---

## 3. Everyday Analogy

> **Explain it like I'm five**

You're in charge of rooms at a school. Teachers arrive with their class times, and you want to open as few rooms as possible.

You handle the teachers **in order of when their class starts**. On your desk you keep one sticky note per open room, showing **when that room becomes free**. You always look at the note with the **earliest** free time first.

When a new teacher arrives:

- If the earliest-free room is **already free** by the class's start time → give them that room and write the new finish time on its note.
- If even the earliest-free room is still busy → every room is busy → **open a new room** with a new sticky note.

At the end, the number of sticky notes is the number of rooms you needed.

The "earliest sticky note" is exactly what a **min-heap** gives you instantly.

---

## 4. Step-by-Step Logic

1. **Rooms needed = peak overlap.** At any moment, the number of rooms in use is the number of meetings running. We need as many rooms as the busiest moment — and that many is always enough (assign greedily as below).
2. **Process meetings by start time** (sort by start).
3. **Track every open room's end time** in a min-heap, so the room that frees up soonest is on top.
4. For each meeting `[start, end]`:
   - If the heap is non-empty and `heap[0] <= start`, the soonest-free room is free → **reuse it**: pop its end time and push `end`.
   - Otherwise every open room is still busy (the soonest one is busy, so all are) → **open a new room**: push `end`.
5. The heap never shrinks, it only grows when a new room is opened, so at the end `len(heap)` = rooms opened = the answer.
6. **Why reuse the soonest-free room?** When it's free, reusing *any* free room keeps the room count the same; we pick the soonest because it's the one we can check in `O(1)`.
7. **Why `<=`?** Half-open times: a room freed at time 10 can host a meeting starting at 10.

---

## 5. Brute-Force Solution

### Algorithm

The busiest moment is always **at the start of some meeting** (the number of running meetings only goes up when a meeting starts). So for every meeting's start time `t`, count the meetings with `start <= t < end`. The answer is the largest count.

### Python code

```python
from typing import List


class Solution:
    def minMeetingRooms(self, intervals: List[List[int]]) -> int:
        best = 0
        for t, _ in intervals:                       # candidate busiest moments
            running = 0
            for start, end in intervals:
                if start <= t < end:                 # this meeting is in progress at time t
                    running += 1
            best = max(best, running)
        return best
```

### Explanation

- The outer loop tries each start time as the "busiest moment".
- The inner loop counts meetings in progress at that moment. `start <= t < end` encodes half-open times: a meeting ending at `t` is already over.
- The count includes the meeting that starts at `t` itself, so `best` is at least 1.

### Complexity

- **Time:** `O(n²)` — about `10^8` checks for `n = 10^4`, which is far too slow in Python and would **time out**.
- **Auxiliary space:** `O(1)`.

---

## 6. Optimized Solution

### Idea

Sort meetings by start, and keep a min-heap of the end times of rooms in use. Reuse the earliest-ending room when it's free; otherwise open a new room.

### Algorithm

1. Sort `intervals` by start.
2. `end_times = []` (a min-heap).
3. For each `[start, end]`:
   - if `end_times` and `end_times[0] <= start`: `heapreplace(end_times, end)` (pop the smallest, push `end`);
   - else: `heappush(end_times, end)`.
4. Return `len(end_times)`.

### Python code (LeetCode-ready)

```python
import heapq
from typing import List


class Solution:
    def minMeetingRooms(self, intervals: List[List[int]]) -> int:
        intervals.sort(key=lambda iv: iv[0])         # handle meetings in start order
        end_times = []                               # min-heap: when each open room frees up

        for start, end in intervals:
            if end_times and end_times[0] <= start:  # the soonest-free room is free
                heapq.heapreplace(end_times, end)    # reuse it
            else:
                heapq.heappush(end_times, end)       # all rooms busy -> open a new one

        return len(end_times)
```

### Alternative: sweep over sorted starts and ends (two pointers)

```python
from typing import List


class Solution:
    def minMeetingRooms(self, intervals: List[List[int]]) -> int:
        starts = sorted(s for s, _ in intervals)
        ends = sorted(e for _, e in intervals)

        rooms = 0
        e = 0                                        # next meeting (by end time) to finish
        for s in starts:
            if s >= ends[e]:                         # some meeting has finished -> reuse its room
                e += 1
            else:
                rooms += 1                           # nobody has finished -> need a new room
        return rooms
```

We don't care *which* meeting ends — only *how many* have ended by each start time. Each start either reuses a room freed by the next end (if that end is `<= s`) or opens a new one. `O(n log n)` time for the two sorts, `O(n)` extra space for the two lists.

> **LintCode 919 version:** use `iv.start` / `iv.end` instead of `iv[0]` / `iv[1]` (e.g. `intervals.sort(key=lambda iv: iv.start)` and `for iv in intervals: start, end = iv.start, iv.end`).

---

## 7. Line-by-Line Explanation

(Heap solution)

| Line | What it does | Why |
|---|---|---|
| `import heapq` | Python's min-heap helpers. | They work on a plain list; `list[0]` is always the smallest. |
| `intervals.sort(key=lambda iv: iv[0])` | Sorts meetings by start time. | We assign rooms in the order meetings begin. (Reorders the caller's list.) |
| `end_times = []` | Heap of end times, one per open room. | The smallest end time = the room that frees up first. |
| `for start, end in intervals:` | Handles each meeting. | — |
| `if end_times and end_times[0] <= start:` | Is the soonest-free room free by `start`? | `end_times` must be non-empty before reading `[0]`. `<=` because a room freed at `t` can be reused at `t`. |
| `heapq.heapreplace(end_times, end)` | Pops the smallest end time and pushes `end` in one step. | The room keeps existing; it's now busy until `end`. One `O(log k)` operation instead of a pop plus a push. |
| `heapq.heappush(end_times, end)` | Adds a new room busy until `end`. | If the soonest-free room is still busy, every room is busy. |
| `return len(end_times)` | Number of rooms ever opened. | Rooms are never removed, only reused. |

---

## 8. Dry Run

**Input:** `intervals = [[0,30],[5,10],[15,20]]` (Example 1)

Sorted by start: `[[0,30],[5,10],[15,20]]` (unchanged).

| Step | Meeting | `end_times` before | Check `end_times[0] <= start` | Action | `end_times` after | Rooms |
|---|---|---|---|---|---|---|
| 1 | `[0,30]` | `[]` | heap empty | open new room | `[30]` | 1 |
| 2 | `[5,10]` | `[30]` | `30 <= 5` ✘ | open new room | `[10, 30]` | 2 |
| 3 | `[15,20]` | `[10, 30]` | `10 <= 15` ✔ | reuse: pop 10, push 20 | `[20, 30]` | 2 |

**Result:** `2` ✅

**Second dry run — Example 2:** `[[7,10],[2,4]]` → sorted `[[2,4],[7,10]]`

| Step | Meeting | `end_times` before | Check | Action | `end_times` after |
|---|---|---|---|---|---|
| 1 | `[2,4]` | `[]` | empty | open | `[4]` |
| 2 | `[7,10]` | `[4]` | `4 <= 7` ✔ | reuse | `[10]` |

**Result:** `1` ✅

**Third dry run — touching meetings (own example):** `[[1,4],[2,5],[4,6],[5,7]]`

| Meeting | `end_times` before | Check | Action | `end_times` after |
|---|---|---|---|---|
| `[1,4]` | `[]` | empty | open | `[4]` |
| `[2,5]` | `[4]` | `4 <= 2` ✘ | open | `[4, 5]` |
| `[4,6]` | `[4, 5]` | `4 <= 4` ✔ | reuse | `[5, 6]` |
| `[5,7]` | `[5, 6]` | `5 <= 5` ✔ | reuse | `[6, 7]` |

**Result:** `2` — the `<=` lets rooms be handed over at exactly the end time.

**Two-pointer version on Example 1:** `starts = [0, 5, 15]`, `ends = [10, 20, 30]`.
`s = 0`: `0 >= 10`? No → rooms = 1. `s = 5`: `5 >= 10`? No → rooms = 2. `s = 15`: `15 >= 10` ✔ → reuse, `e = 1`. **Result:** `2` ✅

---

## 9. Concepts, Data Structures, and Patterns

- **Min-heap (priority queue):** `heapq` keeps the smallest item at index 0. `heappush` and `heapreplace` cost `O(log k)` for a heap of size `k`. More heap problems: Top K Frequent Elements ([074](../10_heap/074_top_k_frequent_elements.md)), Find Median from Data Stream ([075](../10_heap/075_find_median_from_data_stream.md)), Merge K Sorted Lists ([024](../04_linked_list/024_merge_k_sorted_lists.md)).
- **Greedy resource allocation:** handle requests in start order and reuse the resource that frees up earliest.
- **Sweep line / chronological ordering:** turn meetings into events (+1 at start, -1 at end) and track the running count; the peak is the answer. The two-pointer version is this idea in compact form (see Practice Q2 for the explicit event list).
- **Half-open intervals:** ends are processed before starts at the same time, which is why the checks are `<=` / `>=`.
- **Related problems:** Meeting Rooms ([019_meeting_rooms_leetcode_premium.md](019_meeting_rooms_leetcode_premium.md)) asks whether one room is enough (answer `<= 1`); Merge Intervals ([017](017_merge_intervals.md)); Non-overlapping Intervals ([018](018_non_overlapping_intervals.md)); Car Pooling (LeetCode 1094, Practice Q3).

---

## 10. Complexity Analysis

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Brute force (count at each start) | `O(n²)` | `O(1)` | `n` candidate moments × `n` meetings each. |
| Sort + min-heap (optimized) | `O(n log n)` | `O(n)` | Sorting is `O(n log n)`; each of the `n` heap operations is `O(log n)`. The heap holds up to `n` end times (all meetings overlapping). |
| Sorted starts/ends, two pointers | `O(n log n)` | `O(n)` | Two sorts plus one linear pass; two extra lists of length `n`. |

---

## 11. Edge Cases

| Case | Input | Expected result | Why |
|---|---|---|---|
| One meeting | `[[1,5]]` | `1` | One room. |
| All identical | `[[1,5],[1,5],[1,5]]` | `3` | All run at the same time. |
| Back-to-back chain | `[[1,5],[5,10],[10,15]]` | `1` | Each starts exactly when the previous ends. |
| One long meeting with short ones inside | `[[1,10],[2,3],[4,5]]` | `2` | The short ones can share the second room. |
| Overlap with handovers | `[[1,4],[2,5],[4,6],[5,7]]` | `2` | Never more than two at once. |
| Unsorted input | `[[9,10],[4,9],[4,17]]` | `2` | Sorting fixes the order; `[9,10]` reuses the room of `[4,9]`. |

---

## 12. Common Mistakes and Debugging

1. **Using `<` instead of `<=`** in `end_times[0] <= start`. Back-to-back meetings then each get a new room: `[[1,5],[5,10],[10,15]]` returns 3 instead of 1.
2. **Forgetting to sort by start.** Meetings must be handled in time order; otherwise a room might be "reused" before the earlier meeting even happened.
3. **Looking at the wrong room.** Comparing with the most recently opened room (e.g. a plain list's last element) or using a max-heap checks a room that may still be busy while another room is already free, so you open rooms you don't need. Always check the **earliest** end time.
4. **Returning the number of reuses or the heap's top** instead of `len(end_times)`.
5. **Two-pointer version: sorting starts and ends together as pairs.** They must be sorted **independently**; the trick is that we only need *counts* of ended meetings.

**Debugging tip:** print `start, end_times` at each step and compare with the dry-run table.

---

## 13. Practice Questions

**Q1. Why is it enough to compare with only the smallest end time in the heap?**

<details><summary>Hint</summary>If the room that frees up earliest is still busy, what about the others?</summary></details>

**Answer:** The heap's top is the earliest end time among all open rooms. If even that room is still busy at `start` (`end_times[0] > start`), every other room ends later and is also busy, so a new room is required. If it is free, reusing it keeps the room count unchanged — reusing any other free room couldn't do better.

**Q2. Solve it with an explicit sweep line: create `(time, +1)` for each start and `(time, -1)` for each end, sort, and track the running count.**

<details><summary>Hint</summary>At equal times, process ends (`-1`) before starts (`+1`) — sorting tuples does this automatically because `-1 < +1`.</summary></details>

**Answer:**

```python
def min_rooms_sweep(intervals):
    events = []
    for start, end in intervals:
        events.append((start, 1))
        events.append((end, -1))
    events.sort()                    # (t, -1) comes before (t, +1)
    running = best = 0
    for _, change in events:
        running += change
        best = max(best, running)
    return best


assert min_rooms_sweep([[0, 30], [5, 10], [15, 20]]) == 2
assert min_rooms_sweep([[7, 10], [2, 4]]) == 1
assert min_rooms_sweep([[1, 5], [5, 10], [10, 15]]) == 1
assert min_rooms_sweep([[1, 5], [1, 5], [1, 5]]) == 3
```

**Q3. "Car Pooling" (LeetCode 1094): `trips[i] = [passengers, from, to]`, the car only drives forward, and passengers leave at `to`. Can a car with `capacity` seats complete all trips?**

<details><summary>Hint</summary>It's the same sweep line, but each event adds or removes `passengers` instead of 1. Check the running total never exceeds `capacity`.</summary></details>

**Answer:**

```python
def car_pooling(trips, capacity):
    events = []
    for passengers, start, end in trips:
        events.append((start, passengers))
        events.append((end, -passengers))
    events.sort()                    # drop-offs (negative) before pick-ups at the same place
    load = 0
    for _, change in events:
        load += change
        if load > capacity:
            return False
    return True


assert car_pooling([[2, 1, 5], [3, 3, 7]], 4) is False
assert car_pooling([[2, 1, 5], [3, 3, 7]], 5) is True
assert car_pooling([[2, 1, 5], [3, 5, 7]], 3) is True
```

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** Sort by start + min-heap of end times (or sweep line over sorted starts/ends).
- **Key idea:** for each meeting in start order, reuse the earliest-ending room if `end_times[0] <= start`, else open a new room; the answer is `len(heap)` = peak overlap.
- **Time:** `O(n log n)`.
- **Auxiliary space:** `O(n)`.
- **One-line memory hook:** *"Check the sticky note that frees up first; if it's still busy, open a new room."*

### Completion checklist

- [x] Problem requirements written from the well-known signature and commonly published description
- [ ] Examples and constraints verified against official statement — **not done**: this is a LeetCode Premium problem and the official statement could not be fetched; the examples and constraints are the commonly published ones
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force solution written and tested
- [x] Optimized Python solution written and tested (`tools/tests/p020.py`), including the two-pointer alternative
- [x] Line-by-line explanation written
- [x] Dry run completed with the commonly published examples
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
