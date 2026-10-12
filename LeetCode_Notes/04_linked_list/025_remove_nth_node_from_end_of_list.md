# 025. Remove Nth Node From End of List

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Remove Nth Node From End of List |
| **LeetCode number** | 19 |
| **Topic (source list)** | Linked List |
| **Also uses** | Two Pointers |
| **Difficulty** | Medium |
| **LeetCode URL** | <https://leetcode.com/problems/remove-nth-node-from-end-of-list/> |
| **Pattern** | Two pointers with a fixed gap + dummy node |

---

## 2. Problem Explanation

### Linked list primer

A **singly linked list** is a chain of **nodes**; each node has a value `val` and a reference `next` to the following node (`None` after the last node). LeetCode provides the class as a comment in the editor — you never define it yourself:

```text
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
```

We draw lists as `1 -> 2 -> 3 -> None`. To **remove** a node from a linked list, you make the node **before** it skip over it: `before.next = before.next.next`. The skipped node is no longer reachable from the head, so it is gone from the list.

### What are we given?

- `head` — the first node of a linked list (the list has at least one node).
- `n` — a positive whole number.

### What must we return?

The head of the list after deleting the node that is `n`-th **counting from the end** (the last node is 1st from the end, the one before it is 2nd from the end, and so on).

### The rules

1. Exactly one node is removed.
2. `n` is always valid: it is between 1 and the list length, so the node to remove always exists.
3. If the removed node is the first node, the head changes — return the new head (which may be `None` if the list had only one node).

### Examples

**Example 1**

```text
Input:  head = [1, 2, 3, 4, 5], n = 2
Output: [1, 2, 3, 5]
```

Counting from the end: `5` is 1st, `4` is 2nd. Removing `4` gives `1 -> 2 -> 3 -> 5`.

**Example 2**

```text
Input:  head = [1], n = 1
Output: []
```

The only node is also the 1st from the end; removing it leaves an empty list.

**Example 3**

```text
Input:  head = [1, 2], n = 1
Output: [1]
```

The last node (`2`) is removed.

### Constraints

- The number of nodes in the list is `sz`.
- `1 <= sz <= 30`
- `0 <= Node.val <= 100`
- `1 <= n <= sz`

**Follow-up:** Could you do this in one pass?

---

## 3. Everyday Analogy

> **Explain it like I'm five**

Kids are walking in a line through a dark tunnel, and you can only see the kid right in front of you. The teacher says: *"The 2nd kid from the end of the line must step out."* But you can't see the end!

Here's a trick using a **stick that is exactly 2 kids long**. Two helpers hold the stick: the **front helper** starts 2 kids ahead of the **back helper**. They walk forward together, always keeping the stick the same length.

When the front helper walks out of the tunnel (past the last kid), the back helper is standing right behind the kid who has to leave. The back helper taps that kid on the shoulder, and the kid steps out — the kids around them hold hands to close the gap.

Because the helpers walked together, they only went through the tunnel **once**.

---

## 4. Step-by-Step Logic

1. **Translate "from the end" into "from the start".** In a list of length `sz`, the `n`-th node from the end is at 0-based index `sz - n`. For Example 1: `5 - 2 = 3` → the node at index 3 is `4`. ✓
2. **To delete a node, stand on the node before it.** We need a pointer to index `sz - n - 1`, then do `prev.next = prev.next.next`.
3. **Problem: deleting the head** (`n == sz`) has no "node before". Fix: put a **dummy** node in front of `head`. Now every real node — including the head — has a predecessor. Return `dummy.next` at the end.
4. **Simple approach (two passes):** first walk the list to count `sz`, then walk again to the node before the target.
5. **One pass (follow-up):** we don't know `sz`, but we can keep two pointers a fixed distance apart. Move `fast` `n` nodes ahead of `head`, and start `slow` at the dummy. Then advance both together until `fast` falls off the end (`None`).
6. **Why that works:** `slow` starts one node *before* `head` and `fast` starts `n` nodes *after* `head`, so `fast` is always `n + 1` steps ahead of `slow`. When `fast` is `None` (one step past the last node), `slow` is `n + 1` steps behind that point — exactly the node **before** the `n`-th node from the end.

---

## 5. Brute-Force Solution

### Algorithm

1. Walk the list and store every node in a Python list `nodes`.
2. The target is at index `idx = len(nodes) - n`.
3. If `idx == 0`, the head is removed: return `head.next`.
4. Otherwise link the previous node past the target: `nodes[idx - 1].next = nodes[idx].next`, and return `head`.

### Python code

```python
from typing import Optional


class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        nodes = []
        node = head
        while node:                  # store every node so we can index into it
            nodes.append(node)
            node = node.next

        idx = len(nodes) - n         # 0-based index of the node to remove
        if idx == 0:                 # removing the head
            return head.next

        nodes[idx - 1].next = nodes[idx].next   # skip over the target
        return head
```

### Explanation

- Copying node references into a Python list gives us **random access**: we can jump straight to any index, which a linked list can't do.
- The head case is handled separately because it has no previous node.
- Only references are stored, not copies of the nodes, so relinking `nodes[idx - 1]` changes the real list.

### Complexity

- **Time:** `O(sz)` — one walk plus constant work.
- **Auxiliary space:** `O(sz)` — the Python list holds a reference to every node.
- **Trade-off:** easy to get right, but it spends memory proportional to the list size. The two-pointer solution needs only `O(1)` extra memory and also answers the one-pass follow-up.

---

## 6. Optimized Solution

### A middle step: count first, then remove (two passes, `O(1)` space)

```python
from typing import Optional


class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        length = 0
        node = head
        while node:                      # pass 1: count the nodes
            length += 1
            node = node.next

        dummy = ListNode(0, head)
        prev = dummy
        for _ in range(length - n):      # pass 2: stop just before the target
            prev = prev.next

        prev.next = prev.next.next
        return dummy.next
```

This already uses constant memory, but walks the list twice. Starting at `dummy` and taking `length - n` steps lands on the node at 0-based index `length - n - 1` — the one before the target (or on `dummy` itself when the head is removed).

### Idea — one pass with a fixed gap (follow-up)

Give `fast` a head start of `n` nodes, start `slow` at a dummy node before `head`, then move them together. When `fast` reaches `None`, `slow` is right before the node to delete.

### Algorithm

1. `dummy = ListNode(0, head)`.
2. `fast = head`; move `fast` forward `n` times.
3. `slow = dummy`.
4. While `fast` is not `None`: `slow = slow.next`, `fast = fast.next`.
5. `slow.next = slow.next.next`.
6. Return `dummy.next`.

### Python code (LeetCode-ready)

```python
from typing import Optional


class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        dummy = ListNode(0, head)   # gives the head a "previous" node

        fast = head
        for _ in range(n):          # open a gap of n nodes
            fast = fast.next

        slow = dummy
        while fast:                 # move both until fast falls off the end
            slow = slow.next
            fast = fast.next

        slow.next = slow.next.next  # slow is just before the target: skip it
        return dummy.next
```

---

## 7. Line-by-Line Explanation

(One-pass version)

| Line | What it does | Why |
|---|---|---|
| `dummy = ListNode(0, head)` | Creates a fake node whose `next` is the real head. | If the head itself must be removed, `slow` can stay on `dummy` and still do `slow.next = slow.next.next`. No special case needed. |
| `fast = head` | `fast` starts at the first real node. | We'll measure the gap from here. |
| `for _ in range(n): fast = fast.next` | Moves `fast` forward `n` nodes. | Since `n <= sz`, this never steps past `None` (at most it *becomes* `None` when `n == sz`). |
| `slow = dummy` | `slow` starts one node before the head. | Now `fast` is `n + 1` steps ahead of `slow`. |
| `while fast:` | Repeats until `fast` is `None`. | `None` is the position just after the last node. |
| `slow = slow.next; fast = fast.next` | Moves both one step, keeping the gap. | The gap stays `n + 1`. |
| `slow.next = slow.next.next` | Unlinks the target node. | `slow` is `n + 1` steps before `None`, i.e. the node just before the `n`-th from the end. |
| `return dummy.next` | Returns the (possibly new) head. | If the original head was removed, `dummy.next` now points to the second node (or `None`). Returning `head` would be wrong in that case. |

---

## 8. Dry Run

**Input:** `head = [1, 2, 3, 4, 5]`, `n = 2`

List with dummy: `D -> 1 -> 2 -> 3 -> 4 -> 5 -> None`

**Phase 1 — open the gap** (`fast` starts at node `1`):

| Step | `fast` after the step |
|---|---|
| 1 | 2 |
| 2 | 3 |

**Phase 2 — move together** (`slow` starts at `D`):

| Iteration | `slow` | `fast` | Gap (steps from `slow` to `fast`) |
|---|---|---|---|
| start | D | 3 | 3 (= `n + 1`) |
| 1 | 1 | 4 | 3 |
| 2 | 2 | 5 | 3 |
| 3 | 3 | None | 3 → loop stops |

**Phase 3 — remove:** `slow` is node `3`; `slow.next` is node `4` (the target). Set `3.next = 4.next = 5`.

```text
Before: D -> 1 -> 2 -> 3 -> 4 -> 5 -> None
After:  D -> 1 -> 2 -> 3 ------> 5 -> None
```

Return `dummy.next` (node `1`).

**Result:** `[1, 2, 3, 5]` ✅

**Second dry run (removing the head):** `head = [1]`, `n = 1`

| Step | `slow` | `fast` | Note |
|---|---|---|---|
| gap phase | — | 1 → None | one step |
| start loop | D | None | loop body never runs |
| remove | D | — | `D.next = D.next.next` = `1.next` = `None` |

Return `dummy.next` = `None`. **Result:** `[]` ✅ (returning `head` here would wrongly give `[1]`).

**Third dry run:** `head = [1, 2]`, `n = 1` → gap phase: `fast` = `2`. Loop: `slow = 1`, `fast = None`. Remove: `1.next = 2.next = None`. **Result:** `[1]` ✅

---

## 9. Concepts, Data Structures, and Patterns

- **Two pointers with a fixed gap ("runner" technique):** two references that move at the same speed but start a set distance apart. When the leader hits the end, the follower is a known distance from the end. Compare with the **different-speed** pointers in [022_detect_cycle_in_a_linked_list.md](022_detect_cycle_in_a_linked_list.md).
- **Dummy (sentinel) node:** removes the special case of deleting the head. Also used in [023_merge_two_sorted_lists.md](023_merge_two_sorted_lists.md) and [024_merge_k_sorted_lists.md](024_merge_k_sorted_lists.md).
- **Deleting from a singly linked list:** you need the **previous** node, because you change *its* `next`. A node can't unlink itself without help.
- **Index conversion:** `n`-th from the end = 0-based index `sz - n` from the start.
- **Random access via a Python list:** the brute force trades `O(sz)` memory for the ability to jump to any index.
- **Related notes in this project:** [021_reverse_a_linked_list.md](021_reverse_a_linked_list.md) (pointer basics), [026_reorder_list.md](026_reorder_list.md) (combines several linked-list techniques). Related LeetCode problems: Remove Linked List Elements (203), Delete the Middle Node of a Linked List (2095), Rotate List (61).

---

## 10. Complexity Analysis

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Brute force (store nodes in a Python list) | `O(sz)` | `O(sz)` | One walk; the list holds every node reference. |
| Count length, then remove (two passes) | `O(sz)` | `O(1)` | Up to `2·sz` steps, a few variables. |
| Fixed-gap two pointers (optimized, one pass) | `O(sz)` | `O(1)` | `fast` walks the list exactly once (`n` steps, then `sz - n` more); `slow` follows. Only `dummy`, `fast`, `slow` are extra. |

All three are linear; the optimized version wins on memory (vs. brute force) and on number of passes (vs. two-pass). With `sz <= 30`, all are instantly fast — the follow-up is about technique, not speed.

---

## 11. Edge Cases

| Case | Input | Expected result | Why it works |
|---|---|---|---|
| Single node | `[1]`, `n = 1` | `[]` | `slow` stays on `dummy`; `dummy.next` becomes `None`. |
| Remove the head | `[1, 2]`, `n = 2` | `[2]` | `fast` becomes `None` after the gap phase; `slow = dummy` removes node `1`. |
| Remove the head (longer) | `[1, 2, 3, 4, 5]`, `n = 5` | `[2, 3, 4, 5]` | Same reasoning: `n == sz`. |
| Remove the tail | `[1, 2]`, `n = 1` | `[1]` | `slow` ends on the second-to-last node. |
| Remove the tail (longer) | `[1, 2, 3, 4, 5]`, `n = 1` | `[1, 2, 3, 4]` | `slow.next.next` is `None`, so the tail is cut off. |
| Duplicate values | `[7, 7, 7]`, `n = 2` | `[7, 7]` | We remove by position, not value. |
| Maximum size | 30 nodes, any valid `n` | 29 nodes | Still a single pass. |

---

## 12. Common Mistakes and Debugging

1. **Returning `head` instead of `dummy.next`.** When the head is removed (`n == sz`), `head` still points to the deleted node. Example 2 would return `[1]` instead of `[]`.
2. **Starting `slow` at `head` instead of `dummy`.** Then `slow` ends **on** the target instead of before it, and removing the head becomes impossible without a special case.
3. **Wrong gap size.** If `fast` starts at `dummy` too, it must move `n + 1` steps; if it starts at `head`, `n` steps. Mixing the two conventions shifts the deletion by one node.
4. **Loop condition `while fast.next:`** with this setup stops one step early and deletes the wrong node (and crashes with `AttributeError` when `fast` is already `None` after the gap phase, e.g. Example 2).
5. **Off-by-one in the index formula.** The `n`-th from the end is index `sz - n` (0-based), not `sz - n + 1`.
6. **Trying to delete the node itself** with `slow = None` or `del slow` — that only changes your local variable. You must change the previous node's `next`.

**Debugging tip:** print the list with the dummy (`D -> 1 -> …`) and mark where `slow` and `fast` are after each iteration. The gap between them must always be `n + 1`.

---

## 13. Practice Questions

**Q1. For `head = [10, 20, 30, 40]` and `n = 3`, which node is removed, and where are `slow` and `fast` when the loop ends?**

<details><summary>Hint</summary>`sz = 4`, so the target index is `sz - n`. Then trace the gap phase (3 steps from `10`).</summary></details>

**Answer:** Target index `4 - 3 = 1` → value `20`. Gap phase: `fast` goes `10 → 20 → 30 → 40`. Loop: `slow = 10`, `fast = None` → stop. `slow` is on `10`, so `10.next = 30`. Result: `[10, 30, 40]`.

**Q2. Return the value of the `k`-th node from the end in one pass (without deleting anything).**

<details><summary>Hint</summary>Same gap idea, but start `slow` at `head` instead of a dummy, so it lands **on** the node instead of before it.</summary></details>

**Answer:**

```python
def build(values):
    head = None
    for v in reversed(values):
        head = ListNode(v, head)
    return head


def kth_from_end(head, k):
    fast = slow = head
    for _ in range(k):
        fast = fast.next
    while fast:
        slow, fast = slow.next, fast.next
    return slow.val


assert kth_from_end(build([1, 2, 3, 4, 5]), 2) == 4
assert kth_from_end(build([1, 2, 3, 4, 5]), 5) == 1
assert kth_from_end(build([9]), 1) == 9
```

**Q3. Remove every node whose value equals `val` (LeetCode 203).**

<details><summary>Hint</summary>Use a dummy node. Look at `curr.next`: if it should be removed, skip it **without** moving `curr`; otherwise move `curr` forward.</summary></details>

**Answer:**

```python
def build(values):
    head = None
    for v in reversed(values):
        head = ListNode(v, head)
    return head


def to_list(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


def remove_elements(head, val):
    dummy = ListNode(0, head)
    curr = dummy
    while curr.next:
        if curr.next.val == val:
            curr.next = curr.next.next   # skip, stay put (next may also match)
        else:
            curr = curr.next
    return dummy.next


assert to_list(remove_elements(build([1, 2, 6, 3, 4, 5, 6]), 6)) == [1, 2, 3, 4, 5]
assert to_list(remove_elements(build([7, 7, 7, 7]), 7)) == []
assert to_list(remove_elements(build([]), 1)) == []
```

**Q4. Delete the middle node of a list — index `sz // 2` (LeetCode 2095) — in one pass.**

<details><summary>Hint</summary>Combine ideas: a slow/fast pair moving at speeds 1 and 2, with `slow` starting at a dummy so it stops **before** the middle.</summary></details>

**Answer:** With `slow` at the dummy and `fast` at `head`, each round moves `slow` 1 and `fast` 2. When `fast` can't move two more steps, `slow` sits right before index `sz // 2`.

```python
def build(values):
    head = None
    for v in reversed(values):
        head = ListNode(v, head)
    return head


def to_list(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


def delete_middle(head):
    dummy = ListNode(0, head)
    slow, fast = dummy, head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
    slow.next = slow.next.next
    return dummy.next


assert to_list(delete_middle(build([1, 3, 4, 7, 1, 2, 6]))) == [1, 3, 4, 1, 2, 6]
assert to_list(delete_middle(build([1, 2, 3, 4]))) == [1, 2, 4]
assert to_list(delete_middle(build([2, 1]))) == [2]
assert to_list(delete_middle(build([5]))) == []
```

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** Two pointers with a fixed gap + dummy node.
- **Key idea:** `fast` moves `n` steps from `head`; `slow` starts at `dummy`; move both until `fast` is `None`; then `slow.next = slow.next.next`; return `dummy.next`.
- **Time:** `O(sz)`, one pass.
- **Auxiliary space:** `O(1)`.
- **One-line memory hook:** *"Hold a stick n + 1 long; when the front falls off the end, the back is right behind the victim."*

### Completion checklist

- [x] Problem requirements verified
- [x] Examples and constraints verified
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force solution written and tested
- [x] Two-pass intermediate solution written and tested
- [x] Optimized Python solution written and tested (`tools/tests/p025.py`)
- [x] Line-by-line explanation written
- [x] Dry run completed with a real example
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
