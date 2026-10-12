# 046. Serialize and Deserialize Binary Tree

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Serialize and Deserialize Binary Tree |
| **LeetCode number** | 297 |
| **Topic (source list)** | Tree |
| **Also uses** | Design, DFS (preorder), BFS (level order), String parsing |
| **Difficulty** | Hard |
| **LeetCode URL** | <https://leetcode.com/problems/serialize-and-deserialize-binary-tree/> |
| **Pattern** | Traversal with explicit null markers, then rebuild by replaying the same traversal |

---

## 2. Problem Explanation

### Beginner primer: what is a `TreeNode`?

A binary tree is made of **nodes**. Each node stores a value and two links: one to a **left child** and one to a **right child**. A missing child is `None`. LeetCode shows the definition as a comment at the top of the editor (it is already provided — you never write it yourself):

```text
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None
```

(For this problem LeetCode's Python template uses the `TreeNode(x)` form above; other tree problems use `TreeNode(val=0, left=None, right=None)`. Both create a node with a `val`, a `left` and a `right`.)

### How LeetCode writes a tree as a list

LeetCode prints trees in **level order** (row by row, left to right), writing `null` for a missing child. Trailing `null`s at the very end are dropped. For example `root = [1,2,3,null,null,4,5]` means:

```text
Level-order list:  [1, 2, 3, null, null, 4, 5]

            1            <- row 0: 1
          /   \
         2     3         <- row 1: 2, 3
              / \
             4   5       <- row 2: children of 2 are null, null; children of 3 are 4, 5
```

Read the list from the left: the first value is the root; the next two values are the root's left and right children; the next two are the children of the first real node in the next row, and so on. `null` slots get no children of their own.

### What are we given?

A class to design, called `Codec`, with two methods:

- `serialize(self, root)` — receives the root of a binary tree (possibly `None`) and must return a **string**.
- `deserialize(self, data)` — receives a string produced by `serialize` and must return the root of a tree.

### What must we return?

Nothing is compared directly except the final tree. LeetCode runs:

```text
ser = Codec()
deser = Codec()
ans = deser.deserialize(ser.serialize(root))
```

and checks that `ans` has **exactly the same shape and values** as the original `root`.

### The rules

1. **You choose the string format.** It does not have to look like LeetCode's list format; it just has to let you rebuild the exact same tree.
2. The two methods must work as a pair, even on **two different `Codec` objects** — so do not store the tree in `self` and "cheat" by returning it later.
3. The empty tree (`root = None`) must survive the round trip.

### Examples

**Example 1**

```text
Input:  root = [1,2,3,null,null,4,5]
Output: [1,2,3,null,null,4,5]
```

The tree drawn above is turned into a string and back; the rebuilt tree prints the same list.

**Example 2**

```text
Input:  root = []
Output: []
```

The empty tree must come back as the empty tree.

### Constraints

- The number of nodes in the tree is in the range `[0, 10^4]`.
- `-1000 <= Node.val <= 1000`

There is no follow-up in the statement. Note that values can be **negative** (so the string will contain `-` signs) and can have **up to four digits** — your format must separate values clearly.

---

## 3. Everyday Analogy

> **Explain it like I'm five**

You built a beautiful LEGO tree and want to mail it to a friend. It won't fit in an envelope, so you write **instructions** on a piece of paper: "Put a 1 block. On its left put a 2. The 2 has nothing on its left and nothing on its right. On the 1's right put a 3…"

The important trick is to also write **"nothing here"** whenever a spot is empty. If you only listed the blocks, your friend wouldn't know whether the 4 sits on the left of 3 or on the right of 2. With the "nothing here" notes, your friend can follow the instructions **in the same order you wrote them** and end up with exactly your tree.

Writing the instructions = **serialize**. Following them = **deserialize**.

---

## 4. Step-by-Step Logic

1. **Why values alone are not enough.** The preorder list `[1, 2, 3]` could be a root with two children, or a chain 1 → 2 → 3, or several other shapes. We must record **where the empty spots are**.
2. **Add a null marker.** Write a special token (we use `#`) every time we reach a missing child. Now the string describes the shape completely.
3. **Pick a traversal.** Any fixed order works as long as the reader uses the same order:
   - *Level order (BFS)* — row by row, like LeetCode's own format.
   - *Preorder (DFS)* — node, then its whole left subtree, then its whole right subtree.
4. **Separate tokens with a delimiter** (a comma), because values can have several digits and a minus sign. `"12"` must never be confused with `"1"` followed by `"2"`.
5. **Rebuild by replaying the traversal.** In preorder, the first token is the root. Then the next tokens describe the left subtree completely (the `#` markers tell us exactly where it ends), and then the right subtree. A recursive function that reads one token at a time does this naturally.
6. **Count check:** a tree with `n` nodes has `n + 1` empty child spots, so both formats produce exactly `2n + 1` tokens. That is linear in `n`.

---

## 5. Brute-Force Solution

For a design problem there is no "slow but obvious" search. The most **direct** approach is to copy what LeetCode itself does: write the tree **level by level** with a `null` for every missing child. We keep **all** the `null`s (including trailing ones) so that the reader never has to guess.

### Algorithm

**serialize**

1. If the tree is empty, return the empty string `""`.
2. Put the root in a queue. Repeatedly take the front node:
   - if it is `None`, write `null`;
   - otherwise write its value and put both of its children (even if they are `None`) at the back of the queue.
3. Join the tokens with commas.

**deserialize**

1. If the string is empty, return `None`.
2. Split on commas. The first token is the root; put it in a queue.
3. Repeatedly take the front node and read the **next two tokens** as its left and right child. Each real child is created and added to the queue.

### Python code

```python
from collections import deque


class Codec:
    def serialize(self, root):
        """Level order with an explicit 'null' for every missing child."""
        if root is None:
            return ""
        tokens = []
        queue = deque([root])
        while queue:
            node = queue.popleft()
            if node is None:
                tokens.append("null")
                continue
            tokens.append(str(node.val))
            queue.append(node.left)
            queue.append(node.right)
        return ",".join(tokens)

    def deserialize(self, data):
        if not data:
            return None
        tokens = data.split(",")
        root = TreeNode(int(tokens[0]))
        queue = deque([root])
        i = 1
        while queue:
            node = queue.popleft()
            if tokens[i] != "null":            # left child
                node.left = TreeNode(int(tokens[i]))
                queue.append(node.left)
            i += 1
            if tokens[i] != "null":            # right child
                node.right = TreeNode(int(tokens[i]))
                queue.append(node.right)
            i += 1
        return root
```

### Explanation

- For Example 1 the string is `"1,2,3,null,null,4,5,null,null,null,null"` (11 tokens = `2 × 5 + 1`).
- Because every real node writes **both** child slots, the reader can safely read `tokens[i]` and `tokens[i + 1]` for every node it takes from the queue — the index never runs past the end.
- `int(token)` handles negative numbers such as `"-1000"` automatically.

### Complexity and trade-offs

- **Time:** `O(n)` for both methods — every node is enqueued and dequeued once and every token is read once.
- **Auxiliary space:** `O(n)` for the token list / string, plus the queue, which can hold up to one full level (about `n/2` nodes in a balanced tree), so `O(n)` in the worst case.
- **Honest trade-off:** this is *not* slow — it is already linear. Its downsides are smaller: the code is longer, it writes many `null` tokens on the last level, and the reader needs careful index bookkeeping. Its upside is that it uses **no recursion**, so it never hits Python's recursion limit, even on a 10^4-node chain.

---

## 6. Optimized Solution

### Idea

Use **preorder DFS** (node → left subtree → right subtree) and write `#` for every missing child. To rebuild, read the tokens **one at a time** with an iterator and call the same recursive shape: make a node from the current token, then build its left subtree, then its right subtree. A `#` means "this subtree is empty, stop here".

It has the same `O(n)` complexity as the level-order version, but it is shorter, has no index arithmetic, and the serialize/deserialize functions mirror each other exactly — which makes it much easier to get right in an interview. It is also the building block for other problems (see [047_subtree_of_another_tree.md](047_subtree_of_another_tree.md)).

### Algorithm

**serialize**

1. `dfs(node)`: if `node` is `None`, append `#`; otherwise append `str(node.val)`, then `dfs(node.left)`, then `dfs(node.right)`.
2. Return the tokens joined by commas.

**deserialize**

1. Make an iterator over `data.split(",")`.
2. `build()`: take the next token. If it is `#`, return `None`. Otherwise create a node, set `node.left = build()`, `node.right = build()`, return the node.
3. Return `build()`.

### Python code (LeetCode-ready)

```python
class Codec:
    def serialize(self, root):
        """Encodes a tree to a single string (preorder with '#' for null)."""
        tokens = []

        def dfs(node):
            if node is None:
                tokens.append("#")
                return
            tokens.append(str(node.val))
            dfs(node.left)
            dfs(node.right)

        dfs(root)
        return ",".join(tokens)

    def deserialize(self, data):
        """Decodes your encoded data to tree."""
        tokens = iter(data.split(","))

        def build():
            token = next(tokens)
            if token == "#":
                return None
            node = TreeNode(int(token))
            node.left = build()     # consumes exactly the left subtree's tokens
            node.right = build()    # then exactly the right subtree's tokens
            return node

        return build()


# Your Codec object will be instantiated and called as such:
# ser = Codec()
# deser = Codec()
# ans = deser.deserialize(ser.serialize(root))
```

### Recursion depth — an honest warning

Both recursive helpers go as deep as the tree's **height `h`**. The constraints allow 10^4 nodes, so a completely skewed tree (a chain) has `h = 10^4`. CPython's default recursion limit is **1000**, so in a plain Python script this code would raise `RecursionError` on such a chain. Whether it passes on LeetCode depends on the judge's settings and test data, so don't rely on it. Two safe options:

- call `sys.setrecursionlimit(20000)` (works for this size, but very deep recursion can still crash the interpreter on some systems), or
- use the **iterative** version below, which keeps its own stack.

### Iterative preorder version (no recursion limit)

```python
class Codec:
    def serialize(self, root):
        tokens = []
        stack = [root]
        while stack:
            node = stack.pop()
            if node is None:
                tokens.append("#")
                continue
            tokens.append(str(node.val))
            stack.append(node.right)   # pushed first, so popped after the left
            stack.append(node.left)
        return ",".join(tokens)

    def deserialize(self, data):
        tokens = data.split(",")
        if tokens[0] == "#":
            return None
        root = TreeNode(int(tokens[0]))
        stack = [[root, 0]]            # [node, 0 = needs left / 1 = needs right]
        for token in tokens[1:]:
            child = None if token == "#" else TreeNode(int(token))
            parent = stack[-1]
            if parent[1] == 0:
                parent[0].left = child
                parent[1] = 1
            else:
                parent[0].right = child
                stack.pop()            # both children are now filled in
            if child is not None:
                stack.append([child, 0])
        return root
```

The stack always holds the nodes that are still waiting for a child; the top of the stack is exactly the node the next preorder token belongs to.

---

## 7. Line-by-Line Explanation

(Recursive preorder `Codec` from Section 6.)

| Line | What it does | Why |
|---|---|---|
| `tokens = []` | Collects the pieces of the output string. | Appending to a list and joining once is `O(n)`; building a string with `+=` in a loop can be slower. |
| `def dfs(node):` | Nested helper that visits the tree in preorder. | Being nested lets it append to `tokens` directly. |
| `if node is None: tokens.append("#")` | Records an empty spot. | The `#` markers are what make the string describe the **shape**, not just the values. |
| `tokens.append(str(node.val))` | Records the node's value first. | Preorder = node, left, right. The reader will also create the node first. |
| `dfs(node.left)` / `dfs(node.right)` | Records the whole left subtree, then the whole right subtree. | The reader will consume them in the same order. |
| `return ",".join(tokens)` | Builds e.g. `"1,2,#,#,3,4,#,#,5,#,#"`. | Commas separate multi-digit and negative values unambiguously. |
| `tokens = iter(data.split(","))` | Turns the list of tokens into an iterator. | `next(tokens)` hands out tokens one at a time in `O(1)` — no index variable and no `list.pop(0)` (which would be `O(n)` each). |
| `token = next(tokens)` | Reads the next instruction. | Each call to `build` consumes exactly one token for its own node. |
| `if token == "#": return None` | An empty subtree. | This is where the recursion stops. |
| `node = TreeNode(int(token))` | Creates the node. | `int("-12")` correctly gives `-12`. |
| `node.left = build()` | Builds the entire left subtree. | It keeps reading tokens until the left subtree's last `#`. |
| `node.right = build()` | Builds the entire right subtree from the tokens that follow. | Exactly mirrors `dfs`. |
| `return build()` | Returns the rebuilt root. | For the empty tree the string is `"#"` and `build()` returns `None`. |

---

## 8. Dry Run

**Input:** Example 1, `root = [1,2,3,null,null,4,5]`

```text
            1
          /   \
         2     3
              / \
             4   5
```

### Serialize (preorder)

| Step | Call | Action | `tokens` so far |
|---|---|---|---|
| 1 | `dfs(1)` | append `1`, go left | `1` |
| 2 | `dfs(2)` | append `2`, go left | `1,2` |
| 3 | `dfs(None)` (2.left) | append `#` | `1,2,#` |
| 4 | `dfs(None)` (2.right) | append `#` | `1,2,#,#` |
| 5 | `dfs(3)` | append `3`, go left | `1,2,#,#,3` |
| 6 | `dfs(4)` | append `4` | `1,2,#,#,3,4` |
| 7 | `dfs(None)` ×2 (4's children) | append `#`, `#` | `1,2,#,#,3,4,#,#` |
| 8 | `dfs(5)` | append `5` | `1,2,#,#,3,4,#,#,5` |
| 9 | `dfs(None)` ×2 (5's children) | append `#`, `#` | `1,2,#,#,3,4,#,#,5,#,#` |

**String:** `"1,2,#,#,3,4,#,#,5,#,#"` — 11 tokens = `2 × 5 + 1` ✅

### Deserialize

| Step | Token read | Created / returned | Attached as | Call stack after the step |
|---|---|---|---|---|
| 1 | `1` | node 1 | root | `build(1)` waiting for left |
| 2 | `2` | node 2 | 1.left (in progress) | `1 → 2` waiting for left |
| 3 | `#` | `None` | 2.left | `1 → 2` waiting for right |
| 4 | `#` | `None` | 2.right; node 2 finished | `1` waiting for right |
| 5 | `3` | node 3 | 1.right (in progress) | `1 → 3` waiting for left |
| 6 | `4` | node 4 | 3.left (in progress) | `1 → 3 → 4` |
| 7 | `#`, `#` | `None`, `None` | 4.left, 4.right; node 4 finished | `1 → 3` waiting for right |
| 8 | `5` | node 5 | 3.right (in progress) | `1 → 3 → 5` |
| 9 | `#`, `#` | `None`, `None` | 5.left, 5.right; 5, 3, 1 finished | empty |

**Result:** the rebuilt tree prints as `[1,2,3,null,null,4,5]` ✅

### Second dry run: Example 2

`root = []` → `serialize` calls `dfs(None)`, which appends `#`, so the string is `"#"`. `deserialize("#")` reads `#` and returns `None`, which prints as `[]` ✅.

---

## 9. Concepts, Data Structures, and Patterns

- **Serialization:** turning an in-memory structure into a flat string (or bytes) that can be saved or sent, then rebuilt later. JSON, pickle and database formats all do this.
- **Null markers make traversals unique.** A single traversal of values (like preorder alone) does *not* identify a tree. With null markers, preorder **does**. Without null markers you need **two** traversals, e.g. preorder + inorder — see [048_construct_binary_tree_from_preorder_and_inorder_traversal.md](048_construct_binary_tree_from_preorder_and_inorder_traversal.md).
- **Preorder DFS** (recursion or an explicit stack) and **level-order BFS** (a `deque` queue) — see [045_binary_tree_level_order_traversal.md](045_binary_tree_level_order_traversal.md) and [041_maximum_depth_of_binary_tree.md](041_maximum_depth_of_binary_tree.md).
- **Iterator as a cursor:** `iter(list)` plus `next()` is a clean way to share "current position" across recursive calls without global indices.
- **Delimiters:** separate tokens so multi-digit/negative values can't blend together. The same idea is critical in [047_subtree_of_another_tree.md](047_subtree_of_another_tree.md).
- **Comparing trees:** checking that the round trip worked is exactly the [042_same_tree.md](042_same_tree.md) problem.

---

## 10. Complexity Analysis

Let `n` = number of nodes and `h` = height of the tree (`h` is about `log n` for a balanced tree and up to `n` for a chain).

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Level order with nulls (Section 5) | `O(n)` both ways | `O(n)` | `2n + 1` tokens are written/read once. The queue can hold an entire level, up to about `n/2` nodes. |
| Preorder DFS, recursive (Section 6) | `O(n)` both ways | `O(n)` for the string/token list, plus `O(h)` recursion stack | Each node and each null marker is handled once. The call stack is as deep as the tree. |
| Preorder DFS, iterative | `O(n)` both ways | `O(n)` for tokens, `O(h)` stack | Same work; the explicit stack replaces the call stack, so deep trees are safe. |

The output string itself is `O(n)` characters (each value has at most 5 characters, like `-1000`), so no correct approach can use less than `O(n)` space overall.

---

## 11. Edge Cases

| Case | Example | Serialized (preorder version) | Expected result after round trip |
|---|---|---|---|
| Empty tree | `[]` | `"#"` | `[]` |
| Single node | `[1]` | `"1,#,#"` | `[1]` |
| Negative / extreme values | `[-1000, 1000]` | `"-1000,1000,#,#,#"` | `[-1000,1000]` |
| Multi-digit values | `[12, 1, 2]` | `"12,1,#,#,2,#,#"` | `[12,1,2]` — commas keep `12` separate from `1`, `2` |
| Right-skewed chain | `[1,null,2,null,3]` | `"1,#,2,#,3,#,#"` | `[1,null,2,null,3]` |
| Left-skewed chain | `[1,2,null,3]` | `"1,2,3,#,#,#,#"` | `[1,2,null,3]` |
| Duplicate values | `[0,0,0,null,0,0]` | `"0,0,#,0,#,#,0,0,#,#,#"` | same tree — shape comes from the `#`s, not from values |
| 10^4-node chain | — | 20001 tokens | Recursive version needs a raised recursion limit; BFS or iterative version works as is |

---

## 12. Common Mistakes and Debugging

1. **Forgetting null markers.** Writing only values (e.g. `"1,2,3,4,5"`) loses the shape; many different trees produce the same string.
2. **No delimiter.** `"1234"` could be `[12, 34]` or `[1, 2, 3, 4]`. Always separate tokens.
3. **Reading single characters.** Iterating over `data` character by character breaks on `-5` or `100`. Split on the delimiter first.
4. **Using `tokens.pop(0)`.** Removing from the front of a Python list shifts every element — `O(n)` per call, `O(n²)` total. Use an iterator, a `deque`, or an index.
5. **Storing the tree in `self`.** LeetCode serializes with one `Codec` object and deserializes with another, so `self.saved = root` does not work (and is not a real solution).
6. **Trimming trailing nulls in the level-order version without adjusting the reader.** If you drop them (like LeetCode does), the reader must check `i < len(tokens)` before each read.
7. **Mixing traversal orders.** Serializing in preorder but rebuilding as if it were level order gives a different tree.

**Debugging tip:** print `ser.serialize(root)` for small trees and check it by hand: a tree with `n` nodes must give exactly `2n + 1` tokens. Then compare `deserialize(serialize(root))` with the original using a same-tree check.

---

## 13. Practice Questions

**Q1. What does the preorder `Codec` produce for `root = [1,null,2,3]`?**

<details><summary>Hint</summary>Draw the tree first: 2 is the right child of 1, and 3 is the left child of 2.</summary></details>

**Answer:** `"1,#,2,3,#,#,#"`. Preorder visits 1, then its left (`#`), then its right subtree: 2, then 2's left subtree (3 with `#`, `#`), then 2's right (`#`). That is 7 tokens = `2 × 3 + 1` ✅.

**Q2. Prove that a tree with `n` nodes always gives `2n + 1` tokens.**

<details><summary>Hint</summary>Count the child links. Every node has exactly two child slots, and every node except the root fills exactly one slot.</summary></details>

**Answer:** There are `2n` child slots in total. `n - 1` of them are filled by the non-root nodes, so `2n - (n - 1) = n + 1` slots are empty. Each empty slot writes one `#`, and each node writes one value: `n + (n + 1) = 2n + 1` tokens. (For the empty tree, `n = 0` and we write one `#`.)

**Q3. Serialize a Binary Search Tree as compactly as possible — values only, no null markers (this is LeetCode 449).**

<details><summary>Hint</summary>In a BST every value tells you where it belongs. Rebuild the preorder list using allowed ranges `(low, high)`: the next value belongs to the current subtree only if it lies inside the range.</summary></details>

**Answer:**

```python
def serialize_bst(root):
    out = []

    def walk(node):
        if node:
            out.append(str(node.val))
            walk(node.left)
            walk(node.right)

    walk(root)
    return ",".join(out)


def deserialize_bst(data):
    values = [int(x) for x in data.split(",")] if data else []
    pos = 0

    def build(low, high):
        nonlocal pos
        if pos == len(values) or not (low < values[pos] < high):
            return None
        value = values[pos]
        pos += 1
        node = TreeNode(value)
        node.left = build(low, value)
        node.right = build(value, high)
        return node

    return build(float("-inf"), float("inf"))


bst = TreeNode(5, TreeNode(3, TreeNode(1), TreeNode(4)), TreeNode(8, None, TreeNode(9)))
text = serialize_bst(bst)
assert text == "5,3,1,4,8,9"
rebuilt = deserialize_bst(text)
assert serialize_bst(rebuilt) == text
assert rebuilt.left.right.val == 4 and rebuilt.right.right.val == 9
assert deserialize_bst("") is None
```

Because the BST ordering already fixes where each value goes, the null markers are unnecessary, and the string has only `n` tokens.

**Q4. Why does preorder *without* null markers fail for general trees? Give two different trees with the same preorder.**

<details><summary>Hint</summary>Try three nodes 1, 2, 3.</summary></details>

**Answer:** `[1,2,3]` (1 with children 2 and 3) and `[1,2,null,3]` (chain 1 → 2 → 3 on the left) both have preorder `1, 2, 3`. With markers they become `1,2,#,#,3,#,#` and `1,2,3,#,#,#,#` — different.

```python
def preorder_with_markers(node):
    if node is None:
        return ["#"]
    return [str(node.val)] + preorder_with_markers(node.left) + preorder_with_markers(node.right)


def preorder_values(node):
    if node is None:
        return []
    return [node.val] + preorder_values(node.left) + preorder_values(node.right)


wide = TreeNode(1, TreeNode(2), TreeNode(3))
chain = TreeNode(1, TreeNode(2, TreeNode(3)))
assert preorder_values(wide) == preorder_values(chain) == [1, 2, 3]
assert preorder_with_markers(wide) != preorder_with_markers(chain)
```

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** Preorder DFS with null markers; rebuild by replaying the same preorder with an iterator.
- **Key idea:** Values + `#` for every empty child slot describe the shape completely; commas separate tokens.
- **Time:** `O(n)` for both methods.
- **Auxiliary space:** `O(n)` for the string, plus `O(h)` stack (recursive or explicit).
- **Watch out:** recursion depth on a 10^4-node chain — use the iterative or BFS version if needed.
- **One-line memory hook:** *"Write down every empty spot, then read the instructions back in the same order."*

### Completion checklist

- [x] Problem requirements verified
- [x] Examples and constraints verified
- [x] Beginner-friendly analogy, TreeNode primer and logic written
- [x] Brute-force (level-order) solution written and tested
- [x] Optimized Python solution written and tested (`tools/tests/p046.py`), plus the iterative version
- [x] Line-by-line explanation written
- [x] Dry run completed with a real example
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
