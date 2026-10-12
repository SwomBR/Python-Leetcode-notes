# 051. Lowest Common Ancestor of a Binary Search Tree

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Lowest Common Ancestor of a Binary Search Tree |
| **LeetCode number** | 235 |
| **Topic (source list)** | Tree |
| **Also uses** | Binary Search Tree, Depth-First Search |
| **Difficulty** | Medium |
| **LeetCode URL** | <https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/> |
| **Pattern** | Walk down a BST and stop at the "split point" |

---

## 2. Problem Explanation

### A quick tree primer

LeetCode gives you the tree as linked `TreeNode` objects. The class looks like this (it is already provided on LeetCode, so you never write it yourself):

```text
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None
```

A **binary search tree (BST)** is a binary tree with an ordering rule at **every** node:

- every value in the node's **left** subtree is **smaller** than the node's value;
- every value in the node's **right** subtree is **larger** than the node's value.

### What are we given?

- `root` — the root node of a BST.
- `p` and `q` — two **nodes** that are somewhere inside that tree. (In Python, LeetCode passes the actual `TreeNode` objects, not just their values: the signature is `lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode'`.)

### What must we return?

The **lowest common ancestor (LCA)** of `p` and `q`: the node that is an ancestor of both of them and sits **as deep (as low) in the tree as possible**.

An important detail: a node counts as its **own** ancestor (descendant). So if `p` is directly above `q` in the tree, the answer is `p` itself.

### Examples

The first two examples use this tree (`root = [6,2,8,0,4,7,9,null,null,3,5]` in level order):

```text
            6
          /   \
         2     8
        / \   / \
       0   4 7   9
          / \
         3   5
```

**Example 1**

```text
Input:  root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 8
Output: 6
```

`2` is in the left subtree of `6` and `8` is in the right subtree, so the deepest node above both is `6`.

**Example 2**

```text
Input:  root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 4
Output: 2
```

`4` lives under `2`, and `2` is allowed to be its own ancestor, so the answer is `2`.

**Example 3**

```text
Input:  root = [2,1], p = 2, q = 1
Output: 2
```

The tree is just `2` with a left child `1`. `2` is an ancestor of `1` and of itself.

### Constraints

- The number of nodes in the tree is in the range `[2, 10^5]`.
- `-10^9 <= Node.val <= 10^9`
- All `Node.val` are unique.
- `p != q`
- `p` and `q` will exist in the BST.

There is no official follow-up.

---

## 3. Everyday Analogy

> **Explain it like I'm five**

Imagine a big hiking trail that keeps splitting into two paths. At every fork there is a sign with a number: *"Smaller numbers go left, bigger numbers go right."*

Two friends live in cabins with numbers `p` and `q`. You start at the trailhead and want to find the **last fork you can walk to together** before you have to split up.

At each fork you ask: *"Do both friends need to go left? Do both need to go right?"*

- If both go left, walk left together.
- If both go right, walk right together.
- If one needs left and the other needs right — or one of the friends **lives right here** — this is the spot where you part ways. That fork is the answer.

You never have to explore side paths. You just follow the signs.

---

## 4. Step-by-Step Logic

1. **What does "lowest common ancestor" mean geometrically?** Start at the root and walk down. As long as `p` and `q` are in the **same** subtree, the current node is a common ancestor but not the lowest one, because its child on that side is also a common ancestor. The first node where they are **no longer on the same side** is the LCA.
2. **How can we tell which side a node is on without searching?** The BST rule! If `p.val < node.val`, then `p` is in the left subtree; if `p.val > node.val`, it's in the right subtree; if equal, `p` *is* this node.
3. **Three cases at the current node:**
   - Both values are **smaller** → both are on the left → move left.
   - Both values are **larger** → both are on the right → move right.
   - Otherwise (one smaller and one larger, **or** one of them equals the node) → this node is the split point → return it.
4. **Why is the split point correct?** If `p` and `q` are on different sides, any deeper node lives on only one side, so it cannot be an ancestor of both. If the node equals `p`, then `q` is below it (we only got here because `q` is on the same path), so the node is an ancestor of both and nothing deeper is an ancestor of `p`.
5. **We visit only one root-to-node path**, so the work is proportional to the tree's height `h`, not to the number of nodes.

---

## 5. Brute-Force Solution

### Algorithm

Ignore the BST ordering and treat the tree as an ordinary binary tree:

1. Find the path (list of nodes) from the root to `p` with a depth-first search.
2. Find the path from the root to `q` the same way.
3. Walk both paths together from the root; the last node they have in common is the LCA.

### Python code

```python
class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        def find_path(node, target, path):
            """Append the nodes from node down to target; return True if found."""
            if node is None:
                return False
            path.append(node)
            if node is target:
                return True
            if find_path(node.left, target, path) or find_path(node.right, target, path):
                return True
            path.pop()            # target is not under this node: undo the step
            return False

        path_p, path_q = [], []
        find_path(root, p, path_p)
        find_path(root, q, path_q)

        lca = root
        for a, b in zip(path_p, path_q):
            if a is not b:        # the paths split here
                break
            lca = a
        return lca
```

### Explanation

- `find_path` is a classic backtracking DFS: it adds a node to `path`, explores both children, and removes the node again if the target was not found below it.
- Both paths start at the root, so their first entries are equal. They stay equal until the point where `p` and `q` go different ways. The last shared node is the deepest common ancestor.
- `zip` stops at the shorter path, which handles the case where one node is an ancestor of the other (for example 2, `path_p = [6, 2]` and `path_q = [6, 2, 4]` → the answer is `2`).

### Complexity

- **Time:** `O(n)`. In the worst case each DFS visits every node once.
- **Auxiliary space:** `O(n)` in the worst case: two path lists of length up to `h`, plus a recursion stack of depth up to `h`, where `h` can be `n` for a skewed tree.
- **Trade-off:** it is correct for *any* binary tree, but it wastes the BST ordering. On a skewed tree of `10^5` nodes the recursion would also exceed Python's default recursion limit (about 1000), so this version is mainly a stepping stone. (The general-tree version of this problem is LeetCode 236; see Practice Question 2.)

---

## 6. Optimized Solution

### Idea

Use the BST ordering to decide, at each node, whether both targets are on the same side. Walk down until they are not.

### Algorithm

1. Set `node = root`.
2. While `node` exists:
   - If `p.val` and `q.val` are both smaller than `node.val`, move to `node.left`.
   - Else if both are larger, move to `node.right`.
   - Else return `node` (the split point).

### Python code (LeetCode-ready)

```python
class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        node = root
        while node:
            if p.val < node.val and q.val < node.val:
                node = node.left           # both targets are in the left subtree
            elif p.val > node.val and q.val > node.val:
                node = node.right          # both targets are in the right subtree
            else:
                return node                # they split here (or one of them is here)
        return None  # unreachable: p and q are guaranteed to be in the tree
```

### Alternative: the same idea written recursively

```python
class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        if p.val < root.val and q.val < root.val:
            return self.lowestCommonAncestor(root.left, p, q)
        if p.val > root.val and q.val > root.val:
            return self.lowestCommonAncestor(root.right, p, q)
        return root
```

The recursive version is shorter, but every step adds a stack frame: `O(h)` auxiliary space, and a skewed tree with tens of thousands of nodes can hit Python's recursion limit. The iterative loop uses `O(1)` space and is the safer choice.

---

## 7. Line-by-Line Explanation

(Iterative optimized solution)

| Line | What it does | Why |
|---|---|---|
| `node = root` | Starts the walk at the root. | The root is an ancestor of every node, so it is always a common ancestor; we look for a lower one. |
| `while node:` | Keeps walking while there is a node. | With valid input we always return inside the loop; the condition simply protects against walking off the tree. |
| `if p.val < node.val and q.val < node.val:` | Both targets are smaller than the current value. | By the BST rule, both live in the left subtree, so the left child is a lower common ancestor. |
| `node = node.left` | Moves one level down to the left. | Narrows the search. |
| `elif p.val > node.val and q.val > node.val:` | Both targets are larger. | Both live in the right subtree. |
| `node = node.right` | Moves one level down to the right. | Narrows the search. |
| `else: return node` | Targets are on different sides, or one of them equals `node`. | No deeper node can be an ancestor of both, so this is the lowest common ancestor. |
| `return None` | Fallback after the loop. | Never reached for valid LeetCode input. |

**Why compare values instead of nodes?** The BST rule is about values. Because all values are unique, `p.val == node.val` means `node` *is* `p`.

---

## 8. Dry Run

**Input (Example 2):** `root = [6,2,8,0,4,7,9,null,null,3,5]`, `p = 2`, `q = 4`

| Step | `node.val` | `p.val` vs node | `q.val` vs node | Case | Action |
|---|---|---|---|---|---|
| 1 | 6 | 2 < 6 | 4 < 6 | both smaller | `node = node.left` (2) |
| 2 | 2 | 2 == 2 | 4 > 2 | not "both smaller", not "both larger" | **return node 2** |

**Result:** `2` ✅

**Example 1:** `p = 2`, `q = 8`

| Step | `node.val` | `p.val` vs node | `q.val` vs node | Case | Action |
|---|---|---|---|---|---|
| 1 | 6 | 2 < 6 | 8 > 6 | split | **return node 6** |

**Result:** `6` ✅

**A deeper example:** same tree, `p = 3`, `q = 5`

| Step | `node.val` | `p.val` vs node | `q.val` vs node | Action |
|---|---|---|---|---|
| 1 | 6 | 3 < 6 | 5 < 6 | go left to 2 |
| 2 | 2 | 3 > 2 | 5 > 2 | go right to 4 |
| 3 | 4 | 3 < 4 | 5 > 4 | split → **return 4** |

**Result:** `4` ✅

**Example 3:** `root = [2,1]`, `p = 2`, `q = 1` → at node `2`, `p.val == 2` so it is neither "both smaller" nor "both larger" → return `2` ✅.

---

## 9. Concepts, Data Structures, and Patterns

- **Binary tree / `TreeNode`:** each node has a value and up to two children. Related warm-ups: [041_maximum_depth_of_binary_tree.md](041_maximum_depth_of_binary_tree.md), [042_same_tree.md](042_same_tree.md).
- **Binary search tree property:** smaller values on the left, larger on the right — at every node. This lets you discard half of the remaining tree at each step, like binary search on an array (compare [008_search_in_rotated_sorted_array.md](../01_array/008_search_in_rotated_sorted_array.md)). Other notes that rely on the BST property: [049_validate_binary_search_tree.md](049_validate_binary_search_tree.md) and [050_kth_smallest_element_in_a_bst.md](050_kth_smallest_element_in_a_bst.md).
- **Lowest common ancestor:** the deepest node that has both targets in its subtree (a node is in its own subtree).
- **"Split point" pattern:** walk down while both targets agree on a direction; stop where they disagree.
- **Path-comparison / backtracking DFS:** the brute force records root-to-node paths and pops nodes on the way back up — the same backtracking shape you see in [030_word_search.md](../05_matrix/030_word_search.md).
- **Iteration vs recursion:** a tail-recursive walk can always be turned into a `while` loop, removing the `O(h)` call stack.
- **Related problems:** Lowest Common Ancestor of a Binary Tree (LeetCode 236) — no ordering, so you need the general DFS; Practice Question 2 solves it.

---

## 10. Complexity Analysis

Let `n` be the number of nodes and `h` the height of the tree (`h ≈ log₂ n` when balanced, `h = n - 1` when skewed like a linked list).

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Brute force (paths in a general tree) | `O(n)` | `O(n)` (more precisely `O(h)`) | Two DFS passes may each visit every node; the two path lists and the recursion stack each hold at most `h + 1` nodes. |
| Iterative BST walk (optimized) | `O(h)` | `O(1)` | One step down per loop iteration, at most `h + 1` nodes visited; only the `node` variable is stored. |
| Recursive BST walk | `O(h)` | `O(h)` | Same visits, but each step adds a call-stack frame. |

In the worst case (skewed tree) `h = O(n)`, so the optimized walk is `O(n)` time — but it never explores side branches, and for a balanced tree it is only `O(log n)`.

---

## 11. Edge Cases

All rows use the Example 1 tree unless stated otherwise.

| Case | Example | Expected result | Why |
|---|---|---|---|
| Targets on different sides of the root | `p = 2`, `q = 8` | `6` | The root is the split point. |
| One target is the ancestor of the other | `p = 2`, `q = 4` | `2` | A node is its own descendant. |
| Two-node tree | `root = [2,1]`, `p = 2`, `q = 1` | `2` | The root is `p` itself. |
| Both targets deep in the same subtree | `p = 3`, `q = 5` | `4` | Walk 6 → 2 → 4, then split. |
| `p` and `q` given in "reverse" order | `p = 8`, `q = 2` | `6` | The checks are symmetric in `p` and `q`. |
| Siblings that are leaves | `p = 7`, `q = 9` | `8` | Their parent is the split point. |
| Negative / extreme values | BST built from `0, -10^9, 10^9, -5, 5`; `p = -5`, `q = 5` | node `0` | Comparisons work with any integers; Python has no overflow. |
| Skewed tree (a chain `0 → 1 → … → 299` going right) | `p = 150`, `q = 299` | `150` | `150` is an ancestor of `299`; the iterative loop handles long chains without recursion limits. |

---

## 12. Common Mistakes and Debugging

1. **Returning a value instead of a node.** LeetCode expects the `TreeNode` object. Return `node`, not `node.val`.
2. **Using `<=` / `>=` in the "move" conditions.** If you write `p.val <= node.val and q.val <= node.val`, then when `node` *is* `p` you move past it and lose the answer. Use strict `<` and `>`.
3. **Checking only one target.** `if p.val < node.val: go left` ignores where `q` is. Both targets must agree before you move.
4. **Assuming `p.val < q.val`.** The input can give them in either order. The "both smaller / both larger" checks are symmetric, so no swap is needed.
5. **Forgetting the BST property and doing a full DFS.** It works (it's the brute force) but costs `O(n)` and a deep recursion stack.
6. **Deep recursion on skewed trees.** With up to `10^5` nodes, a recursive solution can raise `RecursionError` in Python. Prefer the iterative loop.

**Debugging tip:** print `node.val, p.val, q.val` at the top of the loop and compare with the dry-run tables above.

---

## 13. Practice Questions

The runnable answers below build small trees with `TreeNode(val, left, right)` — the three-argument helper used throughout this project — rather than LeetCode's one-argument `TreeNode(x)`.

**Q1. Using the Example 1 tree, what does the optimized solution return for `p = 0`, `q = 5`, and which nodes does it visit?**

<details><summary>Hint</summary>Compare both values with 6, then with 2.</summary></details>

**Answer:** At `6`, both `0` and `5` are smaller → go left. At `2`, `0 < 2` but `5 > 2` → split. It visits `6` and `2` and returns node `2`.

**Q2. Solve LCA for a general binary tree (no ordering), LeetCode 236.**

<details><summary>Hint</summary>Recurse into both children. If both sides report finding something, the current node is the split point. If only one side does, pass that result up.</summary></details>

**Answer:** A post-order DFS. Each call returns `p`, `q`, the LCA, or `None` for its subtree.

```python
def lca_binary_tree(root, p, q):
    if root is None or root is p or root is q:
        return root
    left = lca_binary_tree(root.left, p, q)
    right = lca_binary_tree(root.right, p, q)
    if left and right:      # p and q were found on different sides
        return root
    return left or right


# Not a BST on purpose:      3
#                           / \
#                          5   1
#                         / \
#                        6   2
n6, n2 = TreeNode(6), TreeNode(2)
n5 = TreeNode(5, n6, n2)
n1 = TreeNode(1)
tree = TreeNode(3, n5, n1)
assert lca_binary_tree(tree, n6, n2) is n5
assert lca_binary_tree(tree, n6, n1) is tree
assert lca_binary_tree(tree, n5, n2) is n5
```

Time `O(n)`, auxiliary space `O(h)` for the recursion.

**Q3. In a BST, return the number of edges on the path between two nodes with values `a` and `b`.**

<details><summary>Hint</summary>Find the LCA first. Then the distance is depth(a from LCA) + depth(b from LCA).</summary></details>

**Answer:**

```python
def bst_distance(root, a, b):
    node = root
    while True:                                  # find the split point (LCA)
        if a < node.val and b < node.val:
            node = node.left
        elif a > node.val and b > node.val:
            node = node.right
        else:
            break

    def depth_from(start, value):
        steps = 0
        while start.val != value:
            start = start.left if value < start.val else start.right
            steps += 1
        return steps

    return depth_from(node, a) + depth_from(node, b)


#            6
#          /   \
#         2     8
#        / \   / \
#       0   4 7   9
#          / \
#         3   5
t = TreeNode(6,
             TreeNode(2, TreeNode(0), TreeNode(4, TreeNode(3), TreeNode(5))),
             TreeNode(8, TreeNode(7), TreeNode(9)))
assert bst_distance(t, 3, 9) == 5     # 3-4-2-6-8-9
assert bst_distance(t, 2, 4) == 1
assert bst_distance(t, 7, 9) == 2
```

Time `O(h)`, auxiliary space `O(1)`.

**Q4. What changes if `p` or `q` might *not* be in the tree?**

<details><summary>Hint</summary>The split-point walk never checks that the targets really exist.</summary></details>

**Answer:** The walk would still return some node (the split point of the two *values*), which would be wrong. You would first search the BST for each value (`O(h)` each) and return `None` if either is missing. LeetCode 235 guarantees both exist, so the check is unnecessary there.

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** Walk down the BST to the split point.
- **Key idea:** Both smaller → go left; both larger → go right; otherwise the current node is the LCA.
- **Time:** `O(h)` (`O(log n)` balanced, `O(n)` skewed).
- **Auxiliary space:** `O(1)` iterative (`O(h)` recursive).
- **One-line memory hook:** *"Walk together until the signs send you different ways."*

### Completion checklist

- [x] Problem requirements verified
- [x] Examples and constraints verified
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force solution written and tested
- [x] Optimized Python solution written and tested (`tools/tests/p051.py`), including the recursive alternative
- [x] Line-by-line explanation written
- [x] Dry run completed with real examples
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
