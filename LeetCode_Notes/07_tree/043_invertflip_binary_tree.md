# 043. Invert/Flip Binary Tree

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Invert Binary Tree (listed in the source as "Invert/Flip Binary Tree") |
| **LeetCode number** | 226 |
| **Topic (source list)** | Tree |
| **Also uses** | Depth-First Search, Breadth-First Search, Recursion |
| **Difficulty** | Easy |
| **LeetCode URL** | <https://leetcode.com/problems/invert-binary-tree/> |
| **Pattern** | Visit every node once and swap its two children |

---

## 2. Problem Explanation

### Beginner primer: what is a `TreeNode`?

A **binary tree** is built from **nodes**. Each node has a value `val` and two child pointers, `left` and `right`; a missing child is `None`. LeetCode already defines the class and shows it as a comment:

```text
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
```

### How LeetCode's list input becomes a tree

LeetCode writes trees as **level-order lists**: the root first, then each row from left to right, with `null` for a missing child. Every real node takes the next two list items as its left and right children. `[4,2,7,1,3,6,9]` is a full tree of three rows:

```text
          4
        /   \
       2     7
      / \   / \
     1   3 6   9
```

The **output** is written the same way, so the answer `[4,7,2,9,6,3,1]` describes the tree your function returns.

### What are we given?

`root` — the root of a binary tree (possibly `None`).

### What must we return?

The root of the **inverted** tree. Inverting means producing the **mirror image**: at **every** node, the left child and the right child trade places. Imagine holding the tree up to a mirror — what was on the left side appears on the right, at every level.

You may change the tree in place and return the same root (the usual solution), or build a new mirrored tree — LeetCode checks the tree you return.

### Examples

**Example 1**

```text
Input:  root = [4,2,7,1,3,6,9]
Output: [4,7,2,9,6,3,1]
```

```text
     before                 after
       4                      4
     /   \                  /   \
    2     7      ==>       7     2
   / \   / \              / \   / \
  1   3 6   9            9   6 3   1
```

Each row reads in reverse order.

**Example 2**

```text
Input:  root = [2,1,3]
Output: [2,3,1]
```

```text
    2            2
   / \   ==>    / \
  1   3        3   1
```

**Example 3**

```text
Input:  root = []
Output: []
```

An empty tree stays empty: return `None`.

### Constraints

- The number of nodes in the tree is in the range `[0, 100]`.
- `-100 <= Node.val <= 100`

There is no follow-up for this problem.

---

## 3. Everyday Analogy

> **Explain it like I'm five**

Picture a mobile hanging over a baby's crib: a stick with toys hanging from the left and right ends, and some toys have their own little sticks with more toys.

To make its mirror image, you go to the top stick and **swap what hangs on its left and right ends**. Then you go to each smaller stick below and do the same swap. When every stick has been swapped once, the whole mobile looks like its reflection in a mirror.

Important: swapping only the top stick isn't enough — the smaller sticks would still be in their old order. **Every** stick must be swapped.

---

## 4. Step-by-Step Logic

1. **What does "mirror" mean node by node?** The mirror of a tree with root `r`, left subtree `L`, right subtree `R` is: root `r`, left = mirror of `R`, right = mirror of `L`.
2. **That is a recursive definition.** Mirror the two subtrees and put them on opposite sides.
3. **Equivalent simpler view:** swap the children of every node, in any order. Each node's swap is independent of the others, because a swap only touches that node's two pointers and moves whole subtrees intact.
4. **Base case:** an empty tree (`None`) is its own mirror.
5. **Traversal choice:** any traversal that visits each node once works — preorder recursion, BFS with a queue, or DFS with a stack.
6. **Return the root.** The root node itself never moves; only pointers below it change.

---

## 5. Brute-Force Solution

### Algorithm

The most direct reading of "mirror image" is to **build a brand-new tree**: for each node, create a new node with the same value whose left child is the mirrored copy of the old right subtree and whose right child is the mirrored copy of the old left subtree.

### Python code

```python
from typing import Optional


class Solution:
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        def mirror_copy(node: Optional[TreeNode]) -> Optional[TreeNode]:
            if node is None:
                return None
            return TreeNode(node.val,
                            mirror_copy(node.right),   # old right becomes new left
                            mirror_copy(node.left))    # old left becomes new right

        return mirror_copy(root)
```

### Explanation

- Every call creates exactly one new node and recurses into both children, with the sides crossed.
- The original tree is **not** modified, which can be a benefit if someone else still needs it.
- `TreeNode` is provided by LeetCode, so creating new nodes is allowed.

### Complexity

- **Time:** `O(n)` — one new node per old node. Asymptotically the same as the optimized version, but every node is allocated again, which is slower in practice.
- **Auxiliary space:** `O(n)` for the `n` new nodes, plus `O(h)` recursion stack. This is the real cost: it doubles memory, while the in-place version needs only the stack.

For this problem the "simple" approach is not asymptotically slower — the improvement is from `O(n)` extra memory to `O(h)` and no allocations.

---

## 6. Optimized Solution

### Idea

Don't copy anything. Walk the existing tree and **swap `left` and `right` at every node, in place**.

### Algorithm (recursive DFS, preorder)

1. If `root` is `None`, return `None`.
2. Swap `root.left` and `root.right`.
3. Invert the (new) left subtree and the (new) right subtree.
4. Return `root`.

### Python code (LeetCode-ready, recursive DFS)

```python
from typing import Optional


class Solution:
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        if root is None:
            return None
        root.left, root.right = root.right, root.left   # swap the two children
        self.invertTree(root.left)                      # then mirror each subtree
        self.invertTree(root.right)
        return root
```

A common one-line variant is `root.left, root.right = self.invertTree(root.right), self.invertTree(root.left)` — it is correct because Python evaluates the whole right-hand side before assigning.

### Python code (iterative BFS)

```python
from collections import deque
from typing import Optional


class Solution:
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        if root is None:
            return None
        queue = deque([root])
        while queue:
            node = queue.popleft()
            node.left, node.right = node.right, node.left
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        return root
```

### Python code (iterative DFS with a stack)

```python
from typing import Optional


class Solution:
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        stack = [root]
        while stack:
            node = stack.pop()
            if node is None:
                continue
            node.left, node.right = node.right, node.left
            stack.append(node.left)
            stack.append(node.right)
        return root
```

### Recursion limit — is the recursive version safe?

The tree has at most 100 nodes, so its height is at most 100 and the recursion is at most about 101 calls deep. Python's default recursion limit is 1000, so the recursive versions (including the brute force) are **safe for every input allowed by the constraints**. The iterative versions would matter only for much larger trees than this problem allows.

---

## 7. Line-by-Line Explanation

(Recursive DFS)

| Line | What it does | Why |
|---|---|---|
| `if root is None: return None` | Base case. | An empty subtree is its own mirror; also handles Example 3. |
| `root.left, root.right = root.right, root.left` | Swaps the two child pointers with tuple assignment. | Python builds the tuple `(root.right, root.left)` first, then assigns, so no temporary variable is needed. |
| `self.invertTree(root.left)` | Mirrors the subtree now on the left (the old right subtree). | Swapping only this node is not enough; every node must swap. |
| `self.invertTree(root.right)` | Mirrors the subtree now on the right. | Same reason. The return value is ignored because the change happens in place. |
| `return root` | Returns the same root object. | The root never moves; LeetCode reads the tree from it. |

(Iterative BFS)

| Line | What it does | Why |
|---|---|---|
| `queue = deque([root])` | Starts with the root. | Nodes waiting to have their children swapped. |
| `node.left, node.right = node.right, node.left` | Swaps this node's children. | Each node is swapped exactly once. |
| `if node.left: queue.append(...)` | Schedules real children. | They need their own swap later. Order doesn't matter for correctness. |

---

## 8. Dry Run

**Input (Example 1):** `root = [4,2,7,1,3,6,9]` (recursive DFS)

```text
          4
        /   \
       2     7
      / \   / \
     1   3 6   9
```

| Step | Call | Children before swap (left, right) | Children after swap | Next action |
|---|---|---|---|---|
| 1 | `invertTree(4)` | (2, 7) | (7, 2) | recurse into new left = 7 |
| 2 | `invertTree(7)` | (6, 9) | (9, 6) | recurse into 9 |
| 3 | `invertTree(9)` | (None, None) | (None, None) | both children `None` → return 9 |
| 4 | `invertTree(6)` | (None, None) | (None, None) | return 6; back to 7 → return 7 |
| 5 | back in `invertTree(4)` | | | recurse into new right = 2 |
| 6 | `invertTree(2)` | (1, 3) | (3, 1) | recurse into 3 |
| 7 | `invertTree(3)` | (None, None) | (None, None) | return 3 |
| 8 | `invertTree(1)` | (None, None) | (None, None) | return 1; back to 2 → return 2 |
| 9 | finish `invertTree(4)` | | | return 4 |

Final tree:

```text
          4
        /   \
       7     2
      / \   / \
     9   6 3   1
```

Level-order: `[4,7,2,9,6,3,1]` ✅

**Second dry run (BFS), Example 2:** `root = [2,1,3]`

| Pop | Node | Swap | Queue after |
|---|---|---|---|
| 1 | 2 | (1, 3) → (3, 1) | `[3, 1]` |
| 2 | 3 | leaf, nothing changes | `[1]` |
| 3 | 1 | leaf | `[]` |

Result `[2,3,1]` ✅. **Example 3:** `root = None` → return `None`, printed as `[]` ✅.

---

## 9. Concepts, Data Structures, and Patterns

- **Tree recursion / preorder traversal:** do the work at the node (swap) and then visit the children.
- **In-place modification:** change pointers instead of building new structures — saves memory.
- **Tuple assignment swap:** `a, b = b, a` evaluates the right side first; it's Python's idiomatic swap.
- **BFS (queue) and DFS (stack):** any full traversal works because each node's swap is independent.
- **Mirror symmetry:** inverting twice returns the original tree; a tree is symmetric exactly when it equals its own inversion (see Q3).
- **Related notes in this project:**
  - [042_same_tree.md](042_same_tree.md) — pairs of nodes; Symmetric Tree is "same tree with left paired against right".
  - [041_maximum_depth_of_binary_tree.md](041_maximum_depth_of_binary_tree.md) and [045_binary_tree_level_order_traversal.md](045_binary_tree_level_order_traversal.md) — the same DFS/BFS skeletons.
  - [049_validate_binary_search_tree.md](049_validate_binary_search_tree.md) — inverting a BST reverses its in-order sequence (Q2).

---

## 10. Complexity Analysis

Let `n` = number of nodes, `h` = height.

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Mirrored copy (brute force) | `O(n)` | `O(n)` new nodes + `O(h)` stack | One new node per old node. |
| Recursive in-place swap | `O(n)` | `O(h)` — best `O(log n)` (balanced), worst `O(n)` (skewed chain) | Each node is visited and swapped once; the call stack follows one root-to-node path. |
| Iterative BFS | `O(n)` | `O(w)`, `w` = widest level (up to about `n/2` for a complete tree) | The queue holds at most about one level. |
| Iterative DFS (stack) | `O(n)` | `O(h)` | Each level of the current path leaves at most one pending sibling; `None` children are pushed but popped immediately. |

Every approach must touch all `n` nodes (each one must swap), so `O(n)` time is optimal.

---

## 11. Edge Cases

| Case | Example | Expected result | Why |
|---|---|---|---|
| Empty tree | `[]` | `[]` | Return `None`. |
| Single node | `[1]` | `[1]` | Swapping two `None`s changes nothing. |
| Only a left child | `[1,2]` | `[1,null,2]` | `2` moves to the right. |
| Right chain | `[1,null,2,null,3]` | `[1,2,null,3]` | Becomes a left chain. |
| Perfect tree | `[4,2,7,1,3,6,9]` | `[4,7,2,9,6,3,1]` | Official example 1. |
| Symmetric tree | `[1,2,2,3,4,4,3]` | `[1,2,2,3,4,4,3]` | A symmetric tree is its own mirror. |
| Inverting twice | any tree | the original tree | Mirror of a mirror. |

---

## 12. Common Mistakes and Debugging

1. **Sequential assignment instead of a simultaneous swap.**
   ```text
   root.left = self.invertTree(root.right)
   root.right = self.invertTree(root.left)   # BUG: root.left was already replaced
   ```
   The second line inverts the *new* left subtree (the old right one) again, so the old left subtree is lost. Use tuple assignment or a temporary variable.
2. **Swapping only the root.** Gives `[4,7,2,6,9,1,3]` for Example 1 — the lower levels are not mirrored. Every node must swap.
3. **Swapping values instead of subtrees.** Swapping `root.left.val` and `root.right.val` fails when the two subtrees have different shapes (or one is `None`).
4. **Forgetting to return `root`.** The function would return `None` and LeetCode would see an empty tree.
5. **Swapping twice at the same node.** Swapping before recursing (pre-order) or after recursing (post-order) both work — but doing both at one node undoes the swap and leaves that node un-mirrored.

**Debugging tip:** write a small helper that converts the tree back to a level-order list (like the one in `tools/tests/p043.py`) and print it after inverting.

---

## 13. Practice Questions

**Q1. What is the inverted tree of `root = [1,2,null,3]`, in LeetCode list form?**

<details><summary>Hint</summary>Draw it: 2 is the left child of 1, and 3 is the left child of 2.</summary></details>

**Answer:** `[1,null,2,null,3]`. The left chain `1 → 2 → 3` becomes a right chain.

```text
      1            1
     /              \
    2      ==>       2
   /                  \
  3                    3
```

**Q2. If you invert a binary search tree, what happens to its in-order traversal?**

<details><summary>Hint</summary>In-order visits left, node, right. After inversion, "left" holds what used to be on the right.</summary></details>

**Answer:** It comes out **reversed** (descending instead of ascending), because in-order of the mirror visits old-right, node, old-left.

```python
def invert(node):
    if node is not None:
        node.left, node.right = node.right, node.left
        invert(node.left)
        invert(node.right)
    return node


def inorder(node):
    return inorder(node.left) + [node.val] + inorder(node.right) if node else []


bst = TreeNode(4, TreeNode(2, TreeNode(1), TreeNode(3)), TreeNode(6, TreeNode(5), TreeNode(7)))
assert inorder(bst) == [1, 2, 3, 4, 5, 6, 7]
assert inorder(invert(bst)) == [7, 6, 5, 4, 3, 2, 1]
```

**Q3. Use inversion to test whether a tree is symmetric (LeetCode 101).**

<details><summary>Hint</summary>A tree is symmetric when it equals its own mirror. Don't destroy the original — compare against a mirrored copy.</summary></details>

**Answer:** Build a mirrored copy (the brute-force idea) and run a Same Tree check ([042_same_tree.md](042_same_tree.md)). `O(n)` time and `O(n)` extra space; the direct mirror comparison avoids the copy.

```python
def mirror_copy(node):
    if node is None:
        return None
    return TreeNode(node.val, mirror_copy(node.right), mirror_copy(node.left))


def same(a, b):
    if a is None or b is None:
        return a is b
    return a.val == b.val and same(a.left, b.left) and same(a.right, b.right)


def is_symmetric(root):
    return same(root, mirror_copy(root))


assert is_symmetric(TreeNode(1, TreeNode(2, TreeNode(3), TreeNode(4)), TreeNode(2, TreeNode(4), TreeNode(3)))) is True
assert is_symmetric(TreeNode(1, TreeNode(2, None, TreeNode(3)), TreeNode(2, None, TreeNode(3)))) is False
assert is_symmetric(None) is True
```

**Q4. Write the inversion as a function that also returns the level-order list, and check Example 1.**

<details><summary>Hint</summary>Invert with a stack, then BFS with a deque, writing `None` for missing children and trimming trailing `None`s.</summary></details>

**Answer:**

```python
from collections import deque


def invert_iterative(root):
    stack = [root]
    while stack:
        node = stack.pop()
        if node:
            node.left, node.right = node.right, node.left
            stack.extend((node.left, node.right))
    return root


def to_level_list(root):
    out, queue = [], deque([root])
    while queue:
        node = queue.popleft()
        if node is None:
            out.append(None)
            continue
        out.append(node.val)
        queue.extend((node.left, node.right))
    while out and out[-1] is None:
        out.pop()
    return out


ex1 = TreeNode(4, TreeNode(2, TreeNode(1), TreeNode(3)), TreeNode(7, TreeNode(6), TreeNode(9)))
assert to_level_list(invert_iterative(ex1)) == [4, 7, 2, 9, 6, 3, 1]
assert to_level_list(invert_iterative(None)) == []
```

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** Visit every node once (DFS or BFS) and swap its children.
- **Key idea:** `root.left, root.right = root.right, root.left`, then recurse into both children; return `root`.
- **Time:** `O(n)`.
- **Auxiliary space:** `O(h)` for DFS (`O(log n)` balanced, `O(n)` skewed), `O(w)` for BFS. At most 100 nodes, so recursion is safe.
- **One-line memory hook:** *"Swap every stick on the mobile, not just the top one."*

### Completion checklist

- [x] Problem requirements verified
- [x] Examples and constraints verified
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force solution (mirrored copy) written and tested
- [x] Optimized Python solutions (recursive, BFS, stack) written and tested (`tools/tests/p043.py`)
- [x] Line-by-line explanation written
- [x] Dry run completed with a real example
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
