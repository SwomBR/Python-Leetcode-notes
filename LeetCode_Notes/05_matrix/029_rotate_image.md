# 029. Rotate Image

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Rotate Image |
| **LeetCode number** | 48 |
| **Topic (source list)** | Matrix |
| **Also uses** | Array, Math (index mapping), In-place swapping |
| **Difficulty** | Medium |
| **LeetCode URL** | <https://leetcode.com/problems/rotate-image/> |
| **Pattern** | Transpose, then reverse each row (or rotate four cells at a time, layer by layer) |

---

## 2. Problem Explanation

### What are we given?

`matrix` — a **square** grid of integers, `n` rows by `n` columns. Think of each number as one pixel of a picture.

### What must we do?

Turn the picture **90 degrees clockwise** — like rotating a photo on your phone once to the right.

### The rules

1. The rotation must be done **in place**: change the given `matrix` itself. The method returns nothing (`None`).
2. You are **not allowed to create a second 2D matrix** and build the answer there. Only a few extra variables are allowed.

### Examples

**Example 1**

```text
Input:  matrix = [[1,2,3],[4,5,6],[7,8,9]]
Output: [[7,4,1],[8,5,2],[9,6,3]]
```

```text
Before        After (90° clockwise)
1 2 3         7 4 1
4 5 6   -->   8 5 2
7 8 9         9 6 3
```

The first **column** read from bottom to top (`7,4,1`) becomes the first **row**.

**Example 2**

```text
Input:  matrix = [[5,1,9,11],[2,4,8,10],[13,3,6,7],[15,14,12,16]]
Output: [[15,13,2,5],[14,3,4,1],[12,6,8,9],[16,7,10,11]]
```

```text
Before              After
 5  1  9 11         15 13  2  5
 2  4  8 10   -->   14  3  4  1
13  3  6  7         12  6  8  9
15 14 12 16         16  7 10 11
```

### Constraints

- `n == matrix.length == matrix[i].length`
- `1 <= n <= 20`
- `-1000 <= matrix[i][j] <= 1000`

There is no separate follow-up; the in-place requirement **is** the challenge.

---

## 3. Everyday Analogy

> **Explain it like I'm five**

Put a square sticker sheet on the table and turn it a quarter turn to the right. The stickers along the **left edge** slide up to become the **top edge**; the **top edge** becomes the **right edge**, and so on.

There's a neat two-move trick to get the same result without a second sheet:

1. **Flip the sheet over its diagonal** (top-left to bottom-right) — like folding it along that line. Rows become columns. This is called a **transpose**.
2. **Mirror each row left-to-right.**

Flip + mirror = a quarter turn to the right. Each move only swaps pairs of stickers, so you never need a second sheet.

---

## 4. Step-by-Step Logic

1. **Where does each value go?** In a clockwise rotation, the value at row `i`, column `j` moves to row `j`, column `n - 1 - i`.
   Check with Example 1: `1` is at `(0,0)` → goes to `(0, 2)` ✔ (top-right). `7` at `(2,0)` → `(0, 0)` ✔.
2. **Doing it with a copy is easy** (the brute force), but the problem forbids a second matrix.
3. **Split the move into two simple, swap-only steps:**
   - **Transpose:** `(i, j) → (j, i)`. Swap `matrix[i][j]` with `matrix[j][i]` for every pair above the diagonal (`j > i`).
   - **Reverse each row:** `(j, i) → (j, n - 1 - i)`.
   - Combined: `(i, j) → (j, i) → (j, n - 1 - i)` — exactly the clockwise rule.
4. **Swaps are naturally in place** — every swap exchanges two cells, so nothing is lost.
5. **Transpose only the upper triangle.** If you swapped for every `(i, j)` you would swap each pair twice and undo your work.
6. **Alternative view:** rotate **rings** (layers). In each ring, four cells move together in a cycle: top → right → bottom → left → top. Saving one value in `tmp` lets you move the other three.

---

## 5. Brute-Force Solution

### Algorithm

1. Build a new `n × n` grid `rotated` where `rotated[j][n - 1 - i] = matrix[i][j]`.
2. Copy every value from `rotated` back into `matrix`.

### Python code

```python
from typing import List


class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """
        n = len(matrix)
        rotated = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                rotated[j][n - 1 - i] = matrix[i][j]
        for i in range(n):
            for j in range(n):
                matrix[i][j] = rotated[i][j]
```

### Explanation

- The first double loop applies the rotation rule directly.
- The second double loop writes the result back, so the caller's `matrix` object changes.
- **Trade-off:** this is correct and easy to reason about, but it allocates a second 2D matrix, which the problem explicitly forbids. It is useful for understanding the index rule and for testing, not as the final answer.

### Complexity

- **Time:** `O(n²)` — two passes over `n²` cells.
- **Auxiliary space:** `O(n²)` — the `rotated` grid.

---

## 6. Optimized Solution

### Idea

Rotate 90° clockwise = **transpose** + **reverse every row**. Both steps only swap cells.

### Algorithm

1. For `i` in `0..n-1`, for `j` in `i+1..n-1`: swap `matrix[i][j]` and `matrix[j][i]`.
2. For each row: reverse it in place.

### Python code (LeetCode-ready)

```python
from typing import List


class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """
        n = len(matrix)

        # 1) Transpose: swap across the main diagonal.
        for i in range(n):
            for j in range(i + 1, n):
                matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]

        # 2) Reverse each row.
        for row in matrix:
            left, right = 0, n - 1
            while left < right:
                row[left], row[right] = row[right], row[left]
                left += 1
                right -= 1
```

(`row.reverse()` does the same as the two-pointer loop; the loop is shown so every swap is visible.)

### Alternative optimized solution — four-way swaps, ring by ring

```python
from typing import List


class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        n = len(matrix)
        for i in range(n // 2):                 # ring index
            for j in range(i, n - 1 - i):       # position along the ring
                tmp = matrix[i][j]                              # save top
                matrix[i][j] = matrix[n - 1 - j][i]             # left   -> top
                matrix[n - 1 - j][i] = matrix[n - 1 - i][n - 1 - j]  # bottom -> left
                matrix[n - 1 - i][n - 1 - j] = matrix[j][n - 1 - i]  # right  -> bottom
                matrix[j][n - 1 - i] = tmp                      # top    -> right
```

This moves each value directly to its final place (one read and one write per cell) but the index arithmetic is easier to get wrong. Both versions are `O(n²)` time and `O(1)` extra space.

---

## 7. Line-by-Line Explanation

(For the transpose + reverse version.)

| Line | What it does | Why |
|---|---|---|
| `n = len(matrix)` | Size of the square. | Used for all bounds. |
| `for i in range(n):` | Each row of the upper triangle. | |
| `for j in range(i + 1, n):` | Only columns to the **right of the diagonal**. | Each off-diagonal pair is swapped exactly once; diagonal cells stay put. |
| `matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]` | Swap across the diagonal. | Python's tuple assignment swaps without a temporary variable. |
| `for row in matrix:` | Visit each row object. | `row` is the actual list inside `matrix`, so changing it changes `matrix`. |
| `left, right = 0, n - 1` | Two pointers at the ends of the row. | Standard in-place reversal. |
| `while left < right:` | Stop when they meet. | The middle element (odd `n`) does not move. |
| `row[left], row[right] = row[right], row[left]` | Swap the ends. | Mirrors the row. |
| `left += 1; right -= 1` | Move inward. | |
| *(no `return`)* | Returns `None`. | The matrix was changed in place. |

---

## 8. Dry Run

**Input:** `matrix = [[1,2,3],[4,5,6],[7,8,9]]` (official Example 1), `n = 3`

### Step 1 — transpose (upper-triangle swaps)

| `(i, j)` | Swap | Matrix after |
|---|---|---|
| (0, 1) | `2 ↔ 4` | `[[1,4,3],[2,5,6],[7,8,9]]` |
| (0, 2) | `3 ↔ 7` | `[[1,4,7],[2,5,6],[3,8,9]]` |
| (1, 2) | `6 ↔ 8` | `[[1,4,7],[2,5,8],[3,6,9]]` |

```text
Original      Transposed
1 2 3         1 4 7
4 5 6   -->   2 5 8
7 8 9         3 6 9
```

The diagonal `1, 5, 9` did not move.

### Step 2 — reverse each row

| Row | Before | Swaps (`left`, `right`) | After |
|---|---|---|---|
| 0 | `[1,4,7]` | (0,2): `1 ↔ 7` | `[7,4,1]` |
| 1 | `[2,5,8]` | (0,2): `2 ↔ 8` | `[8,5,2]` |
| 2 | `[3,6,9]` | (0,2): `3 ↔ 9` | `[9,6,3]` |

```text
Transposed    Rows reversed
1 4 7         7 4 1
2 5 8   -->   8 5 2
3 6 9         9 6 3
```

**Result:** `[[7,4,1],[8,5,2],[9,6,3]]` ✅

### Second dry run — four-way swap on the outer ring of Example 2 (`n = 4`, ring `i = 0`)

```text
 5  1  9 11
 2  4  8 10
13  3  6  7
15 14 12 16
```

| `j` | Four cells (top, right, bottom, left) | Values before | After the cycle (top, right, bottom, left) |
|---|---|---|---|
| 0 | (0,0), (0,3), (3,3), (3,0) | 5, 11, 16, 15 | 15, 5, 11, 16 |
| 1 | (0,1), (1,3), (3,2), (2,0) | 1, 10, 12, 13 | 13, 1, 10, 12 |
| 2 | (0,2), (2,3), (3,1), (1,0) | 9, 7, 14, 2 | 2, 9, 7, 14 |

```text
After ring 0
15 13  2  5
14  4  8  1
12  3  6  9
16  7 10 11
```

Ring `i = 1` has one cycle (`j = 1`): cells (1,1), (1,2), (2,2), (2,1) hold `4, 8, 6, 3` and become `3, 4, 8, 6`.

```text
Final
15 13  2  5
14  3  4  1
12  6  8  9
16  7 10 11
```

**Result:** `[[15,13,2,5],[14,3,4,1],[12,6,8,9],[16,7,10,11]]` ✅

---

## 9. Concepts, Data Structures, and Patterns

- **Index mapping:** clockwise `(i, j) → (j, n-1-i)`; counter-clockwise `(i, j) → (n-1-j, i)`; 180° `(i, j) → (n-1-i, n-1-j)`.
- **Transpose:** swap across the main diagonal — only the upper triangle.
- **Two-pointer reversal:** the same in-place reversal idea as reversing a linked list ([Reverse a Linked List](../04_linked_list/021_reverse_a_linked_list.md)) but on an array.
- **Composing simple transformations:** a hard move (rotation) = two easy moves (transpose + mirror).
- **Layer (ring) traversal:** the same "outside ring first" view as [Spiral Matrix](028_spiral_matrix.md).
- **Python tuple swap:** `a, b = b, a`.
- **In-place modification:** like [Set Matrix Zeroes](027_set_matrix_zeroes.md), the method returns `None` and the caller sees the changed matrix.

---

## 10. Complexity Analysis

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Brute force (copy) | `O(n²)` | `O(n²)` | Two passes over the grid; a second `n × n` grid (forbidden by the problem). |
| Transpose + reverse | `O(n²)` | `O(1)` | About `n²/2` swaps for the transpose and `n²/2` swaps for the reversals; only loop indices are extra. |
| Four-way swaps | `O(n²)` | `O(1)` | About `n²/4` cycles of 4 moves; one `tmp` variable. |

`O(n²)` is optimal: every one of the `n²` cells (except possibly the centre) must move.

---

## 11. Edge Cases

| Case | Input | Expected result | Why |
|---|---|---|---|
| `1 × 1` | `[[42]]` | `[[42]]` | Rotating one pixel changes nothing. |
| `2 × 2` | `[[1,2],[3,4]]` | `[[3,1],[4,2]]` | Smallest real rotation; one ring, one cycle. |
| Odd `n` | `[[1,2,3],[4,5,6],[7,8,9]]` | `[[7,4,1],[8,5,2],[9,6,3]]` | The centre stays put. |
| Even `n` | Example 2 | `[[15,13,2,5],[14,3,4,1],[12,6,8,9],[16,7,10,11]]` | No centre cell; `n/2` rings. |
| Negative / extreme values | `[[-1000,1000],[0,-1000]]` | `[[0,-1000],[-1000,1000]]` | Values never affect positions. |
| Four rotations | any matrix | the original matrix | 4 × 90° = 360°. |

---

## 12. Common Mistakes and Debugging

1. **Transposing the full square** (`for j in range(n)`) — each pair is swapped twice, leaving the matrix unchanged.
2. **Reversing columns instead of rows** after the transpose — that gives a **counter-clockwise** rotation.
3. **Reassigning instead of modifying:** `matrix = new_grid` inside the method only rebinds the local name; LeetCode's matrix is unchanged. Write into `matrix[i][j]` (or use `matrix[:] = ...`, which still creates a new grid and breaks the "no second matrix" rule).
4. **Wrong order in the four-way swap.** You must copy *into* the cell you just saved first (`tmp = top; top = left; left = bottom; bottom = right; right = tmp`). Copying in the other direction overwrites a value before it is read.
5. **Wrong inner range in the four-way swap.** Use `range(i, n - 1 - i)`; going to `n - i` processes the ring's last corner again.

**Debugging tip:** check one value's journey with the rule `(i, j) → (j, n-1-i)`: e.g. the top-left value must end up in the top-right corner.

---

## 13. Practice Questions

**Q1. How do you rotate 90° counter-clockwise in place? Write it.**

<details><summary>Hint</summary>Transpose, then reverse each **column** (equivalently: reverse the order of the rows).</summary></details>

**Answer:** Transpose maps `(i, j) → (j, i)`; reversing the row order maps `(j, i) → (n-1-j, i)`, which is the counter-clockwise rule.

```python
def rotate_counter_clockwise(matrix):
    n = len(matrix)
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    matrix.reverse()          # reverse the order of the row lists, in place


g = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
rotate_counter_clockwise(g)
assert g == [[3, 6, 9], [2, 5, 8], [1, 4, 7]]
```

**Q2. Rotate by 180° in place.**

<details><summary>Hint</summary>Reverse the order of the rows, then reverse each row. (Or rotate clockwise twice.)</summary></details>

**Answer:**

```python
def rotate_180(matrix):
    matrix.reverse()
    for row in matrix:
        row.reverse()


g = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
rotate_180(g)
assert g == [[9, 8, 7], [6, 5, 4], [3, 2, 1]]
```

**Q3. In a `5 × 5` matrix, where does the value at `(1, 3)` end up after one clockwise rotation? After two?**

<details><summary>Hint</summary>Apply `(i, j) → (j, n-1-i)` once, then again.</summary></details>

**Answer:** `(1, 3) → (3, 5-1-1) = (3, 3)`. Second rotation: `(3, 3) → (3, 5-1-3) = (3, 1)`, which matches the 180° rule `(n-1-i, n-1-j) = (3, 1)`.

```python
def new_position(i, j, n):
    return j, n - 1 - i


assert new_position(1, 3, 5) == (3, 3)
assert new_position(*new_position(1, 3, 5), 5) == (3, 1)
```

**Q4. Given two `n × n` matrices `a` and `b`, check whether `b` can be obtained by rotating `a` by 0°, 90°, 180° or 270°.**

<details><summary>Hint</summary>Rotate a copy of `a` up to four times and compare after each rotation.</summary></details>

**Answer:**

```python
def is_rotation(a, b):
    grid = [row[:] for row in a]
    n = len(grid)
    for _ in range(4):
        if grid == b:
            return True
        grid = [[grid[n - 1 - j][i] for j in range(n)] for i in range(n)]
    return False


assert is_rotation([[1, 2], [3, 4]], [[3, 1], [4, 2]]) is True
assert is_rotation([[1, 2], [3, 4]], [[4, 3], [2, 1]]) is True
assert is_rotation([[1, 2], [3, 4]], [[2, 1], [4, 3]]) is False
```

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** Transpose + reverse rows (or four-way swaps per ring).
- **Key idea:** Clockwise rule `(i, j) → (j, n-1-i)` = transpose `(i, j) → (j, i)` followed by a row mirror `(r, c) → (r, n-1-c)`.
- **Time:** `O(n²)`.
- **Auxiliary space:** `O(1)` (copy-based brute force: `O(n²)`, and not allowed).
- **Gotchas:** transpose only `j > i`; reverse **rows** for clockwise, row **order** for counter-clockwise.
- **One-line memory hook:** *"Flip on the diagonal, then mirror."*

### Completion checklist

- [x] Problem requirements verified
- [x] Examples and constraints verified
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force solution written and tested
- [x] Optimized Python solution written and tested (`tools/tests/p029.py`)
- [x] Alternative four-way-swap solution written and tested
- [x] Line-by-line explanation written
- [x] Dry run completed with real examples
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
