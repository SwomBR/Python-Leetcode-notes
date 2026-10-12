# 049. Validate Binary Search Tree

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Validate Binary Search Tree |
| **LeetCode number** | 98 |
| **Topic (source list)** | Tree |
| **Also uses** | Binary Search Tree, DFS, Inorder Traversal |
| **Difficulty** | Medium |
| **LeetCode URL** | <https://leetcode.com/problems/validate-binary-search-tree/> |
| **Pattern** | DFS passing down an allowed `(low, high)` range; or inorder traversal must be strictly increasing |

---

## 2. Problem Explanation

### Beginner primer: `TreeNode` and LeetCode's tree lists

A binary tree is made of nodes; each node has a value `val` and two links `left` and `right` (`None` if there is no child). LeetCode provides the class as a comment:

```text
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
```

The input `root = [5,1,4,null,null,3,6]` is a **level-order list**: row by row, left to right, `null` for a missing child, trailing `null`s removed:

```text
List: [5, 1, 4, null, null, 3, 6]

        5            <- row 0
       / \
      1   4          <- row 1: children of 5
         / \
        3   6        <- children of 1: null, null ; children of 4: 3, 6
```

### What is a Binary Search Tree (BST)?

A binary tree is a **valid BST** when, for **every** node:

1. **every** value in its left subtree is **strictly smaller** than the node's value,
2. **every** value in its right subtree is **strictly larger** than the node's value,
3. and both subtrees are themselves valid BSTs.

"Every value in the subtree" — not just the direct child! — and "strictly", so **equal values are not allowed anywhere**.

### What are we given?

`root` — the root of a binary tree with at least one node.

### What must we return?

`True` if the tree is a valid BST, otherwise `False`.

### Examples

**Example 1**

```text
Input:  root = [2,1,3]
Output: true
```

```text
      2
     / \
    1   3
```

`1 < 2 < 3`, and the leaves are trivially fine.

**Example 2**

```text
Input:  root = [5,1,4,null,null,3,6]
Output: false
```

The root is 5, but its right child is 4, and 4 is not greater than 5 (tree drawn above).

### Constraints

- The number of nodes in the tree is in the range `[1, 10^4]`.
- `-2^31 <= Node.val <= 2^31 - 1`

There is no follow-up in the statement. Notice the value range: nodes can hold the **smallest and largest 32-bit integers**, which breaks some "sentinel value" tricks (see Common Mistakes).

---

## 3. Everyday Analogy

> **Explain it like I'm five**

Imagine a library where every shelf has a sign, and the rule is: "Books with smaller numbers go **left**, bigger numbers go **right**." When you walk left from a shelf labelled 50, you are promising that **everything** from now on is below 50. If you then walk right from a shelf labelled 30, everything there must be **between 30 and 50**.

So as you walk down, you carry a little card that says *"allowed numbers: from ___ to ___"*. At each shelf you check the number is inside the card's range (not equal to the edges!), then you hand a **narrower card** to each side. If any shelf breaks its card's rule, the library is badly organized.

---

## 4. Step-by-Step Logic

1. **The tempting idea is wrong.** Checking only `node.left.val < node.val < node.right.val` misses grandchildren. In `[5,4,6,null,null,3,7]` every parent–child pair looks fine, but `3` is in the **right** subtree of `5` and is smaller than 5.

   ```text
         5
        / \
       4   6
          / \
         3   7      <- 3 < 5, but it sits on 5's right side: invalid
   ```

2. **What does a node really need to satisfy?** Every ancestor imposes a limit. Going **left** from an ancestor `a` adds "must be `< a`"; going **right** adds "must be `> a`". All these limits combine into one open interval `(low, high)`.
3. **Pass the interval down.** The root may be anything: `(-∞, +∞)`. For a node with value `v` and interval `(low, high)`:
   - check `low < v < high` (strict on both sides — equal values are invalid);
   - the left child gets `(low, v)`; the right child gets `(v, high)`.
4. **Any failure → `False`.** If every node passes, the tree is a valid BST.
5. **Equivalent view:** a tree is a valid BST **exactly when its inorder traversal (left, node, right) is strictly increasing**. That gives a second linear-time method.
6. **Use real infinities, not 32-bit sentinels.** Python's `float("-inf")`/`float("inf")` (or `None` meaning "no limit") never collide with an actual node value like `-2^31`.

---

## 5. Brute-Force Solution

### Algorithm

Use the definition literally: for every node, collect **all** values in its left subtree and **all** values in its right subtree, and check that they are all strictly smaller / strictly larger. Then repeat for every node.

### Python code

```python
from typing import Optional


class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        def all_values(node):
            """Every value in the subtree rooted at node (iterative DFS)."""
            values, stack = [], [node]
            while stack:
                cur = stack.pop()
                if cur is not None:
                    values.append(cur.val)
                    stack.append(cur.left)
                    stack.append(cur.right)
            return values

        stack = [root]
        while stack:                      # visit every node
            node = stack.pop()
            if node is None:
                continue
            if any(v >= node.val for v in all_values(node.left)):
                return False
            if any(v <= node.val for v in all_values(node.right)):
                return False
            stack.append(node.left)
            stack.append(node.right)
        return True
```

### Explanation

- `all_values` lists the whole subtree below a child.
- For each node we check the definition directly: all left values `< node.val`, all right values `> node.val`. Using `>=` / `<=` in the failure tests enforces the "strictly" rule.
- Iterative stacks are used, so even a 10^4-node chain causes no recursion problems.

### Complexity

- **Time:** each node's value is collected once for **every ancestor** it has, so the total work is the sum of all node depths: `O(n · h)`. For a chain that's about `n²/2` = 50 million steps when `n = 10^4` — too slow in Python. For a balanced tree it's `O(n log n)`.
- **Auxiliary space:** `O(n)` for the value lists and stacks.
- **Trade-off:** obviously correct (it *is* the definition), but repeats work that the range method does in one pass.

---

## 6. Optimized Solution

### Idea

DFS that passes the allowed open interval `(low, high)` down the tree. Each node is checked exactly once against **all** of its ancestors' limits at the same time.

### Algorithm

1. `valid(node, low, high)`:
   - if `node` is `None` → `True` (an empty tree is a valid BST);
   - if not `low < node.val < high` → `False`;
   - return `valid(node.left, low, node.val) and valid(node.right, node.val, high)`.
2. Answer: `valid(root, -∞, +∞)`.

### Python code (LeetCode-ready)

```python
from typing import Optional


class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        def valid(node, low, high):
            if node is None:
                return True
            if not (low < node.val < high):          # strict on both sides
                return False
            return (valid(node.left, low, node.val) and
                    valid(node.right, node.val, high))

        return valid(root, float("-inf"), float("inf"))
```

### Alternative: iterative inorder traversal (no recursion limit)

```python
from typing import Optional


class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        stack = []
        prev = None                 # value of the previously visited node
        node = root
        while stack or node:
            while node:             # go as far left as possible
                stack.append(node)
                node = node.left
            node = stack.pop()
            if prev is not None and node.val <= prev:
                return False        # inorder must be strictly increasing
            prev = node.val
            node = node.right
        return True
```

`prev = None` (instead of a number like `-2^31`) means "nothing visited yet", so a tree whose smallest value is exactly `-2^31` is handled correctly.

### Recursion depth — an honest note

The recursive `valid` goes as deep as the tree's height. The constraints allow 10^4 nodes, so a chain needs about 10^4 nested calls, while CPython's default recursion limit is 1000. Don't rely on the judge raising it; the iterative inorder version above (or `sys.setrecursionlimit(20000)`) is the safe choice for very deep trees.

---

## 7. Line-by-Line Explanation

(Recursive range version.)

| Line | What it does | Why |
|---|---|---|
| `def valid(node, low, high):` | Checks the subtree at `node`, where every value must lie strictly between `low` and `high`. | `low`/`high` summarise the rules of **all** ancestors, not just the parent. |
| `if node is None: return True` | An empty subtree is valid. | Base case of the recursion. |
| `if not (low < node.val < high): return False` | The node breaks some ancestor's rule (or equals a limit). | Strict `<` on both sides implements "strictly less / strictly greater". |
| `valid(node.left, low, node.val)` | Left subtree: keep the old lower limit, new upper limit is this node. | Everything on the left must be smaller than this node **and** still respect older limits. |
| `valid(node.right, node.val, high)` | Right subtree: new lower limit is this node, keep the old upper limit. | Mirror of the left case. |
| `and` | Stops early if the left side already failed. | Saves work; the answer is already `False`. |
| `valid(root, float("-inf"), float("inf"))` | Starts with no limits. | Infinities are smaller/larger than every integer, including `-2^31` and `2^31 - 1`. Python compares `int` and `float` correctly. |

---

## 8. Dry Run

**Input:** Example 2, `root = [5,1,4,null,null,3,6]`

| Step | Call | `low` | `high` | `node.val` | `low < val < high`? | Result |
|---|---|---|---|---|---|---|
| 1 | `valid(5, -inf, inf)` | -inf | inf | 5 | Yes | check left, then right |
| 2 | `valid(1, -inf, 5)` | -inf | 5 | 1 | Yes | check children |
| 3 | `valid(None, -inf, 1)` | — | — | — | — | `True` |
| 4 | `valid(None, 1, 5)` | — | — | — | — | `True` → node 1 is valid |
| 5 | `valid(4, 5, inf)` | 5 | inf | 4 | **No** (`5 < 4` is false) | `False` |

The `and` in step 1 receives `True and False` → **`false`** ✅. Nodes 3 and 6 are never visited.

**Example 1:** `[2,1,3]` → `valid(2,-inf,inf)` ✓, `valid(1,-inf,2)` ✓, `valid(3,2,inf)` ✓, all `None` children `True` → **`true`** ✅.

### Second dry run: the "grandchild" trap `[5,4,6,null,null,3,7]`

| Step | Call | Interval | `val` | Inside? | Result |
|---|---|---|---|---|---|
| 1 | `valid(5, -inf, inf)` | (-inf, inf) | 5 | Yes | continue |
| 2 | `valid(4, -inf, 5)` | (-inf, 5) | 4 | Yes | leaf → `True` |
| 3 | `valid(6, 5, inf)` | (5, inf) | 6 | Yes | continue |
| 4 | `valid(3, 5, 6)` | (5, 6) | 3 | **No** | `False` |

A "compare with direct children only" solution would accept this tree (4 < 5 < 6 and 3 < 6 < 7), but the range method correctly rejects it.

---

## 9. Concepts, Data Structures, and Patterns

- **BST property:** left subtree < node < right subtree, for **every** node. Searching, inserting and finding the k-th smallest all rely on it — see [050_kth_smallest_element_in_a_bst.md](050_kth_smallest_element_in_a_bst.md) and [051_lowest_common_ancestor_of_bst.md](051_lowest_common_ancestor_of_bst.md).
- **Passing information down (top-down DFS):** each call receives constraints from its ancestors. Compare with bottom-up DFS that returns information upward, as in [041_maximum_depth_of_binary_tree.md](041_maximum_depth_of_binary_tree.md) and [044_binary_tree_maximum_path_sum.md](044_binary_tree_maximum_path_sum.md).
- **Inorder traversal of a BST is sorted.** This single fact gives the alternative solution, and powers 050 as well.
- **Iterative inorder with a stack:** "go left as far as possible, pop, visit, go right".
- **Sentinels vs. infinities:** prefer `float("inf")` or `None` over magic numbers when the input range includes the extreme integers.

---

## 10. Complexity Analysis

Let `n` = number of nodes, `h` = tree height (`log n` balanced, up to `n` for a chain).

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Brute force (check every subtree's values) | `O(n · h)`, i.e. `O(n²)` worst | `O(n)` | Each value is re-collected once per ancestor. |
| Range DFS (optimized) | `O(n)` | `O(h)` | Each node is checked once with `O(1)` work; recursion stack depth is the height. |
| Iterative inorder | `O(n)` | `O(h)` | Each node is pushed and popped once; the stack holds at most one root-to-leaf path. Stops early at the first violation. |

---

## 11. Edge Cases

| Case | Tree | Expected | Why |
|---|---|---|---|
| Single node | `[1]` | `true` | No children, nothing to violate. |
| Smallest 32-bit value alone | `[-2147483648]` | `true` | `-inf < -2^31 < inf`; a sentinel of `-2^31` with `<` would wrongly fail. |
| Largest 32-bit value alone | `[2147483647]` | `true` | Same reason with `+inf`. |
| Both extremes | `[-2147483648,null,2147483647]` | `true` | Right child is greater. |
| Equal left child | `[1,1]` | `false` | Must be strictly smaller. |
| Equal right child | `[1,null,1]` | `false` | Must be strictly greater. |
| Equal extremes | `[2147483647,2147483647]` | `false` | Duplicates invalid even at the limit. |
| Grandchild breaks an ancestor's rule | `[5,4,6,null,null,3,7]` | `false` | 3 is in 5's right subtree. |
| Grandchild on the left side | `[3,1,5,0,4]` | `false` | 4 is in 3's left subtree but 4 > 3. |
| Perfect valid BST | `[3,1,5,0,2,4,6]` | `true` | Inorder `0..6` strictly increasing. |

---

## 12. Common Mistakes and Debugging

1. **Only comparing a node with its direct children.** Accepts `[5,4,6,null,null,3,7]`. The limits from **all** ancestors matter.
2. **Allowing equal values.** Using `<=` instead of `<` (or `>=` instead of `>`) accepts `[1,1]`. The statement requires *strictly* less/greater.
3. **Using 32-bit sentinels.** Starting with `low = -2**31`, `high = 2**31 - 1` and checking `low < val < high` rejects the valid single-node tree `[-2147483648]`. Use infinities or `None`.
4. **Initialising `prev` to a number in the inorder method.** `prev = -2**31` fails on a tree whose first inorder value is `-2^31`. Use `None` or `-inf`.
5. **Passing the wrong limit down.** The left child must get `(low, node.val)` — keep `low`! Writing `(-inf, node.val)` forgets the ancestors' lower bound.
6. **Returning `True` too early** (e.g. `return valid(left)` without also checking the right side).

**Debugging tip:** print `node.val, low, high` in each call; the first line where the value is outside its interval is the culprit.

---

## 13. Practice Questions

**Q1. Is `[10,5,15,null,null,6,20]` a valid BST? Trace the intervals.**

<details><summary>Hint</summary>What interval does the node 6 receive?</summary></details>

**Answer:** No. 10 gets `(-inf, inf)`, 15 gets `(10, inf)`, and 6 (left child of 15) gets `(10, 15)`. Since `6 < 10`, it's outside → `false`. Note 6 < 15 alone looks fine — that's the direct-children trap.

**Q2. A variant allows duplicates, but only in the left subtree (left `<=` node `<` right). Adjust the range check.**

<details><summary>Hint</summary>The upper limit becomes inclusive, the lower limit stays exclusive.</summary></details>

**Answer:** Each node needs `low < val <= high`, with the left child getting `(low, val]` and the right child `(val, high]`.

```python
def is_bst_left_duplicates(root):
    def valid(node, low, high):
        if node is None:
            return True
        if not (low < node.val <= high):
            return False
        return valid(node.left, low, node.val) and valid(node.right, node.val, high)

    return valid(root, float("-inf"), float("inf"))


assert is_bst_left_duplicates(TreeNode(2, TreeNode(2), TreeNode(3))) is True
assert is_bst_left_duplicates(TreeNode(2, None, TreeNode(2))) is False
assert is_bst_left_duplicates(TreeNode(5, None, TreeNode(6, TreeNode(5)))) is False
```

**Q3. Two values of a valid BST were swapped by mistake (LeetCode 99 idea). Find which two values were swapped.**

<details><summary>Hint</summary>Look at the inorder list: it is sorted except at one or two "drops" where a value is bigger than the next one.</summary></details>

**Answer:** The first wrong value is the larger element of the **first** drop; the second wrong value is the smaller element of the **last** drop.

```python
def find_swapped(root):
    order, stack, node = [], [], root
    while stack or node:
        while node:
            stack.append(node)
            node = node.left
        node = stack.pop()
        order.append(node.val)
        node = node.right
    drops = [i for i in range(len(order) - 1) if order[i] > order[i + 1]]
    first = order[drops[0]]
    second = order[drops[-1] + 1]
    return sorted((first, second))


# Correct BST [2,1,3] with 1 and 3 swapped -> [2,3,1]
assert find_swapped(TreeNode(2, TreeNode(3), TreeNode(1))) == [1, 3]
# Correct BST [2,1,4,null,null,3] with 2 and 3 swapped -> [3,1,4,null,null,2]
# inorder 1,3,2,4 has a single drop (adjacent swap)
assert find_swapped(TreeNode(3, TreeNode(1), TreeNode(4, TreeNode(2)))) == [2, 3]
```

**Q4. Why does an inorder traversal that is strictly increasing prove the tree is a valid BST?**

<details><summary>Hint</summary>Where do the left-subtree values of a node appear in the inorder list?</summary></details>

**Answer:** In inorder, the whole left subtree of a node appears **immediately before** it and the whole right subtree **immediately after** it. If the list is strictly increasing, every left-subtree value is before (so smaller than) the node and every right-subtree value is after (so larger than) it — for every node. That is exactly the BST definition. Conversely, a valid BST always produces a strictly increasing inorder list.

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** Top-down DFS with an allowed open interval `(low, high)`; or inorder must be strictly increasing.
- **Key idea:** Every ancestor adds a limit; left child gets `(low, val)`, right child gets `(val, high)`; equal values are invalid.
- **Time:** `O(n)`.
- **Auxiliary space:** `O(h)`.
- **Watch out:** values reach `-2^31` and `2^31 - 1` — use infinities or `None`, never those numbers as sentinels.
- **One-line memory hook:** *"Carry the allowed range down the tree and keep narrowing it."*

### Completion checklist

- [x] Problem requirements verified
- [x] Examples and constraints verified
- [x] Beginner-friendly analogy, TreeNode primer and logic written
- [x] Brute-force solution written and tested
- [x] Optimized Python solution written and tested (`tools/tests/p049.py`), plus the iterative inorder version, including integer-limit cases
- [x] Line-by-line explanation written
- [x] Dry run completed with a real example
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
