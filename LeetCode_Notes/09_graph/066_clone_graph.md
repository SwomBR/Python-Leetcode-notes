# 066. Clone Graph

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Clone Graph |
| **LeetCode number** | 133 |
| **Topic (source list)** | Graph |
| **Also uses** | Hash Table, Depth-First Search, Breadth-First Search |
| **Difficulty** | Medium |
| **LeetCode URL** | <https://leetcode.com/problems/clone-graph/> |
| **Pattern** | Graph traversal + "old node → new node" hash map |

---

## 2. Problem Explanation

### A quick graph primer (read this first if graphs are new to you)

This is the first graph note in the project, so here are the words you will see in every graph problem:

- **Node (vertex):** a "thing" — a person, a city, a course, a grid cell. Here each node is a `Node` object holding a number `val`.
- **Edge:** a connection between two nodes. In an **undirected** graph an edge goes both ways (if 1 is connected to 2, then 2 is connected to 1). In a **directed** graph an edge has an arrow (see Course Schedule, [067_course_schedule.md](067_course_schedule.md)).
- **Adjacency list:** for every node, the list of its neighbours. This is the most common way to store a graph.
- **Visited set / map:** graphs can have **cycles** (you can walk in a loop and come back to where you started). To avoid looping forever, we remember which nodes we have already handled.
- **DFS (depth-first search):** go as deep as possible along one path before backing up — naturally written with recursion or an explicit stack.
- **BFS (breadth-first search):** visit all neighbours first, then their neighbours, layer by layer — written with a queue.

```text
The graph from Example 1 (undirected, 4 nodes, 4 edges):

    1 ----- 2
    |       |
    |       |
    4 ----- 3

Adjacency list (index 0 describes node 1, index 1 describes node 2, ...):
    node 1: [2, 4]
    node 2: [1, 3]
    node 3: [2, 4]
    node 4: [1, 3]
```

Both DFS and BFS visit every node once and look at every edge a constant number of times, so both cost `O(V + E)` time, where `V` = number of nodes and `E` = number of edges.

### What are we given?

A reference to **one node** of a connected, undirected graph (or `None` if the graph is empty). Each node has:

- `val` — an integer;
- `neighbors` — a Python list of the `Node` objects it is connected to.

LeetCode's definition (shown for reference only — on LeetCode and in this project's verifier the class already exists, so you must **not** redefine it):

```text
# Definition for a Node.
# class Node:
#     def __init__(self, val = 0, neighbors = None):
#         self.val = val
#         self.neighbors = neighbors if neighbors is not None else []
```

### What must we return?

A **deep copy** of the whole graph: a brand-new set of `Node` objects with the same values and the same connections, and you return the copy of the node you were given.

"Deep" means **no node in your answer may be one of the original objects**. Returning `node` itself, or building new nodes whose `neighbors` lists point back at old nodes, is wrong.

### How LeetCode shows the tests

- Node values equal their 1-based position: the first node has `val = 1`, the second `val = 2`, and so on.
- The test input is written as an adjacency list `adjList`, where `adjList[i]` lists the neighbours of node `i + 1`.
- The node handed to your function is always the node with `val = 1`.
- The judge rebuilds an adjacency list from your returned node and compares it with the input. It also checks that your nodes are new objects.

### Examples

**Example 1**

```text
Input:  adjList = [[2,4],[1,3],[2,4],[1,3]]
Output: [[2,4],[1,3],[2,4],[1,3]]
```

Four nodes in a square: 1 touches 2 and 4, 2 touches 1 and 3, 3 touches 2 and 4, 4 touches 1 and 3. The copy must have the same shape.

**Example 2**

```text
Input:  adjList = [[]]
Output: [[]]
```

One node (`val = 1`) with no neighbours. The answer is a single new node with no neighbours.

**Example 3**

```text
Input:  adjList = []
Output: []
```

An empty graph: the input node is `None`, so return `None`.

### Constraints

- The number of nodes in the graph is in the range `[0, 100]`.
- `1 <= Node.val <= 100`
- `Node.val` is unique for each node.
- There are no repeated edges and no self-loops in the graph.
- The graph is connected and all nodes can be visited starting from the given node.

There is no follow-up.

---

## 3. Everyday Analogy

> **Explain it like I'm five**

Imagine a group of friends holding strings that tie them to each other. You want to build an **identical group of LEGO figures**, with LEGO strings tied in exactly the same pattern — but you may not use any of the real friends.

You walk up to the first friend and build their LEGO twin. Then you ask: *"Who are you tied to?"* For each of those friends you check your **notebook**: *"Have I already built a LEGO twin for this friend?"*

- If **yes**, just tie a LEGO string to the twin you already built.
- If **no**, build the twin now, write it in the notebook, and visit that friend next.

The notebook ("friend → LEGO twin") is the whole trick. Without it, two friends tied to each other would make you build twins forever, because each one keeps sending you back to the other.

---

## 4. Step-by-Step Logic

1. **Empty graph?** If `node` is `None`, return `None`.
2. **We must visit every node.** The graph is connected, so a traversal (DFS or BFS) from the given node reaches all of them.
3. **Every original node needs exactly one copy.** Keep a dictionary `old_to_new` that maps each original node to its copy. Dictionaries can use node objects as keys because Python hashes objects by identity by default.
4. **The dictionary doubles as the visited set.** If a node is already a key, we have already copied it — don't copy it again.
5. **Register the copy before visiting neighbours.** Cycles (like 1 → 2 → 1) would otherwise cause infinite recursion: when we come back to node 1, it must already be in the map.
6. **Wire the edges using copies only.** For each neighbour `nb` of an original node, append `old_to_new[nb]` (a copy) to the copy's neighbour list — never `nb` itself.
7. **Return `old_to_new[node]`**, the copy of the starting node.

---

## 5. Brute-Force Solution

### Algorithm (three simple passes)

There is no exponential "try everything" approach here, so the simplest correct method is to split the work into separate, easy passes:

1. **Collect** every original node with a BFS, using a visited set.
2. **Create** a fresh copy for each collected node (no edges yet) and store `original → copy` in a dictionary.
3. **Wire** the edges: for each original node, set the copy's neighbours to the copies of the original's neighbours.

### Python code

```python
from typing import Optional


class Solution:
    def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:
        if node is None:
            return None

        # Pass 1: collect every original node (BFS with a visited set).
        all_nodes = [node]
        visited = {node}
        i = 0
        while i < len(all_nodes):
            current = all_nodes[i]
            i += 1
            for nb in current.neighbors:
                if nb not in visited:
                    visited.add(nb)
                    all_nodes.append(nb)

        # Pass 2: create one copy per original node (no edges yet).
        copy_of = {}
        for original in all_nodes:
            copy_of[original] = Node(original.val)

        # Pass 3: wire edges between the copies, keeping neighbour order.
        for original in all_nodes:
            copy_of[original].neighbors = [copy_of[nb] for nb in original.neighbors]

        return copy_of[node]
```

### Explanation

- Pass 1 uses `all_nodes` as a queue (the index `i` plays the role of `popleft`) so every node is discovered exactly once.
- Pass 2 guarantees that **every** node already has a copy before any edge is wired, so pass 3 can never look up a missing copy.
- Pass 3 builds each new neighbour list from copies only, so nothing in the result points back to the original graph.

### Complexity — be honest

- **Time:** `O(V + E)`. Each pass touches each node once and each adjacency entry a constant number of times.
- **Auxiliary space:** `O(V)` for `all_nodes`, `visited` and `copy_of` (the `O(V + E)` new graph itself is the required output).

So this "brute force" is **not slower** than the optimized solution in big-O terms. It just walks the graph more times and uses an extra list and set. What it teaches: cloning a graph is really two separate jobs — *making nodes* and *making edges* — and the optimized solution simply fuses them into one traversal.

---

## 6. Optimized Solution

### Idea

Do a single DFS. The dictionary `old_to_new` is both the "visited" set and the lookup table for copies. When DFS reaches a node it has already copied, it returns the existing copy instead of making another one.

### Algorithm

1. Create an empty dictionary `old_to_new`.
2. Define `dfs(original)`:
   1. If `original` is already in `old_to_new`, return its copy.
   2. Otherwise create `copy = Node(original.val)` and store `old_to_new[original] = copy` **immediately**.
   3. For every neighbour `nb` of `original`, append `dfs(nb)` to `copy.neighbors`.
   4. Return `copy`.
3. Return `dfs(node)` if `node` exists, otherwise `None`.

### Python code (LeetCode-ready, DFS — recommended)

```python
from typing import Optional


class Solution:
    def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:
        old_to_new = {}  # original node -> its copy

        def dfs(original):
            if original in old_to_new:
                return old_to_new[original]
            copy = Node(original.val)
            old_to_new[original] = copy  # register BEFORE visiting neighbours
            for nb in original.neighbors:
                copy.neighbors.append(dfs(nb))
            return copy

        return dfs(node) if node else None
```

The recursion depth is at most the number of nodes, which is at most 100, so Python's default recursion limit (1000) is never a problem here.

### Alternative: BFS with a queue

Same idea, but iterative. A copy is created the moment a node is **discovered**, and edges are wired when a node is **processed**.

```python
from collections import deque
from typing import Optional


class Solution:
    def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:
        if node is None:
            return None
        old_to_new = {node: Node(node.val)}
        queue = deque([node])
        while queue:
            current = queue.popleft()
            for nb in current.neighbors:
                if nb not in old_to_new:          # first time we see nb
                    old_to_new[nb] = Node(nb.val)
                    queue.append(nb)
                old_to_new[current].neighbors.append(old_to_new[nb])
        return old_to_new[node]
```

Each node is processed exactly once, so each copy's neighbour list is built exactly once, in the same order as the original.

---

## 7. Line-by-Line Explanation

For the recommended DFS version:

| Line | What it does | Why |
|---|---|---|
| `old_to_new = {}` | Creates the map from original nodes to copies. | Lets us find a node's copy in `O(1)` and doubles as the visited set. |
| `def dfs(original):` | Helper that returns the copy of `original`, creating it if needed. | Recursion follows the edges for us. |
| `if original in old_to_new:` | Checks whether this node was already copied. | Stops infinite loops on cycles and prevents duplicate copies. |
| `return old_to_new[original]` | Reuses the existing copy. | Two edges pointing at the same node must point at the same copy. |
| `copy = Node(original.val)` | Builds a brand-new node with the same value and an empty neighbour list. | This is the "deep" part: a new object, not the old one. |
| `old_to_new[original] = copy` | Registers the copy **before** recursing. | If a neighbour leads back here (it always does in an undirected graph), the lookup above finds it. |
| `for nb in original.neighbors:` | Goes through the original neighbours in order. | Keeps the same neighbour order as the input. |
| `copy.neighbors.append(dfs(nb))` | Adds the **copy** of each neighbour. | `dfs(nb)` always returns a new node, never `nb` itself. |
| `return copy` | Hands the finished copy back to the caller. | The caller appends it to its own neighbour list. |
| `return dfs(node) if node else None` | Starts the DFS, or returns `None` for an empty graph. | Example 3 passes `None`. |

**Why use the node object as the key and not `val`?** Here values are unique, so `val` would also work. Using the object itself is the general solution: it still works when two different nodes share a value.

---

## 8. Dry Run

**Input:** `adjList = [[2,4],[1,3],[2,4],[1,3]]` (Example 1). Copies are written with a prime: `1'` is the copy of node 1.

| Step | Call | In map? | Action | `old_to_new` keys | Neighbour lists of copies after this step |
|---|---|---|---|---|---|
| 1 | `dfs(1)` | No | Create `1'`, register it, loop over `[2, 4]` | 1 | `1': []` |
| 2 | `dfs(2)` (from 1) | No | Create `2'`, register it, loop over `[1, 3]` | 1, 2 | `2': []` |
| 3 | `dfs(1)` (from 2) | **Yes** | Return `1'` | 1, 2 | `2': [1']` |
| 4 | `dfs(3)` (from 2) | No | Create `3'`, register it, loop over `[2, 4]` | 1, 2, 3 | `3': []` |
| 5 | `dfs(2)` (from 3) | **Yes** | Return `2'` | 1, 2, 3 | `3': [2']` |
| 6 | `dfs(4)` (from 3) | No | Create `4'`, register it, loop over `[1, 3]` | 1, 2, 3, 4 | `4': []` |
| 7 | `dfs(1)` (from 4) | **Yes** | Return `1'` | 1, 2, 3, 4 | `4': [1']` |
| 8 | `dfs(3)` (from 4) | **Yes** | Return `3'` (it is still being built — that's fine, it's the same object) | 1, 2, 3, 4 | `4': [1', 3']` → `dfs(4)` returns `4'` |
| 9 | back in `dfs(3)` | — | Append `4'` | — | `3': [2', 4']` → `dfs(3)` returns `3'` |
| 10 | back in `dfs(2)` | — | Append `3'` | — | `2': [1', 3']` → `dfs(2)` returns `2'` |
| 11 | back in `dfs(1)` | — | Append `2'`, then call `dfs(4)` | — | `1': [2']` |
| 12 | `dfs(4)` (from 1) | **Yes** | Return `4'` | — | `1': [2', 4']` → `dfs(1)` returns `1'` |

**Result:** `1': [2', 4']`, `2': [1', 3']`, `3': [2', 4']`, `4': [1', 3']` — serialized as `[[2,4],[1,3],[2,4],[1,3]]` ✅. Exactly four `Node(...)` constructors ran, and none of the returned objects is an original.

**Second dry run:** `adjList = [[]]` (Example 2). `dfs(1)` creates `1'`, the neighbour loop runs zero times, and `1'` is returned → `[[]]` ✅. For Example 3, `node` is `None`, so the function returns `None` → `[]` ✅.

---

## 9. Concepts, Data Structures, and Patterns

- **Graph basics:** nodes, undirected edges, adjacency lists, cycles (see the primer in section 2).
- **Hash map keyed by object identity:** `old_to_new` maps original objects to copies. Python's default `__hash__`/`__eq__` for user classes are identity-based, so each `Node` object is its own key.
- **Visited set = memo:** the same dictionary records "already handled" and stores the answer for that node. This is the memoization idea from dynamic programming applied to a graph.
- **DFS vs BFS:** both visit everything in `O(V + E)`. DFS is shorter to write; BFS avoids recursion.
- **Deep copy vs shallow copy:** a shallow copy reuses inner objects; a deep copy duplicates them. Python's `copy.deepcopy` actually handles cyclic graphs (it keeps its own memo dictionary), but interviewers want to see you build it yourself.
- **Related problems in this project:**
  - Course Schedule — directed graphs and cycle detection: [067_course_schedule.md](067_course_schedule.md)
  - Number of Islands — the same traversal on a grid: [069_number_of_islands.md](069_number_of_islands.md)
  - Graph Valid Tree: [072_graph_valid_tree_leetcode_premium.md](072_graph_valid_tree_leetcode_premium.md)
  - Serialize and Deserialize Binary Tree (turning a linked structure into a list and back): [../07_tree/046_serialize_and_deserialize_binary_tree.md](../07_tree/046_serialize_and_deserialize_binary_tree.md)
  - Two Sum — the same "look it up in a dictionary" habit: [../01_array/001_two_sum.md](../01_array/001_two_sum.md)

---

## 10. Complexity Analysis

`V` = number of nodes, `E` = number of edges (each undirected edge appears twice in the adjacency lists).

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Brute force (collect, create, wire) | `O(V + E)` | `O(V)` | Three linear passes; `all_nodes`, `visited`, `copy_of` each hold `V` items. |
| DFS + hash map (optimized) | `O(V + E)` | `O(V)` | Each node is created once; each adjacency entry triggers one `dfs` call that is `O(1)` if already copied. The map holds `V` entries and the recursion stack is at most `V` deep. |
| BFS + hash map | `O(V + E)` | `O(V)` | Each node is enqueued once; the queue and the map hold at most `V` entries. |

The new graph itself takes `O(V + E)` memory, but that is the required output, so it is not counted as auxiliary space. With at most 100 nodes and no repeated edges, `E <= 100·99/2 = 4950`, so every approach is instant.

---

## 11. Edge Cases

| Case | Input `adjList` | Expected result | Why |
|---|---|---|---|
| Empty graph | `[]` | `[]` (return `None`) | `node` is `None`; nothing to copy. |
| Single node | `[[]]` | `[[]]` | One new node, empty neighbour list. |
| Two nodes | `[[2],[1]]` | `[[2],[1]]` | The simplest cycle in undirected form: 1 → 2 → 1. The map stops the ping-pong. |
| Triangle | `[[2,3],[1,3],[1,2]]` | `[[2,3],[1,3],[1,2]]` | A real cycle; node 3 is reached from both 1 and 2 but copied once. |
| Path | `[[2],[1,3],[2,4],[3]]` | `[[2],[1,3],[2,4],[3]]` | Deepest DFS shape (depth = V). |
| Star | `[[2,3,4,5],[1],[1],[1],[1]]` | `[[2,3,4,5],[1],[1],[1],[1]]` | One hub; all leaves point back to the same copy of node 1. |

All of these, plus Example 1 and 200 random connected graphs (and one 100-node graph), are checked in `tools/tests/p066.py`, which also verifies that no returned node is an original object.

---

## 12. Common Mistakes and Debugging

1. **Returning the original (`return node`).** The values and shape match, but it is not a copy. The judge rejects it.
2. **Copying the neighbour list directly** (`copy.neighbors = original.neighbors` or `list(original.neighbors)`). The new node then points at *old* nodes — a shallow copy.
3. **Registering the copy after the recursion.** If you write the loop first and `old_to_new[original] = copy` afterwards, `dfs(1) → dfs(2) → dfs(1) → ...` never ends (`RecursionError`).
4. **Creating a new copy every time a node is reached.** Without the "already in map?" check, node 3 in a triangle would get two different copies and the clone would have more nodes than the original.
5. **Forgetting the `None` input.** `Node(node.val)` crashes with `AttributeError` on Example 3.
6. **(BFS) wiring edges when a node is discovered instead of when it is processed.** That can append the same neighbour twice. Wire edges only while processing `current`.

**Debugging tip:** after cloning, collect `id(x)` for every original and every copied node and check the two sets are disjoint; also print `[n.val for n in copy.neighbors]` for each copy and compare with the input adjacency list.

---

## 13. Practice Questions

**Q1. For Example 1, how many times is `Node(...)` called by the DFS solution, and how many times is `dfs` called in total?**

<details><summary>Hint</summary>One constructor per node; one `dfs` call for the start plus one per adjacency-list entry.</summary></details>

**Answer:** `Node(...)` runs **4** times (once per node). `dfs` runs `1 + (2 + 2 + 2 + 2) = 9` times: one initial call plus one per entry in the four neighbour lists. Five of those calls (steps 3, 5, 7, 8, 12 in the dry run) find the node already in the map.

**Q2. Write `to_adj_list(node)` that turns a graph (given by its node with `val = 1`) back into LeetCode's adjacency-list format.**

<details><summary>Hint</summary>Traverse with BFS and a visited set, then output the neighbour values for `val = 1, 2, ..., n`.</summary></details>

**Answer:**

```python
from collections import deque


def to_adj_list(node):
    if node is None:
        return []
    seen = {node}
    queue = deque([node])
    by_val = {}
    while queue:
        cur = queue.popleft()
        by_val[cur.val] = [nb.val for nb in cur.neighbors]
        for nb in cur.neighbors:
            if nb not in seen:
                seen.add(nb)
                queue.append(nb)
    return [by_val[v] for v in range(1, len(by_val) + 1)]


a, b = Node(1), Node(2)
a.neighbors, b.neighbors = [b], [a]
assert to_adj_list(a) == [[2], [1]]
assert to_adj_list(Node(1)) == [[]]
assert to_adj_list(None) == []
```

**Q3. Write `is_deep_copy(original, clone)` that returns `True` only if the two graphs have the same adjacency list and share no node objects.**

<details><summary>Hint</summary>Collect all reachable node objects from each start and compare their `id`s.</summary></details>

**Answer:**

```python
def reachable_nodes(start):
    if start is None:
        return []
    seen, stack = {start}, [start]
    while stack:
        cur = stack.pop()
        for nb in cur.neighbors:
            if nb not in seen:
                seen.add(nb)
                stack.append(nb)
    return list(seen)


def same_shape(a, b):
    def adj(start):
        return {n.val: [x.val for x in n.neighbors] for n in reachable_nodes(start)}
    return adj(a) == adj(b)


def is_deep_copy(original, clone):
    ids_a = {id(n) for n in reachable_nodes(original)}
    ids_b = {id(n) for n in reachable_nodes(clone)}
    return same_shape(original, clone) and not (ids_a & ids_b)


x, y = Node(1), Node(2)
x.neighbors, y.neighbors = [y], [x]
x2, y2 = Node(1), Node(2)
x2.neighbors, y2.neighbors = [y2], [x2]
assert is_deep_copy(x, x2) is True
assert is_deep_copy(x, x) is False          # same objects: not a copy
bad = Node(1)
bad.neighbors = [y]                         # new node 1 but old node 2
assert is_deep_copy(x, bad) is False
```

**Q4. A graph is given as a dictionary `{node_label: [neighbour labels]}` instead of `Node` objects. How do you "clone" it, and why is it so much easier?**

<details><summary>Hint</summary>Labels are plain integers — immutable values, not objects with identity.</summary></details>

**Answer:** Copy each list: `{k: list(v) for k, v in graph.items()}`. Integers are immutable, so sharing them is harmless; only the lists must be new. The `Node` version is harder because each node is a mutable object that other nodes point to, so we need the old → new map to keep all those pointers consistent.

```python
def clone_dict_graph(graph):
    return {k: list(v) for k, v in graph.items()}


g = {1: [2, 4], 2: [1, 3], 3: [2, 4], 4: [1, 3]}
g2 = clone_dict_graph(g)
assert g2 == g and all(g2[k] is not g[k] for k in g)
```

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** Graph traversal (DFS or BFS) + hash map `original → copy`.
- **Key idea:** The map is both the visited set and the copy lookup. Register a copy **before** visiting its neighbours; wire edges using copies only.
- **Time:** `O(V + E)`.
- **Auxiliary space:** `O(V)` (map + recursion stack or queue).
- **One-line memory hook:** *"Check the notebook, build the twin, write it down, then tie the strings."*

### Completion checklist

- [x] Problem requirements verified against the official statement
- [x] Examples and constraints verified
- [x] Graph primer, beginner-friendly analogy and logic written
- [x] Brute-force (three-pass) solution written and tested, with honest complexity
- [x] Optimized DFS solution and BFS alternative written and tested (`tools/tests/p066.py`)
- [x] Line-by-line explanation written
- [x] Dry run completed with Example 1 (plus Examples 2 and 3)
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
