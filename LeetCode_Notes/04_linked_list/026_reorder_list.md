# 026. Reorder List

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Reorder List |
| **LeetCode number** | 143 |
| **Topic (source list)** | Linked List |
| **Also uses** | Two Pointers (fast/slow), In-place list reversal, Merging lists |
| **Difficulty** | Medium |
| **LeetCode URL** | <https://leetcode.com/problems/reorder-list/> |
| **Pattern** | Find middle → reverse second half → weave the two halves |

---

## 2. Problem Explanation

### What are we given?

`head` — the first node of a **singly linked list** (each node knows only its value and the node after it).

LeetCode defines the node class like this (it is already provided on LeetCode, so you do **not** write it yourself):

```text
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
```

### What must we do?

Rearrange the nodes so the list alternates between "next one from the front" and "next one from the back".

If we name the nodes by position `L0, L1, L2, …, Ln`, then:

```text
Before:  L0 → L1 → L2 → … → Ln-1 → Ln
After:   L0 → Ln → L1 → Ln-1 → L2 → Ln-2 → …
```

### The rules

1. The work happens **in place**: the function returns **nothing** (`None`). LeetCode checks the list by walking it again from the same `head`.
2. You may **not** solve it by swapping the **values** stored in the nodes. You must change the **links** (`next` pointers) between the existing nodes.
3. The first node stays first, so `head` itself never changes.

### Examples

**Example 1**

```text
Input:  head = [1,2,3,4]
Output: [1,4,2,3]
```

Take from the front (`1`), then the back (`4`), then the front (`2`), then the back (`3`).

**Example 2**

```text
Input:  head = [1,2,3,4,5]
Output: [1,5,2,4,3]
```

Front `1`, back `5`, front `2`, back `4`, and the middle node `3` ends up last.

### Constraints

- The number of nodes in the list is in the range `[1, 5 * 10^4]`.
- `1 <= Node.val <= 1000`

There is no official follow-up, but the classic interview goal is to do it in **`O(n)` time and `O(1)` extra space**.

---

## 3. Everyday Analogy

> **Explain it like I'm five**

Imagine a line of kids holding hands, numbered 1 to 5, and the teacher wants them to stand in the order "first, last, second, second-last, …" — `1, 5, 2, 4, 3`.

The teacher does it in three moves:

1. **Find the middle kid.** Two helpers walk along the line: one takes one step at a time, the other takes two steps. When the fast helper reaches the end, the slow helper is standing in the middle. The line is split there into a front half `1, 2, 3` and a back half `4, 5`.
2. **Turn the back half around.** The back half now faces the other way: `5, 4`.
3. **Zip the two halves together** like a zipper: one kid from the front half, one from the back half, one from the front, one from the back… → `1, 5, 2, 4, 3`.

Nobody swapped name tags — kids only changed **whose hand they hold**.

---

## 4. Step-by-Step Logic

1. **Notice the shape of the answer.** The output alternates between the front half (in normal order) and the back half (in **reverse** order).
   For `[1,2,3,4,5]`: front half `1,2,3`, back half reversed `5,4` → interleave → `1,5,2,4,3`.
2. **The hard part is "from the back".** A singly linked list can only move forward, so we cannot step backwards from `Ln` to `Ln-1`.
3. **Easy fix with extra memory:** copy the nodes into a Python list. A list allows index access, so `nodes[j]` with a shrinking `j` walks from the back. (This is our brute-force method — it costs `O(n)` extra memory.)
4. **Fix without extra memory:** if we **reverse** the back half of the list itself, then "walking from the back" becomes ordinary forward walking.
5. **Find the middle** with slow and fast pointers: `slow` moves 1 step, `fast` moves 2 steps. When `fast` cannot move two more steps, `slow` is at the end of the front half.
6. **Cut** the list after `slow` (`slow.next = None`) so the front half ends cleanly.
7. **Reverse** the back half.
8. **Merge alternately:** take a node from the front half, then a node from the back half, until the back half is used up. The front half is never shorter than the back half, so any leftover node (the middle) is already in the right place at the end.

---

## 5. Brute-Force Solution

### Algorithm

1. Walk the list and store **every node** (not just the values) in a Python list `nodes`.
2. Use two indices: `i` at the front, `j` at the back.
3. While `i < j`: link `nodes[i] → nodes[j]`, move `i` forward, then (if `i < j` still) link `nodes[j] → nodes[i]`, move `j` back.
4. The node where `i` and `j` meet is the last node; set its `next` to `None` so no old link creates a cycle.

### Python code

```python
from typing import Optional


class Solution:
    def reorderList(self, head: Optional[ListNode]) -> None:
        """
        Do not return anything, modify head in-place instead.
        """
        if head is None:
            return

        nodes = []
        node = head
        while node:
            nodes.append(node)
            node = node.next

        i, j = 0, len(nodes) - 1
        while i < j:
            nodes[i].next = nodes[j]    # front -> back
            i += 1
            if i == j:
                break
            nodes[j].next = nodes[i]    # back -> next front
            j -= 1
        nodes[i].next = None            # the meeting node is the new tail
```

### Explanation

- Storing the **nodes** (not values) lets us rewire links while obeying "do not modify the values".
- `i` and `j` close in from both ends, which produces the front/back/front/back order.
- `nodes[i].next = None` is essential: the last node still has its **old** `next` pointer, which would point back into the list and create a cycle.

### Complexity

- **Time:** `O(n)` — one pass to collect the nodes, one pass to relink them.
- **Auxiliary space:** `O(n)` — the `nodes` list holds a reference to every node. That is the trade-off: easy to write, but it uses memory proportional to the list length (up to `5 * 10^4` references).

> An even more naive idea — repeatedly walk to the current tail, unhook it and insert it after the front pointer — uses `O(1)` space but takes `O(n²)` time (about `1.25 × 10^9` steps for `n = 5 * 10^4`). See Practice Question 3.

---

## 6. Optimized Solution

### Idea

Three classic linked-list moves, each `O(n)` time and `O(1)` space:

1. **Middle** — slow/fast pointers.
2. **Reverse** — reverse the second half in place.
3. **Merge** — weave the two halves together.

### Algorithm

1. `slow = fast = head`. While `fast.next` and `fast.next.next` exist: `slow = slow.next`, `fast = fast.next.next`.
2. `second = slow.next`; `slow.next = None` (cut).
3. Reverse `second` with the three-pointer technique (`prev`, `curr`, `nxt`).
4. `first = head`. While `second` is not `None`: save both `next` pointers, link `first → second → old first.next`, advance both.

### Python code (LeetCode-ready)

```python
from typing import Optional


class Solution:
    def reorderList(self, head: Optional[ListNode]) -> None:
        """
        Do not return anything, modify head in-place instead.
        """
        if head is None or head.next is None:
            return

        # 1) Find the end of the first half.
        slow, fast = head, head
        while fast.next and fast.next.next:
            slow = slow.next
            fast = fast.next.next

        # 2) Cut the list into two halves.
        second = slow.next
        slow.next = None

        # 3) Reverse the second half.
        prev = None
        while second:
            nxt = second.next
            second.next = prev
            prev = second
            second = nxt
        second = prev

        # 4) Weave: first, second, first, second, ...
        first = head
        while second:
            first_next = first.next
            second_next = second.next
            first.next = second
            second.next = first_next
            first = first_next
            second = second_next
```

---

## 7. Line-by-Line Explanation

| Line | What it does | Why |
|---|---|---|
| `if head is None or head.next is None: return` | Stops early for 0 or 1 node. | Nothing to reorder. (The constraints guarantee at least 1 node, but the guard is cheap.) |
| `slow, fast = head, head` | Both pointers start at the first node. | Standard start for the middle-finding trick. |
| `while fast.next and fast.next.next:` | Continue only while `fast` can take two full steps. | This stops `slow` at the **end of the first half**; the first half gets the extra node when `n` is odd. |
| `slow = slow.next` | One step. | `slow` covers half the distance of `fast`. |
| `fast = fast.next.next` | Two steps. | When `fast` stops, `slow` is in the middle. |
| `second = slow.next` | Remember where the second half starts. | We are about to cut the link. |
| `slow.next = None` | Cut. | Ends the first half; prevents cycles later. |
| `prev = None` | The reversed part is empty at first. | The old first node of the second half becomes its tail, so it must point to `None`. |
| `nxt = second.next` | Save the rest of the list. | We overwrite `second.next` on the next line. |
| `second.next = prev` | Flip the arrow. | This is the reversal step. |
| `prev = second; second = nxt` | Move both pointers forward. | Continue reversing. |
| `second = prev` | `prev` is the new head of the reversed half. | When the loop ends, `second` is `None`. |
| `first = head` | Start weaving at the front. | |
| `while second:` | Loop until the (shorter or equal) second half is used up. | The first half has the same length or one more node. |
| `first_next = first.next` / `second_next = second.next` | Save the onward links. | Both are about to be overwritten. |
| `first.next = second` | Front node points to the back node. | Produces `L0 → Ln`. |
| `second.next = first_next` | Back node points to the next front node. | Produces `Ln → L1`. |
| `first = first_next; second = second_next` | Advance both halves. | Ready for the next pair. |
| *(no `return`)* | The function returns `None`. | LeetCode reads the reordered list from `head`. |

---

## 8. Dry Run

**Input:** `head = [1,2,3,4,5]` (official Example 2)

### Step 1 — find the middle

| Iteration | `slow` | `fast` | `fast.next` and `fast.next.next` exist? |
|---|---|---|---|
| start | 1 | 1 | 2 and 3 → yes |
| 1 | 2 | 3 | 4 and 5 → yes |
| 2 | 3 | 5 | `fast.next` is `None` → stop |

`slow` is node `3`.

### Step 2 — cut

```text
first half : 1 → 2 → 3 → None
second half: 4 → 5 → None
```

### Step 3 — reverse the second half

| Step | `second` (curr) | `nxt` | Link changed | `prev` after |
|---|---|---|---|---|
| 1 | 4 | 5 | `4.next = None` | 4 |
| 2 | 5 | None | `5.next = 4` | 5 |

Reversed second half: `5 → 4 → None`.

### Step 4 — weave

| Round | `first` | `second` | `first_next` | `second_next` | Links set | List from head so far |
|---|---|---|---|---|---|---|
| 1 | 1 | 5 | 2 | 4 | `1→5`, `5→2` | `1 → 5 → 2 → 3` |
| 2 | 2 | 4 | 3 | None | `2→4`, `4→3` | `1 → 5 → 2 → 4 → 3` |
| — | 3 | None | | | loop ends | |

**Result:** `[1,5,2,4,3]` ✅ (node `3` already ends with `None` because of the cut.)

### Second dry run (even length) — `head = [1,2,3,4]`

- Middle: start `slow=1, fast=1` → `slow=2, fast=3` → `fast.next.next` is `None`, stop. `slow = 2`.
- Cut: `1 → 2` and `3 → 4`. Reverse: `4 → 3`.
- Weave round 1: `1→4`, `4→2` → `1 → 4 → 2`. Round 2: `first=2, second=3`, `first_next = None`: `2→3`, `3→None`.

**Result:** `[1,4,2,3]` ✅

---

## 9. Concepts, Data Structures, and Patterns

- **Singly linked list:** each node has `val` and `next`; you can only move forward, which is why "from the back" needs a trick.
- **Fast and slow pointers:** the same tortoise-and-hare idea used in [Detect Cycle in a Linked List](022_detect_cycle_in_a_linked_list.md) and the gap-pointer idea in [Remove Nth Node From End of List](025_remove_nth_node_from_end_of_list.md).
- **In-place reversal:** the three-pointer loop from [Reverse a Linked List](021_reverse_a_linked_list.md).
- **Merging two lists:** alternating merge is a simpler cousin of [Merge Two Sorted Lists](023_merge_two_sorted_lists.md) — here we alternate instead of comparing values.
- **Pointer rewiring vs value swapping:** the problem forbids changing values, so every operation changes `next` links only.
- **Cutting lists to avoid cycles:** whenever you relink nodes, make sure the final tail points to `None`.

---

## 10. Complexity Analysis

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Repeatedly move the tail (Practice Q3) | `O(n²)` | `O(1)` | Each of about `n/2` moves walks to the end of the list. |
| Brute force (array of nodes) | `O(n)` | `O(n)` | One pass to collect nodes, one pass to relink; the array stores `n` references. |
| Optimized (middle + reverse + merge) | `O(n)` | `O(1)` | Finding the middle is about `n/2` steps, reversing is about `n/2`, merging is about `n/2`; only a handful of pointer variables are used. |

---

## 11. Edge Cases

| Case | Input | Expected result | Why |
|---|---|---|---|
| Single node | `[7]` | `[7]` | Nothing to reorder; early return. |
| Two nodes | `[1,2]` | `[1,2]` | `L0 → L1` is already the required order. |
| Three nodes | `[1,2,3]` | `[1,3,2]` | Front, back, then the middle. |
| Even length | `[1,2,3,4]` | `[1,4,2,3]` | Halves have equal length. |
| Odd length | `[1,2,3,4,5]` | `[1,5,2,4,3]` | Middle node ends last. |
| Equal values | `[5,5,5,5]` | `[5,5,5,5]` | Values look the same, but the **nodes** were rearranged. |
| Maximum length | `5 * 10^4` nodes | Reordered list | Iterative code: no recursion depth problems. |

---

## 12. Common Mistakes and Debugging

1. **Returning a new list or a new head.** The method returns `None`; LeetCode reads from the original `head`.
2. **Swapping values instead of nodes.** It may pass simple tests but breaks the rule "only nodes themselves may be changed".
3. **Forgetting `slow.next = None`.** The first half still points into the second half, so the merged list contains a **cycle** and printing it loops forever.
4. **Wrong middle-loop condition.** `while fast and fast.next` stops `slow` one node later for even lengths (at `3` for `[1,2,3,4]`). That can still work if you cut after `slow`, but mixing the two styles is a common source of off-by-one bugs — pick one and trace it on both an even and an odd list.
5. **Losing the rest of the list during reversal or merging.** Always save `next` pointers (`nxt`, `first_next`, `second_next`) **before** overwriting them.
6. **Looping on `while first` during the merge** and then dereferencing `second.next` when `second` is `None`. Loop on `while second`.

**Debugging tip:** add a helper that prints at most `n + 2` values from a node. If it prints more than `n` values, you have created a cycle.

---

## 13. Practice Questions

**Q1. What is the reordered list for `[1,2,3,4,5,6]`? Which node does `slow` stop on?**

<details><summary>Hint</summary>Run the `fast.next and fast.next.next` loop by hand, then split, reverse and weave.</summary></details>

**Answer:** `slow` stops on `3` (`slow` moves 1 → 2 → 3 while `fast` moves 1 → 3 → 5; then `fast.next.next` is `None`). Halves: `1,2,3` and `4,5,6` → reversed `6,5,4`. Weave → `[1,6,2,5,3,4]`.

**Q2. Write a function that returns the values of the reordered list without changing the input (useful for checking answers).**

<details><summary>Hint</summary>Copy the values into a Python list and take from both ends alternately.</summary></details>

**Answer:**

```python
def reorder_values(values):
    result = []
    i, j = 0, len(values) - 1
    while i <= j:
        result.append(values[i])
        if i != j:
            result.append(values[j])
        i += 1
        j -= 1
    return result


assert reorder_values([1, 2, 3, 4]) == [1, 4, 2, 3]
assert reorder_values([1, 2, 3, 4, 5]) == [1, 5, 2, 4, 3]
assert reorder_values([1, 2, 3, 4, 5, 6]) == [1, 6, 2, 5, 3, 4]
assert reorder_values([9]) == [9]
```

**Q3. Write the `O(1)`-space but `O(n²)`-time version: repeatedly detach the current tail and insert it after the current front node.**

<details><summary>Hint</summary>Walk to the second-last node to unhook the tail. Stop when the front node or the node after it is the tail.</summary></details>

**Answer:**

```python
def reorder_quadratic(head):
    front = head
    while front and front.next and front.next.next:
        before_tail = front
        while before_tail.next.next:          # walk to the node before the tail
            before_tail = before_tail.next
        tail = before_tail.next
        before_tail.next = None               # unhook the tail
        tail.next = front.next                # insert it after front
        front.next = tail
        front = tail.next                     # next front node


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


for vals, expected in [([1, 2, 3, 4], [1, 4, 2, 3]),
                       ([1, 2, 3, 4, 5], [1, 5, 2, 4, 3]),
                       ([1], [1]), ([1, 2], [1, 2])]:
    h = build(vals)
    reorder_quadratic(h)
    assert to_list(h) == expected
```

Each step walks to the tail (`O(n)`), and there are about `n/2` steps, so the total is `O(n²)`.

**Q4. Write a helper that returns the end of the first half (the node `slow` stops on) and check it.**

<details><summary>Hint</summary>Reuse the loop condition `fast.next and fast.next.next`.</summary></details>

**Answer:**

```python
def end_of_first_half(head):
    slow = fast = head
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next
    return slow


def make(values):
    head = None
    for v in reversed(values):
        head = ListNode(v, head)
    return head


assert end_of_first_half(make([1, 2, 3, 4])).val == 2
assert end_of_first_half(make([1, 2, 3, 4, 5])).val == 3
assert end_of_first_half(make([1])).val == 1
assert end_of_first_half(make([1, 2])).val == 1
```

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** Find middle (slow/fast) → reverse second half → alternate merge.
- **Key idea:** "Take from the back" is impossible in a singly linked list, so reverse the back half and walk it forward.
- **Time:** `O(n)`.
- **Auxiliary space:** `O(1)` (brute force with a node array: `O(n)`).
- **Gotchas:** cut with `slow.next = None`; save `next` pointers before overwriting; return nothing.
- **One-line memory hook:** *"Split, flip, zip."*

### Completion checklist

- [x] Problem requirements verified
- [x] Examples and constraints verified
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force solution written and tested
- [x] Optimized Python solution written and tested (`tools/tests/p026.py`)
- [x] Line-by-line explanation written
- [x] Dry run completed with a real example
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
