# 060. Combination Sum IV (listed as "Combination Sum")

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Combination Sum IV |
| **LeetCode number** | 377 |
| **Topic (source list)** | Dynamic Programming |
| **Also uses** | Recursion + memoization |
| **Difficulty** | Medium |
| **LeetCode URL** | <https://leetcode.com/problems/combination-sum-iv/> |
| **Pattern** | 1-D counting DP over totals (ordered sequences / permutations) |

> **Note about the title.** The source list names this problem "Combination Sum", but its link points to **LeetCode 377 – Combination Sum IV** (the problem in the original Blind 75 list). This note follows the link and covers **377**. The similarly named **LeetCode 39 – Combination Sum** (return the *lists*, order ignored) is a different problem; it is compared with 377 in practice question Q2.

---

## 2. Problem Explanation

### What are we given?

- `nums` — a list of **distinct** positive integers.
- `target` — a positive integer.

### What must we return?

The **number of ordered sequences** built from values in `nums` whose sum is exactly `target`.

### The rules

1. A value from `nums` may be used **any number of times** in a sequence.
2. **Order matters.** `(1, 2)` and `(2, 1)` are two *different* sequences and are counted separately. Even though LeetCode calls them "combinations", mathematically we are counting **ordered** sequences (compositions / permutations with repetition).
3. Only the **count** is returned, not the sequences.
4. The tests are generated so that the **final answer** fits in a 32-bit integer.

### Examples

**Example 1**

```text
Input:  nums = [1, 2, 3], target = 4
Output: 7
```

The seven ordered sequences are:

```text
(1, 1, 1, 1)
(1, 1, 2)
(1, 2, 1)
(1, 3)
(2, 1, 1)
(2, 2)
(3, 1)
```

Notice that `(1, 1, 2)`, `(1, 2, 1)` and `(2, 1, 1)` all count separately.

**Example 2**

```text
Input:  nums = [9], target = 3
Output: 0
```

The only value, 9, is already bigger than 3, so no sequence works.

### Constraints

- `1 <= nums.length <= 200`
- `1 <= nums[i] <= 1000`
- All the elements of `nums` are unique.
- `1 <= target <= 1000`

**Follow-up:** What if negative numbers were allowed in `nums`? How would that change the problem, and what extra limitation would we need to add so the question still makes sense? (Answered in section 9 and practice question Q3.)

---

## 3. Everyday Analogy

> **Explain it like I'm five**

You're climbing a staircase with `target` steps. You have some special jump sizes — say you can jump **1, 2 or 3** steps at a time. How many different **jump patterns** get you exactly to the top?

"Jump 1 then 2" and "jump 2 then 1" are different patterns — you landed on different steps along the way.

Here's the trick: think about your **very last jump**. To reach step 4:
- if your last jump was 1, you were on step 3 before it,
- if it was 2, you were on step 2,
- if it was 3, you were on step 1.

So *patterns to step 4* = *patterns to step 3* + *patterns to step 2* + *patterns to step 1*. Write the counts on each step, starting from the bottom (there's exactly **1** way to "be at step 0": do nothing), and add your way up.

That's exactly [Climbing Stairs](055_climbing_stairs.md), except the allowed jump sizes come from `nums`.

---

## 4. Step-by-Step Logic

Follow the DP recipe.

1. **Find the choice.** Every sequence that sums to `t` has a **last number** `x` (some value in `nums` with `x <= t`). Removing it leaves a sequence that sums to `t - x`.
2. **State definition.** `dp[t]` = number of ordered sequences of values from `nums` that sum to exactly `t`.
3. **Recurrence.** Group the sequences by their last number:

   ```text
   dp[t] = sum(dp[t - x] for x in nums if x <= t)
   ```

   Different last numbers give different sequences, and every sequence has exactly one last number, so nothing is double-counted or missed.
4. **Base case.** `dp[0] = 1` — the **empty** sequence is the one way to make 0. It is what lets a single number `x == t` count as one sequence.
5. **Iteration order.** `dp[t]` needs smaller totals, so compute `t = 1, 2, …, target`. **The totals loop is outside and the `nums` loop is inside.** That loop order is precisely what makes the count *ordered* — see section 9 for why swapping the loops counts unordered combinations instead.
6. **Answer location.** `dp[target]`.

---

## 5. Brute-Force Solution

### Algorithm

`count(remaining)` = number of ordered sequences summing to `remaining`. Try every number as the **next** element; when `remaining` hits 0, we've found one complete sequence.

### Python code

```python
from typing import List


class Solution:
    def combinationSum4(self, nums: List[int], target: int) -> int:
        def count(remaining: int) -> int:
            if remaining == 0:
                return 1                     # one finished sequence
            total = 0
            for num in nums:
                if num <= remaining:
                    total += count(remaining - num)
            return total

        return count(target)
```

### Explanation

- Each branch of the recursion tree is one choice of "next number", so each root-to-leaf path that reaches 0 is one ordered sequence.
- Because all numbers are positive, `remaining` strictly decreases, so the recursion always ends.
- The answer is correct but every successful sequence is reached by its own path, so the running time is **at least the answer itself**.

### Complexity

- **Time:** exponential. The number of calls is at least the number of sequences found; for `nums = [1, 2]`, `target = 1000` that is the 1001st Fibonacci number (over 200 digits). This **times out** at LeetCode limits. A rough bound is `O(k^(target / min(nums)))` for `k = len(nums)`.
- **Auxiliary space:** `O(target / min(nums))` recursion depth.

### The bridge: memoization

There are only `target + 1` distinct values of `remaining`. Caching `count(remaining)` makes each one cost `O(k)` once → `O(target × k)` in total.

```python
from typing import List
from functools import lru_cache


class Solution:
    def combinationSum4(self, nums: List[int], target: int) -> int:
        @lru_cache(maxsize=None)
        def count(remaining: int) -> int:
            if remaining == 0:
                return 1
            return sum(count(remaining - num) for num in nums if num <= remaining)

        return count(target)
```

The recursion can be `target = 1000` calls deep (when `1` is in `nums`), and each level also adds a generator-expression frame, so it exceeds Python's default recursion limit of 1000 — `nums = [1, 2, 3]`, `target = 1000` raises `RecursionError` unless you raise the limit. The bottom-up table avoids recursion entirely.

---

## 6. Optimized Solution

### Idea — bottom-up counting table

Fill `dp[0..target]` from small to large totals, adding `dp[t - num]` for every usable `num`.

### Algorithm

1. `dp = [0] * (target + 1)`, `dp[0] = 1`.
2. For `t` from `1` to `target`:
   - For each `num` in `nums` with `num <= t`: `dp[t] += dp[t - num]`.
3. Return `dp[target]`.

### Python code (LeetCode-ready)

```python
from typing import List


class Solution:
    def combinationSum4(self, nums: List[int], target: int) -> int:
        dp = [0] * (target + 1)   # dp[t] = number of ordered sequences summing to t
        dp[0] = 1                 # the empty sequence

        for t in range(1, target + 1):       # totals OUTSIDE ...
            for num in nums:                 # ... numbers INSIDE -> order matters
                if num <= t:
                    dp[t] += dp[t - num]     # sequences ending with num

        return dp[target]
```

**About the 32-bit guarantee:** only the *final* answer is guaranteed to fit. Some intermediate `dp[t]` values for other totals can be much larger. Python integers never overflow, so this is not an issue here; in Java/C++ people use a wider or unsigned type (or skip values above the 32-bit limit, since they can't contribute to a valid answer).

---

## 7. Line-by-Line Explanation

| Line | What it does | Why |
|---|---|---|
| `dp = [0] * (target + 1)` | One counter for every total `0..target`. | `dp[t]` will hold the number of sequences summing to `t`. |
| `dp[0] = 1` | Base case. | The empty sequence sums to 0. Without it every count stays 0. |
| `for t in range(1, target + 1):` | Visits totals in increasing order. | `dp[t]` uses `dp[t - num]` with smaller indices, already final. |
| `for num in nums:` | Tries each value as the **last** element of the sequence. | Grouping by the last element splits the sequences into disjoint groups. |
| `if num <= t:` | Skips values that overshoot. | `t - num` would be negative (and Python would silently read from the end of the list). |
| `dp[t] += dp[t - num]` | Adds every sequence for `t - num`, each extended by `num`. | Each such sequence + `num` is a distinct sequence for `t`. |
| `return dp[target]` | Returns the count for the requested total. | — |

---

## 8. Dry Run

**Input:** `nums = [1, 2, 3]`, `target = 4` (official Example 1).

| `t` | last = 1: `dp[t-1]` | last = 2: `dp[t-2]` | last = 3: `dp[t-3]` | `dp[t]` | Sequences counted |
|---|---|---|---|---|---|
| 0 | — | — | — | **1** | `()` (empty) |
| 1 | `dp[0] = 1` | — | — | **1** | `(1)` |
| 2 | `dp[1] = 1` | `dp[0] = 1` | — | **2** | `(1,1)`, `(2)` |
| 3 | `dp[2] = 2` | `dp[1] = 1` | `dp[0] = 1` | **4** | `(1,1,1)`, `(2,1)`, `(1,2)`, `(3)` |
| 4 | `dp[3] = 4` | `dp[2] = 2` | `dp[1] = 1` | **7** | 4 ending in 1, 2 ending in 2, 1 ending in 3 |

Final table: `dp = [1, 1, 2, 4, 7]`.

Breaking down `dp[4] = 7` by the last number:
- **ends with 1** (4 sequences): every sequence for 3, plus a 1 → `(1,1,1,1)`, `(2,1,1)`, `(1,2,1)`, `(3,1)`.
- **ends with 2** (2 sequences): every sequence for 2, plus a 2 → `(1,1,2)`, `(2,2)`.
- **ends with 3** (1 sequence): the sequence for 1, plus a 3 → `(1,3)`.

That's exactly the 7 sequences listed in the official example ✅.

**Second dry run:** `nums = [9]`, `target = 3` (Example 2). For `t = 1, 2, 3`, the only number 9 is `> t`, so nothing is added: `dp = [1, 0, 0, 0]` → answer `0` ✅.

---

## 9. Concepts, Data Structures, and Patterns

- **Counting DP:** like the minimizing DP in [Coin Change](056_coin_change.md), but `min` becomes `+`. Same "last choice" structure.
- **Ordered vs unordered counting — the loop-order rule:**

  | Loop order | What is counted | Problem |
  |---|---|---|
  | totals outside, numbers inside | **ordered** sequences (`(1,2)` ≠ `(2,1)`) | 377 Combination Sum IV (this note) |
  | numbers outside, totals inside | **unordered** combinations (multisets) | 518 Coin Change II |

  With numbers outside, each combination is built in one fixed order (all copies of the first number, then the second, …), so it's counted once. With totals outside, every number can be the last one at every total, so every arrangement is counted.
- **Generalized Climbing Stairs:** [Climbing Stairs](055_climbing_stairs.md) is exactly this problem with `nums = [1, 2]`.
- **Backtracking contrast:** LeetCode 39 Combination Sum asks for the **lists themselves** (unordered), which requires backtracking with a start index, not just counting.
- **Follow-up — negative numbers:** if `nums` contains both a positive and a negative number, the answer can become **infinite**. Example: `nums = [1, -1]`, `target = 1`: `(1)`, `(1, 1, -1)`, `(1, -1, 1)`, `(1, 1, -1, 1, -1)`, … — you can keep inserting `+1, -1` pairs forever. Also, `t - num` no longer moves toward 0, so the table has no valid fill order. To make the problem well-defined we must add a restriction, most commonly a **maximum sequence length** `L` (or "each element used at most once"). With a length limit, the state becomes `(length, total)` and we count level by level (practice Q3).
- **Related notes:** [Coin Change](056_coin_change.md), [Word Break](059_word_break_problem.md) (same "last piece" recurrence, booleans instead of counts), [Decode Ways](063_decode_ways.md) (counting splits of a string).

---

## 10. Complexity Analysis

Let `k = len(nums)` (≤ 200) and `T = target` (≤ 1000).

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Brute-force recursion | Exponential (at least the answer; about `O(k^(T / min(nums)))`) | `O(T / min(nums))` | Every sequence is generated one by one. |
| Memoized recursion | `O(T × k)` | `O(T)` | `T + 1` states, each sums over `k` numbers once; cache + stack. |
| Bottom-up DP (optimized) | `O(T × k)` | `O(T)` | Double loop: `1000 × 200 = 2 × 10^5` additions at the limits; one list of `T + 1` counters. |

(Arithmetic on Python's big integers is treated as `O(1)` here, which is reasonable because the answer fits in 32 bits.)

---

## 11. Edge Cases

| Case | Example | Expected result | Why |
|---|---|---|---|
| All numbers too big | `nums = [9]`, `target = 3` | `0` | Nothing fits. |
| Single number equals target | `nums = [1]`, `target = 1` | `1` | Just `(1)`; relies on `dp[0] = 1`. |
| Single number, multiple of target | `nums = [5]`, `target = 10` | `1` | Only `(5, 5)`. |
| Order creates extra answers | `nums = [2, 3]`, `target = 7` | `3` | `(2,2,3)`, `(2,3,2)`, `(3,2,2)`. |
| Unsorted input | `nums = [4, 2, 1]`, `target = 5` | `10` | The order of `nums` doesn't matter to the algorithm. |
| Largest number, small target | `nums = [1000]`, `target = 1` | `0` | `1000 > 1`. |
| Large answer | `nums = [1, 2, 3]`, `target = 32` | `181997601` | Still fits in 32 bits; the table computes it instantly while brute force would take far too long. |

---

## 12. Common Mistakes and Debugging

1. **Swapping the loops.** Putting `for num in nums` outside and `for t in …` inside counts **unordered** combinations (Coin Change II) — for Example 1 it returns 4 instead of 7.
2. **Forgetting `dp[0] = 1`.** Every count stays 0.
3. **Treating the problem like LeetCode 39.** 377 wants a **number**, and order matters; 39 wants the **lists** and order doesn't matter.
4. **Negative index.** Without `num <= t`, `dp[t - num]` with a negative index reads from the end of the list and silently adds garbage.
5. **Generating all sequences.** Even for moderate targets the count is huge (`181997601` for `[1, 2, 3]`, `32`); count, don't list.
6. **Worrying about overflow in Python.** Not needed, but in fixed-width languages intermediate values can overflow even when the final answer fits.

**Debugging tip:** print `dp` for `nums = [1, 2, 3]`, `target = 4`; it must be `[1, 1, 2, 4, 7]`. If you see `[1, 1, 2, 3, 4]`, your loops are swapped.

---

## 13. Practice Questions

**Q1. Compute `combinationSum4([2, 3], 7)` by hand with the table, and list the sequences.**

<details><summary>Hint</summary>`dp[t] = dp[t-2] + dp[t-3]` (when the indices are valid), starting from `dp[0] = 1`.</summary></details>

**Answer:** `dp[0..7] = [1, 0, 1, 1, 1, 2, 2, 3]`:
- `dp[2] = dp[0] = 1`, `dp[3] = dp[1] + dp[0] = 1`, `dp[4] = dp[2] + dp[1] = 1`,
- `dp[5] = dp[3] + dp[2] = 2`, `dp[6] = dp[4] + dp[3] = 2`, `dp[7] = dp[5] + dp[4] = 3`.

The 3 sequences are `(2,2,3)`, `(2,3,2)`, `(3,2,2)`.

**Q2. Compare three look-alike problems on the same input: LeetCode 377 (this note), LeetCode 518 Coin Change II, and LeetCode 39 Combination Sum. What changes in the code?**

<details><summary>Hint</summary>377 and 518 differ only in the loop order. 39 must output the actual lists, so it needs backtracking with a "start index" so that each combination is produced in non-decreasing order exactly once.</summary></details>

**Answer:**

- **377 Combination Sum IV:** count **ordered** sequences → totals outside, numbers inside.
- **518 Coin Change II:** count **unordered** combinations → numbers outside, totals inside (the swap).
- **39 Combination Sum:** return each **unordered** combination as a list → backtracking that only reuses candidates from the current index onward.

```python
def count_ordered(nums, target):                 # LeetCode 377
    dp = [0] * (target + 1)
    dp[0] = 1
    for t in range(1, target + 1):               # totals outside
        for num in nums:                         # numbers inside
            if num <= t:
                dp[t] += dp[t - num]
    return dp[target]


def count_unordered(amount, coins):              # LeetCode 518
    dp = [0] * (amount + 1)
    dp[0] = 1
    for coin in coins:                           # numbers outside
        for t in range(coin, amount + 1):        # totals inside
            dp[t] += dp[t - coin]
    return dp[amount]


def list_combinations(candidates, target):       # LeetCode 39
    candidates = sorted(candidates)
    result, path = [], []

    def backtrack(start, remaining):
        if remaining == 0:
            result.append(path[:])
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remaining:
                break                            # sorted: later ones are bigger
            path.append(candidates[i])
            backtrack(i, remaining - candidates[i])   # i, not i + 1: reuse allowed
            path.pop()

    backtrack(0, target)
    return result


assert count_ordered([1, 2, 3], 4) == 7          # (1,1,2), (1,2,1), (2,1,1) all count
assert count_unordered(4, [1, 2, 3]) == 4        # {1,1,1,1}, {1,1,2}, {2,2}, {1,3}
assert list_combinations([1, 2, 3], 4) == [[1, 1, 1, 1], [1, 1, 2], [1, 3], [2, 2]]
assert count_unordered(5, [1, 2, 5]) == 4        # LeetCode 518 example
assert list_combinations([2, 3, 6, 7], 7) == [[2, 2, 3], [7]]          # LeetCode 39 example
assert list_combinations([2, 3, 5], 8) == [[2, 2, 2, 2], [2, 3, 3], [3, 5]]
assert len(list_combinations([1, 2, 3], 4)) == count_unordered(4, [1, 2, 3])
```

Same input `[1, 2, 3]`, total 4: 377 gives **7**, 518 gives **4**, and 39 lists those **4** combinations.

**Q3. Follow-up: allow negative numbers, but limit the sequence length to at most `max_len`. Count the ordered sequences that sum to `target`.**

<details><summary>Hint</summary>Without a length limit the answer can be infinite (`[1, -1]`, target 1). With a limit, build sequences one element at a time: `ways[s]` = number of sequences of the current length with sum `s`. Totals can now be negative, so use a dictionary.</summary></details>

**Answer:** Keep a `Counter` from sum to count for sequences of length `L`, extend every sequence by every number to get length `L + 1`, and add up the ones that hit `target`.

```python
from collections import Counter


def count_with_negatives(nums, target, max_len):
    total = 0
    ways = Counter({0: 1})                 # length 0: the empty sequence
    for _ in range(max_len):               # build lengths 1, 2, ..., max_len
        nxt = Counter()
        for s, c in ways.items():
            for num in nums:
                nxt[s + num] += c
        ways = nxt
        total += ways[target]
    return total


assert count_with_negatives([1, -1], 1, 1) == 1        # (1)
assert count_with_negatives([1, -1], 1, 3) == 4        # (1), (1,1,-1), (1,-1,1), (-1,1,1)
assert count_with_negatives([1, 2, 3], 4, 4) == 7      # no negatives: same as Example 1
assert count_with_negatives([5, -3], 2, 2) == 2        # (5,-3), (-3,5)
```

Each extra length step does `O(#sums × k)` work, and the number of distinct sums is bounded by `max_len × (max(nums) − min(nums)) + 1`.

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Problem:** LeetCode 377 Combination Sum IV (source title says "Combination Sum").
- **Pattern:** 1-D counting DP over totals; counts **ordered** sequences.
- **State:** `dp[t]` = number of ordered sequences summing to `t`.
- **Recurrence:** `dp[t] = Σ dp[t - x]` for `x` in `nums`, `x <= t`.
- **Base / order / answer:** `dp[0] = 1`; totals outside, numbers inside; answer `dp[target]`.
- **Loop swap:** numbers outside → unordered count (LeetCode 518).
- **Negatives follow-up:** answer can be infinite; add a maximum length.
- **Time:** `O(target × len(nums))`. **Auxiliary space:** `O(target)`.
- **One-line memory hook:** *"Which number did I add last? Sum the ways to reach what was before it."*

### Completion checklist

- [x] Problem requirements verified (title/link discrepancy documented)
- [x] Examples and constraints verified
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force solution written and tested
- [x] Memoized (top-down) bridge solution written and tested
- [x] Optimized Python solution written and tested (`tools/tests/p060.py`)
- [x] Line-by-line explanation written
- [x] Dry run completed with a real example (DP table)
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added (including 377 vs 518 vs 39 and the negative-numbers follow-up)
- [x] Final review completed
