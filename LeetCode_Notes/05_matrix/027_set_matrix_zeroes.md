# 027. Set Matrix Zeroes

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Set Matrix Zeroes |
| **LeetCode number** | 73 |
| **Topic (source list)** | Matrix |
| **Also uses** | Array, Hash Set (middle step), In-place marking |
| **Difficulty** | Medium |
| **LeetCode URL** | <https://leetcode.com/problems/set-matrix-zeroes/> |
| **Pattern** | Use the first row and first column as marker storage |

---

## 2. Problem Explanation

### What are we given?

`matrix` — a grid of integers with `m` rows and `n` columns (a list of `m` lists, each of length `n`).

### What must we do?

Wherever the **original** matrix has a `0`, wipe out that cell's **whole row** and **whole column** (set every cell in them to `0`).

### The rules

1. Change `matrix` **in place**. The method returns nothing (`None`); LeetCode inspects the same `matrix` object afterwards.
2. Only zeros that were in the **input** cause wiping. A cell that *becomes* zero because of a wipe must **not** trigger more wiping — otherwise one zero would spread and turn the entire matrix into zeros.

### Examples

**Example 1**

```text
Input:  matrix = [[1,1,1],[1,0,1],[1,1,1]]
Output: [[1,0,1],[0,0,0],[1,0,1]]
```

```text
Before        After
1 1 1         1 0 1
1 0 1   -->   0 0 0
1 1 1         1 0 1
```

The single zero at row 1, column 1 clears row 1 and column 1.

**Example 2**

```text
Input:  matrix = [[0,1,2,0],[3,4,5,2],[1,3,1,5]]
Output: [[0,0,0,0],[0,4,5,0],[0,3,1,0]]
```

```text
Before           After
0 1 2 0          0 0 0 0
3 4 5 2   -->    0 4 5 0
1 3 1 5          0 3 1 0
```

The zeros at `(0,0)` and `(0,3)` clear row 0, column 0 and column 3.

### Constraints

- `m == matrix.length`
- `n == matrix[0].length`
- `1 <= m, n <= 200`
- `-2^31 <= matrix[i][j] <= 2^31 - 1`

### Follow-up (from the statement)

- A straightforward solution using `O(mn)` extra space is probably a bad idea.
- A simple improvement uses `O(m + n)` space, but it is still not the best solution.
- Could you devise a **constant space** solution?

This note walks through all three levels: `O(mn)` (brute force) → `O(m + n)` (row/column sets) → `O(1)` (optimized).

---

## 3. Everyday Analogy

> **Explain it like I'm five**

Imagine a classroom where desks are arranged in rows and columns. Some kids have a cold (the zeros). The rule: if a kid has a cold, everyone in that kid's row **and** column must go home.

If you send kids home *while* you're still checking, you get confused — an empty desk looks like a sick kid, and soon you send the whole class home by mistake!

So you do it in two rounds:

1. **Look first.** Walk around and only *write down* which rows and columns have a sick kid.
2. **Act second.** Then send home everyone in those rows and columns.

The clever part (the optimized version) is where you write the notes: instead of a separate notebook, you put a sticky note on the **first desk of each row** and the **first desk of each column**. You just have to remember separately whether the first row and first column had sick kids of their own, because their sticky notes share those desks.

---

## 4. Step-by-Step Logic

1. **Why not wipe immediately?** If we set a row to zeros while scanning, later we would see those new zeros and wrongly wipe their columns too. We must **separate finding from wiping**.
2. **What do we actually need to remember?** Not each zero's exact position — only **which rows** and **which columns** contain a zero. A cell `(i, j)` ends up `0` exactly when row `i` or column `j` had a zero.
3. **Level 1 (brute force):** keep an untouched copy of the matrix and read zeros from the copy. Simple, but `O(mn)` extra memory.
4. **Level 2:** store a set of zero rows and a set of zero columns. At most `m + n` entries → `O(m + n)` memory.
5. **Level 3 (optimized):** store those flags **inside the matrix**:
   - `matrix[i][0] == 0` means "row `i` must be zeroed".
   - `matrix[0][j] == 0` means "column `j` must be zeroed".
6. **The overlap problem:** the cell `matrix[0][0]` would have to mean both "row 0" and "column 0", and writing markers into row 0 / column 0 destroys their original contents. So **before** writing markers, record two booleans: `first_row_zero` and `first_col_zero`.
7. **Order matters:** first zero the inner cells (rows/columns `1..`) using the markers, and only **at the end** zero the first row and first column (using the two booleans). If we cleared the first row earlier, every column marker would read as "zero this column".

---

## 5. Brute-Force Solution

### Algorithm

1. Make a full copy of the matrix.
2. For every cell that is `0` **in the copy**, set its whole row and whole column to `0` in the real matrix.

Because we read from the copy, newly written zeros never trigger extra wiping.

### Python code

```python
from typing import List


class Solution:
    def setZeroes(self, matrix: List[List[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """
        m, n = len(matrix), len(matrix[0])
        original = [row[:] for row in matrix]      # untouched copy

        for i in range(m):
            for j in range(n):
                if original[i][j] == 0:
                    for c in range(n):
                        matrix[i][c] = 0           # wipe row i
                    for r in range(m):
                        matrix[r][j] = 0           # wipe column j
```

### Explanation

- `row[:]` copies each row, so `original` is independent of `matrix` (a shallow `matrix[:]` would share the rows and be useless).
- Each original zero wipes `n + m` cells.

### Complexity

- **Time:** `O(mn × (m + n))` in the worst case (every cell is zero and each wipes `m + n` cells). For `200 × 200` that is about `40,000 × 400 = 1.6 × 10^7` writes — fine in practice, but wasteful.
- **Auxiliary space:** `O(mn)` for the copy. This is exactly the "probably a bad idea" level from the follow-up.

### Middle step — `O(m + n)` space with row/column sets

```python
from typing import List


class Solution:
    def setZeroes(self, matrix: List[List[int]]) -> None:
        m, n = len(matrix), len(matrix[0])
        zero_rows, zero_cols = set(), set()

        for i in range(m):                 # pass 1: find
            for j in range(n):
                if matrix[i][j] == 0:
                    zero_rows.add(i)
                    zero_cols.add(j)

        for i in range(m):                 # pass 2: wipe
            for j in range(n):
                if i in zero_rows or j in zero_cols:
                    matrix[i][j] = 0
```

- **Time:** `O(mn)` — two full passes.
- **Auxiliary space:** `O(m + n)` — at most `m` row indices and `n` column indices.

---

## 6. Optimized Solution

### Idea

Reuse the **first column** as the `zero_rows` set and the **first row** as the `zero_cols` set. Two booleans remember whether the first row and first column themselves need wiping.

### Algorithm

1. `first_row_zero` = does row 0 contain a `0`? `first_col_zero` = does column 0 contain a `0`?
2. For every inner cell `(i, j)` with `i ≥ 1, j ≥ 1`: if it is `0`, set `matrix[i][0] = 0` and `matrix[0][j] = 0`.
3. For every inner cell `(i, j)`: if `matrix[i][0] == 0` or `matrix[0][j] == 0`, set it to `0`.
4. If `first_row_zero`, zero row 0. If `first_col_zero`, zero column 0.

### Python code (LeetCode-ready)

```python
from typing import List


class Solution:
    def setZeroes(self, matrix: List[List[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """
        m, n = len(matrix), len(matrix[0])

        # 1) Remember whether the first row / first column need wiping.
        first_row_zero = any(matrix[0][j] == 0 for j in range(n))
        first_col_zero = any(matrix[i][0] == 0 for i in range(m))

        # 2) Use the first row and first column as markers.
        for i in range(1, m):
            for j in range(1, n):
                if matrix[i][j] == 0:
                    matrix[i][0] = 0      # mark row i
                    matrix[0][j] = 0      # mark column j

        # 3) Wipe inner cells using the markers.
        for i in range(1, m):
            for j in range(1, n):
                if matrix[i][0] == 0 or matrix[0][j] == 0:
                    matrix[i][j] = 0

        # 4) Finally wipe the first row and first column if needed.
        if first_row_zero:
            for j in range(n):
                matrix[0][j] = 0
        if first_col_zero:
            for i in range(m):
                matrix[i][0] = 0
```

---

## 7. Line-by-Line Explanation

| Line | What it does | Why |
|---|---|---|
| `m, n = len(matrix), len(matrix[0])` | Number of rows and columns. | Used by every loop. |
| `first_row_zero = any(...)` | `True` if row 0 has an original zero. | Row 0 is about to be overwritten with column markers, so we save this fact first. |
| `first_col_zero = any(...)` | `True` if column 0 has an original zero. | Same reason for column 0 (row markers). |
| `for i in range(1, m): for j in range(1, n):` | Visit inner cells only. | Inner zeros are recorded in row 0 / column 0. Zeros already in row 0 / column 0 are themselves markers, which is exactly what we want. |
| `matrix[i][0] = 0` | Marks row `i`. | The first cell of the row acts as the row's flag. |
| `matrix[0][j] = 0` | Marks column `j`. | The first cell of the column acts as the column's flag. |
| second double loop | Reads the markers and zeros inner cells. | A cell is zeroed if its row **or** column is marked. |
| `if first_row_zero:` loop | Zeros row 0 last. | Doing it earlier would make every `matrix[0][j]` look like a column marker. |
| `if first_col_zero:` loop | Zeros column 0 last. | Doing it earlier would make every `matrix[i][0]` look like a row marker. |
| *(no `return`)* | Returns `None`. | The matrix was changed in place. |

**Why does an original zero in row 0 still wipe its column?** If `matrix[0][j]` was already `0`, it works as a column marker in step 3 automatically. Likewise an original zero in column 0 acts as a row marker.

---

## 8. Dry Run

### Dry run 1 — official Example 1

**Input:**

```text
     c0 c1 c2
r0 [  1  1  1 ]
r1 [  1  0  1 ]
r2 [  1  1  1 ]
```

**Step 1:** row 0 = `1 1 1` → `first_row_zero = False`; column 0 = `1 1 1` → `first_col_zero = False`.

**Step 2 — mark:**

| Cell `(i,j)` | Value | Action | Matrix after |
|---|---|---|---|
| (1,1) | 0 | `matrix[1][0] = 0`, `matrix[0][1] = 0` | `[[1,0,1],[0,0,1],[1,1,1]]` |
| (1,2) | 1 | — | unchanged |
| (2,1) | 1 | — | unchanged |
| (2,2) | 1 | — | unchanged |

```text
After marking (markers shown with *)
     c0  c1  c2
r0 [  1  0*  1 ]
r1 [ 0*   0  1 ]
r2 [  1   1  1 ]
```

**Step 3 — wipe inner cells:**

| Cell | `matrix[i][0]` (row marker) | `matrix[0][j]` (column marker) | Result |
|---|---|---|---|
| (1,1) | 0 | 0 | 0 |
| (1,2) | 0 | 1 | **0** |
| (2,1) | 1 | 0 | **0** |
| (2,2) | 1 | 1 | stays 1 |

**Step 4:** both booleans are `False` → nothing more.

```text
Final
1 0 1
0 0 0
1 0 1
```

**Result:** `[[1,0,1],[0,0,0],[1,0,1]]` ✅

### Dry run 2 — official Example 2 (zeros in the first row)

```text
     c0 c1 c2 c3
r0 [  0  1  2  0 ]
r1 [  3  4  5  2 ]
r2 [  1  3  1  5 ]
```

| Step | Detail | State |
|---|---|---|
| 1 | Row 0 contains 0 → `first_row_zero = True`. Column 0 = `0,3,1` contains 0 → `first_col_zero = True`. | unchanged |
| 2 | Inner cells `4 5 2 / 3 1 5` contain no zero → no new markers. | unchanged |
| 3 | Column markers: `matrix[0][1]=1`, `matrix[0][2]=2`, `matrix[0][3]=0`. Row markers: `matrix[1][0]=3`, `matrix[2][0]=1`. Only column 3 is marked → `(1,3)` and `(2,3)` become 0. | `[[0,1,2,0],[3,4,5,0],[1,3,1,0]]` |
| 4a | `first_row_zero` → row 0 becomes all 0. | `[[0,0,0,0],[3,4,5,0],[1,3,1,0]]` |
| 4b | `first_col_zero` → column 0 becomes all 0. | `[[0,0,0,0],[0,4,5,0],[0,3,1,0]]` |

**Result:** `[[0,0,0,0],[0,4,5,0],[0,3,1,0]]` ✅

Notice how the original zero at `(0,3)` acted as a column marker by itself in step 3.

---

## 9. Concepts, Data Structures, and Patterns

- **2D lists (matrices) in Python:** `matrix[i][j]` is row `i`, column `j`; `len(matrix)` rows, `len(matrix[0])` columns.
- **Separate "find" from "modify":** a general rule whenever changes could affect what you read later.
- **Hash sets** (middle step) for fast "is this row marked?" lookups — the same tool used in [Contains Duplicate](../01_array/003_contains_duplicate.md).
- **In-place marking / reusing input storage:** like storing prefix products in the output array in [Product of Array Except Self](../01_array/004_product_of_array_except_self.md), we store bookkeeping inside the data itself to reach `O(1)` space.
- **Shallow vs deep copy:** `[row[:] for row in matrix]` copies each row; `matrix[:]` would not.
- **Related matrix problems:** [Spiral Matrix](028_spiral_matrix.md), [Rotate Image](029_rotate_image.md), [Word Search](030_word_search.md).

---

## 10. Complexity Analysis

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Brute force (copy) | `O(mn(m + n))` worst case | `O(mn)` | Each original zero wipes a row and a column; the copy stores every cell. |
| Row/column sets | `O(mn)` | `O(m + n)` | Two passes over all cells; sets hold at most `m` rows and `n` columns. |
| Optimized (first row/column markers) | `O(mn)` | `O(1)` | A constant number of passes over the grid (checking the first row/column, marking, wiping, then the first row/column again); only two booleans and loop counters are extra. |

---

## 11. Edge Cases

| Case | Input | Expected result | Why |
|---|---|---|---|
| Single cell, non-zero | `[[5]]` | `[[5]]` | No zeros. |
| Single cell, zero | `[[0]]` | `[[0]]` | Already zero. |
| Single row | `[[1,0,3]]` | `[[0,0,0]]` | The zero wipes its only row. |
| Single column | `[[1],[0],[3]]` | `[[0],[0],[0]]` | The zero wipes its only column. |
| No zeros | `[[1,2],[3,4]]` | `[[1,2],[3,4]]` | Nothing changes. |
| Zero in first column only | `[[1,0],[1,1],[0,1]]` | `[[0,0],[0,0],[0,0]]` | Zeros cover column 0, column 1, row 0 and row 2 — every cell. |
| Extreme values | `[[2147483647,-2147483648],[0,7]]` | `[[0,-2147483648],[0,0]]` | Values never matter except for being zero; no sentinel trick needed. |

---

## 12. Common Mistakes and Debugging

1. **Wiping while scanning.** New zeros trigger more wipes and the whole matrix becomes zero. Always find first, then wipe.
2. **Zeroing the first row/column too early.** Then every marker reads as "zero", wiping everything. Handle them **last**.
3. **Using one shared flag at `matrix[0][0]` without a second boolean.** `matrix[0][0]` cannot mean both "row 0" and "column 0"; you need at least one separate boolean (see Practice Q2).
4. **Using a sentinel value** (like `-1` or `float('inf')`) to mark cells. Any 32-bit integer can be a real value, so a sentinel can collide with real data; and in typed languages `None` is not allowed in an `int` matrix.
5. **Shallow copy in the brute force.** `copy = matrix[:]` shares inner lists, so changes show up in the "copy".
6. **Returning the matrix.** It works locally but the expected signature returns `None`.

**Debugging tip:** print the matrix after the marking step; the first row and column should show exactly which columns and rows will be wiped.

---

## 13. Practice Questions

**Q1. For `[[1,2,3],[4,0,6],[7,8,9],[0,1,1]]`, what are the markers after step 2 and the final matrix?**

<details><summary>Hint</summary>Compute the two booleans first. Then mark only inner zeros.</summary></details>

**Answer:** `first_row_zero = False` (row 0 is `1,2,3`); `first_col_zero = True` (`matrix[3][0] = 0`). The inner zero `(1,1)` marks `matrix[1][0] = 0` and `matrix[0][1] = 0`. The original `matrix[3][0] = 0` already marks row 3. Final:

```text
0 0 3
0 0 0
0 0 9
0 0 0
```

**Q2. Write the variant that uses only one extra boolean (`first_col_zero`) and lets `matrix[0][0]` stand for row 0.**

<details><summary>Hint</summary>Scan **all** columns (including column 0) when marking, but record column 0 in the boolean instead of `matrix[0][0]`. Wipe bottom-up so row 0 is processed last.</summary></details>

**Answer:**

```python
def set_zeroes_one_flag(matrix):
    m, n = len(matrix), len(matrix[0])
    first_col_zero = False
    for i in range(m):
        if matrix[i][0] == 0:
            first_col_zero = True
        for j in range(1, n):
            if matrix[i][j] == 0:
                matrix[i][0] = 0
                matrix[0][j] = 0
    for i in range(m - 1, -1, -1):          # bottom-up: row 0 last
        for j in range(n - 1, 0, -1):
            if matrix[i][0] == 0 or matrix[0][j] == 0:
                matrix[i][j] = 0
        if first_col_zero:
            matrix[i][0] = 0


g = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
set_zeroes_one_flag(g)
assert g == [[1, 0, 1], [0, 0, 0], [1, 0, 1]]
g = [[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]]
set_zeroes_one_flag(g)
assert g == [[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]]
g = [[1, 0], [1, 1], [0, 1]]
set_zeroes_one_flag(g)
assert g == [[0, 0], [0, 0], [0, 0]]
```

**Q3. Without changing the matrix, count how many cells will be zero after the operation.**

<details><summary>Hint</summary>If `r` rows and `c` columns contain a zero, inclusion–exclusion gives `r·n + c·m − r·c`.</summary></details>

**Answer:**

```python
def count_zero_cells(matrix):
    m, n = len(matrix), len(matrix[0])
    rows = {i for i in range(m) for j in range(n) if matrix[i][j] == 0}
    cols = {j for i in range(m) for j in range(n) if matrix[i][j] == 0}
    r, c = len(rows), len(cols)
    return r * n + c * m - r * c


assert count_zero_cells([[1, 1, 1], [1, 0, 1], [1, 1, 1]]) == 5
assert count_zero_cells([[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]]) == 8
assert count_zero_cells([[1, 2], [3, 4]]) == 0
```

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** In-place markers in the first row and first column.
- **Key idea:** Only *which rows* and *which columns* matter. Store row flags in column 0, column flags in row 0, and remember row 0 / column 0 themselves in two booleans.
- **Order:** booleans → mark → wipe inner cells → wipe first row/column.
- **Time:** `O(mn)`.
- **Auxiliary space:** `O(1)` (sets version: `O(m + n)`; copy version: `O(mn)`).
- **One-line memory hook:** *"Look first, act second — and clean the notepad last."*

### Completion checklist

- [x] Problem requirements verified
- [x] Examples and constraints verified
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force solution written and tested
- [x] Middle-step `O(m + n)` solution written and tested
- [x] Optimized Python solution written and tested (`tools/tests/p027.py`)
- [x] Line-by-line explanation written
- [x] Dry run completed with real examples
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
