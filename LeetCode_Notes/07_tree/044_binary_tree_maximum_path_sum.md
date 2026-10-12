# 044. Binary Tree Maximum Path Sum

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Binary Tree Maximum Path Sum |
| **LeetCode number** | 124 |
| **Topic (source list)** | Tree |
| **Also uses** | Depth-First Search, Dynamic Programming (on trees), Recursion |
| **Difficulty** | Hard |
| **LeetCode URL** | <https://leetcode.com/problems/binary-tree-maximum-path-sum/> |
| **Pattern** | Post-order DFS that **returns** one thing (best one-sided "arm") and **records** another (best bent path) |

---

## 2. Problem Explanation

### Beginner primer: what is a `TreeNode`?

A **binary tree** is made of **nodes**; each node has a value `val`, a `left` child and a `right` child (`None` when missing). LeetCode already defines the class and shows it as a comment:

```text
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
```

### How LeetCode's list input becomes a tree

The input is a **level-order list**: root first, then each row from left to right, `null` for a missing child; every real node takes the next two items as its left and right child. `[-10,9,20,null,null,15,7]` is:

```text
        -10
        /  \
       9    20
           /  \
          15   7
```

(`9` takes the two `null`s; `20` takes `15` and `7`.)

### What are we given?

`root` — the root of a binary tree with **at least one node**. Values may be negative.

### What must we return?

The largest **path sum** of any **path** in the tree.

- A **path** is a chain of nodes where each neighbouring pair is joined by a tree edge (parent–child). You may travel up and down along edges, but **no node may be used twice**, so a path can never branch.
- The path must contain **at least one node**.
- The path does **not** have to include the root, and does not have to end at a leaf.
- The **path sum** is the total of the values of its nodes.

Because a path can't branch, its shape is always: go **up** from some node to a single highest point (the "top" or "bend"), then go **down** the other side. Either side may be empty.

```text
            top
           /   \
        ...     ...      <- at most one arm into the left subtree,
        /         \         at most one arm into the right subtree
```

### Examples

**Example 1**

```text
Input:  root = [1,2,3]
Output: 6
```

```text
      1
     / \
    2   3
```

The best path is `2 → 1 → 3`, with sum `2 + 1 + 3 = 6`.

**Example 2**

```text
Input:  root = [-10,9,20,null,null,15,7]
Output: 42
```

The best path is `15 → 20 → 7`, with sum `15 + 20 + 7 = 42`. It does not pass through the root: adding `-10` and `9` would give `41`, which is worse.

### Constraints

- The number of nodes in the tree is in the range `[1, 3 * 10^4]`.
- `-1000 <= Node.val <= 1000`

There is no follow-up for this problem.

---

## 3. Everyday Analogy

> **Explain it like I'm five**

Imagine a tree of rooms connected by doors. Each room has some coins on the floor — but some rooms have a "debt" sign instead (negative coins). You want to walk **one hallway route** without visiting a room twice and collect the most coins.

Every room manager answers two questions:

1. **To my boss (the parent room):** *"If a route comes down into my room from above, what's the best I can add?"* The route enters from above, so the manager may continue into **only one** of their child rooms — whichever is richer — or stop right here if both children are in debt.
2. **To the notebook on the wall:** *"What's the best route that has **my room as its highest point**?"* That route may use **both** child sides, because it doesn't continue upward.

The best number ever written in the notebook is the answer.

---

## 4. Step-by-Step Logic

1. **Every path has exactly one highest node** (closest to the root). Call it the **top**. So: answer = max over all nodes of "best path whose top is this node".
2. **Best path with top `x`** = `x.val` + (best downward arm into the left subtree, or 0 if it hurts) + (best downward arm into the right subtree, or 0 if it hurts).
3. **Downward arm ("gain")**: `gain(x)` = best sum of a path that **starts at `x` and only goes down**. It can continue into at most **one** child: `gain(x) = x.val + max(0, gain(x.left), gain(x.right))`.
4. **Why clip at 0?** A negative arm only lowers the total, so we simply don't take it.
5. **Why only one side in `gain`?** The parent will attach this arm to itself. A path that came up from the left child, went through `x`, and continued into `x`'s right child **and** up to the parent would branch — not allowed.
6. **Do it in one pass.** Compute `gain` bottom-up (post-order): when we have `left` and `right` gains of a node, we can both record `node.val + left + right` and return `node.val + max(left, right)`.
7. **Initialise the best answer to a node value, not 0.** If every value is negative, the answer is the largest single node (path must be non-empty).

---

## 5. Brute-Force Solution

### Algorithm

Use step 1 and 2 directly: for **every** node `x` treated as the top, compute the best downward arms into its left and right subtrees with a **fresh** DFS each time, and keep the maximum of `x.val + max(0, armL) + max(0, armR)`.

### Python code

```python
from typing import Optional


class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        def best_down(node: Optional[TreeNode]) -> int:
            # Best sum of a path that starts at `node` and only goes down.
            # Recomputed from scratch on every call (no memory) - this is the slow part.
            if node is None:
                return 0
            return node.val + max(0, best_down(node.left), best_down(node.right))

        best = root.val
        stack = [root]                      # visit every node as a possible "top"
        while stack:
            node = stack.pop()
            left_arm = max(0, best_down(node.left))
            right_arm = max(0, best_down(node.right))
            best = max(best, node.val + left_arm + right_arm)
            if node.left:
                stack.append(node.left)
            if node.right:
                stack.append(node.right)
        return best
```

### Explanation

- The outer loop treats each node as the top of the path. Every path has exactly one top, so every path is considered.
- `best_down(None)` is 0, meaning "no arm"; `max(0, …)` drops arms that would lower the sum.
- It is correct, but `best_down` re-walks entire subtrees for every node above them.

### Complexity

- **Time:** `O(n · h)`. Computing the arms of node `x` walks its whole subtree, so each node is re-walked once for every ancestor it has — that's `depth` times. Total = sum of depths = `O(n · h)`: about `O(n log n)` for a balanced tree but `O(n²)` for a skewed chain — roughly `4.5 · 10^8` steps for `3 · 10^4` nodes, far too slow.
- **Auxiliary space:** `O(h)` for the `best_down` recursion plus the stack.

---

## 6. Optimized Solution

### Idea

Compute each node's `gain` **once**, bottom-up. While a node knows both children's gains, record the best path bending at it, and return its one-sided gain to the parent.

### Algorithm (recursive post-order DFS)

1. `best = root.val`.
2. Define `gain(node)`:
   - `None` → 0.
   - `left = max(gain(node.left), 0)`, `right = max(gain(node.right), 0)`.
   - `best = max(best, node.val + left + right)` — path with `node` as its top.
   - return `node.val + max(left, right)` — one arm for the parent.
3. Call `gain(root)`; return `best`.

### Python code (LeetCode-ready, recursive DFS)

```python
from typing import Optional


class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        best = root.val                       # the tree has at least one node

        def gain(node: Optional[TreeNode]) -> int:
            nonlocal best
            if node is None:
                return 0
            left = max(gain(node.left), 0)    # drop a negative arm
            right = max(gain(node.right), 0)
            best = max(best, node.val + left + right)   # path bending at node
            return node.val + max(left, right)          # only one side may go up

        gain(root)
        return best
```

### Python code (iterative post-order, no recursion)

```python
from typing import Optional


class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        # 1) List nodes so that every parent appears before its children.
        order, stack = [], [root]
        while stack:
            node = stack.pop()
            order.append(node)
            if node.left:
                stack.append(node.left)
            if node.right:
                stack.append(node.right)

        # 2) Walk that list backwards: children are finished before parents.
        gain = {None: 0}                      # node -> best downward arm
        best = root.val
        for node in reversed(order):
            left = max(gain[node.left], 0)
            right = max(gain[node.right], 0)
            best = max(best, node.val + left + right)
            gain[node] = node.val + max(left, right)
        return best
```

### Recursion limit — is the recursive version safe?

- Python's default recursion limit is **1000**. The recursive `gain` uses about `h + 1` frames.
- The constraints allow `3 · 10^4` nodes, so a skewed tree can be `3 · 10^4` levels tall — **30 times** the default limit. In plain Python that raises `RecursionError`.
- The recursive solution is widely reported to be accepted on LeetCode, but the judge's recursion settings are not documented, so don't rely on them: that would be a property of the judge, not of Python. The iterative version above is safe for every allowed input. (The brute force's `best_down` is recursive too, so it has the same issue on top of being slow.)
- For a balanced tree the height is only about `log2(3 · 10^4) ≈ 15`, so recursion depth is not a concern there.

---

## 7. Line-by-Line Explanation

(Recursive DFS)

| Line | What it does | Why |
|---|---|---|
| `best = root.val` | Starting value for the answer. | Any single node is a valid path. Starting at 0 would be wrong for an all-negative tree like `[-3]`. |
| `def gain(node)` / `nonlocal best` | Helper that returns the best downward arm; may update `best` from the outer function. | `nonlocal` lets the inner function assign to the outer variable. |
| `if node is None: return 0` | An empty child offers an arm of 0. | "Taking nothing" from that side. |
| `left = max(gain(node.left), 0)` | Best arm into the left subtree, clipped at 0. | A negative arm would only reduce any path, so we refuse it. |
| `right = max(gain(node.right), 0)` | Same for the right. | |
| `best = max(best, node.val + left + right)` | Records the best path whose **top** is `node`. | Both arms may be used because this path ends here and does not go up. |
| `return node.val + max(left, right)` | Gives the parent a one-sided arm. | Going up to the parent means the path continues; it can't use both sides without branching. |
| `gain(root)` / `return best` | Runs the post-order walk and returns the record. | The return value of `gain(root)` itself is **not** the answer — it's only a one-sided arm. |

---

## 8. Dry Run

**Input (Example 2):** `root = [-10,9,20,null,null,15,7]`

```text
        -10
        /  \
       9    20
           /  \
          15   7
```

Start: `best = -10`.

| Step | Node finished | `left` (clipped) | `right` (clipped) | Bent path `val + left + right` | `best` after | Returns `val + max(left, right)` |
|---|---|---|---|---|---|---|
| 1 | 9 | 0 | 0 | 9 + 0 + 0 = 9 | 9 | 9 |
| 2 | 15 | 0 | 0 | 15 | 15 | 15 |
| 3 | 7 | 0 | 0 | 7 | 15 | 7 |
| 4 | 20 | 15 | 7 | 20 + 15 + 7 = **42** | **42** | 20 + 15 = 35 |
| 5 | -10 | 9 | 35 | -10 + 9 + 35 = 34 | 42 | -10 + 35 = 25 |

**Result:** `42` ✅ (path `15 → 20 → 7`). Notice that `gain(root) = 25` is not the answer — the answer was recorded at node `20`.

**Example 1:** `root = [1,2,3]`, start `best = 1`

| Node finished | `left` | `right` | Bent path | `best` | Returns |
|---|---|---|---|---|---|
| 2 | 0 | 0 | 2 | 2 | 2 |
| 3 | 0 | 0 | 3 | 3 | 3 |
| 1 | 2 | 3 | 1 + 2 + 3 = **6** | **6** | 4 |

**Result:** `6` ✅

**All-negative check:** `[-1,-2,-3]`: node `-2` → bent `-2`, `best = max(-1, -2) = -1`, returns `-2`; node `-3` → `best` stays `-1`; root: both arms clipped to 0, bent `-1` → `best = -1` ✅.

---

## 9. Concepts, Data Structures, and Patterns

- **"Return one thing, record another":** the helper's return value (one-sided gain) is what the **parent** needs; the global `best` holds what the **problem** asks. This pattern also solves Diameter of Binary Tree (543) and Longest Univalue Path (687, Q3 below).
- **Post-order DFS / tree DP:** each node's value depends only on its children's results, so compute bottom-up and reuse — this is what removes the brute force's repeated work.
- **Kadane-style clipping:** `max(gain, 0)` is the same "drop a negative running sum" rule as in [005_maximum_subarray.md](../01_array/005_maximum_subarray.md). In fact, on a chain-shaped tree this problem *is* Maximum Subarray.
- **`nonlocal`:** lets a nested function update a variable of the enclosing function.
- **Iterative post-order via reversed preorder:** list nodes parent-before-children with a stack, then process the list backwards.
- **Related notes in this project:**
  - [041_maximum_depth_of_binary_tree.md](041_maximum_depth_of_binary_tree.md) — the same post-order shape, returning a height instead of a gain (its Q4 is Diameter).
  - [045_binary_tree_level_order_traversal.md](045_binary_tree_level_order_traversal.md) — BFS, the other main tree traversal.

---

## 10. Complexity Analysis

Let `n` = number of nodes, `h` = height (about `log2 n` balanced, up to `n` skewed).

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Brute force (fresh arms for every top) | `O(n · h)`; worst `O(n²)` | `O(h)` | Each node is re-walked once per ancestor. |
| Recursive post-order DFS | `O(n)` | `O(h)` — best `O(log n)`, worst `O(n)` | Each node's gain is computed once with `O(1)` extra work; the call stack follows one root-to-node path. |
| Iterative post-order | `O(n)` | `O(n)` | The `order` list and the `gain` dictionary each hold all `n` nodes (the explicit stack is smaller). Uses more memory than recursion, but can never hit a recursion limit. |

`O(n)` time is optimal: any node could be part of the best path, so all must be looked at.

---

## 11. Edge Cases

| Case | Example | Expected result | Why |
|---|---|---|---|
| Single negative node | `[-3]` | `-3` | Path must be non-empty. |
| All negative | `[-1,-2,-3]` | `-1` | Best is the single largest node; `best` must not start at 0. |
| Negative child | `[2,-1]` | `2` | Arm `-1` is clipped to 0. |
| Bend skipping a negative side | `[1,-2,3]` | `4` | `1 → 3`; the left arm `-2` is dropped. |
| Best path avoids the root | `[-10,9,20,null,null,15,7]` | `42` | Official example 2. |
| Long bent path | `[5,4,8,11,null,13,4,7,2,null,null,null,1]` | `48` | `7 → 11 → 4 → 5 → 8 → 13`. |
| Positive tree | `[1,2,3]` | `6` | Official example 1: use both sides. |
| Skewed tree of `3 · 10^4` nodes | chain | (depends on values) | Iterative version is safe; recursive needs the judge's raised limit. |

---

## 12. Common Mistakes and Debugging

1. **Returning both sides to the parent.** `return node.val + left + right` lets paths branch and over-counts. Return `node.val + max(left, right)`.
2. **Initialising `best = 0`.** Fails for all-negative trees (`[-3]` → should be `-3`). Use `root.val` or `float("-inf")`.
3. **Not clipping negative arms.** Without `max(…, 0)`, a node is forced to take a bad child: `[2,-1]` would give `1`.
4. **Clipping the node's own value.** `max(node.val, 0)` is wrong — the node itself must be on the path; only the arms are optional.
5. **Returning `gain(root)` as the answer.** That is the best path *starting at the root and going down one side*, not the best path anywhere (Example 2: 25 vs 42).
6. **Assigning to `best` inside the helper without `nonlocal`.** Python then treats `best` as a new local variable and raises `UnboundLocalError`. Use `nonlocal`, or `self.best`.

**Debugging tip:** print `node.val, left, right, best` right after updating `best` and compare with the dry-run table.

---

## 13. Practice Questions

**Q1. What does the algorithm return for `root = [1,-2,3]`, and at which node is the answer recorded?**

<details><summary>Hint</summary>Compute the clipped gains of `-2` and `3` first.</summary></details>

**Answer:** `4`, recorded at the root. Start `best = 1`. Node `-2`: bent path `-2`, `best` stays 1, returns `-2`. Node `3`: bent `3`, `best = 3`, returns 3. Root: `left = max(-2, 0) = 0`, `right = 3`, bent path `1 + 0 + 3 = 4` → `best = 4`. The path is `1 → 3`.

**Q2. Easier variant: the path must start at the root and end at a leaf. Return the maximum sum.**

<details><summary>Hint</summary>No bending and no clipping: you must go all the way down to a leaf, so a negative child may be forced.</summary></details>

**Answer:**

```python
def max_root_to_leaf(node):
    if node.left is None and node.right is None:
        return node.val
    options = []
    if node.left:
        options.append(max_root_to_leaf(node.left))
    if node.right:
        options.append(max_root_to_leaf(node.right))
    return node.val + max(options)


ex2 = TreeNode(-10, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))
assert max_root_to_leaf(ex2) == 25           # -10 -> 20 -> 15
assert max_root_to_leaf(TreeNode(1, TreeNode(-5))) == -4   # must reach the leaf
```

**Q3. Longest Univalue Path (LeetCode 687): the most edges on a path where all nodes have the same value.**

<details><summary>Hint</summary>Same "return one arm, record the bend" pattern. An arm only extends into a child with the same value.</summary></details>

**Answer:**

```python
def longest_univalue_path(root):
    best = 0

    def arm(node):
        nonlocal best
        if node is None:
            return 0
        left, right = arm(node.left), arm(node.right)
        left = left + 1 if node.left and node.left.val == node.val else 0
        right = right + 1 if node.right and node.right.val == node.val else 0
        best = max(best, left + right)      # bend at node
        return max(left, right)             # one side goes up

    arm(root)
    return best


t1 = TreeNode(5, TreeNode(4, TreeNode(1), TreeNode(1)), TreeNode(5, None, TreeNode(5)))
t2 = TreeNode(1, TreeNode(4, TreeNode(4), TreeNode(4)), TreeNode(5, None, TreeNode(5)))
assert longest_univalue_path(t1) == 2
assert longest_univalue_path(t2) == 2
assert longest_univalue_path(None) == 0
```

**Q4. Show that on a chain-shaped tree, this problem becomes Maximum Subarray.**

<details><summary>Hint</summary>In a chain every node has at most one child, so a path is a contiguous run of the chain.</summary></details>

**Answer:** Build a right-leaning chain from a list and compare with Kadane's algorithm from [005_maximum_subarray.md](../01_array/005_maximum_subarray.md).

```python
def max_path_sum(root):
    best = root.val

    def gain(node):
        nonlocal best
        if node is None:
            return 0
        left, right = max(gain(node.left), 0), max(gain(node.right), 0)
        best = max(best, node.val + left + right)
        return node.val + max(left, right)

    gain(root)
    return best


def kadane(nums):
    current = best = nums[0]
    for num in nums[1:]:
        current = max(num, current + num)
        best = max(best, current)
    return best


nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
chain = None
for value in reversed(nums):
    chain = TreeNode(value, None, chain)
assert max_path_sum(chain) == kadane(nums) == 6
```

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** Post-order tree DP — return the one-sided gain, record the two-sided bend.
- **Key idea:** `left, right = max(gain(L), 0), max(gain(R), 0)`; `best = max(best, val + left + right)`; `return val + max(left, right)`.
- **Time:** `O(n)`.
- **Auxiliary space:** `O(h)` recursive (`O(log n)` balanced, `O(n)` skewed); `O(n)` for the iterative version.
- **Traps:** start `best` at `root.val`; never return both sides upward; a `3 · 10^4`-deep chain exceeds Python's default recursion limit.
- **One-line memory hook:** *"Tell your parent your best arm; tell the notebook your best bend."*

### Completion checklist

- [x] Problem requirements verified
- [x] Examples and constraints verified
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force solution written and tested
- [x] Optimized Python solutions (recursive and iterative post-order) written and tested (`tools/tests/p044.py`)
- [x] Line-by-line explanation written
- [x] Dry run completed with a real example
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
