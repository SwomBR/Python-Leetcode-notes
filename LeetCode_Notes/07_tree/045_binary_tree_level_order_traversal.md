# 045. Binary Tree Level Order Traversal

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Binary Tree Level Order Traversal |
| **LeetCode number** | 102 |
| **Topic (source list)** | Tree |
| **Also uses** | Breadth-First Search, Queue, Depth-First Search |
| **Difficulty** | Medium |
| **LeetCode URL** | <https://leetcode.com/problems/binary-tree-level-order-traversal/> |
| **Pattern** | BFS with a queue, processing one level at a time (`for _ in range(len(queue))`) |

---

## 2. Problem Explanation

### Beginner primer: what is a `TreeNode`?

A **binary tree** is made of **nodes**. Each node stores a value `val` and links to a `left` child and a `right` child (`None` when missing). LeetCode already defines the class and shows it as a comment:

```text
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
```

### How LeetCode's list input becomes a tree

The input list is itself written in level order: the root, then each row from left to right, with `null` for a missing child. Each real node takes the next two items as its left and right children. `[3,9,20,null,null,15,7]` is:

```text
level 0:          3
                 / \
level 1:        9   20
                   /  \
level 2:          15   7
```

`9` takes the two `null`s (it has no children); `20` takes `15` and `7`.

Careful: the **input** list includes `null` placeholders, but the **output** you return contains **only real values**, grouped by level.

### What are we given?

`root` — the root of a binary tree (possibly `None`).

### What must we return?

A list of lists: one inner list per **level** (row) of the tree, from the top row down. Inside each inner list, the values appear from **left to right**. An empty tree gives an empty list `[]`.

### Examples

**Example 1**

```text
Input:  root = [3,9,20,null,null,15,7]
Output: [[3],[9,20],[15,7]]
```

Row 0 holds `3`; row 1 holds `9, 20`; row 2 holds `15, 7`.

**Example 2**

```text
Input:  root = [1]
Output: [[1]]
```

One node → one level.

**Example 3**

```text
Input:  root = []
Output: []
```

No nodes → no levels.

### Constraints

- The number of nodes in the tree is in the range `[0, 2000]`.
- `-1000 <= Node.val <= 1000`

There is no follow-up for this problem.

---

## 3. Everyday Analogy

> **Explain it like I'm five**

A school photo is being taken of a family tree. The photographer calls people **one row at a time**: "Grandma, please step forward!" — that's row 1. Then Grandma says: "My children are next," and they line up left to right — row 2. Each of them calls their own children for row 3, and so on.

The photographer uses a **waiting line**: people who have been called stand in line in order. When it's a row's turn, the photographer counts how many people are in line **right now** — that's exactly this row — takes their photo, and each of them sends their children to the **back** of the line for the next row's photo.

---

## 4. Step-by-Step Logic

1. **Levels come in order from the top.** Children of level `d` nodes form level `d + 1`, and left-to-right order is kept if we always add the left child before the right child.
2. **First in, first out.** Nodes discovered first must be processed first. That's exactly what a **queue** does — this is breadth-first search (BFS).
3. **Separating levels.** When a level starts, the queue contains **exactly** that level's nodes (all of the previous level have been removed and only their children were added). So record `size = len(queue)` and pop exactly `size` nodes — those make one inner list. Children added meanwhile wait for the next round.
4. **Empty tree:** return `[]` right away.
5. **DFS alternative:** a depth-first traversal that knows each node's depth can append `node.val` to `result[depth]`. Visiting left before right keeps each level's left-to-right order, even though levels are filled in an interleaved way.

---

## 5. Brute-Force Solution

### Algorithm

1. Compute the height `H` of the tree (number of levels).
2. For each level `d = 0, 1, …, H - 1`, run a **separate** DFS from the root that goes down exactly `d` steps and collects the nodes it reaches, left subtree before right subtree.

### Python code

```python
from typing import List, Optional


class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        def height(node: Optional[TreeNode]) -> int:
            if node is None:
                return 0
            return 1 + max(height(node.left), height(node.right))

        def collect(node: Optional[TreeNode], steps_left: int, out: List[int]) -> None:
            # Append the values exactly `steps_left` levels below `node`, left to right.
            if node is None:
                return
            if steps_left == 0:
                out.append(node.val)
                return
            collect(node.left, steps_left - 1, out)
            collect(node.right, steps_left - 1, out)

        result = []
        for depth in range(height(root)):
            level = []
            collect(root, depth, level)
            result.append(level)
        return result
```

### Explanation

- `height` tells us how many levels to produce (0 for an empty tree, so the loop doesn't run and we return `[]`).
- `collect(root, d, level)` walks every node above level `d` again just to reach level `d`. Left is explored before right, so the values come out left to right.

### Complexity

- **Time:** `O(n · h)`. The pass for level `d` visits every node at depths `0..d`, which can be up to `n` nodes, and there are `h` passes. For a balanced tree that's `O(n log n)`; for a skewed chain of 2000 nodes it is about `2000²/2 = 2 · 10^6` visits — acceptable at this size, but quadratic in general. The waste: the top levels are re-walked for every level below them.
- **Auxiliary space:** `O(h)` recursion stack (output not counted).

---

## 6. Optimized Solution

### Idea

BFS with a queue visits each node **once**, in exactly the required order. Freezing the queue size at the start of each round separates the levels.

### Algorithm

1. If `root` is `None`, return `[]`.
2. `queue = deque([root])`, `result = []`.
3. While the queue is not empty:
   - `level = []`; repeat `len(queue)` times: pop a node from the front, add its value to `level`, push its left child then its right child (if present).
   - append `level` to `result`.
4. Return `result`.

### Python code (LeetCode-ready, BFS)

```python
from collections import deque
from typing import List, Optional


class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if root is None:
            return []

        result = []
        queue = deque([root])
        while queue:
            level = []
            for _ in range(len(queue)):        # exactly the nodes of this level
                node = queue.popleft()
                level.append(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            result.append(level)
        return result
```

### Alternative: recursive DFS with a depth index

```python
from typing import List, Optional


class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        result = []

        def visit(node: Optional[TreeNode], depth: int) -> None:
            if node is None:
                return
            if depth == len(result):          # first node seen on this level
                result.append([])
            result[depth].append(node.val)
            visit(node.left, depth + 1)       # left first keeps left-to-right order
            visit(node.right, depth + 1)

        visit(root, 0)
        return result
```

Also `O(n)` time. Each level's list is filled left to right because, for any two nodes on the same level, preorder visits the left one first.

### Recursion limit — is the recursive version safe?

- Python's default recursion limit is **1000**; the DFS version (and the brute force) recurse once per level.
- The constraints allow 2000 nodes, so a skewed chain can be 2000 levels deep — **beyond** the default limit. In plain Python the recursive versions would raise `RecursionError` on such a tree.
- They are widely reported to be accepted on LeetCode (the judge's recursion settings are not documented), but the BFS version is the one that is safe for every allowed input everywhere. It uses no recursion at all.

---

## 7. Line-by-Line Explanation

(BFS)

| Line | What it does | Why |
|---|---|---|
| `if root is None: return []` | Handles the empty tree. | Otherwise `None` would enter the queue and `node.val` would crash. |
| `result = []` | Will hold one list per level. | The final answer. |
| `queue = deque([root])` | Queue starts with level 0. | `deque.popleft()` is `O(1)`; `list.pop(0)` is `O(n)`. |
| `while queue:` | One iteration per level. | When the queue is empty, every level is done. |
| `level = []` | Fresh list for this level. | Must be new each round, not reused. |
| `for _ in range(len(queue)):` | Fixes the number of pops to the current level's size. | `range(len(queue))` is evaluated once, so children appended during the loop are not popped this round. |
| `node = queue.popleft()` | Takes the leftmost waiting node. | FIFO keeps left-to-right order. |
| `level.append(node.val)` | Records its value. | Only values go in the output, not nodes. |
| `if node.left: queue.append(node.left)` then right | Schedules children for the next level. | Left before right preserves order; `None` children are skipped. |
| `result.append(level)` | Saves the finished level. | |

---

## 8. Dry Run

**Input (Example 1):** `root = [3,9,20,null,null,15,7]`

| Round | Queue at start | `len(queue)` | Pops (in order) | Children appended | `level` | `result` after round |
|---|---|---|---|---|---|---|
| 1 | `[3]` | 1 | 3 | 9, 20 | `[3]` | `[[3]]` |
| 2 | `[9, 20]` | 2 | 9, then 20 | (none from 9); 15, 7 from 20 | `[9, 20]` | `[[3], [9, 20]]` |
| 3 | `[15, 7]` | 2 | 15, then 7 | none | `[15, 7]` | `[[3], [9, 20], [15, 7]]` |
| — | `[]` | — | loop ends | | | |

**Result:** `[[3],[9,20],[15,7]]` ✅

In round 2, while `20` is popped the queue temporarily holds `15, 7`, but they are not popped in that round because the loop runs exactly 2 times.

**Second dry run (DFS version), same tree:**

| Call `visit(node, depth)` | `len(result)` before | Action | `result` after |
|---|---|---|---|
| `visit(3, 0)` | 0 | new level 0, append 3 | `[[3]]` |
| `visit(9, 1)` | 1 | new level 1, append 9 | `[[3], [9]]` |
| `visit(20, 1)` | 2 | append 20 to level 1 | `[[3], [9, 20]]` |
| `visit(15, 2)` | 2 | new level 2, append 15 | `[[3], [9, 20], [15]]` |
| `visit(7, 2)` | 3 | append 7 to level 2 | `[[3], [9, 20], [15, 7]]` |

(`None` children return immediately and are omitted.) **Examples 2 and 3:** `[1]` → one round → `[[1]]`; `[]` → `[]` ✅.

---

## 9. Concepts, Data Structures, and Patterns

- **Breadth-first search (BFS):** explore all nodes at distance `d` before any node at distance `d + 1`.
- **Queue (`collections.deque`):** FIFO; `append` at the back and `popleft` from the front are both `O(1)`.
- **Level-size snapshot:** `for _ in range(len(queue))` — the key trick for every "per level" tree problem (right side view, zigzag, averages, minimum depth…).
- **DFS with a depth parameter:** an alternative when you'd rather recurse; uses `result[depth]` as a bucket per level.
- **Related notes in this project:**
  - [041_maximum_depth_of_binary_tree.md](041_maximum_depth_of_binary_tree.md) — the BFS there counts rounds; here we keep each round's values.
  - [046_serialize_and_deserialize_binary_tree.md](046_serialize_and_deserialize_binary_tree.md) — LeetCode's level-order list format is a BFS serialization.
  - [043_invertflip_binary_tree.md](043_invertflip_binary_tree.md) — inverting a tree reverses every level of this output.
  - BFS on graphs works the same way, with a `visited` set (see [069_number_of_islands.md](../09_graph/069_number_of_islands.md)).

---

## 10. Complexity Analysis

Let `n` = number of nodes, `h` = height, `w` = maximum width (largest level).

| Approach | Time | Auxiliary space (excluding the output) | Explanation |
|---|---|---|---|
| Height + one DFS per level (brute force) | `O(n · h)`; worst `O(n²)` | `O(h)` | Upper levels are re-walked for every lower level. |
| BFS with level snapshot | `O(n)` | `O(w)` — up to about `n/2` (the last level of a complete tree); `O(1)` for a chain | Each node enters and leaves the queue once. The queue holds at most one level plus part of the next. |
| Recursive DFS with depth | `O(n)` | `O(h)` — best `O(log n)`, worst `O(n)` | One visit per node; stack depth = height. |

The output itself always has `n` values, so `O(n)` total space is unavoidable if you count it.

---

## 11. Edge Cases

| Case | Example | Expected result | Why |
|---|---|---|---|
| Empty tree | `[]` | `[]` | No levels at all (not `[[]]`). |
| Single node | `[1]` | `[[1]]` | One level. |
| Left chain | `[1,2,null,3]` | `[[1],[2],[3]]` | One node per level. |
| Gaps in the middle | `[1,2,3,4,null,null,5]` | `[[1],[2,3],[4,5]]` | Missing children are skipped, not written as `null`. |
| Repeated / negative values | `[0,-1,-1]` | `[[0],[-1,-1]]` | Values are copied as they are. |
| Chain of 2000 nodes | `[1,null,1,…]` | 2000 lists of one value | BFS is safe; recursive DFS exceeds Python's default limit. |

---

## 12. Common Mistakes and Debugging

1. **Not separating levels.** A plain BFS that appends every value to one list returns `[3, 9, 20, 15, 7]` — a flat list, not grouped.
2. **Using `while` with a changing `len(queue)`.** `i = 0; while i < len(queue)` re-reads the length as children are added, mixing levels. Snapshot the size once with `range(len(queue))`.
3. **Appending `None` children.** Pushing `None` and then reading `.val` crashes; push only real children (or skip `None` after popping).
4. **Returning `[[]]` for an empty tree.** The expected output is `[]`.
5. **Right child before left child.** Breaks the left-to-right order within each level.
6. **Using a list with `pop(0)`.** Correct but each pop shifts the whole list — `O(n)` per pop, `O(n²)` total in the worst case.
7. **Reusing one `level` list object.** Creating `level = []` outside the `while` loop makes all inner lists the same object.

**Debugging tip:** print `[n.val for n in queue]` at the top of each `while` round — each line should be exactly one level of the tree.

---

## 13. Practice Questions

**Q1. What does `levelOrder` return for `root = [1,2,3,4,null,null,5]`?**

<details><summary>Hint</summary>Draw the tree: `2` gets `4, null`; `3` gets `null, 5`.</summary></details>

**Answer:** `[[1],[2,3],[4,5]]`.

```text
        1
       / \
      2   3
     /     \
    4       5
```

Level 2 contains `4` (under `2`) and `5` (under `3`), left to right.

**Q2. Zigzag Level Order (LeetCode 103): alternate left-to-right and right-to-left per level.**

<details><summary>Hint</summary>Do the normal BFS and reverse every second level before saving it.</summary></details>

**Answer:**

```python
from collections import deque


def zigzag(root):
    if root is None:
        return []
    result, queue, left_to_right = [], deque([root]), True
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(level if left_to_right else level[::-1])
        left_to_right = not left_to_right
    return result


ex1 = TreeNode(3, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))
assert zigzag(ex1) == [[3], [20, 9], [15, 7]]
assert zigzag(None) == []
```

**Q3. Right Side View (LeetCode 199): the value you'd see from the right of each level.**

<details><summary>Hint</summary>It's the last value of each level.</summary></details>

**Answer:**

```python
from collections import deque


def right_side_view(root):
    view, queue = [], deque([root] if root else [])
    while queue:
        size = len(queue)
        for i in range(size):
            node = queue.popleft()
            if i == size - 1:          # last node of this level
                view.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    return view


tree = TreeNode(1, TreeNode(2, None, TreeNode(5)), TreeNode(3, None, TreeNode(4)))
assert right_side_view(tree) == [1, 3, 4]
assert right_side_view(TreeNode(1, TreeNode(2))) == [1, 2]   # a left node is visible if nothing is to its right
```

**Q4. Average of Levels (LeetCode 637): return the average value of each level.**

<details><summary>Hint</summary>Same loop; sum each level and divide by its size.</summary></details>

**Answer:**

```python
from collections import deque


def average_of_levels(root):
    averages, queue = [], deque([root])
    while queue:
        size, total = len(queue), 0
        for _ in range(size):
            node = queue.popleft()
            total += node.val
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        averages.append(total / size)
    return averages


ex1 = TreeNode(3, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))
assert average_of_levels(ex1) == [3.0, 14.5, 11.0]
```

(LeetCode 637 guarantees at least one node, so the root is never `None` here.)

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** BFS with a queue + level-size snapshot.
- **Key idea:** `while queue:` → `for _ in range(len(queue)):` pop, record value, push left then right → save the level.
- **Time:** `O(n)`.
- **Auxiliary space:** `O(w)` for the queue (up to about `n/2`); DFS alternative `O(h)`.
- **Recursion warning:** a 2000-node chain is deeper than Python's default limit of 1000, so the BFS version is the safe one.
- **One-line memory hook:** *"Count the line, photograph that many, send their kids to the back."*

### Completion checklist

- [x] Problem requirements verified
- [x] Examples and constraints verified
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force solution written and tested
- [x] Optimized Python solutions (BFS and recursive DFS) written and tested (`tools/tests/p045.py`)
- [x] Line-by-line explanation written
- [x] Dry run completed with a real example
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
