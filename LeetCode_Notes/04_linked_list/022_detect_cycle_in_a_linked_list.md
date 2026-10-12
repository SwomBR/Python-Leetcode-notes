# 022. Detect Cycle in a Linked List

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Linked List Cycle |
| **LeetCode number** | 141 |
| **Topic (source list)** | Linked List |
| **Also uses** | Two Pointers (fast/slow), Hash Table |
| **Difficulty** | Easy |
| **LeetCode URL** | <https://leetcode.com/problems/linked-list-cycle/> |
| **Pattern** | Floyd's cycle detection ("tortoise and hare") |

---

## 2. Problem Explanation

### Linked list primer

A **singly linked list** is a chain of **nodes**. Each node has a `val` (its value) and a `next` reference pointing to the following node, or `None` at the end. LeetCode provides the node class (shown here as a comment, exactly as in the editor — you don't write it yourself):

```text
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None
```

(For this problem LeetCode's comment uses the older constructor `ListNode(x)`. It does not matter for our solution, because we never create nodes — we only follow `next`.)

A normal list ends: `1 -> 2 -> 3 -> None`. A list **with a cycle** never ends, because some node's `next` points back to an earlier node:

```text
3 -> 2 -> 0 -> -4
     ^          |
     |__________|
```

Here the last node (`-4`) points back to node `2`, so following `next` goes round and round forever.

### What are we given?

`head` — the first node of a linked list (or `None` for an empty list). **That's the only argument.**

### What must we return?

`True` if the list contains a cycle (some node can be reached again by repeatedly following `next`), otherwise `False`.

### What is `pos`?

The examples mention `pos`. It is only LeetCode's way of **describing the test input**: `pos` is the index of the node that the last node's `next` points back to, and `pos = -1` means the last node points to `None` (no cycle). **`pos` is not passed to your function** — you must discover the cycle by walking the list.

### Examples

**Example 1**

```text
Input:  head = [3, 2, 0, -4], pos = 1
Output: true
```

The last node (`-4`) links back to the node at index 1 (value `2`), forming a loop.

**Example 2**

```text
Input:  head = [1, 2], pos = 0
Output: true
```

The last node (`2`) links back to the node at index 0 (value `1`): `1 -> 2 -> 1 -> 2 -> …`

**Example 3**

```text
Input:  head = [1], pos = -1
Output: false
```

A single node whose `next` is `None` — the walk ends, so there is no cycle.

### Constraints

- The number of nodes in the list is in the range `[0, 10^4]`.
- `-10^5 <= Node.val <= 10^5`
- `pos` is `-1` or a valid index in the linked list.

**Follow-up:** Can you solve it using `O(1)` (constant) memory?

---

## 3. Everyday Analogy

> **Explain it like I'm five**

Two kids go running along a path: a **slow turtle** that takes one step at a time and a **fast rabbit** that takes two steps at a time. They both start at the same spot.

- If the path is a **straight road** with an end, the rabbit simply reaches the end first, and we know there's no loop.
- If the path is a **round running track**, the rabbit never finds an end. Instead, because it's faster, it eventually comes around from behind and **lands on the same spot as the turtle**. The moment they meet, we know the track is a loop!

The turtle and rabbit don't need a notebook to remember where they've been — they just keep running. That's why this trick uses almost no memory.

---

## 4. Step-by-Step Logic

1. **Why can't we just walk until we hit `None`?** If there's a cycle, we'd never hit `None` — the loop would run forever.
2. **Simple idea: remember visited nodes.** Store every node we pass in a set. If we ever arrive at a node already in the set, we've gone around a loop. If we reach `None`, there's no loop. This works, but needs `O(n)` memory.
3. **Important detail:** remember the **node objects**, not their values. Different nodes can hold the same value (e.g. `[5, 5, 5]` with no cycle).
4. **Constant-memory idea:** use two pointers moving at different speeds — `slow` moves 1 step, `fast` moves 2 steps per round.
5. **No cycle →** `fast` reaches the end (`fast` or `fast.next` becomes `None`). Return `False`.
6. **Cycle →** both pointers eventually enter the loop. Once inside, each round `fast` gains exactly one step on `slow`, so the gap between them shrinks by 1 every round and must eventually become 0 — they land on the **same node**. Return `True`.
7. **Check `fast and fast.next` before jumping** two steps, otherwise `fast.next.next` crashes on `None`.

---

## 5. Brute-Force Solution

### Algorithm

1. Create an empty set `visited`.
2. Walk the list from `head`:
   - If the current node is already in `visited`, return `True`.
   - Otherwise add it and move to `next`.
3. If the walk reaches `None`, return `False`.

### Python code

```python
from typing import Optional


class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        visited = set()          # stores node OBJECTS, not values
        node = head
        while node:
            if node in visited:  # we've been here before -> loop
                return True
            visited.add(node)
            node = node.next
        return False             # reached None -> the list ends
```

### Explanation

- A `ListNode` object is hashable by **identity** by default (its class doesn't define `__eq__`/`__hash__`), so `node in visited` asks "is this exact node object stored?" — not "is some node with the same value stored?".
- In a cyclic list, the first node to be visited twice is the node where the loop starts.
- In a normal list, every node is new, and we eventually reach `None`.

### Complexity

- **Time:** `O(n)` — each node is added once; with a cycle we stop at the first repeated node, after at most `n + 1` steps. Set operations are `O(1)` on average.
- **Auxiliary space:** `O(n)` — the set can hold every node.
- **Trade-off:** It's fast and easy to reason about, but it does not meet the `O(1)` memory follow-up.

---

## 6. Optimized Solution

### Idea — Floyd's tortoise and hare

Move `slow` one step and `fast` two steps per round. If `fast` runs off the end, there is no cycle. If they ever point to the same node, there is a cycle.

### Algorithm

1. `slow = fast = head`.
2. While `fast` is not `None` and `fast.next` is not `None`:
   - `slow = slow.next`
   - `fast = fast.next.next`
   - If `slow is fast`, return `True`.
3. Return `False`.

### Python code (LeetCode-ready)

```python
from typing import Optional


class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        slow = fast = head

        while fast and fast.next:     # fast can safely take two steps
            slow = slow.next          # tortoise: 1 step
            fast = fast.next.next     # hare: 2 steps
            if slow is fast:          # same node object -> they met in a loop
                return True

        return False                  # fast reached the end -> no loop
```

---

## 7. Line-by-Line Explanation

| Line | What it does | Why |
|---|---|---|
| `slow = fast = head` | Both pointers start at the first node. | Starting together is simplest; we only compare **after** moving, so the start doesn't count as a meeting. |
| `while fast and fast.next:` | Continue only if `fast` can move two steps. | If `fast` is `None` or `fast.next` is `None`, the list has an end, so there is no cycle. It also prevents `AttributeError` on `None.next`. For an empty list (`head = None`) the loop never runs. |
| `slow = slow.next` | Moves the slow pointer one node. | `slow` is always behind `fast`, so if `fast` could move, `slow.next` exists. |
| `fast = fast.next.next` | Moves the fast pointer two nodes. | Twice the speed means it gains one node on `slow` every round. |
| `if slow is fast:` | Checks whether both refer to the **same node object**. | `is` compares identity. Comparing `slow.val == fast.val` would be wrong — distinct nodes can share a value. |
| `return True` | Reports a cycle. | Two pointers can only meet again (after starting) if the path loops. |
| `return False` | Reports no cycle. | `fast` found the end of the list. |

**Why must they meet (and not jump over each other)?** Once both are inside a loop of length `L`, let `d` be how many steps `fast` is *behind* `slow` along the loop. Each round, `slow` moves 1 and `fast` moves 2, so `d` drops by exactly 1. Since `d` decreases one at a time, it hits `0` exactly — `fast` can't skip past `slow`. This takes at most `L` rounds after `slow` enters the loop.

---

## 8. Dry Run

**Input:** `head = [3, 2, 0, -4]`, `pos = 1`

Label the nodes by index so equal-looking values can't confuse us:

```text
n0(3) -> n1(2) -> n2(0) -> n3(-4)
          ^                  |
          |__________________|      (n3.next = n1)
```

| Round | `slow` moves to | `fast` moves to (two steps) | `slow is fast`? | Action |
|---|---|---|---|---|
| start | n0 (3) | n0 (3) | — (not checked) | enter loop |
| 1 | n1 (2) | n0 → n1 → **n2 (0)** | No | continue |
| 2 | n2 (0) | n2 → n3 → **n1 (2)** (wrapped around) | No | continue |
| 3 | n3 (-4) | n1 → n2 → **n3 (-4)** | **Yes** | return `True` |

**Result:** `true` ✅

**Second dry run:** `head = [1, 2]`, `pos = 0` → `n0(1) -> n1(2) -> n0 …`

| Round | `slow` | `fast` | Same node? |
|---|---|---|---|
| 1 | n1 | n0 → n1 → n0 | No |
| 2 | n0 | n0 → n1 → n0 | **Yes** → `True` ✅ |

**Third dry run:** `head = [1]`, `pos = -1` → `n0(1) -> None`. At the loop check, `fast = n0` but `fast.next = None`, so the loop body never runs and we return `False` ✅.

**Brute-force check on Example 1:** `visited` grows `{n0}`, `{n0, n1}`, `{n0, n1, n2}`, `{n0, n1, n2, n3}`; then `n3.next` is `n1`, which is already in `visited` → `True` ✅.

---

## 9. Concepts, Data Structures, and Patterns

- **Fast and slow pointers (Floyd's cycle detection):** two references moving at different speeds through the same structure. Besides detecting cycles, the same idea finds the **middle** of a list (when `fast` reaches the end, `slow` is in the middle) — used in [026_reorder_list.md](026_reorder_list.md).
- **Identity vs. equality:** `a is b` asks "same object?", `a == b` asks "same value?". Cycle detection is about the same *node*, so we use `is` (and a set of node objects in the brute force).
- **Hash set:** `O(1)` average membership tests; the classic way to detect "have I seen this before?".
- **Space–time trade-off:** the set uses `O(n)` memory; Floyd's algorithm uses `O(1)` memory with the same `O(n)` time.
- **Related notes in this project:**
  - [021_reverse_a_linked_list.md](021_reverse_a_linked_list.md) — basic pointer handling.
  - [025_remove_nth_node_from_end_of_list.md](025_remove_nth_node_from_end_of_list.md) — another two-pointer technique (a fixed gap instead of different speeds).
  - Linked List Cycle II (LeetCode 142) finds *where* the cycle starts (Practice Q2), and Find the Duplicate Number (LeetCode 287) applies the same algorithm to an array.

---

## 10. Complexity Analysis

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Hash set of visited nodes (brute force) | `O(n)` average | `O(n)` | Every node is visited and stored at most once. |
| Floyd's fast/slow pointers (optimized) | `O(n)` | `O(1)` | See below. Only two pointer variables. |

**Why Floyd's is `O(n)`:**

- **No cycle:** `fast` reaches the end after about `n / 2` rounds.
- **Cycle:** let `μ` be the number of nodes before the loop and `L` the loop length (`μ + L = n`). `slow` enters the loop after `μ` rounds; from then on the gap closes by 1 per round, so they meet within at most `L` more rounds. Total rounds `<= μ + L = n`, i.e. `O(n)`.

---

## 11. Edge Cases

| Case | Input | Expected result | Why it works |
|---|---|---|---|
| Empty list | `head = []`, `pos = -1` | `false` | `fast` is `None`; loop never runs. |
| Single node, no cycle | `[1]`, `pos = -1` | `false` | `fast.next` is `None`. |
| Single node pointing to itself | `[1]`, `pos = 0` | `true` | Round 1: `slow = n0`, `fast = n0` → meet. |
| Two nodes, no cycle | `[1, 2]`, `pos = -1` | `false` | After round 1, `fast` is `None`. |
| Tail points to itself | `[1, 2, 3]`, `pos = 2` | `true` | Loop of length 1 at the end; both pointers get trapped on `n2`. |
| Whole list is a loop | `[1, 2]`, `pos = 0` | `true` | Example 2. |
| Equal values, no cycle | `[5, 5, 5, 5]`, `pos = -1` | `false` | We compare node identity, not values. |
| Largest input | `10^4` nodes | `true`/`false` as built | Linear time, constant memory. |

---

## 12. Common Mistakes and Debugging

1. **Comparing values (`slow.val == fast.val`) instead of nodes (`slow is fast`).** For `[1, 2, 2]` with `pos = -1` (no cycle), after round 1 `slow` is the first `2` and `fast` is the second `2`. Their values are equal, so a value comparison wrongly returns `True`. Always compare identity.
2. **Checking `slow is fast` before moving.** They start equal, so you'd return `True` immediately for every non-empty list.
3. **Loop condition `while fast.next:`** crashes when `fast` itself is `None` (e.g. empty list, or after jumping past the end of an even-length list). Use `while fast and fast.next:`.
4. **Storing values in the brute-force set.** `visited.add(node.val)` reports a cycle for `[1, 1]` with `pos = -1`. Store nodes.
5. **Trying to "print the list" while debugging a cyclic list.** It never ends. Add a step limit to any debug print.
6. **Relying on the node-count constraint** ("if I walk more than 10^4 steps, there must be a loop"). It happens to work for these limits, but it isn't a real algorithm and breaks if limits change.

**Debugging tip:** print `slow.val, fast.val` (or `id(slow), id(fast)`) each round for Example 1 and compare with the dry-run table.

---

## 13. Practice Questions

**Q1. For `head = [1, 2, 3, 4, 5, 6]` with `pos = 2` (`6` links back to `3`), in which round do `slow` and `fast` meet, and on which node?**

<details><summary>Hint</summary>Write the node sequence for `fast`: it visits every second node, wrapping from `6` back to `3`.</summary></details>

**Answer:** Nodes are `n0..n5` with values `1..6`, and `n5.next = n2`.

| Round | `slow` | `fast` |
|---|---|---|
| 1 | n1 (2) | n2 (3) |
| 2 | n2 (3) | n4 (5) |
| 3 | n3 (4) | n5 → n2 = n2 (3) |
| 4 | n4 (5) | n4 (5) ✅ |

They meet in round 4 on the node with value `5`.

```python
def build_with_cycle(values, pos):
    nodes = [ListNode(v) for v in values]
    for a, b in zip(nodes, nodes[1:]):
        a.next = b
    if pos != -1:
        nodes[-1].next = nodes[pos]
    return nodes[0] if nodes else None


def meeting_point(head):
    slow = fast = head
    rounds = 0
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        rounds += 1
        if slow is fast:
            return rounds, slow.val
    return None


assert meeting_point(build_with_cycle([1, 2, 3, 4, 5, 6], 2)) == (4, 5)
assert meeting_point(build_with_cycle([3, 2, 0, -4], 1)) == (3, -4)
assert meeting_point(build_with_cycle([1, 2, 3], -1)) is None
```

**Q2. Return the node where the cycle begins, or `None` if there is no cycle (LeetCode 142), in `O(1)` space.**

<details><summary>Hint</summary>After `slow` and `fast` meet, move one pointer back to `head`. Now move both pointers one step at a time; they meet at the cycle's entrance.</summary></details>

**Answer:** If `μ` nodes come before the loop, the math of Floyd's algorithm shows that walking `μ` steps forward from the meeting point (possibly going around the loop several times) lands exactly on the loop entrance. So a pointer from `head` and a pointer from the meeting point, both moving one step at a time, arrive at the entrance together.

```python
def build_with_cycle(values, pos):
    nodes = [ListNode(v) for v in values]
    for a, b in zip(nodes, nodes[1:]):
        a.next = b
    if pos != -1:
        nodes[-1].next = nodes[pos]
    return (nodes[0] if nodes else None), nodes


def detect_cycle_start(head):
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow is fast:
            finder = head
            while finder is not slow:
                finder, slow = finder.next, slow.next
            return finder
    return None


head, nodes = build_with_cycle([3, 2, 0, -4], 1)
assert detect_cycle_start(head) is nodes[1]
head, nodes = build_with_cycle([1, 2], 0)
assert detect_cycle_start(head) is nodes[0]
head, nodes = build_with_cycle([1], -1)
assert detect_cycle_start(head) is None
head, nodes = build_with_cycle([1, 2, 3, 4, 5, 6], 2)
assert detect_cycle_start(head) is nodes[2]
```

**Q3. Return the length of the cycle (0 if there is none).**

<details><summary>Hint</summary>Once the pointers meet, you are standing inside the loop. Walk around it once and count.</summary></details>

**Answer:**

```python
def build_with_cycle(values, pos):
    nodes = [ListNode(v) for v in values]
    for a, b in zip(nodes, nodes[1:]):
        a.next = b
    if pos != -1:
        nodes[-1].next = nodes[pos]
    return nodes[0] if nodes else None


def cycle_length(head):
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow is fast:
            length, node = 1, slow.next
            while node is not slow:
                node = node.next
                length += 1
            return length
    return 0


assert cycle_length(build_with_cycle([3, 2, 0, -4], 1)) == 3
assert cycle_length(build_with_cycle([1], 0)) == 1
assert cycle_length(build_with_cycle([1, 2, 3], -1)) == 0
```

**Q4. Return the middle node of a (non-cyclic) list; for an even length return the second middle (LeetCode 876).**

<details><summary>Hint</summary>Same loop as Floyd's algorithm, but you never compare — just return `slow` when `fast` reaches the end.</summary></details>

**Answer:**

```python
def build(values):
    head = None
    for v in reversed(values):
        head = ListNode(v, head)
    return head


def middle_node(head):
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
    return slow


assert middle_node(build([1, 2, 3, 4, 5])).val == 3
assert middle_node(build([1, 2, 3, 4, 5, 6])).val == 4
assert middle_node(build([9])).val == 9
```

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** Fast/slow pointers (Floyd's tortoise and hare).
- **Key idea:** `slow` moves 1, `fast` moves 2. `fast` hits `None` → no cycle. `slow is fast` → cycle.
- **Brute force:** set of visited **node objects** — `O(n)` time, `O(n)` space.
- **Time:** `O(n)`.
- **Auxiliary space:** `O(1)`.
- **One-line memory hook:** *"On a round track, the rabbit always catches the turtle."*

### Completion checklist

- [x] Problem requirements verified
- [x] Examples and constraints verified
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force solution written and tested
- [x] Optimized Python solution written and tested (`tools/tests/p022.py`)
- [x] Line-by-line explanation written
- [x] Dry run completed with a real example
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
