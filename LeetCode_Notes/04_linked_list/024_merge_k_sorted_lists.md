# 024. Merge K Sorted Lists

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Merge k Sorted Lists |
| **LeetCode number** | 23 |
| **Topics (source list)** | Linked List, Heap |
| **Also uses** | Divide and Conquer, Merge Sort |
| **Difficulty** | Hard |
| **LeetCode URL** | <https://leetcode.com/problems/merge-k-sorted-lists/> |
| **Pattern** | K-way merge with a min-heap (alternative: divide-and-conquer pairwise merging) |

> **Note:** The source collection lists this problem under **both** "Linked List" and "Heap". This file is the single canonical note for both sections.

---

## 2. Problem Explanation

### Linked list primer

A **singly linked list** is a chain of **nodes**; each node has a value `val` and a reference `next` to the following node (or `None` after the last node). LeetCode provides the class as a comment in the editor — you never define it yourself:

```text
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
```

We draw lists like `1 -> 4 -> 5 -> None`. A list is passed around as its first node; `None` means an empty list.

### What are we given?

`lists` — a Python list of `k` linked-list heads. Each linked list is sorted in ascending order. Some entries can be `None` (empty lists), and `lists` itself can be empty (`k = 0`).

### What must we return?

The head of a **single** sorted linked list that contains every node from all `k` lists (or `None` if there are no nodes at all).

### The rules

1. The output must be sorted in ascending order (equal values may appear next to each other).
2. Every value from every input list must appear exactly once in the output.
3. Reusing (relinking) the existing nodes is allowed and is the memory-friendly way to do it.

### Examples

**Example 1**

```text
Input:  lists = [[1, 4, 5], [1, 3, 4], [2, 6]]
Output: [1, 1, 2, 3, 4, 4, 5, 6]
```

The three lists are:

```text
1 -> 4 -> 5
1 -> 3 -> 4
2 -> 6
```

Merged together: `1 -> 1 -> 2 -> 3 -> 4 -> 4 -> 5 -> 6`.

**Example 2**

```text
Input:  lists = []
Output: []
```

No lists at all (`k = 0`) → empty result.

**Example 3**

```text
Input:  lists = [[]]
Output: []
```

One list, but it's empty (`lists = [None]` in code) → empty result.

### Constraints

- `k == lists.length`
- `0 <= k <= 10^4`
- `0 <= lists[i].length <= 500`
- `-10^4 <= lists[i][j] <= 10^4`
- `lists[i]` is sorted in ascending order.
- The sum of `lists[i].length` will not exceed `10^4`.

(No follow-up is given for this problem.)

Throughout this note, **`N`** = total number of nodes across all lists (at most `10^4`) and **`k`** = number of lists.

---

## 3. Everyday Analogy

> **Explain it like I'm five**

Imagine `k` friends, each holding a stack of numbered cards sorted smallest-on-top. You want to make one big sorted pile.

The only cards that could possibly be the smallest are the **top cards** — one per friend. So each friend shows you their top card, and you put all those cards on a little **"smallest-first" tray** that always shows you the smallest card instantly.

You take the smallest card off the tray and put it on your pile. Then the friend who gave you that card shows their **next** card, and it goes on the tray. Repeat until every friend runs out.

The tray never holds more than one card per friend, so it stays small even if there are thousands of cards. That tray is a **min-heap**.

A second way: pair the friends up. Each pair merges their two stacks into one sorted stack (like [023_merge_two_sorted_lists.md](023_merge_two_sorted_lists.md)). Now there are half as many stacks. Pair them up again… until only one stack is left — just like a sports tournament bracket.

---

## 4. Step-by-Step Logic

1. **Where is the smallest remaining value?** Every list is sorted, so the smallest remaining value is at the **front** of one of the `k` lists.
2. **Finding the minimum of `k` fronts** by scanning them all costs `O(k)` per node → `O(N·k)` total. Too slow when `k` is large.
3. **Use a min-heap** (Python's `heapq`) holding one entry per non-empty list: the front value and its node. Popping the smallest costs `O(log k)`; pushing that list's next node also costs `O(log k)`.
4. **The comparison problem:** `heapq` compares entries as tuples. If two entries have the same value, Python compares the **next** tuple element. If that element is a `ListNode`, Python raises `TypeError` because nodes have no `<` operator. Fix: put a **tie-breaker** between the value and the node — the list's index `i`. Entries become `(val, i, node)`. Since each list has at most one node in the heap at a time, `(val, i)` is always unique, so Python never needs to compare nodes.
5. **Build the output** with a dummy head and a `tail` pointer (the same trick as merging two lists).
6. **Alternative — divide and conquer:** merging two lists is easy and linear. Merge lists in pairs: `k` lists → `k/2` → `k/4` → … → 1. There are about `log k` rounds, and each round touches every node once, giving `O(N log k)` too.

---

## 5. Brute-Force Solution

### Algorithm

1. Walk every list and collect every **node** into one Python list.
2. Sort the nodes by value.
3. Relink them in sorted order and end the last node with `None`.
4. Return the first node, or `None` if there were no nodes.

### Python code

```python
from typing import List, Optional


class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        nodes = []
        for head in lists:
            while head:
                nodes.append(head)
                head = head.next

        if not nodes:
            return None

        nodes.sort(key=lambda node: node.val)  # ListNode can't be compared directly

        for i in range(len(nodes) - 1):
            nodes[i].next = nodes[i + 1]
        nodes[-1].next = None

        return nodes[0]
```

### Explanation

- Collecting nodes ignores the fact that each list is already sorted — we simply sort everything again.
- `key=lambda node: node.val` sorts by value; without it, Python would try `node_a < node_b` and fail.
- Relinking reuses the original nodes, and `nodes[-1].next = None` makes sure the result ends properly.

### Complexity

- **Time:** `O(N log N)` — the sort dominates.
- **Auxiliary space:** `O(N)` — the Python list of node references.
- **Trade-off:** correct and short, but it doesn't use the sortedness of the inputs and needs memory for all `N` nodes. The heap approach needs only `O(k)` extra memory and runs in `O(N log k)`, which is better when `k` is much smaller than `N`.

---

## 6. Optimized Solution

### Idea — min-heap of list fronts

Keep a min-heap containing the current front node of each non-empty list, keyed by value. Repeatedly pop the smallest node, attach it to the result, and push that node's successor.

### Algorithm

1. `heap = []`. For each index `i` and head `node` in `lists`: if `node` is not `None`, push `(node.val, i, node)`.
2. `dummy = ListNode()`, `tail = dummy`.
3. While the heap is not empty:
   - Pop `(val, i, node)` — the smallest front.
   - `tail.next = node`, `tail = node`.
   - If `node.next` exists, push `(node.next.val, i, node.next)`.
4. Return `dummy.next`.

### Python code (LeetCode-ready)

```python
import heapq
from typing import List, Optional


class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        heap = []
        for i, node in enumerate(lists):
            if node:
                # i breaks ties so Python never has to compare two ListNodes
                heap.append((node.val, i, node))
        heapq.heapify(heap)                  # O(k)

        dummy = ListNode()
        tail = dummy

        while heap:
            val, i, node = heapq.heappop(heap)   # smallest front overall
            tail.next = node
            tail = node
            if node.next:
                heapq.heappush(heap, (node.next.val, i, node.next))

        return dummy.next
```

### Alternative: divide and conquer (pairwise merging)

```python
from typing import List, Optional


class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        def merge_two(a, b):
            dummy = tail = ListNode()
            while a and b:
                if a.val <= b.val:
                    tail.next, a = a, a.next
                else:
                    tail.next, b = b, b.next
                tail = tail.next
            tail.next = a if a else b
            return dummy.next

        k = len(lists)
        if k == 0:
            return None

        interval = 1
        while interval < k:
            # Merge lists[i] with lists[i + interval]; store the result in lists[i].
            for i in range(0, k - interval, interval * 2):
                lists[i] = merge_two(lists[i], lists[i + interval])
            interval *= 2

        return lists[0]
```

Round 1 merges pairs `(0,1), (2,3), …`; round 2 merges `(0,2), (4,6), …`; round 3 merges `(0,4), …`; and so on, like a tournament bracket. After about `log₂ k` rounds, `lists[0]` holds everything. Each round touches every node at most once, so the total is `O(N log k)` time, and because it merges in place with a few pointers it uses `O(1)` auxiliary space. (It does overwrite entries of the input `lists` array; copy it first if the caller needs it unchanged.)

---

## 7. Line-by-Line Explanation

(Min-heap version)

| Line | What it does | Why |
|---|---|---|
| `import heapq` | Python's binary min-heap functions. | They work on a plain list and always keep the smallest item at `heap[0]`. |
| `heap = []` | The heap starts empty. | It will hold at most one entry per list. |
| `for i, node in enumerate(lists):` | Visits each list head with its index. | The index becomes the tie-breaker. |
| `if node:` | Skips empty lists (`None`). | `None` has no `.val`, and empty lists contribute nothing. |
| `heap.append((node.val, i, node))` | Adds a tuple entry. | Tuples compare element by element: by `val` first, then by `i`. Because `(val, i)` is unique, the third element (the node) is never compared. |
| `heapq.heapify(heap)` | Rearranges the list into a valid heap in `O(k)`. | Faster than `k` separate pushes (`O(k log k)`), though both are fine. |
| `dummy = ListNode()`; `tail = dummy` | Placeholder head and pointer to the end of the result. | Attaching the first real node needs no special case. |
| `while heap:` | Runs until every node has been attached. | An empty heap means all lists are exhausted. |
| `val, i, node = heapq.heappop(heap)` | Removes and returns the entry with the smallest value. | That node is the smallest remaining value overall. `O(log k)`. |
| `tail.next = node`; `tail = node` | Appends the node and moves `tail`. | Builds the answer by splicing existing nodes. |
| `if node.next:` | Checks whether that list has more nodes. | Only the list we just took from has a new front. |
| `heapq.heappush(heap, (node.next.val, i, node.next))` | Pushes the new front with the **same** index `i`. | Keeps exactly one entry per non-empty list. `O(log k)`. |
| `return dummy.next` | Returns the first real node. | `None` if there were no nodes (Examples 2 and 3). |

**Why not `heapq.heappush(heap, (node.val, node))`?** When two values tie — e.g. both lists start with `1` in Example 1 — Python moves on to compare the nodes and fails with `TypeError: '<' not supported between instances of 'ListNode' and 'ListNode'`. The index `i` in the middle prevents that.

**Note on the final node:** the last node popped is the last node of some input list, so its `next` is already `None`. Every other node's `next` is overwritten when the following node is attached — the result is always properly terminated.

---

## 8. Dry Run

**Input:** `lists = [[1, 4, 5], [1, 3, 4], [2, 6]]` (min-heap version)

Name the nodes by list: list 0 = `a1 -> a4 -> a5`, list 1 = `b1 -> b3 -> b4`, list 2 = `c2 -> c6`. Heap entries are written as `(val, i)`; they are shown **sorted** for readability (Python's internal heap array order can differ, but `heappop` always returns the smallest).

Initial heap: `(1,0) (1,1) (2,2)`

| Step | Pop | Attach | Push (successor) | Heap after | Result so far |
|---|---|---|---|---|---|
| 1 | `(1,0)` a1 | 1 | `(4,0)` a4 | `(1,1) (2,2) (4,0)` | `1` |
| 2 | `(1,1)` b1 | 1 | `(3,1)` b3 | `(2,2) (3,1) (4,0)` | `1 -> 1` |
| 3 | `(2,2)` c2 | 2 | `(6,2)` c6 | `(3,1) (4,0) (6,2)` | `1 -> 1 -> 2` |
| 4 | `(3,1)` b3 | 3 | `(4,1)` b4 | `(4,0) (4,1) (6,2)` | `1 -> 1 -> 2 -> 3` |
| 5 | `(4,0)` a4 | 4 | `(5,0)` a5 | `(4,1) (5,0) (6,2)` | `… -> 3 -> 4` |
| 6 | `(4,1)` b4 | 4 | — (b4 is last) | `(5,0) (6,2)` | `… -> 4 -> 4` |
| 7 | `(5,0)` a5 | 5 | — (a5 is last) | `(6,2)` | `… -> 4 -> 4 -> 5` |
| 8 | `(6,2)` c6 | 6 | — (c6 is last) | empty | `… -> 5 -> 6` |

Step 1 and step 5 both involve tied values (`1` vs `1`, `4` vs `4`). The tie is broken by the list index, so the nodes are never compared.

**Result:** `1 -> 1 -> 2 -> 3 -> 4 -> 4 -> 5 -> 6 -> None` = `[1, 1, 2, 3, 4, 4, 5, 6]` ✅

**Second dry run (divide and conquer), same input, `k = 3`:**

| `interval` | Pairs merged (`i`, `i + interval`) | `lists` afterwards |
|---|---|---|
| 1 | `range(0, 2, 2)` → `(0, 1)` | `[1->1->3->4->4->5, (old list 1), 2->6]` |
| 2 | `range(0, 1, 4)` → `(0, 2)` | `[1->1->2->3->4->4->5->6, …]` |
| 4 | loop stops (`4 >= 3`) | return `lists[0]` |

**Result:** `[1, 1, 2, 3, 4, 4, 5, 6]` ✅ (Entry 1 still references node `b1`, which is now inside the merged list — that's why the code only returns `lists[0]`.)

**Examples 2 and 3:** `lists = []` → the heap stays empty, return `dummy.next = None`. `lists = [None]` → `if node:` skips it, heap empty, return `None`. Both give `[]` ✅.

---

## 9. Concepts, Data Structures, and Patterns

- **Min-heap / priority queue:** a structure that returns the smallest item in `O(log size)` and accepts new items in `O(log size)`. Python's `heapq` module implements a binary min-heap on a regular list (`heappush`, `heappop`, `heapify`).
- **Tuple comparison and tie-breakers:** tuples compare element by element. When storing objects that can't be compared, insert a unique tie-breaker (an index or an `itertools.count()` counter) before the object.
- **K-way merge pattern:** "keep one candidate per source in a heap; pop the best; refill from the same source". It also solves: Kth Smallest Element in a Sorted Matrix (LeetCode 378), Find K Pairs with Smallest Sums (LeetCode 373), Smallest Range Covering Elements from K Lists (LeetCode 632), and external sorting of huge files.
- **Divide and conquer:** split the problem into halves (pairs of lists), solve each with the two-list merge, and combine. It's merge sort's structure applied to whole lists.
- **Dummy head + tail pointer:** the standard way to build an output linked list.
- **Related notes in this project:**
  - [023_merge_two_sorted_lists.md](023_merge_two_sorted_lists.md) — the building block for the divide-and-conquer approach.
  - [074_top_k_frequent_elements.md](../10_heap/074_top_k_frequent_elements.md) and [075_find_median_from_data_stream.md](../10_heap/075_find_median_from_data_stream.md) — other heap problems from the Heap section.
  - [021_reverse_a_linked_list.md](021_reverse_a_linked_list.md) — linked-list basics.

---

## 10. Complexity Analysis

`N` = total nodes, `k` = number of lists.

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Brute force (collect, sort, relink) | `O(N log N)` | `O(N)` | Sorting all nodes; the Python list holds all `N` references. |
| Scan all `k` fronts each step | `O(N·k)` | `O(1)` | Each of `N` steps looks at up to `k` fronts. |
| Merge lists one after another | `O(N·k)` worst case | `O(1)` | The growing result is re-walked on every merge; e.g. `k` lists of equal length `N/k` cost `N/k·(2 + 3 + … + k)` ≈ `N·k/2`. |
| **Min-heap (optimized)** | **`O(N log k)`** | **`O(k)`** | `heapify` is `O(k)`. Each of the `N` nodes is popped once and pushed at most once, each `O(log k)`. The heap holds at most `k` entries. |
| Divide and conquer (pairwise) | `O(N log k)` | `O(1)` | About `⌈log₂ k⌉` rounds; in each round every node takes part in at most one two-list merge, so each round is `O(N)`. Merging in place needs only a few pointers. |

Since `log k <= log N`, the heap and divide-and-conquer approaches are never worse than sorting, and they're much better when `k` is small compared to `N`. (With `k` up to `10^4` and `N <= 10^4`, many lists may be empty — the heap simply skips them.)

---

## 11. Edge Cases

| Case | Input | Expected result | Why it works |
|---|---|---|---|
| No lists | `[]` | `[]` | Heap empty → `None`; divide and conquer returns `None` when `k == 0`. |
| One empty list | `[[]]` | `[]` | `None` entries are skipped. |
| All lists empty | `[[], [], []]` | `[]` | Same. |
| Single list | `[[1]]` | `[1]` | One push, one pop. |
| Only one non-empty list | `[[], [1], []]` | `[1]` | Empty entries skipped. |
| Many equal values | `[[5, 5], [5], [5, 5, 5]]` | `[5, 5, 5, 5, 5, 5]` | Tie-breaker index prevents node comparison. |
| Lists that don't overlap | `[[1, 2, 3], [4, 5, 6], [7, 8, 9]]` | `[1, 2, …, 9]` | Heap simply drains one list after another. |
| Extreme values | `[[-10000], [10000], [0]]` | `[-10000, 0, 10000]` | Plain integer comparisons. |
| Very many lists | `k = 10^4`, most short or empty | sorted merge | Heap size stays `<= k`; `log k ≈ 14`. |

---

## 12. Common Mistakes and Debugging

1. **Pushing `(val, node)` without a tie-breaker.** Works until two values are equal, then crashes with `TypeError` comparing `ListNode`s. Always push `(val, index, node)`.
2. **Pushing `None` nodes.** `None.val` raises `AttributeError`. Check `if node:` before pushing (both at the start and when pushing `node.next`).
3. **Pushing all nodes at once** (every node of every list). Still correct, but the heap grows to `N`, giving `O(N log N)` time and `O(N)` space — you lose the advantage.
4. **Forgetting to advance `tail`.** Only the last attached node survives.
5. **Using a max-heap mindset.** Python's `heapq` is a **min**-heap — perfect here; no negation needed.
6. **Divide and conquer off-by-one:** `range(0, k - interval, interval * 2)` ensures `i + interval < k`. Using `range(0, k, interval * 2)` can index past the end.
7. **Sequential merging into one growing list** looks like divide and conquer but is `O(N·k)` — the result is re-walked every time.

**Debugging tip:** print `sorted((v, i) for v, i, _ in heap)` at each step and compare with the dry-run table.

---

## 13. Practice Questions

**Q1. Show that pushing `(val, node)` fails on Example 1, and that `(val, i, node)` works.**

<details><summary>Hint</summary>Both `lists[0]` and `lists[1]` start with value 1. What does Python compare when the first tuple elements are equal?</summary></details>

**Answer:** With `(1, a1)` and `(1, b1)` in the heap, Python compares `a1 < b1` and raises `TypeError`. Adding a unique index in the middle settles every tie before the node is reached.

```python
import heapq

a1, b1 = ListNode(1), ListNode(1)

bad_heap = []
heapq.heappush(bad_heap, (a1.val, a1))
try:
    heapq.heappush(bad_heap, (b1.val, b1))
    failed = False
except TypeError:
    failed = True
assert failed

good_heap = []
heapq.heappush(good_heap, (a1.val, 0, a1))
heapq.heappush(good_heap, (b1.val, 1, b1))
assert heapq.heappop(good_heap)[2] is a1   # tie broken by index 0 < 1
```

**Q2. Merge `k` sorted Python lists (arrays) into one sorted list using a heap.**

<details><summary>Hint</summary>The heap entry can be `(value, list_index, element_index)` — all integers, so no tie-breaker trouble at all.</summary></details>

**Answer:**

```python
import heapq


def merge_k_arrays(arrays):
    heap = [(arr[0], i, 0) for i, arr in enumerate(arrays) if arr]
    heapq.heapify(heap)
    out = []
    while heap:
        val, i, j = heapq.heappop(heap)
        out.append(val)
        if j + 1 < len(arrays[i]):
            heapq.heappush(heap, (arrays[i][j + 1], i, j + 1))
    return out


assert merge_k_arrays([[1, 4, 5], [1, 3, 4], [2, 6]]) == [1, 1, 2, 3, 4, 4, 5, 6]
assert merge_k_arrays([]) == []
assert merge_k_arrays([[], [2], []]) == [2]
```

(Python's standard library also has `heapq.merge(*arrays)`, which does exactly this lazily: `list(heapq.merge([1, 4], [2, 3])) == [1, 2, 3, 4]`.)

**Q3. Find the `k`-th smallest element in an `n x n` matrix whose rows and columns are sorted (LeetCode 378).**

<details><summary>Hint</summary>Each row is a sorted list. Run the k-way merge over the rows and stop after `k` pops.</summary></details>

**Answer:**

```python
import heapq


def kth_smallest(matrix, k):
    heap = [(row[0], r, 0) for r, row in enumerate(matrix)]
    heapq.heapify(heap)
    for _ in range(k - 1):
        val, r, c = heapq.heappop(heap)
        if c + 1 < len(matrix[r]):
            heapq.heappush(heap, (matrix[r][c + 1], r, c + 1))
    return heap[0][0]


assert kth_smallest([[1, 5, 9], [10, 11, 13], [12, 13, 15]], 8) == 13
assert kth_smallest([[-5]], 1) == -5
assert kth_smallest([[1, 2], [1, 3]], 2) == 1
```

Time `O(k log n)`, space `O(n)`.

**Q4. With `k = 8` lists of 100 nodes each (`N = 800`), roughly how many node "touches" do sequential merging and divide-and-conquer merging need?**

<details><summary>Hint</summary>Sequential: the result grows 200, 300, …, 800. Divide and conquer: how many rounds for 8 lists?</summary></details>

**Answer:** Sequential merging walks the growing result each time: `200 + 300 + 400 + 500 + 600 + 700 + 800 = 3500` touches. Divide and conquer has `log₂ 8 = 3` rounds of `800` touches each = `2400`. The gap widens as `k` grows: `O(N·k)` versus `O(N log k)`.

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** K-way merge with a min-heap (Linked List + Heap).
- **Key idea:** Heap holds one `(val, list_index, node)` per non-empty list; pop the smallest, attach it, push its `next`. The index breaks ties so nodes are never compared.
- **Alternative:** pairwise divide-and-conquer merging using Merge Two Sorted Lists, `O(N log k)` time, `O(1)` space.
- **Time:** `O(N log k)`.
- **Auxiliary space:** `O(k)` for the heap.
- **One-line memory hook:** *"One card per friend on the tray; take the smallest, ask that friend for the next."*

### Completion checklist

- [x] Problem requirements verified
- [x] Examples and constraints verified
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force solution written and tested
- [x] Optimized Python solution (min-heap) written and tested (`tools/tests/p024.py`)
- [x] Divide-and-conquer alternative written and tested
- [x] Line-by-line explanation written
- [x] Dry run completed with a real example
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
