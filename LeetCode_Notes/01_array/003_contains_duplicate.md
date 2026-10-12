# 003. Contains Duplicate

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Contains Duplicate |
| **LeetCode number** | 217 |
| **Topic (source list)** | Array |
| **Also uses** | Hash Table, Sorting |
| **Difficulty** | Easy |
| **LeetCode URL** | <https://leetcode.com/problems/contains-duplicate/> |
| **Pattern** | Seen-set membership check |

---

## 2. Problem Explanation

### What are we given?

`nums` — a list of whole numbers.

### What must we return?

- `True` if **any** value appears **at least twice** in the list.
- `False` if **every** value is different (distinct).

### Examples

**Example 1**

```text
Input:  nums = [1, 2, 3, 1]
Output: true
```

The value `1` appears at positions 0 and 3.

**Example 2**

```text
Input:  nums = [1, 2, 3, 4]
Output: false
```

All four values are different.

**Example 3**

```text
Input:  nums = [1, 1, 1, 3, 3, 4, 3, 2, 4, 2]
Output: true
```

Several values repeat (1, 3, 4 and 2). We only need to detect that *at least one* repeat exists.

### Constraints

- `1 <= nums.length <= 10^5`
- `-10^9 <= nums[i] <= 10^9`

(In Python, LeetCode prints `true`/`false`, but your function returns the Python booleans `True`/`False`.)

---

## 3. Everyday Analogy

> **Explain it like I'm five**

You're collecting stickers from a big pile, one at a time. You have a sticker album. For every sticker you pick up, you check: *"Do I already have this one in my album?"*

- If yes — you found a duplicate! Shout "I have two of these!" and stop.
- If no — stick it in the album and pick up the next one.

If you finish the whole pile without shouting, every sticker was different.

The album is like a Python **set**: you can check "Is this sticker in here?" super quickly, without flipping through every page.

---

## 4. Step-by-Step Logic

1. **What is a duplicate?** Two different positions holding the same value.
2. **Naïve thought:** compare every pair → too many comparisons for `10^5` numbers.
3. **Better thought:** as we walk the list, remember every value already seen. The current value is a duplicate exactly when it's already remembered.
4. **Tool:** a `set` gives average `O(1)` membership checks and inserts.
5. **Stop early:** as soon as one duplicate is found, return `True`. If the loop finishes, return `False`.
6. **Alternative idea:** if you sort the list, equal values become neighbors, so you only compare adjacent elements. This uses `O(n log n)` time.

---

## 5. Brute-Force Solution

### Algorithm

For each pair of positions `i < j`, if `nums[i] == nums[j]`, return `True`. If no pair matches, return `False`.

### Python code

```python
from typing import List


class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        n = len(nums)
        for i in range(n):
            for j in range(i + 1, n):
                if nums[i] == nums[j]:
                    return True
        return False
```

### Explanation

- Every pair is compared exactly once because `j` starts at `i + 1`.
- The first equal pair proves a duplicate exists.

### Complexity

- **Time:** `O(n²)` — about 5 billion comparisons for `n = 10^5`, which **times out**.
- **Auxiliary space:** `O(1)`.

### Middle-ground: sorting

```python
from typing import List


class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        ordered = sorted(nums)  # make a sorted copy; equal values become neighbors
        for i in range(1, len(ordered)):
            if ordered[i] == ordered[i - 1]:
                return True
        return False
```

- **Time:** `O(n log n)` for sorting.
- **Auxiliary space:** `O(n)` for the sorted copy (`nums.sort()` in place would avoid the copy, but it changes the caller's list, and Python's sort still uses up to `O(n)` temporary memory).

---

## 6. Optimized Solution

### Idea

Walk once through the list, storing values in a set. If a value is already in the set, it's a duplicate.

### Algorithm

1. Create an empty set `seen`.
2. For each `num` in `nums`:
   - If `num` is in `seen`, return `True`.
   - Otherwise add `num` to `seen`.
3. Return `False`.

### Python code (LeetCode-ready)

```python
from typing import List


class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        seen = set()

        for num in nums:
            if num in seen:
                return True
            seen.add(num)

        return False
```

**One-liner alternative** (same complexity, but never stops early):

```python
from typing import List


class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        return len(set(nums)) != len(nums)
```

---

## 7. Line-by-Line Explanation

| Line | What it does | Why |
|---|---|---|
| `seen = set()` | Creates an empty set. | A set stores unique values with fast lookups. |
| `for num in nums:` | Visits every value once. | Each value must be checked against everything before it. |
| `if num in seen:` | Average `O(1)` membership test. | If true, an earlier position held the same value. |
| `return True` | Stop immediately. | One duplicate is enough; no need to scan further. |
| `seen.add(num)` | Remember this value. | Later values will be compared against it. |
| `return False` | The loop finished without a repeat. | Every value was distinct. |

**One-liner explained:** `set(nums)` removes duplicates. If the set is smaller than the list, something was removed — so a duplicate existed.

---

## 8. Dry Run

**Input:** `nums = [1, 2, 3, 1]`

| Step | `num` | `seen` before | `num in seen`? | Action | `seen` after |
|---|---|---|---|---|---|
| 1 | 1 | `{}` | No | add 1 | `{1}` |
| 2 | 2 | `{1}` | No | add 2 | `{1, 2}` |
| 3 | 3 | `{1, 2}` | No | add 3 | `{1, 2, 3}` |
| 4 | 1 | `{1, 2, 3}` | **Yes** | return `True` | — |

**Result:** `True` ✅

**Second dry run:** `nums = [1, 2, 3, 4]` → each value is new, `seen` grows to `{1, 2, 3, 4}`, the loop ends, and we return `False` ✅.

---

## 9. Concepts, Data Structures, and Patterns

- **Hash set (Python `set`):** stores unique values. `x in s` and `s.add(x)` are `O(1)` on average.
- **Early exit:** returning as soon as the answer is known saves time on inputs with an early duplicate.
- **Sorting brings equal values together:** a common trick for duplicate detection when memory is tight.
- **Space–time trade-off:**
  - Brute force: `O(n²)` time, `O(1)` space.
  - Sorting: `O(n log n)` time, little extra space if sorting in place.
  - Hash set: `O(n)` time, `O(n)` space.
- **Related problems:** Two Sum ([001_two_sum.md](001_two_sum.md)) uses a dictionary in the same "remember what you've seen" way; Valid Anagram ([../06_string/034_valid_anagram.md](../06_string/034_valid_anagram.md)) uses counting.

---

## 10. Complexity Analysis

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Brute force | `O(n²)` | `O(1)` | Compares every pair. |
| Sorting | `O(n log n)` | `O(n)` for a copy (`O(1)` extra only if an in-place sort is allowed and ignoring sort internals) | Sort, then compare neighbors. |
| Hash set (optimized) | `O(n)` average | `O(n)` | Each value is checked and inserted once; in the worst case (all distinct) the set holds all `n` values. |

---

## 11. Edge Cases

| Case | Example | Expected result | Why |
|---|---|---|---|
| Single element | `[7]` | `False` | Nothing to compare with. |
| Two equal values | `[-1, -1]` | `True` | Negatives behave like any other value. |
| All distinct | `[1, 2, 3, 4]` | `False` | Loop finishes. |
| Duplicate at the very end | `[5, 6, 7, 5]` | `True` | Found on the last step. |
| Zero and negative zero (integers) | `[0, -0]` | `True` | For integers, `-0` is just `0`. |
| Large range | `[10**9, -10**9, 10**9]` | `True` | Sets handle any integer. |

---

## 12. Common Mistakes and Debugging

1. **Adding before checking.** `seen.add(num)` followed by `if num in seen` is always true, so every list would "contain a duplicate."
2. **Using a list instead of a set.** `if num in seen_list` is an `O(n)` scan, making the whole solution `O(n²)`.
3. **Comparing non-adjacent elements after sorting.** After sorting, only neighbors need checking. Also remember `range(1, len(nums))` so `i - 1` is valid.
4. **Returning strings `"true"`/`"false"`.** Return the Python booleans `True`/`False`.
5. **Sorting the caller's list unexpectedly.** `nums.sort()` mutates the input; fine on LeetCode, but be aware in real code.

**Debugging tip:** print `num` and `seen` each iteration to see exactly when the duplicate is detected.

---

## 13. Practice Questions

**Q1. Which approach would you choose if memory were extremely limited and the input could be modified?**

<details><summary>Hint</summary>Which method does not need an extra container?</summary></details>

**Answer:** Sort in place with `nums.sort()` and compare neighbors. It uses `O(n log n)` time and avoids the `O(n)` set (Python's Timsort may still use some temporary memory, but no second container of values is created by you).

**Q2. Return the first value (in reading order) that appears for the second time, or `None`.**

<details><summary>Hint</summary>The optimized loop already finds it — return the value instead of `True`.</summary></details>

**Answer:**

```python
def first_repeated(nums):
    seen = set()
    for num in nums:
        if num in seen:
            return num
        seen.add(num)
    return None


assert first_repeated([2, 5, 1, 5, 2]) == 5
assert first_repeated([1, 2, 3]) is None
```

**Q3 (Contains Duplicate II, LeetCode 219). Return `True` if two equal values exist whose positions are at most `k` apart.**

<details><summary>Hint</summary>Store each value's most recent index in a dictionary.</summary></details>

**Answer:**

```python
def contains_nearby_duplicate(nums, k):
    last_index = {}
    for i, num in enumerate(nums):
        if num in last_index and i - last_index[num] <= k:
            return True
        last_index[num] = i
    return False


assert contains_nearby_duplicate([1, 2, 3, 1], 3) is True
assert contains_nearby_duplicate([1, 2, 3, 1, 2, 3], 2) is False
```

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** Seen-set membership check.
- **Key idea:** Walk once; if the current value is already in the set, a duplicate exists.
- **Time:** `O(n)` average.
- **Auxiliary space:** `O(n)`.
- **One-line memory hook:** *"Check the sticker album before adding the sticker."*

### Completion checklist

- [x] Problem requirements verified
- [x] Examples and constraints verified
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force solution written and tested
- [x] Optimized Python solution written and tested (`tools/tests/p003.py`)
- [x] Line-by-line explanation written
- [x] Dry run completed with a real example
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
