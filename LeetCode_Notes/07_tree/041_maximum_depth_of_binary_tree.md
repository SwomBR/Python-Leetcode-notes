# 041. Maximum Depth of Binary Tree

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Maximum Depth of Binary Tree |
| **LeetCode number** | 104 |
| **Topic (source list)** | Tree |
| **Also uses** | Depth-First Search, Breadth-First Search, Recursion |
| **Difficulty** | Easy |
| **LeetCode URL** | <https://leetcode.com/problems/maximum-depth-of-binary-tree/> |
| **Pattern** | Post-order recursion ("ask the children, then combine") / level-by-level BFS |

---

## 2. Problem Explanation

### Beginner primer: what is a `TreeNode`?

A **binary tree** is made of **nodes**. Each node stores a value and points to at most two children: a **left** child and a **right** child. A missing child is `None`. The top node is the **root**; a node with no children is a **leaf**.

LeetCode describes the node class in a comment above your code (it already exists on LeetCode — you never write it yourself):

```text
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
```

Your function receives **only the root node** (or `None` for an empty tree). Everything else is reached by following `.left` and `.right`.

### How LeetCode's list input becomes a tree

LeetCode writes trees as a **level-order list**: read the tree top to bottom, each row left to right, writing `null` where a child is missing. Children are filled in pairs (left, right) for each real node, in the order those nodes appeared. Trailing `null`s are dropped.

`root = [3,9,20,null,null,15,7]` is read like this:

| List item | Meaning |
|---|---|
| `3` | the root |
| `9`, `20` | left and right child of `3` |
| `null`, `null` | `9` has no left and no right child |
| `15`, `7` | left and right child of `20` |

```text
        3
       / \
      9   20
         /  \
        15   7
```

Note that `null` children do **not** get their own child slots — that is why `15, 7` belong to `20`, not to the missing children of `9`.

### What are we given?

`root` — the root of a binary tree (possibly `None`, meaning an empty tree).

### What must we return?

The tree's **maximum depth**: how many nodes lie on the **longest path that starts at the root and goes downward to a leaf**. We count **nodes**, not edges, so a single-node tree has depth 1 and an empty tree has depth 0.

### Examples

**Example 1**

```text
Input:  root = [3,9,20,null,null,15,7]
Output: 3
```

The longest downward paths are `3 → 20 → 15` and `3 → 20 → 7`, each with 3 nodes.

**Example 2**

```text
Input:  root = [1,null,2]
Output: 2
```

```text
    1
     \
      2
```

Root `1` has no left child and a right child `2`. The path `1 → 2` has 2 nodes.

### Constraints

- The number of nodes in the tree is in the range `[0, 10^4]`.
- `-100 <= Node.val <= 100`

There is no follow-up for this problem. The values never matter — only the **shape** of the tree does.

---

## 3. Everyday Analogy

> **Explain it like I'm five**

Think of a family tree drawn on a wall, with great-grandma at the top. You want to know: "How many generations tall is the longest line in this family?"

Great-grandma can't see the whole wall, so she asks each of her (at most two) children: *"How many generations tall is **your** part of the family?"* Each child asks their own children the same question, and so on. Someone with no children simply answers *"Just me — 1."*

When the answers come back up, each person says: *"Take the taller of my children's answers and add 1 for me."* When great-grandma gets her answers back and adds herself, she knows the height of the whole family.

A second way: line the family up **row by row** — great-grandma in row 1, her children in row 2, grandchildren in row 3… The number of rows is the answer.

---

## 4. Step-by-Step Logic

1. **Smallest cases first.** An empty tree (`None`) has depth 0. A single leaf has depth 1.
2. **Split the problem.** The longest root-to-leaf path goes either into the left subtree or into the right subtree. Each subtree is itself a binary tree, so we can ask the **same question** about it.
3. **Combine.** `depth(node) = 1 + max(depth(node.left), depth(node.right))`. The `1` counts the node itself.
4. **This is recursion with a base case.** The base case `node is None → 0` stops the recursion and also makes leaves work automatically: a leaf gets `1 + max(0, 0) = 1`.
5. **Order of work:** children are finished before the parent (post-order). Every node is visited exactly once.
6. **Alternative view (BFS):** process the tree one level at a time with a queue. Each time we finish a full level, add 1. The count of levels is the depth.
7. **Watch the recursion depth.** A recursive call chain is as long as the tree is tall. For a very tall, skewed tree this matters in Python (see section 6).

---

## 5. Brute-Force Solution

### Algorithm

Ask a yes/no question over and over: *"Does the tree have any node at depth `d`?"* for `d = 1, 2, 3, …`. Each question is answered by a fresh DFS that walks down at most `d` levels. The first `d` that has **no** node tells us the depth is `d - 1`.

### Python code

```python
from typing import Optional


class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        def has_node_at(node: Optional[TreeNode], depth: int) -> bool:
            # Is there a node exactly `depth` levels down, counting `node` as level 1?
            if node is None:
                return False
            if depth == 1:
                return True
            return has_node_at(node.left, depth - 1) or has_node_at(node.right, depth - 1)

        depth = 0
        while has_node_at(root, depth + 1):
            depth += 1
        return depth
```

### Explanation

- `has_node_at(root, d)` explores every node at depths `1..d` (stopping early if it finds one at depth `d`).
- The loop keeps increasing `depth` while the next level exists. For an empty tree, `has_node_at(None, 1)` is `False` immediately, so we return 0.
- It is correct because depths are "contiguous": if a node exists at depth `d`, its parent exists at depth `d - 1`, so the first missing level marks the end.

### Complexity

- **Time:** `O(n · h)`, where `h` is the tree height. We run `h + 1` probes, and each probe can visit up to `n` nodes. Balanced tree: `O(n log n)`. Skewed tree (a chain): probe `d` walks `d` nodes, so the total is about `h²/2` — about 50 million steps when `n = h = 10^4`, which is far too slow in Python. The waste: upper levels are re-walked on every probe.
- **Auxiliary space:** `O(h)` for the recursion stack of one probe.

---

## 6. Optimized Solution

### Idea

Visit every node **once** and let each node report its own depth to its parent: `1 + max(left, right)`.

### Algorithm (recursive DFS)

1. If `root` is `None`, return 0.
2. Recursively get the depth of the left subtree and of the right subtree.
3. Return `1 + max(left_depth, right_depth)`.

### Python code (LeetCode-ready, recursive DFS)

```python
from typing import Optional


class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if root is None:              # empty tree / missing child
            return 0
        left_depth = self.maxDepth(root.left)
        right_depth = self.maxDepth(root.right)
        return 1 + max(left_depth, right_depth)
```

### Python code (iterative BFS, level by level)

```python
from collections import deque
from typing import Optional


class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if root is None:
            return 0
        depth = 0
        queue = deque([root])
        while queue:
            depth += 1                         # we are about to process one full level
            for _ in range(len(queue)):        # exactly the nodes of this level
                node = queue.popleft()
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
        return depth
```

### Python code (iterative DFS with an explicit stack)

```python
from typing import Optional


class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        best = 0
        stack = [(root, 1)] if root else []    # (node, depth of that node)
        while stack:
            node, depth = stack.pop()
            best = max(best, depth)
            if node.left:
                stack.append((node.left, depth + 1))
            if node.right:
                stack.append((node.right, depth + 1))
        return best
```

### Recursion limit — is the recursive version safe?

- Python's default recursion limit is **1000** frames (`sys.getrecursionlimit()`).
- The recursive solution uses one frame per level, so it needs about `h + 1` frames.
- The constraints allow up to `10^4` nodes, so a completely **skewed** tree (a chain) can be `10^4` levels tall. With the default limit of 1000 that would raise `RecursionError` in a plain Python script.
- The recursive solution is widely reported to be accepted on LeetCode (its judge's recursion settings are not documented, so this note does not rely on them). But the only version that is safe **everywhere** for this constraint range is an iterative one (BFS or explicit stack). In your own scripts you could call `sys.setrecursionlimit(20000)`, but the iterative versions avoid the issue entirely.
- For balanced trees the height is only about `log2(10^4) ≈ 14`, so recursion is never a problem there.

---

## 7. Line-by-Line Explanation

**Recursive DFS**

| Line | What it does | Why |
|---|---|---|
| `if root is None: return 0` | Base case. | An empty subtree contributes no nodes. It also stops the recursion. |
| `left_depth = self.maxDepth(root.left)` | Depth of the left subtree. | Same problem on a smaller tree. |
| `right_depth = self.maxDepth(root.right)` | Depth of the right subtree. | Same problem on the other side. |
| `return 1 + max(left_depth, right_depth)` | Picks the taller side and counts the current node. | The longest path through this node continues into its taller subtree. |

**Iterative BFS**

| Line | What it does | Why |
|---|---|---|
| `if root is None: return 0` | Handles the empty tree. | Otherwise we would put `None` into the queue. |
| `queue = deque([root])` | Queue holding the current level. | `deque.popleft()` is `O(1)`; `list.pop(0)` would be `O(n)`. |
| `depth += 1` | Counts a new level. | Each outer-loop iteration processes exactly one level. |
| `for _ in range(len(queue))` | Freezes the size of the current level. | Children appended during the loop belong to the **next** level and are not processed yet. |
| `if node.left: queue.append(...)` | Schedules children for the next level. | Missing children are skipped. |
| `return depth` | Number of levels processed. | One level = one node on the longest root-to-leaf path. |

---

## 8. Dry Run

**Input:** `root = [3,9,20,null,null,15,7]` (recursive DFS)

```text
        3
       / \
      9   20
         /  \
        15   7
```

| Step | Call | `left_depth` | `right_depth` | Returns | Note |
|---|---|---|---|---|---|
| 1 | `maxDepth(3)` | (waits) | (waits) | — | starts with the left child |
| 2 | `maxDepth(9)` | `maxDepth(None) = 0` | `maxDepth(None) = 0` | `1 + max(0, 0) = 1` | 9 is a leaf |
| 3 | back in `maxDepth(3)` | 1 | (waits) | — | now the right child |
| 4 | `maxDepth(20)` | (waits) | (waits) | — | |
| 5 | `maxDepth(15)` | 0 | 0 | 1 | leaf |
| 6 | `maxDepth(7)` | 0 | 0 | 1 | leaf |
| 7 | finish `maxDepth(20)` | 1 | 1 | `1 + max(1, 1) = 2` | |
| 8 | finish `maxDepth(3)` | 1 | 2 | `1 + max(1, 2) = 3` | |

**Result:** `3` ✅

**Second dry run (BFS), same tree:**

| Outer iteration | Queue at start | `depth` after `+= 1` | Nodes popped | Queue at end |
|---|---|---|---|---|
| 1 | `[3]` | 1 | 3 | `[9, 20]` |
| 2 | `[9, 20]` | 2 | 9, 20 | `[15, 7]` |
| 3 | `[15, 7]` | 3 | 15, 7 | `[]` |

Queue empty → return `3` ✅

**Example 2:** `[1,null,2]` → `maxDepth(2) = 1`, `maxDepth(1) = 1 + max(0, 1) = 2` ✅

---

## 9. Concepts, Data Structures, and Patterns

- **Binary tree and `TreeNode`:** nodes linked by `.left` / `.right`; `None` marks a missing child.
- **Recursion on trees:** "solve for the children, combine at the parent." The base case is the empty tree.
- **Post-order traversal:** the children's results are needed before the parent can answer.
- **Breadth-first search (BFS) with `collections.deque`:** visit nodes level by level. The `for _ in range(len(queue))` trick separates levels — the same trick builds the answer in [045_binary_tree_level_order_traversal.md](045_binary_tree_level_order_traversal.md).
- **Height vs depth:** the "maximum depth" of the tree equals the **height** of the root counted in nodes.
- **Related notes in this project:**
  - [042_same_tree.md](042_same_tree.md) and [043_invertflip_binary_tree.md](043_invertflip_binary_tree.md) use the same "recurse on both children" shape.
  - [044_binary_tree_maximum_path_sum.md](044_binary_tree_maximum_path_sum.md) is the same post-order idea, but returning a *best downward sum* instead of a height.
- **Related LeetCode problems:** Minimum Depth of Binary Tree (111), Balanced Binary Tree (110), Diameter of Binary Tree (543).

---

## 10. Complexity Analysis

Let `n` = number of nodes and `h` = height of the tree (between about `log2 n` for a balanced tree and `n` for a chain).

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Brute force (probe each depth) | `O(n · h)` (worst `O(n²)`) | `O(h)` | `h + 1` separate DFS probes; upper levels are re-walked each time. |
| Recursive DFS | `O(n)` | `O(h)` — best `O(log n)` (balanced), worst `O(n)` (skewed) | Each node is visited once; the call stack holds one frame per level of the current path. |
| Iterative BFS | `O(n)` | `O(w)`, `w` = widest level — up to about `n/2` for a complete tree, `O(1)` for a chain | The queue holds at most one full level plus some of the next. |
| Iterative DFS (stack) | `O(n)` | `O(h)` | Each level of the current path leaves at most one pending sibling on the stack. |

DFS and BFS have opposite worst cases: DFS uses the most memory on a tall, thin tree; BFS on a short, wide tree.

---

## 11. Edge Cases

| Case | Example | Expected result | Why |
|---|---|---|---|
| Empty tree | `[]` | `0` | No nodes, no path. |
| Single node | `[0]` | `1` | The root alone is a path of one node. |
| Only right children | `[1,null,2]` | `2` | Official example 2. |
| Left-skewed chain | `[1,2,null,3]` | `3` | `1 → 2 → 3`. |
| Perfect tree | `[1,2,3,4,5,6,7]` | `3` | All leaves at depth 3. |
| Negative values | `[-100,-100]` | `2` | Values don't matter, only shape. |
| Chain of `10^4` nodes | `[1,null,1,null,1,…]` | `10000` | Iterative versions are safe; the recursive one needs a raised recursion limit outside LeetCode. |

---

## 12. Common Mistakes and Debugging

1. **Returning 1 for an empty tree.** The base case must be `None → 0`; otherwise every answer is off by one.
2. **Counting edges instead of nodes.** This problem counts nodes (a single node has depth 1). Some textbooks define height in edges — read the definition.
3. **Using `min` by mistake / mixing up Minimum Depth.** For minimum depth (LeetCode 111) a node with only one child must **not** use the missing side's 0 — that is a different problem.
4. **BFS without freezing the level size.** Writing `while queue:` with `depth += 1` per popped node counts nodes, not levels. Use `for _ in range(len(queue))`.
5. **Using `list.pop(0)` as a queue.** Works, but each pop is `O(n)`; use `collections.deque`.
6. **Forgetting `self.` in the recursive call.** Inside the class, call `self.maxDepth(...)`.

**Debugging tip:** add a `depth` parameter to a helper and print `"  " * depth + str(node.val)` on entry — you'll see the tree's shape and the call order.

---

## 13. Practice Questions

**Q1. What does `maxDepth` return for `root = [1,2,3,4,null,null,5,null,6]`?**

<details><summary>Hint</summary>Draw the tree first: fill children pairs for each real node in order.</summary></details>

**Answer:** `4`. The tree is:

```text
          1
        /   \
       2     3
      /       \
     4         5
      \
       6
```

`2`'s children are `4, null`; `3`'s children are `null, 5`; `4`'s children are `null, 6`. The longest path `1 → 2 → 4 → 6` has 4 nodes.

**Q2. Minimum Depth (LeetCode 111): return the number of nodes on the shortest root-to-**leaf** path.**

<details><summary>Hint</summary>BFS finds the first leaf level directly. In recursion, a node with one child must not take the missing side's 0.</summary></details>

**Answer:** BFS stops at the first leaf it meets.

```python
from collections import deque


def min_depth(root):
    if root is None:
        return 0
    queue = deque([(root, 1)])
    while queue:
        node, depth = queue.popleft()
        if node.left is None and node.right is None:
            return depth            # first leaf found is the shallowest
        if node.left:
            queue.append((node.left, depth + 1))
        if node.right:
            queue.append((node.right, depth + 1))


tree = TreeNode(3, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))
assert min_depth(tree) == 2
chain = TreeNode(2, None, TreeNode(3, None, TreeNode(4)))
assert min_depth(chain) == 3        # the root is not a leaf, so the answer is not 1
assert min_depth(None) == 0
```

**Q3. Balanced Binary Tree (LeetCode 110): is every node's left and right height within 1 of each other?**

<details><summary>Hint</summary>Return the height as in maxDepth, but return -1 as a "not balanced" signal and pass it upward.</summary></details>

**Answer:** One post-order pass, `O(n)`.

```python
def is_balanced(root):
    def height(node):
        if node is None:
            return 0
        left = height(node.left)
        right = height(node.right)
        if left == -1 or right == -1 or abs(left - right) > 1:
            return -1
        return 1 + max(left, right)
    return height(root) != -1


assert is_balanced(TreeNode(3, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))) is True
assert is_balanced(TreeNode(1, TreeNode(2, TreeNode(3, TreeNode(4))), TreeNode(2))) is False
assert is_balanced(None) is True
```

**Q4. Diameter of Binary Tree (LeetCode 543): the number of edges on the longest path between any two nodes.**

<details><summary>Hint</summary>At each node, a path can bend: left height + right height. Track the best bend while returning heights.</summary></details>

**Answer:** This is the same "return one thing, record another" trick used in [044_binary_tree_maximum_path_sum.md](044_binary_tree_maximum_path_sum.md).

```python
def diameter(root):
    best = 0

    def height(node):
        nonlocal best
        if node is None:
            return 0
        left, right = height(node.left), height(node.right)
        best = max(best, left + right)   # edges on a path bending here
        return 1 + max(left, right)

    height(root)
    return best


assert diameter(TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5)), TreeNode(3))) == 3
assert diameter(TreeNode(1, TreeNode(2))) == 1
```

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** Post-order recursion on a tree (or BFS counting levels).
- **Key idea:** `depth(None) = 0`; `depth(node) = 1 + max(depth(left), depth(right))`.
- **Time:** `O(n)`.
- **Auxiliary space:** `O(h)` for DFS (`O(log n)` balanced, `O(n)` skewed); `O(w)` for BFS.
- **Recursion warning:** a skewed tree of `10^4` nodes exceeds Python's default limit of 1000; iterative versions are always safe.
- **One-line memory hook:** *"Ask both children how tall they are, take the taller, add yourself."*

### Completion checklist

- [x] Problem requirements verified
- [x] Examples and constraints verified
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force solution written and tested
- [x] Optimized Python solutions (recursive DFS, BFS, stack DFS) written and tested (`tools/tests/p041.py`)
- [x] Line-by-line explanation written
- [x] Dry run completed with a real example
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
