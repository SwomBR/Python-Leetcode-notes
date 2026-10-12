# 028. Spiral Matrix

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Spiral Matrix |
| **LeetCode number** | 54 |
| **Topic (source list)** | Matrix |
| **Also uses** | Array, Simulation |
| **Difficulty** | Medium |
| **LeetCode URL** | <https://leetcode.com/problems/spiral-matrix/> |
| **Pattern** | Layer-by-layer traversal with four shrinking boundaries |

---

## 2. Problem Explanation

### What are we given?

`matrix` — a grid of integers with `m` rows and `n` columns. It does **not** have to be square.

### What must we return?

A flat list of **all** the numbers in the grid, read in **spiral order**: start at the top-left corner, go right along the top, down the right side, left along the bottom, up the left side, and then keep curling inward clockwise until every cell has been read exactly once.

### The rules

1. Every cell appears in the output **exactly once**.
2. The direction is always **clockwise**, starting by moving **right** from the top-left cell.
3. The matrix itself is not changed; we just read it.

### Examples

**Example 1**

```text
Input:  matrix = [[1,2,3],[4,5,6],[7,8,9]]
Output: [1,2,3,6,9,8,7,4,5]
```

```text
1 → 2 → 3
          ↓
4 → 5     6
↑         ↓
7 ← 8 ← 9
```

Outer ring: `1,2,3,6,9,8,7,4`; then the centre `5`.

**Example 2**

```text
Input:  matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]
Output: [1,2,3,4,8,12,11,10,9,5,6,7]
```

```text
 1 →  2 →  3 →  4
                ↓
 5 →  6 →  7    8
 ↑              ↓
 9 ← 10 ← 11 ← 12
```

Outer ring: `1,2,3,4,8,12,11,10,9,5`; inner strip: `6,7`.

### Constraints

- `m == matrix.length`
- `n == matrix[i].length`
- `1 <= m, n <= 10`
- `-100 <= matrix[i][j] <= 100`

There is no official follow-up.

---

## 3. Everyday Analogy

> **Explain it like I'm five**

Think of peeling an onion — or eating a square cake by always biting around the outside edge.

You walk around the **outer edge** of the cake clockwise: along the top, down the right side, back along the bottom, up the left side. Once the outside ring is eaten, there's a smaller cake left in the middle. You do the exact same walk on the smaller cake, and keep going until nothing is left.

To know where the "edge" is each time, you keep four fences: a **top fence**, a **bottom fence**, a **left fence** and a **right fence**. Each time you finish one side, you move that fence one step inward.

---

## 4. Step-by-Step Logic

1. **See the repeating pattern.** A spiral is just rings (layers) peeled from the outside in. Each ring is four straight walks: right, down, left, up.
2. **Track the unread rectangle** with four indices: `top`, `bottom`, `left`, `right`. Everything outside them has been read.
3. **Walk right** along row `top` from `left` to `right`; then the top row is done → `top += 1`.
4. **Walk down** column `right` from `top` to `bottom`; then the right column is done → `right -= 1`.
5. **Walk left** along row `bottom` from `right` to `left` — but **only if `top <= bottom`**, i.e. a row is still left. Then `bottom -= 1`.
6. **Walk up** column `left` from `bottom` to `top` — **only if `left <= right`**. Then `left += 1`.
7. **Repeat** while `top <= bottom and left <= right`.
8. **Why the two extra checks?** When the leftover part is a single row or a single column, the "walk right" or "walk down" already read it. Without the checks, the "walk left" or "walk up" would read the same cells **again**.

---

## 5. Brute-Force Solution

### Algorithm — "walk like a robot"

1. Keep a `seen` grid of booleans, all `False`.
2. Start at `(0, 0)` facing right. Directions in clockwise order: right, down, left, up.
3. Repeat `m × n` times: record the current cell and mark it seen. Look at the next cell in the current direction; if it is outside the grid or already seen, **turn clockwise**. Move.

### Python code

```python
from typing import List


class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        m, n = len(matrix), len(matrix[0])
        seen = [[False] * n for _ in range(m)]
        dr = [0, 1, 0, -1]          # right, down, left, up
        dc = [1, 0, -1, 0]
        result = []
        r = c = d = 0
        for _ in range(m * n):
            result.append(matrix[r][c])
            seen[r][c] = True
            nr, nc = r + dr[d], c + dc[d]
            if not (0 <= nr < m and 0 <= nc < n) or seen[nr][nc]:
                d = (d + 1) % 4     # turn clockwise
                nr, nc = r + dr[d], c + dc[d]
            r, c = nr, nc
        return result
```

### Explanation

- The robot moves straight until it would hit a wall or a visited cell, then turns right. That produces the spiral automatically.
- We loop exactly `m × n` times, so every cell is recorded once. After the last cell the robot may "move" to an invalid position, but the loop ends before reading it.
- One turn is always enough: after turning, the next cell is guaranteed to be valid whenever cells remain.

### Complexity

- **Time:** `O(mn)` — each cell is visited once with constant work.
- **Auxiliary space:** `O(mn)` for the `seen` grid (the output list is required and not counted). This extra grid is the trade-off: the optimized version replaces it with four integers.

---

## 6. Optimized Solution

### Idea

Instead of remembering every visited cell, remember only the **boundaries** of the unvisited rectangle. Shrink a boundary after walking its side.

### Algorithm

1. `top, bottom, left, right = 0, m - 1, 0, n - 1`.
2. While `top <= bottom and left <= right`:
   - read row `top` left→right; `top += 1`
   - read column `right` top→bottom; `right -= 1`
   - if `top <= bottom`: read row `bottom` right→left; `bottom -= 1`
   - if `left <= right`: read column `left` bottom→top; `left += 1`
3. Return the result.

### Python code (LeetCode-ready)

```python
from typing import List


class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        result = []
        top, bottom = 0, len(matrix) - 1
        left, right = 0, len(matrix[0]) - 1

        while top <= bottom and left <= right:
            # Top row: left -> right
            for j in range(left, right + 1):
                result.append(matrix[top][j])
            top += 1

            # Right column: top -> bottom
            for i in range(top, bottom + 1):
                result.append(matrix[i][right])
            right -= 1

            # Bottom row: right -> left (only if a row remains)
            if top <= bottom:
                for j in range(right, left - 1, -1):
                    result.append(matrix[bottom][j])
                bottom -= 1

            # Left column: bottom -> top (only if a column remains)
            if left <= right:
                for i in range(bottom, top - 1, -1):
                    result.append(matrix[i][left])
                left += 1

        return result
```

---

## 7. Line-by-Line Explanation

| Line | What it does | Why |
|---|---|---|
| `result = []` | Output list. | Collects values in spiral order. |
| `top, bottom = 0, len(matrix) - 1` | First and last unread rows. | Start with the whole grid. |
| `left, right = 0, len(matrix[0]) - 1` | First and last unread columns. | Start with the whole grid. |
| `while top <= bottom and left <= right:` | Continue while the unread rectangle is non-empty. | When a pair of fences crosses, every cell has been read. |
| `for j in range(left, right + 1):` | Walk the top row to the right. | `right + 1` because `range` excludes its end. |
| `top += 1` | The top row is finished. | Move the top fence down. |
| `for i in range(top, bottom + 1):` | Walk the right column downward. | Starts at the new `top`, so the corner is not read twice. |
| `right -= 1` | The right column is finished. | Move the right fence left. |
| `if top <= bottom:` | Is there still an unread row? | Prevents re-reading a single remaining row. |
| `for j in range(right, left - 1, -1):` | Walk the bottom row to the left. | `left - 1` as the stop so `left` itself is included. |
| `bottom -= 1` | The bottom row is finished. | Move the bottom fence up. |
| `if left <= right:` | Is there still an unread column? | Prevents re-reading a single remaining column. |
| `for i in range(bottom, top - 1, -1):` | Walk the left column upward. | Stops at `top`, which is already below the finished top row. |
| `left += 1` | The left column is finished. | Move the left fence right. |
| `return result` | Done. | Contains all `m × n` values. |

---

## 8. Dry Run

**Input:** `matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]` (official Example 2)

```text
        c0  c1  c2  c3
  r0 [   1   2   3   4 ]
  r1 [   5   6   7   8 ]
  r2 [   9  10  11  12 ]
```

Start: `top=0, bottom=2, left=0, right=3`.

| Step | Walk | Cells read | Values added | Fences after | `result` so far |
|---|---|---|---|---|---|
| 1 | top row → | (0,0)…(0,3) | 1, 2, 3, 4 | `top=1` | `[1,2,3,4]` |
| 2 | right col ↓ | (1,3), (2,3) | 8, 12 | `right=2` | `[1,2,3,4,8,12]` |
| 3 | `top(1) <= bottom(2)` ✔ bottom row ← | (2,2), (2,1), (2,0) | 11, 10, 9 | `bottom=1` | `[…,12,11,10,9]` |
| 4 | `left(0) <= right(2)` ✔ left col ↑ | (1,0) | 5 | `left=1` | `[…,9,5]` |
| — | loop check: `1<=1` and `1<=2` ✔ | | | | |
| 5 | top row → | (1,1), (1,2) | 6, 7 | `top=2` | `[…,5,6,7]` |
| 6 | right col ↓ `range(2, 2)` | none | — | `right=1` | unchanged |
| 7 | `top(2) <= bottom(1)` ✘ skip | | | | |
| 8 | `left(1) <= right(1)` ✔ left col ↑ `range(1, 1, -1)` | none | — | `left=2` | unchanged |
| — | loop check: `2 <= 1` ✘ stop | | | | |

After the first ring the unread part is just the strip `6 7`:

```text
        c0  c1  c2  c3
  r0 [   .   .   .   . ]
  r1 [   .   6   7   . ]
  r2 [   .   .   .   . ]
```

**Result:** `[1,2,3,4,8,12,11,10,9,5,6,7]` ✅

### Second dry run — official Example 1 (3 × 3)

| Ring | Walks | Values | Fences after |
|---|---|---|---|
| 1 | → `1,2,3`; ↓ `6,9`; ← `8,7`; ↑ `4` | `1,2,3,6,9,8,7,4` | `top=1, bottom=1, left=1, right=1` |
| 2 | → `5`; ↓ none (`range(2,2)`); ← skipped (`top=2 > bottom=1`); ↑ skipped (`left=1 > right=0`) | `5` | `top=2, bottom=1, left=1, right=0` → loop stops |

**Result:** `[1,2,3,6,9,8,7,4,5]` ✅

---

## 9. Concepts, Data Structures, and Patterns

- **Matrix indexing:** `matrix[row][col]`; rows grow downward, columns grow to the right.
- **Boundary (fence) pointers:** four indices describing a shrinking rectangle — the 2D cousin of the two-pointer technique in [Container With Most Water](../01_array/010_container_with_most_water.md).
- **Simulation with direction vectors:** the `dr`/`dc` arrays in the brute force are the same tool used in grid searches such as [Word Search](030_word_search.md) and [Number of Islands](../09_graph/069_number_of_islands.md).
- **Python `range` with a negative step:** `range(right, left - 1, -1)` counts down and includes `left`.
- **Layers of a matrix:** the same ring-by-ring view is used in [Rotate Image](029_rotate_image.md).
- **Related:** [Set Matrix Zeroes](027_set_matrix_zeroes.md).

---

## 10. Complexity Analysis

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Brute force (robot + `seen` grid) | `O(mn)` | `O(mn)` | Each cell visited once; the `seen` grid has `m × n` booleans. |
| Optimized (four boundaries) | `O(mn)` | `O(1)` | Each cell is appended exactly once; only four integers and loop variables are extra. The output list (`m × n` values) is required by the problem and not counted. |

With `m, n <= 10` both versions are instant; the optimized one is the standard interview answer because it needs no extra grid.

---

## 11. Edge Cases

| Case | Input | Expected result | Why |
|---|---|---|---|
| Single cell | `[[7]]` | `[7]` | One step right, then fences cross. |
| Single row | `[[1,2,3]]` | `[1,2,3]` | The bottom-row walk is skipped by `top <= bottom`. |
| Single column | `[[1],[2],[3]]` | `[1,2,3]` | The left-column walk is skipped by `left <= right`. |
| Wide rectangle | `[[1,2,3],[4,5,6]]` | `[1,2,3,6,5,4]` | Two rows: one ring and done. |
| Tall rectangle | `[[1,2],[3,4],[5,6]]` | `[1,2,4,6,5,3]` | Two columns: one ring and done. |
| Square, odd size | `[[1,2,3],[4,5,6],[7,8,9]]` | `[1,2,3,6,9,8,7,4,5]` | Centre cell read last. |
| Negative values | `[[-100,100]]` | `[-100,100]` | Values do not affect the order. |

---

## 12. Common Mistakes and Debugging

1. **Missing the `top <= bottom` / `left <= right` checks.** Without them `[[1,2,3]]` returns `[1,2,3,2,1]` and `[[1],[2],[3]]` returns `[1,2,3,2]` — cells read twice. Always test a single row and a single column.
2. **Off-by-one in `range`.** `range(left, right + 1)` includes `right`; `range(right, left - 1, -1)` includes `left`. Forgetting the `+1`/`-1` drops corner cells.
3. **Updating a fence before using it.** The right-column walk must start at the **already incremented** `top`, otherwise the top-right corner is read twice.
4. **Assuming the matrix is square.** Use `len(matrix)` for rows and `len(matrix[0])` for columns.
5. **Turning only when hitting the wall** in the brute force (forgetting the `seen` check) — the robot would walk back over the outer ring forever.

**Debugging tip:** assert `len(result) == m * n` at the end. Too many values means a duplicated walk; too few means a missed corner.

---

## 13. Practice Questions

**Q1. What is the spiral order of `[[1,2,3],[4,5,6],[7,8,9],[10,11,12]]` (4 rows, 3 columns)?**

<details><summary>Hint</summary>Outer ring first (10 cells), then the inner column of two cells, read top to bottom.</summary></details>

**Answer:** Outer ring: `1,2,3,6,9,12,11,10,7,4`. Remaining fences `top=1, bottom=2, left=1, right=1` → the inner column `5,8`: the "top row →" walk reads `5` (`top` becomes 2), then the "right column ↓" walk reads `8`; the ← walk reads nothing (`range(0, 0, -1)` is empty) and the ↑ walk is skipped because `left=1 > right=0`. Final: `[1,2,3,6,9,12,11,10,7,4,5,8]`.

**Q2. (Spiral Matrix II) Generate an `n × n` matrix filled with `1, 2, …, n²` in spiral order.**

<details><summary>Hint</summary>Same four fences, but **write** a counter into each cell instead of reading.</summary></details>

**Answer:**

```python
def generate_spiral(n):
    grid = [[0] * n for _ in range(n)]
    top, bottom, left, right = 0, n - 1, 0, n - 1
    value = 1
    while top <= bottom and left <= right:
        for j in range(left, right + 1):
            grid[top][j] = value
            value += 1
        top += 1
        for i in range(top, bottom + 1):
            grid[i][right] = value
            value += 1
        right -= 1
        if top <= bottom:
            for j in range(right, left - 1, -1):
                grid[bottom][j] = value
                value += 1
            bottom -= 1
        if left <= right:
            for i in range(bottom, top - 1, -1):
                grid[i][left] = value
                value += 1
            left += 1
    return grid


assert generate_spiral(1) == [[1]]
assert generate_spiral(3) == [[1, 2, 3], [8, 9, 4], [7, 6, 5]]
```

**Q3. A short "Pythonic" trick: take the top row, rotate the rest counter-clockwise, repeat. Write it and state its cost.**

<details><summary>Hint</summary>`list(zip(*grid))[::-1]` rotates a grid 90° counter-clockwise.</summary></details>

**Answer:**

```python
def spiral_by_rotation(matrix):
    grid = [list(row) for row in matrix]
    out = []
    while grid:
        out.extend(grid.pop(0))
        grid = [list(row) for row in zip(*grid)][::-1]
    return out


assert spiral_by_rotation([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == [1, 2, 3, 6, 9, 8, 7, 4, 5]
assert spiral_by_rotation([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]) == \
    [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]
```

It is elegant but slower: each rotation copies all remaining cells, and there are up to `m + n` rotations, so the time is `O(mn·(m + n))` with `O(mn)` extra space.

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** Four shrinking boundaries (`top`, `bottom`, `left`, `right`).
- **Key idea:** Walk right, down, left, up; shrink the fence after each side; guard the left and up walks with `top <= bottom` and `left <= right`.
- **Time:** `O(mn)`.
- **Auxiliary space:** `O(1)` besides the output (robot + `seen` version: `O(mn)`).
- **Must-test cases:** single row, single column, non-square.
- **One-line memory hook:** *"Peel the onion: right, down, left, up — then move the fences in."*

### Completion checklist

- [x] Problem requirements verified
- [x] Examples and constraints verified
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force solution written and tested
- [x] Optimized Python solution written and tested (`tools/tests/p028.py`)
- [x] Line-by-line explanation written
- [x] Dry run completed with real examples
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
