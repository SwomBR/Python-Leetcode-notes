# 069. Number of Islands

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Number of Islands |
| **LeetCode number** | 200 |
| **Topic (source list)** | Graph |
| **Also uses** | Matrix, Breadth-First Search, Depth-First Search, Union-Find |
| **Difficulty** | Medium |
| **LeetCode URL** | <https://leetcode.com/problems/number-of-islands/> |
| **Pattern** | Counting connected components with flood fill |

---

## 2. Problem Explanation

### Grid = graph (quick refresher)

The general graph primer is in [066_clone_graph.md](066_clone_graph.md). For grids:

- each **cell** is a node;
- two land cells are joined by an edge when they touch **up, down, left or right** (diagonal does **not** count);
- an **island** is a **connected component**: a group of land cells where you can walk from any one to any other using those 4 moves.

```text
grid (Example 2)          islands labelled
1 1 0 0 0                 A A . . .
1 1 0 0 0                 A A . . .
0 0 1 0 0                 . . B . .
0 0 0 1 1                 . . . C C
```

`B` and `C` touch only diagonally, so they are separate islands.

### What are we given?

`grid` — an `m × n` list of lists of **strings**: `"1"` is land, `"0"` is water. (Note: the strings `"1"` and `"0"`, not the integers `1` and `0`.) Everything outside the grid counts as water.

### What must we return?

The number of islands (an integer).

### Examples

**Example 1**

```text
Input: grid = [
  ["1","1","1","1","0"],
  ["1","1","0","1","0"],
  ["1","1","0","0","0"],
  ["0","0","0","0","0"]
]
Output: 1
```

All nine land cells are connected (for example `(0,3)` joins the rest through `(0,2)`, and `(1,3)` hangs below `(0,3)`), so there is one island.

**Example 2**

```text
Input: grid = [
  ["1","1","0","0","0"],
  ["1","1","0","0","0"],
  ["0","0","1","0","0"],
  ["0","0","0","1","1"]
]
Output: 3
```

A 2×2 block in the top-left, a single cell in the middle, and a pair at the bottom-right.

### Constraints

- `m == grid.length`
- `n == grid[i].length`
- `1 <= m, n <= 300`
- `grid[i][j]` is `'0'` or `'1'`.

There is no follow-up.

---

## 3. Everyday Analogy

> **Explain it like I'm five**

You have a map with green land squares and blue water squares, and a bucket of blue paint.

Start at the top-left corner and look at each square, row by row. Whenever you find a green square, shout *"New island!"* and add one to your count. Then paint that square blue, and keep painting every green square **touching** it, and every green square touching *those*, until the whole island is blue.

Now keep scanning. You will never shout twice for the same island, because you already painted it blue. The number of shouts is the number of islands.

This "spread paint to everything connected" trick is called **flood fill** (it's what the paint-bucket tool in drawing apps does).

---

## 4. Step-by-Step Logic

1. **Scan every cell** in row-major order (row by row, left to right).
2. **Find an unvisited land cell** (`"1"`). It must belong to an island we have not counted yet — otherwise the flood fill of that island would already have turned it into `"0"`.
3. **Count it:** `islands += 1`.
4. **Flood fill:** visit every land cell connected to it (BFS with a queue or DFS with a stack/recursion) and mark each one visited. The simplest marker is to overwrite it with `"0"` ("sink" it).
5. **Continue scanning.** When the scan ends, `islands` is the answer.

Why is it correct? Each island is counted exactly once: at its first cell in scan order, and never again because the fill sinks all of it.

---

## 5. Brute-Force Solution

### Algorithm (no shared "visited" information)

Without remembering anything between cells, how do we avoid counting an island several times? Give each island one **representative**: its first cell in row-major order.

1. For each land cell, find its **whole island** from scratch with a fresh search.
2. Count the cell only if it is the smallest coordinate (row-major) in its island.

### Python code

```python
from typing import List


class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        m, n = len(grid), len(grid[0])

        def island_of(sr: int, sc: int) -> set:
            seen = {(sr, sc)}
            stack = [(sr, sc)]
            while stack:
                r, c = stack.pop()
                for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                    if (0 <= nr < m and 0 <= nc < n and grid[nr][nc] == "1"
                            and (nr, nc) not in seen):
                        seen.add((nr, nc))
                        stack.append((nr, nc))
            return seen

        count = 0
        for r in range(m):
            for c in range(n):
                # Tuples compare row first, then column: min() is the first cell in scan order.
                if grid[r][c] == "1" and min(island_of(r, c)) == (r, c):
                    count += 1
        return count
```

### Explanation

- Every land cell rediscovers its entire island, so an island of size `k` is explored `k` times.
- Exactly one cell per island is its own minimum, so each island is counted once.
- This version never modifies `grid`.

### Complexity

- **Time:** `O((m·n)²)` in the worst case. With an all-land grid, each of the `m·n` cells explores all `m·n` cells. At `300 × 300` that is `90,000² ≈ 8.1·10^9` steps — hopeless.
- **Auxiliary space:** `O(m·n)` for one search's `seen` set and stack.

The lesson: the work is wasted because searches **don't share** what they found. Sharing a single visited marker across the whole scan is the entire optimization.

---

## 6. Optimized Solution

### Idea

Scan once; when you meet land, count it and flood-fill the whole island with BFS, sinking cells to `"0"` as you go. Every cell is sunk at most once, so the total work is linear.

### Algorithm

1. `islands = 0`.
2. For each cell `(r, c)`: if it is `"1"`:
   1. `islands += 1`.
   2. Set it to `"0"` and push it into a queue.
   3. While the queue is not empty, pop a cell and, for each in-bounds neighbour that is `"1"`, set it to `"0"` and push it.
3. Return `islands`.

### Python code (LeetCode-ready, iterative BFS — recommended)

```python
from collections import deque
from typing import List


class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        m, n = len(grid), len(grid[0])
        islands = 0

        for r in range(m):
            for c in range(n):
                if grid[r][c] != "1":
                    continue
                islands += 1                  # first cell of a new island
                grid[r][c] = "0"              # sink it so it's never counted again
                queue = deque([(r, c)])
                while queue:
                    cr, cc = queue.popleft()
                    for nr, nc in ((cr + 1, cc), (cr - 1, cc), (cr, cc + 1), (cr, cc - 1)):
                        if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == "1":
                            grid[nr][nc] = "0"    # mark when ADDED, not when popped
                            queue.append((nr, nc))

        return islands
```

This modifies the input grid. LeetCode allows that; if you must keep the grid intact, use a `visited` set (or a boolean matrix) instead of sinking — same complexity, see Q2.

### Alternative: recursive DFS (the most common textbook version) — and its Python risk

```python
from typing import List


class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        m, n = len(grid), len(grid[0])

        def sink(r: int, c: int) -> None:
            if r < 0 or r >= m or c < 0 or c >= n or grid[r][c] != "1":
                return
            grid[r][c] = "0"
            sink(r + 1, c)
            sink(r - 1, c)
            sink(r, c + 1)
            sink(r, c - 1)

        islands = 0
        for r in range(m):
            for c in range(n):
                if grid[r][c] == "1":
                    islands += 1
                    sink(r, c)
        return islands
```

It is short and correct, **but** each recursive call adds a stack frame, and the depth can reach the size of the island:

- I measured this exact function (Python 3.14, default recursion limit 1000): on an all-land grid the recursion depth reaches `m·n` (900 for 30×30), and the first all-land square that raises `RecursionError` is **32×32** (1,024 cells). A `300 × 300` all-land grid — allowed by the constraints — would need a depth of about **90,000**.
- `sys.setrecursionlimit(...)` raises Python's counter, but very deep recursion can then overflow the real (C) stack and crash the process instead of raising a clean error, depending on Python version and platform.
- Whether it passes on LeetCode depends on their test data and interpreter settings, which I cannot verify from here. Recursive versions are widely shared online, but the iterative BFS above does not depend on any of that.

**Recommendation:** submit the iterative BFS (or the same loop with a list used as a stack, i.e. iterative DFS). Know the recursive version because interviewers often write it, and be ready to explain its depth limit.

---

## 7. Line-by-Line Explanation

For the recommended BFS:

| Line | What it does | Why |
|---|---|---|
| `m, n = len(grid), len(grid[0])` | Grid size. | `m, n >= 1`. |
| `islands = 0` | Island counter. | |
| `for r ... for c ...` | Row-major scan of every cell. | Every island has a first cell in scan order. |
| `if grid[r][c] != "1": continue` | Skip water and already-sunk land. | Compare with the **string** `"1"`. |
| `islands += 1` | Count a new island. | Unsunk land here can't belong to an island we already filled. |
| `grid[r][c] = "0"` | Sink the starting cell. | Marks it visited. |
| `queue = deque([(r, c)])` | Start a BFS from this cell. | `deque.popleft()` is `O(1)`. |
| `cr, cc = queue.popleft()` | Next cell of the island. | |
| `for nr, nc in (...)` | The four neighbours. | Diagonals are not connections. |
| `0 <= nr < m and 0 <= nc < n` | Bounds check. | Negative indices would silently wrap around in Python. |
| `grid[nr][nc] == "1"` | Unvisited land neighbour. | Water and sunk cells are `"0"`. |
| `grid[nr][nc] = "0"` | Sink it **as soon as it is queued**. | Prevents the same cell from being queued twice by two neighbours. |
| `queue.append((nr, nc))` | Explore it later. | |
| `return islands` | Final count. | |

---

## 8. Dry Run

**Input:** Example 2.

```text
     c: 0 1 2 3 4
r0:     1 1 0 0 0
r1:     1 1 0 0 0
r2:     0 0 1 0 0
r3:     0 0 0 1 1
```

| Step | Scan cell | Value | Action | Queue pops (sinking new land) | `islands` |
|---|---|---|---|---|---|
| 1 | (0,0) | "1" | New island, sink (0,0) | pop (0,0) → sink (1,0), (0,1); pop (1,0) → sink (1,1); pop (0,1) → nothing new; pop (1,1) → nothing new | 1 |
| 2 | (0,1)…(2,1) | "0" | Skip (water or already sunk) | — | 1 |
| 3 | (2,2) | "1" | New island, sink (2,2) | pop (2,2) → all four neighbours are "0" | 2 |
| 4 | (2,3)…(3,2) | "0" | Skip | — | 2 |
| 5 | (3,3) | "1" | New island, sink (3,3) | pop (3,3) → sink (3,4); pop (3,4) → nothing new | 3 |
| 6 | (3,4) | "0" | Skip (sunk in step 5) | — | 3 |

**Result:** `3` ✅

Grid after the run: all `"0"` — every land cell was sunk exactly once (4 + 1 + 2 = 7 land cells).

**Second dry run (Example 1):** the scan meets `(0,0)` first; the BFS from there sinks all 9 land cells (`(0,0)`, `(0,1)`, `(0,2)`, `(0,3)`, `(1,0)`, `(1,1)`, `(1,3)`, `(2,0)`, `(2,1)`), so the rest of the scan finds only `"0"` → `1` ✅.

---

## 9. Concepts, Data Structures, and Patterns

- **Connected components:** the number of islands is the number of connected components among land cells.
- **Flood fill:** BFS/DFS that marks a whole region.
- **Implicit graph on a grid:** neighbours are computed (`r±1`, `c±1`) instead of stored.
- **In-place visited marking:** overwriting `"1"` with `"0"` saves a separate visited structure (the queue still uses memory).
- **BFS vs DFS:** both are `O(m·n)` here. Iterative versions avoid Python's recursion limit.
- **Union-Find (Disjoint Set Union):** another way to count components: start with one set per land cell and union adjacent land cells; the answer is the number of sets. Useful when land is added over time (LeetCode 305, Number of Islands II).
- **Related problems in this project:**
  - Pacific Atlantic Water Flow — grid BFS with a height rule: [068_pacific_atlantic_water_flow.md](068_pacific_atlantic_water_flow.md)
  - Number of Connected Components in an Undirected Graph — the same idea on an edge list: [073_number_of_connected_components_in_an_undirected_graph_leetcode_premium.md](073_number_of_connected_components_in_an_undirected_graph_leetcode_premium.md)
  - Word Search — DFS on a grid: [../05_matrix/030_word_search.md](../05_matrix/030_word_search.md)
  - Clone Graph — graph primer: [066_clone_graph.md](066_clone_graph.md)

---

## 10. Complexity Analysis

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Brute force (fresh search per land cell) | `O((m·n)²)` | `O(m·n)` | Up to `m·n` searches of up to `m·n` cells each. |
| BFS + sinking (optimized) | `O(m·n)` | `O(m·n)` worst case for the queue | Each cell is scanned once and sunk at most once; each sunk cell checks 4 neighbours. The queue holds one BFS "wavefront" — for an all-land grid filled from the corner `(0,0)` that is one anti-diagonal, at most `min(m, n)` cells — but `O(m·n)` is the safe general bound. The grid is reused as the visited marker, so no extra visited structure. |
| Recursive DFS + sinking | `O(m·n)` | `O(m·n)` | Same work, but the recursion depth can reach `m·n` (measured: exactly `m·n` on all-land grids). |
| Union-Find | `O(m·n · α(m·n))` | `O(m·n)` | One parent entry per cell; `α` is the inverse Ackermann function (≤ 4 in practice). |

---

## 11. Edge Cases

| Case | Input | Expected | Why |
|---|---|---|---|
| Single water cell | `[["0"]]` | `0` | No land. |
| Single land cell | `[["1"]]` | `1` | One island of size 1. |
| All water | `5 × 7` grid of `"0"` | `0` | The scan never starts a fill. |
| All land | `20 × 20` grid of `"1"` | `1` | One big island (the case that makes recursive DFS deep). |
| Alternating row | `[["1","0","1","0","1"]]` | `3` | Separated by water. |
| Diagonal only | `[["1","0"],["0","1"]]` | `2` | Diagonal neighbours are **not** connected. |
| Two bars joined by a bridge | `[["1","1","1"],["0","1","0"],["1","1","1"]]` | `1` | The middle cell of row 1 connects the top and bottom rows. |

All of these, plus 400 random grids compared with a union-find reference, are in `tools/tests/p069.py`. The tests pass a **deep copy** of each grid to the solution, because the solutions sink cells in place.

---

## 12. Common Mistakes and Debugging

1. **Comparing with integers:** `grid[r][c] == 1` is always `False` because the cells are strings. Use `"1"`.
2. **Counting diagonal neighbours.** Only 4 directions.
3. **Marking visited when popping instead of when pushing.** Two neighbours can both queue the same cell; the answer stays right but work and memory grow. Mark (sink) when you append.
4. **Missing bounds check.** `grid[-1][c]` reads the last row in Python rather than failing — a silent bug.
5. **Recursive DFS on large grids** → `RecursionError` beyond depth 1000 (see section 6).
6. **Reusing a grid after the call.** The optimized solution destroys the input. In your own tests, pass `copy.deepcopy(grid)`, or the second call on the "same" grid will return 0.
7. **Shallow-copying a grid** with `grid[:]` or `list(grid)`: the inner rows are still shared. Use `[row[:] for row in grid]` or `copy.deepcopy`.

**Debugging tip:** print the grid after each new island is counted. Exactly one island should have disappeared each time.

---

## 13. Practice Questions

**Q1. In Example 2, how many times does the BFS append a cell to a queue (including each island's start), and why is that number equal to the number of land cells?**

<details><summary>Hint</summary>A cell is sunk exactly when it is queued.</summary></details>

**Answer:** 7 — once for each land cell (4 + 1 + 2). A cell is appended only while it is still `"1"`, and it becomes `"0"` in the same moment, so it can never be appended again.

**Q2. Write a version that does not modify the grid.**

<details><summary>Hint</summary>Replace sinking with a `visited` set.</summary></details>

**Answer:**

```python
from collections import deque


def num_islands_no_mutation(grid):
    m, n = len(grid), len(grid[0])
    visited = set()
    islands = 0
    for r in range(m):
        for c in range(n):
            if grid[r][c] == "1" and (r, c) not in visited:
                islands += 1
                visited.add((r, c))
                queue = deque([(r, c)])
                while queue:
                    cr, cc = queue.popleft()
                    for nr, nc in ((cr + 1, cc), (cr - 1, cc), (cr, cc + 1), (cr, cc - 1)):
                        if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == "1" \
                                and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            queue.append((nr, nc))
    return islands


g = [["1", "1", "0"], ["0", "0", "0"], ["0", "1", "1"]]
assert num_islands_no_mutation(g) == 2
assert g == [["1", "1", "0"], ["0", "0", "0"], ["0", "1", "1"]]   # unchanged
big = [["1"] * 300 for _ in range(300)]
assert num_islands_no_mutation(big) == 1      # iterative: no recursion limit
```

**Q3. Return the size of the largest island (LeetCode 695, Max Area of Island, uses 0/1 integers; here we keep strings).**

<details><summary>Hint</summary>Same flood fill, but count the cells you sink.</summary></details>

**Answer:**

```python
def max_island_area(grid):
    grid = [row[:] for row in grid]      # work on a copy
    m, n = len(grid), len(grid[0])
    best = 0
    for r in range(m):
        for c in range(n):
            if grid[r][c] == "1":
                grid[r][c] = "0"
                stack, area = [(r, c)], 0
                while stack:                       # iterative DFS
                    cr, cc = stack.pop()
                    area += 1
                    for nr, nc in ((cr + 1, cc), (cr - 1, cc), (cr, cc + 1), (cr, cc - 1)):
                        if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == "1":
                            grid[nr][nc] = "0"
                            stack.append((nr, nc))
                best = max(best, area)
    return best


assert max_island_area([["1", "1", "0", "0", "0"], ["1", "1", "0", "0", "0"],
                        ["0", "0", "1", "0", "0"], ["0", "0", "0", "1", "1"]]) == 4
assert max_island_area([["0"]]) == 0
```

**Q4. Count islands with Union-Find.**

<details><summary>Hint</summary>Start with `count = number of land cells`; every successful union of two different sets reduces the count by 1.</summary></details>

**Answer:**

```python
def num_islands_union_find(grid):
    m, n = len(grid), len(grid[0])
    parent = list(range(m * n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]   # path halving
            x = parent[x]
        return x

    count = sum(row.count("1") for row in grid)
    for r in range(m):
        for c in range(n):
            if grid[r][c] != "1":
                continue
            for nr, nc in ((r + 1, c), (r, c + 1)):   # right and down are enough
                if nr < m and nc < n and grid[nr][nc] == "1":
                    a, b = find(r * n + c), find(nr * n + nc)
                    if a != b:
                        parent[a] = b
                        count -= 1
    return count


assert num_islands_union_find([["1", "1", "0", "0", "0"], ["1", "1", "0", "0", "0"],
                               ["0", "0", "1", "0", "0"], ["0", "0", "0", "1", "1"]]) == 3
assert num_islands_union_find([["1", "0"], ["0", "1"]]) == 2
```

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** Count connected components with flood fill.
- **Key idea:** Scan the grid; each time you find `"1"`, count an island and sink the whole island (BFS), so it is never counted again.
- **Time:** `O(m·n)`.
- **Auxiliary space:** `O(m·n)` worst case for the queue; the grid itself is the visited marker (modified in place).
- **Python warning:** recursive DFS can be `m·n` deep — use iterative BFS/DFS for large grids.
- **One-line memory hook:** *"Shout, then paint the island blue."*

### Completion checklist

- [x] Problem requirements verified against the official statement
- [x] Examples and constraints verified
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force solution written and tested
- [x] Optimized iterative BFS and recursive DFS alternative written and tested (`tools/tests/p069.py`, deep-copied grids)
- [x] Recursion-depth risk measured locally and documented
- [x] Line-by-line explanation written
- [x] Dry run completed with Example 2 (plus Example 1)
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
