# 048. Construct Binary Tree from Preorder and Inorder Traversal

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Construct Binary Tree from Preorder and Inorder Traversal |
| **LeetCode number** | 105 |
| **Topic (source list)** | Tree |
| **Also uses** | Array, Hash Table, Divide and Conquer, Recursion |
| **Difficulty** | Medium |
| **LeetCode URL** | <https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/> |
| **Pattern** | Divide and conquer: preorder gives the root, inorder splits left/right; hash map of inorder positions |

---

## 2. Problem Explanation

### Beginner primer: `TreeNode`, traversals and LeetCode's tree lists

A binary tree is made of nodes; each node has a `val` and `left`/`right` links (`None` when missing). LeetCode provides the class as a comment:

```text
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
```

Two ways to list a tree's values (both visit the left subtree before the right subtree):

- **Preorder:** node **first**, then the left subtree, then the right subtree. → *Root, Left, Right*
- **Inorder:** the left subtree, then the node, then the right subtree. → *Left, Root, Right*

LeetCode prints the **answer** tree as a **level-order list** (row by row, `null` for missing children, trailing `null`s dropped):

```text
Output list: [3, 9, 20, null, null, 15, 7]

        3              <- row 0
       / \
      9   20           <- row 1: children of 3
         /  \
        15   7         <- children of 9: null, null ; children of 20: 15, 7
```

For this tree: preorder = `[3, 9, 20, 15, 7]`, inorder = `[9, 3, 15, 20, 7]`.

### What are we given?

- `preorder` — the preorder listing of some binary tree's values.
- `inorder` — the inorder listing of the **same** tree.

### What must we return?

The root `TreeNode` of the tree that produced these two listings.

### The rules

1. All values are **unique**, so each value identifies exactly one node.
2. Both lists describe the same tree and have the same length; the input is always valid.
3. Because the values are unique, the tree is **uniquely determined** — there is exactly one correct answer.

### Examples

**Example 1**

```text
Input:  preorder = [3,9,20,15,7], inorder = [9,3,15,20,7]
Output: [3,9,20,null,null,15,7]
```

The tree is the one drawn above.

**Example 2**

```text
Input:  preorder = [-1], inorder = [-1]
Output: [-1]
```

A single node.

### Constraints

- `1 <= preorder.length <= 3000`
- `inorder.length == preorder.length`
- `-3000 <= preorder[i], inorder[i] <= 3000`
- `preorder` and `inorder` consist of **unique** values.
- Each value of `inorder` also appears in `preorder`.
- `preorder` is guaranteed to be the preorder traversal of the tree.
- `inorder` is guaranteed to be the inorder traversal of the tree.

There is no follow-up in the statement.

---

## 3. Everyday Analogy

> **Explain it like I'm five**

A class lines up for a photo in two different ways.

- In the **preorder** line, every team captain stands **before** their whole team.
- In the **inorder** line, every captain stands **in the middle** — their left-side team on their left, their right-side team on their right.

The very first kid in the preorder line is the big boss. Find the boss in the inorder line: everyone to the boss's left is the boss's left team, and everyone to the right is the right team. Now do the same thing again inside each team: the next kid in the preorder line is that team's captain, and so on, until every team has only one kid.

The slow part is *finding* a kid in the inorder line. So we make a **name tag list** ahead of time: "Kid 9 stands at spot 0, kid 3 at spot 1, …". Then finding anyone is instant.

---

## 4. Step-by-Step Logic

1. **The root is easy.** In preorder the root comes first, so `preorder[0]` is the root.
2. **Split with inorder.** Find the root's position `mid` in `inorder`. Everything left of `mid` is the left subtree; everything right of it is the right subtree. The left subtree therefore has `mid` nodes (counting from the start of the current range).
3. **Split preorder the same way.** After the root, preorder lists the whole left subtree (`mid` values), then the whole right subtree.
4. **Recurse.** Build the left subtree from its two pieces and the right subtree from its two pieces. A piece of length 0 means "no child".
5. **Speed-up 1 — no searching.** Store `value -> inorder index` in a dictionary so finding `mid` is `O(1)` instead of an `O(n)` scan.
6. **Speed-up 2 — no slicing.** Instead of copying sub-lists, describe each piece by an inorder range `[lo, hi]`, and read roots from preorder with a single moving pointer: since we build *root → left subtree → right subtree*, we consume preorder values in exactly preorder order.

---

## 5. Brute-Force Solution

### Algorithm

1. If `preorder` is empty, return `None`.
2. The root value is `preorder[0]`; find its position `mid` with `inorder.index(...)`.
3. Left subtree: `preorder[1 : mid + 1]` and `inorder[:mid]`.
4. Right subtree: `preorder[mid + 1 :]` and `inorder[mid + 1 :]`.
5. Build both recursively and attach them.

### Python code

```python
from typing import List, Optional


class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        if not preorder:
            return None
        root_val = preorder[0]
        mid = inorder.index(root_val)          # O(n) linear search
        root = TreeNode(root_val)
        root.left = self.buildTree(preorder[1:mid + 1], inorder[:mid])
        root.right = self.buildTree(preorder[mid + 1:], inorder[mid + 1:])
        return root
```

### Explanation

- `mid` is both the root's position in `inorder` **and** the size of the left subtree.
- In `preorder`, index 0 is the root, indices `1..mid` are the left subtree, and the rest is the right subtree.
- Slicing creates new lists, so every recursive call gets its own smaller problem.

### Complexity

- **Time:** `O(n²)` in the worst case. For a chain-shaped tree each level calls `index` and makes slices of length `n-1`, `n-2`, …, which sums to about `n²/2`. For a balanced tree it is `O(n log n)`. With `n = 3000` even the worst case (about 4.5 million element operations, done by fast C code) is accepted — but it scales badly.
- **Auxiliary space:** `O(n²)` in the worst case, because the slices along the current recursion path are all alive at once (`n-1 + n-2 + …` for a chain), plus `O(h)` call stack.

---

## 6. Optimized Solution

### Idea

- A dictionary `index_of[value] = position in inorder` makes each split `O(1)`.
- A shared pointer `pre_idx` walks through `preorder`; every time we create a node we take `preorder[pre_idx]` and move the pointer forward.
- Each recursive call works on an inorder range `[lo, hi]` — no slicing.

### Algorithm

1. Build `index_of` from `inorder`.
2. `pre_idx = 0`.
3. `build(lo, hi)`:
   - if `lo > hi` → empty range → return `None`;
   - `root_val = preorder[pre_idx]`, `pre_idx += 1`, create the node;
   - `mid = index_of[root_val]`;
   - `node.left = build(lo, mid - 1)` **first** (preorder lists the left subtree next), then `node.right = build(mid + 1, hi)`.
4. Return `build(0, n - 1)`.

### Python code (LeetCode-ready)

```python
from typing import List, Optional


class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        index_of = {value: i for i, value in enumerate(inorder)}
        pre_idx = 0

        def build(lo: int, hi: int) -> Optional[TreeNode]:
            nonlocal pre_idx
            if lo > hi:                       # no values in this inorder range
                return None
            root_val = preorder[pre_idx]
            pre_idx += 1
            node = TreeNode(root_val)
            mid = index_of[root_val]
            node.left = build(lo, mid - 1)    # must be built before the right side
            node.right = build(mid + 1, hi)
            return node

        return build(0, len(inorder) - 1)
```

### Recursion depth — an honest note

`build` recurses as deep as the tree's height `h`. With up to 3000 nodes, a chain-shaped tree has `h = 3000`, but CPython's default recursion limit is 1000, so in a normal Python script this would raise `RecursionError`. Whether a given judge raises the limit is outside your control; to be safe add `sys.setrecursionlimit(10000)` or use the iterative version below.

### Iterative version (stack, no recursion)

```python
from typing import List, Optional


class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        root = TreeNode(preorder[0])
        stack = [root]          # nodes whose right child is not decided yet
        j = 0                   # next position in inorder
        for value in preorder[1:]:
            node = TreeNode(value)
            parent = stack[-1]
            if parent.val != inorder[j]:
                parent.left = node             # still going down-left
            else:
                # Pop every node whose left side is finished (in inorder order);
                # the last one popped is the parent of this right child.
                while stack and stack[-1].val == inorder[j]:
                    parent = stack.pop()
                    j += 1
                parent.right = node
            stack.append(node)
        return root
```

While the top of the stack is not the next inorder value, we are still walking down left edges. When it *is* the next inorder value, that node's left side is complete; we pop up until the inorder sequence and the stack disagree, and the new value becomes the right child of the last node popped. Each node is pushed and popped once → `O(n)` time, `O(h)` stack.

---

## 7. Line-by-Line Explanation

(Recursive hash-map version.)

| Line | What it does | Why |
|---|---|---|
| `index_of = {value: i for i, value in enumerate(inorder)}` | Maps each value to its inorder position. | Values are unique, so the mapping is well defined; lookups are `O(1)`. |
| `pre_idx = 0` | Pointer to the next root in `preorder`. | We create nodes in preorder order, so we just walk forward. |
| `def build(lo, hi):` | Builds the subtree whose inorder values are `inorder[lo..hi]`. | A range describes the piece without copying it. |
| `nonlocal pre_idx` | Lets the inner function update the outer variable. | Without it, `pre_idx += 1` would raise `UnboundLocalError`. |
| `if lo > hi: return None` | Empty range → no node. | This is the base case (an empty left or right side). |
| `root_val = preorder[pre_idx]; pre_idx += 1` | Takes the next preorder value as this subtree's root. | In preorder, a subtree's root comes before all its descendants. |
| `mid = index_of[root_val]` | Finds where the root sits in `inorder`. | Splits the range into left part `[lo, mid-1]` and right part `[mid+1, hi]`. |
| `node.left = build(lo, mid - 1)` | Builds the left subtree. | Must come **before** the right subtree, because preorder lists all left-subtree values next. |
| `node.right = build(mid + 1, hi)` | Builds the right subtree. | By now `pre_idx` points at the right subtree's root. |
| `return build(0, len(inorder) - 1)` | Builds the whole tree. | The full inorder range. |

---

## 8. Dry Run

**Input:** `preorder = [3,9,20,15,7]`, `inorder = [9,3,15,20,7]`

`index_of = {9: 0, 3: 1, 15: 2, 20: 3, 7: 4}`

| Step | Call `build(lo, hi)` | `pre_idx` before | Root value | `mid` | Next calls | Result |
|---|---|---|---|---|---|---|
| 1 | `build(0, 4)` | 0 | 3 | 1 | left `build(0, 0)`, right `build(2, 4)` | node 3 |
| 2 | `build(0, 0)` | 1 | 9 | 0 | left `build(0, -1)`, right `build(1, 0)` | node 9 |
| 3 | `build(0, -1)` | 2 | — | — | `lo > hi` | `None` (9.left) |
| 4 | `build(1, 0)` | 2 | — | — | `lo > hi` | `None` (9.right) |
| 5 | `build(2, 4)` | 2 | 20 | 3 | left `build(2, 2)`, right `build(4, 4)` | node 20 (3.right) |
| 6 | `build(2, 2)` | 3 | 15 | 2 | `build(2, 1)`, `build(3, 2)` → both `None` | node 15 (20.left) |
| 7 | `build(4, 4)` | 4 | 7 | 4 | `build(4, 3)`, `build(5, 4)` → both `None` | node 7 (20.right) |

`pre_idx` ends at 5 = `len(preorder)` — every value was used exactly once.

```text
        3
       / \
      9   20
         /  \
        15   7
```

**Result:** `[3,9,20,null,null,15,7]` ✅

**Second dry run (Example 2):** `preorder = [-1]`, `inorder = [-1]` → `build(0, 0)` takes `-1`, `mid = 0`, both children are empty ranges → `[-1]` ✅.

---

## 9. Concepts, Data Structures, and Patterns

- **Tree traversals:** preorder (root-left-right), inorder (left-root-right), postorder (left-right-root), level order — see [045_binary_tree_level_order_traversal.md](045_binary_tree_level_order_traversal.md).
- **Why two traversals?** A single traversal of values can't identify a tree. Preorder tells you **who is the root**; inorder tells you **who is on which side**. Together (with unique values) they determine the tree uniquely. Another way to make one traversal enough is to add null markers — see [046_serialize_and_deserialize_binary_tree.md](046_serialize_and_deserialize_binary_tree.md).
- **Divide and conquer:** solve for the root, split into two independent smaller problems.
- **Hash map for index lookup:** precomputing positions turns `O(n)` searches into `O(1)` lookups (same trick as [001_two_sum.md](../01_array/001_two_sum.md)).
- **Index ranges instead of slices:** avoids copying lists — a common optimisation in recursive array problems.
- **`nonlocal`:** lets a nested function modify a variable of the enclosing function.
- **Related problems:** Construct from Inorder and Postorder (LeetCode 106), Construct BST from Preorder (LeetCode 1008), Validate BST ([049_validate_binary_search_tree.md](049_validate_binary_search_tree.md)) — the inorder of a BST is sorted.

---

## 10. Complexity Analysis

Let `n` = number of nodes, `h` = tree height (`log n` if balanced, up to `n` for a chain).

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Brute force (`list.index` + slicing) | `O(n²)` worst, `O(n log n)` balanced | `O(n²)` worst | Every call scans and copies its whole piece; in a chain the pieces have sizes `n-1, n-2, …` and stay alive down the recursion path. |
| Hash map + index ranges (optimized) | `O(n)` | `O(n)` | Dictionary of `n` entries; each `build` call does `O(1)` work and there are `2n + 1` calls (`n` nodes + `n + 1` empty ranges). Recursion stack is `O(h)`, which is within `O(n)`. |
| Iterative stack | `O(n)` | `O(n)` worst (stack up to `h`) | Each node pushed and popped once; no dictionary needed. |

The output tree itself (`n` nodes) is not counted as auxiliary space.

---

## 11. Edge Cases

| Case | `preorder` | `inorder` | Expected output |
|---|---|---|---|
| Single node | `[-1]` | `[-1]` | `[-1]` |
| Two nodes, left child | `[1,2]` | `[2,1]` | `[1,2]` |
| Two nodes, right child | `[1,2]` | `[1,2]` | `[1,null,2]` |
| Left-only chain | `[1,2,3]` | `[3,2,1]` | `[1,2,null,3]` |
| Right-only chain | `[1,2,3]` | `[1,2,3]` | `[1,null,2,null,3]` |
| Extreme values | `[-3000,3000,0]` | `[3000,-3000,0]` | `[-3000,3000,0]` |
| Chain of 3000 nodes | — | — | Recursive versions need a raised recursion limit; the iterative version works as is |

---

## 12. Common Mistakes and Debugging

1. **Building the right subtree first.** With a shared `pre_idx`, you must build left before right, because preorder lists the left subtree first. Swapping them assigns roots to the wrong subtrees.
2. **Wrong slice bounds in the brute force.** The left preorder part is `preorder[1 : mid + 1]` (length `mid`), not `preorder[1 : mid]`.
3. **Using the inorder index as a preorder index.** `mid` is a position in `inorder`; in the range version it is not a position in `preorder`. Only its relation to `lo` (the size `mid - lo`) carries over.
4. **Forgetting `nonlocal`.** `pre_idx += 1` inside the nested function raises `UnboundLocalError` without it. (Alternatives: a one-element list, an iterator over `preorder`, or an instance attribute.)
5. **Building the dictionary inside the recursion.** That brings back `O(n²)`.
6. **Assuming duplicates are fine.** The method relies on unique values; with duplicates the tree may not be unique (see Q3).

**Debugging tip:** print `lo, hi, root_val, mid` at the start of every non-empty call and compare with the dry-run table. If `pre_idx` doesn't end at `n`, a range is wrong.

---

## 13. Practice Questions

**Q1. Build the tree for `preorder = [1,2,4,5,3]`, `inorder = [4,2,5,1,3]` by hand. What does LeetCode print?**

<details><summary>Hint</summary>The root is 1. In inorder, `[4,2,5]` is left of 1 and `[3]` is right.</summary></details>

**Answer:** Root 1. Left part: preorder `[2,4,5]`, inorder `[4,2,5]` → root 2 with left 4 and right 5. Right part: `[3]`. LeetCode prints `[1,2,3,4,5]`.

**Q2. Construct the tree from `inorder` and `postorder` (LeetCode 106).**

<details><summary>Hint</summary>In postorder the root is **last**. Walk the postorder list from the end, and build the **right** subtree before the left one.</summary></details>

**Answer:**

```python
def build_from_in_post(inorder, postorder):
    index_of = {value: i for i, value in enumerate(inorder)}
    post_idx = len(postorder) - 1

    def build(lo, hi):
        nonlocal post_idx
        if lo > hi:
            return None
        value = postorder[post_idx]
        post_idx -= 1
        node = TreeNode(value)
        mid = index_of[value]
        node.right = build(mid + 1, hi)   # right first: postorder read backwards is root, right, left
        node.left = build(lo, mid - 1)
        return node

    return build(0, len(inorder) - 1)


def preorder_of(node):
    return [] if node is None else [node.val] + preorder_of(node.left) + preorder_of(node.right)


root = build_from_in_post([9, 3, 15, 20, 7], [9, 15, 7, 20, 3])
assert preorder_of(root) == [3, 9, 20, 15, 7]
assert root.right.left.val == 15 and root.right.right.val == 7
```

**Q3. Why does the problem insist on unique values? Give a counter-example with duplicates.**

<details><summary>Hint</summary>Try two nodes that both have value 1.</summary></details>

**Answer:** `preorder = [1,1]`, `inorder = [1,1]` fits both "root 1 with **left** child 1" (preorder 1,1; inorder 1,1) and "root 1 with **right** child 1" (preorder 1,1; inorder 1,1). Two different trees, same traversals — so the answer would not be unique, and `index_of` would not know which `1` is meant.

```python
def traversals(node):
    if node is None:
        return [], []
    lp, li = traversals(node.left)
    rp, ri = traversals(node.right)
    return [node.val] + lp + rp, li + [node.val] + ri


left_version = TreeNode(1, TreeNode(1), None)
right_version = TreeNode(1, None, TreeNode(1))
assert traversals(left_version) == traversals(right_version) == ([1, 1], [1, 1])
```

**Q4. Can preorder + postorder always identify a binary tree?**

<details><summary>Hint</summary>Compare `[1,2]` and `[1,null,2]`.</summary></details>

**Answer:** No. Both trees have preorder `[1,2]` and postorder `[2,1]`: when a node has only one child, preorder and postorder can't tell whether it's on the left or the right. (They do identify a **full** binary tree, where every node has 0 or 2 children — LeetCode 889.)

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** Divide and conquer with a hash map of inorder indices.
- **Key idea:** `preorder[pre_idx]` is the current root; its inorder position splits the range into left and right; build left before right.
- **Time:** `O(n)` (optimized), `O(n²)` brute force.
- **Auxiliary space:** `O(n)` for the map, `O(h)` recursion stack.
- **One-line memory hook:** *"Preorder names the boss; inorder shows who stands on each side."*

### Completion checklist

- [x] Problem requirements verified
- [x] Examples and constraints verified
- [x] Beginner-friendly analogy, TreeNode primer and logic written
- [x] Brute-force solution written and tested
- [x] Optimized Python solution written and tested (`tools/tests/p048.py`), plus the iterative stack version
- [x] Line-by-line explanation written
- [x] Dry run completed with a real example
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
