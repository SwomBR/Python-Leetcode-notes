# 053. Design Add and Search Words Data Structure

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Design Add and Search Words Data Structure (older title: "Add and Search Word – Data structure design") |
| **LeetCode number** | 211 |
| **Topic (source list)** | Tree |
| **Also uses** | Trie, Depth-First Search, String, Design |
| **Difficulty** | Medium |
| **LeetCode URL** | <https://leetcode.com/problems/design-add-and-search-words-data-structure/> (the old link `add-and-search-word-data-structure-design` in the source list now redirects here) |
| **Pattern** | Trie + DFS that branches on wildcards |

---

## 2. Problem Explanation

The source list calls this problem **"Add and Search Word"**; LeetCode has since renamed it. It is the trie from [052_implement_trie_prefix_tree.md](052_implement_trie_prefix_tree.md) with one twist: search patterns may contain **wildcards**.

### What must we build?

A class named `WordDictionary` with these methods (exact LeetCode names):

| Method | What it does | Returns |
|---|---|---|
| `WordDictionary()` | Creates an empty dictionary. | — |
| `addWord(word)` | Stores `word` (lowercase letters only). | nothing (`None`) |
| `search(word)` | Is there a stored word that **matches** this pattern? | `True` / `False` |

### The matching rules

1. The pattern may contain lowercase letters and dots `'.'`.
2. A letter must match the **same** letter at that position.
3. A dot matches **exactly one** letter — any letter. It never matches "nothing" and never matches two letters.
4. So a match needs the **same length** as the stored word. For example, after adding `"bad"`:
   - `".ad"`, `"b.d"`, `"..."` match;
   - `".."` and `"...."` do not (wrong length).
5. Without dots, `search` is an ordinary exact-word lookup.

### Example

```text
Input
["WordDictionary","addWord","addWord","addWord","search","search","search","search"]
[[],["bad"],["dad"],["mad"],["pad"],["bad"],[".ad"],["b.."]]
Output
[null,null,null,null,false,true,true,true]
```

Step by step:

```text
wordDictionary = WordDictionary()
wordDictionary.addWord("bad")
wordDictionary.addWord("dad")
wordDictionary.addWord("mad")
wordDictionary.search("pad")   -> False  (no stored word is "pad")
wordDictionary.search("bad")   -> True   (exact match)
wordDictionary.search(".ad")   -> True   (the dot can be b, d or m)
wordDictionary.search("b..")   -> True   ("bad" fits)
```

### Constraints

- `1 <= word.length <= 25`
- `word` in `addWord` consists of lowercase English letters.
- `word` in `search` consist of `'.'` or lowercase English letters.
- There will be at most `2` dots in `word` for `search` queries.
- At most `10^4` calls will be made to `addWord` and `search`.

There is no official follow-up.

---

## 3. Everyday Analogy

> **Explain it like I'm five**

Remember the tree of lettered doors from the Trie note: to find `bad`, you walk through door `b`, then `a`, then `d`, and look for a gold star.

Now some letters in your search are **smudged** — `.ad`. At the smudged spot you don't know which door to take, so you **try every door** in that room, one at a time. Behind each one you continue with the clear letters (`a`, then `d`). If any of these tries reaches a room with a gold star at exactly the right moment, you shout "found it!" and stop. If every door leads to a dead end, the answer is "no".

Because there are at most two smudges, you never have to try too many doors.

---

## 4. Step-by-Step Logic

1. **Start from the trie.** Store every word as a path of letter nodes with an `is_end` flag (exactly as in Problem 052).
2. **A pattern without dots** is a normal trie walk: follow one child per letter.
3. **A dot means "any child".** At that position we don't know which child to follow, so we must try **all** of them.
4. **"Try all, succeed if any works" is depth-first search with backtracking.** Define `dfs(i, node)` = "can `word[i:]` be matched starting from `node`?"
   - If `i == len(word)`: we've used up the pattern; succeed only if `node.is_end`.
   - If `word[i]` is a letter: follow that one child (fail if it doesn't exist).
   - If `word[i]` is `'.'`: for every child, if `dfs(i + 1, child)` succeeds, return `True`. Otherwise return `False`.
5. **Length is handled automatically.** We only succeed when the pattern ends at a node marked `is_end`, so a stored word must have exactly the pattern's length.
6. **Why it's fast enough:** only dots branch, and there are at most 2 dots, so we explore at most `26 × 26` paths of length at most 25.

---

## 5. Brute-Force Solution

### Algorithm

Store words in a plain list. To search, scan every stored word of the same length and compare it character by character, treating `.` as "anything".

### Python code

```python
class WordDictionary:
    def __init__(self):
        self.words = []

    def addWord(self, word: str) -> None:
        self.words.append(word)

    def search(self, word: str) -> bool:
        for stored in self.words:                 # linear scan
            if len(stored) != len(word):
                continue
            if all(p == "." or p == c for p, c in zip(word, stored)):
                return True
        return False
```

### Explanation

- `addWord` is a simple append.
- `search` checks every word. Words of a different length can never match, so they are skipped immediately.
- `all(...)` compares position by position; a dot accepts any character.

### Complexity

Let `N` be the number of stored words and `L` the pattern length (`L <= 25`).

- **addWord:** `O(1)` amortized (the list append; the string itself is already built).
- **search:** `O(N · L)` — every word may need up to `L` comparisons.
- **Auxiliary space:** `O(1)` per search; `O(total characters)` for the stored list.
- **Trade-off:** correct and very easy to write, but with up to `10^4` calls, about 5,000 adds followed by 5,000 searches means about `25 × 10^6` word checks, each doing up to 25 character comparisons — too slow in Python, and it gets no benefit from shared prefixes.

---

## 6. Optimized Solution

### Idea

Store words in a trie. Search with a DFS that follows the matching child for a letter and tries every child for a dot.

### Algorithm

1. `addWord`: standard trie insert (create missing children, mark the last node).
2. `search(word)`: return `dfs(0, root)`, where:
   - `dfs(i, node)`: if `i == len(word)`, return `node.is_end`;
   - if `word[i] == '.'`: return `True` if any child `c` gives `dfs(i + 1, c)`;
   - else: follow `node.children[word[i]]` if it exists, otherwise return `False`.

### Python code (LeetCode-ready)

```python
class TrieNode:
    def __init__(self):
        self.children = {}    # letter -> TrieNode
        self.is_end = False   # True if an added word ends here


class WordDictionary:
    def __init__(self):
        self.root = TrieNode()

    def addWord(self, word: str) -> None:
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True

    def search(self, word: str) -> bool:
        def dfs(i: int, node: TrieNode) -> bool:
            if i == len(word):                 # whole pattern consumed
                return node.is_end
            ch = word[i]
            if ch == ".":                      # wildcard: try every child
                for child in node.children.values():
                    if dfs(i + 1, child):
                        return True
                return False
            child = node.children.get(ch)      # normal letter: one path only
            if child is None:
                return False
            return dfs(i + 1, child)

        return dfs(0, self.root)
```

### Alternative: iterative search with a "frontier" of nodes

Instead of recursion, keep the list of all nodes that the pattern prefix can currently reach. A letter keeps one child per node; a dot keeps all children.

```python
class WordDictionary:
    def __init__(self):
        self.root = {}

    def addWord(self, word: str) -> None:
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {})
        node["$"] = True                      # end-of-word marker

    def search(self, word: str) -> bool:
        frontier = [self.root]
        for ch in word:
            next_frontier = []
            for node in frontier:
                if ch == ".":
                    next_frontier.extend(child for key, child in node.items() if key != "$")
                elif ch in node:
                    next_frontier.append(node[ch])
            if not next_frontier:
                return False
            frontier = next_frontier
        return any("$" in node for node in frontier)
```

This version explores breadth-first, so it cannot stop early when the first match is found, but it never recurses and is easy to trace by hand.

---

## 7. Line-by-Line Explanation

(Optimized DFS version; `addWord` is the same as Trie `insert` in Problem 052.)

| Line | What it does | Why |
|---|---|---|
| `def dfs(i, node)` | Answers "can `word[i:]` be matched starting at `node`?" | Breaking the pattern into "current character + the rest" makes the wildcard branching natural. |
| `if i == len(word): return node.is_end` | Base case: no characters left. | A match requires a stored word to end **exactly** here, which also enforces equal length. |
| `ch = word[i]` | Reads the current pattern character. | — |
| `if ch == ".":` | Wildcard branch. | Any letter is allowed here. |
| `for child in node.children.values():` | Tries each existing child letter. | Only letters that actually appear in stored words need trying (at most 26). |
| `if dfs(i + 1, child): return True` | Recurses into that child; stops at the first success. | We only need **one** matching word. |
| `return False` | All children failed (or there were none). | No stored word fits this branch. |
| `child = node.children.get(ch)` | Normal letter: look up the one matching child. | `get` returns `None` instead of raising. |
| `if child is None: return False` | Dead end. | No stored word has this letter here. |
| `return dfs(i + 1, child)` | Continue with the next character. | Only one path to follow. |
| `return dfs(0, self.root)` | Starts the search at the root with the first character. | — |

Recursion depth is at most `len(word) + 1 <= 26`, so Python's recursion limit is never a concern here.

---

## 8. Dry Run

**Input:** the official sequence. After the three `addWord` calls the trie is:

```text
(root)
 ├─ b ─ a ─ d*
 ├─ d ─ a ─ d*
 └─ m ─ a ─ d*
```

**`search("pad")`**

| Call | `i` | `word[i]` | Node | Action | Result |
|---|---|---|---|---|---|
| `dfs(0, root)` | 0 | `p` | root | `root.children.get("p")` → `None` | `False` |

**`search("bad")`** follows `b → a → d`, reaches `i = 3` at a node with `is_end = True` → `True`.

**`search(".ad")`**

| Call | `i` | `word[i]` | Node | Action | Result |
|---|---|---|---|---|---|
| `dfs(0, root)` | 0 | `.` | root | try children in insertion order: `b` first | waits |
| `dfs(1, b)` | 1 | `a` | `b` | child `a` exists → recurse | waits |
| `dfs(2, b-a)` | 2 | `d` | `a` | child `d` exists → recurse | waits |
| `dfs(3, b-a-d)` | 3 | — | `d*` | `i == 3`, `is_end = True` | `True` |
| back in `dfs(0, root)` | | | | first child succeeded → stop | **`True`** |

Children `d` and `m` were never explored, because the DFS stops at the first success.

**`search("b..")`**

| Call | `i` | `word[i]` | Node | Action | Result |
|---|---|---|---|---|---|
| `dfs(0, root)` | 0 | `b` | root | follow `b` | waits |
| `dfs(1, b)` | 1 | `.` | `b` | try each child: only `a` | waits |
| `dfs(2, b-a)` | 2 | `.` | `a` | try each child: only `d` | waits |
| `dfs(3, b-a-d)` | 3 | — | `d*` | `is_end = True` | `True` |

**Output:** `[None, None, None, None, False, True, True, True]` ✅

**Second dry run (a failing wildcard):** `search("..")` on the same trie: at the root, try `b` → at `b`, try `a` → `i == 2` at node `a`, `is_end = False` → fail; same for `d` and `m` → `False`. The dot cannot stretch to match `"bad"`.

---

## 9. Concepts, Data Structures, and Patterns

- **Trie:** the base structure — see [052_implement_trie_prefix_tree.md](052_implement_trie_prefix_tree.md) for the node design and `is_end` flag.
- **Depth-first search with backtracking:** at a dot the DFS tries one child, and if that fails it "backs up" and tries the next. The same shape appears in [030_word_search.md](../05_matrix/030_word_search.md) (try each neighbour) and [054_word_search_ii.md](054_word_search_ii.md) (trie + grid DFS).
- **Early exit with `any`-style logic:** return `True` as soon as one branch succeeds, so most searches touch only a small part of the trie.
- **Breadth-first frontier:** the alternative solution keeps a list of "currently reachable states" and advances them all one character at a time — the same idea as BFS level order in [045_binary_tree_level_order_traversal.md](045_binary_tree_level_order_traversal.md).
- **Nested functions / closures:** `dfs` is defined inside `search`, so it can read `word` without passing it as a parameter.
- **Constraint-driven design:** the "at most 2 dots" constraint is what keeps wildcard search cheap; always read constraints for hints about intended complexity.

---

## 10. Complexity Analysis

Let `L` be the word/pattern length (`<= 25`), `d` the number of dots in a pattern (`<= 2`), `N` the number of stored words, and `T` the total number of characters added.

| Approach | `addWord` | `search` (no dots) | `search` (with dots) | Space |
|---|---|---|---|---|
| Brute force (list scan) | `O(1)` amortized | `O(N · L)` | `O(N · L)` | `O(T)` |
| Trie + DFS (optimized) | `O(L)` | `O(L)` | `O(26^d · L)` | `O(T)` nodes worst case |
| Trie + frontier (alternative) | `O(L)` | `O(L)` | `O(26^d · L)` | `O(T)`; frontier up to `26^d` nodes |

**Explanation:**

- **No dots:** the DFS follows exactly one path of length `L`.
- **With dots:** each dot can multiply the number of active paths by at most 26 (the alphabet size), so at most `26^d` paths are followed, each of length at most `L`. With `d <= 2` that is at most `676 · 25 ≈ 17,000` steps — a constant bound in practice. (The number of explored nodes is also never more than the number of nodes in the trie.)
- **Auxiliary space for search:** `O(L)` for the DFS recursion stack (depth `L + 1`); the frontier alternative stores up to `26^d` nodes at a time.
- **Structure space:** at most one node per added character, less when prefixes are shared.

---

## 11. Edge Cases

| Case | Calls | Expected result | Why |
|---|---|---|---|
| Search before any add | `search("a")`, `search(".")` | `False`, `False` | The root has no children. |
| Single dot | `addWord("a")`, `search(".")` | `True` | The dot matches `a`. |
| Dots must match exact length | `addWord("a")`, `search("..")` | `False` | No stored word of length 2. |
| Pattern longer than every word | `addWord("a")`, `search("a.")` | `False` | The path ends at `a`; the trie has nothing below it. |
| Dot first | `addWord("ab")`, `search(".b")` | `True` | Try every first letter, then `b`. |
| Dot with no fitting child | `addWord("ab")`, `search(".c")` | `False` | Every branch fails at `c`. |
| Prefix is not a word | `addWord("bad")`, `search("ba")` | `False` | `is_end` is `False` at `a`. |
| Longest words, two dots | `addWord("x" * 25)`, `search("x" * 23 + "..")` | `True` | Two wildcards at the end. |
| Duplicate add | `addWord("bad")` twice, `search("bad")` | `True` | Re-marking `is_end` is harmless. |

---

## 12. Common Mistakes and Debugging

1. **Forgetting the end check.** Returning `True` when the pattern runs out, without checking `is_end`, makes `search("ba")` succeed after adding `"bad"`.
2. **Treating `.` as "zero or more" (like a regex `.*`).** Here a dot is exactly one character.
3. **Returning the result of the first child only.** Writing `return dfs(i + 1, child)` inside the dot loop stops after one child even if it failed. Only return early on success; return `False` after the loop.
4. **Iterating over the end marker as if it were a child.** In the dict-of-dicts version, `"$"` is a key too; skip it when expanding a dot (the alternative does `if key != "$"`).
5. **Creating nodes while searching** (for example with `setdefault`). Searches must not change the trie.
6. **Wrong method names.** LeetCode calls `addWord` and `search`.

**Debugging tip:** add `print("  " * i, i, repr(word[i:]))` at the top of `dfs` to see the recursion tree, and compare it with the dry-run tables.

---

## 13. Practice Questions

**Q1. After adding `"cat"`, `"car"`, `"cut"`, how many `dfs` calls does `search("c.t")` make with the optimized solution (children are tried in insertion order)?**

<details><summary>Hint</summary>At the dot, the children of `c` are `a` (from cat/car) and `u` (from cut). Which succeeds first?</summary></details>

**Answer:** `dfs(0, root)` → `dfs(1, c)` → dot: first child `a` → `dfs(2, c-a)` → letter `t` exists → `dfs(3, c-a-t)` returns `True`. That is **4 calls**; the `u` branch is never visited.

**Q2. Return how many stored words match a pattern (instead of just `True`/`False`).**

<details><summary>Hint</summary>Same DFS, but add up the results of all branches instead of stopping at the first success.</summary></details>

**Answer:**

```python
def count_matches(words, pattern):
    root = {}
    for w in set(words):                     # count distinct words
        node = root
        for ch in w:
            node = node.setdefault(ch, {})
        node["$"] = True

    def dfs(i, node):
        if i == len(pattern):
            return 1 if "$" in node else 0
        ch = pattern[i]
        if ch == ".":
            return sum(dfs(i + 1, child) for key, child in node.items() if key != "$")
        return dfs(i + 1, node[ch]) if ch in node else 0

    return dfs(0, root)


assert count_matches(["bad", "dad", "mad"], ".ad") == 3
assert count_matches(["bad", "dad", "mad"], "b..") == 1
assert count_matches(["bad", "dad", "mad"], "..") == 0
```

**Q3. A simpler improvement over the brute force: bucket words by length. What does it change?**

<details><summary>Hint</summary>Use a dictionary `length -> set of words`. When can you use the set directly?</summary></details>

**Answer:** Patterns without dots become an `O(L)` set lookup. Patterns with dots only scan words of the same length. The worst case (all words the same length) is still `O(N · L)`, so the trie remains the better general solution.

```python
from collections import defaultdict


class LengthBuckets:
    def __init__(self):
        self.by_len = defaultdict(set)

    def add(self, word):
        self.by_len[len(word)].add(word)

    def search(self, pattern):
        bucket = self.by_len.get(len(pattern), set())
        if "." not in pattern:
            return pattern in bucket
        return any(all(p in (".", c) for p, c in zip(pattern, w)) for w in bucket)


lb = LengthBuckets()
for w in ["bad", "dad", "mad"]:
    lb.add(w)
assert lb.search("pad") is False
assert lb.search(".ad") is True
assert lb.search("b..") is True
assert lb.search("..") is False
```

**Q4. Why is "at most 2 dots" important? What would happen with a pattern of 25 dots?**

<details><summary>Hint</summary>How many paths can each dot multiply the search by?</summary></details>

**Answer:** Each dot can branch into up to 26 children. With 2 dots that's at most 676 paths. With 25 dots the DFS could, in principle, visit every node of the trie at depth ≤ 25 — the search becomes `O(T)` (the size of the trie), no better than scanning all words. The constraint guarantees wildcard searches stay small.

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** Trie + DFS (branch on wildcards).
- **Key idea:** `dfs(i, node)`: end of pattern → `node.is_end`; letter → follow one child; dot → try every child, succeed if any does.
- **Time:** `addWord` `O(L)`; `search` `O(L)` without dots, `O(26^d · L)` with `d <= 2` dots.
- **Space:** `O(total characters added)`; `O(L)` recursion stack per search.
- **One-line memory hook:** *"At a smudged letter, try every door; one gold star is enough."*

### Completion checklist

- [x] Problem requirements verified (current title and URL, old title noted)
- [x] Examples and constraints verified
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force solution written and tested
- [x] Optimized Python solution written and tested (`tools/tests/p053.py`), including the iterative frontier alternative
- [x] Line-by-line explanation written
- [x] Dry run completed with the official example
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
