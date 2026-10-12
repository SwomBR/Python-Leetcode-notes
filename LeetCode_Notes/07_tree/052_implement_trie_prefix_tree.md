# 052. Implement Trie (Prefix Tree)

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Implement Trie (Prefix Tree) |
| **LeetCode number** | 208 |
| **Topic (source list)** | Tree |
| **Also uses** | Trie, Hash Table, String, Design |
| **Difficulty** | Medium |
| **LeetCode URL** | <https://leetcode.com/problems/implement-trie-prefix-tree/> |
| **Pattern** | Trie: one tree node per character of a shared prefix |

---

## 2. Problem Explanation

### What is a trie?

A **trie** (said like "try", short for re*trie*val) is a tree for storing words. Each edge stands for one letter, so every path from the root spells a string. Words that start the same way **share** the beginning of their path. That makes "does any stored word start with `___`?" very fast. Tries are used for autocomplete and spell checking.

### What must we build?

A class named `Trie` with these methods (exact LeetCode names):

| Method | What it does | Returns |
|---|---|---|
| `Trie()` | Creates an empty trie. | — |
| `insert(word)` | Stores `word`. | nothing (`None`) |
| `search(word)` | Is this **exact** word stored? | `True` / `False` |
| `startsWith(prefix)` | Is there **at least one** stored word that begins with `prefix`? | `True` / `False` |

### The rules

1. `search` needs a **whole-word** match. After inserting only `"apple"`, `search("app")` is `False`.
2. `startsWith` only needs a **prefix** match. After inserting `"apple"`, `startsWith("app")` is `True`. A word counts as a prefix of itself, so `startsWith("apple")` is `True` too.
3. Inserting the same word twice is allowed and changes nothing.

### How LeetCode shows the example

Design problems are written as two lists: the method names to call, and the arguments for each call. The output list holds what each call returns (`null` means "returns nothing").

### Example

**Example 1**

```text
Input
["Trie", "insert", "search", "search", "startsWith", "insert", "search"]
[[], ["apple"], ["apple"], ["app"], ["app"], ["app"], ["app"]]
Output
[null, null, true, false, true, null, true]
```

Step by step:

```text
trie = Trie()
trie.insert("apple")
trie.search("apple")     -> True   ("apple" was inserted)
trie.search("app")       -> False  ("app" is only a prefix so far)
trie.startsWith("app")   -> True   ("apple" starts with "app")
trie.insert("app")
trie.search("app")       -> True   ("app" is now a stored word)
```

### Constraints

- `1 <= word.length, prefix.length <= 2000`
- `word` and `prefix` consist only of lowercase English letters.
- At most `3 * 10^4` calls in total will be made to `insert`, `search`, and `startsWith`.

There is no official follow-up.

---

## 3. Everyday Analogy

> **Explain it like I'm five**

Think of a big tree of doors. Behind the front door there are up to 26 doors labelled `a` to `z`. Behind each of those there are 26 more doors, and so on.

To **store** the word `cat`, you walk through door `c`, then door `a`, then door `t` (building any door that doesn't exist yet), and you put a **gold star** on the room you end up in: "a word ends here".

- To **search** for `cat`, walk `c → a → t`. If a door is missing, the word isn't there. If you reach the room, check for the gold star.
- To check if anything **starts with** `ca`, walk `c → a`. If you get there, some word passes through this room — you don't need a star.

Words like `car`, `cat`, and `cap` share the same `c → a` doors, so the tree never stores that beginning twice.

---

## 4. Step-by-Step Logic

1. **What do the three operations really need?** Exact-word lookup and prefix lookup.
2. **A plain set handles exact lookup well** but has no idea about prefixes; checking a prefix means scanning every stored word.
3. **Organize by letters instead.** Put the first letter at depth 1, the second at depth 2, and so on. Then all words with prefix `"app"` live **below one node**: the node reached by `a → p → p`.
4. **Each node stores:**
   - `children` — a dictionary `letter -> child node`;
   - `is_end` — `True` if some inserted word ends exactly at this node.
5. **insert:** walk letter by letter from the root, creating missing children; set `is_end = True` on the last node.
6. **A shared helper `_walk(s)`:** follow the letters of `s`; return the node you reach, or `None` if a letter is missing.
7. **search(word):** `node = _walk(word)`; answer `node is not None and node.is_end`.
8. **startsWith(prefix):** answer `_walk(prefix) is not None`. Reaching the node is enough, because a node only exists if some inserted word passed through it.

---

## 5. Brute-Force Solution

### Algorithm

Keep all inserted words in a Python `set`.

- `insert` → add to the set.
- `search` → set membership.
- `startsWith` → scan every stored word and test `w.startswith(prefix)`.

### Python code

```python
class Trie:
    def __init__(self):
        self.words = set()

    def insert(self, word: str) -> None:
        self.words.add(word)

    def search(self, word: str) -> bool:
        return word in self.words

    def startsWith(self, prefix: str) -> bool:
        for w in self.words:              # linear scan over every stored word
            if w.startswith(prefix):
                return True
        return False
```

### Explanation

- `insert` and `search` are fast: hashing a string of length `L` costs `O(L)`, then the set lookup is `O(1)` on average.
- `startsWith` is the weak spot: a set cannot jump to "words beginning with `app`", so it checks every word.

### Complexity

Let `N` be the number of stored words and `P` the prefix length.

- **insert / search:** `O(L)` average time.
- **startsWith:** `O(N · P)` time — every word is compared on up to `P` characters.
- **Auxiliary space:** `O(total characters inserted)` for the set.
- **Trade-off:** correct and simple, but with up to `3 * 10^4` calls, a workload of many inserts followed by many `startsWith` calls approaches `10^4 × 10^4 = 10^8` comparisons — too slow in Python. It also does not demonstrate the trie that the problem asks you to implement.

---

## 6. Optimized Solution

### Idea

Build an actual trie: nodes with a `children` dictionary and an `is_end` flag. Every operation walks one node per character.

### Algorithm

1. The constructor creates an empty root node.
2. `insert(word)`: for each character, step into the child (creating it if needed); mark the final node `is_end = True`.
3. `_walk(s)`: follow characters; return the reached node or `None`.
4. `search(word)`: reached node exists **and** `is_end` is `True`.
5. `startsWith(prefix)`: reached node exists.

### Python code (LeetCode-ready)

```python
class TrieNode:
    def __init__(self):
        self.children = {}     # letter -> TrieNode
        self.is_end = False    # True if an inserted word ends here


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True

    def _walk(self, s: str):
        """Return the node reached by following s from the root, or None."""
        node = self.root
        for ch in s:
            node = node.children.get(ch)
            if node is None:
                return None
        return node

    def search(self, word: str) -> bool:
        node = self._walk(word)
        return node is not None and node.is_end

    def startsWith(self, prefix: str) -> bool:
        return self._walk(prefix) is not None
```

### Alternative: nested dictionaries

The same trie can be stored as dictionaries inside dictionaries, using a special key to mark the end of a word. It is compact, but less self-explanatory than named fields.

```python
class Trie:
    END = "$"   # not a lowercase letter, so it can never clash with a real child

    def __init__(self):
        self.root = {}

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {})   # get the child, creating it if missing
        node[self.END] = True

    def _walk(self, s: str):
        node = self.root
        for ch in s:
            if ch not in node:
                return None
            node = node[ch]
        return node

    def search(self, word: str) -> bool:
        node = self._walk(word)
        return node is not None and self.END in node

    def startsWith(self, prefix: str) -> bool:
        return self._walk(prefix) is not None
```

---

## 7. Line-by-Line Explanation

(Optimized `TrieNode` version)

| Line | What it does | Why |
|---|---|---|
| `self.children = {}` | Each node starts with no children. | A dictionary gives `O(1)` average lookup by letter and only stores letters that are actually used. |
| `self.is_end = False` | Marks whether a word ends at this node. | Distinguishes a stored word (`"app"`) from a mere prefix of one (`"app"` inside `"apple"`). |
| `self.root = TrieNode()` | The root represents the empty string. | Every word's path starts here. |
| `node = self.root` (insert) | Start at the root. | — |
| `if ch not in node.children: node.children[ch] = TrieNode()` | Creates the child for this letter if it is missing. | Shared prefixes reuse existing nodes; only new letters create nodes. |
| `node = node.children[ch]` | Steps one level deeper. | Moves to the node for the prefix read so far. |
| `node.is_end = True` | Marks the last node. | The full word now exists. Re-inserting just sets it to `True` again. |
| `node = node.children.get(ch)` (in `_walk`) | Looks up the next letter; `get` returns `None` if absent. | Avoids a `KeyError`. |
| `if node is None: return None` | Stops early. | No stored word contains this prefix. |
| `return node is not None and node.is_end` | Exact-word check. | The path must exist **and** a word must end there. |
| `return self._walk(prefix) is not None` | Prefix check. | A node exists only if an inserted word passed through it, so reaching it proves a match. |

---

## 8. Dry Run

**Input:** the official sequence.

| Step | Call | Walk / changes | Trie after the call (letters, `*` = `is_end`) | Returns |
|---|---|---|---|---|
| 1 | `Trie()` | create root | `(root)` | `None` |
| 2 | `insert("apple")` | create `a`, `p`, `p`, `l`, `e`; mark `e` | `a → p → p → l → e*` | `None` |
| 3 | `search("apple")` | walk `a p p l e` → reach `e`, `is_end = True` | unchanged | `True` |
| 4 | `search("app")` | walk `a p p` → reach second `p`, `is_end = False` | unchanged | `False` |
| 5 | `startsWith("app")` | walk `a p p` → node exists | unchanged | `True` |
| 6 | `insert("app")` | walk `a p p` (all exist, nothing created); mark second `p` | `a → p → p* → l → e*` | `None` |
| 7 | `search("app")` | walk `a p p` → `is_end = True` | unchanged | `True` |

**Output:** `[None, None, True, False, True, None, True]` ✅ (LeetCode prints `None` as `null`).

The trie after step 6:

```text
(root)
  └─ a
     └─ p
        └─ p*        <- "app" ends here
           └─ l
              └─ e*  <- "apple" ends here
```

**Second dry run (a missing letter):** after the steps above, `startsWith("apx")` walks `a`, `p`, then looks for `x` in the second `p`'s children → `get` returns `None` → `False`.

---

## 9. Concepts, Data Structures, and Patterns

- **Trie (prefix tree):** a tree keyed by characters; the path from the root to a node spells a prefix. It is listed under *Tree* because it is literally a rooted tree, just with up to 26 children per node instead of 2 (compare binary trees in [041_maximum_depth_of_binary_tree.md](041_maximum_depth_of_binary_tree.md)).
- **End-of-word marker:** `is_end` (or a special key such as `"$"`) is what separates "stored word" from "prefix of a stored word".
- **Hash map children vs fixed array:** `dict` children only allocate used letters; a `[None] * 26` array is the classic C/Java approach (index `ord(ch) - ord('a')`).
- **Class design:** a small helper class (`TrieNode`) keeps the main class readable; a private helper method (`_walk`) removes duplicated code between `search` and `startsWith`.
- **Where tries come next:**
  - [053_add_and_search_word.md](053_add_and_search_word.md) adds `.` wildcards — a trie plus DFS.
  - [054_word_search_ii.md](054_word_search_ii.md) searches a whole word list on a grid at once using a trie.
  - Word Break ([059_word_break_problem.md](../08_dynamic_programming/059_word_break_problem.md)) can use a trie to find dictionary words starting at each position.
- **String prefixes in sets:** the brute force uses `str.startswith`, the simple tool for one-off prefix checks; the anagram notes ([034_valid_anagram.md](../06_string/034_valid_anagram.md), [035_group_anagrams.md](../06_string/035_group_anagrams.md)) show other hash-based string grouping.

---

## 10. Complexity Analysis

Let `L` be the length of the word or prefix in a call, `N` the number of stored words, and `T` the total number of characters ever inserted.

| Approach | `insert` | `search` | `startsWith` | Space for the structure |
|---|---|---|---|---|
| Brute force (set + scan) | `O(L)` average | `O(L)` average | `O(N · L)` | `O(T)` |
| Trie (optimized, either version) | `O(L)` | `O(L)` | `O(L)` | `O(T)` nodes in the worst case |

**Explanation:**

- In the trie, every operation does one dictionary lookup per character, and each lookup is `O(1)` on average, so the time depends only on the length of the input string — **not** on how many words are stored.
- **Auxiliary space per call:** `insert` creates at most `L` new nodes (`O(L)`); `search` and `startsWith` use `O(1)` extra space (one pointer).
- **Total space:** at most one node per inserted character (`O(T)`), and usually much less because shared prefixes are stored once. Each node also carries a dictionary, so the constant factor is larger than a set of strings.

---

## 11. Edge Cases

| Case | Calls | Expected result | Why |
|---|---|---|---|
| Search in an empty trie | `search("a")`, `startsWith("a")` | `False`, `False` | No nodes below the root. |
| Prefix that is not a word | `insert("apple")`, `search("app")` | `False` | `is_end` is `False` at the second `p`. |
| Word is a prefix of itself | `insert("apple")`, `startsWith("apple")` | `True` | The node for `"apple"` exists. |
| Query longer than any word | `insert("a")`, `search("aa")`, `startsWith("aa")` | `False`, `False` | The walk runs out of nodes. |
| Duplicate insert | `insert("a")` twice, `search("a")` | `True` | Setting `is_end = True` twice is harmless. |
| Very long word | `insert("z" * 2000)`, `search("z" * 1999)`, `startsWith("z" * 1999)` | `False`, `True` | Only the 2000th node is marked; the loops are iterative, so there are no recursion-depth issues. |
| Shorter word inserted after longer | `insert("apple")`, `insert("app")`, `search("app")` | `True` | Insert reuses existing nodes and only flips `is_end`. |

---

## 12. Common Mistakes and Debugging

1. **Forgetting `is_end`.** Without it, `search("app")` would return `True` after inserting only `"apple"`.
2. **Using `is_end` in `startsWith`.** `startsWith("app")` must be `True` even if `"app"` itself was never inserted.
3. **Creating nodes during `search`.** Using `node.children.setdefault(ch, TrieNode())` in a lookup silently grows the trie, and then `startsWith` gives wrong `True` answers. Lookups must never modify the trie.
4. **Sharing one children dict between nodes.** Writing `def __init__(self, children={})` uses Python's mutable default argument — every node would share the same dictionary. Create a fresh `{}` inside `__init__`.
5. **Wrong method names.** LeetCode calls `startsWith` (camelCase); `starts_with` will fail.
6. **Returning the node instead of a boolean.** `return self._walk(prefix)` returns a `TrieNode` or `None`; convert with `is not None`.

**Debugging tip:** write a tiny `dump(node, prefix="")` that prints every path with its `is_end` flag, and compare the output with the dry-run diagram.

---

## 13. Practice Questions

**Q1. After `insert("car")`, `insert("cart")`, `insert("cat")`, how many trie nodes exist (not counting the root), and what are `search("ca")` and `startsWith("ca")`?**

<details><summary>Hint</summary>Draw the shared `c → a` path, then the branches.</summary></details>

**Answer:** Nodes: `c`, `a`, `r`, `t` (under `r`), `t` (under `a`) = **5 nodes** for 10 inserted characters. `search("ca")` is `False` (no word ends at `a`); `startsWith("ca")` is `True`.

**Q2. Extend the trie to count how many inserted words start with a prefix (each insert counts, duplicates included).**

<details><summary>Hint</summary>Store a counter on every node and increase it on each node you pass while inserting.</summary></details>

**Answer:**

```python
class PrefixCounter:
    def __init__(self):
        self.root = {"#": 0}            # "#" holds the pass-through count

    def insert(self, word):
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {"#": 0})
            node["#"] += 1

    def count_prefix(self, prefix):
        node = self.root
        for ch in prefix:
            if ch not in node:
                return 0
            node = node[ch]
        return node["#"]


pc = PrefixCounter()
for w in ["apple", "app", "apply", "bat"]:
    pc.insert(w)
assert pc.count_prefix("app") == 3
assert pc.count_prefix("appl") == 2
assert pc.count_prefix("b") == 1
assert pc.count_prefix("c") == 0
```

Each operation is still `O(L)`.

**Q3. Return all stored words that start with a prefix, in alphabetical order (autocomplete).**

<details><summary>Hint</summary>Walk to the prefix node, then DFS below it, visiting children in sorted order and collecting every node marked as a word end.</summary></details>

**Answer:**

```python
def build_trie(words):
    root = {}
    for w in words:
        node = root
        for ch in w:
            node = node.setdefault(ch, {})
        node["$"] = True
    return root


def autocomplete(root, prefix):
    node = root
    for ch in prefix:
        if ch not in node:
            return []
        node = node[ch]
    results = []

    def dfs(n, path):
        if "$" in n:
            results.append(path)
        for ch in sorted(k for k in n if k != "$"):
            dfs(n[ch], path + ch)

    dfs(node, prefix)
    return results


t = build_trie(["car", "cart", "cat", "dog", "ca"])
assert autocomplete(t, "ca") == ["ca", "car", "cart", "cat"]
assert autocomplete(t, "d") == ["dog"]
assert autocomplete(t, "x") == []
```

**Q4. Find the longest common prefix of a list of words using a trie.**

<details><summary>Hint</summary>Insert all words, then walk down from the root while the node has exactly one child and no word ends there.</summary></details>

**Answer:**

```python
def longest_common_prefix(words):
    root = {}                    # same nested-dict trie as in Q3
    for w in words:
        node = root
        for ch in w:
            node = node.setdefault(ch, {})
        node["$"] = True

    node, prefix = root, ""
    while len(node) == 1 and "$" not in node:
        ch = next(iter(node))
        prefix += ch
        node = node[ch]
    return prefix


assert longest_common_prefix(["flower", "flow", "flight"]) == "fl"
assert longest_common_prefix(["dog", "racecar", "car"]) == ""
assert longest_common_prefix(["ab", "abc"]) == "ab"
```

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** Trie (prefix tree).
- **Key idea:** One node per character; `children` dict + `is_end` flag. `search` = walk + `is_end`; `startsWith` = walk only.
- **Time:** `O(L)` per operation.
- **Space:** `O(total inserted characters)` worst case; `O(1)` extra for lookups.
- **One-line memory hook:** *"Walk the doors letter by letter; a gold star means a whole word ends here."*

### Completion checklist

- [x] Problem requirements verified
- [x] Examples and constraints verified
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force solution written and tested
- [x] Optimized Python solution written and tested (`tools/tests/p052.py`), including the nested-dictionary alternative
- [x] Line-by-line explanation written
- [x] Dry run completed with the official example
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
