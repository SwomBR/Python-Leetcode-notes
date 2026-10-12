# 042. Same Tree

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Same Tree |
| **LeetCode number** | 100 |
| **Topic (source list)** | Tree |
| **Also uses** | Depth-First Search, Breadth-First Search, Recursion |
| **Difficulty** | Easy |
| **LeetCode URL** | <https://leetcode.com/problems/same-tree/> |
| **Pattern** | Walk two trees in lockstep (paired recursion) |

---

## 2. Problem Explanation

### Beginner primer: what is a `TreeNode`?

A **binary tree** is built from **nodes**. Each node has a value `val`, a `left` child and a `right` child; a missing child is `None`. LeetCode shows the class as a comment — it is already defined for you:

```text
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
```

### How LeetCode's list input becomes a tree

Trees are written as **level-order lists**: top row first, each row left to right, `null` for a missing child, and each real node takes the next two list items as its (left, right) children. For example `[1,null,2]` means "root 1, no left child, right child 2", and `[3,9,20,null,null,15,7]` is:

```text
        3
       / \
      9   20
         /  \
        15   7
```

(`9` uses the two `null`s, then `20` gets `15` and `7`.)

### What are we given?

Two roots, `p` and `q`. Either (or both) may be `None` (an empty tree).

### What must we return?

`True` if the two trees are **the same**, otherwise `False`. "The same" means **both**:

1. **Same shape** — wherever one tree has a node, the other has a node in the exact same position (same left/right choices from the root), and wherever one has `None`, so does the other.
2. **Same values** — the nodes in matching positions hold equal values.

Two empty trees count as the same.

### Examples

**Example 1**

```text
Input:  p = [1,2,3], q = [1,2,3]
Output: true
```

```text
    p:  1        q:  1
       / \          / \
      2   3        2   3
```

Same shape, same values everywhere.

**Example 2**

```text
Input:  p = [1,2], q = [1,null,2]
Output: false
```

```text
    p:  1        q:  1
       /              \
      2                2
```

The values are the same, but `2` hangs on the **left** in `p` and on the **right** in `q`. Different shape → not the same.

**Example 3**

```text
Input:  p = [1,2,1], q = [1,1,2]
Output: false
```

```text
    p:  1        q:  1
       / \          / \
      2   1        1   2
```

Same shape, but the left children are `2` vs `1`. Different values → not the same.

### Constraints

- The number of nodes in both trees is in the range `[0, 100]`.
- `-10^4 <= Node.val <= 10^4`

There is no follow-up for this problem.

---

## 3. Everyday Analogy

> **Explain it like I'm five**

Two friends each built a LEGO tower that branches like a tree, and you want to know whether they built **exactly the same thing**.

You put one finger on the top block of each tower. Are both blocks there? Same color? Good. Now move **both** fingers to the left branch together and check again, then do the same on the right branch. If at any moment one finger touches a block and the other touches empty air, or the colors differ, you shout "Different!" and stop.

If you have checked every matching spot and never found a difference, the towers are the same.

---

## 4. Step-by-Step Logic

1. **Compare position by position.** Two trees are equal exactly when their roots match **and** their left subtrees are equal **and** their right subtrees are equal. That is a recursive definition.
2. **Handle the `None` cases first** (otherwise `p.val` crashes on `None`):
   - both `None` → this position is empty in both trees → equal (`True`);
   - exactly one `None` → shapes differ → `False`.
3. **Both real nodes:** if `p.val != q.val` → `False`.
4. **Recurse:** `same(p.left, q.left) and same(p.right, q.right)`. Python's `and` short-circuits, so the right side is skipped if the left side already failed.
5. **Early exit:** the first difference anywhere ends the whole search.

---

## 5. Brute-Force Solution

### Algorithm

Turn each tree into a flat list (**serialize** it) using a preorder traversal that writes a `None` marker for every missing child, then compare the two lists.

The null markers are essential. Without them, `[1,2]` and `[1,null,2]` both serialize to `1, 2` in preorder, even though their shapes differ (Example 2). With markers they become `1, 2, None, None, None` and `1, None, 2, None, None`.

### Python code

```python
from typing import Optional


class Solution:
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        def serialize(node: Optional[TreeNode], out: list) -> None:
            if node is None:
                out.append(None)          # null marker records the shape
                return
            out.append(node.val)          # preorder: node, left, right
            serialize(node.left, out)
            serialize(node.right, out)

        first, second = [], []
        serialize(p, first)
        serialize(q, second)
        return first == second
```

### Explanation

- A preorder sequence **with null markers** describes a binary tree uniquely: reading it back, every value says "make a node here" and every `None` says "nothing here". So equal sequences ⇔ equal trees.
- We store values as list items (not glued into a string), so `12, 3` can never be confused with `1, 23`.

### Complexity

- **Time:** `O(n + m)` where `n`, `m` are the node counts. The asymptotic time equals the optimized version, but it is still wasteful: it **always** serializes both trees completely, even when the roots already differ, and then compares the lists in a second pass.
- **Auxiliary space:** `O(n + m)` for the two lists (each has `2·size + 1` entries) plus `O(h)` recursion stack. The optimized solution needs no lists at all.

---

## 6. Optimized Solution

### Idea

Walk both trees **at the same time**, comparing matching positions, and stop at the first difference.

### Algorithm (recursive DFS)

1. If `p` and `q` are both `None`, return `True`.
2. If only one is `None`, return `False`.
3. If `p.val != q.val`, return `False`.
4. Return `isSameTree(p.left, q.left) and isSameTree(p.right, q.right)`.

### Python code (LeetCode-ready, recursive DFS)

```python
from typing import Optional


class Solution:
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        if p is None and q is None:       # both empty here: match
            return True
        if p is None or q is None:        # only one empty: shapes differ
            return False
        if p.val != q.val:                # same position, different value
            return False
        return (self.isSameTree(p.left, q.left)
                and self.isSameTree(p.right, q.right))
```

### Python code (iterative BFS over pairs)

```python
from collections import deque
from typing import Optional


class Solution:
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        queue = deque([(p, q)])           # pairs of nodes in matching positions
        while queue:
            a, b = queue.popleft()
            if a is None and b is None:
                continue
            if a is None or b is None or a.val != b.val:
                return False
            queue.append((a.left, b.left))
            queue.append((a.right, b.right))
        return True
```

Replacing `deque`/`popleft` with a list used as a stack (`pop()`) gives an iterative DFS with the same result.

### Recursion limit — is the recursive version safe?

Each tree has at most 100 nodes, so the height is at most 100 and the recursion is at most about 101 calls deep. Python's default recursion limit is 1000, so the recursive version is **completely safe** for these constraints, on LeetCode and anywhere else.

---

## 7. Line-by-Line Explanation

(Recursive DFS)

| Line | What it does | Why |
|---|---|---|
| `if p is None and q is None: return True` | Both positions empty. | Nothing to compare; the shapes agree here. Also the base case of the recursion. |
| `if p is None or q is None: return False` | Exactly one is empty (the previous line ruled out "both"). | One tree has a node where the other has none → different shape. Must come **before** reading `.val`. |
| `if p.val != q.val: return False` | Compares the values at this position. | Same position, different value → different trees. |
| `return (self.isSameTree(p.left, q.left) and ...)` | Compares the left subtrees, then the right subtrees. | Equal trees need both pairs of subtrees equal. `and` short-circuits, so a left mismatch skips the right side. |

(Iterative BFS)

| Line | What it does | Why |
|---|---|---|
| `queue = deque([(p, q)])` | Starts with the pair of roots. | We always move through the trees in pairs. |
| `if a is None and b is None: continue` | Skips matching empty spots. | Not a difference, nothing to expand. |
| `if a is None or b is None or a.val != b.val: return False` | Any structural or value mismatch. | Thanks to short-circuiting, `a.val` is only read when both are real. |
| `queue.append((a.left, b.left))` / `(a.right, b.right)` | Schedules the matching child pairs. | Left goes with left, right with right. |
| `return True` | Queue emptied with no mismatch. | Every position matched. |

---

## 8. Dry Run

**Input (Example 2):** `p = [1,2]`, `q = [1,null,2]` (recursive DFS)

| Step | Call | `p` node | `q` node | Check that decides | Returns |
|---|---|---|---|---|---|
| 1 | `isSameTree(p=1, q=1)` | 1 | 1 | both real, `1 == 1` → recurse left | (waits) |
| 2 | `isSameTree(p.left, q.left)` | 2 | `None` | exactly one is `None` | `False` |
| 3 | back in step 1 | | | `False and ...` short-circuits; right side never called | `False` |

**Result:** `false` ✅

**Example 1:** `p = [1,2,3]`, `q = [1,2,3]`

| Step | Pair compared | Result |
|---|---|---|
| 1 | (1, 1) | values equal → check children |
| 2 | (2, 2) | equal → children `(None, None)` twice → `True` |
| 3 | (3, 3) | equal → children `(None, None)` twice → `True` |
| 4 | back at root | `True and True` → `True` |

**Result:** `true` ✅

**Example 3** (BFS version): `p = [1,2,1]`, `q = [1,1,2]`

| Pop | Pair `(a, b)` | Decision | Queue afterwards |
|---|---|---|---|
| 1 | (1, 1) | equal, enqueue children | `[(2,1), (1,2)]` |
| 2 | (2, 1) | `2 != 1` → return `False` | — |

**Result:** `false` ✅

---

## 9. Concepts, Data Structures, and Patterns

- **Paired traversal:** two pointers that move through two structures in lockstep — the tree version of comparing two lists element by element.
- **Recursion with multiple base cases:** handle every combination of `None` before touching attributes.
- **Short-circuit evaluation:** `and` / `or` stop as soon as the answer is known, which gives early exit for free.
- **Serialization:** preorder with null markers uniquely encodes a binary tree (used by the brute force). The full idea is developed in [046_serialize_and_deserialize_binary_tree.md](046_serialize_and_deserialize_binary_tree.md).
- **BFS with `collections.deque`:** the queue holds pairs instead of single nodes.
- **Related notes in this project:**
  - [047_subtree_of_another_tree.md](047_subtree_of_another_tree.md) calls a same-tree check at every node of the bigger tree.
  - [043_invertflip_binary_tree.md](043_invertflip_binary_tree.md) — mirror comparison (Symmetric Tree, Q2 below) is "same tree, but left pairs with right".
  - [041_maximum_depth_of_binary_tree.md](041_maximum_depth_of_binary_tree.md) — the same "visit both children" recursion skeleton.

---

## 10. Complexity Analysis

Let `n` and `m` be the node counts of `p` and `q`, and `h` the height.

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Serialize and compare (brute force) | `O(n + m)` | `O(n + m)` | Both trees fully serialized into lists, then compared. No early exit. |
| Recursive paired DFS | `O(min(n, m))` | `O(min(h_p, h_q))` — best `O(log n)` (balanced), worst `O(n)` (skewed) | Every pair of real nodes compared exists in **both** trees, so at most `min(n, m)` such pairs; stops at the first mismatch. The stack holds one frame per level of the current path. |
| Iterative BFS | `O(min(n, m))` | `O(w)`, `w` = widest level compared (up to about `n/2`) | Queue holds pairs from at most about two levels. |

With at most 100 nodes all of these are instant; the difference is about clean technique, early exit, and memory.

---

## 11. Edge Cases

| Case | Example | Expected result | Why |
|---|---|---|---|
| Both empty | `p = []`, `q = []` | `true` | Two empty trees are identical. |
| One empty | `p = [1]`, `q = []` | `false` | Shape differs at the root. |
| Single nodes, different values | `p = [1]`, `q = [2]` | `false` | Values differ. |
| Same values, mirrored shape | `p = [1,2]`, `q = [1,null,2]` | `false` | Official example 2. |
| Same shape, swapped values | `p = [1,2,1]`, `q = [1,1,2]` | `false` | Official example 3. |
| Digit-gluing trap | `p = [12,3]`, `q = [1,23]` | `false` | A serialization without separators would make both `"123"`. |
| Difference deep down | `p = [1,null,2,3]`, `q = [1,null,2,null,3]` | `false` | `3` is the left child of `2` in `p` but the right child in `q`. |
| Zero values | `p = [0]`, `q = [0]` | `true` | Use `is None`, not truthiness — a node with value 0 is still a real node. |

---

## 12. Common Mistakes and Debugging

1. **Reading `.val` before checking for `None`.** `if p.val != q.val` crashes with `AttributeError` when one side is `None`. Do the two `None` checks first.
2. **Only checking "both None" or only "one None".** You need both checks; the order "both None → True" then "either None → False" is the cleanest.
3. **Testing truthiness of values.** `if not p.val` treats a node with value `0` as missing. Check the node (`p is None`), never the value.
4. **Comparing traversals without null markers.** Plain preorder or inorder lists cannot tell `[1,2]` from `[1,null,2]`.
5. **Comparing nodes with `==` or `is`.** `p == q` compares object identity for `TreeNode` (no `__eq__` defined), so two identical-looking trees built separately are "not equal". Compare values and recurse.
6. **Pairing left with right.** That's the Symmetric Tree check, not Same Tree.

**Debugging tip:** print `(p.val if p else None, q.val if q else None)` at the start of each call to see exactly which pair produced `False`.

---

## 13. Practice Questions

**Q1. Why does comparing plain preorder traversals (no null markers) fail? Give a counterexample.**

<details><summary>Hint</summary>Look at official Example 2.</summary></details>

**Answer:** `p = [1,2]` and `q = [1,null,2]` both have preorder `[1, 2]`, but the trees differ. Without null markers, the traversal loses the information "left or right". With markers they become `[1, 2, None, None, None]` and `[1, None, 2, None, None]`.

```python
def preorder(node, markers):
    if node is None:
        return [None] if markers else []
    return [node.val] + preorder(node.left, markers) + preorder(node.right, markers)


p = TreeNode(1, TreeNode(2))
q = TreeNode(1, None, TreeNode(2))
assert preorder(p, False) == preorder(q, False) == [1, 2]       # fooled
assert preorder(p, True) != preorder(q, True)                     # correct
```

**Q2. Symmetric Tree (LeetCode 101): is a tree a mirror image of itself?**

<details><summary>Hint</summary>Same as Same Tree, but compare `a.left` with `b.right` and `a.right` with `b.left`.</summary></details>

**Answer:**

```python
def is_symmetric(root):
    def mirror(a, b):
        if a is None and b is None:
            return True
        if a is None or b is None or a.val != b.val:
            return False
        return mirror(a.left, b.right) and mirror(a.right, b.left)
    return root is None or mirror(root.left, root.right)


sym = TreeNode(1, TreeNode(2, TreeNode(3), TreeNode(4)), TreeNode(2, TreeNode(4), TreeNode(3)))
assert is_symmetric(sym) is True
assert is_symmetric(TreeNode(1, TreeNode(2, None, TreeNode(3)), TreeNode(2, None, TreeNode(3)))) is False
```

**Q3. Subtree of Another Tree (LeetCode 572): does `root` contain a subtree identical to `sub_root`?**

<details><summary>Hint</summary>Try a same-tree check starting at every node of `root`.</summary></details>

**Answer:** `O(n · m)` in the worst case. See [047_subtree_of_another_tree.md](047_subtree_of_another_tree.md) for faster ideas.

```python
def same(a, b):
    if a is None or b is None:
        return a is b
    return a.val == b.val and same(a.left, b.left) and same(a.right, b.right)


def is_subtree(root, sub_root):
    if root is None:
        return sub_root is None
    return same(root, sub_root) or is_subtree(root.left, sub_root) or is_subtree(root.right, sub_root)


big = TreeNode(3, TreeNode(4, TreeNode(1), TreeNode(2)), TreeNode(5))
assert is_subtree(big, TreeNode(4, TreeNode(1), TreeNode(2))) is True
big.left.right.left = TreeNode(0)
assert is_subtree(big, TreeNode(4, TreeNode(1), TreeNode(2))) is False
```

(`a is b` when at least one is `None` is `True` only if both are `None` — a compact version of the two `None` checks.)

**Q4. Flip Equivalent (LeetCode 951): trees are equal if you may swap the children of any nodes. Check it.**

<details><summary>Hint</summary>At each pair, the children may match straight or crossed.</summary></details>

**Answer:**

```python
def flip_equiv(a, b):
    if a is None or b is None:
        return a is b
    if a.val != b.val:
        return False
    return ((flip_equiv(a.left, b.left) and flip_equiv(a.right, b.right))
            or (flip_equiv(a.left, b.right) and flip_equiv(a.right, b.left)))


assert flip_equiv(TreeNode(1, TreeNode(2), TreeNode(3)), TreeNode(1, TreeNode(3), TreeNode(2))) is True
assert flip_equiv(TreeNode(1, TreeNode(2)), TreeNode(1, TreeNode(3))) is False
```

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** Paired DFS over two trees.
- **Key idea:** both `None` → `True`; one `None` → `False`; values differ → `False`; else recurse left-with-left **and** right-with-right.
- **Time:** `O(min(n, m))`.
- **Auxiliary space:** `O(h)` recursion (`O(log n)` balanced, `O(n)` skewed); at most ~100 frames here, so recursion is safe.
- **One-line memory hook:** *"Two fingers, same moves, stop at the first difference."*

### Completion checklist

- [x] Problem requirements verified
- [x] Examples and constraints verified
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force solution written and tested
- [x] Optimized Python solutions (recursive and BFS) written and tested (`tools/tests/p042.py`)
- [x] Line-by-line explanation written
- [x] Dry run completed with a real example
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
