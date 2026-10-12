# 062. House Robber II

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | House Robber II |
| **LeetCode number** | 213 |
| **Topic (source list)** | Dynamic Programming |
| **Also uses** | Array, Case splitting |
| **Difficulty** | Medium |
| **LeetCode URL** | <https://leetcode.com/problems/house-robber-ii/> |
| **Pattern** | Break the circle into two straight lines, run House Robber on each |

---

## 2. Problem Explanation

> Read [061_house_robber.md](061_house_robber.md) first — this problem reuses its solution.

### What are we given?

`nums` — a list of non-negative integers; `nums[i]` is the money in house `i`. This time the houses are arranged **in a circle**: the last house sits right next to the first one.

### What must we return?

The **largest total amount of money** you can take in one night.

### The rules

1. You may not rob two **neighbouring** houses.
2. Because the street is a circle, house `0` and house `n - 1` **are neighbours** (when there is more than one house).
3. If there is only **one** house, it has no neighbours at all — you simply rob it.

### Examples

**Example 1**

```text
Input:  nums = [2, 3, 2]
Output: 3
```

Houses 0 and 2 both hold 2, but they are neighbours on the circle, so `2 + 2` is not allowed. The best is house 1 alone: `3`.

**Example 2**

```text
Input:  nums = [1, 2, 3, 1]
Output: 4
```

Rob house 0 (money 1) and house 2 (money 3): `1 + 3 = 4`. They are not neighbours.

**Example 3**

```text
Input:  nums = [1, 2, 3]
Output: 3
```

Every pair of houses is adjacent in a 3-house circle, so you can rob only one house; the richest has 3.

### Constraints

- `1 <= nums.length <= 100`
- `0 <= nums[i] <= 1000`

There is no follow-up in the official statement.

---

## 3. Everyday Analogy

> **Explain it like I'm five**

Children sit around a round table, each with a plate of sweets. You may take a plate, but never from two children sitting side by side — and because the table is round, the first child and the last child are sitting side by side too.

The circle is confusing, so you play a trick: **ask one child to leave the table.** Once someone is gone, the circle is broken and the remaining children form a simple line — and you already know how to solve the line problem (House Robber I).

But who should leave? The first child and the last child can never *both* be robbed, so at least one of them is left untouched. So you try twice:

1. The **first** child leaves → solve the line `nums[1:]`.
2. The **last** child leaves → solve the line `nums[:-1]`.

The better of the two answers is the best you can do around the whole table.

---

## 4. Step-by-Step Logic

1. **What is new compared to House Robber I?** Only one extra rule: houses `0` and `n - 1` cannot both be robbed.
2. **Split into cases.** In any valid plan, at least one of house `0` and house `n - 1` is **not** robbed.
   - **Case A:** house `0` is not robbed → the problem is House Robber I on `nums[1:]` (a straight line, because without house 0 the circle is open).
   - **Case B:** house `n - 1` is not robbed → House Robber I on `nums[:-1]`.
3. **Every valid plan appears in at least one case**, and every plan in either case is valid on the circle. So the answer is `max(caseA, caseB)`.
4. **The DP inside each case** is exactly the one from 061:
   - **State:** `dp[i]` = best total from the first `i + 1` houses of the line.
   - **Recurrence:** `dp[i] = max(dp[i - 1], dp[i - 2] + line[i])`.
   - **Base cases:** `dp[-1] = dp[-2] = 0`.
   - **Order:** left to right. **Answer:** the last `dp` value.
5. **Single-house special case.** If `n == 1`, both `nums[1:]` and `nums[:-1]` are empty and would give 0 — but the correct answer is `nums[0]`. So handle `n == 1` first.

---

## 5. Brute-Force Solution

### Algorithm (plain recursion that remembers whether house 0 was robbed)

`best(i, robbed_first)` = most money from houses `i..n-1`, given whether house 0 was robbed.

- If `i >= n` → `0`.
- Skipping house `i` is always allowed → `best(i + 1, robbed_first)`.
- Robbing house `i` is allowed unless `i` is the last house **and** house 0 was robbed (they are neighbours on the circle). If allowed → `nums[i] + best(i + 2, robbed_first or i == 0)`.

### Python code

```python
from typing import List


class Solution:
    def rob(self, nums: List[int]) -> int:
        n = len(nums)

        def best(i: int, robbed_first: bool) -> int:
            if i >= n:
                return 0
            skip = best(i + 1, robbed_first)
            if i == n - 1 and robbed_first:   # last house touches house 0
                return skip
            take = nums[i] + best(i + 2, robbed_first or i == 0)
            return max(skip, take)

        return best(0, False)
```

### Explanation

- This tries every allowed plan, branching "skip / take" at each house.
- The extra flag `robbed_first` carries the circular rule to the end of the street.
- With one house (`n = 1`), index 0 is also the last index, but `robbed_first` is still `False` when we look at it, so robbing it is allowed — the single-house case works naturally.

### Complexity

- **Time:** exponential, about `1.618^n` calls (Fibonacci-shaped tree), `O(2^n)` as a safe bound. For `n = 100` it would **time out**.
- **Auxiliary space:** `O(n)` recursion depth.

### The bridge — memoization

The state is just `(i, robbed_first)`: at most `2(n + 2)` different states. Caching makes it linear:

```python
from functools import lru_cache
from typing import List


class Solution:
    def rob(self, nums: List[int]) -> int:
        n = len(nums)

        @lru_cache(maxsize=None)
        def best(i: int, robbed_first: bool) -> int:
            if i >= n:
                return 0
            skip = best(i + 1, robbed_first)
            if i == n - 1 and robbed_first:
                return skip
            return max(skip, nums[i] + best(i + 2, robbed_first or i == 0))

        return best(0, False)
```

`O(n)` time and `O(n)` space. The two values of `robbed_first` are exactly the two cases of the optimized solution.

---

## 6. Optimized Solution

### Idea

Run the `O(1)`-space House Robber I loop twice — once without the first house, once without the last — and take the larger result.

### Algorithm

1. If `n == 1`, return `nums[0]`.
2. `rob_line(houses)` = the House Robber I rolling-variable loop.
3. Return `max(rob_line(nums[1:]), rob_line(nums[:-1]))`.

### Python code (LeetCode-ready)

```python
from typing import List


class Solution:
    def rob(self, nums: List[int]) -> int:
        if len(nums) == 1:                 # one house: no neighbours at all
            return nums[0]

        def rob_line(houses: List[int]) -> int:
            prev2 = prev1 = 0              # dp[i-2], dp[i-1]
            for money in houses:
                prev2, prev1 = prev1, max(prev1, prev2 + money)
            return prev1

        skip_first = rob_line(nums[1:])    # house 0 stays untouched
        skip_last = rob_line(nums[:-1])    # house n-1 stays untouched
        return max(skip_first, skip_last)
```

### Variant without slicing (index range)

Slicing copies the list (`O(n)` extra memory). Passing index bounds keeps the extra space at `O(1)`:

```python
from typing import List


class Solution:
    def rob(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 1:
            return nums[0]

        def rob_range(lo: int, hi: int) -> int:   # houses lo..hi inclusive
            prev2 = prev1 = 0
            for i in range(lo, hi + 1):
                prev2, prev1 = prev1, max(prev1, prev2 + nums[i])
            return prev1

        return max(rob_range(1, n - 1), rob_range(0, n - 2))
```

---

## 7. Line-by-Line Explanation

(Slicing version)

| Line | What it does | Why |
|---|---|---|
| `if len(nums) == 1: return nums[0]` | Handles a single house. | Both slices would be empty and return 0, but one house has no neighbour, so we can rob it. |
| `def rob_line(houses):` | House Robber I on a straight line. | Once one end is removed, the circle is a line. |
| `prev2 = prev1 = 0` | `dp[-2] = dp[-1] = 0`. | No houses → no money. |
| `prev2, prev1 = prev1, max(prev1, prev2 + money)` | Recurrence + window shift in one line. | Skip (`prev1`) or rob (`prev2 + money`); the right side is evaluated before assignment. |
| `return prev1` | Best total for this line. | `dp` of the last house. |
| `skip_first = rob_line(nums[1:])` | Case A: house 0 not robbed. | House `n-1` is then free to be robbed. |
| `skip_last = rob_line(nums[:-1])` | Case B: house `n-1` not robbed. | House 0 is then free to be robbed. |
| `return max(skip_first, skip_last)` | Best of both cases. | Every valid plan leaves house 0 or house `n-1` untouched, so it is counted in at least one case. |

---

## 8. Dry Run

**Input:** `nums = [1, 2, 3, 1]` (Example 2), `n = 4`.

**Case A — skip the first house:** line `[2, 3, 1]`

| Step | `money` | `prev2` | `prev1` | `max(prev1, prev2 + money)` | new `prev2`, `prev1` |
|---|---|---|---|---|---|
| 1 | 2 | 0 | 0 | `max(0, 2) = 2` | 0, 2 |
| 2 | 3 | 0 | 2 | `max(2, 3) = 3` | 2, 3 |
| 3 | 1 | 2 | 3 | `max(3, 3) = 3` | 3, 3 |

`skip_first = 3` (house 2 alone, or houses 1 and 3).

**Case B — skip the last house:** line `[1, 2, 3]`

| Step | `money` | `prev2` | `prev1` | `max(prev1, prev2 + money)` | new `prev2`, `prev1` |
|---|---|---|---|---|---|
| 1 | 1 | 0 | 0 | `max(0, 1) = 1` | 0, 1 |
| 2 | 2 | 0 | 1 | `max(1, 2) = 2` | 1, 2 |
| 3 | 3 | 1 | 2 | `max(2, 4) = 4` | 2, 4 |

`skip_last = 4` (houses 0 and 2).

**Result:** `max(3, 4) = 4` ✅

**Second dry run:** `nums = [2, 3, 2]` (Example 1)

- Case A, line `[3, 2]`: `dp = [3, max(3, 0 + 2) = 3]` → 3.
- Case B, line `[2, 3]`: `dp = [2, max(2, 0 + 3) = 3]` → 3.
- **Result:** `max(3, 3) = 3` ✅ — the forbidden plan `2 + 2` never appears, because each line contains only one of the two end houses.

**Single house:** `nums = [5]` → the early return gives `5` ✅ (without it, both lines are empty and we would wrongly return 0).

---

## 9. Concepts, Data Structures, and Patterns

- **Reduction to a solved problem:** the circular version is two calls to the linear version ([061_house_robber.md](061_house_robber.md)).
- **Case analysis on a constraint:** when one rule links the two ends, split on "which end is definitely unused". Both cases together cover every valid plan.
- **DP recipe (inside each case):** state `dp[i]`, recurrence `max(dp[i-1], dp[i-2] + x)`, base `0, 0`, left-to-right order, answer = last value.
- **Extra state instead of case splitting:** the memoized brute force carries a flag `robbed_first` — another general way to handle a constraint that connects far-apart positions.
- **Circular arrays:** a common trick is to "cut" the circle somewhere and solve linear subproblems. Compare Maximum Sum Circular Subarray in [../01_array/005_maximum_subarray.md](../01_array/005_maximum_subarray.md) (practice Q3 there).
- **Related:** [055_climbing_stairs.md](055_climbing_stairs.md) (same two-variable recurrence shape), House Robber III (LeetCode 337, houses on a tree).

---

## 10. Complexity Analysis

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Plain recursion | `O(1.618^n)` (exponential) | `O(n)` | Skip/take branching; recursion depth `n`. |
| Memoization | `O(n)` | `O(n)` | `2(n+2)` states, each `O(1)` work; cache + stack. |
| Two linear passes, slicing (optimized) | `O(n)` | `O(n)` | Two loops of `n - 1` steps; each slice copies `n - 1` items. |
| Two linear passes, index range | `O(n)` | `O(1)` | Same loops, no copies — only a few variables. |

---

## 11. Edge Cases

| Case | Example | Expected result | Why |
|---|---|---|---|
| One house | `[5]` | `5` | No neighbours; must be handled before slicing. |
| One empty house | `[0]` | `0` | Nothing to take. |
| Two houses | `[5, 9]` | `9` | They are neighbours both ways; rob the richer. |
| Three houses | `[1, 2, 3]` | `3` | All pairs adjacent; take the max single house. |
| Ends are the best pair | `[2, 1, 1, 2]` | `3` | `2 + 2` uses houses 0 and 3, which touch on the circle. (On a line the answer would be 4.) |
| Best plan avoids the last house | `[200, 3, 140, 20, 10]` | `340` | Houses 0 and 2. |

---

## 12. Common Mistakes and Debugging

1. **Forgetting `n == 1`.** `nums[1:]` and `nums[:-1]` are both empty, so the function returns 0 instead of `nums[0]`.
2. **Running House Robber I on the whole circle.** `[2, 3, 2]` would give 4 (houses 0 and 2), which is illegal here.
3. **Excluding both ends at once** (`nums[1:-1]`). This misses plans that rob house 0 *or* house `n-1`. Example: `[1, 2, 3, 1]` → `nums[1:-1] = [2, 3]` gives 3, but the answer is 4.
4. **Thinking the two cases must be disjoint.** They overlap (plans that skip both ends appear in both); that is fine because we take a `max`, not a sum.
5. **Off-by-one in the index-range variant.** The ranges are `1..n-1` and `0..n-2`, inclusive.

**Debugging tip:** print `skip_first` and `skip_last` separately — if the answer is wrong, one of the two lines is wrong, and you can check it with your 061 code.

---

## 13. Practice Questions

**Q1. Compute the answer for `nums = [2, 1, 1, 2]` and explain why it differs from House Robber I.**

<details><summary>Hint</summary>Run the linear DP on `[1, 1, 2]` and on `[2, 1, 1]`.</summary></details>

**Answer:** Line `[1, 1, 2]`: `dp = 1, 1, 3` → 3. Line `[2, 1, 1]`: `dp = 2, 2, 3` → 3. The answer is `3`. House Robber I gives 4 by robbing houses 0 and 3, but on a circle they are neighbours.

**Q2. Why is `max(rob_line(nums[1:]), rob_line(nums[:-1]))` never too large — could it accidentally count an illegal plan?**

<details><summary>Hint</summary>Which houses does each line contain?</summary></details>

**Answer:** Each line contains **at most one** of the two end houses, and inside a line the linear DP never picks two adjacent houses. The only adjacency that exists on the circle but not on a line is `(0, n-1)`, and no line contains both. So every plan the DP finds is legal on the circle.

**Q3. Write the circular robber using a single helper that takes the list and a range, and check it against a brute force on small inputs.**

<details><summary>Hint</summary>Brute force: try every bitmask, reject masks with two neighbours on the circle.</summary></details>

**Answer:**

```python
import random


def rob_circle(nums):
    n = len(nums)
    if n == 1:
        return nums[0]

    def rob_range(lo, hi):
        prev2 = prev1 = 0
        for i in range(lo, hi + 1):
            prev2, prev1 = prev1, max(prev1, prev2 + nums[i])
        return prev1

    return max(rob_range(1, n - 1), rob_range(0, n - 2))


def rob_circle_brute(nums):
    n = len(nums)
    best = 0
    for mask in range(1 << n):
        if n > 1 and any(mask >> i & 1 and mask >> ((i + 1) % n) & 1 for i in range(n)):
            continue
        best = max(best, sum(nums[i] for i in range(n) if mask >> i & 1))
    return best


assert rob_circle([2, 3, 2]) == 3
assert rob_circle([1, 2, 3, 1]) == 4
assert rob_circle([1]) == 1
rng = random.Random(0)
for _ in range(200):
    houses = [rng.randint(0, 20) for _ in range(rng.randint(1, 9))]
    assert rob_circle(houses) == rob_circle_brute(houses), houses
```

**Q4. What does the code return for `nums = [0, 0, 7]`?**

<details><summary>Hint</summary>Which two lines are solved?</summary></details>

**Answer:** Lines `[0, 7]` → 7 and `[0, 0]` → 0, so the answer is `7`.

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** Break the circle → two House Robber I runs.
- **Key idea:** House 0 and house `n-1` can't both be robbed, so answer = `max(rob(nums[1:]), rob(nums[:-1]))`.
- **Special case:** `n == 1` → `nums[0]`.
- **Time:** `O(n)`.
- **Auxiliary space:** `O(1)` with index ranges (`O(n)` if you slice).
- **One-line memory hook:** *"Send one end-child away, solve the line, try both ends."*

### Completion checklist

- [x] Problem requirements verified
- [x] Examples and constraints verified
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force (recursion with a flag) and memoized solutions written and tested
- [x] Optimized Python solution (slicing and index-range variants) written and tested (`tools/tests/p062.py`)
- [x] Line-by-line explanation written
- [x] Dry run completed with real examples
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
