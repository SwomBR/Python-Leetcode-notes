# 005. Maximum Subarray

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Maximum Subarray |
| **LeetCode number** | 53 |
| **Topic (source list)** | Array |
| **Also uses** | Dynamic Programming, Divide and Conquer |
| **Difficulty** | Medium |
| **LeetCode URL** | <https://leetcode.com/problems/maximum-subarray/> |
| **Pattern** | Kadane's algorithm |

---

## 2. Problem Explanation

### What are we given?

`nums` — a list of integers (it can contain negatives).

### What must we return?

The **largest possible sum** of a **subarray**.

A **subarray** is a **contiguous, non-empty** slice of the list — elements that sit next to each other, with at least one element. For `[4, -1, 2]`:
- `[4, -1]` and `[-1, 2]` and `[4, -1, 2]` are subarrays.
- `[4, 2]` is **not** (it skips `-1`).
- `[]` is **not allowed** (must be non-empty).

### Examples

**Example 1**

```text
Input:  nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
Output: 6
```

The subarray `[4, -1, 2, 1]` sums to 6, and no other subarray beats it.

**Example 2**

```text
Input:  nums = [1]
Output: 1
```

The only subarray is `[1]`.

**Example 3**

```text
Input:  nums = [5, 4, -1, 7, 8]
Output: 23
```

The whole array sums to 23. Including the `-1` is worth it because it connects `5, 4` with `7, 8`.

### Constraints

- `1 <= nums.length <= 10^5`
- `-10^4 <= nums[i] <= 10^4`

**Follow-up:** If you've found the `O(n)` solution, try a **divide and conquer** solution as well.

---

## 3. Everyday Analogy

> **Explain it like I'm five**

You're walking down a path picking up coins. Some spots give you coins (positive numbers) and some spots have a troll that takes coins away (negative numbers). You must collect from **one unbroken stretch** of the path, and you want to finish the stretch with the most coins possible.

As you walk, you keep a bag with your current stretch's total. At each spot you ask:

> "Is my bag helping me or hurting me?"

If your bag has gone **negative**, it's a burden — you'd be better off **dropping it** and starting a fresh stretch right here. Otherwise you keep it and add the current spot.

You also write down the **best bag total you've ever had**. At the end of the path, that number is the answer.

---

## 4. Step-by-Step Logic

1. **Think about where a subarray ends.** Every subarray ends at some index `i`.
2. **Define `best_ending_here`** = the largest sum of a subarray that **ends exactly at `i`**.
3. **Recurrence.** A subarray ending at `i` either:
   - is just `[nums[i]]` alone, **or**
   - extends the best subarray ending at `i - 1`.

   So `best_ending_here(i) = max(nums[i], best_ending_here(i-1) + nums[i])`.
4. **Intuition:** if the previous running sum is negative, adding it only makes things worse, so start fresh at `nums[i]`.
5. **The overall answer** is the maximum of `best_ending_here` over all `i`.
6. **Only the previous value is needed**, so two variables (`current`, `best`) suffice.
7. **All-negative input:** starting `best` at `nums[0]` (not 0) makes sure we return the largest single element, because subarrays must be non-empty.

---

## 5. Brute-Force Solution

### Algorithm

For every start index `i`, extend the end index `j` one step at a time, keeping a running sum, and track the largest sum seen.

### Python code

```python
from typing import List


class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        n = len(nums)
        best = nums[0]
        for start in range(n):
            running = 0
            for end in range(start, n):
                running += nums[end]          # sum of nums[start..end]
                best = max(best, running)
        return best
```

### Explanation

- Each pair `(start, end)` defines one subarray.
- Instead of re-adding the whole slice each time (`O(n³)`), we extend the running sum by one element (`O(n²)`).
- `best` starts at `nums[0]` so an all-negative list is handled correctly.

### Complexity

- **Time:** `O(n²)` — about 5 billion steps for `n = 10^5`, which **times out**.
- **Auxiliary space:** `O(1)`.

---

## 6. Optimized Solution

### Idea — Kadane's algorithm

Keep the best sum of a subarray ending at the current position (`current`) and the best sum seen anywhere (`best`).

### Algorithm

1. `current = best = nums[0]`.
2. For each `num` in `nums[1:]`:
   - `current = max(num, current + num)` — extend or restart.
   - `best = max(best, current)`.
3. Return `best`.

### Python code (LeetCode-ready)

```python
from typing import List


class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        current = best = nums[0]

        for num in nums[1:]:
            current = max(num, current + num)  # extend the run or start fresh
            best = max(best, current)

        return best
```

### Follow-up: divide and conquer (`O(n log n)`)

```python
from typing import List


class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        def solve(lo: int, hi: int) -> int:
            if lo == hi:
                return nums[lo]
            mid = (lo + hi) // 2

            # Best sum crossing the middle: best suffix of the left half
            # plus best prefix of the right half.
            left_best, total = float("-inf"), 0
            for i in range(mid, lo - 1, -1):
                total += nums[i]
                left_best = max(left_best, total)
            right_best, total = float("-inf"), 0
            for i in range(mid + 1, hi + 1):
                total += nums[i]
                right_best = max(right_best, total)

            return max(solve(lo, mid), solve(mid + 1, hi), left_best + right_best)

        return solve(0, len(nums) - 1)
```

The best subarray is either entirely in the left half, entirely in the right half, or crosses the middle. Each level of recursion does `O(n)` work across `O(log n)` levels → `O(n log n)` time, `O(log n)` recursion stack.

---

## 7. Line-by-Line Explanation

(Kadane's algorithm)

| Line | What it does | Why |
|---|---|---|
| `current = best = nums[0]` | Both start at the first element. | The best subarray ending at index 0 is `[nums[0]]`. Starting at `nums[0]` (not 0) handles all-negative lists. |
| `for num in nums[1:]:` | Visits the remaining elements. | Index 0 is already processed. (`nums[1:]` makes a copy; `for i in range(1, len(nums))` avoids it.) |
| `current = max(num, current + num)` | Chooses between starting a new subarray at `num` or extending the previous one. | If `current` is negative, `current + num < num`, so we restart. |
| `best = max(best, current)` | Records the best subarray seen so far. | The answer could end at any index. |
| `return best` | Returns the overall maximum. | — |

---

## 8. Dry Run

**Input:** `nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]`

| Index | `num` | `current + num` | `current = max(num, current + num)` | Decision | `best` |
|---|---|---|---|---|---|
| 0 | -2 | — | -2 | start | -2 |
| 1 | 1 | -2 + 1 = -1 | 1 | restart (old run was negative) | 1 |
| 2 | -3 | 1 + (-3) = -2 | -2 | extend | 1 |
| 3 | 4 | -2 + 4 = 2 | 4 | restart | 4 |
| 4 | -1 | 4 + (-1) = 3 | 3 | extend | 4 |
| 5 | 2 | 3 + 2 = 5 | 5 | extend | 5 |
| 6 | 1 | 5 + 1 = 6 | 6 | extend | **6** |
| 7 | -5 | 6 + (-5) = 1 | 1 | extend | 6 |
| 8 | 4 | 1 + 4 = 5 | 5 | extend | 6 |

**Result:** `6` ✅ (the run that restarted at index 3 and reached 6 at index 6 is `[4, -1, 2, 1]`)

**All-negative check:** `nums = [-3, -1, -2]` → `current`: -3, then `max(-1, -4) = -1`, then `max(-2, -3) = -2`; `best` ends at `-1` ✅.

---

## 9. Concepts, Data Structures, and Patterns

- **Kadane's algorithm:** a one-pass dynamic programming technique for maximum-sum contiguous subarrays.
- **Dynamic programming (DP):** break the problem into "best answer ending at `i`" subproblems; each depends only on the previous one, so the DP table collapses to one variable.
- **Greedy restart rule:** a negative running prefix can never help a future subarray, so it's dropped.
- **Divide and conquer:** split, solve halves, combine with the crossing case (follow-up).
- **Prefix-sum view:** the sum of `nums[i..j]` equals `prefix[j+1] - prefix[i]`. Maximizing it means, for each `j`, subtracting the smallest earlier prefix — the same "running minimum" idea as [002_best_time_to_buy_and_sell_stock.md](002_best_time_to_buy_and_sell_stock.md).
- **Related problems:** Maximum Product Subarray ([006_maximum_product_subarray.md](006_maximum_product_subarray.md)) adapts Kadane to products; Maximum Sum Circular Subarray (LeetCode 918).

---

## 10. Complexity Analysis

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Brute force | `O(n²)` | `O(1)` | Every start/end pair with a running sum. |
| Kadane (optimized) | `O(n)` | `O(1)` | One pass, two variables. (Iterating over `nums[1:]` creates an `O(n)` copy; use `range(1, len(nums))` for strict `O(1)`.) |
| Divide and conquer | `O(n log n)` | `O(log n)` | `O(n)` combine work per level, `log n` levels; recursion stack depth `log n`. |

---

## 11. Edge Cases

| Case | Example | Expected result | Why |
|---|---|---|---|
| Single element | `[1]` | `1` | The only subarray. |
| All negative | `[-3, -1, -2]` | `-1` | Must pick at least one element; pick the largest. |
| All positive | `[5, 4, 7]` | `16` | Take everything. |
| Negative bridge worth crossing | `[5, 4, -1, 7, 8]` | `23` | `-1` connects two strong runs. |
| Zero with negatives | `[0, -1]` | `0` | `[0]` beats `[-1]` and `[0, -1]`. |
| Single negative | `[-5]` | `-5` | Non-empty rule. |

---

## 12. Common Mistakes and Debugging

1. **Starting `best` at 0.** For `[-3, -1, -2]` this returns 0, but an empty subarray isn't allowed. Start at `nums[0]`.
2. **Resetting `current` to 0 in the wrong place.** Writing `current = max(0, current + num)` and *then* `best = max(best, current)` returns 0 for `[-3, -1, -2]`, because `best` only ever sees the reset value. The reset-to-zero style is correct only in this order: `current += num`, then `best = max(best, current)`, then `if current < 0: current = 0`. The form `current = max(num, current + num)` avoids the trap entirely.
3. **Updating `best` before `current`.** Then `best` lags one element behind and can miss the last element.
4. **Confusing subarray with subsequence.** Subsequences may skip elements; subarrays may not.
5. **Using `sum(nums[i:j])` inside two loops.** That's `O(n³)`.

**Debugging tip:** print `num, current, best` each step; compare with the dry-run table.

---

## 13. Practice Questions

**Q1. What does Kadane return for `[2, -1, 2, -10, 3]`?**

<details><summary>Hint</summary>Track `current` step by step; watch what happens at -10.</summary></details>

**Answer:** `current` goes 2 → 1 → 3 → -7 → 3 (restart, since `max(3, -7 + 3) = 3`). `best` = 3. The answer is `3` (from `[2, -1, 2]` or `[3]`).

**Q2. Return the start and end indices of the maximum subarray (first one found).**

<details><summary>Hint</summary>Remember where the current run started; when `best` improves, save `(run_start, i)`.</summary></details>

**Answer:**

```python
def max_subarray_indices(nums):
    current = best = nums[0]
    run_start = 0
    best_range = (0, 0)
    for i in range(1, len(nums)):
        if nums[i] > current + nums[i]:   # restarting is better
            current = nums[i]
            run_start = i
        else:
            current += nums[i]
        if current > best:
            best = current
            best_range = (run_start, i)
    return best, best_range


assert max_subarray_indices([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == (6, (3, 6))
assert max_subarray_indices([-3, -1, -2]) == (-1, (1, 1))
```

**Q3. Solve "Maximum Sum Circular Subarray" (the end wraps around to the start).**

<details><summary>Hint</summary>A wrapping subarray = total sum − a minimum (non-wrapping) subarray. Be careful when every number is negative.</summary></details>

**Answer:**

```python
def max_circular_subarray(nums):
    cur_max = best_max = nums[0]
    cur_min = best_min = nums[0]
    for num in nums[1:]:
        cur_max = max(num, cur_max + num)
        best_max = max(best_max, cur_max)
        cur_min = min(num, cur_min + num)
        best_min = min(best_min, cur_min)
    if best_max < 0:          # all negative: wrapping would mean taking nothing
        return best_max
    return max(best_max, sum(nums) - best_min)


assert max_circular_subarray([5, -3, 5]) == 10
assert max_circular_subarray([-3, -2, -3]) == -2
assert max_circular_subarray([1, -2, 3, -2]) == 3
```

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** Kadane's algorithm (1-D DP).
- **Key idea:** `current = max(num, current + num)`; `best = max(best, current)`. Drop a negative running sum.
- **Time:** `O(n)`.
- **Auxiliary space:** `O(1)`.
- **One-line memory hook:** *"If your bag is a burden, drop it and start fresh."*

### Completion checklist

- [x] Problem requirements verified
- [x] Examples and constraints verified
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force solution written and tested
- [x] Optimized Python solution written and tested (`tools/tests/p005.py`), including the divide-and-conquer follow-up
- [x] Line-by-line explanation written
- [x] Dry run completed with a real example
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
