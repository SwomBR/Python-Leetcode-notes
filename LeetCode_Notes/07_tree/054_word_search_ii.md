# 054. Word Search II

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Word Search II |
| **LeetCode number** | 212 |
| **Topic (source list)** | Tree |
| **Also uses** | Trie, Backtracking, Depth-First Search, Matrix |
| **Difficulty** | Hard |
| **LeetCode URL** | <https://leetcode.com/problems/word-search-ii/> |
| **Pattern** | Trie-guided grid DFS with backtracking and pruning |

---

## 2. Problem Explanation

This is the "many words at once" version of Word Search ([030_word_search.md](../05_matrix/030_word_search.md)), and it uses the trie from [052_implement_trie_prefix_tree.md](052_implement_trie_prefix_tree.md).

### What are we given?

- `board` — an `m × n` grid of lowercase letters (a list of lists of one-character strings).
- `words` — a list of distinct lowercase words.

### What must we return?

A list of every word from `words` that can be **traced on the board**. The words may be returned in **any order**.

### How a word is traced

1. Start on any cell whose letter is the word's first letter.
2. Each next letter must be in a cell that **touches** the previous one **up, down, left, or right** (no diagonals).
3. A single cell may be used **at most once within the same word**. (Different words may reuse the same cells.)
4. Each word is reported once, even if it can be traced in several places.

### Examples

**Example 1**

```text
Input:  board = [["o","a","a","n"],
                 ["e","t","a","e"],
                 ["i","h","k","r"],
                 ["i","f","l","v"]],
        words = ["oath","pea","eat","rain"]
Output: ["eat","oath"]
```

- `"oath"`: `o(0,0) → a(0,1) → t(1,1) → h(2,1)`.
- `"eat"`: `e(1,3) → a(1,2) → t(1,1)`.
- `"pea"`: there is no `p` on the board.
- `"rain"`: `r(2,3)` has no neighbouring `a`.

**Example 2**

```text
Input:  board = [["a","b"],["c","d"]], words = ["abcb"]
Output: []
```

`a → b` works, but `b` and `c` are diagonal (not adjacent), and the second `b` would reuse the same cell anyway.

### Constraints

- `m == board.length`
- `n == board[i].length`
- `1 <= m, n <= 12`
- `board[i][j]` is a lowercase English letter.
- `1 <= words.length <= 3 * 10^4`
- `1 <= words[i].length <= 10`
- `words[i]` consists of lowercase English letters.
- All the strings of `words` are unique.

There is no official follow-up.

---

## 3. Everyday Analogy

> **Explain it like I'm five**

You have a letter grid like a Boggle game and a long shopping list of words to find.

The slow way: take the first word, hunt for it everywhere on the grid, then take the second word and hunt for it everywhere **again**, and so on — 30,000 separate hunts.

The clever way: first turn your shopping list into a **tree of doors** (a trie), where words that start the same way share doors. Then put your finger on each cell and slide it to neighbouring cells, walking through the matching door each time. As long as there is a door for the next letter, keep going; if there isn't, no word on your list continues this way, so stop immediately. Whenever you reach a room with a word's name on it, you've found that word — cross it off the list (and knock down the doors that no longer lead anywhere, so you never walk into them again).

One sweep of the grid checks **all** words at the same time.

---

## 4. Step-by-Step Logic

1. **Start from Word Search I.** For a single word, a DFS from each cell with backtracking (mark a cell as used, explore, unmark) decides whether it exists.
2. **The problem with many words:** repeating that DFS for each of up to `3 × 10^4` words repeats the same exploration again and again (all words starting with `"oa"` walk the same cells).
3. **Share the work with a trie.** Insert every word into a trie. Now one DFS path on the board corresponds to one path in the trie; it tests all words with that prefix at once.
4. **DFS state:** the current cell `(r, c)` and the trie node for the letters collected so far.
5. **Pruning rule:** only step into a neighbour if its letter is a child of the current trie node. If it isn't, no word continues that way — don't even enter the cell.
6. **Recording a match:** store the complete word on its last trie node (`node.word`). When the DFS arrives at a node with a word, add it to the answer and **clear** `node.word`, so it is never added twice.
7. **Backtracking:** mark the cell (`board[r][c] = "#"`) before exploring neighbours and restore the letter afterwards, so a cell is used at most once per path.
8. **Leaf pruning (big speed-up):** after exploring, if the trie node has no children and no word left, delete it from its parent. Branches whose words have all been found disappear, so later DFS calls stop earlier.

---

## 5. Brute-Force Solution

### Algorithm

For each word, run the Word Search I backtracking search ([030_word_search.md](../05_matrix/030_word_search.md)). Keep the words that exist.

### Python code

```python
from typing import List


class Solution:
    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        rows, cols = len(board), len(board[0])

        def exist(word: str) -> bool:
            def dfs(r: int, c: int, i: int) -> bool:
                if i == len(word):                     # every letter matched
                    return True
                if r < 0 or r >= rows or c < 0 or c >= cols or board[r][c] != word[i]:
                    return False
                board[r][c] = "#"                      # mark as used on this path
                found = (dfs(r + 1, c, i + 1) or dfs(r - 1, c, i + 1)
                         or dfs(r, c + 1, i + 1) or dfs(r, c - 1, i + 1))
                board[r][c] = word[i]                  # backtrack: restore the letter
                return found

            return any(dfs(r, c, 0) for r in range(rows) for c in range(cols))

        return [word for word in words if exist(word)]
```

### Explanation

- `exist(word)` is exactly Word Search I: try every starting cell, then extend letter by letter to neighbours.
- `"#"` is not a lowercase letter, so a marked cell can never match again on the same path; restoring it afterwards lets other paths use it.
- Words are distinct in the input, and each is checked once, so the result has no duplicates.

### Complexity

Let `W` be the number of words, `L` the maximum word length (`<= 10`), and `m · n` the number of cells.

- **Time:** `O(W · m · n · 3^L)`. Each word starts a DFS from each of the `m · n` cells; each DFS step has at most 3 new directions (it never goes back into the cell it came from, which is marked), so a path explores at most `4 · 3^(L-1)` branches.
- **Auxiliary space:** `O(L)` for the recursion stack (the board is modified in place and restored).
- **Trade-off:** easy to write and correct, but with `W = 3 × 10^4` words and `144` cells it repeats the shared exploration for every word. On large tests it is far too slow (Time Limit Exceeded).

---

## 6. Optimized Solution

### Idea

Build a trie of all words and run a single grid DFS that walks the board and the trie together, collecting every word it reaches and pruning trie branches that are used up.

### Algorithm

1. Build a trie. On the last node of each word, store the word itself (`node.word = word`).
2. For each cell whose letter is a child of the root, call `dfs(r, c, root)`.
3. `dfs(r, c, parent)`:
   1. `node = parent.children[board[r][c]]`.
   2. If `node.word` is set: append it to the result and set it to `None`.
   3. Mark the cell `"#"`.
   4. For each in-bounds neighbour whose letter is in `node.children`, recurse with `node` as the parent.
   5. Restore the cell's letter.
   6. If `node` has no children and no word, delete it from `parent.children`.
4. Return the result list.

### Python code (LeetCode-ready)

```python
from typing import List


class TrieNode:
    def __init__(self):
        self.children = {}   # letter -> TrieNode
        self.word = None     # the full word if one ends at this node


class Solution:
    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        # 1. Build the trie of all words.
        root = TrieNode()
        for word in words:
            node = root
            for ch in word:
                node = node.children.setdefault(ch, TrieNode())
            node.word = word

        rows, cols = len(board), len(board[0])
        found = []

        def dfs(r: int, c: int, parent: TrieNode) -> None:
            ch = board[r][c]
            node = parent.children[ch]

            if node.word is not None:          # a complete word ends here
                found.append(node.word)
                node.word = None               # report each word only once

            board[r][c] = "#"                  # mark the cell as used
            for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
                if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] in node.children:
                    dfs(nr, nc, node)
            board[r][c] = ch                   # backtrack: restore the letter

            if not node.children and node.word is None:
                del parent.children[ch]        # prune a branch with nothing left to find

        # 2. Start a DFS from every cell that can begin some word.
        for r in range(rows):
            for c in range(cols):
                if board[r][c] in root.children:
                    dfs(r, c, root)

        return found
```

The method returns the words in the order they are discovered (`["oath", "eat"]` for Example 1). LeetCode accepts any order.

---

## 7. Line-by-Line Explanation

| Line | What it does | Why |
|---|---|---|
| `class TrieNode` with `children` and `word` | Trie node; `word` holds the whole word at its last letter. | Storing the word (instead of a boolean) means we don't need to rebuild the string from the path. |
| `node = node.children.setdefault(ch, TrieNode())` | Gets the child for `ch`, creating it if missing. | Standard trie insert in one line. |
| `node.word = word` | Marks the end of the word. | — |
| `found = []` | Collects answers. | — |
| `ch = board[r][c]` / `node = parent.children[ch]` | Moves one step down the trie for this cell. | The caller already checked that `ch` is a child, so this never fails. |
| `if node.word is not None:` → append, set `None` | Records a finished word exactly once. | The same word may be reachable from several paths; clearing it prevents duplicates. |
| `board[r][c] = "#"` | Temporarily marks the cell. | A cell may appear only once per word path; `"#"` matches no trie child. |
| `for nr, nc in (...)` | The four orthogonal neighbours. | Diagonals are not allowed. |
| `0 <= nr < rows and 0 <= nc < cols` | Bounds check. | Avoid index errors and Python's negative-index wrap-around. |
| `board[nr][nc] in node.children` | Prune: only enter cells that continue some word. | This is what makes the search fast — dead prefixes are never explored. |
| `board[r][c] = ch` | Restores the cell. | Other paths (and other words) may use this cell. |
| `if not node.children and node.word is None: del parent.children[ch]` | Removes an exhausted leaf. | Future DFS calls reach a dead end one step earlier; repeated pruning removes whole finished branches. |
| `if board[r][c] in root.children: dfs(r, c, root)` | Starts only from cells that begin some remaining word. | Cells whose letter starts no word are skipped. |

---

## 8. Dry Run

**Input (Example 1):**

```text
      c=0 c=1 c=2 c=3
r=0    o   a   a   n
r=1    e   t   a   e
r=2    i   h   k   r
r=3    i   f   l   v

words = ["oath", "pea", "eat", "rain"]
Trie: o-a-t-h(oath)   p-e-a(pea)   e-a-t(eat)   r-a-i-n(rain)
```

Neighbours are tried in the order up, down, left, right.

| Step | Event | Cell | Trie path | What happens | `found` |
|---|---|---|---|---|---|
| 1 | start | (0,0) `o` | `o` | `o` is a root child. Neighbours: up/left out of bounds; down `e` is not a child of `o`; right `a` is. | `[]` |
| 2 | dfs | (0,1) `a` | `oa` | Down `t` is a child of `oa`. | `[]` |
| 3 | dfs | (1,1) `t` | `oat` | Up is `#`; down `h` is a child. | `[]` |
| 4 | dfs | (2,1) `h` | `oath` | `node.word = "oath"` → **found**, cleared. `h` has no children. | `["oath"]` |
| 5 | prune | — | — | `h` is now empty → deleted; then `t`, `a`, `o` each become empty on the way back and are deleted. Root keeps `p`, `e`, `r`. | `["oath"]` |
| 6 | scan | (0,1)…(0,3) | — | `a`, `a`, `n` are not root children → skipped. | `["oath"]` |
| 7 | start | (1,0) `e` | `e` | Neighbours `o`, `i`, `t` are not children of `e` (only `a` is) → dead end, nothing pruned (`e` still has child `a`). | `["oath"]` |
| 8 | scan | (1,1), (1,2) | — | `t`, `a` not root children. | `["oath"]` |
| 9 | start | (1,3) `e` | `e` | Up `n`, down `r` no; left `a` yes. | `["oath"]` |
| 10 | dfs | (1,2) `a` | `ea` | Up `a`, down `k` no; left `t` yes. | `["oath"]` |
| 11 | dfs | (1,1) `t` | `eat` | `node.word = "eat"` → **found**, cleared. | `["oath", "eat"]` |
| 12 | prune | — | — | `t`, then `a`, then `e` are deleted. Root keeps `p`, `r`. | `["oath", "eat"]` |
| 13 | scan | (2,0)…(2,2) | — | `i`, `h`, `k` not root children. | `["oath", "eat"]` |
| 14 | start | (2,3) `r` | `r` | Neighbours `e`, `v`, `k` are not `a` → dead end. | `["oath", "eat"]` |
| 15 | scan | row 3 | — | `i`, `f`, `l`, `v` not root children. | `["oath", "eat"]` |

**Result:** `["oath", "eat"]` — the same set as the expected `["eat","oath"]` ✅ (order does not matter).

**Example 2:** `board = [["a","b"],["c","d"]]`, `words = ["abcb"]`. Start at `a(0,0)`; neighbours are `c(1,0)` (not a child of `a`) and `b(0,1)` (child). At `b`, the trie wants `c`, but `b`'s neighbours are `a` (marked `#`) and `d`. Dead end → `[]` ✅.

---

## 9. Concepts, Data Structures, and Patterns

- **Trie:** shares common prefixes between words so one board walk tests many words at once. Built exactly as in [052_implement_trie_prefix_tree.md](052_implement_trie_prefix_tree.md); the wildcard DFS of [053_add_and_search_word.md](053_add_and_search_word.md) is the closest cousin ("walk the trie while exploring choices").
- **Grid DFS with backtracking:** mark → explore four neighbours → unmark. This is the core of [030_word_search.md](../05_matrix/030_word_search.md) and also appears in [069_number_of_islands.md](../09_graph/069_number_of_islands.md) (without the unmarking).
- **Pruning:** two kinds —
  1. *Prefix pruning:* never step into a cell whose letter does not continue any word.
  2. *Leaf pruning:* delete trie nodes whose words have all been found.
- **In-place marking:** temporarily overwriting the board with `"#"` avoids a separate `visited` set.
- **De-duplication by mutation:** clearing `node.word` after the first match guarantees each word is reported once.
- **Order-independent output:** when a problem says "any order", compare results as sorted lists or sets in your own tests.

---

## 10. Complexity Analysis

Let `m · n` be the number of cells, `W` the number of words, `L` the maximum word length (`<= 10`), and `S` the total number of characters in `words`.

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Brute force (Word Search I per word) | `O(W · m · n · 3^L)` | `O(L)` | Each word restarts a full backtracking search from every cell. |
| Trie + DFS (optimized) | `O(S + m · n · 4 · 3^(L-1))` | `O(S)` | Building the trie costs `O(S)`. Each cell starts at most one DFS; a DFS path can never be longer than `L` (the trie has no deeper nodes) and branches at most 4 ways first and 3 ways after. |

**Explanation:**

- The key improvement is that the `W` factor disappears from the search term: all words are explored **together** through the shared trie.
- `3^(L-1)` with `L = 10` is 19,683, so the worst-case bound is about `144 × 4 × 19,683 ≈ 1.1 × 10^7` steps. Pruning (both kinds) makes real runs much smaller.
- **Space:** the trie stores at most `S` nodes (`O(S)`, at most `3 × 10^5`); the recursion stack is at most `L + 1` deep; the board is modified in place and restored. The output list holds at most `W` words.

---

## 11. Edge Cases

| Case | Example | Expected result | Why |
|---|---|---|---|
| 1 × 1 board, word matches | `[["a"]]`, `["a"]` | `["a"]` | A one-letter word is found at its start cell. |
| 1 × 1 board, no match | `[["a"]]`, `["b", "aa"]` | `[]` | `"aa"` would reuse the single cell. |
| Reuse not allowed | `[["a","a"]]`, `["aaa","aa","a"]` | `["a","aa"]` (any order) | Only two cells, so `"aaa"` is impossible. |
| Word and its prefixes | `[["a","b"],["c","d"]]`, `["ab","abd","abdc","abdca"]` | `["ab","abd","abdc"]` | The DFS keeps going after finding `"ab"`; `"abdca"` would need `a` twice. |
| Word findable in several places | `[["a","b"],["b","a"]]`, `["ab","ba"]` | `["ab","ba"]` | Clearing `node.word` reports each word once. |
| Diagonal-only path | `[["a","b"],["c","d"]]`, `["abcb"]` | `[]` | `b → c` is diagonal. |
| First letter absent | Example 1 board, `["pea"]` | `[]` | No DFS ever starts. |

---

## 12. Common Mistakes and Debugging

1. **Reporting a word twice.** If you don't clear `node.word` (or use a set), a word reachable from two paths appears twice in the output.
2. **Stopping the DFS after finding a word.** `"ab"` and `"abd"` can share a path; after recording `"ab"` keep exploring deeper.
3. **Forgetting to restore the cell.** Without `board[r][c] = ch`, later paths see `"#"` and miss words.
4. **Pruning too early.** Delete a node only when it has **no children and no word**; deleting a node that still has children loses other words.
5. **Pruning before restoring the board.** It doesn't break correctness here, but keep the order *explore → restore → prune* so the code is easy to reason about.
6. **Allowing diagonal moves**, or forgetting the bounds check (Python's `board[-1]` silently wraps around).
7. **Comparing results in a fixed order** in your own tests. The problem allows any order — sort before comparing.

**Debugging tip:** print `(r, c, path)` on entry to `dfs` and "FOUND"/"prune" events, then compare with the dry-run table above.

---

## 13. Practice Questions

**Q1. With the Example 1 board, which of `["oat", "tae", "kite", "ate"]` are found?**

<details><summary>Hint</summary>Look for each start letter and check neighbours: `t` is at (1,1), `a` at (0,1), (0,2), (1,2), `e` at (1,0), (1,3).</summary></details>

**Answer:** `"oat"`: `o(0,0) → a(0,1) → t(1,1)` ✅. `"tae"`: `t(1,1) → a(1,2) → e(1,3)` ✅. `"ate"`: `a(1,2) → t(1,1) → e(1,0)` ✅. `"kite"`: `k(2,2)`'s neighbours are `a, l, h, r` — no `i` ❌. So the answer is `["oat", "tae", "ate"]` in some order.

**Q2. Boggle allows diagonal moves too. Adapt the solution to 8 directions.**

<details><summary>Hint</summary>Only the neighbour list changes.</summary></details>

**Answer:**

```python
def find_words_8dir(board, words):
    root = {}
    for w in words:
        node = root
        for ch in w:
            node = node.setdefault(ch, {})
        node["$"] = w
    rows, cols = len(board), len(board[0])
    found = []
    steps = [(dr, dc) for dr in (-1, 0, 1) for dc in (-1, 0, 1) if (dr, dc) != (0, 0)]

    def dfs(r, c, parent):
        ch = board[r][c]
        node = parent[ch]
        word = node.pop("$", None)
        if word is not None:
            found.append(word)
        board[r][c] = "#"
        for dr, dc in steps:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] in node:
                dfs(nr, nc, node)
        board[r][c] = ch
        if not node:
            del parent[ch]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] in root:
                dfs(r, c, root)
    return found


assert sorted(find_words_8dir([["a", "b"], ["c", "d"]], ["abcb", "ad", "bc", "abc"])) == ["abc", "ad", "bc"]
assert find_words_8dir([["a"]], ["aa"]) == []
```

(`"abcb"` still fails: it needs the single `b` cell twice.)

**Q3. Return the longest word found on the board (ties → alphabetically smallest).**

<details><summary>Hint</summary>Reuse any `findWords` result and pick with a sort key.</summary></details>

**Answer:** Find all words, then choose with `min(found, key=lambda w: (-len(w), w))`.

```python
def longest_found(found):
    return min(found, key=lambda w: (-len(w), w)) if found else ""


assert longest_found(["eat", "oath"]) == "oath"
assert longest_found(["tae", "oat", "ate"]) == "ate"
assert longest_found([]) == ""
```

**Q4. Why does the optimized solution store `node.word` instead of a boolean `is_end` like the plain Trie?**

<details><summary>Hint</summary>What would you need to rebuild the word when you reach its last letter?</summary></details>

**Answer:** With only a boolean, the DFS would have to carry the current path string (or a list of letters) and join it when a word ends — extra work and memory on every call. Storing the word at its last node lets you append it directly, and setting it to `None` doubles as the "already found" marker.

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** Trie + grid DFS backtracking + pruning.
- **Key idea:** Put all words in a trie; DFS from each cell, stepping only into neighbours whose letter is a child of the current trie node. Record and clear `node.word`; delete empty leaves.
- **Time:** `O(S + m · n · 4 · 3^(L-1))`.
- **Auxiliary space:** `O(S)` for the trie, `O(L)` recursion.
- **One-line memory hook:** *"Walk the board and the trie together; when a branch is used up, cut it off."*

### Completion checklist

- [x] Problem requirements verified
- [x] Examples and constraints verified
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force solution written and tested
- [x] Optimized Python solution written and tested (`tools/tests/p054.py`, results compared as sorted lists)
- [x] Line-by-line explanation written
- [x] Dry run completed with the official example (checked against an instrumented run)
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
