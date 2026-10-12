# 047. Subtree of Another Tree

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Subtree of Another Tree |
| **LeetCode number** | 572 |
| **Topic (source list)** | Tree |
| **Also uses** | DFS, String Matching (KMP), Hashing / Serialization |
| **Difficulty** | Easy |
| **LeetCode URL** | <https://leetcode.com/problems/subtree-of-another-tree/> |
| **Pattern** | "Same tree" check at every node; or serialize both trees and do substring search |

---

## 2. Problem Explanation

### Beginner primer: `TreeNode` and LeetCode's tree lists

A binary tree is built from nodes. Each node has a value `val` and two links, `left` and `right`, which are `None` when the child is missing. LeetCode provides this class as a comment (you don't write it):

```text
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
```

LeetCode writes a tree as a **level-order list**: row by row, left to right, with `null` for a missing child and trailing `null`s removed. For `root = [3,4,5,1,2,null,null,null,null,0]`:

```text
List:  [3, 4, 5, 1, 2, null, null, null, null, 0]

            3            <- row 0: 3
          /   \
         4     5         <- row 1: 4, 5
        / \
       1   2             <- children of 4: 1, 2 ; children of 5: null, null
          /
         0               <- children of 1: null, null ; children of 2: 0 (right child omitted)
```

### What are we given?

- `root` — the root of a binary tree (the "big" tree).
- `subRoot` — the root of another binary tree (the "pattern").

### What must we return?

`True` if some node of `root`, **together with all of that node's descendants**, looks **exactly** like `subRoot` (same shape and same values everywhere); otherwise `False`.

### The rules

1. A **subtree** starts at some node and includes **everything below it** — you are not allowed to cut off part of it. So if the matching node in `root` has extra children further down that `subRoot` doesn't have, it is **not** a match (that is exactly Example 2).
2. The whole tree `root` counts as a subtree of itself.
3. Both trees are non-empty (see constraints).

### Examples

**Example 1**

```text
Input:  root = [3,4,5,1,2], subRoot = [4,1,2]
Output: true
```

```text
   root:        3           subRoot:     4
              /   \                     / \
             4     5                   1   2
            / \
           1   2
```

The node `4` in `root`, with its children `1` and `2`, is identical to `subRoot`.

**Example 2**

```text
Input:  root = [3,4,5,1,2,null,null,null,null,0], subRoot = [4,1,2]
Output: false
```

The node `4` looks right at first, but its child `2` has an extra child `0`. The subtree rooted at `4` is `4 → (1, 2 → 0)`, which is not identical to `subRoot`. No other node matches either.

### Constraints

- The number of nodes in the `root` tree is in the range `[1, 2000]`.
- The number of nodes in the `subRoot` tree is in the range `[1, 1000]`.
- `-10^4 <= root.val <= 10^4`
- `-10^4 <= subRoot.val <= 10^4`

There is no follow-up in the statement.

---

## 3. Everyday Analogy

> **Explain it like I'm five**

You have a huge family tree poster and a small photo of one branch of a family: grandma, her two kids, and nobody else. You want to know: *"Is this exact branch somewhere on the big poster?"*

The simple way: put your finger on each person on the poster, one at a time, and ask "If I start here, does everything below match my small photo **exactly** — same people, same places, nobody extra?"

The clever way: write both family trees out as a **sentence**, using a fixed reading order and writing "nobody" for empty spots. Then just check whether the small sentence appears inside the big sentence. But be careful with how you write names: if you write them without spaces, "Al" + "Ice" could look like "Alice"! So you put a clear separator before every name.

---

## 4. Step-by-Step Logic

1. **Break the problem in two.** "Is `subRoot` a subtree of `root`?" = "Is there **some** node in `root` where the tree starting there is **the same tree** as `subRoot`?"
2. **Same-tree check** (LeetCode 100, [042_same_tree.md](042_same_tree.md)): two trees are the same if both are empty, or both roots have equal values **and** their left subtrees are the same **and** their right subtrees are the same.
3. **Try every node.** Visit every node of `root` and run the same-tree check there. Stop at the first success. That's the straightforward `O(m · n)` solution.
4. **Can we avoid repeated comparisons?** Turn each tree into a string with a fixed traversal (preorder) and **null markers**. Two trees are identical exactly when their strings are identical (see [046_serialize_and_deserialize_binary_tree.md](046_serialize_and_deserialize_binary_tree.md)), and the string of a subtree is a **contiguous piece** of the big string, because preorder writes a node and then its whole subtree in one block.
5. **Delimiters are essential.** Without separators, the tree `[12]` written as `12,#,#` contains `2,#,#` (the tree `[2]`) — a false match. Writing a comma **before** every token (`,12,#,#` vs `,2,#,#`) means a match can only begin at the start of a token.
6. **Search fast.** Use a linear-time substring search (KMP) so the whole algorithm is `O(m + n)`.

---

## 5. Brute-Force Solution

### Algorithm

1. If `root` is `None`, there is nothing to match → `False`.
2. If the tree starting at `root` is the same as `subRoot` → `True`.
3. Otherwise try `root.left` and `root.right` recursively.

### Python code

```python
from typing import Optional


class Solution:
    def isSubtree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
        def same(a, b):
            if a is None and b is None:
                return True
            if a is None or b is None or a.val != b.val:
                return False
            return same(a.left, b.left) and same(a.right, b.right)

        if root is None:
            return False
        if same(root, subRoot):
            return True
        return self.isSubtree(root.left, subRoot) or self.isSubtree(root.right, subRoot)
```

### Explanation

- `same(a, b)` compares two trees node by node and stops at the first difference.
- The main function walks over every node of `root` and calls `same` there.
- `or` short-circuits: once a match is found on the left, the right side is not searched.

### Complexity

- **Time:** `O(m · n)` in the worst case, where `m` = nodes in `root` and `n` = nodes in `subRoot`. Each of the `m` start nodes may compare up to `n` nodes before finding a difference (imagine a tree full of `1`s with a different leaf at the very bottom). With `m = 2000`, `n = 1000` that is at most about 2 million node comparisons — fine for this problem's limits, which is why this is the standard accepted answer.
- **Auxiliary space:** `O(h_root + h_sub)` for the recursion stacks, where `h` is the tree height.
- **Honest trade-off:** simple, clear, and fast enough here. It only becomes a problem for much larger trees.

---

## 6. Optimized Solution

### Idea

1. **Serialize** both trees in preorder, writing `,value` for a node and `,#` for a missing child. The comma comes **before** every token.
2. `subRoot` is a subtree of `root` **if and only if** the string of `subRoot` appears inside the string of `root`.
3. Find it with **KMP** (Knuth–Morris–Pratt), which runs in time linear in the two string lengths.

Why is the match unambiguous?

- The pattern starts with a comma, and commas appear only at the start of tokens → a match must **start at a token boundary**.
- Every token in the pattern is followed by another comma, except the very last one, which is always `#` (the last thing preorder writes is a null marker) → value tokens must match **completely** (`,2,` can never match inside `,21,`), and the match **ends exactly at a token's end**.
- So a match lines up token-for-token with a complete preorder block of `root` — that block is exactly one node's full subtree.

### Algorithm

1. `text = serialize(root)`, `pattern = serialize(subRoot)`.
2. Build the KMP "longest proper prefix which is also suffix" (`lps`) table for `pattern`.
3. Scan `text` once, keeping how many pattern characters are currently matched; on a mismatch fall back using `lps` instead of restarting.
4. Return `True` as soon as the whole pattern is matched.

### Python code (LeetCode-ready)

```python
from typing import Optional


class Solution:
    def isSubtree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
        def serialize(node, out):
            if node is None:
                out.append(",#")
                return
            out.append("," + str(node.val))   # delimiter BEFORE every value
            serialize(node.left, out)
            serialize(node.right, out)

        text_parts, pattern_parts = [], []
        serialize(root, text_parts)
        serialize(subRoot, pattern_parts)
        text = "".join(text_parts)
        pattern = "".join(pattern_parts)

        # KMP prefix table: lps[i] = length of the longest proper prefix of
        # pattern[:i + 1] that is also a suffix of it.
        lps = [0] * len(pattern)
        length = 0
        for i in range(1, len(pattern)):
            while length and pattern[i] != pattern[length]:
                length = lps[length - 1]
            if pattern[i] == pattern[length]:
                length += 1
            lps[i] = length

        # Scan the text once.
        matched = 0
        for ch in text:
            while matched and ch != pattern[matched]:
                matched = lps[matched - 1]
            if ch == pattern[matched]:
                matched += 1
                if matched == len(pattern):
                    return True
        return False
```

### Shorter version using Python's `in`

```python
from typing import Optional


class Solution:
    def isSubtree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
        def serialize(node):
            parts = []
            stack = [node]
            while stack:                      # iterative preorder
                cur = stack.pop()
                if cur is None:
                    parts.append(",#")
                    continue
                parts.append("," + str(cur.val))
                stack.append(cur.right)
                stack.append(cur.left)
            return "".join(parts)

        return serialize(subRoot) in serialize(root)
```

This is what most people write in practice. CPython's substring search is very fast on real inputs (and since Python 3.10 it switches to a linear-time algorithm for long patterns), but the language does not document a worst-case bound, so the KMP version is the one that **guarantees** `O(m + n)`. This version also uses an explicit stack, so deep trees cannot hit the recursion limit.

### Alternative idea: tree hashing

You can also compute a hash (or a unique integer ID) for every subtree bottom-up — `id(node) = lookup[(val, id(left), id(right))]` — and check whether `subRoot`'s ID appears among `root`'s subtree IDs. Using a dictionary that assigns fresh IDs to new triples avoids collisions entirely and also runs in `O(m + n)` average time.

### Recursion depth — an honest note

The recursive `same`/`isSubtree`/`serialize` functions go as deep as the tree height. `root` may have 2000 nodes, so a chain-shaped tree needs about 2000 nested calls, while CPython's default limit is 1000. Whether LeetCode's judge raises that limit is not something to depend on; the iterative-stack version above is safe either way, or you can call `sys.setrecursionlimit(10000)`.

---

## 7. Line-by-Line Explanation

(KMP version from Section 6.)

| Line | What it does | Why |
|---|---|---|
| `def serialize(node, out):` | Preorder walk that appends tokens to `out`. | Preorder writes a node followed by its **whole** subtree as one contiguous block. |
| `out.append(",#")` | Marks an empty child. | Without null markers, different shapes could give the same string. |
| `out.append("," + str(node.val))` | Writes the value with a **leading** comma. | Prevents `2` from matching inside `12` or `-2`. |
| `text = "".join(text_parts)` | Builds the big string, e.g. `,3,4,1,#,#,2,#,#,5,#,#`. | Joining a list once is linear time. |
| `lps = [0] * len(pattern)` | KMP helper table. | Tells us how far we can fall back after a mismatch without re-reading text. |
| `while length and pattern[i] != pattern[length]: length = lps[length - 1]` | Shrinks the current border on mismatch. | Standard KMP prefix-function step. |
| `if pattern[i] == pattern[length]: length += 1` | Extends the border. | — |
| `for ch in text:` | One left-to-right pass over the big string. | Each text character is read once. |
| `while matched and ch != pattern[matched]: matched = lps[matched - 1]` | On mismatch, reuse the part already matched. | This is what makes KMP linear instead of `O(m · n)`. |
| `if matched == len(pattern): return True` | Whole pattern found. | By the delimiter argument, this is a complete subtree of `root`. |
| `return False` | Pattern never found. | No node of `root` has an identical subtree. |

---

## 8. Dry Run

### Brute force on Example 2

`root = [3,4,5,1,2,null,null,null,null,0]`, `subRoot = [4,1,2]`

| Step | Node of `root` tried | `same(node, subRoot)` | Reason |
|---|---|---|---|
| 1 | 3 | False | `3 != 4` |
| 2 | 4 | False | values 4 = 4; left: `same(1, 1)` is True; right: `same(2, 2)` compares children — `2.left` is `0` but `subRoot`'s `2.left` is `None` → False |
| 3 | 1 | False | `1 != 4` |
| 4 | 2 | False | `2 != 4` |
| 5 | 0 | False | `0 != 4` |
| 6 | 5 | False | `5 != 4` |

Every node failed → **`false`** ✅

### Optimized version on Example 1

`root = [3,4,5,1,2]`, `subRoot = [4,1,2]`

**Serialization of `root` (preorder):**

| Visit | Token appended | String so far |
|---|---|---|
| 3 | `,3` | `,3` |
| 4 | `,4` | `,3,4` |
| 1 | `,1` | `,3,4,1` |
| 1.left, 1.right | `,#` `,#` | `,3,4,1,#,#` |
| 2 | `,2` | `,3,4,1,#,#,2` |
| 2.left, 2.right | `,#` `,#` | `,3,4,1,#,#,2,#,#` |
| 5 | `,5` | `,3,4,1,#,#,2,#,#,5` |
| 5.left, 5.right | `,#` `,#` | `,3,4,1,#,#,2,#,#,5,#,#` |

**Serialization of `subRoot`:** `,4,1,#,#,2,#,#`

**Search:**

```text
text:     ,3,4,1,#,#,2,#,#,5,#,#
pattern:    ,4,1,#,#,2,#,#
            ^ starts at index 2 (the comma before 4)
```

| Text index | Char | `matched` before | Action | `matched` after |
|---|---|---|---|---|
| 0 | `,` | 0 | equals `pattern[0]` = `,` | 1 |
| 1 | `3` | 1 | `3 != pattern[1]` (`4`) → fall back to `lps[0] = 0`; `3 != ,` | 0 |
| 2 | `,` | 0 | match | 1 |
| 3 | `4` | 1 | match | 2 |
| 4–15 | `,1,#,#,2,#,#` | 2 … 13 | every character matches | 14 = `len(pattern)` |

The full pattern (14 characters) is matched → **`true`** ✅

### Example 2 with the optimized version

`text = ,3,4,1,#,#,2,0,#,#,#,5,#,#` and `pattern = ,4,1,#,#,2,#,#`. The match runs through `,4,1,#,#,2,` and then sees `0` where the pattern wants `#`. No other position starts with `,4`, so the answer is **`false`** ✅.

---

## 9. Concepts, Data Structures, and Patterns

- **Same Tree as a building block:** the brute force is "Same Tree at every node" — see [042_same_tree.md](042_same_tree.md).
- **Tree serialization with null markers** turns structural equality into string equality — see [046_serialize_and_deserialize_binary_tree.md](046_serialize_and_deserialize_binary_tree.md).
- **Preorder contiguity:** in preorder, a node's subtree occupies one consecutive block of the output. That's why "subtree" becomes "substring".
- **Delimiters:** a classic source of bugs in any encoding. Put a separator at a fixed position (here: before each token) so tokens can't merge.
- **KMP string matching:** `O(text + pattern)` substring search using a prefix table.
- **Hashing / Merkle-style IDs:** give each subtree an ID from `(val, left_id, right_id)`; used in "Find Duplicate Subtrees" (LeetCode 652).
- **DFS recursion vs. explicit stack** and Python's recursion limit.

---

## 10. Complexity Analysis

Let `m` = nodes in `root`, `n` = nodes in `subRoot`, `h_root`/`h_sub` = their heights.

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Brute force (same-tree at every node) | `O(m · n)` worst case | `O(h_root + h_sub)` | Up to `m` start nodes × up to `n` comparisons each; recursion stacks only. |
| Serialization + KMP | `O(m + n)` | `O(m + n)` | Each string has `2k + 1` tokens of at most 7 characters (`,-10000`), so lengths are `O(m)` and `O(n)`. KMP is linear in their sum. The strings and the `lps` table take `O(m + n)` space (plus `O(h)` recursion while serializing). |
| Serialization + `in` | `O(m + n)` to build; search is linear in practice but not documented as worst-case linear | `O(m + n)` | Shortest code. |
| Tree hashing with ID dictionary | `O(m + n)` average | `O(m + n)` | One dictionary lookup per node. |

---

## 11. Edge Cases

| Case | `root` | `subRoot` | Expected | Why |
|---|---|---|---|---|
| Whole tree matches | `[1,2,3]` | `[1,2,3]` | `true` | A tree is a subtree of itself. |
| Single equal nodes | `[1]` | `[1]` | `true` | — |
| Digit overlap `12` vs `2` | `[12]` | `[2]` | `false` | Leading comma: `,2,#,#` is not inside `,12,#,#`. |
| Sign overlap `-2` vs `2` | `[-2]` | `[2]` | `false` | `,2` is not inside `,-2`. |
| Prefix overlap `21` vs `2` | `[1,21]` | `[2]` | `false` | `,2,` can't match inside `,21,`. |
| Matching node has extra descendants | `[4,1,2,0]` | `[4,1,2]` | `false` | `1` has an extra child `0`. |
| Same values, mirrored shape | `[1,2]` | `[1,null,2]` | `false` | Null markers record the shape. |
| Match deep in a chain | `[1,null,1,null,1]` | `[1,null,1]` | `true` | The subtree starting at the second `1`. |
| Match is a leaf | `[1,1]` | `[1]` | `true` | The left child `1` is a leaf, like `subRoot`. |
| Extreme values | `[-10000,10000]` | `[10000]` | `true` | The leaf `10000` matches. |

---

## 12. Common Mistakes and Debugging

1. **Only checking the top part.** Returning `True` when the values match but ignoring that the node in `root` has *extra* children (Example 2). The same-tree check must compare `None` against `None` at the bottom.
2. **Missing or misplaced delimiters.** Serializing as `str(val) + ","` (delimiter *after*) makes `[12]` → `"12,#,#,"` contain `[2]` → `"2,#,#,"`. Put the delimiter **before** each value (or on both sides).
3. **Forgetting null markers.** Without them, `[1,2]` and `[1,null,2]` produce the same string.
4. **Using inorder serialization.** Inorder does not keep a subtree as a recognizable block with an unambiguous root; stick to preorder (or postorder) with null markers.
5. **Confusing `same` with `isSubtree` in the recursion.** The recursive calls on `root.left`/`root.right` must call `isSubtree` (search anywhere), while the comparison must call `same` (exact match from this node).
6. **Short-circuit misunderstanding:** `same(a.left, b.left) and same(a.right, b.right)` — both must hold.

**Debugging tip:** print the two serialized strings for a failing case. If you see something like `"12,#,#,"` containing `"2,#,#,"`, it's a delimiter bug.

---

## 13. Practice Questions

**Q1. Show the delimiter bug in code: compare "delimiter after" with "delimiter before" on `root = [12]`, `subRoot = [2]`.**

<details><summary>Hint</summary>Serialize both trees both ways and test with `in`.</summary></details>

**Answer:**

```python
def serialize_after(node):
    if node is None:
        return "#,"
    return str(node.val) + "," + serialize_after(node.left) + serialize_after(node.right)


def serialize_before(node):
    if node is None:
        return ",#"
    return "," + str(node.val) + serialize_before(node.left) + serialize_before(node.right)


big, small = TreeNode(12), TreeNode(2)
assert serialize_after(big) == "12,#,#,"
assert serialize_after(small) in serialize_after(big)          # WRONG: false match
assert serialize_before(small) not in serialize_before(big)    # correct: no match
```

**Q2. Count how many nodes of `root` start a subtree identical to `subRoot`.**

<details><summary>Hint</summary>Serialize every subtree bottom-up (postorder) and count how many equal the pattern's serialization.</summary></details>

**Answer:**

```python
def count_matching_subtrees(root, sub):
    def encode(node, record):
        if node is None:
            return "#"
        code = "(" + encode(node.left, record) + "," + str(node.val) + "," + encode(node.right, record) + ")"
        record.append(code)
        return code

    target = encode(sub, [])
    codes = []
    encode(root, codes)
    return sum(1 for code in codes if code == target)


# root = [1,1,1]: both leaves equal the tree [1]
tree = TreeNode(1, TreeNode(1), TreeNode(1))
assert count_matching_subtrees(tree, TreeNode(1)) == 2
assert count_matching_subtrees(tree, TreeNode(1, TreeNode(1))) == 0
assert count_matching_subtrees(tree, TreeNode(1, TreeNode(1), TreeNode(1))) == 1
```

The parentheses around each encoded subtree make the encoding unambiguous. (Building strings this way is `O(m²)` in the worst case because long strings are copied at every level; the ID-dictionary trick fixes that.)

**Q3. Find the values at the roots of all duplicate subtrees (LeetCode 652 idea).**

<details><summary>Hint</summary>Give each distinct subtree shape an integer ID with a dictionary keyed by `(val, left_id, right_id)`, and count how often each ID appears.</summary></details>

**Answer:**

```python
def duplicate_subtree_roots(root):
    ids = {}            # (val, left_id, right_id) -> id
    count = {}          # id -> how many times seen
    result = []

    def get_id(node):
        if node is None:
            return 0
        key = (node.val, get_id(node.left), get_id(node.right))
        if key not in ids:
            ids[key] = len(ids) + 1
        uid = ids[key]
        count[uid] = count.get(uid, 0) + 1
        if count[uid] == 2:          # report each duplicate shape once
            result.append(node.val)
        return uid

    get_id(root)
    return sorted(result)


# [1,2,3,4,null,2,4,null,null,4] has duplicate subtrees [4] and [2,4]
four_a, four_b, four_c = TreeNode(4), TreeNode(4), TreeNode(4)
tree = TreeNode(1, TreeNode(2, four_a), TreeNode(3, TreeNode(2, four_b), four_c))
assert duplicate_subtree_roots(tree) == [2, 4]
assert duplicate_subtree_roots(TreeNode(1)) == []
```

Each node does `O(1)` average dictionary work, so this is `O(m)` — the same ID trick can solve "Subtree of Another Tree" too.

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** Same-tree check at every node (simple) **or** preorder serialization + substring search (linear).
- **Key idea:** In preorder with null markers, a subtree is a contiguous block of the string; delimiters before every token prevent `2`/`12`/`-2` false matches.
- **Time:** brute force `O(m · n)`; serialization + KMP `O(m + n)`.
- **Auxiliary space:** brute force `O(h_root + h_sub)`; serialization `O(m + n)`.
- **One-line memory hook:** *"Write both trees as sentences with a comma before every word, then look for the small sentence in the big one."*

### Completion checklist

- [x] Problem requirements verified
- [x] Examples and constraints verified
- [x] Beginner-friendly analogy, TreeNode primer and logic written
- [x] Brute-force solution written and tested
- [x] Optimized Python solution written and tested (`tools/tests/p047.py`), plus the `in` version, including the `2` vs `12` delimiter pitfall
- [x] Line-by-line explanation written
- [x] Dry run completed with real examples
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
