# 068. Pacific Atlantic Water Flow

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Pacific Atlantic Water Flow |
| **LeetCode number** | 417 |
| **Topic (source list)** | Graph |
| **Also uses** | Matrix, Breadth-First Search, Depth-First Search |
| **Difficulty** | Medium |
| **LeetCode URL** | <https://leetcode.com/problems/pacific-atlantic-water-flow/> |
| **Pattern** | Multi-source BFS from the borders ("reverse the flow") |

---

## 2. Problem Explanation

### A grid is a graph

If graphs are new to you, start with the primer in [066_clone_graph.md](066_clone_graph.md). In grid problems:

- every **cell** `(r, c)` is a node;
- edges go to the 4 neighbours **up, down, left, right** (not diagonals);
- here the edges are **directed by height**: water can step from a cell to a neighbour only if the neighbour is **not higher**.

### What are we given?

`heights` — an `m × n` grid of non-negative integers. `heights[r][c]` is the height of the land at row `r`, column `c`.

The island is surrounded by two oceans:

```text
            Pacific (top edge)
          ┌───────────────────┐
 Pacific  │                   │  Atlantic
 (left)   │      island       │  (right)
          │                   │
          └───────────────────┘
            Atlantic (bottom edge)
```

- The **Pacific** touches the **top row** and the **left column**.
- The **Atlantic** touches the **bottom row** and the **right column**.
- The top-right and bottom-left corner cells touch **both** oceans.

### The flow rule

Rain on a cell can move to a north/south/east/west neighbour whose height is **less than or equal to** the current cell's height. A cell on an edge can pour directly into the ocean on that edge.

### What must we return?

A list of all coordinates `[r, c]` from which water can reach **both** the Pacific and the Atlantic (possibly by different paths). The list may be in **any order**.

### Examples

**Example 1**

```text
Input:  heights = [[1,2,2,3,5],[3,2,3,4,4],[2,4,5,3,1],[6,7,1,4,5],[5,1,1,2,4]]
Output: [[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]]
```

```text
          col: 0  1  2  3  4
   row 0:      1  2  2  3  5
   row 1:      3  2  3  4  4
   row 2:      2  4  5  3  1
   row 3:      6  7  1  4  5
   row 4:      5  1  1  2  4
```

For example, from `[2,2]` (height 5) water can go `[2,2] → [1,2] → [0,2]` (heights 5 → 3 → 2) into the Pacific, and `[2,2] → [2,3] → [2,4]` (5 → 3 → 1) into the Atlantic. `[0,4]` is a corner cell, so it touches both oceans directly. Other cells may have more than one working path.

**Example 2**

```text
Input:  heights = [[1]]
Output: [[0,0]]
```

The single cell touches all four edges, so it drains into both oceans.

### Constraints

- `m == heights.length`
- `n == heights[r].length`
- `1 <= m, n <= 200`
- `0 <= heights[r][c] <= 10^5`

There is no follow-up.

---

## 3. Everyday Analogy

> **Explain it like I'm five**

Imagine a bumpy sandbox with a blue lake on the top and left sides and a green lake on the bottom and right sides. You want to know: *"If I pour water on this spot, can it trickle into both lakes?"*

The slow way: pour a cup of water on **every** spot, one at a time, and watch where it goes. That's a lot of pouring.

The clever way: stand **in** the blue lake and walk **uphill** (or flat) into the sandbox. Every spot you can climb to is a spot whose water could roll back down to the blue lake. Colour those spots blue. Then do the same from the green lake and colour spots green. The spots with **both** colours are the answer. You only walk each lake's hill once!

---

## 4. Step-by-Step Logic

1. **Direct question:** "From this cell, can water go downhill to the Pacific? And to the Atlantic?" Asking it for each cell separately repeats a lot of work.
2. **Flip the direction.** Water flows from `A` to neighbour `B` when `heights[B] <= heights[A]`. Reversed: starting at `B`, we may "climb" to `A` when `heights[A] >= heights[B]`.
3. **Every Pacific border cell already reaches the Pacific.** Start a search from **all** of them at once (a multi-source BFS) and climb to neighbours that are at least as high. Every cell we reach can drain to the Pacific.
4. **Same for the Atlantic** from its border cells.
5. **Answer = intersection** of the two reachable sets.
6. **Each search visits each cell at most once**, so the whole thing is linear in the grid size.

---

## 5. Brute-Force Solution

### Algorithm

For every cell, run a search (DFS with a stack) that follows the real water direction — to neighbours with height `<=` the current one — and record whether it ever stands on a Pacific edge cell (row 0 or column 0) and an Atlantic edge cell (last row or last column). Stop early once both are found.

### Python code

```python
from typing import List


class Solution:
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        m, n = len(heights), len(heights[0])
        directions = ((1, 0), (-1, 0), (0, 1), (0, -1))

        def reaches_both(sr: int, sc: int) -> bool:
            pacific = atlantic = False
            seen = {(sr, sc)}
            stack = [(sr, sc)]
            while stack:
                r, c = stack.pop()
                if r == 0 or c == 0:
                    pacific = True
                if r == m - 1 or c == n - 1:
                    atlantic = True
                if pacific and atlantic:
                    return True
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if (0 <= nr < m and 0 <= nc < n and (nr, nc) not in seen
                            and heights[nr][nc] <= heights[r][c]):   # water flows down/flat
                        seen.add((nr, nc))
                        stack.append((nr, nc))
            return False

        return [[r, c] for r in range(m) for c in range(n) if reaches_both(r, c)]
```

### Explanation

- `reaches_both` is an ordinary graph search on the grid where an edge exists only "downhill or flat".
- Standing on an edge cell means the water can pour off that edge into the ocean.
- The `seen` set is created fresh for every starting cell, so nothing is shared between searches — that is exactly what makes it slow.

### Complexity

- **Time:** `O((m·n)²)`. There are `m·n` starting cells and each search can visit all `m·n` cells. For a `200 × 200` grid that is up to `40,000² = 1.6·10^9` cell visits — far too slow.
- **Auxiliary space:** `O(m·n)` for one search's `seen` set and stack (only one search runs at a time).

---

## 6. Optimized Solution

### Idea

Search **backwards from the oceans**. Two multi-source BFS runs — one from all Pacific border cells, one from all Atlantic border cells — each moving to neighbours that are **at least as high**. A cell is in the answer if both runs reach it.

### Algorithm

1. Build the Pacific start list: the whole top row and the whole left column.
2. Build the Atlantic start list: the whole bottom row and the whole right column.
3. `reachable(starts)`: BFS from all starts; from `(r, c)`, move to an in-bounds, unseen neighbour `(nr, nc)` with `heights[nr][nc] >= heights[r][c]`. Return the set of seen cells.
4. Return every cell that is in both sets (row-major order, though any order is accepted).

### Python code (LeetCode-ready)

```python
from collections import deque
from typing import List


class Solution:
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        m, n = len(heights), len(heights[0])
        directions = ((1, 0), (-1, 0), (0, 1), (0, -1))

        def reachable(starts):
            seen = set(starts)
            queue = deque(starts)
            while queue:
                r, c = queue.popleft()
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if (0 <= nr < m and 0 <= nc < n and (nr, nc) not in seen
                            and heights[nr][nc] >= heights[r][c]):   # climb up/flat
                        seen.add((nr, nc))
                        queue.append((nr, nc))
            return seen

        # Top row + left column (row 0 of the left column is already listed).
        pacific_starts = [(0, c) for c in range(n)] + [(r, 0) for r in range(1, m)]
        # Bottom row + right column (row m-1 of the right column is already listed).
        atlantic_starts = [(m - 1, c) for c in range(n)] + [(r, n - 1) for r in range(m - 1)]

        pacific = reachable(pacific_starts)
        atlantic = reachable(atlantic_starts)

        return [[r, c] for r in range(m) for c in range(n)
                if (r, c) in pacific and (r, c) in atlantic]
```

The ranges `range(1, m)` and `range(m - 1)` skip the corner cell that the row already contains, so no cell is queued twice, even when `m` or `n` is 1.

**BFS or DFS?** Either works and both are `O(m·n)`. A recursive DFS can go up to `m·n = 40,000` calls deep on a large grid, which exceeds CPython's default recursion limit of 1000, so the iterative BFS above is the safer choice in Python.

---

## 7. Line-by-Line Explanation

| Line | What it does | Why |
|---|---|---|
| `m, n = len(heights), len(heights[0])` | Grid size. | `m, n >= 1`, so `heights[0]` always exists. |
| `directions = (...)` | The four moves: down, up, right, left. | No diagonal moves allowed. |
| `seen = set(starts)` | Marks every border cell as reached. | They touch the ocean directly. |
| `queue = deque(starts)` | Starts the BFS from **all** border cells at once. | Multi-source BFS: one search instead of one per cell. |
| `r, c = queue.popleft()` | Takes the next reached cell. | |
| `nr, nc = r + dr, c + dc` | A neighbour position. | |
| `0 <= nr < m and 0 <= nc < n` | Stays inside the grid. | Avoids index errors and Python's negative-index wrap-around. |
| `(nr, nc) not in seen` | Skips cells already reached. | Each cell is processed at most once per search. |
| `heights[nr][nc] >= heights[r][c]` | Only climbs up or stays level. | Reverse of the flow rule: water could run from `(nr, nc)` down to `(r, c)`. |
| `seen.add(...)`, `queue.append(...)` | Marks and schedules the neighbour. | Marking when **added** (not when popped) prevents duplicates in the queue. |
| `pacific_starts = ...` | Top row + left column (without repeating `(0, 0)`). | The Pacific's coastline. |
| `atlantic_starts = ...` | Bottom row + right column (without repeating `(m-1, n-1)`). | The Atlantic's coastline. |
| `return [[r, c] ... if ... in pacific and ... in atlantic]` | Intersection of the two sets. | A cell must drain to both oceans. |

---

## 8. Dry Run

**Input:** Example 1.

```text
          col: 0  1  2  3  4
   row 0:      1  2  2  3  5
   row 1:      3  2  3  4  4
   row 2:      2  4  5  3  1
   row 3:      6  7  1  4  5
   row 4:      5  1  1  2  4
```

### Pacific search

Starting queue (the 9 Pacific border cells): `(0,0) (0,1) (0,2) (0,3) (0,4) (1,0) (2,0) (3,0) (4,0)`.

| Pop | Height | Neighbours checked (not yet seen) | Added |
|---|---|---|---|
| (0,0) | 1 | — (all neighbours are already starts) | — |
| (0,1) | 2 | (1,1) h=2 ≥ 2 ✔ | (1,1) |
| (0,2) | 2 | (1,2) h=3 ≥ 2 ✔ | (1,2) |
| (0,3) | 3 | (1,3) h=4 ≥ 3 ✔ | (1,3) |
| (0,4) | 5 | (1,4) h=4 < 5 ✘ | — |
| (1,0) | 3 | — | — |
| (2,0) | 2 | (2,1) h=4 ≥ 2 ✔ | (2,1) |
| (3,0) | 6 | (3,1) h=7 ≥ 6 ✔ | (3,1) |
| (4,0) | 5 | (4,1) h=1 < 5 ✘ | — |
| (1,1) | 2 | — | — |
| (1,2) | 3 | (2,2) h=5 ≥ 3 ✔ | (2,2) |
| (1,3) | 4 | (2,3) h=3 < 4 ✘; (1,4) h=4 ≥ 4 ✔ | (1,4) |
| (2,1) | 4 | — | — |
| (3,1) | 7 | (4,1) h=1 ✘; (3,2) h=1 ✘ | — |
| (2,2) | 5 | (3,2) h=1 ✘; (2,3) h=3 ✘ | — |
| (1,4) | 4 | (2,4) h=1 < 4 ✘ | — |

### Atlantic search (summary)

Starting from the bottom row and right column, the BFS adds `(3,0)` (6 ≥ 5), `(3,1)` (7 ≥ 1), `(3,2)` (1 ≥ 1), `(3,3)` (4 ≥ 2), `(1,3)` (4 ≥ 4, from `(1,4)`), `(2,3)` (3 ≥ 1, from `(2,4)`) and finally `(2,2)` (5 ≥ 1, from `(3,2)`).

### Combine

```text
Pacific reach (P)      Atlantic reach (A)     Both
P P P P P              . . . . A              . . . . X
P P P P P              . . . A A              . . . X X
P P P . .              . . A A A              . . X . .
P P . . .              A A A A A              X X . . .
P . . . .              A A A A A              X . . . .
```

**Result (row-major):** `[[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]]` ✅ — the same 7 cells as the official output.

**Second dry run:** `heights = [[1]]`. Both start lists contain `(0,0)`, so both searches reach it immediately → `[[0,0]]` ✅.

---

## 9. Concepts, Data Structures, and Patterns

- **Grid as an implicit graph:** cells are nodes, 4-directional moves are edges; no adjacency list needs to be built.
- **Directed edges from a rule:** "can flow" depends on heights, so edges are one-way.
- **Reversing the edges:** asking "who can reach the target?" is easier by searching backwards from the target.
- **Multi-source BFS:** start the queue with many cells at once — here, a whole coastline.
- **Set intersection** to combine two independent searches.
- **Related problems in this project:**
  - Number of Islands — 4-directional grid traversal: [069_number_of_islands.md](069_number_of_islands.md)
  - Word Search — DFS on a grid with backtracking: [../05_matrix/030_word_search.md](../05_matrix/030_word_search.md)
  - Course Schedule — directed graphs: [067_course_schedule.md](067_course_schedule.md)
  - Clone Graph — graph primer: [066_clone_graph.md](066_clone_graph.md)

---

## 10. Complexity Analysis

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Brute force (search from every cell) | `O((m·n)²)` | `O(m·n)` | `m·n` independent searches, each up to `m·n` cells with 4 neighbour checks. |
| Reverse BFS from both oceans (optimized) | `O(m·n)` | `O(m·n)` | Each of the 2 searches adds each cell at most once and checks 4 neighbours per cell; the two `seen` sets and the queue hold at most `m·n` cells each. |

The output list is not counted; it can hold up to `m·n` pairs (for a flat grid every cell qualifies).

---

## 11. Edge Cases

| Case | Input | Expected result (any order) | Why |
|---|---|---|---|
| Single cell | `[[1]]` | `[[0,0]]` | Touches all four edges. |
| Single row | `[[1,2,3]]` | `[[0,0],[0,1],[0,2]]` | Every cell is on the top (Pacific) and bottom (Atlantic) edge. |
| Single column | `[[3],[2],[1]]` | `[[0,0],[1,0],[2,0]]` | Every cell is on the left and right edge. |
| Flat grid | `[[5,5],[5,5]]` | all 4 cells | Equal heights allow flow (`<=`), and all cells are on edges anyway. |
| Pit in the middle | `[[1,1,1],[1,0,1],[1,1,1]]` | the 8 border cells | The centre (height 0) cannot flow uphill to anything. Border cells reach the far ocean by flowing along the flat rim. |
| Slope towards the Atlantic | `[[1,2],[3,4]]` | `[[0,1],[1,0],[1,1]]` | `(0,0)` (height 1) is the lowest cell and cannot climb to the Atlantic. |

All these and 300 random grids are checked in `tools/tests/p068.py`, which sorts results before comparing because any order is allowed.

---

## 12. Common Mistakes and Debugging

1. **Wrong comparison in the reverse search.** Going backwards you must climb: `heights[next] >= heights[current]`. Using `<=` (the forward rule) gives nonsense.
2. **Using `>` instead of `>=`.** Water flows onto **equal** heights too; a strict comparison misses flat plateaus.
3. **Mixing up the oceans.** Pacific = top row + **left** column; Atlantic = bottom row + **right** column.
4. **Forgetting bounds checks.** In Python, `heights[-1]` silently reads the last row instead of raising an error, so a missing `0 <= nr` check gives wrong answers rather than crashes.
5. **One shared `seen` set for both oceans.** Each ocean needs its own set; otherwise the second search stops at cells the first already visited.
6. **Recursive DFS on a 200 × 200 grid.** Depth can reach tens of thousands → `RecursionError` with CPython's default limit.
7. **Comparing results in a fixed order** when testing. The problem accepts any order — sort both lists first.

**Debugging tip:** print the two reachability grids as `P`/`.` and `A`/`.` (like the dry run). Mistakes are usually obvious when you see the picture.

---

## 13. Practice Questions

**Q1. For `heights = [[1,2],[3,4]]`, which cells reach both oceans and why is `(0,0)` excluded?**

<details><summary>Hint</summary>`(0,0)` is a Pacific corner. Where can water go from height 1?</summary></details>

**Answer:** `[[0,1],[1,0],[1,1]]`. `(0,1)` and `(1,0)` are the two corners that touch both oceans. `(1,1)` (height 4) touches the Atlantic and can flow to `(0,1)` (height 2), which touches the Pacific. `(0,0)` touches the Pacific, but both its neighbours are higher (2 and 3), so its water can never get to the bottom or right edge.

**Q2. Write a function that returns only the cells that reach the Pacific (not necessarily the Atlantic).**

<details><summary>Hint</summary>Run just one of the two reverse searches.</summary></details>

**Answer:**

```python
from collections import deque


def pacific_only(heights):
    m, n = len(heights), len(heights[0])
    starts = {(0, c) for c in range(n)} | {(r, 0) for r in range(m)}
    seen, queue = set(starts), deque(starts)
    while queue:
        r, c = queue.popleft()
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < m and 0 <= nc < n and (nr, nc) not in seen \
                    and heights[nr][nc] >= heights[r][c]:
                seen.add((nr, nc))
                queue.append((nr, nc))
    return sorted([r, c] for r, c in seen)


assert pacific_only([[1, 2], [3, 4]]) == [[0, 0], [0, 1], [1, 0], [1, 1]]
assert pacific_only([[3, 3], [3, 1]]) == [[0, 0], [0, 1], [1, 0]]
```

**Q3. Why is the brute force `O((m·n)²)` while the reverse search is `O(m·n)`, even though both use BFS/DFS?**

<details><summary>Hint</summary>Count how many separate searches each version runs.</summary></details>

**Answer:** The brute force runs one search **per cell** (`m·n` searches), and each search may visit the whole grid. The reverse version runs exactly **two** searches (one per ocean), each visiting every cell at most once, because all coastline cells are put into one queue at the start.

**Q4. Count the cells that can reach *at least one* ocean.**

<details><summary>Hint</summary>Union of the two sets instead of the intersection — or one search from all four borders.</summary></details>

**Answer:** Start a single BFS from every border cell (all four edges). Every cell it reaches can drain to some ocean.

```python
from collections import deque


def count_reach_any(heights):
    m, n = len(heights), len(heights[0])
    starts = {(r, c) for r in range(m) for c in range(n)
              if r in (0, m - 1) or c in (0, n - 1)}
    seen, queue = set(starts), deque(starts)
    while queue:
        r, c = queue.popleft()
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < m and 0 <= nc < n and (nr, nc) not in seen \
                    and heights[nr][nc] >= heights[r][c]:
                seen.add((nr, nc))
                queue.append((nr, nc))
    return len(seen)


assert count_reach_any([[1, 1, 1], [1, 0, 1], [1, 1, 1]]) == 8   # the pit is trapped
assert count_reach_any([[1, 1, 1], [1, 5, 1], [1, 1, 1]]) == 9
```

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** Multi-source BFS from the borders, edges reversed.
- **Key idea:** Instead of asking "where does this cell's water go?", ask "which cells can each ocean climb up to?" (`>=` heights). Intersect the Pacific and Atlantic sets.
- **Time:** `O(m·n)`.
- **Auxiliary space:** `O(m·n)`.
- **One-line memory hook:** *"Walk uphill from each lake; cells painted twice are the answer."*

### Completion checklist

- [x] Problem requirements verified against the official statement
- [x] Examples and constraints verified
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force solution written and tested
- [x] Optimized Python solution written and tested (`tools/tests/p068.py`, order-independent comparison)
- [x] Line-by-line explanation written
- [x] Dry run completed with Example 1 (plus Example 2)
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
