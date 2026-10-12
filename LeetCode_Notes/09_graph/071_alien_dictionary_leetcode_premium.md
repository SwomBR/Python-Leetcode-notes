# 071. Alien Dictionary

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Alien Dictionary |
| **LeetCode number** | 269 (LeetCode Premium) |
| **Topic (source list)** | Graph |
| **Also uses** | Topological Sort, BFS (Kahn's algorithm), DFS, Hash Table, String |
| **Difficulty** | Hard |
| **LeetCode URL** | <https://leetcode.com/problems/alien-dictionary/> |
| **Pattern** | Build a directed graph from adjacent pairs, then topological sort |
| **Free practice** | LintCode 892 "Alien Dictionary" (check the LintCode number; LintCode's version asks for the *smallest* order in normal lexicographic order when several are valid, so its expected output can differ) |

---

## 2. Problem Explanation

> **Premium caveat:** This is a LeetCode Premium problem. The official statement could not be checked for these notes; the examples and constraints below are the commonly published ones — confirm them on LeetCode if you have Premium access.

### What are we given?

`words` — a list of strings written in an alien language that uses lowercase English letters, but in an **unknown alphabetical order**. The list is claimed to be **sorted** according to that alien order (the way words are sorted in a dictionary).

### What must we return?

A string containing **every distinct letter that appears in `words`, each exactly once**, arranged in an order that is consistent with the sorted list.

- If **several** orders are consistent, any one of them is accepted.
- If **no** order can make the list sorted, return the empty string `""`.

### How "sorted like a dictionary" works

Compare two neighbouring words letter by letter from the left:

1. At the **first position where they differ**, the letter in the earlier word must come before the letter in the later word. That single comparison is the *only* thing we learn from the pair — later letters tell us nothing.
2. If one word runs out before any difference appears, the **shorter word must come first** (just like "app" comes before "apple"). So `["abc", "ab"]` is impossible → return `""`.

### Examples (commonly published)

**Example 1**

```text
Input:  words = ["wrt", "wrf", "er", "ett", "rftt"]
Output: "wertf"
```

- "wrt" vs "wrf": first difference `t` vs `f` → `t` before `f`.
- "wrf" vs "er": `w` before `e`.
- "er" vs "ett": `r` before `t`.
- "ett" vs "rftt": `e` before `r`.
- Chain: `w → e → r → t → f`, so the only valid answer is `"wertf"`.

**Example 2**

```text
Input:  words = ["z", "x"]
Output: "zx"
```

**Example 3**

```text
Input:  words = ["z", "x", "z"]
Output: ""
```

The pairs say `z` before `x` **and** `x` before `z` — a contradiction (a cycle), so no valid order exists.

**Extra (rule 2):** `words = ["abc", "ab"]` → `""` because a longer word appears before its own prefix.

### Constraints (commonly published)

- `1 <= words.length <= 100`
- `1 <= words[i].length <= 100`
- `words[i]` consists of only lowercase English letters.

There is no official follow-up.

---

## 3. Everyday Analogy

> **Explain it like I'm five**

You find a class register from an alien school. The teacher wrote the children's names "in alphabetical order", but you don't know the alien alphabet. You want to rebuild it.

Look at two names next to each other, like "wrt" and "wrf". They start the same ("wr…"), and the first place they differ is `t` versus `f`. Because "wrt" is listed first, `t` must come before `f` in the alien alphabet. Write that down as an arrow on a sticky note: **t → f**.

Do this for every pair of neighbours and you get a pile of arrows. Now line the letters up so **every arrow points forward**. A good way: first pick a letter that **no arrow points to** (nobody needs to come before it), put it in line, tear up its arrows, and repeat. If at some point every remaining letter still has an arrow pointing at it, the arrows go in a circle — the register is broken, and the answer is "".

---

## 4. Step-by-Step Logic

1. **Collect every letter.** Each distinct letter must appear in the answer, even if no rule mentions it.
2. **Only compare neighbours.** Sorting is transitive: if word1 ≤ word2 and word2 ≤ word3, then word1 ≤ word3. So the rules from adjacent pairs already imply all others.
3. **Each adjacent pair gives at most one rule** — from its first differing position: `a → b` means "a comes before b".
4. **Prefix check.** If no position differs and the first word is longer, the input is invalid → `""`.
5. **The rules form a directed graph.** Letters are nodes; each rule is an edge.
6. **We need a topological order** — a list of nodes in which every edge points forward. One exists **if and only if** the graph has **no cycle**.
7. **Kahn's algorithm** finds it: count incoming edges (in-degree) for each letter; repeatedly take a letter with in-degree 0, output it, and lower the in-degree of its neighbours.
8. **Cycle detection is free:** if the output has fewer letters than the graph, some letters were stuck on a cycle → `""`.

---

## 5. Brute-Force Solution

### Algorithm

Try **every possible ordering** (permutation) of the distinct letters. For each one, translate every word into a list of ranks and check that the list of words is sorted. Return the first ordering that works; if none works, return `""`.

Python compares lists lexicographically, and a list that is a prefix of another counts as smaller (`[1, 2] < [1, 2, 3]`), so the prefix rule is handled automatically.

### Python code

```python
from typing import List
from itertools import permutations


class Solution:
    def alienOrder(self, words: List[str]) -> str:
        letters = sorted(set("".join(words)))
        for perm in permutations(letters):
            rank = {ch: i for i, ch in enumerate(perm)}
            ok = True
            for first, second in zip(words, words[1:]):
                if [rank[c] for c in first] > [rank[c] for c in second]:
                    ok = False
                    break
            if ok:
                return "".join(perm)
        return ""
```

### Explanation

- `letters` holds each distinct letter once.
- Each `perm` is one candidate alphabet; `rank` maps a letter to its position in it.
- Words are compared as rank lists. If any neighbouring pair is out of order, this alphabet fails.
- If no permutation keeps the list sorted (a contradiction or a prefix violation), we fall through to `""`.

### Complexity

- **Time:** `O(U! · C)`, where `U` is the number of distinct letters (at most 26) and `C` is the total number of characters. With `U = 26`, `26!` is about `4 × 10^26` — completely hopeless. It is only usable for tiny alphabets (it is tested here with at most 6 letters).
- **Auxiliary space:** `O(U + L)` for the rank map and the two rank lists being compared (`L` = longest word length), plus the iterator state.

The trade-off: the brute force is easy to trust (it literally checks the definition) but explodes factorially. The graph approach below is linear in the input size.

---

## 6. Optimized Solution

### Idea — topological sort with Kahn's algorithm (BFS)

Turn the adjacent-pair rules into a directed graph and output its letters in topological order.

### Algorithm

1. Create an empty neighbour set `graph[c]` and `indegree[c] = 0` for every letter in every word.
2. For each adjacent pair `(first, second)`:
   - Walk both words together. At the first `a != b`, add edge `a → b` (only once — use a set) and increase `indegree[b]`. Stop scanning this pair.
   - If no difference was found and `len(first) > len(second)`, return `""`.
3. Put every letter with `indegree == 0` in a queue.
4. While the queue is not empty: pop a letter, append it to `order`, and for each neighbour decrease its in-degree; push it when it reaches 0.
5. If `len(order)` is smaller than the number of letters, there is a cycle → return `""`. Otherwise return `"".join(order)`.

### Python code (LeetCode-ready)

```python
from typing import List
from collections import deque


class Solution:
    def alienOrder(self, words: List[str]) -> str:
        # 1. One node per distinct letter
        graph = {c: set() for word in words for c in word}
        indegree = {c: 0 for c in graph}

        # 2. One rule (at most) from each adjacent pair
        for first, second in zip(words, words[1:]):
            for a, b in zip(first, second):
                if a != b:
                    if b not in graph[a]:
                        graph[a].add(b)
                        indegree[b] += 1
                    break
            else:  # no differing letter found
                if len(first) > len(second):
                    return ""  # longer word placed before its own prefix

        # 3-4. Kahn's algorithm
        queue = deque(c for c in indegree if indegree[c] == 0)
        order = []
        while queue:
            c = queue.popleft()
            order.append(c)
            for nxt in graph[c]:
                indegree[nxt] -= 1
                if indegree[nxt] == 0:
                    queue.append(nxt)

        # 5. Letters left over were stuck on a cycle
        if len(order) < len(indegree):
            return ""
        return "".join(order)
```

### Alternative: DFS with three colours

A depth-first search also produces a topological order: a letter is finished only after everything that must come **after** it is finished, so the reversed finishing order is valid. Meeting a "grey" (in-progress) letter again means a cycle.

```python
from typing import List


class Solution:
    def alienOrder(self, words: List[str]) -> str:
        graph = {c: set() for word in words for c in word}
        for first, second in zip(words, words[1:]):
            for a, b in zip(first, second):
                if a != b:
                    graph[a].add(b)
                    break
            else:
                if len(first) > len(second):
                    return ""

        WHITE, GREY, BLACK = 0, 1, 2
        color = {c: WHITE for c in graph}
        finished = []

        def dfs(c: str) -> bool:          # returns False if a cycle is found
            color[c] = GREY
            for nxt in graph[c]:
                if color[nxt] == GREY:
                    return False
                if color[nxt] == WHITE and not dfs(nxt):
                    return False
            color[c] = BLACK
            finished.append(c)
            return True

        for c in graph:
            if color[c] == WHITE and not dfs(c):
                return ""
        return "".join(reversed(finished))
```

Recursion depth is at most 26 (one level per letter), so Python's recursion limit is not a concern here.

---

## 7. Line-by-Line Explanation

(Kahn's algorithm version)

| Line | What it does | Why |
|---|---|---|
| `graph = {c: set() for word in words for c in word}` | Creates a node for every distinct letter, with an empty set of "comes before" neighbours. | Letters that never appear in a rule must still be in the answer. A set prevents counting the same edge twice. |
| `indegree = {c: 0 for c in graph}` | Number of letters that must come before each letter. | In-degree 0 means "free to place now". |
| `for first, second in zip(words, words[1:]):` | Visits each adjacent pair. | Adjacent pairs are enough thanks to transitivity. |
| `for a, b in zip(first, second):` | Walks the two words side by side, stopping at the shorter length. | We look for the first difference. |
| `if a != b:` | First differing position found. | Only this position carries information. |
| `if b not in graph[a]:` / `graph[a].add(b)` / `indegree[b] += 1` | Adds edge `a → b` once and records one more prerequisite for `b`. | A duplicate edge would inflate `indegree[b]` and leave it stuck above 0 — the classic bug. |
| `break` | Stops scanning this pair. | Later letters say nothing about the order. |
| `else:` (attached to the `for`) | Runs only if the loop finished **without** `break`. | That means one word is a prefix of the other. |
| `if len(first) > len(second): return ""` | Detects "abc" before "ab". | No alphabet can make a word come before its own prefix. |
| `queue = deque(c for c in indegree if indegree[c] == 0)` | Starts with letters that have no prerequisites. | They can safely go first. |
| `c = queue.popleft()` / `order.append(c)` | Places the next free letter. | Everything required before `c` is already placed. |
| `indegree[nxt] -= 1` | "Tears up" the arrow `c → nxt`. | One prerequisite of `nxt` is now satisfied. |
| `if indegree[nxt] == 0: queue.append(nxt)` | `nxt` became free. | All its prerequisites are placed. |
| `if len(order) < len(indegree): return ""` | Some letters never reached in-degree 0. | They lie on (or behind) a cycle. |
| `return "".join(order)` | Builds the answer string. | `order` is a valid topological order. |

---

## 8. Dry Run

**Input:** `words = ["wrt", "wrf", "er", "ett", "rftt"]`

### Building the graph

Letters in first-seen order: `w, r, t, f, e`.

| Pair | First difference | Edge added | In-degrees after (`w r t f e`) |
|---|---|---|---|
| "wrt" / "wrf" | index 2: `t` vs `f` | `t → f` | 0 0 0 1 0 |
| "wrf" / "er" | index 0: `w` vs `e` | `w → e` | 0 0 0 1 1 |
| "er" / "ett" | index 1: `r` vs `t` | `r → t` | 0 0 1 1 1 |
| "ett" / "rftt" | index 0: `e` vs `r` | `e → r` | 0 1 1 1 1 |

### Kahn's algorithm

| Step | Queue before | Pop | `order` | In-degree changes | Pushed |
|---|---|---|---|---|---|
| start | `[w]` | — | `[]` | only `w` has in-degree 0 | — |
| 1 | `[w]` | `w` | `w` | `e`: 1 → 0 | `e` |
| 2 | `[e]` | `e` | `we` | `r`: 1 → 0 | `r` |
| 3 | `[r]` | `r` | `wer` | `t`: 1 → 0 | `t` |
| 4 | `[t]` | `t` | `wert` | `f`: 1 → 0 | `f` |
| 5 | `[f]` | `f` | `wertf` | none | — |

`len(order) = 5 = number of letters`, so there is no cycle. **Result:** `"wertf"` ✅

### Second dry run (cycle)

**Input:** `words = ["z", "x", "z"]`

| Pair | Edge | In-degrees (`z x`) |
|---|---|---|
| "z" / "x" | `z → x` | 0 1 |
| "x" / "z" | `x → z` | 1 1 |

No letter has in-degree 0, so the queue starts empty and `order = []`. `0 < 2` → **Result:** `""` ✅

---

## 9. Concepts, Data Structures, and Patterns

- **Directed graph from constraints:** each "a before b" fact becomes an edge `a → b`. Many ordering puzzles reduce to this.
- **Topological sort:** an ordering of a directed graph's nodes where every edge points forward. It exists exactly when the graph is a **DAG** (directed acyclic graph).
- **Kahn's algorithm (BFS):** repeatedly remove in-degree-0 nodes; leftover nodes reveal a cycle.
- **DFS with three colours:** white = unvisited, grey = on the current path, black = finished. Reaching a grey node = back edge = cycle.
- **Hash maps / sets:** `dict` for adjacency and in-degrees, `set` to avoid duplicate edges.
- **Python `for … else`:** the `else` runs only if the loop did not `break` — perfect for "no difference found".
- **Related notes:**
  - Course Schedule ([067_course_schedule.md](067_course_schedule.md)) — the same cycle detection / topological sort on prerequisites.
  - Graph Valid Tree ([072_graph_valid_tree_leetcode_premium.md](072_graph_valid_tree_leetcode_premium.md)) — cycle detection in an **undirected** graph.
  - Clone Graph ([066_clone_graph.md](066_clone_graph.md)) — basic graph traversal.
- **Similar problems:** Course Schedule II (LeetCode 210) returns the order itself; Verifying an Alien Dictionary (LeetCode 953) is the reverse task (see Q2 below).

---

## 10. Complexity Analysis

Let `C` = total number of characters in all words, `U` = number of distinct letters (≤ 26), `E` = number of edges (≤ number of adjacent pairs, and ≤ `U²`).

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Brute force (all permutations) | `O(U! · C)` | `O(U + L)` | Every alphabet ordering is checked against all adjacent pairs. |
| Kahn's algorithm (optimized) | `O(C + U + E)` = `O(C)` | `O(U + E)` | Building edges scans each adjacent pair at most up to the shorter word, so at most `C` character comparisons. The BFS touches each letter and each edge once. Since `U ≤ 26` and `E ≤ min(U², words.length − 1)`, the graph part is tiny. |
| DFS three-colour | `O(C + U + E)` | `O(U + E)` | Same graph; recursion depth ≤ `U`. |

---

## 11. Edge Cases

| Case | Example | Expected result | Why |
|---|---|---|---|
| Single word | `["z"]` | `"z"` | One letter, no rules. |
| Single word, several letters | `["abc"]` | any permutation of `a, b, c` (the Kahn version returns `"abc"`) | Letters inside one word give no ordering information. |
| Duplicate words | `["abc", "abc"]` | any permutation of `a, b, c` | Equal words are allowed in sorted order and give no rule. |
| Prefix, correct order | `["ab", "abc"]` | any permutation of `a, b, c` | Shorter word first is fine; no rule. |
| Prefix violation | `["abc", "ab"]` | `""` | A word cannot come before its own prefix. |
| Direct contradiction | `["z", "x", "z"]` | `""` | Cycle `z → x → z`. |
| Longer cycle | `["ab", "bc", "ca", "ab"]` | `""` | The three pairs give `a → b`, `b → c`, `c → a`: a cycle. |
| Letters without rules | `["ac", "ab", "zc", "zb"]` | any order with `c` before `b` and `a` before `z` (the Kahn version returns `"aczb"`) | Rules are `c → b` and `a → z`; every letter must still appear. |
| Unique chain | `["wrt", "wrf", "er", "ett", "rftt"]` | `"wertf"` | The rules form one chain. |

---

## 12. Common Mistakes and Debugging

1. **Comparing non-adjacent letters.** Only the **first** differing position counts. "wrt" vs "wrf" says `t → f`, nothing about later letters. Forgetting `break` adds false edges and can create fake cycles.
2. **Missing the prefix rule.** `["abc", "ab"]` has no differing letter, so no edge is added and a naive solution returns `"abc"`. You must return `""`.
3. **Counting the same edge twice.** If "a → b" is discovered twice, `indegree[b]` becomes 2 but only one edge is stored (or the edge is stored twice inconsistently). Use a set and only increment when the edge is new.
4. **Forgetting letters that have no edges.** Build nodes from **all** letters of **all** words, not just letters that appear in rules.
5. **Forgetting the cycle check.** Kahn's algorithm silently stops early on a cycle; you must compare `len(order)` with the number of letters.
6. **Comparing every pair of words (`O(n²)` pairs).** Not wrong, but unnecessary — adjacent pairs suffice.
7. **Expecting one exact string in tests.** When several orders are valid, any is accepted; test by validating the rules instead.

**Debugging tip:** print the edge list built from the pairs. Most bugs are in that step, not in the BFS.

---

## 13. Practice Questions

**Q1. Which rules do you get from `["baa", "abcd", "abca", "cab", "cad"]`, and what order does Kahn's algorithm return?**

<details><summary>Hint</summary>Look only at the first differing letter of each adjacent pair.</summary></details>

**Answer:** Pairs give `b → a` ("baa"/"abcd"), `d → a` ("abcd"/"abca"), `a → c` ("abca"/"cab"), `b → d` ("cab"/"cad"). Letters in first-seen order: `b, a, c, d`. In-degrees: `b 0, a 2, c 1, d 1`. Queue `[b]` → output `b`, which frees `d` (`a` still has in-degree 1) → output `d`, frees `a` → output `a`, frees `c` → output `c`. Answer: `"bdac"`, the only valid order.

**Q2. (LeetCode 953, Verifying an Alien Dictionary) Given `words` and a full alien `order` string, check whether `words` is sorted.**

<details><summary>Hint</summary>Map each letter to its rank and compare adjacent words as rank lists.</summary></details>

**Answer:**

```python
def is_alien_sorted(words, order):
    rank = {c: i for i, c in enumerate(order)}
    for first, second in zip(words, words[1:]):
        for a, b in zip(first, second):
            if a != b:
                if rank[a] > rank[b]:
                    return False
                break
        else:
            if len(first) > len(second):
                return False
    return True


assert is_alien_sorted(["hello", "leetcode"], "hlabcdefgijkmnopqrstuvwxyz") is True
assert is_alien_sorted(["word", "world", "row"], "worldabcefghijkmnpqstuvxyz") is False
assert is_alien_sorted(["apple", "app"], "abcdefghijklmnopqrstuvwxyz") is False
```

**Q3. How can you tell whether the alien alphabet is uniquely determined?**

<details><summary>Hint</summary>In Kahn's algorithm, when is there a choice?</summary></details>

**Answer:** The order is unique exactly when the queue never holds more than one letter (every step has only one possible next letter) and there is no cycle.

```python
from collections import deque


def unique_alien_order(words):
    graph = {c: set() for w in words for c in w}
    indeg = {c: 0 for c in graph}
    for first, second in zip(words, words[1:]):
        for a, b in zip(first, second):
            if a != b:
                if b not in graph[a]:
                    graph[a].add(b)
                    indeg[b] += 1
                break
        else:
            if len(first) > len(second):
                return None
    queue = deque(c for c in indeg if indeg[c] == 0)
    order = []
    while queue:
        if len(queue) > 1:
            return None          # a choice exists -> not unique
        c = queue.popleft()
        order.append(c)
        for nxt in graph[c]:
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                queue.append(nxt)
    return "".join(order) if len(order) == len(indeg) else None


assert unique_alien_order(["wrt", "wrf", "er", "ett", "rftt"]) == "wertf"
assert unique_alien_order(["ac", "ab", "zc", "zb"]) is None   # several valid orders
assert unique_alien_order(["z", "x", "z"]) is None            # no valid order
```

**Q4. Why is it enough to compare only adjacent words, not every pair?**

<details><summary>Hint</summary>Think about what "sorted" means for three words in a row.</summary></details>

**Answer:** Dictionary order is transitive: if `w1 ≤ w2` and `w2 ≤ w3` under some alphabet, then `w1 ≤ w3` under the same alphabet. So any alphabet that satisfies every adjacent pair automatically satisfies every pair. Comparing all pairs would add only redundant (implied) edges and cost `O(n²)` pair checks.

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** Constraints → directed graph → topological sort (Kahn's BFS or DFS).
- **Key idea:** Each adjacent pair gives one edge from its first differing letters; a longer word before its prefix is invalid; a cycle means `""`.
- **Time:** `O(C)` where `C` = total characters.
- **Auxiliary space:** `O(U + E)` (at most 26 letters).
- **One-line memory hook:** *"First difference makes an arrow; place letters nobody points at."*

### Completion checklist

- [x] Problem requirements written from the commonly published statement
- [ ] Examples and constraints verified against official statement — not possible: this is a LeetCode Premium problem and the official statement could not be fetched; the commonly published examples and constraints are used instead
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force solution written and tested
- [x] Optimized Python solution written and tested (`tools/tests/p071.py`), plus the DFS alternative; tests validate outputs because several orders can be correct
- [x] Line-by-line explanation written
- [x] Dry run completed with a real example
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
