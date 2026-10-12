# 023. Merge Two Sorted Lists

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Merge Two Sorted Lists |
| **LeetCode number** | 21 |
| **Topic (source list)** | Linked List |
| **Also uses** | Two Pointers, Recursion |
| **Difficulty** | Easy |
| **LeetCode URL** | <https://leetcode.com/problems/merge-two-sorted-lists/> |
| **Pattern** | Two-pointer merge with a dummy (sentinel) head |

---

## 2. Problem Explanation

### Linked list primer

A **singly linked list** is a chain of **nodes**. Each node stores a value `val` and a reference `next` to the following node (`None` after the last node). LeetCode provides this class — it appears as a comment in the editor, and you never define it yourself:

```text
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
```

We draw lists with arrows, e.g. `1 -> 2 -> 4 -> None`. A variable such as `list1` refers to the **first** node; an empty list is `None`.

### What are we given?

- `list1` — the head of a linked list whose values are in non-decreasing order (each value is `>=` the one before it).
- `list2` — the head of a second list, also in non-decreasing order.

Either one (or both) may be empty (`None`).

### What must we return?

The head of **one** list containing all the nodes of both inputs, still in non-decreasing order.

### The rules

1. The result must be sorted in non-decreasing order.
2. Build the result by **splicing** — reconnecting the `next` arrows of the nodes you were given — rather than creating new nodes.
3. If both inputs are empty, return `None` (an empty list).

### Examples

**Example 1**

```text
Input:  list1 = [1, 2, 4], list2 = [1, 3, 4]
Output: [1, 1, 2, 3, 4, 4]
```

`1 -> 2 -> 4` and `1 -> 3 -> 4` interleave into `1 -> 1 -> 2 -> 3 -> 4 -> 4`.

**Example 2**

```text
Input:  list1 = [], list2 = []
Output: []
```

**Example 3**

```text
Input:  list1 = [], list2 = [0]
Output: [0]
```

When one list is empty, the answer is simply the other list.

### Constraints

- The number of nodes in both lists is in the range `[0, 50]`.
- `-100 <= Node.val <= 100`
- Both `list1` and `list2` are sorted in non-decreasing order.

(No follow-up is given for this problem.)

---

## 3. Everyday Analogy

> **Explain it like I'm five**

Two lines of kids are waiting for ice cream, and in each line the kids already stand from shortest to tallest. The teacher wants **one** line, still shortest to tallest.

The teacher looks only at the **front kid of each line** and asks: "Which of you two is shorter?" That kid steps into the new line. Then the teacher looks at the two front kids again, and again, and again.

When one line runs out of kids, the rest of the other line is already in order, so they all just walk to the end of the new line together.

To get started, the teacher puts a little **flag** on the floor where the new line will begin. The flag isn't a kid — it just marks the spot, so the teacher doesn't need a special rule for "who goes first".

---

## 4. Step-by-Step Logic

1. **The smallest remaining value is always at one of the two fronts.** Both lists are sorted, so nothing deeper in a list can be smaller than its own front.
2. **Repeatedly take the smaller front** and attach it to the end of the result. Move that list's pointer one node forward.
3. **Ties:** if the fronts are equal, either choice is correct. Taking from `list1` first (`<=`) keeps equal values in a stable order.
4. **Keep a `tail` pointer** to the last node of the result so we can attach in `O(1)` time instead of walking the result every time.
5. **The empty-start problem:** the result has no first node yet, so "attach to the end" has nowhere to attach. Solution: create a **dummy** node before the real result. Attach everything after it, and return `dummy.next` at the end.
6. **When one list runs out,** attach the remainder of the other list in one step (`tail.next = list1 or list2`). Its nodes are already sorted and already linked together.

---

## 5. Brute-Force Solution

### Algorithm

1. Walk both lists and collect every **node** into one Python list.
2. Sort the nodes by their values.
3. Relink them in sorted order: each node's `next` becomes the following node in the sorted Python list; the last node's `next` becomes `None`.
4. Return the first node (or `None` if there are no nodes).

This ignores the fact that the inputs are already sorted, but it is correct and it still splices the original nodes.

### Python code

```python
from typing import Optional


class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        nodes = []
        for head in (list1, list2):
            node = head
            while node:
                nodes.append(node)
                node = node.next

        if not nodes:
            return None

        nodes.sort(key=lambda node: node.val)  # sort node objects by value

        for i in range(len(nodes) - 1):        # relink in sorted order
            nodes[i].next = nodes[i + 1]
        nodes[-1].next = None                  # the last node ends the list

        return nodes[0]
```

### Explanation

- We sort **node objects** using `key=lambda node: node.val`. `ListNode` has no `<` operator, so `nodes.sort()` without a key would raise `TypeError`.
- Relinking reuses the original nodes, which satisfies the "splice" rule.
- `nodes[-1].next = None` is essential: the last node may have pointed somewhere else before, which could leave a loop.

### Complexity

- **Time:** `O((n + m) log(n + m))` — dominated by the sort, where `n` and `m` are the lengths of the two lists.
- **Auxiliary space:** `O(n + m)` — the Python list of node references.
- **Trade-off:** simple, but it wastes the "already sorted" information. The optimized merge is linear and uses `O(1)` extra space. (With at most 100 nodes in total this brute force is still fast, but the merge technique is what interviews — and Merge K Sorted Lists — build on.)

---

## 6. Optimized Solution

### Idea — two-pointer merge with a dummy head

Compare the two fronts, attach the smaller one to `tail`, advance. When one list is empty, attach the other.

### Algorithm

1. `dummy = ListNode()`, `tail = dummy`.
2. While both `list1` and `list2` are non-empty:
   - If `list1.val <= list2.val`: `tail.next = list1`, `list1 = list1.next`.
   - Else: `tail.next = list2`, `list2 = list2.next`.
   - `tail = tail.next`.
3. `tail.next = list1 if list1 else list2`.
4. Return `dummy.next`.

### Python code (LeetCode-ready)

```python
from typing import Optional


class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode()   # placeholder before the real head
        tail = dummy         # last node of the merged list so far

        while list1 and list2:
            if list1.val <= list2.val:
                tail.next = list1
                list1 = list1.next
            else:
                tail.next = list2
                list2 = list2.next
            tail = tail.next

        # At most one list still has nodes; they are already sorted.
        tail.next = list1 if list1 else list2

        return dummy.next
```

### Alternative: recursive merge

```python
from typing import Optional


class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        if list1 is None:
            return list2
        if list2 is None:
            return list1
        if list1.val <= list2.val:
            # list1's head is the smallest; merge the rest behind it.
            list1.next = self.mergeTwoLists(list1.next, list2)
            return list1
        list2.next = self.mergeTwoLists(list1, list2.next)
        return list2
```

The recursive version is short and elegant: "the smaller head goes first, followed by the merge of everything else". It uses one stack frame per node (`O(n + m)` stack space). With at most 100 nodes here that's fine, but for long lists the iterative version is safer in Python (default recursion limit ≈ 1000).

---

## 7. Line-by-Line Explanation

(Iterative version)

| Line | What it does | Why |
|---|---|---|
| `dummy = ListNode()` | Creates a throwaway node with value 0. | Gives `tail` a starting node, so attaching the very first real node needs no special case. |
| `tail = dummy` | `tail` points to the end of the merged list. | We always attach new nodes at `tail.next`. |
| `while list1 and list2:` | Runs while both lists have nodes. | We can only compare when both fronts exist. |
| `if list1.val <= list2.val:` | Compares the two front values. | The smaller front is the smallest remaining value overall. `<=` takes `list1` on ties (stable). |
| `tail.next = list1` | Attaches `list1`'s front node to the result. | Splices the existing node — no new node is created. |
| `list1 = list1.next` | Advances `list1` to its next node. | That front node is now used. |
| `else: tail.next = list2; list2 = list2.next` | Same for `list2`. | `list2`'s front was strictly smaller. |
| `tail = tail.next` | Moves `tail` onto the node just attached. | Keeps `tail` at the end of the merged list. |
| `tail.next = list1 if list1 else list2` | Attaches whatever is left (possibly `None`). | The leftover part is already sorted and linked, so one assignment attaches all of it. If both are empty this sets `tail.next = None`, correctly ending the list. |
| `return dummy.next` | Returns the first real node. | `dummy` itself is not part of the answer. If both inputs were empty, `dummy.next` is `None`. |

**Why don't we need to set the last node's `next` to `None`?** The leftover list ends in `None` already, and every node we attached earlier gets its `next` overwritten when the following node is attached.

---

## 8. Dry Run

**Input:** `list1 = [1, 2, 4]`, `list2 = [1, 3, 4]`

To tell equal values apart, call the nodes `a1 -> a2 -> a4` (from `list1`) and `b1 -> b3 -> b4` (from `list2`).

| Step | `list1` front | `list2` front | Compare | Attach | Merged list so far (after `dummy`) | `list1` now | `list2` now |
|---|---|---|---|---|---|---|---|
| 1 | a1 (1) | b1 (1) | 1 <= 1 ✓ | a1 | `1 ->` | a2 (2) | b1 (1) |
| 2 | a2 (2) | b1 (1) | 2 <= 1 ✗ | b1 | `1 -> 1 ->` | a2 (2) | b3 (3) |
| 3 | a2 (2) | b3 (3) | 2 <= 3 ✓ | a2 | `1 -> 1 -> 2 ->` | a4 (4) | b3 (3) |
| 4 | a4 (4) | b3 (3) | 4 <= 3 ✗ | b3 | `1 -> 1 -> 2 -> 3 ->` | a4 (4) | b4 (4) |
| 5 | a4 (4) | b4 (4) | 4 <= 4 ✓ | a4 | `1 -> 1 -> 2 -> 3 -> 4 ->` | None | b4 (4) |
| end | None | b4 (4) | loop stops | leftover `b4` | `1 -> 1 -> 2 -> 3 -> 4 -> 4 -> None` | — | — |

Return `dummy.next` = `a1`.

**Result:** `[1, 1, 2, 3, 4, 4]` ✅

**Second dry run:** `list1 = []`, `list2 = [0]`. The `while` loop doesn't run because `list1` is `None`. Then `tail.next = list2`, so `dummy -> 0 -> None`, and we return the node `0`. **Result:** `[0]` ✅

**Example 2:** both empty → loop skipped, `tail.next = None`, return `dummy.next = None` → `[]` ✅

---

## 9. Concepts, Data Structures, and Patterns

- **Merge step of merge sort:** combining two sorted sequences in linear time by repeatedly taking the smaller front. This exact routine is the "conquer" half of merge sort.
- **Dummy (sentinel) node:** a fake node placed before the real head so that inserting the first node works the same way as inserting any other. It's one of the most useful linked-list tricks; you'll see it again in [025_remove_nth_node_from_end_of_list.md](025_remove_nth_node_from_end_of_list.md).
- **Tail pointer:** keeping a reference to the last node makes appending `O(1)`.
- **Splicing:** relinking existing nodes instead of copying values — uses no extra memory for nodes.
- **Recursion:** the alternative solution defines the merge in terms of a smaller merge.
- **Related notes in this project:**
  - [024_merge_k_sorted_lists.md](024_merge_k_sorted_lists.md) generalizes this to `k` lists (and reuses this function in its divide-and-conquer approach).
  - [021_reverse_a_linked_list.md](021_reverse_a_linked_list.md) for the basics of re-pointing `next`.
  - [017_merge_intervals.md](../03_interval/017_merge_intervals.md) — a different kind of "merge", on sorted intervals.

---

## 10. Complexity Analysis

Let `n` = length of `list1`, `m` = length of `list2`.

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Brute force (collect, sort, relink) | `O((n + m) log(n + m))` | `O(n + m)` | Sorting dominates; the Python list stores every node reference. |
| Iterative merge (optimized) | `O(n + m)` | `O(1)` | Each loop iteration attaches one node, so at most `n + m` iterations. Only `dummy`, `tail` and the two pointers are extra. |
| Recursive merge | `O(n + m)` | `O(n + m)` | One call per attached node; all calls stay on the stack until the base case. |

The output list itself isn't extra space — it's made of the input nodes.

---

## 11. Edge Cases

| Case | Input | Expected result | Why it works |
|---|---|---|---|
| Both empty | `[]`, `[]` | `[]` | Loop skipped; `dummy.next` stays `None`. |
| One empty | `[]`, `[0]` | `[0]` | Leftover assignment attaches the non-empty list. |
| Other one empty | `[0]`, `[]` | `[0]` | Same, symmetric. |
| All of `list1` smaller | `[1, 2, 3]`, `[4, 5, 6]` | `[1, 2, 3, 4, 5, 6]` | `list1` runs out first; `list2` is attached whole. |
| All of `list2` smaller | `[4, 5, 6]`, `[1, 2, 3]` | `[1, 2, 3, 4, 5, 6]` | Symmetric. |
| Equal values everywhere | `[2, 2, 2]`, `[2]` | `[2, 2, 2, 2]` | `<=` keeps taking from `list1` on ties; nothing is lost. |
| Extreme values | `[-100, 100]`, `[-100, 100]` | `[-100, -100, 100, 100]` | Plain comparisons. |

---

## 12. Common Mistakes and Debugging

1. **Returning `dummy` instead of `dummy.next`.** The answer would start with a fake `0`.
2. **Forgetting `tail = tail.next`.** Every new node overwrites `dummy.next`, so the result only ever has one node.
3. **Forgetting the leftover attachment.** Without `tail.next = list1 or list2`, the result is cut off as soon as one list is exhausted (e.g. Example 1 would lose the final `4`).
4. **Using `while list1 or list2:`** and then reading `list1.val` crashes with `AttributeError` when `list1` is `None`. Use `and`, then attach the leftover.
5. **Creating new nodes (`ListNode(list1.val)`)** works for the judge but ignores the "splice" requirement and uses `O(n + m)` extra memory.
6. **Sorting nodes without a key** (`nodes.sort()`) raises `TypeError: '<' not supported between instances of 'ListNode' and 'ListNode'`.

**Debugging tip:** after each loop iteration, print the merged list from `dummy.next` along with `list1.val` and `list2.val`. Compare to the dry-run table.

---

## 13. Practice Questions

**Q1. Merge `list1 = [5]` and `list2 = [1, 2, 3]`. How many loop iterations run, and what does the leftover assignment attach?**

<details><summary>Hint</summary>Count how many times `list2`'s front is smaller than 5.</summary></details>

**Answer:** Three iterations, each attaching a node from `list2` (1, then 2, then 3), because each is smaller than 5. After the third, `list2` is `None`, so the loop stops and `tail.next = list1` attaches `5`. Result: `[1, 2, 3, 5]`.

**Q2. Merge two sorted Python lists (arrays) into one sorted list without calling `sorted`.**

<details><summary>Hint</summary>Same two-pointer idea, using indices `i` and `j` instead of node pointers.</summary></details>

**Answer:**

```python
def merge_arrays(a, b):
    i = j = 0
    out = []
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            out.append(a[i])
            i += 1
        else:
            out.append(b[j])
            j += 1
    out.extend(a[i:])   # at most one of these two is non-empty
    out.extend(b[j:])
    return out


assert merge_arrays([1, 2, 4], [1, 3, 4]) == [1, 1, 2, 3, 4, 4]
assert merge_arrays([], [0]) == [0]
assert merge_arrays([], []) == []
```

**Q3. Sort an unsorted linked list in `O(n log n)` time using the merge routine (LeetCode 148).**

<details><summary>Hint</summary>Split the list in half with slow/fast pointers, sort each half recursively, then merge the two sorted halves.</summary></details>

**Answer:** This is merge sort on a linked list. Find the node before the middle, cut the list there, recurse, and merge.

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


def merge(a, b):
    dummy = tail = ListNode()
    while a and b:
        if a.val <= b.val:
            tail.next, a = a, a.next
        else:
            tail.next, b = b, b.next
        tail = tail.next
    tail.next = a if a else b
    return dummy.next


def sort_list(head):
    if head is None or head.next is None:
        return head
    slow, fast = head, head.next          # slow stops at the end of the first half
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
    second = slow.next
    slow.next = None                      # cut the list in two
    return merge(sort_list(head), sort_list(second))


assert to_list(sort_list(build([4, 2, 1, 3]))) == [1, 2, 3, 4]
assert to_list(sort_list(build([-1, 5, 3, 4, 0]))) == [-1, 0, 3, 4, 5]
assert to_list(sort_list(build([]))) == []
```

**Q4. Merge two sorted linked lists but keep only one copy of each value (the result has no duplicates).**

<details><summary>Hint</summary>Merge as usual, but before attaching a node, skip it if its value equals `tail.val` (and `tail` isn't the dummy).</summary></details>

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


def merge_unique(a, b):
    dummy = tail = ListNode()
    while a or b:
        if b is None or (a is not None and a.val <= b.val):
            node, a = a, a.next
        else:
            node, b = b, b.next
        if tail is dummy or node.val != tail.val:
            tail.next = node
            tail = node
    tail.next = None   # the last attached node may still point at a skipped duplicate
    return dummy.next


assert to_list(merge_unique(build([1, 2, 4]), build([1, 3, 4]))) == [1, 2, 3, 4]
assert to_list(merge_unique(build([1, 1]), build([1]))) == [1]
assert to_list(merge_unique(build([]), build([]))) == []
```

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** Two-pointer merge with a dummy head and a tail pointer.
- **Key idea:** Attach the smaller front, advance that list, move `tail`; finally attach the leftover list; return `dummy.next`.
- **Time:** `O(n + m)`.
- **Auxiliary space:** `O(1)` iterative (`O(n + m)` stack if recursive).
- **One-line memory hook:** *"Smaller front steps forward; whoever's left walks in together."*

### Completion checklist

- [x] Problem requirements verified
- [x] Examples and constraints verified
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force solution written and tested
- [x] Optimized Python solution written and tested (`tools/tests/p023.py`)
- [x] Recursive alternative written and tested
- [x] Line-by-line explanation written
- [x] Dry run completed with a real example
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
