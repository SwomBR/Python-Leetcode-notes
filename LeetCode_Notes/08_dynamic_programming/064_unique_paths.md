# 064. Unique Paths

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Unique Paths |
| **LeetCode number** | 62 |
| **Topic (source list)** | Dynamic Programming |
| **Also uses** | Math (Combinatorics), Matrix / Grid |
| **Difficulty** | Medium |
| **LeetCode URL** | <https://leetcode.com/problems/unique-paths/> |
| **Pattern** | 2-D grid DP (`ways = from above + from left`), compressible to one row; or a binomial coefficient |

---

## 2. Problem Explanation

### What are we given?

Two integers:

- `m` — the number of **rows** in a grid,
- `n` — the number of **columns**.

A robot starts in the **top-left** cell `(0, 0)` and wants to reach the **bottom-right** cell `(m - 1, n - 1)`.

### What must we return?

The **number of different routes** the robot can take.

### The rules

1. At every step the robot moves **one cell right** or **one cell down**. It can never move up or left.
2. Two routes are different if their sequences of moves differ.
3. The test cases guarantee that the answer is **at most `2 * 10^9`**.

### Examples

**Example 1**

```text
Input:  m = 3, n = 7
Output: 28
```

A 3-row, 7-column grid has 28 different right/down routes from corner to corner.

**Example 2**

```text
Input:  m = 3, n = 2
Output: 3
```

The three routes are:

1. Right → Down → Down
2. Down → Down → Right
3. Down → Right → Down

### Constraints

- `1 <= m, n <= 100`

(Plus the guarantee above: the answer is `<= 2 * 10^9`.)

There is no follow-up in the official statement.

---

## 3. Everyday Analogy

> **Explain it like I'm five**

Imagine a town with streets in a perfect grid. You live at the top-left corner and your school is at the bottom-right corner. You're in a hurry, so you only ever walk **towards** school: right or down, never backwards.

How many different ways can you walk to school?

Stand on any street corner and ask: *"How did I get here?"* You must have arrived either **from the corner above** or **from the corner to the left**. So:

> ways to reach this corner = ways to reach the corner above + ways to reach the corner to the left.

Corners along the top edge can only be reached one way (walk right, right, right…), and corners down the left edge also only one way (down, down, down…). Fill in the rest of the map with the rule above, and the number written on the school corner is the answer.

---

## 4. Step-by-Step Logic

We follow the **DP recipe**.

1. **State definition.** `dp[r][c]` = number of routes from `(0, 0)` to cell `(r, c)`.
2. **Recurrence.** The last move into `(r, c)` came from above `(r-1, c)` or from the left `(r, c-1)`. These two groups of routes don't overlap (their last moves differ), so we **add**:

   `dp[r][c] = dp[r-1][c] + dp[r][c-1]`
3. **Base cases.** Every cell in row 0 has `dp = 1` (only "all right"), and every cell in column 0 has `dp = 1` (only "all down"). This includes the start: `dp[0][0] = 1` (the "empty route").
4. **Iteration order.** Row by row, left to right — then the cell above and the cell to the left are always ready.
5. **Answer location.** `dp[m-1][n-1]`.
6. **Space trick.** A row only needs the row above it. Keep a single list `row` of length `n`: before updating, `row[c]` still holds the value from the row above, and `row[c-1]` already holds the new value to the left. So `row[c] += row[c-1]`.
7. **Math shortcut.** Every route is exactly `m - 1` downs and `n - 1` rights in some order — `m + n - 2` moves in total. A route is determined by **which** of those moves are downs, so the count is the binomial coefficient `C(m + n - 2, m - 1)`.

---

## 5. Brute-Force Solution

### Algorithm (plain recursion)

`paths(r, c)` = number of routes from `(r, c)` to the target.

- If `(r, c)` is the target → `1`.
- If `(r, c)` is outside the grid → `0`.
- Otherwise → `paths(r + 1, c) + paths(r, c + 1)` (go down, or go right).

### Python code

```python
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        def paths(r: int, c: int) -> int:
            if r == m - 1 and c == n - 1:   # reached the target
                return 1
            if r >= m or c >= n:            # walked off the grid
                return 0
            return paths(r + 1, c) + paths(r, c + 1)

        return paths(0, 0)
```

### Explanation

- The recursion literally walks every route, so the result is correct.
- But it walks them **one at a time**: the work is at least proportional to the answer itself. Many cells are reached by many different routes, and each time the whole sub-count below that cell is redone.

### Complexity

- **Time:** exponential — each call branches into two, and the depth is up to `m + n - 2`, so it is `O(2^(m+n))`. Even `m = n = 20` needs tens of billions of calls; `m = n = 100` is hopeless. It would **time out** on LeetCode.
- **Auxiliary space:** `O(m + n)` — the recursion depth (one frame per move).

### The bridge — memoization

There are only `m × n` different cells, so cache `paths(r, c)`:

```python
from functools import lru_cache


class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        @lru_cache(maxsize=None)
        def paths(r: int, c: int) -> int:
            if r == m - 1 or c == n - 1:   # last row/column: only one way left
                return 1
            return paths(r + 1, c) + paths(r, c + 1)

        return paths(0, 0)
```

Here we also use a shortcut base case: from anywhere in the last row (or last column) there is exactly one way to finish. Time and space become `O(m × n)`.

---

## 6. Optimized Solution

### Idea — bottom-up DP with one row

Fill the DP table row by row, but store only one row. Updating `row[c] += row[c-1]` adds "from the left" (`row[c-1]`, already updated for this row) to "from above" (`row[c]`, still holding the previous row's value).

### Algorithm

1. `row = [1] * n` — the first row is all 1s.
2. Repeat `m - 1` times (once for each remaining row):
   - for `c` from 1 to `n - 1`: `row[c] += row[c - 1]`.
   - (`row[0]` stays 1 — the left column has one route.)
3. Return `row[n - 1]`.

### Python code (LeetCode-ready)

```python
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        row = [1] * n                      # first row: one route to each cell

        for _ in range(1, m):              # rows 1 .. m-1
            for c in range(1, n):          # column 0 always stays 1
                row[c] += row[c - 1]       # from above (old row[c]) + from left

        return row[n - 1]
```

### Full 2-D table version (easier to visualise)

```python
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        dp = [[1] * n for _ in range(m)]   # row 0 and column 0 are all 1
        for r in range(1, m):
            for c in range(1, n):
                dp[r][c] = dp[r - 1][c] + dp[r][c - 1]
        return dp[m - 1][n - 1]
```

### Alternative — combinatorics `C(m + n - 2, m - 1)`

```python
import math


class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        # Every route = (m - 1) downs + (n - 1) rights, in some order.
        # Choose which of the m + n - 2 moves are downs.
        return math.comb(m + n - 2, m - 1)
```

`math.comb` (Python 3.8+) computes the exact integer; no floating-point rounding. For `m = 3, n = 7`: `C(8, 2) = 8 × 7 / 2 = 28` ✅.

---

## 7. Line-by-Line Explanation

(One-row DP)

| Line | What it does | Why |
|---|---|---|
| `row = [1] * n` | `row[c] = dp[0][c] = 1` for all columns. | In the top row the robot can only move right, so each cell has one route. |
| `for _ in range(1, m):` | Processes rows 1 to `m-1`. | Row 0 is already done. If `m = 1` the loop doesn't run and the answer is 1. |
| `for c in range(1, n):` | Processes columns 1 to `n-1`. | Column 0 is always 1 (only "all down"), so `row[0]` never changes. |
| `row[c] += row[c - 1]` | `new row[c] = old row[c] + new row[c-1]`. | Old `row[c]` = `dp[r-1][c]` (from above); `row[c-1]` was just updated = `dp[r][c-1]` (from the left). Left-to-right order makes this work. |
| `return row[n - 1]` | `dp[m-1][n-1]`. | Routes to the bottom-right cell. |

---

## 8. Dry Run

**Input:** `m = 3, n = 7` (Example 1).

**2-D DP table** (each cell = cell above + cell to the left):

| row \ col | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| **0** | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| **1** | 1 | 1+1=2 | 1+2=3 | 1+3=4 | 1+4=5 | 1+5=6 | 1+6=7 |
| **2** | 1 | 2+1=3 | 3+3=6 | 4+6=10 | 5+10=15 | 6+15=21 | 7+21=**28** |

**The same thing with one row:**

| After processing | `row` |
|---|---|
| start (row 0) | `[1, 1, 1, 1, 1, 1, 1]` |
| row 1 | `[1, 2, 3, 4, 5, 6, 7]` |
| row 2 | `[1, 3, 6, 10, 15, 21, 28]` |

Inside row 2, for example at `c = 3`: old `row[3] = 4` (from above) plus new `row[2] = 6` (from the left) → `10`.

**Result:** `28` ✅ — and `C(3 + 7 - 2, 3 - 1) = C(8, 2) = 28` ✅.

**Second dry run:** `m = 3, n = 2` (Example 2)

| After processing | `row` | Detail |
|---|---|---|
| start (row 0) | `[1, 1]` | |
| row 1 | `[1, 2]` | `row[1] = 1 + 1` |
| row 2 | `[1, 3]` | `row[1] = 2 + 1` |

**Result:** `3` ✅ (and `C(3, 2) = 3`).

---

## 9. Concepts, Data Structures, and Patterns

- **DP recipe on a grid:** state `dp[r][c]`, recurrence "above + left", base = first row/column all 1, row-major order, answer at the bottom-right.
- **Counting by last move:** split the routes into a cell by how they arrived; the groups are disjoint, so counts add (the same "sum rule" as [063_decode_ways.md](063_decode_ways.md) and [055_climbing_stairs.md](055_climbing_stairs.md)).
- **Rolling array:** a 2-D table where each row needs only the previous row can be squeezed into one 1-D list updated in place — the update direction (left to right) matters.
- **Combinatorics:** routes ↔ arrangements of `m-1` `D`s and `n-1` `R`s ↔ `C(m+n-2, m-1)` (Pascal's triangle — the DP table *is* a rotated Pascal's triangle).
- **Grid problems in this project:** [../05_matrix/027_set_matrix_zeroes.md](../05_matrix/027_set_matrix_zeroes.md), [../05_matrix/030_word_search.md](../05_matrix/030_word_search.md); 2-D DP tables also appear in [058_longest_common_subsequence.md](058_longest_common_subsequence.md).
- **Follow-on problems:** Unique Paths II (LeetCode 63, obstacles) and Minimum Path Sum (LeetCode 64) — see practice questions.

---

## 10. Complexity Analysis

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Plain recursion | `O(2^(m+n))` | `O(m + n)` | Two branches per call, depth up to `m + n - 2`. |
| Memoization | `O(m·n)` | `O(m·n)` | Each cell computed once; cache of `m·n` entries plus `O(m + n)` stack. |
| 2-D DP table | `O(m·n)` | `O(m·n)` | Every cell filled once. |
| One-row DP (optimized) | `O(m·n)` | `O(n)` | Same work, one row of `n` numbers. (Use `min(m, n)` as the row length for `O(min(m, n))` space — the grid is symmetric.) |
| `math.comb` | `O(min(m, n))` arithmetic steps | `O(1)` | Computes the binomial coefficient with about `min(m-1, n-1)` multiplications/divisions on small integers. |

With `m, n <= 100`, the DP does at most 10,000 additions — instant.

---

## 11. Edge Cases

| Case | Example | Expected result | Why |
|---|---|---|---|
| Single cell | `m = 1, n = 1` | `1` | Already at the target: the empty route counts once. |
| Single row | `m = 1, n = 9` | `1` | Only "right, right, …". |
| Single column | `m = 9, n = 1` | `1` | Only "down, down, …". |
| 2 × 2 | `m = 2, n = 2` | `2` | Right-Down or Down-Right. |
| 3 × 3 | `m = 3, n = 3` | `6` | `C(4, 2) = 6`. |
| Swapped dimensions | `m = 7, n = 3` | `28` | Symmetric: `C(8, 6) = C(8, 2)`. |

---

## 12. Common Mistakes and Debugging

1. **Mixing up rows and columns.** `m` is rows, `n` is columns. The answer happens to be symmetric, but a 2-D table indexed wrongly will crash with `IndexError` when `m != n`.
2. **Initialising the first row/column to 0.** Then everything stays 0. Edge cells have exactly one route.
3. **Wrong update direction in the 1-D version.** Iterating `c` from right to left would use the *old* `row[c-1]` (the row above) instead of the new left neighbour.
4. **`[[1] * n] * m` for the 2-D table.** That creates `m` references to the **same** row; changing one row changes all. Use a list comprehension.
5. **Using floating point for combinations** (e.g. `factorial(a) / (factorial(b) * factorial(c))`): `/` makes a float, which can round for big values. Use `math.comb` or `//`.
6. **Off-by-one in the formula.** The robot makes `m - 1` downs and `n - 1` rights, not `m` and `n`: it is `C(m+n-2, m-1)`, not `C(m+n, m)`.

**Debugging tip:** print the table for `m = 3, n = 3` — it must be `[[1,1,1],[1,2,3],[1,3,6]]`.

---

## 13. Practice Questions

**Q1. How many routes are there in a 3 × 3 grid? Show the table and check with the formula.**

<details><summary>Hint</summary>Build rows `[1,1,1]`, then add left neighbours.</summary></details>

**Answer:** Rows: `[1, 1, 1]` → `[1, 2, 3]` → `[1, 3, 6]`. The answer is `6`, and `C(3 + 3 - 2, 3 - 1) = C(4, 2) = 6` ✅.

**Q2. Unique Paths II (LeetCode 63): some cells contain obstacles (`1`) the robot cannot enter. Count the routes.**

<details><summary>Hint</summary>Same recurrence, but a cell with an obstacle has 0 routes. The first row/column is no longer automatically all 1s — an obstacle blocks everything after it.</summary></details>

**Answer:**

```python
def unique_paths_with_obstacles(grid):
    cols = len(grid[0])
    row = [0] * cols
    row[0] = 1 if grid[0][0] == 0 else 0
    for r in range(len(grid)):
        for c in range(cols):
            if grid[r][c] == 1:
                row[c] = 0                 # blocked cell: no route ends here
            elif c > 0:
                row[c] += row[c - 1]       # from above (old) + from left (new)
    return row[-1]


assert unique_paths_with_obstacles([[0, 0, 0], [0, 1, 0], [0, 0, 0]]) == 2
assert unique_paths_with_obstacles([[0, 1], [0, 0]]) == 1
assert unique_paths_with_obstacles([[1]]) == 0
assert unique_paths_with_obstacles([[0, 0], [0, 0]]) == 2
```

**Q3. Minimum Path Sum (LeetCode 64): each cell has a cost; find the cheapest right/down route's total cost.**

<details><summary>Hint</summary>Replace "+" between the two incoming options by `min`, and add the cell's own cost.</summary></details>

**Answer:**

```python
def min_path_sum(grid):
    rows, cols = len(grid), len(grid[0])
    best = [float("inf")] * cols
    best[0] = 0
    for r in range(rows):
        best[0] += grid[r][0]
        for c in range(1, cols):
            best[c] = min(best[c], best[c - 1]) + grid[r][c]
    return best[-1]


assert min_path_sum([[1, 3, 1], [1, 5, 1], [4, 2, 1]]) == 7
assert min_path_sum([[1, 2, 3], [4, 5, 6]]) == 12
```

**Q4. Why is `C(m+n-2, m-1)` equal to `C(m+n-2, n-1)`?**

<details><summary>Hint</summary>Choosing which moves are downs vs. choosing which are rights.</summary></details>

**Answer:** Picking the positions of the `m-1` downs automatically fixes the positions of the `n-1` rights (they're the remaining moves), and vice versa. In general `C(k, j) = C(k, k - j)`, and here `k - (m-1) = n-1`.

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** 2-D grid counting DP → one rolling row; or binomial coefficient.
- **State:** `dp[r][c]` = routes from the start to `(r, c)`.
- **Recurrence:** `dp[r][c] = dp[r-1][c] + dp[r][c-1]`; first row and column are 1.
- **Time:** `O(m·n)` DP (or `O(min(m, n))` with `math.comb`).
- **Auxiliary space:** `O(n)` one-row DP (`O(1)` for `math.comb`).
- **One-line memory hook:** *"You came from above or from the left — add them up."*

### Completion checklist

- [x] Problem requirements verified
- [x] Examples and constraints verified (including the `2 * 10^9` answer bound)
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force (recursion) and memoized solutions written and tested
- [x] Optimized Python solution (one row), 2-D table version and `math.comb` alternative written and tested (`tools/tests/p064.py`)
- [x] Line-by-line explanation written
- [x] Dry run completed with real examples
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
