# 055. Climbing Stairs

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Climbing Stairs |
| **LeetCode number** | 70 |
| **Topic (source list)** | Dynamic Programming |
| **Also uses** | Math, Memoization, Recursion |
| **Difficulty** | Easy |
| **LeetCode URL** | <https://leetcode.com/problems/climbing-stairs/> |
| **Pattern** | 1-D DP: `ways(i) = ways(i-1) + ways(i-2)` (Fibonacci) |

---

## 2. Problem Explanation

### What are we given?

`n` — the number of steps in a staircase. You start at the bottom (step 0) and the top is step `n`.

### What must we return?

The number of **different ways** to reach the top, if each move climbs **either 1 step or 2 steps**.

### What counts as "different"?

Two ways are different if their **sequences of moves** are different. Order matters: `1 + 2` and `2 + 1` are two separate ways, even though they use the same moves.

### Examples

**Example 1**

```text
Input:  n = 2
Output: 2
```

1. `1 + 1`
2. `2`

**Example 2**

```text
Input:  n = 3
Output: 3
```

1. `1 + 1 + 1`
2. `1 + 2`
3. `2 + 1`

### Constraints

- `1 <= n <= 45`

There is no official follow-up. (The answer for `n = 45` is `1,836,311,903`, which fits in a 32-bit signed integer; in Python integers never overflow anyway.)

---

## 3. Everyday Analogy

> **Explain it like I'm five**

Imagine you're standing on the top step and you look back down. How did you get here? There are only two possibilities:

- your **last move was a small hop** (1 step) from the step just below, or
- your **last move was a big jump** (2 steps) from two steps below.

So the number of ways to reach the top is: *(ways to reach the step just below) + (ways to reach the step two below)*.

It's like a family tree of paths: each step "inherits" all the paths from the two steps under it. If you write the answers from the bottom up — 1, 1, 2, 3, 5, 8, … — each number is just the sum of the two before it. You only ever need to remember the last two numbers you wrote.

---

## 4. Step-by-Step Logic

1. **Name the subproblem.** Let `ways(i)` = the number of ways to stand on step `i`.
2. **Look at the last move.** To stand on step `i`, the last move came from step `i - 1` (a 1-step) or from step `i - 2` (a 2-step). These two groups don't overlap (their last moves differ) and together cover every way.
3. **Recurrence:** `ways(i) = ways(i - 1) + ways(i - 2)`.
4. **Base cases:**
   - `ways(0) = 1` — standing at the bottom, there is exactly one way: make no moves.
   - `ways(1) = 1` — only `1`.
   - Check: `ways(2) = ways(1) + ways(0) = 2` ✅ and `ways(3) = 2 + 1 = 3` ✅ — both match the examples.
5. **Notice the pattern:** 1, 1, 2, 3, 5, 8, 13, … — the **Fibonacci numbers** (`ways(i)` is the `(i+1)`-th Fibonacci number).
6. **Plain recursion repeats work** (it recomputes `ways(3)` many times while computing `ways(5)`). Remembering answers (memoization) or building from the bottom (tabulation) fixes this.
7. **Each value needs only the previous two**, so two variables are enough — `O(1)` space.

---

## 5. Brute-Force Solution

### Algorithm

Translate the recurrence directly into recursion: `ways(n) = ways(n-1) + ways(n-2)`, with `ways(0) = ways(1) = 1`.

### Python code

```python
class Solution:
    def climbStairs(self, n: int) -> int:
        if n <= 1:          # step 0 or step 1: exactly one way
            return 1
        return self.climbStairs(n - 1) + self.climbStairs(n - 2)
```

### Explanation

- Each call splits into two smaller calls: "last move was 1 step" and "last move was 2 steps".
- The recursion stops at `n = 0` or `n = 1`, each contributing `1`.
- The answer is correct, because it literally counts every sequence of moves — it adds a `1` for each complete path.

### Complexity

- **Time:** `O(φ^n)` where `φ ≈ 1.618` (often loosely written `O(2^n)`). The call tree for `n` has `2 · ways(n) - 1` calls: 15 calls for `n = 5`, about 2.7 million for `n = 30`, and about **3.7 billion** for `n = 45`. In Python, `n = 30` already takes a noticeable fraction of a second, and `n = 45` would take minutes — **Time Limit Exceeded** near the top of the constraint range.
- **Auxiliary space:** `O(n)` for the recursion stack (the deepest chain is `n → n-1 → … → 1`).
- **Why so slow?** Overlapping subproblems. The call tree for `n = 5`:

```text
                     5
               /           \
             4               3
           /   \           /   \
          3     2         2     1
         / \   / \       / \
        2   1 1   0     1   0
       / \
      1   0
```

`ways(3)` is computed twice, `ways(2)` three times, and the repetition grows exponentially with `n`.

---

## 6. Optimized Solution

### Step 1 — Memoization (top-down DP)

Keep the recursion but **remember** each answer the first time it's computed. Every `ways(i)` for `i = 0..n` is then computed once.

```python
from functools import lru_cache


class Solution:
    def climbStairs(self, n: int) -> int:
        @lru_cache(maxsize=None)
        def ways(i: int) -> int:
            if i <= 1:
                return 1
            return ways(i - 1) + ways(i - 2)

        return ways(n)
```

- **Time:** `O(n)` — `n + 1` distinct states, each doing `O(1)` work after its two sub-results are known.
- **Auxiliary space:** `O(n)` — the cache plus a recursion stack of depth up to `n` (fine for `n <= 45`).

### Step 2 — Bottom-up table (tabulation)

Fill the answers from step 0 upward, so no recursion is needed.

```python
class Solution:
    def climbStairs(self, n: int) -> int:
        dp = [0] * (n + 1)
        dp[0] = 1                       # one way to stand at the bottom
        dp[1] = 1                       # only "1"
        for i in range(2, n + 1):
            dp[i] = dp[i - 1] + dp[i - 2]
        return dp[n]
```

`O(n)` time, `O(n)` auxiliary space for the table.

### Step 3 — Bottom-up with two variables (final, LeetCode-ready)

The table only ever reads the last two entries, so keep just those.

### Algorithm

1. `one_back = 1` (ways to reach step 1), `two_back = 1` (ways to reach step 0).
2. For each step `i` from 2 to `n`: the new count is `one_back + two_back`; shift the window: `two_back` becomes the old `one_back`, `one_back` becomes the new count.
3. Return `one_back`.

### Python code (LeetCode-ready)

```python
class Solution:
    def climbStairs(self, n: int) -> int:
        one_back, two_back = 1, 1          # ways(1), ways(0)
        for _ in range(2, n + 1):
            one_back, two_back = one_back + two_back, one_back
        return one_back                     # ways(n)
```

For `n = 1`, the loop body never runs and the function returns `1`.

---

## 7. Line-by-Line Explanation

(Two-variable bottom-up solution)

| Line | What it does | Why |
|---|---|---|
| `one_back, two_back = 1, 1` | `one_back` holds `ways(i-1)`, `two_back` holds `ways(i-2)`. Before the loop, they are `ways(1)` and `ways(0)`. | These are the base cases of the recurrence. |
| `for _ in range(2, n + 1):` | Computes `ways(2)`, `ways(3)`, …, `ways(n)` in order. | Each value depends only on smaller steps, which are already known. `_` signals that the loop index itself isn't used. |
| `one_back, two_back = one_back + two_back, one_back` | New `ways(i)` = sum of the previous two; the old `one_back` slides into `two_back`. | Python evaluates the whole right side **before** assigning, so both updates use the old values — no temporary variable needed. |
| `return one_back` | After the loop, `one_back` is `ways(n)`. | For `n = 1` the loop is skipped and `ways(1) = 1` is returned. |

**Why the simultaneous assignment matters:** writing it as two lines, `one_back = one_back + two_back` then `two_back = one_back`, would copy the *new* value into `two_back` — a bug. Either use the tuple assignment or a temporary variable.

---

## 8. Dry Run

**Input (Example 2):** `n = 3`

| Loop step | `i` (step being computed) | `one_back` before | `two_back` before | New `ways(i)` | `one_back` after | `two_back` after |
|---|---|---|---|---|---|---|
| start | — | — | — | — | 1 (`ways(1)`) | 1 (`ways(0)`) |
| 1 | 2 | 1 | 1 | 1 + 1 = 2 | 2 | 1 |
| 2 | 3 | 2 | 1 | 2 + 1 = 3 | 3 | 2 |

**Result:** `3` ✅

**Example 1:** `n = 2` → one loop iteration → `one_back = 2` → returns `2` ✅.

**Longer dry run:** `n = 5`

| `i` | `ways(i)` = `ways(i-1) + ways(i-2)` |
|---|---|
| 0 | 1 (base) |
| 1 | 1 (base) |
| 2 | 1 + 1 = 2 |
| 3 | 2 + 1 = 3 |
| 4 | 3 + 2 = 5 |
| 5 | 5 + 3 = **8** |

The 8 ways for `n = 5`: `11111`, `2111`, `1211`, `1121`, `1112`, `221`, `212`, `122` ✅.

---

## 9. Concepts, Data Structures, and Patterns

- **Dynamic programming (DP):** solve a problem by combining answers to smaller versions of itself, storing those answers so each is computed once. It needs:
  - *Optimal substructure / a recurrence:* `ways(i) = ways(i-1) + ways(i-2)`.
  - *Overlapping subproblems:* the same `ways(i)` is needed many times.
- **Top-down (memoization) vs bottom-up (tabulation):** memoization keeps the natural recursion and caches results (`functools.lru_cache` or a dict); tabulation fills an array from the base cases up. Both are `O(n)` here.
- **Space optimization ("rolling variables"):** when each state depends only on a fixed number of previous states, keep only those. The same trick turns Kadane's DP into two variables in [005_maximum_subarray.md](../01_array/005_maximum_subarray.md).
- **Counting by the last move:** split all solutions by their final choice into non-overlapping groups and add the counts. The same idea drives Coin Change ([056_coin_change.md](056_coin_change.md)), Decode Ways ([063_decode_ways.md](063_decode_ways.md)), and Unique Paths ([064_unique_paths.md](064_unique_paths.md)).
- **Fibonacci sequence:** `ways(n) = F(n+1)` with `F(1) = F(2) = 1`.
- **Close cousins:** House Robber ([061_house_robber.md](061_house_robber.md)) uses the same "look back one or two" shape with `max` instead of `+`.
- **Recursion vs backtracking:** the brute force here *counts* paths without listing them; when you need to *list* or *test* paths, as in [030_word_search.md](../05_matrix/030_word_search.md), you use backtracking — and you can't memoize away the exponential output (see Practice Question 3).

---

## 10. Complexity Analysis

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Plain recursion (brute force) | `O(φ^n)` ≈ `O(1.618^n)` | `O(n)` | `2 · ways(n) - 1` calls; recursion depth `n`. |
| Memoization (top-down) | `O(n)` | `O(n)` | `n + 1` cached states; cache + recursion stack. |
| Tabulation (bottom-up array) | `O(n)` | `O(n)` | One pass filling an array of size `n + 1`. |
| Two variables (optimized) | `O(n)` | `O(1)` | One pass, two integers. |

**Note on number size:** the answer grows exponentially, but for `n <= 45` it stays below `2^31`, so every addition is a constant-time operation. (There is also an `O(log n)` method using matrix exponentiation — see Practice Question 4 — but for `n <= 45` the simple loop is already instant.)

---

## 11. Edge Cases

| Case | Input | Expected result | Why |
|---|---|---|---|
| Smallest input | `n = 1` | `1` | Only `1`; the loop body never runs. |
| Example 1 | `n = 2` | `2` | `1+1`, `2`. |
| Example 2 | `n = 3` | `3` | `1+1+1`, `1+2`, `2+1`. |
| Small check | `n = 4` | `5` | `1111, 112, 121, 211, 22`. |
| Medium | `n = 10` | `89` | 11th Fibonacci number. |
| Largest input | `n = 45` | `1836311903` | Fast with the loop; the plain recursion would make about 3.7 billion calls. |

---

## 12. Common Mistakes and Debugging

1. **Wrong base cases.** Using `ways(1) = 1, ways(2) = 1` (or forgetting `ways(0) = 1`) shifts the whole sequence. Check your base cases against both examples.
2. **Off-by-one loop bounds.** `range(2, n)` stops one step early; you need `range(2, n + 1)`.
3. **Sequential (non-simultaneous) updates.** `a = a + b; b = a` overwrites `a` before `b` reads it. Use `a, b = a + b, a`.
4. **Submitting plain recursion.** It's correct but exponential; it times out for the larger tests near `n = 45`.
5. **Indexing a DP array for `n = 1`.** Writing `dp = [0] * (n + 1); dp[2] = 2` crashes when `n = 1` (the array has only 2 slots). Set only `dp[0]` and `dp[1]`, or handle `n = 1` first.
6. **Treating `1 + 2` and `2 + 1` as the same way.** Order matters here; counting unordered combinations is a different problem.

**Debugging tip:** print the first ten answers (`1, 2, 3, 5, 8, 13, 21, 34, 55, 89` for `n = 1..10`) and compare with your function.

---

## 13. Practice Questions

**Q1. What is `climbStairs(7)`, and how do you get it quickly by hand?**

<details><summary>Hint</summary>Keep adding the last two numbers starting from 1, 1.</summary></details>

**Answer:** `1, 1, 2, 3, 5, 8, 13, 21` for `n = 0..7`, so `climbStairs(7) = 21`.

**Q2. Now you may climb 1, 2, or 3 steps at a time. How many ways for `n` steps?**

<details><summary>Hint</summary>Look at the last move again: it came from `i-1`, `i-2`, or `i-3`.</summary></details>

**Answer:** `ways(i) = ways(i-1) + ways(i-2) + ways(i-3)` with `ways(0) = 1`, and steps below 0 contribute 0 (the "tribonacci" shape).

```python
def climb_123(n):
    a, b, c = 0, 0, 1          # ways(-2), ways(-1), ways(0)
    for _ in range(n):
        a, b, c = b, c, a + b + c
    return c


assert climb_123(1) == 1
assert climb_123(2) == 2       # 1+1, 2
assert climb_123(3) == 4       # 1+1+1, 1+2, 2+1, 3
assert climb_123(4) == 7
```

**Q3. List every way for small `n` (as tuples of moves). Why can't memoization make this fast for big `n`?**

<details><summary>Hint</summary>Use backtracking: try a 1-step, recurse, undo; try a 2-step, recurse, undo.</summary></details>

**Answer:**

```python
def all_ways(n):
    result, path = [], []

    def backtrack(remaining):
        if remaining == 0:
            result.append(tuple(path))
            return
        for move in (1, 2):
            if move <= remaining:
                path.append(move)
                backtrack(remaining - move)
                path.pop()

    backtrack(n)
    return result


assert all_ways(3) == [(1, 1, 1), (1, 2), (2, 1)]
assert len(all_ways(10)) == 89
```

The **output itself** has `ways(n)` items (exponentially many), so any method that lists them takes exponential time. DP only makes **counting** fast.

**Q4. (Min Cost Climbing Stairs, LeetCode 746) Each step `i` has a cost `cost[i]` you pay when you leave it. You may start at step 0 or step 1. What is the minimum cost to reach the top (just past the last step)?**

<details><summary>Hint</summary>Same "came from one or two back" shape, but with `min` and costs instead of `+` on counts.</summary></details>

**Answer:** `best(i) = min(best(i-1) + cost[i-1], best(i-2) + cost[i-2])`, with `best(0) = best(1) = 0`.

```python
def min_cost_climbing_stairs(cost):
    two_back, one_back = 0, 0                  # best(0), best(1)
    for i in range(2, len(cost) + 1):
        two_back, one_back = one_back, min(one_back + cost[i - 1], two_back + cost[i - 2])
    return one_back


assert min_cost_climbing_stairs([10, 15, 20]) == 15
assert min_cost_climbing_stairs([1, 100, 1, 1, 1, 100, 1, 1, 100, 1]) == 6
```

**Q5. (Challenge) Compute `climbStairs(n)` in `O(log n)` arithmetic steps.**

<details><summary>Hint</summary>`[[1, 1], [1, 0]]` raised to the power `k` contains Fibonacci numbers. Use fast exponentiation (square-and-multiply).</summary></details>

**Answer:**

```python
def mat_mult(a, b):
    return [[a[0][0] * b[0][0] + a[0][1] * b[1][0], a[0][0] * b[0][1] + a[0][1] * b[1][1]],
            [a[1][0] * b[0][0] + a[1][1] * b[1][0], a[1][0] * b[0][1] + a[1][1] * b[1][1]]]


def climb_fast(n):
    result = [[1, 0], [0, 1]]                  # identity matrix
    base = [[1, 1], [1, 0]]
    power = n
    while power:
        if power & 1:
            result = mat_mult(result, base)
        base = mat_mult(base, base)
        power >>= 1
    return result[0][0]                        # [[F(n+1), F(n)], [F(n), F(n-1)]]


assert climb_fast(1) == 1
assert climb_fast(3) == 3
assert climb_fast(45) == 1836311903
assert [climb_fast(n) for n in (2, 5, 10)] == [2, 8, 89]
```

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** 1-D DP (Fibonacci).
- **Key idea:** The last move is a 1-step or a 2-step, so `ways(n) = ways(n-1) + ways(n-2)`, with `ways(0) = ways(1) = 1`. Keep only the last two values.
- **Time:** `O(n)`.
- **Auxiliary space:** `O(1)`.
- **One-line memory hook:** *"Every step inherits the paths of the two steps below it."*

### Completion checklist

- [x] Problem requirements verified
- [x] Examples and constraints verified
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force (plain recursion) solution written and tested
- [x] Memoization, tabulation, and optimized two-variable solutions written and tested (`tools/tests/p055.py`)
- [x] Line-by-line explanation written
- [x] Dry run completed with real examples
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
