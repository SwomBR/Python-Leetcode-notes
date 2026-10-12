# 065. Jump Game

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Jump Game |
| **LeetCode number** | 55 |
| **Topic (source list)** | Dynamic Programming |
| **Also uses** | Greedy, Array |
| **Difficulty** | Medium |
| **LeetCode URL** | <https://leetcode.com/problems/jump-game/> |
| **Pattern** | Greedy "farthest reach" (DP gives an `O(n²)` solution; greedy improves it to `O(n)`) |

---

## 2. Problem Explanation

### What are we given?

`nums` — a list of non-negative integers. You stand on index `0`. The value `nums[i]` is the **longest jump** you may make from index `i`.

### What must we return?

`True` if you can get to the **last index** (`len(nums) - 1`), otherwise `False`.

### The rules

1. From index `i` you may jump forward by **any** number of steps from `1` up to `nums[i]` — not only exactly `nums[i]`.
2. A value of `0` means you cannot move from that spot.
3. The goal is to reach index `n - 1`. If some index's maximum jump would carry you *beyond* the end, that is still a success, because you can simply choose the shorter jump that lands exactly on index `n - 1`.
4. If the list has one element, you are already on the last index → `True`.

### Examples

**Example 1**

```text
Input:  nums = [2, 3, 1, 1, 4]
Output: true
```

Jump 1 step from index 0 to index 1, then 3 steps from index 1 to index 4 (the last index).

**Example 2**

```text
Input:  nums = [3, 2, 1, 0, 4]
Output: false
```

Whatever you do, you end up at index 3, whose value is 0. You can never get past it to index 4.

### Constraints

- `1 <= nums.length <= 10^4`
- `0 <= nums[i] <= 10^5`

There is no follow-up in the official statement.

---

## 3. Everyday Analogy

> **Explain it like I'm five**

You're crossing a river on stepping stones. Each stone has a number painted on it: how many stones ahead you can hop **at most** from there.

Instead of trying every possible hop sequence, you carry a **flag** that marks "the farthest stone I know I can reach". You walk forward stone by stone:

- If the stone you're standing on is **beyond** the flag, you could never have got here — you're stuck. Answer: **no**.
- Otherwise, look at the number on this stone: maybe it lets you move the flag further. Move the flag if so.
- If the flag ever reaches the last stone, answer: **yes**.

Why is one flag enough? Because if you can reach a far stone, you can also reach every stone before it (just take shorter hops). So "what can I reach?" is always "everything up to the flag".

---

## 4. Step-by-Step Logic

### First, the DP view (the source lists this under DP)

1. **State definition.** `reachable[i]` = `True` if index `i` can be reached from index `0`.
2. **Recurrence.** `reachable[j]` is `True` if some earlier `i` is reachable and `i + nums[i] >= j`.
3. **Base case.** `reachable[0] = True`.
4. **Iteration order.** Left to right: when we're at `i`, all ways into `i` came from smaller indices.
5. **Answer location.** `reachable[n - 1]`.

This is correct but can cost `O(n²)` — each reachable index may mark up to `n` later indices.

### Then, the key observation that makes greedy valid

6. **The reachable indices always form a prefix** `0, 1, …, farthest`. Proof by induction: index 0 is reachable. Suppose every index up to `farthest` is reachable. If some reachable `i` has `i + nums[i] = R`, then from `i` you can jump **any** length `1..nums[i]`, so every index from `i + 1` to `R` is reachable too — no gaps appear.
7. **So the whole DP table is described by a single number**, `farthest`. Instead of a list of booleans, keep `farthest = max(farthest, i + nums[i])` while scanning.
8. **Getting stuck:** if we arrive at an `i` with `i > farthest`, then `i` (and everything after it) is unreachable → `False`.
9. **Success:** once `farthest >= n - 1`, the last index is reachable → `True`.

### The backwards view (another greedy)

10. Call an index **good** if you can reach the end from it. The last index is good. Moving right to left, index `i` is good if it can jump to the **leftmost good index found so far** (`i + nums[i] >= goal`). If yes, `i` becomes the new `goal`. The answer is `goal == 0`. Checking only the leftmost good index is enough for the same "no gaps" reason.

---

## 5. Brute-Force Solution

### Algorithm 1 (plain recursion)

`can_reach_end(i)`: if `i` is the last index → `True`; otherwise try every jump length `1..nums[i]` and recurse.

```python
from typing import List


class Solution:
    def canJump(self, nums: List[int]) -> bool:
        last = len(nums) - 1

        def can_reach_end(i: int) -> bool:
            if i >= last:
                return True
            for step in range(1, nums[i] + 1):      # try every jump length
                if can_reach_end(i + step):
                    return True
            return False

        return can_reach_end(0)
```

- **Correct:** it explores every possible sequence of jumps.
- **Time:** exponential in the worst case. When the answer is `False`, it explores every jump sequence before giving up. Example 2 generalised, `[k, k-1, …, 2, 1, 0, x]`, lets every index before the 0 jump to any later index up to the 0, so the recursion visits all `2^k` subsets of stepping points. It would **time out** on LeetCode.
- **Auxiliary space:** `O(n)` recursion depth (and `n = 10^4` would also exceed Python's default recursion limit of 1000).

### The bridge — memoization

`can_reach_end(i)` depends only on `i`, so cache it: each index is solved once, but each solution may try up to `nums[i]` jumps.

```python
from functools import lru_cache
from typing import List


class Solution:
    def canJump(self, nums: List[int]) -> bool:
        last = len(nums) - 1

        @lru_cache(maxsize=None)
        def can_reach_end(i: int) -> bool:
            if i >= last:
                return True
            return any(can_reach_end(i + step) for step in range(1, nums[i] + 1))

        return can_reach_end(0)
```

`O(n²)` time (capping each loop at the end of the array), `O(n)` space — but still deep recursion for large `n`.

### Algorithm 2 (bottom-up DP, `O(n²)`)

Mark reachable indices from left to right.

```python
from typing import List


class Solution:
    def canJump(self, nums: List[int]) -> bool:
        n = len(nums)
        reachable = [False] * n
        reachable[0] = True                       # we start here
        for i in range(n):
            if not reachable[i]:
                continue                          # can't stand here, can't jump from here
            for j in range(i + 1, min(n, i + nums[i] + 1)):
                reachable[j] = True               # every shorter jump is allowed
        return reachable[n - 1]
```

- **Time:** `O(n²)` in the worst case: each index marks up to `n - 1` others. With `n = 10^4` that's up to ~5 × 10^7 inner steps — far too slow in Python. Note that the work is `O(n · min(n, max(nums)))`.
- **Auxiliary space:** `O(n)` for `reachable`.

---

## 6. Optimized Solution

### Idea — greedy farthest reach

The DP table `reachable` is always `True` for a prefix and `False` after it (see Step 6), so store only the boundary `farthest`.

### Algorithm

1. `farthest = 0`.
2. For each index `i` with jump length `jump`:
   - If `i > farthest` → return `False` (we can't even stand on `i`).
   - `farthest = max(farthest, i + jump)`.
   - If `farthest >= n - 1` → return `True`.
3. Return `True` (only reached for safety; the loop's last iteration always decides).

### Python code (LeetCode-ready)

```python
from typing import List


class Solution:
    def canJump(self, nums: List[int]) -> bool:
        last = len(nums) - 1
        farthest = 0                              # farthest index we can reach so far

        for i, jump in enumerate(nums):
            if i > farthest:                      # index i is beyond our reach
                return False
            farthest = max(farthest, i + jump)    # jumping from i may extend the reach
            if farthest >= last:
                return True

        return True
```

### Alternative greedy — walk backwards with a goal

```python
from typing import List


class Solution:
    def canJump(self, nums: List[int]) -> bool:
        goal = len(nums) - 1                      # leftmost index known to reach the end
        for i in range(len(nums) - 2, -1, -1):
            if i + nums[i] >= goal:               # from i we can land on the goal
                goal = i
        return goal == 0
```

Both are `O(n)` time and `O(1)` extra space.

---

## 7. Line-by-Line Explanation

(Farthest-reach greedy)

| Line | What it does | Why |
|---|---|---|
| `last = len(nums) - 1` | Index we must reach. | Saves recomputing it. |
| `farthest = 0` | Reach before any jump: only index 0. | We start on index 0. |
| `for i, jump in enumerate(nums):` | Scans indices left to right. | Every way into `i` comes from a smaller index, so `farthest` already accounts for all of them. |
| `if i > farthest: return False` | Detects a gap we can't cross. | Since reachable indices form a prefix `0..farthest`, an index past it is unreachable, and so is everything after it. |
| `farthest = max(farthest, i + jump)` | Updates the reach. | `i` is reachable, and from `i` we can land anywhere up to `i + jump`. |
| `if farthest >= last: return True` | Early success. | The last index is inside the reachable prefix. Also covers `n = 1` immediately (`0 >= 0`). |
| `return True` | Fallback. | Never actually needed: at `i = last` either `i > farthest` (False) or `farthest >= last` (True). It keeps the function total. |

**Why greedy is safe here (exchange argument in one sentence):** jumping shorter is always allowed, so the only fact that matters is the furthest point reachable — any plan that reaches some index can be matched by the greedy reach, which never misses an index inside it.

---

## 8. Dry Run

**Input:** `nums = [2, 3, 1, 1, 4]` (Example 1), `last = 4`.

| `i` | `jump` | `i > farthest`? | `i + jump` | `farthest` after | `farthest >= 4`? |
|---|---|---|---|---|---|
| 0 | 2 | 0 > 0? no | 2 | 2 | no |
| 1 | 3 | 1 > 2? no | 4 | 4 | **yes → return True** |

**Result:** `True` ✅

**Second dry run:** `nums = [3, 2, 1, 0, 4]` (Example 2), `last = 4`.

| `i` | `jump` | `i > farthest`? | `i + jump` | `farthest` after | `farthest >= 4`? |
|---|---|---|---|---|---|
| 0 | 3 | no | 3 | 3 | no |
| 1 | 2 | no | 3 | 3 | no |
| 2 | 1 | no | 3 | 3 | no |
| 3 | 0 | no | 3 | 3 | no |
| 4 | 4 | **4 > 3 → return False** | — | — | — |

**Result:** `False` ✅ — every path tops out at index 3.

**DP table view of Example 2** (the `O(n²)` solution):

| After processing `i` | `reachable` |
|---|---|
| start | `[T, F, F, F, F]` |
| 0 (jump 3) | `[T, T, T, T, F]` |
| 1 (jump 2) | `[T, T, T, T, F]` |
| 2 (jump 1) | `[T, T, T, T, F]` |
| 3 (jump 0) | `[T, T, T, T, F]` |
| 4 (not reachable, skipped) | `[T, T, T, T, F]` |

The `True`s always form a prefix — exactly what the single number `farthest = 3` encodes. Answer `reachable[4] = False` ✅.

**Backwards greedy on Example 1:** `goal = 4`; `i = 3`: `3 + 1 >= 4` → `goal = 3`; `i = 2`: `2 + 1 >= 3` → `goal = 2`; `i = 1`: `1 + 3 >= 2` → `goal = 1`; `i = 0`: `0 + 2 >= 1` → `goal = 0`. `goal == 0` → `True` ✅.

---

## 9. Concepts, Data Structures, and Patterns

- **DP recipe (reachability):** state `reachable[i]`, recurrence "some reachable `i` with `i + nums[i] >= j`", base `reachable[0] = True`, left-to-right, answer `reachable[n-1]`.
- **Greedy as a collapsed DP:** when a DP table always has a simple shape (here: a `True` prefix), store only the shape's boundary. This is the same idea as Kadane's algorithm in [../01_array/005_maximum_subarray.md](../01_array/005_maximum_subarray.md) collapsing a DP to one variable.
- **"Farthest reach" / interval extension:** keep extending a covered range while scanning — closely related to merging intervals ([../03_interval/017_merge_intervals.md](../03_interval/017_merge_intervals.md)).
- **Monotonic goal (backwards greedy):** keep the leftmost "good" index; any index that reaches it is good.
- **Recursion → memoization → tabulation → greedy:** this problem shows the full ladder of optimizations.
- **Related problems:** Jump Game II (LeetCode 45, fewest jumps — practice Q2), Jump Game III (LeetCode 1306 — practice Q3), [055_climbing_stairs.md](055_climbing_stairs.md) (counting rather than reachability).

---

## 10. Complexity Analysis

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Plain recursion | Exponential (up to about `2^n`) | `O(n)` | Re-explores the same indices through different jump sequences; depth up to `n`. |
| Memoization | `O(n²)` | `O(n)` | `n` states, each trying up to `n` jumps (capped at the array end); cache + stack. |
| Bottom-up DP | `O(n²)` | `O(n)` | Each reachable index marks up to `n` later indices. |
| Greedy farthest reach (optimized) | `O(n)` | `O(1)` | One pass, one variable. |
| Backwards goal greedy | `O(n)` | `O(1)` | One pass from the right, one variable. |

---

## 11. Edge Cases

| Case | Example | Expected result | Why |
|---|---|---|---|
| Single element | `[0]` | `True` | Already standing on the last index. |
| Stuck at the start | `[0, 1]` | `False` | Can't move from index 0. |
| Zero at the end | `[1, 0]` | `True` | A 0 on the last index doesn't matter. |
| Jump over zeros | `[2, 0, 0]` | `True` | Index 0 jumps straight to index 2. |
| Zero blocks in the middle | `[1, 0, 1]` | `False` | Index 1 is a dead end. |
| Huge first jump | `[5, 0, 0, 0, 0, 0]` | `True` | `0 + 5 = 5 = last`. |
| Barrier after a few steps | `[1, 1, 0, 1]` | `False` | Reach stops at index 2. |

---

## 12. Common Mistakes and Debugging

1. **Thinking you must jump exactly `nums[i]`.** You may jump any length from 1 to `nums[i]`. With exact jumps, `[2, 3, 1, 1, 4]` would be a different problem.
2. **Forgetting the `i > farthest` check.** Without it, the loop happily extends `farthest` from unreachable indices: `[0, 5]` would wrongly return `True`.
3. **Checking `farthest > last` instead of `>=`.** `[1, 0]` reaches index 1 exactly, so `>` never fires; the code is then only rescued by the final `return True`. If you write the fallback as `return False` (a common habit), `[1, 0]` and `[0]` come out wrong.
4. **Treating a 0 as automatic failure.** `[2, 0, 0]` succeeds; a 0 only hurts if no earlier index can jump past it.
5. **Recursion depth.** The recursive versions crash on `n = 10^4` with the default recursion limit — another reason to use the iterative greedy.
6. **Using BFS/DP and timing out.** The `O(n²)` approaches are correct but too slow in Python for the largest inputs.

**Debugging tip:** print `i, jump, farthest` each iteration and compare with the dry-run tables.

---

## 13. Practice Questions

**Q1. Trace the greedy on `nums = [1, 1, 0, 1]`. What does it return?**

<details><summary>Hint</summary>Watch what happens to `farthest` at index 2.</summary></details>

**Answer:** `i = 0`: `farthest = 1`. `i = 1`: `farthest = 2`. `i = 2`: `farthest = max(2, 2 + 0) = 2`. `i = 3`: `3 > 2` → return `False`.

**Q2. Jump Game II (LeetCode 45): the end is guaranteed reachable; return the minimum number of jumps.**

<details><summary>Hint</summary>Think in "levels" like BFS: all indices reachable with `k` jumps form a window. When you pass the end of the current window, you must take another jump, and the next window ends at the farthest reach seen so far.</summary></details>

**Answer:**

```python
def min_jumps(nums):
    jumps = 0
    window_end = 0      # last index reachable with `jumps` jumps
    farthest = 0
    for i in range(len(nums) - 1):          # no jump needed from the last index
        farthest = max(farthest, i + nums[i])
        if i == window_end:                 # leaving the current level
            jumps += 1
            window_end = farthest
    return jumps


assert min_jumps([2, 3, 1, 1, 4]) == 2
assert min_jumps([2, 3, 0, 1, 4]) == 2
assert min_jumps([0]) == 0
assert min_jumps([1, 1, 1]) == 2
```

**Q3. Jump Game III (LeetCode 1306): from index `i` you may jump to `i + arr[i]` or `i - arr[i]`. Starting at `start`, can you reach any index whose value is 0?**

<details><summary>Hint</summary>Jumps go both ways now, so the "prefix" trick no longer works. Use BFS (or DFS) with a visited set.</summary></details>

**Answer:**

```python
from collections import deque


def can_reach_zero(arr, start):
    seen = {start}
    queue = deque([start])
    while queue:
        i = queue.popleft()
        if arr[i] == 0:
            return True
        for j in (i + arr[i], i - arr[i]):
            if 0 <= j < len(arr) and j not in seen:
                seen.add(j)
                queue.append(j)
    return False


assert can_reach_zero([4, 2, 3, 0, 3, 1, 2], 5) is True
assert can_reach_zero([4, 2, 3, 0, 3, 1, 2], 0) is True
assert can_reach_zero([3, 0, 2, 1, 2], 2) is False
```

**Q4. Why doesn't the greedy need to remember *which* jumps were taken?**

<details><summary>Hint</summary>The question is yes/no, and reachability has a special shape.</summary></details>

**Answer:** The question only asks *whether* the end is reachable, and the set of reachable indices is always `0..farthest` with no gaps. One number describes that set completely, so no path information is needed.

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** Greedy farthest reach (a DP whose table is always a `True` prefix).
- **Key idea:** `if i > farthest: False`; `farthest = max(farthest, i + nums[i])`; `if farthest >= n-1: True`.
- **DP version:** `reachable[j] = any(reachable[i] and i + nums[i] >= j)` — `O(n²)`.
- **Time:** `O(n)`. **Auxiliary space:** `O(1)`.
- **One-line memory hook:** *"Carry the flag as far as any stone lets you — if you ever walk past the flag, you're stuck."*

### Completion checklist

- [x] Problem requirements verified
- [x] Examples and constraints verified
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force recursion, memoized recursion and `O(n²)` DP written and tested
- [x] Optimized greedy (forward farthest reach and backwards goal) written and tested (`tools/tests/p065.py`)
- [x] Line-by-line explanation written
- [x] Dry run completed with real examples (greedy and DP table)
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
