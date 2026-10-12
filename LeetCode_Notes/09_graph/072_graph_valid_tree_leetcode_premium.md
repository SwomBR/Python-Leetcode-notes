# 072. Graph Valid Tree

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Graph Valid Tree |
| **LeetCode number** | 261 (LeetCode Premium) |
| **Topic (source list)** | Graph |
| **Also uses** | Union-Find (Disjoint Set Union), DFS, BFS |
| **Difficulty** | Medium |
| **LeetCode URL** | <https://leetcode.com/problems/graph-valid-tree/> |
| **Pattern** | Tree = connected + exactly `n − 1` edges; union-find cycle detection |
| **Free practice** | LintCode 178 "Graph Valid Tree" |

---

## 2. Problem Explanation

> **Premium caveat:** This is a LeetCode Premium problem. The official statement could not be checked for these notes; the examples and constraints below are the commonly published ones — confirm them on LeetCode if you have Premium access.

### What are we given?

- `n` — the number of nodes, labelled `0` to `n − 1`.
- `edges` — a list of pairs `[a, b]`, each an **undirected** edge connecting node `a` and node `b`.

### What must we return?

`True` if these edges make the nodes into a **valid tree**, otherwise `False`.

### What is a tree?

An undirected graph is a tree when **both** hold:

1. **Connected** — you can walk from any node to any other node.
2. **No cycles** — there is no way to leave a node and come back to it without reusing an edge.

A very useful fact: a graph with `n` nodes is a tree **if and only if** it is connected **and** has exactly `n − 1` edges. (Equivalently: it has no cycle and exactly `n − 1` edges.)

### Examples (commonly published)

**Example 1**

```text
Input:  n = 5, edges = [[0,1],[0,2],[0,3],[1,4]]
Output: true
```

Node 0 connects to 1, 2 and 3; node 1 connects to 4. Everything is reachable and there is no loop.

**Example 2**

```text
Input:  n = 5, edges = [[0,1],[1,2],[2,3],[1,3],[1,4]]
Output: false
```

`1 – 2 – 3 – 1` is a cycle. (Also, 5 edges is more than `n − 1 = 4`.)

### Constraints (commonly published)

- `1 <= n <= 2000`
- `0 <= edges.length <= 5000`
- `edges[i].length == 2`
- `0 <= ai, bi < n`
- `ai != bi` (no self-loops)
- There are no repeated edges.

There is no official follow-up.

---

## 3. Everyday Analogy

> **Explain it like I'm five**

You have `n` kids on a playground and some pieces of string. Each string ties two kids' hands together. The teacher asks: *"Is this a proper family tree of strings?"* That means:

- **Everyone is joined into one group** — pulling any kid eventually tugs every other kid.
- **No wasted string** — no string connects two kids who were *already* in the same group, because that string would make a loop.

Here's a counting trick: to join `n` separate kids into one group you need **exactly `n − 1` strings**, and every string must join two different groups. So we hand out strings one by one and keep a "which group are you in?" badge for each kid. If a string ever joins two kids who already wear the same badge, that's a loop — not a tree.

---

## 4. Step-by-Step Logic

1. **Count the edges first.** A tree on `n` nodes has exactly `n − 1` edges. Fewer → it cannot be connected; more → it must contain a cycle. If `len(edges) != n − 1`, return `False` immediately.
2. **Now we only need one more check.** With exactly `n − 1` edges, these three statements are equivalent: "connected", "acyclic", "a tree". So we only need to check *either* "no cycle" *or* "connected".
3. **Why?** Start with `n` separate nodes (`n` components). Each edge that does **not** close a cycle merges two components, reducing the count by exactly 1. If all `n − 1` edges merge, we end with `n − (n − 1) = 1` component — connected.
4. **Detect "this edge closes a cycle" with union-find.** Keep each node's group leader. An edge `(a, b)` whose endpoints already share a leader would create a cycle → `False`.
5. **Make union-find fast:** *path compression* (point nodes straight at their leader when you look them up) and *union by size* (hang the smaller group under the larger).
6. **Alternative:** after the edge-count check, run BFS/DFS from node 0 and check that all `n` nodes are reached.

---

## 5. Brute-Force Solution

### Algorithm

Without using the edge-count insight:

1. Add edges one at a time to an adjacency list. **Before** adding edge `(a, b)`, search (DFS) the graph built so far to see whether `a` can already reach `b`. If yes, this edge closes a cycle → return `False`.
2. After all edges are added without a cycle, check connectivity by searching from node 0 to every node.

### Python code

```python
from typing import List


class Solution:
    def validTree(self, n: int, edges: List[List[int]]) -> bool:
        adj = [[] for _ in range(n)]

        def connected(src: int, dst: int) -> bool:
            stack, seen = [src], {src}
            while stack:
                node = stack.pop()
                if node == dst:
                    return True
                for nxt in adj[node]:
                    if nxt not in seen:
                        seen.add(nxt)
                        stack.append(nxt)
            return False

        for a, b in edges:
            if connected(a, b):      # a and b already linked -> cycle
                return False
            adj[a].append(b)
            adj[b].append(a)

        # No cycle: now every node must be reachable from node 0
        return all(connected(0, v) for v in range(n))
```

### Explanation

- `connected` is an iterative DFS that answers "can `src` reach `dst` using the edges added so far?"
- If an edge's endpoints are already connected, adding it creates a second path between them → a cycle.
- If no cycle appeared, the graph is a forest; it is a tree only if node 0 reaches every node.
- Iterative DFS (a stack) avoids Python's recursion limit on long chains.

### Complexity

- **Time:** `O((E + n) · (n + E))`. Each of the `E` cycle checks and each of the `n` final reachability checks may scan the whole graph. With `n = 2000`, `E` up to 5000 this is tens of millions of steps — slow in Python, though correct.
- **Auxiliary space:** `O(n + E)` for the adjacency list, stack and `seen` set.

The trade-off: simple to reason about, but it repeats a full graph search for every edge. Union-find answers "same group?" in almost constant time.

---

## 6. Optimized Solution

### Idea — edge count + union-find

If `len(edges) != n − 1`, it's not a tree. Otherwise, union the endpoints of each edge; if two endpoints already share a root, there is a cycle. With exactly `n − 1` edges and no cycle, the graph is connected, so it's a tree.

### Algorithm

1. If `len(edges) != n − 1`: return `False`.
2. `parent[i] = i` and `size[i] = 1` for every node.
3. `find(x)`: follow `parent` pointers to the root, then point every node on the path directly at the root (path compression).
4. For each edge `(a, b)`: `ra, rb = find(a), find(b)`. If `ra == rb` → return `False`. Otherwise attach the smaller tree's root under the larger one (union by size).
5. Return `True`.

### Python code (LeetCode-ready)

```python
from typing import List


class Solution:
    def validTree(self, n: int, edges: List[List[int]]) -> bool:
        # A tree on n nodes has exactly n - 1 edges
        if len(edges) != n - 1:
            return False

        parent = list(range(n))
        size = [1] * n

        def find(x: int) -> int:
            root = x
            while parent[root] != root:       # walk up to the root
                root = parent[root]
            while parent[x] != root:          # path compression
                parent[x], x = root, parent[x]
            return root

        for a, b in edges:
            ra, rb = find(a), find(b)
            if ra == rb:                      # already connected -> cycle
                return False
            if size[ra] < size[rb]:           # union by size
                ra, rb = rb, ra
            parent[rb] = ra
            size[ra] += size[rb]

        return True  # n - 1 edges and no cycle => connected => tree
```

### Alternative: edge count + BFS connectivity

```python
from typing import List
from collections import deque


class Solution:
    def validTree(self, n: int, edges: List[List[int]]) -> bool:
        if len(edges) != n - 1:
            return False

        adj = [[] for _ in range(n)]
        for a, b in edges:
            adj[a].append(b)
            adj[b].append(a)

        seen = {0}
        queue = deque([0])
        while queue:
            node = queue.popleft()
            for nxt in adj[node]:
                if nxt not in seen:
                    seen.add(nxt)
                    queue.append(nxt)

        return len(seen) == n  # n - 1 edges and connected => tree
```

With exactly `n − 1` edges, "connected" alone proves the graph is a tree, so BFS does not even need to look for cycles.

---

## 7. Line-by-Line Explanation

(Union-find version)

| Line | What it does | Why |
|---|---|---|
| `if len(edges) != n - 1: return False` | Rejects the wrong number of edges. | Fewer edges cannot connect `n` nodes; more must create a cycle. |
| `parent = list(range(n))` | Every node starts as its own root. | Initially, `n` separate groups. |
| `size = [1] * n` | Each group has one node. | Used to hang smaller groups under larger ones. |
| `root = x` / `while parent[root] != root: root = parent[root]` | Climbs to the root (group leader). | Two nodes are in the same group iff they have the same root. |
| `while parent[x] != root: parent[x], x = root, parent[x]` | Re-points every node on the path straight at the root, then moves up. | Path compression makes later `find` calls almost `O(1)`. The right side is evaluated first, so `x` moves to its **old** parent. |
| `ra, rb = find(a), find(b)` | Roots of the two endpoints. | Compare groups, not nodes. |
| `if ra == rb: return False` | Endpoints already connected. | The new edge would make a second path → cycle. |
| `if size[ra] < size[rb]: ra, rb = rb, ra` | Ensures `ra` is the bigger group. | Union by size keeps trees shallow (height ≤ `log n`). |
| `parent[rb] = ra` / `size[ra] += size[rb]` | Merges the groups. | One fewer component. |
| `return True` | All `n − 1` edges merged two different groups. | `n − (n − 1) = 1` component, no cycle → tree. |

---

## 8. Dry Run

**Input:** `n = 5`, `edges = [[0,1],[0,2],[0,3],[1,4]]`

`len(edges) = 4 = n − 1` ✓. Start: `parent = [0,1,2,3,4]`, `size = [1,1,1,1,1]`.

| Edge | `find(a)` | `find(b)` | Same root? | Union (smaller under larger) | `parent` after | `size` of root |
|---|---|---|---|---|---|---|
| `[0,1]` | 0 | 1 | No | sizes 1 vs 1 → `parent[1] = 0` | `[0,0,2,3,4]` | `size[0] = 2` |
| `[0,2]` | 0 | 2 | No | 2 vs 1 → `parent[2] = 0` | `[0,0,0,3,4]` | `size[0] = 3` |
| `[0,3]` | 0 | 3 | No | 3 vs 1 → `parent[3] = 0` | `[0,0,0,0,4]` | `size[0] = 4` |
| `[1,4]` | 0 (via `1 → 0`) | 4 | No | 4 vs 1 → `parent[4] = 0` | `[0,0,0,0,0]` | `size[0] = 5` |

No cycle found. **Result:** `True` ✅

### Second dry run — Example 2

**Input:** `n = 5`, `edges = [[0,1],[1,2],[2,3],[1,3],[1,4]]`

`len(edges) = 5 ≠ 4` → **`False`** immediately ✅.

To see the cycle detection at work anyway, ignore the count check for a moment:

| Edge | Roots | Action | `parent` after |
|---|---|---|---|
| `[0,1]` | 0, 1 | `parent[1] = 0` | `[0,0,2,3,4]` |
| `[1,2]` | 0, 2 | `parent[2] = 0` | `[0,0,0,3,4]` |
| `[2,3]` | 0, 3 | `parent[3] = 0` | `[0,0,0,0,4]` |
| `[1,3]` | 0, 0 | **same root → cycle → `False`** | — |

### Third dry run — right count, still not a tree

**Input:** `n = 4`, `edges = [[0,1],[1,2],[2,0]]` (3 edges = `n − 1`)

`[0,1]` merges, `[1,2]` merges, `[2,0]`: `find(2) = 0 = find(0)` → cycle → `False` ✅. Node 3 is isolated; the edge "wasted" on the cycle is exactly the one that was needed to reach it.

---

## 9. Concepts, Data Structures, and Patterns

- **Tree characterization:** for an undirected graph with `n` nodes, any **two** of these imply the third — (1) connected, (2) acyclic, (3) exactly `n − 1` edges.
- **Union-Find / Disjoint Set Union (DSU):** maintains groups under "merge" and "same group?" operations.
  - **Path compression:** during `find`, link nodes directly to the root.
  - **Union by size (or rank):** attach the smaller tree under the larger.
  - With both, each operation costs amortized `O(α(n))`, where `α` is the inverse Ackermann function (≤ 4 for any practical `n`).
- **Cycle detection in undirected graphs:** union-find (an edge inside one group), or DFS that meets an already-visited node that is not the parent.
- **BFS/DFS connectivity:** count nodes reachable from one start node.
- **Related notes:**
  - Number of Connected Components ([073_number_of_connected_components_in_an_undirected_graph_leetcode_premium.md](073_number_of_connected_components_in_an_undirected_graph_leetcode_premium.md)) — the same union-find, counting groups instead.
  - Course Schedule ([067_course_schedule.md](067_course_schedule.md)) — cycle detection in a **directed** graph (different technique: colours/in-degrees).
  - Number of Islands ([069_number_of_islands.md](069_number_of_islands.md)) — connected components on a grid.
- **Similar problems:** Redundant Connection (LeetCode 684), Minimum Spanning Tree algorithms (Kruskal uses union-find).

---

## 10. Complexity Analysis

`n` = number of nodes, `E` = number of edges.

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Brute force (DFS per edge) | `O((E + n) · (n + E))` | `O(n + E)` | A full graph search for each edge and each final reachability check. |
| Union-find (optimized) | `O(n + E · α(n))` ≈ `O(n)` | `O(n)` | `O(n)` to build `parent`/`size`; each `find`/union is amortized `O(α(n))`. After the count check, `E = n − 1`. |
| Edge count + BFS | `O(n + E)` | `O(n + E)` | Build the adjacency list and visit each node and edge once. |

Note the early return: if `len(edges) != n − 1`, all approaches with the count check finish in `O(1)` (beyond reading the input).

---

## 11. Edge Cases

| Case | Example | Expected result | Why |
|---|---|---|---|
| Single node, no edges | `n = 1`, `[]` | `True` | One node is a tree (0 = `n − 1` edges). |
| Two nodes, no edges | `n = 2`, `[]` | `False` | Not connected. |
| Two nodes, one edge | `n = 2`, `[[1,0]]` | `True` | Edge direction does not matter. |
| Forest | `n = 4`, `[[0,1],[2,3]]` | `False` | Two components; only 2 edges. |
| `n − 1` edges with a cycle | `n = 4`, `[[0,1],[1,2],[2,0]]` | `False` | Cycle uses up an edge, leaving node 3 isolated. |
| Too many edges | `n = 3`, `[[0,1],[1,2],[2,0]]` | `False` | 3 edges > `n − 1`. |
| Long path | `n = 6`, `[[0,1],[1,2],[2,3],[3,4],[4,5]]` | `True` | A path is a tree. |

---

## 12. Common Mistakes and Debugging

1. **Checking only "no cycle".** `n = 4`, `[[0,1],[2,3]]` has no cycle but is disconnected. You need the edge count (or a connectivity check) too.
2. **Checking only "n − 1 edges".** `n = 4`, `[[0,1],[1,2],[2,0]]` has the right count but contains a cycle.
3. **Naive DFS cycle check that ignores the parent.** In an undirected graph, every edge appears in both adjacency lists, so a DFS from `a` sees `b`, then sees `a` again from `b`. Treat "visited node that is my parent" as normal, not as a cycle.
4. **Recursive DFS on long chains.** With `n = 2000`, a path graph needs recursion depth 2000, which exceeds Python's default limit (about 1000). Use an explicit stack, BFS, or union-find.
5. **Union without `find`.** Writing `parent[b] = a` instead of `parent[find(b)] = find(a)` breaks the group structure.
6. **Forgetting `n = 1`.** An empty edge list with one node must return `True`.

**Debugging tip:** print `parent` after each edge and draw the arrows; compare with the dry-run table.

---

## 13. Practice Questions

**Q1. Why must a tree with `n` nodes have exactly `n − 1` edges?**

<details><summary>Hint</summary>Count components as you add edges one by one.</summary></details>

**Answer:** Start with `n` isolated nodes = `n` components. An edge either joins two different components (count drops by 1) or lies inside one component (it creates a cycle). A tree has no cycles, so every edge drops the count by 1, and a tree ends with 1 component: `n − E = 1`, so `E = n − 1`.

**Q2. (LeetCode 684, Redundant Connection) A tree with one extra edge is given as a list of edges on nodes `1..n`. Return the edge that, if removed, leaves a tree (the last such edge in the input).**

<details><summary>Hint</summary>The first edge whose endpoints already share a union-find root is the extra one.</summary></details>

**Answer:**

```python
def find_redundant_connection(edges):
    n = len(edges)
    parent = list(range(n + 1))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]   # path halving
            x = parent[x]
        return x

    for a, b in edges:
        ra, rb = find(a), find(b)
        if ra == rb:
            return [a, b]
        parent[rb] = ra
    return []


assert find_redundant_connection([[1, 2], [1, 3], [2, 3]]) == [2, 3]
assert find_redundant_connection([[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]) == [1, 4]
```

(Since the graph is a tree plus one edge, exactly one cycle exists, and union-find reports the edge that closes it while scanning in input order, which is the last cycle edge in the input.)

**Q3. Write a DFS tree check that does not use the `n − 1` shortcut: detect cycles by tracking each node's parent.**

<details><summary>Hint</summary>From node `u` with parent `p`, seeing a visited neighbour other than `p` means a cycle (the input has no repeated edges).</summary></details>

**Answer:**

```python
def is_tree_dfs(n, edges):
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    seen = {0}
    stack = [(0, -1)]                 # (node, parent)
    while stack:
        node, par = stack.pop()
        for nxt in adj[node]:
            if nxt == par:
                continue
            if nxt in seen:
                return False          # reached a visited node another way
            seen.add(nxt)
            stack.append((nxt, node))
    return len(seen) == n


assert is_tree_dfs(5, [[0, 1], [0, 2], [0, 3], [1, 4]]) is True
assert is_tree_dfs(5, [[0, 1], [1, 2], [2, 3], [1, 3], [1, 4]]) is False
assert is_tree_dfs(4, [[0, 1], [2, 3]]) is False
assert is_tree_dfs(1, []) is True
```

This relies on the "no repeated edges" constraint: with a duplicate edge `[a, b]` twice, the parent-skip rule would hide a 2-edge cycle.

**Q4. What goes wrong without union by size and without path compression?**

<details><summary>Hint</summary>Try edges `[0,1],[1,2],[2,3],…` while always attaching the old root under the new node.</summary></details>

**Answer:** The union-find trees can degenerate into a long chain, so a single `find` walks `O(n)` pointers and `n` operations cost `O(n²)`. Union by size alone guarantees height ≤ `log₂ n` (a node's group at least doubles every time its depth increases); adding path compression brings the amortized cost down to `O(α(n))`.

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** Union-find cycle detection + edge counting.
- **Key idea:** Tree ⇔ exactly `n − 1` edges **and** no cycle (⇔ `n − 1` edges and connected). Reject on count, then union; a repeated root means a cycle.
- **Time:** `O(n + E · α(n))` ≈ linear.
- **Auxiliary space:** `O(n)`.
- **One-line memory hook:** *"`n` kids need `n − 1` strings, and no string may tie two kids already in the same group."*

### Completion checklist

- [x] Problem requirements written from the commonly published statement
- [ ] Examples and constraints verified against official statement — not possible: this is a LeetCode Premium problem and the official statement could not be fetched; the commonly published examples and constraints are used instead
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force solution written and tested
- [x] Optimized Python solution written and tested (`tools/tests/p072.py`), plus the BFS alternative
- [x] Line-by-line explanation written
- [x] Dry run completed with a real example
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
