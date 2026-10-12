# 021. Reverse a Linked List

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Reverse Linked List |
| **LeetCode number** | 206 |
| **Topic (source list)** | Linked List |
| **Also uses** | Recursion |
| **Difficulty** | Easy |
| **LeetCode URL** | <https://leetcode.com/problems/reverse-linked-list/> |
| **Pattern** | In-place pointer reversal (`prev` / `curr` / `next`) |

---

## 2. Problem Explanation

### Linked list primer (read this first if linked lists are new to you)

A **singly linked list** is a chain of small objects called **nodes**. Each node stores:

- `val` — the value it holds, and
- `next` — a reference ("arrow") to the following node, or `None` if it is the last node.

LeetCode describes the node class in a comment at the top of the editor. You do **not** write this class yourself — LeetCode provides it:

```text
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
```

We draw a list with arrows: `1 -> 2 -> 3 -> None`. The variable `head` refers to the first node (`1`). An **empty list** is represented by `head = None`.

Unlike a Python list, you cannot jump to "the 3rd element" directly — you must start at `head` and follow `next` arrows one by one.

### What are we given?

`head` — the first node of a singly linked list (possibly `None`, meaning the list is empty).

### What must we return?

The head of the **same list turned around**, so the last node becomes the first and every arrow points the opposite way.

### The rules

1. Reverse the order of the nodes and return the new first node.
2. An empty list stays empty (return `None`).
3. The usual expectation is to re-point the existing nodes' `next` arrows rather than build a brand-new list (both are accepted by the judge, but re-pointing is the standard, memory-light solution).

### Examples

**Example 1**

```text
Input:  head = [1, 2, 3, 4, 5]
Output: [5, 4, 3, 2, 1]
```

`1 -> 2 -> 3 -> 4 -> 5 -> None` becomes `5 -> 4 -> 3 -> 2 -> 1 -> None`.

**Example 2**

```text
Input:  head = [1, 2]
Output: [2, 1]
```

**Example 3**

```text
Input:  head = []
Output: []
```

An empty list reversed is still empty.

(LeetCode shows lists as Python-style brackets for readability; your function actually receives the `ListNode` at the front, or `None`.)

### Constraints

- The number of nodes in the list is in the range `[0, 5000]`.
- `-5000 <= Node.val <= 5000`

**Follow-up:** A linked list can be reversed either iteratively or recursively. Could you implement both? (Both are given below.)

---

## 3. Everyday Analogy

> **Explain it like I'm five**

Imagine a line of kids playing "follow the leader". Each kid points at the kid **in front of them** (that's the `next` arrow). The last kid points at nobody.

Now the teacher says: *"Turn the line around!"* Instead of making everybody run to new spots, we walk down the line and ask each kid to **turn and point at the kid behind them** instead.

There's one danger: when a kid turns around, they stop pointing at the kid in front — and if we weren't paying attention, we'd forget where the rest of the line is! So before each kid turns, we **hold a sticky note** with the name of the next kid in line. Then the kid turns around, and we use the sticky note to walk to the next kid.

When we run out of kids, the last kid we visited is the new leader.

---

## 4. Step-by-Step Logic

1. **What changes?** Only the arrows. Node `2` used to point to `3`; afterwards it must point to `1`. So each node's `next` must point to the node that was **before** it.
2. **Who comes before the first node?** Nobody — so the old head must point to `None`. It becomes the new tail.
3. **Track two things while walking:** `prev` (the node just behind us, already reversed) and `curr` (the node we're fixing now). Start with `prev = None`, `curr = head`.
4. **Don't lose the rest of the list.** Before changing `curr.next`, save it: `nxt = curr.next`.
5. **Flip the arrow:** `curr.next = prev`.
6. **Step forward:** `prev = curr`, `curr = nxt`.
7. **Stop when `curr` is `None`.** At that moment `prev` is the old last node — the new head. Return `prev`.
8. **Recursive view (follow-up):** "Reverse everything after me, then make the node after me point back to me." The smallest list (0 or 1 node) is already reversed.

---

## 5. Brute-Force Solution

### Algorithm

1. Walk the list and copy every value into a Python list.
2. Walk the list again, writing the values back in reverse order (from the end of the Python list).
3. Return `head` — the same first node, now holding the last value.

### Python code

```python
from typing import Optional


class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        values = []
        node = head
        while node:                 # pass 1: collect the values
            values.append(node.val)
            node = node.next

        node = head
        while node:                 # pass 2: write them back in reverse
            node.val = values.pop() # pop() takes from the end of the list
            node = node.next

        return head
```

### Explanation

- Pass 1 records the values in order, e.g. `[1, 2, 3, 4, 5]`.
- Pass 2 visits the nodes from front to back, and `values.pop()` hands out `5, 4, 3, 2, 1` in that order.
- The node objects never move and no arrows change — we only swap the **values** inside them. The printed list is reversed, which is what the judge checks.

### Complexity

- **Time:** `O(n)` — two passes over `n` nodes.
- **Auxiliary space:** `O(n)` — the `values` list holds a copy of every value.
- **Trade-off:** It is correct and easy, but it uses extra memory and it "cheats" by moving values instead of reversing the structure. In real programs nodes often carry large payloads or are referenced from elsewhere, so you're expected to re-link the nodes in `O(1)` extra space.

---

## 6. Optimized Solution

### Idea — iterative pointer reversal

Walk the list once with `prev` and `curr`. At each node, remember the next node, flip the arrow backwards, and move both pointers one step forward.

### Algorithm

1. `prev = None`, `curr = head`.
2. While `curr` is not `None`:
   - `nxt = curr.next` (save the rest of the list)
   - `curr.next = prev` (flip the arrow)
   - `prev = curr`, `curr = nxt` (advance)
3. Return `prev`.

### Python code (LeetCode-ready, iterative)

```python
from typing import Optional


class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        prev = None
        curr = head

        while curr:
            nxt = curr.next   # 1. remember the rest of the list
            curr.next = prev  # 2. flip this node's arrow backwards
            prev = curr       # 3. prev moves up to this node
            curr = nxt        # 4. curr moves to the saved next node

        return prev           # prev is the old tail = new head
```

### Follow-up: recursive version

```python
from typing import Optional


class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # Base case: an empty list or a single node is already reversed.
        if head is None or head.next is None:
            return head

        # Reverse everything after head. new_head is the old last node.
        new_head = self.reverseList(head.next)

        # head.next is now the TAIL of the reversed rest; hang head after it.
        head.next.next = head
        head.next = None      # head becomes the new tail

        return new_head
```

How it works: for `1 -> 2 -> 3 -> None`, the call on `1` first reverses `2 -> 3` into `3 -> 2 -> None`. Node `1` still points to `2`, which is now the tail of that reversed piece, so `head.next.next = head` makes `2 -> 1`, and `head.next = None` ends the list: `3 -> 2 -> 1 -> None`.

**Recursion depth warning:** the recursive version makes one nested call per node, so it uses `O(n)` call-stack space. Python's default recursion limit is about 1000, and the constraints allow 5000 nodes, so in a plain Python environment a long list can raise `RecursionError`. The iterative version has no such risk and is the one to prefer in Python.

---

## 7. Line-by-Line Explanation

(Iterative version)

| Line | What it does | Why |
|---|---|---|
| `prev = None` | `prev` is the head of the part that is already reversed. | At the start nothing is reversed. `None` is also exactly what the old head must point to once it becomes the tail. |
| `curr = head` | `curr` is the node we are about to flip. | We start at the front. |
| `while curr:` | Loop until we fall off the end. | `curr` becomes `None` after the last node is processed. An empty list skips the loop entirely. |
| `nxt = curr.next` | Saves the rest of the original list. | The next line overwrites `curr.next`; without this copy, we'd lose every node after `curr`. |
| `curr.next = prev` | Flips the arrow to point backwards. | This is the actual reversal step. |
| `prev = curr` | The reversed part now starts at `curr`. | Next iteration, the following node must point to this one. |
| `curr = nxt` | Moves to the next unprocessed node. | Uses the saved reference. |
| `return prev` | Returns the new head. | When the loop ends, `prev` is the last node we flipped — the old tail. For an empty list it is `None`, which is correct. |

(Recursive version, key lines)

| Line | Why |
|---|---|
| `if head is None or head.next is None: return head` | Base case. An empty list or a one-node list is its own reverse. This also stops the recursion. |
| `new_head = self.reverseList(head.next)` | Trust the recursion: it reverses the rest and returns its new head (the original last node). |
| `head.next.next = head` | `head.next` is still the node right after `head`, which is now the **tail** of the reversed rest. Point it back at `head`. |
| `head.next = None` | Cut the old forward arrow so `head` becomes the end of the list (otherwise `1 <-> 2` would form a cycle). |
| `return new_head` | Every level returns the same new head up the chain. |

---

## 8. Dry Run

**Input:** `head = [1, 2, 3, 4, 5]` (iterative version)

Start: `prev = None`, `curr = 1`. Original list: `1 -> 2 -> 3 -> 4 -> 5 -> None`.

| Iteration | `curr` | `nxt = curr.next` | After `curr.next = prev` | `prev` after | `curr` after | Reversed part (from `prev`) | Remaining part (from `curr`) |
|---|---|---|---|---|---|---|---|
| 1 | 1 | 2 | `1 -> None` | 1 | 2 | `1 -> None` | `2 -> 3 -> 4 -> 5 -> None` |
| 2 | 2 | 3 | `2 -> 1` | 2 | 3 | `2 -> 1 -> None` | `3 -> 4 -> 5 -> None` |
| 3 | 3 | 4 | `3 -> 2` | 3 | 4 | `3 -> 2 -> 1 -> None` | `4 -> 5 -> None` |
| 4 | 4 | 5 | `4 -> 3` | 4 | 5 | `4 -> 3 -> 2 -> 1 -> None` | `5 -> None` |
| 5 | 5 | None | `5 -> 4` | 5 | None | `5 -> 4 -> 3 -> 2 -> 1 -> None` | (empty) |

`curr` is `None`, so the loop stops and we return `prev` (node `5`).

**Result:** `5 -> 4 -> 3 -> 2 -> 1 -> None`, i.e. `[5, 4, 3, 2, 1]` ✅

**Second dry run (recursive), `head = [1, 2]`:**

| Call | `head` | What happens | Returns |
|---|---|---|---|
| `reverseList(1)` | 1 | `head.next` is 2, not a base case → calls `reverseList(2)` | (waits) |
| `reverseList(2)` | 2 | `head.next` is `None` → base case | node 2 |
| back in `reverseList(1)` | 1 | `new_head = 2`; `head.next.next = head` makes `2 -> 1`; `head.next = None` makes `1 -> None` | node 2 |

**Result:** `2 -> 1 -> None`, i.e. `[2, 1]` ✅

**Example 3:** `head = None` → the iterative loop never runs and `prev = None` is returned; the recursive base case returns `None` immediately. Output `[]` ✅

---

## 9. Concepts, Data Structures, and Patterns

- **Singly linked list:** nodes connected by one-way `next` references. Moving forward is easy; moving backward is impossible without extra bookkeeping — which is exactly why reversing needs `prev`.
- **Pointer (reference) manipulation:** in Python, `curr.next = prev` changes which object the attribute refers to; no nodes are copied.
- **The "save next before you overwrite it" rule:** the most important habit in linked-list code. Whenever you change `x.next`, ask: "Do I still need the old `x.next`?"
- **Recursion:** a function that solves a smaller copy of the same problem. Needs a **base case** (0 or 1 node) and a step that combines the smaller answer with the current node. Costs `O(n)` stack space.
- **In-place algorithms:** the iterative version uses `O(1)` extra memory by reusing the existing nodes.
- **Related notes in this project:**
  - [026_reorder_list.md](026_reorder_list.md) reverses the second half of a list as one of its steps.
  - [022_detect_cycle_in_a_linked_list.md](022_detect_cycle_in_a_linked_list.md) introduces the fast/slow pointer technique (also used to find the middle of a list).
  - [023_merge_two_sorted_lists.md](023_merge_two_sorted_lists.md) and [025_remove_nth_node_from_end_of_list.md](025_remove_nth_node_from_end_of_list.md) use the same "re-point `next`" skills.
  - Classic follow-ons: Reverse Linked List II (LeetCode 92), Palindrome Linked List (LeetCode 234), Reverse Nodes in k-Group (LeetCode 25).

---

## 10. Complexity Analysis

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Brute force (copy values, write back reversed) | `O(n)` | `O(n)` | Two passes; the Python list stores all `n` values. |
| Iterative pointer reversal (optimized) | `O(n)` | `O(1)` | One pass; each node's arrow is flipped once. Only `prev`, `curr`, `nxt` are stored. |
| Recursive | `O(n)` | `O(n)` | One call per node; every call stays on the call stack until the deepest call returns, so the stack holds up to `n` frames. |

Every approach must at least look at all `n` nodes, so `O(n)` time is optimal.

---

## 11. Edge Cases

| Case | Input | Expected result | Why it works |
|---|---|---|---|
| Empty list | `[]` | `[]` | Loop never runs; return `prev = None`. |
| Single node | `[7]` | `[7]` | One iteration: `7.next = None`; return node 7. |
| Two nodes | `[1, 2]` | `[2, 1]` | Smallest case where arrows actually change direction. |
| Duplicate values | `[3, 3, 3]` | `[3, 3, 3]` | Arrows are reversed even though the values look the same. |
| Extreme values | `[-5000, 5000]` | `[5000, -5000]` | Values are never inspected, only moved. |
| Reverse twice | `[1, 2, 3]` reversed twice | `[1, 2, 3]` | Reversal undoes itself — a handy self-test. |
| Long list (5000 nodes) | `[1, …, 5000]` | `[5000, …, 1]` | Fine iteratively; the recursive version may hit Python's default recursion limit. |

---

## 12. Common Mistakes and Debugging

1. **Overwriting `curr.next` before saving it.** Writing `curr.next = prev` first and then `curr = curr.next` moves `curr` *backwards* to `prev` — you lose the rest of the list (and loop forever or stop early). Always save `nxt` first.
2. **Returning `head` instead of `prev`.** After reversal, the old `head` is the **tail**; returning it gives a one-node list `[1]`.
3. **Forgetting `head.next = None` in the recursive version.** The first two nodes would point at each other (`1 -> 2 -> 1 -> …`), creating a cycle — printing the list would never end.
4. **Base case only checks `head is None`.** Then a single node recurses into `None`, gets `None` back, and `head.next.next` crashes with `AttributeError`. Check `head.next is None` too.
5. **Updating `prev` and `curr` in the wrong order.** `curr = nxt` followed by `prev = curr` sets both to the same node. Move `prev` first.
6. **Defining your own `ListNode` class on LeetCode.** It's already provided; redefining it can cause confusing type mismatches.

**Debugging tip:** write a tiny helper that prints a list (with a step limit so cycles don't hang), and print `prev` and `curr` lists after every iteration. They should match the "Reversed part" and "Remaining part" columns of the dry run.

---

## 13. Practice Questions

**Q1. For `head = [10, 20, 30]`, what do the reversed part and the remaining part look like after the second loop iteration?**

<details><summary>Hint</summary>Each iteration moves exactly one node from the front of the remaining part to the front of the reversed part.</summary></details>

**Answer:** After iteration 1: reversed `10 -> None`, remaining `20 -> 30 -> None`. After iteration 2: `20.next` now points to `10`, so the reversed part is `20 -> 10 -> None` (`prev = 20`) and the remaining part is `30 -> None` (`curr = 30`). One more iteration finishes the job with `30 -> 20 -> 10 -> None`.

**Q2. Reverse only the nodes from position `left` to position `right` (1-indexed), leaving the rest in place (LeetCode 92).**

<details><summary>Hint</summary>Use a dummy node before the head, walk to the node just before position `left`, then repeatedly move the node after the current one to the front of the sub-list ("head insertion").</summary></details>

**Answer:** Keep `before` fixed just in front of the sub-list and `curr` at the first sub-list node. Each step lifts the node after `curr` out and inserts it right after `before`. After `right - left` moves, the sub-list is reversed.

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


def reverse_between(head, left, right):
    dummy = ListNode(0, head)
    before = dummy
    for _ in range(left - 1):
        before = before.next
    curr = before.next
    for _ in range(right - left):
        moved = curr.next          # node to move to the front
        curr.next = moved.next     # unlink it
        moved.next = before.next   # put it at the front of the sub-list
        before.next = moved
    return dummy.next


assert to_list(reverse_between(build([1, 2, 3, 4, 5]), 2, 4)) == [1, 4, 3, 2, 5]
assert to_list(reverse_between(build([5]), 1, 1)) == [5]
assert to_list(reverse_between(build([1, 2, 3]), 1, 3)) == [3, 2, 1]
```

**Q3. Decide whether a linked list reads the same forwards and backwards (LeetCode 234) using `O(1)` extra space.**

<details><summary>Hint</summary>Find the middle with slow/fast pointers, reverse the second half, then compare the two halves node by node.</summary></details>

**Answer:** The slow pointer stops at the middle when the fast pointer reaches the end. Reversing from `slow` gives the second half backwards; walking both halves together compares mirror-image positions.

```python
def build(values):
    head = None
    for v in reversed(values):
        head = ListNode(v, head)
    return head


def reverse(head):
    prev = None
    while head:
        head.next, prev, head = prev, head, head.next
    return prev


def is_palindrome(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    second = reverse(slow)
    first = head
    while second:
        if first.val != second.val:
            return False
        first, second = first.next, second.next
    return True


assert is_palindrome(build([1, 2, 2, 1])) is True
assert is_palindrome(build([1, 2, 3, 2, 1])) is True
assert is_palindrome(build([1, 2])) is False
assert is_palindrome(build([7])) is True
```

(The one-line swap `head.next, prev, head = prev, head, head.next` works because Python evaluates the whole right-hand side first, then assigns left to right. It is compact but easy to get wrong — the four-line version in Section 6 is clearer.)

**Q4. Why does the iterative version use `O(1)` space but the recursive version uses `O(n)`, even though neither creates new nodes?**

<details><summary>Hint</summary>Where does a function keep its local variables while it waits for a nested call to finish?</summary></details>

**Answer:** Each recursive call gets its own stack frame (holding its own `head`). The call for node 1 can't finish until the call for node 2 finishes, and so on, so all `n` frames are alive at once at the deepest point. The iterative loop reuses the same three variables for every node.

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** In-place pointer reversal with `prev`, `curr`, `nxt`.
- **Key idea:** Save `next`, flip `curr.next` to `prev`, advance both. Return `prev`.
- **Recursive form:** reverse the rest, then `head.next.next = head; head.next = None`.
- **Time:** `O(n)`.
- **Auxiliary space:** `O(1)` iterative, `O(n)` recursive (call stack).
- **One-line memory hook:** *"Save, flip, step, step — then hand back `prev`."*

### Completion checklist

- [x] Problem requirements verified
- [x] Examples and constraints verified
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force solution written and tested
- [x] Optimized Python solution written and tested (`tools/tests/p021.py`)
- [x] Recursive follow-up solution written and tested
- [x] Line-by-line explanation written
- [x] Dry run completed with a real example
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
