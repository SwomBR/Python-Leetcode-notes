# 030. Word Search

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Word Search |
| **LeetCode number** | 79 |
| **Topic (source list)** | Matrix |
| **Also uses** | Backtracking, Depth-First Search (DFS), Recursion, Hash Table (counting for pruning) |
| **Difficulty** | Medium |
| **LeetCode URL** | <https://leetcode.com/problems/word-search/> |
| **Pattern** | Grid backtracking DFS with in-place "visited" marking |

---

## 2. Problem Explanation

### What are we given?

- `board` — a grid of single letters with `m` rows and `n` columns.
- `word` — a string.

### What must we return?

`True` if we can spell `word` by walking through the grid, otherwise `False`.

### The rules of the walk

1. Start on **any** cell whose letter equals the first letter of `word`.
2. Each next letter must be in a cell that **touches** the current one **up, down, left or right**. Diagonal moves are **not** allowed.
3. A cell may be used **at most once** in the same word.
4. Letters are compared exactly: uppercase and lowercase are **different** (`"A" != "a"`).

### Examples

All three examples use the same board:

```text
      c0  c1  c2  c3
r0 [  A   B   C   E ]
r1 [  S   F   C   S ]
r2 [  A   D   E   E ]
```

**Example 1**

```text
Input:  board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "ABCCED"
Output: true
```

Path: `A(0,0) → B(0,1) → C(0,2) → C(1,2) → E(2,2) → D(2,1)`.

```text
[A]→[B]→[C]  E
         ↓
 S   F  [C]  S
         ↓
 A  [D]←[E]  E
```

**Example 2**

```text
Input:  board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "SEE"
Output: true
```

Path: `S(1,3) → E(2,3) → E(2,2)`.

**Example 3**

```text
Input:  board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "ABCB"
Output: false
```

`A → B → C` works, but the only `B` next to that `C` is the one we already used, and a cell cannot be reused.

### Constraints

- `m == board.length`
- `n = board[i].length`
- `1 <= m, n <= 6`
- `1 <= word.length <= 15`
- `board` and `word` consist of only lowercase and uppercase English letters.

### Follow-up (from the statement)

Could you use **search pruning** to make the solution faster with a larger board? — Covered in the optimized solution (letter-count check and searching from the rarer end of the word).

---

## 3. Everyday Analogy

> **Explain it like I'm five**

Imagine a floor made of letter tiles, and you want to spell a word by hopping from tile to tile — only forward, backward, left or right, never diagonally. Each tile you step on gets a chalk mark so you don't step on it twice.

You start on a tile with the first letter and hop to a neighbour with the next letter. If you get stuck (no neighbour has the letter you need), you **step back** to the previous tile, **wipe off the chalk mark** from the tile you're leaving, and try a different neighbour. If every choice fails, you try starting on a different tile.

That "try, get stuck, step back, try something else" is called **backtracking**.

A clever shortcut before you even start hopping: count the letters on the floor. If the word needs two `B`s and the floor has only one, you already know the answer is "no".

---

## 4. Step-by-Step Logic

1. **Every path starts somewhere.** Try each cell as the starting point for `word[0]`.
2. **Define a helper `dfs(r, c, k)`:** "Can I spell `word[k:]` starting on cell `(r, c)`?"
3. **Fail fast:** if `(r, c)` is outside the board, already used, or its letter is not `word[k]`, return `False` — this stops a path **as soon as** it goes wrong (the most important pruning).
4. **Success:** if `k` is the last index of `word`, the whole word has been matched → `True`.
5. **Mark** the cell as used (overwrite it with `"#"`, a character that never appears in the input).
6. **Explore** the four neighbours with `k + 1`.
7. **Unmark** (restore the letter) before returning, so other paths can use this cell. This is the "step back" of backtracking.
8. **Extra pruning for the follow-up:**
   - If `word` is longer than the number of cells, it cannot fit.
   - If `word` needs more copies of some letter than the board has, return `False` without searching.
   - If the first letter of `word` is more common on the board than the last letter, search for the **reversed** word instead (a path spells `word` forwards exactly when it spells the reversed word backwards). Fewer starting cells and earlier dead ends mean less work.

---

## 5. Brute-Force Solution

### Algorithm — build every path of the right length, compare at the end

1. From every cell, walk every possible path (4 directions, no cell twice) and collect the letters.
2. When a path has exactly `len(word)` letters, compare the collected string with `word`.
3. Return `True` on the first match.

This explores paths **without** checking letters along the way, so it is correct but does a huge amount of useless work.

### Python code

```python
from typing import List


class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        m, n = len(board), len(board[0])
        L = len(word)
        path, visited = [], set()

        def walk(r, c):
            path.append(board[r][c])
            visited.add((r, c))
            found = False
            if len(path) == L:
                found = "".join(path) == word      # compare only at the end
            else:
                for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < m and 0 <= nc < n and (nr, nc) not in visited:
                        if walk(nr, nc):
                            found = True
                            break
            path.pop()                              # backtrack
            visited.remove((r, c))
            return found

        for r in range(m):
            for c in range(n):
                if walk(r, c):
                    return True
        return False
```

### Explanation

- `path` holds the letters on the current walk, `visited` holds the cells on it.
- After exploring from a cell we remove it from both, so other walks can use it.
- The board itself is never modified.

### Complexity

- **Time:** from each of the `mn` starting cells there are at most `4 · 3^(L−1)` walks of length `L` (4 choices for the first step, at most 3 afterwards because we never step back onto the previous cell), and each finished walk costs `O(L)` to join and compare. Total `O(mn · 3^L · L)` — and this worst case is hit **every time**, because no letter is checked early. For `L = 15` that is about `4 · 3^14 ≈ 1.9 × 10^7` walks **per starting cell** (fewer on a small board, but still far too many).
- **Auxiliary space:** `O(L)` — recursion depth, `path` and `visited` each hold at most `L` items.

---

## 6. Optimized Solution

### Idea

Same backtracking, but:

1. **Check each letter immediately** — abandon a path at its first wrong letter.
2. **Mark visited cells in place** (`"#"`) instead of using a set.
3. **Follow-up pruning** before searching: length check, letter-count check, and searching from the rarer end.

### Algorithm

1. If `len(word) > m * n`, return `False`.
2. Count letters on the board and in the word; if any letter is short, return `False`.
3. If `count[word[0]] > count[word[-1]]`, reverse `word`.
4. For each cell, run `dfs(r, c, 0)`; return `True` if any succeeds.
5. `dfs(r, c, k)`: out of bounds or `board[r][c] != word[k]` → `False`; `k == len(word) - 1` → `True`; otherwise mark, try 4 neighbours with `k + 1`, unmark, return the result.

### Python code (LeetCode-ready)

```python
from typing import List
from collections import Counter


class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        m, n = len(board), len(board[0])

        # --- Pruning before the search (follow-up) ---
        if len(word) > m * n:
            return False
        board_count = Counter(ch for row in board for ch in row)
        for ch, need in Counter(word).items():
            if board_count[ch] < need:
                return False
        if board_count[word[0]] > board_count[word[-1]]:
            word = word[::-1]          # start from the rarer letter

        # --- Backtracking DFS ---
        def dfs(r, c, k):
            if r < 0 or r >= m or c < 0 or c >= n or board[r][c] != word[k]:
                return False
            if k == len(word) - 1:
                return True
            saved = board[r][c]
            board[r][c] = "#"           # mark as used
            found = (dfs(r + 1, c, k + 1) or dfs(r - 1, c, k + 1) or
                     dfs(r, c + 1, k + 1) or dfs(r, c - 1, k + 1))
            board[r][c] = saved         # unmark (backtrack)
            return found

        for r in range(m):
            for c in range(n):
                if dfs(r, c, 0):
                    return True
        return False
```

---

## 7. Line-by-Line Explanation

| Line | What it does | Why |
|---|---|---|
| `m, n = len(board), len(board[0])` | Board size. | Bounds checks. |
| `if len(word) > m * n: return False` | A word longer than the board cannot fit. | Each cell is used at most once. |
| `board_count = Counter(...)` | How many times each letter appears on the board. | Needed for the two pruning checks. |
| `for ch, need in Counter(word).items(): ...` | If the word needs more of a letter than exists → `False`. | Cheap `O(mn + L)` check that can skip an exponential search (e.g. Example 3 needs two `B`s). |
| `if board_count[word[0]] > board_count[word[-1]]: word = word[::-1]` | Search from the rarer end. | Fewer start cells; dead ends appear sooner. Spelling the reversed word along a path = spelling `word` along the same path backwards, so the answer is unchanged. |
| `def dfs(r, c, k):` | "Can `word[k:]` be spelled starting at `(r, c)`?" | The recursive helper. |
| `if r < 0 or ... or board[r][c] != word[k]: return False` | Off the board, or wrong letter (a `"#"` never matches a letter). | Fail fast — the main pruning. Bounds are checked first so we never index outside the board. |
| `if k == len(word) - 1: return True` | Last letter matched. | The whole word is spelled. |
| `saved = board[r][c]` | Remember the letter. | We must restore it later. |
| `board[r][c] = "#"` | Mark the cell as used. | Prevents reusing the cell on this path, with no extra set. |
| `found = (dfs(...) or ... )` | Try down, up, right, left. | `or` short-circuits: once one direction succeeds, the rest are skipped. |
| `board[r][c] = saved` | Unmark. | Other paths may use this cell; it also leaves the board unchanged for the caller. |
| `return found` | Report the result upward. | Restoring happens **before** returning, even on success. |
| outer double loop | Try every cell as the start. | Return `True` as soon as any start works. |
| `return False` | No start worked. | |

---

## 8. Dry Run

### Dry run 1 — official Example 1: `word = "ABCCED"`

**Pruning:** board counts `A:2, B:1, C:2, D:1, E:3, F:1, S:2`. The word needs `A1 B1 C2 E1 D1` → all available. `count['A'] = 2 > count['D'] = 1`, so the search uses the **reversed** word `"DECCBA"`.

**Start cells:** the outer loop tries cells in row order; every cell before `(2,1)` fails immediately because its letter is not `D`. The only `D` is at `(2,1)`.

Neighbour order inside `dfs`: down, up, right, left.

| Call | Cell | Letter | Needs `word[k]` | Result of check | Next action |
|---|---|---|---|---|---|
| `dfs(2,1,0)` | (2,1) | D | `D` (k=0) | match | mark `#`; try neighbours |
| ↳ down `(3,1)` | — | — | `E` | out of bounds | ✗ |
| ↳ up `dfs(1,1,1)` | (1,1) | F | `E` | mismatch | ✗ |
| ↳ right `dfs(2,2,1)` | (2,2) | E | `E` (k=1) | match | mark; try neighbours |
| ↳↳ down `(3,2)` | — | — | `C` | out of bounds | ✗ |
| ↳↳ up `dfs(1,2,2)` | (1,2) | C | `C` (k=2) | match | mark; try neighbours |
| ↳↳↳ down `dfs(2,2,3)` | (2,2) | `#` | `C` | used | ✗ |
| ↳↳↳ up `dfs(0,2,3)` | (0,2) | C | `C` (k=3) | match | mark; try neighbours |
| ↳↳↳↳ down `dfs(1,2,4)` | (1,2) | `#` | `B` | used | ✗ |
| ↳↳↳↳ up `(-1,2)` | — | — | `B` | out of bounds | ✗ |
| ↳↳↳↳ right `dfs(0,3,4)` | (0,3) | E | `B` | mismatch | ✗ |
| ↳↳↳↳ left `dfs(0,1,4)` | (0,1) | B | `B` (k=4) | match | mark; try neighbours |
| ↳↳↳↳↳ down `dfs(1,1,5)` | (1,1) | F | `A` | mismatch | ✗ |
| ↳↳↳↳↳ up `(-1,1)` | — | — | `A` | out of bounds | ✗ |
| ↳↳↳↳↳ right `dfs(0,2,5)` | (0,2) | `#` | `A` | used | ✗ |
| ↳↳↳↳↳ left `dfs(0,0,5)` | (0,0) | A | `A` (k=5) | match, `k == 5` = last | **return `True`** |

Every level restores its letter on the way back up, so the board is unchanged at the end. Board while the deepest call runs (`#` = marked):

```text
 A  [#] [#]  E
 S   F  [#]  S
 A  [#] [#]  E
```

**Result:** `True` ✅ (the path `D,E,C,C,B,A` read backwards is `A,B,C,C,E,D`).

### Dry run 2 — official Example 3: `word = "ABCB"`

| Step | Check | Result |
|---|---|---|
| 1 | `len(word) = 4 <= 12` | continue |
| 2 | word needs `B` twice; board has `B` once | **return `False`** without any DFS |

**Result:** `False` ✅

Without the count check, plain backtracking also returns `False`: from `A(0,0) → B(0,1) → C(0,2)` the neighbours of `(0,2)` are `C(1,2)`, `E(0,3)` and the already-used `B(0,1)`; the other `A(2,0)` has no `B` neighbour.

### Dry run 3 — official Example 2: `word = "SEE"` (short)

Counts `S:2, E:3`; `count['S'] = 2` is not greater than `count['E'] = 3`, so no reversal. Start `(1,0)` S: neighbours `A(2,0)`, `A(0,0)`, `F(1,1)` → no `E`. Start `(1,3)` S: down `E(2,3)` ✓ → from `(2,3)`: down out of bounds, up `(1,3)` is `#`, right out of bounds, left `E(2,2)` ✓ and `k = 2` is last → `True` ✅

---

## 9. Concepts, Data Structures, and Patterns

- **Backtracking:** choose → explore → un-choose. The "un-choose" (restoring the cell) is what lets one cell take part in many different attempts.
- **DFS on a grid:** four direction moves with bounds checks — the same skeleton as [Number of Islands](../09_graph/069_number_of_islands.md) and [Pacific Atlantic Water Flow](../09_graph/068_pacific_atlantic_water_flow.md). The difference: islands mark cells **permanently**; Word Search must **unmark** because paths are independent attempts.
- **In-place marking:** temporarily overwriting the board saves a `visited` set (compare the marker idea in [Set Matrix Zeroes](027_set_matrix_zeroes.md)).
- **Pruning:** stop a branch as soon as it cannot succeed (wrong letter), and skip the whole search when counts make success impossible.
- **Hash map counting:** `Counter` as in [Valid Anagram](../06_string/034_valid_anagram.md).
- **Short-circuit `or`:** stops exploring directions after the first success.
- **Next step:** [Word Search II](../07_tree/054_word_search_ii.md) searches for many words at once using a [Trie](../07_tree/052_implement_trie_prefix_tree.md).

---

## 10. Complexity Analysis

Let `L = len(word)`.

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Brute force (all walks, compare at end) | `O(mn · 3^L · L)` | `O(L)` | Every walk of length `L` from every start is generated (`≤ 4·3^(L−1)` per start), and each is compared in `O(L)`. No early stopping. |
| Optimized backtracking | `O(mn · 3^L)` worst case | `O(L)` | Each start explores at most `4·3^(L−1)` partial paths, each step `O(1)`. In practice wrong letters cut almost every branch immediately. Recursion depth is at most `L`; marking is in place. |
| Pruning pre-checks | `O(mn + L)` | `O(1)` extra here (at most 52 distinct letters in the counters) | One pass to count the board and one over the word. |

The worst case (e.g. a board full of `a` and a word `aaa…ab`) is still exponential — the count check catches that specific case instantly, which is exactly the point of the follow-up.

---

## 11. Edge Cases

| Case | Input | Expected result | Why |
|---|---|---|---|
| `1 × 1`, match | `[["a"]]`, `"a"` | `True` | Single cell spells the word. |
| `1 × 1`, mismatch | `[["a"]]`, `"b"` | `False` | Letter not on board. |
| Reuse needed | `[["a"]]`, `"aa"` | `False` | The only cell cannot be used twice. |
| Reuse needed in a row | `[["a","a"]]`, `"aaa"` | `False` | Only two cells. |
| Word longer than board | `[["a","a"],["a","a"]]`, `"aaaaa"` | `False` | 5 letters, 4 cells. |
| Diagonal not allowed | `[["a","b"],["c","d"]]`, `"abcd"` | `False` | `b(0,1)` and `c(1,0)` are only diagonal neighbours. |
| Turning path | `[["a","b"],["c","d"]]`, `"abdc"` | `True` | Right, down, left. |
| Case-sensitive | `[["A","a"]]`, `"AA"` | `False` | `"a" != "A"`. |
| Uses every cell | Example board, `"ABCESEEDASFC"` | `True` | A snake through all 12 cells. |
| Missing last letter | 4×4 of `"a"`, `"aaaaaaaaab"` | `False` | Count check returns immediately. |

---

## 12. Common Mistakes and Debugging

1. **Forgetting to unmark.** If `board[r][c] = saved` is skipped (or placed after an early `return`), later attempts see `#` and miss valid paths — and the caller's board is left damaged.
2. **Reusing a cell.** Without marking, `"ABCB"` would return `True` by stepping back onto the used `B`.
3. **Checking the letter before the bounds.** `board[r][c]` with `r = -1` silently reads the **last row** in Python instead of crashing — a nasty bug. Check bounds first.
4. **Allowing diagonals.** Only 4 directions are allowed.
5. **Returning as soon as the first start fails.** Try **every** start cell before returning `False`.
6. **Off-by-one on success:** use `k == len(word) - 1` after the letter check (or `k == len(word)` *before* the bounds check) — mixing the two styles skips or overruns the last letter.
7. **Reversing the word but searching for the original.** Assign the reversed string back to `word` before defining/using `dfs`.

**Debugging tip:** print `(r, c, k, word[k])` at the top of `dfs` with indentation `"  " * k` to see the search tree.

---

## 13. Practice Questions

**Q1. Why is the reversed-word trick safe? Does it ever change the answer?**

<details><summary>Hint</summary>Think about reading a valid path from its other end.</summary></details>

**Answer:** No, it never changes the answer. If a path `p0, p1, …, p(L−1)` spells `word`, then the same cells in reverse order `p(L−1), …, p0` spell `word[::-1]`, and they are still adjacent and distinct. The reverse direction holds too. So "`word` exists" ⇔ "`word[::-1]` exists". The trick only changes how much work the search does.

**Q2. Write the letter-count pre-check as a standalone function.**

<details><summary>Hint</summary>Compare `Counter(word)` with `Counter` of all board letters.</summary></details>

**Answer:**

```python
from collections import Counter


def letters_available(board, word):
    have = Counter(ch for row in board for ch in row)
    return all(have[ch] >= need for ch, need in Counter(word).items())


b = [["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]]
assert letters_available(b, "ABCCED") is True
assert letters_available(b, "ABCB") is False     # needs two B's
assert letters_available(b, "SEEE") is True
assert letters_available(b, "SEEEE") is False    # only three E's
```

Passing this check does **not** mean the word exists (`"SEEE"` passes but the three `E`s cannot all be reached in a line from an `S` — verify by running the solution); failing it guarantees the word does not exist.

**Q3. Count how many different paths spell `word` (not just whether one exists).**

<details><summary>Hint</summary>Same DFS, but add up the results of the four directions instead of stopping at the first success.</summary></details>

**Answer:**

```python
def count_paths(board, word):
    m, n = len(board), len(board[0])

    def dfs(r, c, k):
        if r < 0 or r >= m or c < 0 or c >= n or board[r][c] != word[k]:
            return 0
        if k == len(word) - 1:
            return 1
        saved, board[r][c] = board[r][c], "#"
        total = (dfs(r + 1, c, k + 1) + dfs(r - 1, c, k + 1) +
                 dfs(r, c + 1, k + 1) + dfs(r, c - 1, k + 1))
        board[r][c] = saved
        return total

    return sum(dfs(r, c, 0) for r in range(m) for c in range(n))


b = [["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]]
assert count_paths(b, "ABCCED") == 1
assert count_paths(b, "SEE") == 1
assert count_paths(b, "ABCB") == 0
assert count_paths([["a", "a"]], "aa") == 2      # left-to-right and right-to-left
```

**Q4. Does `"SEEE"` exist on the example board? Trace it.**

<details><summary>Hint</summary>There are three `E`s: `(0,3)`, `(2,2)`, `(2,3)`. Which ones are adjacent to each other and to an `S`?</summary></details>

**Answer:** `False`. `E(2,2)` and `E(2,3)` are adjacent, but `E(0,3)` touches neither of them (its neighbours are `C(0,2)` and `S(1,3)`). A path with three `E`s would need all three to be connected in a line, which is impossible. Example 2's `"SEE"` uses only the two bottom `E`s.

```python
def exist_simple(board, word):
    m, n = len(board), len(board[0])

    def dfs(r, c, k):
        if r < 0 or r >= m or c < 0 or c >= n or board[r][c] != word[k]:
            return False
        if k == len(word) - 1:
            return True
        saved, board[r][c] = board[r][c], "#"
        ok = any(dfs(r + dr, c + dc, k + 1) for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)))
        board[r][c] = saved
        return ok

    return any(dfs(r, c, 0) for r in range(m) for c in range(n))


b = [["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]]
assert exist_simple(b, "SEEE") is False
assert exist_simple(b, "SEE") is True
```

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** Grid backtracking DFS (choose → explore → un-choose).
- **Key idea:** `dfs(r, c, k)` fails fast on bounds/wrong letter/used cell, succeeds at the last letter, marks the cell with `#`, tries 4 neighbours, then restores the letter.
- **Pruning (follow-up):** length check, letter-count check, search from the rarer end of the word.
- **Time:** `O(mn · 3^L)` worst case; much faster in practice.
- **Auxiliary space:** `O(L)` recursion depth.
- **One-line memory hook:** *"Step, chalk, look around, wipe the chalk, step back."*

### Completion checklist

- [x] Problem requirements verified
- [x] Examples and constraints verified
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force solution written and tested
- [x] Optimized Python solution (with follow-up pruning) written and tested (`tools/tests/p030.py`)
- [x] Line-by-line explanation written
- [x] Dry run completed with real examples
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
