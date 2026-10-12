# 073. Number of Connected Components in an Undirected Graph

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Number of Connected Components in an Undirected Graph |
| **LeetCode number** | 323 (LeetCode Premium) |
| **Topic (source list)** | Graph |
| **Also uses** | Union-Find (Disjoint Set Union), DFS, BFS |
| **Difficulty** | Medium |
| **LeetCode URL** | <https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/> |
| **Pattern** | Count components: union-find (start at `n`, subtract 1 per successful merge) or one traversal per unvisited node |
| **Free practice** | LintCode 3651 "Number of Connected Components in an Undirected Graph" (check the LintCode number — LintCode's numbering for this problem is not certain) |

---

## 2. Problem Explanation

> **Premium caveat:** This is a LeetCode Premium problem. The official statement could not be checked for these notes; the examples and constraints below are the commonly published ones — confirm them on LeetCode if you have Premium access.

### What are we given?

- `n` — the number of nodes, labelled `0` to `n − 1`.
- `edges` — a list of pairs `[a, b]`; each is an **undirected** edge between nodes `a` and `b`.

### What must we return?

The number of **connected components**: groups of nodes where every node in a group can reach every other node in that group by following edges, and no edge leaves the group.

A node with no edges at all is a component on its own.

### Examples (commonly published)

**Example 1**

```text
Input:  n = 5, edges = [[0,1],[1,2],[3,4]]
Output: 2
```

Groups: `{0, 1, 2}` and `{3, 4}`.

**Example 2**

```text
Input:  n = 5, edges = [[0,1],[1,2],[2,3],[3,4]]
Output: 1
```

All five nodes form one chain.

### Constraints (commonly published)

- `1 <= n <= 2000`
- `1 <= edges.length <= 5000`
- `edges[i].length == 2`
- `0 <= ai <= bi < n`
- `ai != bi`
- There are no repeated edges.

There is no official follow-up. (Our solutions also handle an empty `edges` list, which simply gives `n` components.)

---

## 3. Everyday Analogy

> **Explain it like I'm five**

Imagine `n` islands, and some bridges between pairs of islands. How many separate "countries" are there, if a country is a set of islands you can walk between using bridges?

**Way 1 — explore.** Stand on an island nobody has visited, plant your country's flag, and walk across every bridge you can, planting the same flag everywhere you reach. When you run out of places, that's one country. Find another unflagged island and start a new country. Count the flags you used.

**Way 2 — merge.** Pretend every island starts as its own country: `n` countries. Read the bridges one by one. If a bridge joins two **different** countries, they merge into one — the count drops by 1. If the bridge joins two islands already in the same country, nothing changes. The number left at the end is the answer.

---

## 4. Step-by-Step Logic

1. **Each node starts alone**, so there are `n` components before reading any edge.
2. **An edge either merges two components or does nothing.** If its endpoints are already in the same component, it adds a cycle but doesn't change the count. Otherwise it merges two components → count − 1.
3. **So:** `answer = n − (number of edges that merged two different components)`.
4. **Union-find** answers "are these two nodes in the same component?" in almost `O(1)` and merges components cheaply — exactly what step 2 needs.
5. **Traversal alternative:** build an adjacency list; for each node not yet visited, run BFS/DFS to mark its whole component, and add 1 to the count.
6. **Tree connection** (see [072](072_graph_valid_tree_leetcode_premium.md)): a graph is a tree exactly when it has `n − 1` edges and this count equals 1.

---

## 5. Brute-Force Solution

### Algorithm — repeated label propagation

1. Give every node a label equal to its own number.
2. Sweep over all edges; for each edge, set both endpoints' labels to the smaller of the two.
3. Repeat the sweep until a whole sweep changes nothing.
4. Every component now carries one label (its smallest node). Count distinct labels.

### Python code

```python
from typing import List


class Solution:
    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        label = list(range(n))
        changed = True
        while changed:
            changed = False
            for a, b in edges:
                low = min(label[a], label[b])
                if label[a] != low or label[b] != low:
                    label[a] = label[b] = low
                    changed = True
        return len(set(label))
```

### Explanation

- Labels only ever decrease, so the loop must stop.
- When nothing changes, both ends of every edge carry the same label, so every node in a component carries the same label. Two different components never exchange labels (no edge between them), so they keep different labels.
- The number of distinct labels is therefore the number of components.

### Complexity

- **Time:** `O(n · E)` in the worst case. One sweep is `O(E)`. The smallest label moves at least one more step along every path in each sweep, so at most about `n` sweeps are needed (e.g. a chain whose edges are listed in reverse order needs about `n` sweeps). With `n = 2000` and `E = 5000` this can reach about `10^7` operations — correct but wasteful.
- **Auxiliary space:** `O(n)` for the labels and the final set.

The trade-off: no graph structures are needed and correctness is easy to argue, but it may re-scan every edge many times. Union-find and DFS look at each edge essentially once.

---

## 6. Optimized Solution

### Idea — union-find with a component counter

Start with `components = n`. For every edge whose endpoints have different roots, merge them and decrement `components`.

### Algorithm

1. `parent[i] = i`, `size[i] = 1`, `components = n`.
2. `find(x)`: climb to the root, then compress the path.
3. For each edge `(a, b)`: `ra, rb = find(a), find(b)`. If different, attach the smaller root under the larger, update `size`, and do `components -= 1`.
4. Return `components`.

### Python code (LeetCode-ready)

```python
from typing import List


class Solution:
    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        parent = list(range(n))
        size = [1] * n

        def find(x: int) -> int:
            root = x
            while parent[root] != root:
                root = parent[root]
            while parent[x] != root:          # path compression
                parent[x], x = root, parent[x]
            return root

        components = n
        for a, b in edges:
            ra, rb = find(a), find(b)
            if ra == rb:
                continue                      # already in the same component
            if size[ra] < size[rb]:           # union by size
                ra, rb = rb, ra
            parent[rb] = ra
            size[ra] += size[rb]
            components -= 1                   # two components became one

        return components
```

### Alternative: iterative DFS

```python
from typing import List


class Solution:
    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        adj = [[] for _ in range(n)]
        for a, b in edges:
            adj[a].append(b)
            adj[b].append(a)

        visited = [False] * n
        components = 0
        for start in range(n):
            if visited[start]:
                continue
            components += 1                   # a brand-new component
            visited[start] = True
            stack = [start]
            while stack:
                node = stack.pop()
                for nxt in adj[node]:
                    if not visited[nxt]:
                        visited[nxt] = True
                        stack.append(nxt)

        return components
```

An explicit stack is used on purpose: a recursive DFS on a 2000-node chain would exceed Python's default recursion limit (about 1000).

---

## 7. Line-by-Line Explanation

(Union-find version)

| Line | What it does | Why |
|---|---|---|
| `parent = list(range(n))` | Each node is its own root. | `n` separate components at the start. |
| `size = [1] * n` | Size of each root's group. | Union by size keeps trees shallow. |
| `root = x` … `root = parent[root]` | Walks up to the root. | The root identifies the component. |
| `while parent[x] != root: parent[x], x = root, parent[x]` | Points each node on the path directly at the root. | Path compression: future `find`s are nearly `O(1)`. |
| `components = n` | Counter of current components. | Every node starts alone. |
| `ra, rb = find(a), find(b)` | Roots of both endpoints. | Same root ⇔ same component. |
| `if ra == rb: continue` | Skips edges inside one component. | They close a cycle but merge nothing. |
| `if size[ra] < size[rb]: ra, rb = rb, ra` | Makes `ra` the larger group. | Smaller under larger → height ≤ `log n`. |
| `parent[rb] = ra` / `size[ra] += size[rb]` | Merges the two groups. | One component now. |
| `components -= 1` | Records the merge. | Each successful merge removes exactly one component. |
| `return components` | Final count. | `n − (successful merges)`. |

---

## 8. Dry Run

**Input:** `n = 5`, `edges = [[0,1],[1,2],[3,4]]`

Start: `parent = [0,1,2,3,4]`, `size = [1,1,1,1,1]`, `components = 5`.

| Edge | `find(a)` | `find(b)` | Same? | Union | `parent` after | `components` |
|---|---|---|---|---|---|---|
| `[0,1]` | 0 | 1 | No | 1 vs 1 → `parent[1] = 0`, `size[0] = 2` | `[0,0,2,3,4]` | 4 |
| `[1,2]` | 0 (via `1 → 0`) | 2 | No | 2 vs 1 → `parent[2] = 0`, `size[0] = 3` | `[0,0,0,3,4]` | 3 |
| `[3,4]` | 3 | 4 | No | 1 vs 1 → `parent[4] = 3`, `size[3] = 2` | `[0,0,0,3,3]` | 2 |

**Result:** `2` ✅ (roots 0 and 3)

### Second dry run — brute force on the same input

| Sweep | After `[0,1]` | After `[1,2]` | After `[3,4]` | Changed? |
|---|---|---|---|---|
| 1 | `[0,0,2,3,4]` | `[0,0,0,3,4]` | `[0,0,0,3,3]` | Yes |
| 2 | `[0,0,0,3,3]` | `[0,0,0,3,3]` | `[0,0,0,3,3]` | No → stop |

Distinct labels `{0, 3}` → `2` ✅

### Third dry run — Example 2 with a cycle-free chain

`n = 5`, `edges = [[0,1],[1,2],[2,3],[3,4]]`: each of the 4 edges merges two different groups, so `components = 5 − 4 = 1` ✅.

---

## 9. Concepts, Data Structures, and Patterns

- **Connected component:** a maximal set of nodes that are mutually reachable.
- **Union-Find (DSU)** with **path compression** and **union by size/rank**: amortized `O(α(n))` per operation, where `α` (inverse Ackermann) is at most 4 for any realistic input.
- **Counting by subtraction:** `components = n − successful unions` — a common union-find trick.
- **Graph traversal (DFS/BFS):** every traversal started from an unvisited node discovers exactly one new component.
- **Adjacency list:** `adj[v]` lists neighbours; build it by adding each undirected edge in **both** directions.
- **Related notes:**
  - Graph Valid Tree ([072_graph_valid_tree_leetcode_premium.md](072_graph_valid_tree_leetcode_premium.md)) — tree ⇔ `n − 1` edges and exactly 1 component.
  - Number of Islands ([069_number_of_islands.md](069_number_of_islands.md)) — the same counting on a grid, where neighbours are the 4 adjacent cells.
  - Clone Graph ([066_clone_graph.md](066_clone_graph.md)) — graph traversal with a visited map.
  - Longest Consecutive Sequence ([070_longest_consecutive_sequence.md](070_longest_consecutive_sequence.md)) — can also be solved with union-find over values.
- **Similar problems:** Number of Provinces (LeetCode 547), Number of Operations to Make Network Connected (LeetCode 1319), Accounts Merge (LeetCode 721).

---

## 10. Complexity Analysis

`n` = number of nodes, `E` = number of edges.

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Brute force (label propagation) | `O(n · E)` | `O(n)` | Up to about `n` sweeps over all `E` edges. |
| Union-find (optimized) | `O(n + E · α(n))` ≈ `O(n + E)` | `O(n)` | Arrays of size `n`; two `find`s and at most one union per edge. |
| Iterative DFS / BFS | `O(n + E)` | `O(n + E)` | Adjacency list holds `2E` entries; each node is pushed once and each adjacency entry is scanned once. |

Union-find needs only `O(n)` extra memory because it never stores the edges, which also makes it a good fit when edges arrive as a stream.

---

## 11. Edge Cases

| Case | Example | Expected result | Why |
|---|---|---|---|
| Single node | `n = 1`, `[]` | `1` | One node is one component. |
| No edges (outside the published constraints, but harmless) | `n = 4`, `[]` | `4` | Every node is alone. |
| Cycle | `n = 3`, `[[0,1],[1,2],[0,2]]` | `1` | The third edge joins nodes already connected; count stays 1. |
| Several pairs | `n = 6`, `[[0,1],[2,3],[4,5]]` | `3` | Three separate pairs. |
| Isolated nodes plus one edge | `n = 4`, `[[2,3]]` | `3` | `{0}`, `{1}`, `{2,3}`. |
| Long chain | `n = 2000`, edges `i – i+1` | `1` | Recursive DFS would hit the recursion limit; union-find and iterative DFS are fine. |

---

## 12. Common Mistakes and Debugging

1. **Adding the edge in only one direction** in the adjacency list. For undirected graphs, append both `adj[a].append(b)` and `adj[b].append(a)`, otherwise a DFS from `b` cannot reach `a`.
2. **Decrementing on every edge.** Only edges that join two **different** roots reduce the count. A cycle edge must be skipped.
3. **Comparing nodes instead of roots.** `if parent[a] != parent[b]` is wrong after several unions; always compare `find(a)` and `find(b)`.
4. **Forgetting isolated nodes** when counting from the edge list only (e.g. counting distinct nodes that appear in edges). Nodes with no edges are still components.
5. **Recursive DFS on large inputs.** Depth up to 2000 exceeds Python's default limit; use an explicit stack or BFS, or union-find.
6. **Marking visited when popping instead of when pushing.** It still gives the right count, but the same node can be pushed many times, wasting time and memory.

**Debugging tip:** after processing, print `{find(v) for v in range(n)}`. Its size must equal your `components` counter.

---

## 13. Practice Questions

**Q1. Take `n = 7`, edges `[[0,1],[1,2],[2,0],[3,4]]`. How many successful unions happen, and what is the answer?**

<details><summary>Hint</summary>Answer = `n` − successful unions. The edge `[2,0]` closes a cycle.</summary></details>

**Answer:** `[0,1]` ✓, `[1,2]` ✓, `[2,0]` ✗ (same root), `[3,4]` ✓ → 3 successful unions. `7 − 3 = 4` components: `{0,1,2}`, `{3,4}`, `{5}`, `{6}`.

**Q2. (LeetCode 547, Number of Provinces) The graph is given as an `n × n` adjacency matrix `is_connected`. Count the components.**

<details><summary>Hint</summary>Same DFS, but neighbours of `i` are all `j` with `is_connected[i][j] == 1`.</summary></details>

**Answer:**

```python
def find_circle_num(is_connected):
    n = len(is_connected)
    visited = [False] * n
    count = 0
    for start in range(n):
        if visited[start]:
            continue
        count += 1
        visited[start] = True
        stack = [start]
        while stack:
            i = stack.pop()
            for j in range(n):
                if is_connected[i][j] and not visited[j]:
                    visited[j] = True
                    stack.append(j)
    return count


assert find_circle_num([[1, 1, 0], [1, 1, 0], [0, 0, 1]]) == 2
assert find_circle_num([[1, 0, 0], [0, 1, 0], [0, 0, 1]]) == 3
```

Time `O(n²)` because the matrix has `n²` cells.

**Q3. (LeetCode 1319, Number of Operations to Make Network Connected) You may move existing cables. What is the minimum number of moves to connect all `n` computers, or −1 if impossible?**

<details><summary>Hint</summary>You need at least `n − 1` cables in total. If you have them, each extra component needs exactly one moved cable.</summary></details>

**Answer:** If `len(connections) < n − 1` → `-1`. Otherwise the answer is `components − 1`: every component beyond the first must be linked by one cable, and spare (cycle) cables are guaranteed to exist because there are enough cables overall.

```python
def make_connected(n, connections):
    if len(connections) < n - 1:
        return -1
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    components = n
    for a, b in connections:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra
            components -= 1
    return components - 1


assert make_connected(4, [[0, 1], [0, 2], [1, 2]]) == 1
assert make_connected(6, [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3]]) == 2
assert make_connected(6, [[0, 1], [0, 2], [0, 3], [1, 2]]) == -1
```

**Q4. Return the sizes of all components in descending order.**

<details><summary>Hint</summary>After all unions, count how many nodes share each root.</summary></details>

**Answer:**

```python
from collections import Counter


def component_sizes(n, edges):
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b in edges:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra
    return sorted(Counter(find(v) for v in range(n)).values(), reverse=True)


assert component_sizes(5, [[0, 1], [1, 2], [3, 4]]) == [3, 2]
assert component_sizes(4, [[2, 3]]) == [2, 1, 1]
```

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** Union-find component counting (or one DFS/BFS per unvisited node).
- **Key idea:** Start with `n` components; every edge that joins two different roots reduces the count by 1.
- **Time:** `O(n + E · α(n))` (union-find) or `O(n + E)` (DFS/BFS).
- **Auxiliary space:** `O(n)` (union-find) or `O(n + E)` (DFS/BFS with adjacency list).
- **One-line memory hook:** *"Every island is a country until a bridge merges two of them."*

### Completion checklist

- [x] Problem requirements written from the commonly published statement
- [ ] Examples and constraints verified against official statement — not possible: this is a LeetCode Premium problem and the official statement could not be fetched; the commonly published examples and constraints are used instead
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force solution written and tested
- [x] Optimized Python solution written and tested (`tools/tests/p073.py`), plus the iterative DFS alternative
- [x] Line-by-line explanation written
- [x] Dry run completed with a real example
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
