# 061. House Robber

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | House Robber |
| **LeetCode number** | 198 |
| **Topic (source list)** | Dynamic Programming |
| **Also uses** | Array, Recursion + Memoization |
| **Difficulty** | Medium |
| **LeetCode URL** | <https://leetcode.com/problems/house-robber/> |
| **Pattern** | 1-D DP: "take it or skip it" with two rolling variables |

---

## 2. Problem Explanation

### What are we given?

`nums` — a list of non-negative integers. `nums[i]` is the amount of money hidden in house `i`. The houses stand in a straight line along a street, in the order of the list.

### What must we return?

The **largest total amount of money** you can collect in one night.

### The rules

1. You may pick **any group of houses** to rob (including just one, or even none — but since money is never negative, robbing more never hurts unless a rule forbids it).
2. **You may not rob two houses that are next to each other.** Neighbouring houses share an alarm, so robbing house `i` and house `i + 1` on the same night is forbidden.
3. Houses that are further apart (like house 0 and house 2) are fine.
4. You only return the **amount**, not which houses were chosen.

### Examples

**Example 1**

```text
Input:  nums = [1, 2, 3, 1]
Output: 4
```

Rob house 0 (money 1) and house 2 (money 3): `1 + 3 = 4`. Robbing houses 1 and 3 gives only `2 + 1 = 3`.

**Example 2**

```text
Input:  nums = [2, 7, 9, 3, 1]
Output: 12
```

Rob houses 0, 2 and 4: `2 + 9 + 1 = 12`. No two of them are neighbours.

### Constraints

- `1 <= nums.length <= 100`
- `0 <= nums[i] <= 400`

There is no follow-up in the official statement.

---

## 3. Everyday Analogy

> **Explain it like I'm five**

You walk down a row of cookie jars. Each jar has some cookies inside. There is one rule from Mum: **if you take from a jar, you must leave the very next jar alone.**

At each jar you have only two choices:

- **Skip it** — then you keep whatever best haul you had after the previous jar.
- **Take it** — then you must *not* have taken the previous jar, so you add this jar's cookies to the best haul you had **two jars ago**.

You pick whichever choice gives more cookies, and you write that number on a sticky note. By the time you reach the last jar, the sticky note shows the best possible haul. You only ever need to remember two sticky notes: "best up to the last jar" and "best up to the jar before that".

---

## 4. Step-by-Step Logic

We follow the **DP recipe**.

1. **Look at one house and ask what choices exist.** For the last house `i` there are two options: rob it or don't.
2. **State definition.** Let `dp[i]` = the most money you can get from **houses `0..i` only** (the first `i + 1` houses).
3. **Recurrence.**
   - Skip house `i` → the best is `dp[i - 1]`.
   - Rob house `i` → house `i - 1` is forbidden, so the best is `dp[i - 2] + nums[i]`.

   So `dp[i] = max(dp[i - 1], dp[i - 2] + nums[i])`.
4. **Base cases.** `dp[0] = nums[0]` (only one house). `dp[1] = max(nums[0], nums[1])` (two neighbours — rob the richer one). A neat trick: pretend `dp[-1] = dp[-2] = 0` ("no houses → no money"); then the same formula covers every index.
5. **Iteration order.** `dp[i]` needs `dp[i - 1]` and `dp[i - 2]`, so fill from left to right.
6. **Where is the answer?** `dp[n - 1]` — the best using all houses.
7. **Shrink the memory.** Each step looks back only two places, so two variables (`prev2`, `prev1`) replace the whole table.

**Why not a greedy rule like "rob every other house"?** For `[2, 1, 1, 2]`, taking even indices gives `2 + 1 = 3` and odd indices give `1 + 2 = 3`, but the best is houses 0 and 3: `2 + 2 = 4`. Gaps can be longer than one house, so we need DP to consider every possibility.

---

## 5. Brute-Force Solution

### Algorithm (plain recursion)

Define `best_from(i)` = the most money obtainable from houses `i, i+1, …, n-1`.

- If `i >= n`, there are no houses left → `0`.
- Otherwise choose the better of:
  - skip house `i` → `best_from(i + 1)`,
  - rob house `i` → `nums[i] + best_from(i + 2)` (jump over the neighbour).

### Python code

```python
from typing import List


class Solution:
    def rob(self, nums: List[int]) -> int:
        n = len(nums)

        def best_from(i: int) -> int:
            if i >= n:                     # no houses left
                return 0
            skip = best_from(i + 1)
            take = nums[i] + best_from(i + 2)
            return max(skip, take)

        return best_from(0)
```

### Explanation

- The recursion literally tries **every** valid plan: at each house it branches into "skip" and "take".
- Taking house `i` jumps to `i + 2`, which is exactly how the "no neighbours" rule is enforced.
- It is correct, but it recomputes the same subproblems again and again. For example `best_from(3)` is called three separate times: via `0 → 1 → 2 → 3` (skip, skip, skip), via `0 → 1 → 3` (skip house 0, rob house 1) and via `0 → 2 → 3` (rob house 0, skip house 2). The call tree repeats work exactly like naive Fibonacci.

### Complexity

- **Time:** the number of calls `T(n) = T(n-1) + T(n-2) + 1` grows like the Fibonacci numbers, about `1.618^n`, i.e. exponential (`O(2^n)` is a safe upper bound). For `n = 100` that is roughly `10^21` calls — it would **time out** on LeetCode.
- **Auxiliary space:** `O(n)` for the recursion stack (depth up to `n`).

### The bridge — memoization (top-down DP)

There are only `n + 2` different values of `i`, so we can **cache** each answer the first time we compute it. Same code, one decorator:

```python
from functools import lru_cache
from typing import List


class Solution:
    def rob(self, nums: List[int]) -> int:
        n = len(nums)

        @lru_cache(maxsize=None)
        def best_from(i: int) -> int:
            if i >= n:
                return 0
            return max(best_from(i + 1), nums[i] + best_from(i + 2))

        return best_from(0)
```

Now each `best_from(i)` is computed once: `O(n)` time and `O(n)` space (cache + recursion stack). Turning this around and filling the values from the other end gives the bottom-up solution below.

---

## 6. Optimized Solution

### Idea — bottom-up DP with two rolling variables

Walk the houses left to right. Keep:

- `prev1` = best total using the houses seen so far (that is `dp[i - 1]`),
- `prev2` = best total using all houses except the most recent one (that is `dp[i - 2]`).

### Algorithm

1. `prev2 = prev1 = 0` (no houses yet → no money).
2. For each amount `money` in `nums`:
   - `current = max(prev1, prev2 + money)` — skip this house, or rob it on top of the total from two houses back.
   - Shift: `prev2, prev1 = prev1, current`.
3. Return `prev1`.

### Python code (LeetCode-ready)

```python
from typing import List


class Solution:
    def rob(self, nums: List[int]) -> int:
        prev2 = 0  # best total up to two houses back  (dp[i-2])
        prev1 = 0  # best total up to the previous house (dp[i-1])

        for money in nums:
            current = max(prev1, prev2 + money)  # skip vs. rob this house
            prev2, prev1 = prev1, current

        return prev1
```

### Version with the full DP table (easier to inspect)

```python
from typing import List


class Solution:
    def rob(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 1:
            return nums[0]
        dp = [0] * n
        dp[0] = nums[0]
        dp[1] = max(nums[0], nums[1])
        for i in range(2, n):
            dp[i] = max(dp[i - 1], dp[i - 2] + nums[i])
        return dp[n - 1]
```

The table version uses `O(n)` memory; the rolling version keeps only the two numbers the recurrence actually needs.

---

## 7. Line-by-Line Explanation

(Rolling-variable solution)

| Line | What it does | Why |
|---|---|---|
| `prev2 = 0` | Best total "two houses back". | Before any house exists, the best you can do is 0. Acts as `dp[-2]`. |
| `prev1 = 0` | Best total "one house back". | Acts as `dp[-1]`. With both at 0, the first house gives `max(0, 0 + nums[0]) = nums[0]`, matching the base case. |
| `for money in nums:` | Visits each house once, left to right. | The recurrence needs earlier answers first. |
| `current = max(prev1, prev2 + money)` | The DP recurrence. | `prev1` = skip this house; `prev2 + money` = rob it (the previous house must then be skipped, so we build on the total from two back). |
| `prev2, prev1 = prev1, current` | Slides the two-value window forward. | Python evaluates the right side first, so the old `prev1` moves into `prev2` safely — no temporary variable needed. |
| `return prev1` | After the loop, `prev1` is `dp[n - 1]`. | The best total using all houses. |

**Why is `max` safe even though values can be 0?** All amounts are `>= 0`, so `dp` never decreases as we add houses; the formula naturally keeps the larger option.

---

## 8. Dry Run

**Input:** `nums = [2, 7, 9, 3, 1]` (Example 2)

| `i` | `money` | `prev2` (dp[i-2]) | `prev1` (dp[i-1]) | Skip = `prev1` | Rob = `prev2 + money` | `current` = dp[i] | Decision |
|---|---|---|---|---|---|---|---|
| 0 | 2 | 0 | 0 | 0 | 0 + 2 = 2 | 2 | rob house 0 |
| 1 | 7 | 0 | 2 | 2 | 0 + 7 = 7 | 7 | rob house 1 (instead of 0) |
| 2 | 9 | 2 | 7 | 7 | 2 + 9 = 11 | 11 | rob house 2 (on top of house 0) |
| 3 | 3 | 7 | 11 | 11 | 7 + 3 = 10 | 11 | skip house 3 |
| 4 | 1 | 11 | 11 | 11 | 11 + 1 = 12 | **12** | rob house 4 |

The DP table is `dp = [2, 7, 11, 11, 12]`.

**Result:** `12` ✅ (houses 0, 2, 4 → `2 + 9 + 1`)

**Second dry run:** `nums = [1, 2, 3, 1]` (Example 1)

| `i` | `money` | `prev2` | `prev1` | `max(prev1, prev2 + money)` | dp[i] |
|---|---|---|---|---|---|
| 0 | 1 | 0 | 0 | `max(0, 1)` | 1 |
| 1 | 2 | 0 | 1 | `max(1, 2)` | 2 |
| 2 | 3 | 1 | 2 | `max(2, 4)` | 4 |
| 3 | 1 | 2 | 4 | `max(4, 3)` | **4** |

**Result:** `4` ✅

---

## 9. Concepts, Data Structures, and Patterns

- **Dynamic programming recipe:** state (`dp[i]` = best using houses `0..i`), recurrence (`max(skip, take)`), base cases (`dp[-1] = dp[-2] = 0`), iteration order (left → right), answer location (`dp[n-1]`).
- **Overlapping subproblems:** the brute-force recursion solves `best_from(i)` many times. Memoization stores each result once.
- **Optimal substructure:** the best plan for houses `0..i` is built from the best plans for `0..i-1` and `0..i-2`.
- **Space optimization (rolling variables):** when a recurrence only looks back a fixed number of steps, keep only those values.
- **Include / exclude decision:** the same "take it or skip it" shape appears in the 0/1 knapsack family.
- **Related notes:**
  - [055_climbing_stairs.md](055_climbing_stairs.md) — the same two-variable Fibonacci-style recurrence.
  - [062_house_robber_ii.md](062_house_robber_ii.md) — houses in a circle; reuses this solution twice.
  - [../01_array/005_maximum_subarray.md](../01_array/005_maximum_subarray.md) — another 1-D DP that collapses to `O(1)` variables.
  - Delete and Earn (LeetCode 740) reduces to this problem (see practice Q3).

---

## 10. Complexity Analysis

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Plain recursion | `O(1.618^n)` (exponential) | `O(n)` | Fibonacci-shaped call tree; stack depth `n`. |
| Memoization | `O(n)` | `O(n)` | Each `best_from(i)` computed once; cache + recursion stack. |
| DP table | `O(n)` | `O(n)` | One loop; a list of `n` values. |
| Rolling variables (optimized) | `O(n)` | `O(1)` | One loop; only `prev2`, `prev1`, `current`. |

With `n <= 100` every polynomial version is instant; only the plain recursion is too slow.

---

## 11. Edge Cases

| Case | Example | Expected result | Why |
|---|---|---|---|
| One house | `[5]` | `5` | Rob it; there is no neighbour. |
| One empty house | `[0]` | `0` | Nothing to steal. |
| Two houses | `[1, 9]` | `9` | Neighbours — rob only the richer one. |
| Gap of two | `[2, 1, 1, 2]` | `4` | Houses 0 and 3; "every other house" would give only 3. |
| All zeros | `[0, 0, 0]` | `0` | Nothing to gain. |
| All equal, odd length | `[400, 400, 400]` | `800` | Houses 0 and 2. |

---

## 12. Common Mistakes and Debugging

1. **Greedy "even vs. odd" indices.** Fails on `[2, 1, 1, 2]` (gives 3, correct answer is 4).
2. **Greedy "take the biggest house first".** Fails on `[2, 3, 2]` as a line: taking the 3 blocks both 2s, giving 3, while `2 + 2 = 4` is better.
3. **Wrong base case `dp[1] = nums[1]`.** It must be `max(nums[0], nums[1])`; with `[9, 1]` the answer is 9.
4. **Index errors for `n = 1`.** The table version must return early (or use the rolling version that starts from `0, 0`).
5. **Updating variables in the wrong order.** Writing `prev2 = prev1` then `prev1 = max(prev1, prev2 + money)` uses the *new* `prev2`. Use tuple assignment or a `current` temporary.
6. **Forgetting memoization in the recursive version.** It is correct but exponential.

**Debugging tip:** print `money, prev2, prev1, current` each iteration and compare with the dry-run table.

---

## 13. Practice Questions

**Q1. What does the optimized solution return for `nums = [2, 1, 1, 2]`? Fill in the DP table.**

<details><summary>Hint</summary>Use `dp[i] = max(dp[i-1], dp[i-2] + nums[i])` with `dp[-1] = dp[-2] = 0`.</summary></details>

**Answer:** `dp[0] = max(0, 0 + 2) = 2`, `dp[1] = max(2, 0 + 1) = 2`, `dp[2] = max(2, 2 + 1) = 3`, `dp[3] = max(3, 2 + 2) = 4`. The answer is `4` (houses 0 and 3).

**Q2. Return the indices of the houses robbed in one optimal plan.**

<details><summary>Hint</summary>Fill the full `dp` table, then walk backwards: if `dp[i] == dp[i-1]`, house `i` was skipped; otherwise it was robbed and you jump to `i - 2`.</summary></details>

**Answer:**

```python
def rob_with_houses(nums):
    n = len(nums)
    dp = [0] * (n + 2)          # dp[i + 2] = best using houses 0..i
    for i in range(n):
        dp[i + 2] = max(dp[i + 1], dp[i] + nums[i])
    chosen = []
    i = n - 1
    while i >= 0:
        if dp[i + 2] == dp[i + 1]:  # skipping house i was enough
            i -= 1
        else:                       # house i was robbed
            chosen.append(i)
            i -= 2
    return dp[n + 1], chosen[::-1]


assert rob_with_houses([2, 7, 9, 3, 1]) == (12, [0, 2, 4])
assert rob_with_houses([1, 2, 3, 1]) == (4, [0, 2])
assert rob_with_houses([2, 1, 1, 2]) == (4, [0, 3])
```

**Q3. Delete and Earn (LeetCode 740): picking a value `x` earns `x` points but deletes every `x - 1` and `x + 1`. Maximize the points.**

<details><summary>Hint</summary>Group equal values: `points[x] = x * count(x)`. Values `x` and `x + 1` now behave like neighbouring houses.</summary></details>

**Answer:** Build `points` indexed by value and run House Robber on it.

```python
from collections import Counter


def delete_and_earn(nums):
    counts = Counter(nums)
    prev2 = prev1 = 0
    for value in range(max(nums) + 1):
        current = max(prev1, prev2 + value * counts[value])
        prev2, prev1 = prev1, current
    return prev1


assert delete_and_earn([3, 4, 2]) == 6
assert delete_and_earn([2, 2, 3, 3, 3, 4]) == 9
```

**Q4. Why does starting both `prev2` and `prev1` at 0 work even when `nums[0]` is 0?**

<details><summary>Hint</summary>What is the true best total for "no houses"?</summary></details>

**Answer:** Zero houses give a total of exactly 0, so `0` is the *correct* value of `dp[-1]` and `dp[-2]`, not just a placeholder. The first step computes `max(0, 0 + nums[0]) = nums[0]`, which is right whether `nums[0]` is 0 or 400.

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** 1-D DP, take-or-skip, two rolling variables.
- **State:** `dp[i]` = best total from houses `0..i`.
- **Recurrence:** `dp[i] = max(dp[i-1], dp[i-2] + nums[i])`; base `dp[-1] = dp[-2] = 0`.
- **Time:** `O(n)`.
- **Auxiliary space:** `O(1)`.
- **One-line memory hook:** *"Skip and keep yesterday's best, or rob and add to the day before's."*

### Completion checklist

- [x] Problem requirements verified
- [x] Examples and constraints verified
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force (plain recursion) and memoized solutions written and tested
- [x] Optimized Python solution (rolling variables) and DP-table version written and tested (`tools/tests/p061.py`)
- [x] Line-by-line explanation written
- [x] Dry run completed with real examples
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
