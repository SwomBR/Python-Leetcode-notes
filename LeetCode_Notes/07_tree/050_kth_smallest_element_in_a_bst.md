# 050. Kth Smallest Element in a BST

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Kth Smallest Element in a BST |
| **LeetCode number** | 230 |
| **Topic (source list)** | Tree |
| **Also uses** | Binary Search Tree, Inorder Traversal, Stack |
| **Difficulty** | Medium |
| **LeetCode URL** | <https://leetcode.com/problems/kth-smallest-element-in-a-bst/> |
| **Pattern** | Inorder traversal of a BST visits values in sorted order — stop at the k-th visit |

---

## 2. Problem Explanation

### Beginner primer: `TreeNode`, BSTs and LeetCode's tree lists

A binary tree is made of nodes; each node has a value `val` and two links `left` and `right` (`None` when the child is missing). LeetCode provides the class as a comment:

```text
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
```

In a **binary search tree (BST)**, for every node, all values in its left subtree are smaller and all values in its right subtree are larger (see [049_validate_binary_search_tree.md](049_validate_binary_search_tree.md)).

The input `root = [5,3,6,2,4,null,null,1]` is a **level-order list** (row by row, left to right, `null` for a missing child, trailing `null`s dropped):

```text
List: [5, 3, 6, 2, 4, null, null, 1]

            5            <- row 0
           / \
          3   6          <- row 1: children of 5
         / \
        2   4            <- children of 3: 2, 4 ; children of 6: null, null
       /
      1                  <- children of 2: 1 (right child omitted)
```

### What are we given?

- `root` — the root of a binary search tree.
- `k` — a whole number between 1 and the number of nodes.

### What must we return?

The **k-th smallest** value in the tree, counting from **1** (`k = 1` means the minimum).

### Examples

**Example 1**

```text
Input:  root = [3,1,4,null,2], k = 1
Output: 1
```

```text
        3
       / \
      1   4
       \
        2
```

Sorted values: `1, 2, 3, 4`. The 1st smallest is `1`.

**Example 2**

```text
Input:  root = [5,3,6,2,4,null,null,1], k = 3
Output: 3
```

Sorted values (tree drawn above): `1, 2, 3, 4, 5, 6`. The 3rd smallest is `3`.

### Constraints

- The number of nodes in the tree is `n`.
- `1 <= k <= n <= 10^4`
- `0 <= Node.val <= 10^4`

**Follow-up:** If the BST is modified often (we insert and delete nodes) and we need the k-th smallest value frequently, how could we optimise? (Discussed in Sections 6 and 13.)

---

## 3. Everyday Analogy

> **Explain it like I'm five**

Imagine a family tree of numbered toy boxes where, at every box, smaller numbers are always stacked to the **left** and bigger ones to the **right**. If you want the 3rd smallest box, you don't need to sort anything: just walk the tree in the order *"everything on the left first, then me, then everything on the right"*. That walk visits boxes from smallest to biggest — like reading a sorted list. Count as you go: 1, 2, **3** — stop! That's your answer, and you never had to look at the big boxes on the far right.

---

## 4. Step-by-Step Logic

1. **Key BST fact:** an **inorder** traversal (left subtree, node, right subtree) visits the values in **increasing order**.
2. **So the k-th visited node is the answer.** We don't need all values, only the first `k` in sorted order.
3. **The smallest value** is found by walking left from the root until there is no left child.
4. **Iterative inorder with a stack:**
   - push nodes while moving left (they are waiting to be visited);
   - pop one → that's the next value in sorted order; count it;
   - if the count reaches `k`, return it;
   - otherwise continue with the popped node's right subtree (and again go left as far as possible).
5. **Stopping early** means we touch only about `h + k` nodes (`h` = height), not all `n`.
6. **Follow-up thinking:** if the tree changes often and we query often, store in every node the **size of its subtree**. Then at each node we know how many values are on its left and can jump directly left or right — `O(h)` per query, no traversal.

---

## 5. Brute-Force Solution

### Algorithm

1. Visit every node (in any order) and collect all values into a list.
2. Sort the list.
3. Return the element at index `k - 1`.

### Python code

```python
from typing import Optional


class Solution:
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        values = []
        stack = [root]
        while stack:                     # any traversal order works
            node = stack.pop()
            if node is not None:
                values.append(node.val)
                stack.append(node.left)
                stack.append(node.right)
        values.sort()
        return values[k - 1]             # k is 1-indexed
```

### Explanation

- This ignores the BST property completely — it would work for any binary tree.
- `values[k - 1]` converts the 1-indexed `k` to a 0-indexed list position.

### Complexity

- **Time:** `O(n log n)` for sorting (collecting is `O(n)`).
- **Auxiliary space:** `O(n)` for the list.
- **Trade-off:** easy and correct; with `n ≤ 10^4` it is accepted, but it wastes the BST's built-in order and always processes every node, even when `k = 1`.

---

## 6. Optimized Solution

### Idea

Do an **iterative inorder traversal** and stop as soon as `k` nodes have been visited.

### Algorithm

1. `stack = []`, `node = root`.
2. Loop:
   - While `node` exists: push it and move to `node.left`.
   - Pop the top node — the next smallest value. Decrease `k`.
   - If `k == 0`, return its value.
   - Move to its right child: `node = node.right`.

### Python code (LeetCode-ready)

```python
from typing import Optional


class Solution:
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        stack = []
        node = root
        while True:
            while node:                 # go as far left as possible
                stack.append(node)
                node = node.left
            node = stack.pop()          # next smallest value
            k -= 1
            if k == 0:
                return node.val
            node = node.right           # then explore the right subtree
```

The `while True` loop always ends with a `return`, because the constraints guarantee `1 <= k <= n`.

### Alternative: recursive inorder with early stop

```python
from typing import Optional


class Solution:
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        count = 0
        answer = None

        def inorder(node):
            nonlocal count, answer
            if node is None or answer is not None:
                return
            inorder(node.left)
            if answer is not None:      # found in the left subtree: stop
                return
            count += 1
            if count == k:
                answer = node.val
                return
            inorder(node.right)

        inorder(root)
        return answer
```

Shorter to reason about, but it recurses as deep as the tree's height. With up to 10^4 nodes a chain-shaped BST needs about 10^4 nested calls, while CPython's default recursion limit is 1000, so the iterative version is the safer one (or call `sys.setrecursionlimit`).

### Follow-up: frequent inserts/deletes and frequent queries

Re-running an inorder walk costs `O(h + k)` per query, which can be `O(n)` when `k` is large. If queries are frequent:

1. **Augment each node with `size`** = number of nodes in its subtree.
2. **Query:** at a node, let `left = size(node.left)`.
   - `k <= left` → the answer is in the left subtree;
   - `k == left + 1` → it's this node;
   - otherwise → search the right subtree for `k - left - 1`.
   That is one root-to-leaf path: `O(h)`.
3. **Insert/delete:** update `size` on every node along the path you walk — also `O(h)`.
4. **Keep `h` small:** with a self-balancing BST (AVL, red-black tree; rotations must also fix `size`), `h = O(log n)`, so every operation is `O(log n)`. This structure is called an **order-statistic tree**.

Simpler practical alternatives: keep the values in a sorted list (`bisect.insort` is `O(n)` per insert but very fast in practice), or use a sorted container library. Q2 in Section 13 implements the size-augmented insert and query.

---

## 7. Line-by-Line Explanation

(Iterative version.)

| Line | What it does | Why |
|---|---|---|
| `stack = []` | Holds nodes we have passed on the way left but not visited yet. | They are visited later, in increasing order. |
| `node = root` | The current position. | Start at the top. |
| `while True:` | Repeats until we return. | The answer always exists (`k <= n`). |
| `while node: stack.append(node); node = node.left` | Pushes the whole left spine. | The smallest unvisited value is at the bottom of the left spine. |
| `node = stack.pop()` | Takes the next node in inorder. | All smaller values have already been visited. |
| `k -= 1` | Counts this visit. | When `k` reaches 0, we have visited exactly `k` values. |
| `if k == 0: return node.val` | Returns the k-th smallest. | Early exit — the rest of the tree is never touched. |
| `node = node.right` | Moves to the right subtree. | Values there are larger than this node but smaller than everything still on the stack. |

---

## 8. Dry Run

**Input:** Example 2, `root = [5,3,6,2,4,null,null,1]`, `k = 3`

| Step | Action | `stack` (bottom → top) | Popped | `k` after | Next `node` |
|---|---|---|---|---|---|
| 1 | Go left from 5: push 5, 3, 2, 1 | `[5, 3, 2, 1]` | — | 3 | `None` (1 has no left) |
| 2 | Pop | `[5, 3, 2]` | 1 | 2 | `1.right = None` |
| 3 | Inner loop does nothing; pop | `[5, 3]` | 2 | 1 | `2.right = None` |
| 4 | Inner loop does nothing; pop | `[5]` | 3 | **0** | return `3` |

**Result:** `3` ✅ — nodes 4, 5 and 6 were never popped.

**Example 1:** `root = [3,1,4,null,2]`, `k = 1` → push 3, 1; pop 1; `k` becomes 0 → return `1` ✅.

### Second dry run: Example 1 with `k = 3` (shows the right-subtree step)

| Step | Action | `stack` | Popped | `k` after |
|---|---|---|---|---|
| 1 | Push 3, 1 | `[3, 1]` | — | 3 |
| 2 | Pop 1, move to its right child 2 | `[3]` | 1 | 2 |
| 3 | Push 2 (no left child), pop 2 | `[3]` | 2 | 1 |
| 4 | `2.right` is `None`; pop 3 | `[]` | 3 | **0** → return `3` |

Sorted values are `1, 2, 3, 4`, so the 3rd smallest is `3` ✅.

---

## 9. Concepts, Data Structures, and Patterns

- **Inorder traversal of a BST = sorted order.** The same fact validates a BST in [049_validate_binary_search_tree.md](049_validate_binary_search_tree.md).
- **Iterative inorder with an explicit stack:** "push the left spine, pop, visit, go right". It avoids recursion limits and allows stopping early.
- **Early termination:** stop as soon as the answer is known — cost depends on `k`, not on `n`.
- **Augmented data structures:** storing extra information (`size`) in each node to answer queries faster — the order-statistic tree from the follow-up.
- **Balanced BSTs (AVL / red-black):** keep the height `O(log n)` so every operation is fast.
- **Related problems:** Lowest Common Ancestor of a BST ([051_lowest_common_ancestor_of_bst.md](051_lowest_common_ancestor_of_bst.md)) also exploits BST ordering; "Kth Largest Element in an Array" (LeetCode 215) solves a similar question on an unsorted array with a heap or quickselect.

---

## 10. Complexity Analysis

Let `n` = number of nodes, `h` = tree height (`log n` if balanced, up to `n` for a chain).

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Collect + sort (brute force) | `O(n log n)` | `O(n)` | Visits every node, then sorts. |
| Iterative inorder, early stop (optimized) | `O(h + k)` | `O(h)` | We first walk down at most `h` nodes; after that, every push is "paid for" by a later pop or lies on one root-to-leaf path, and we pop exactly `k` nodes. The stack never holds more than one path. Worst case `O(n)`. |
| Recursive inorder, early stop | `O(h + k)` | `O(h)` | Same work; the call stack replaces the explicit stack. |
| Size-augmented BST (follow-up) | `O(h)` per query, insert and delete; `O(log n)` if balanced | `O(n)` extra for the `size` fields | One root-to-leaf path per operation. |

---

## 11. Edge Cases

| Case | Tree | `k` | Expected | Why |
|---|---|---|---|---|
| Single node | `[0]` | 1 | `0` | Only value; also the minimum allowed value. |
| Maximum value | `[10000]` | 1 | `10000` | — |
| `k = n` (largest) | `[5,3,6,2,4,null,null,1]` | 6 | `6` | Traversal reaches the last node. |
| Left child only | `[2,1]` | 2 | `2` | Visit 1, then 2. |
| Right child only | `[1,null,2]` | 1 | `1` | The root itself is the minimum. |
| Answer is in a right subtree of a left child | `[3,1,4,null,2]` | 2 | `2` | 2 is visited after 1, via `1.right`. |
| Chain (sorted insertion) of 10^4 nodes | — | any | sorted value `k` | Iterative version handles it; the recursive one needs a raised recursion limit. |

---

## 12. Common Mistakes and Debugging

1. **Off-by-one with 1-indexed `k`.** In the brute force, the answer is `values[k - 1]`, not `values[k]`.
2. **Using preorder or level order and expecting sorted output.** Only **inorder** gives sorted values in a BST.
3. **Forgetting to stop early in the recursive version.** Without the `answer is not None` checks the recursion keeps going (still correct, but it visits the whole tree and may overwrite the answer if you don't guard it).
4. **Decrementing `k` before popping**, or checking `k == 0` before decrementing — both shift the answer by one position.
5. **Moving to `node.left` after popping** instead of `node.right` — causes an infinite loop or wrong order.
6. **For the follow-up:** forgetting to update `size` on the path when inserting/deleting (or during rotations) silently breaks later queries.

**Debugging tip:** print the popped values in order — they must come out sorted. If they don't, the traversal (not the counting) is wrong.

---

## 13. Practice Questions

**Q1. For `root = [5,3,6,2,4,null,null,1]`, what does the optimized code return for `k = 5`, and which node is popped last?**

<details><summary>Hint</summary>Write the inorder sequence: 1, 2, 3, 4, 5, 6.</summary></details>

**Answer:** `5`. The pops are 1, 2, 3, 4 (reached via `3.right`), then 5 — when 5 is popped, `k` becomes 0. Node 6 is never popped.

**Q2. (Follow-up) Implement a size-augmented BST: `insert(root, val)` and `kth(root, k)` in `O(h)` each.**

<details><summary>Hint</summary>Store `node.size`. When inserting, add 1 to `size` on every node along the path. When querying, compare `k` with the size of the left subtree.</summary></details>

**Answer:**

```python
import random


def size(node):
    return node.size if node else 0


def insert(root, val):
    if root is None:
        node = TreeNode(val)
        node.size = 1
        return node
    node = root
    while True:
        node.size += 1                     # the new value will live below this node
        if val < node.val:
            if node.left is None:
                node.left = TreeNode(val)
                node.left.size = 1
                return root
            node = node.left
        else:
            if node.right is None:
                node.right = TreeNode(val)
                node.right.size = 1
                return root
            node = node.right


def kth(root, k):
    node = root
    while node:
        left = size(node.left)
        if k <= left:
            node = node.left
        elif k == left + 1:
            return node.val
        else:
            k -= left + 1
            node = node.right
    raise ValueError("k is out of range")


rng = random.Random(0)
values = rng.sample(range(10001), 200)
root = None
for v in values:
    root = insert(root, v)
ordered = sorted(values)
assert all(kth(root, k) == ordered[k - 1] for k in range(1, 201))
root = insert(root, 10001)            # tree changes: query again without re-traversing
assert kth(root, 201) == 10001
```

Deleting works the same way: decrease `size` on every node along the path to the removed node (and, if you replace a node by its inorder successor, along that path too). In a self-balancing tree, rotations recompute `size` from the children.

**Q3. Find the k-th *largest* value in a BST.**

<details><summary>Hint</summary>Do the inorder traversal "mirrored": right subtree, node, left subtree.</summary></details>

**Answer:** Reverse inorder visits values in **decreasing** order.

```python
def kth_largest(root, k):
    stack, node = [], root
    while True:
        while node:
            stack.append(node)
            node = node.right          # go right first
        node = stack.pop()
        k -= 1
        if k == 0:
            return node.val
        node = node.left


tree = TreeNode(5, TreeNode(3, TreeNode(2, TreeNode(1)), TreeNode(4)), TreeNode(6))
assert [kth_largest(tree, k) for k in range(1, 7)] == [6, 5, 4, 3, 2, 1]
```

**Q4. Without the stack, how could you find the k-th smallest with `O(1)` extra space?**

<details><summary>Hint</summary>Morris traversal temporarily links a node's inorder predecessor back to the node.</summary></details>

**Answer:** Morris inorder traversal: for each node with a left child, find its inorder predecessor (rightmost node of the left subtree) and set `predecessor.right = node` as a temporary "thread" back; when you come back along the thread, remove it and visit the node. It visits nodes in sorted order using `O(1)` extra space and `O(n)` time, but it temporarily modifies the tree, so it is rarely worth the complexity in interviews.

```python
def kth_smallest_morris(root, k):
    node, answer = root, None
    while node:
        if node.left is None:
            k -= 1
            if k == 0 and answer is None:
                answer = node.val
            node = node.right
        else:
            pred = node.left
            while pred.right and pred.right is not node:
                pred = pred.right
            if pred.right is None:
                pred.right = node          # create the thread
                node = node.left
            else:
                pred.right = None          # remove the thread, then visit node
                k -= 1
                if k == 0 and answer is None:
                    answer = node.val
                node = node.right
    return answer                          # full walk restores every thread


tree = TreeNode(3, TreeNode(1, None, TreeNode(2)), TreeNode(4))
assert [kth_smallest_morris(tree, k) for k in range(1, 5)] == [1, 2, 3, 4]
assert tree.left.right.right is None       # the tree was restored
```

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** Iterative inorder traversal with early stop.
- **Key idea:** Inorder visits a BST's values in sorted order; the k-th pop is the answer.
- **Time:** `O(h + k)`.
- **Auxiliary space:** `O(h)`.
- **Follow-up:** store subtree sizes (order-statistic tree) → `O(h)` per query/update, `O(log n)` if balanced.
- **One-line memory hook:** *"Left, me, right — count to k and stop."*

### Completion checklist

- [x] Problem requirements verified
- [x] Examples and constraints verified
- [x] Beginner-friendly analogy, TreeNode primer and logic written
- [x] Brute-force solution written and tested
- [x] Optimized Python solution written and tested (`tools/tests/p050.py`), plus the recursive version
- [x] Line-by-line explanation written
- [x] Dry run completed with a real example
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added, including the follow-up
- [x] Final review completed
