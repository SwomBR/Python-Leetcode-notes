# 008. Search in Rotated Sorted Array

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Search in Rotated Sorted Array |
| **LeetCode number** | 33 |
| **Topic (source list)** | Array |
| **Also uses** | Binary Search |
| **Difficulty** | Medium |
| **LeetCode URL** | <https://leetcode.com/problems/search-in-rotated-sorted-array/> |
| **Pattern** | Modified binary search — "one half is always sorted" |

---

## 2. Problem Explanation

### What are we given?

- `nums` — a list of **distinct** integers. It started out sorted in increasing order, and **may** then have been rotated: some number of elements were taken from the front and moved, in order, to the back.
- `target` — the integer we are looking for.

### What does the rotation look like?

If the original array is `[0, 1, 2, 4, 5, 6, 7]` and the split point is index `k = 3`, the front part `[0, 1, 2]` moves to the back:

```text
[0, 1, 2, 4, 5, 6, 7]  -->  [4, 5, 6, 7, 0, 1, 2]
```

In general the array becomes `nums[k], nums[k+1], ..., nums[n-1], nums[0], ..., nums[k-1]` for some unknown `k` with `1 <= k < n`. The word "possibly" in the statement means the array might also arrive not rotated at all, so the code must handle a plain sorted array too.

### What must we return?

The **index** of `target` inside the array we receive, or `-1` if `target` is not there.

### The rules

1. All values are different, so there is at most one correct index.
2. Your algorithm **must run in `O(log n)` time** — a plain left-to-right scan is not acceptable.

### Examples

**Example 1**

```text
Input:  nums = [4, 5, 6, 7, 0, 1, 2], target = 0
Output: 4
```

The value 0 is at position 4 (counting from 0).

**Example 2**

```text
Input:  nums = [4, 5, 6, 7, 0, 1, 2], target = 3
Output: -1
```

3 is not one of the values, so the answer is -1.

**Example 3**

```text
Input:  nums = [1], target = 0
Output: -1
```

The only value is 1, which is not 0.

### Constraints

- `1 <= nums.length <= 5000`
- `-10^4 <= nums[i] <= 10^4`
- All values of `nums` are unique.
- `nums` is an ascending array that is possibly rotated.
- `-10^4 <= target <= 10^4`

---

## 3. Everyday Analogy

> **Explain it like I'm five**

You have a shelf of numbered storybooks in order, 1 to 100. Your little brother grabbed the first chunk of books and put them at the end of the shelf, still in order. So now the shelf reads, for example, 40, 41, …, 100, 1, 2, …, 39.

You want book number 7. Normally you'd open the shelf in the middle and decide "left or right?". You can still do that! Whenever you look at the middle book, **one side of it is still perfectly in order** — the mess (the jump from 100 back to 1) can only be on one side.

So you ask:

1. "Which side is neat?" (Compare the first book of the section with the middle book.)
2. "Is my book's number inside the neat side's range?" If yes, search there. If no, it must be on the other side.

Each question throws away half the shelf, just like a normal binary search.

---

## 4. Step-by-Step Logic

1. **Normal binary search fails directly.** In `[4, 5, 6, 7, 0, 1, 2]`, looking for 0: the middle is 7, and "0 < 7, go left" is wrong.
2. **Key observation:** cut any window `nums[lo..hi]` at `mid`. At least one of the halves `nums[lo..mid]` or `nums[mid..hi]` is **sorted**, because the single "drop" point can only be in one of them.
3. **Which one?** If `nums[lo] <= nums[mid]`, the left half has no drop, so it's sorted. Otherwise the drop is in the left half, so the right half `nums[mid..hi]` is sorted.
4. **Is the target in the sorted half?** For a sorted range we can check membership with two comparisons:
   - left half sorted: `nums[lo] <= target < nums[mid]`
   - right half sorted: `nums[mid] < target <= nums[hi]`
5. **Move the window.** If the target is in the sorted half, search there; otherwise search the other half.
6. **Stop** when `nums[mid] == target` (return `mid`) or the window becomes empty (`lo > hi`, return `-1`).

---

## 5. Brute-Force Solution

### Algorithm

Walk through the list and return the first index whose value equals `target`; return `-1` if none does.

### Python code

```python
from typing import List


class Solution:
    def search(self, nums: List[int], target: int) -> int:
        for i, num in enumerate(nums):
            if num == target:
                return i
        return -1
```

### Explanation

- Every position is checked once; since values are unique, the first match is the only match.
- Rotation does not matter for a linear scan.

### Complexity

- **Time:** `O(n)`. For `n <= 5000` this would actually run quickly, but it **violates the required `O(log n)`**, so it is not an accepted interview answer.
- **Auxiliary space:** `O(1)`.

---

## 6. Optimized Solution

### Idea — binary search on the sorted half

At every step, find the half of the window that is sorted, check whether `target` lies inside its range, and keep only the half that can contain it.

### Algorithm

1. `lo = 0`, `hi = n - 1`.
2. While `lo <= hi`:
   - `mid = (lo + hi) // 2`. If `nums[mid] == target`, return `mid`.
   - If `nums[lo] <= nums[mid]` (left half sorted):
     - if `nums[lo] <= target < nums[mid]`: `hi = mid - 1`, else `lo = mid + 1`.
   - Else (right half sorted):
     - if `nums[mid] < target <= nums[hi]`: `lo = mid + 1`, else `hi = mid - 1`.
3. Return `-1`.

### Python code (LeetCode-ready)

```python
from typing import List


class Solution:
    def search(self, nums: List[int], target: int) -> int:
        lo, hi = 0, len(nums) - 1

        while lo <= hi:
            mid = (lo + hi) // 2
            if nums[mid] == target:
                return mid

            if nums[lo] <= nums[mid]:                 # left half is sorted
                if nums[lo] <= target < nums[mid]:
                    hi = mid - 1                      # target is in the left half
                else:
                    lo = mid + 1
            else:                                     # right half is sorted
                if nums[mid] < target <= nums[hi]:
                    lo = mid + 1                      # target is in the right half
                else:
                    hi = mid - 1

        return -1
```

### Alternative: find the rotation point, then do a normal binary search

1. Use the method from [007_find_minimum_in_rotated_sorted_array.md](007_find_minimum_in_rotated_sorted_array.md) to find `pivot`, the index of the smallest element.
2. The array is now two sorted runs: `nums[pivot..n-1]` and `nums[0..pivot-1]`. Decide which run could hold `target` and binary-search only that run.

```python
from typing import List
import bisect


class Solution:
    def search(self, nums: List[int], target: int) -> int:
        n = len(nums)
        lo, hi = 0, n - 1
        while lo < hi:                       # find index of the minimum
            mid = (lo + hi) // 2
            if nums[mid] > nums[hi]:
                lo = mid + 1
            else:
                hi = mid
        pivot = lo

        # nums[pivot..n-1] holds the values <= nums[-1]; nums[0..pivot-1] the larger ones
        if target <= nums[-1]:
            left, right = pivot, n
        else:
            left, right = 0, pivot
        i = bisect.bisect_left(nums, target, left, right)
        return i if i < right and nums[i] == target else -1
```

Both phases are `O(log n)`, so the total is `O(log n)`. It uses two binary searches instead of one, but some people find it easier to get right.

---

## 7. Line-by-Line Explanation

(One-pass version)

| Line | What it does | Why |
|---|---|---|
| `lo, hi = 0, len(nums) - 1` | Window = whole array. | Target could be anywhere. |
| `while lo <= hi:` | Loop while the window is non-empty. | A one-element window (`lo == hi`) must still be checked. |
| `mid = (lo + hi) // 2` | Middle index. | Halves the window. |
| `if nums[mid] == target: return mid` | Direct hit. | Values are unique, so this is the answer. |
| `if nums[lo] <= nums[mid]:` | Is `nums[lo..mid]` sorted? | If the first element is not bigger than the middle one, the drop is not in this half. `<=` (not `<`) covers `lo == mid`, a one-element half that is trivially sorted. |
| `if nums[lo] <= target < nums[mid]:` | Is the target inside the sorted left half's range? | In a sorted range, membership is just "between the ends". `< nums[mid]` because `mid` was already checked. |
| `hi = mid - 1` / `lo = mid + 1` | Keep the half that can contain the target. | The other half is impossible. |
| `else:` | Otherwise `nums[mid..hi]` is sorted. | The drop is in the left half. |
| `if nums[mid] < target <= nums[hi]:` | Is the target inside the sorted right half? | Same range check on the other side. |
| `lo = mid + 1` / `hi = mid - 1` | Keep the correct half. | — |
| `return -1` | Window became empty. | Target is not in the array. |

---

## 8. Dry Run

**Input:** `nums = [4, 5, 6, 7, 0, 1, 2]`, `target = 0` (Example 1)

| Step | `lo` | `hi` | `mid` | `nums[mid]` | Sorted half | Target in that half's range? | Action |
|---|---|---|---|---|---|---|---|
| 1 | 0 | 6 | 3 | 7 | left (`4 <= 7`): `[4..7]` | `4 <= 0 < 7`? No | `lo = 4` |
| 2 | 4 | 6 | 5 | 1 | left (`0 <= 1`): `[0..1]` | `0 <= 0 < 1`? Yes | `hi = 4` |
| 3 | 4 | 4 | 4 | 0 | — | `nums[mid] == target` | return `4` |

**Result:** `4` ✅

**Example 2:** `nums = [4, 5, 6, 7, 0, 1, 2]`, `target = 3`

| Step | `lo` | `hi` | `mid` | `nums[mid]` | Sorted half | In range? | Action |
|---|---|---|---|---|---|---|---|
| 1 | 0 | 6 | 3 | 7 | left `[4..7]` | `4 <= 3`? No | `lo = 4` |
| 2 | 4 | 6 | 5 | 1 | left `[0..1]` | `0 <= 3 < 1`? No | `lo = 6` |
| 3 | 6 | 6 | 6 | 2 | left `[2..2]` | `2 <= 3 < 2`? No | `lo = 7` |
| — | 7 | 6 | — | — | — | window empty | return `-1` |

**Result:** `-1` ✅

**Example 3:** `nums = [1]`, `target = 0` → `mid = 0`, `1 != 0`, left half `[1..1]` sorted, `1 <= 0`? No → `lo = 1 > hi = 0` → `-1` ✅

---

## 9. Concepts, Data Structures, and Patterns

- **Binary search:** halve the search space each step → `O(log n)`.
- **Modified binary search:** the decision "go left or right" uses extra reasoning (which half is sorted) instead of a single comparison.
- **Invariant:** "if `target` is in the array, it is in `nums[lo..hi]`". Each branch discards only a half that provably cannot contain it.
- **Range check on a sorted segment:** `first <= x <= last` tells you whether `x` could be in a sorted run.
- **Two-phase alternative:** find the rotation point (the minimum — see [007_find_minimum_in_rotated_sorted_array.md](007_find_minimum_in_rotated_sorted_array.md)), then use Python's `bisect` on the right run.
- **Related problems:** Search in Rotated Sorted Array II (LeetCode 81, duplicates), Find Minimum in Rotated Sorted Array (LeetCode 153), Binary Search (LeetCode 704).

---

## 10. Complexity Analysis

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Linear scan (brute force) | `O(n)` | `O(1)` | Checks each element once. |
| One-pass modified binary search | `O(log n)` | `O(1)` | Each iteration does `O(1)` comparisons and removes at least half of the window; at most about 13 iterations for `n = 5000`. |
| Pivot + `bisect` | `O(log n)` | `O(1)` | Two binary searches, each `O(log n)`. `bisect_left` with `lo`/`hi` arguments does not copy the list. |

---

## 11. Edge Cases

| Case | Example | Expected result | Why |
|---|---|---|---|
| Single element, missing | `nums = [1]`, `target = 0` | `-1` | Official Example 3. |
| Single element, present | `nums = [1]`, `target = 1` | `0` | Found at `mid = 0`. |
| Not rotated | `nums = [1, 3]`, `target = 3` | `1` | Behaves like normal binary search. |
| Two elements, rotated | `nums = [3, 1]`, `target = 1` | `1` | Needs `nums[lo] <= nums[mid]` with `<=` (see mistakes). |
| Target is the first element | `nums = [4, 5, 6, 7, 0, 1, 2]`, `target = 4` | `0` | Left half `[4..7]` contains 4. |
| Target is the last element | `nums = [4, 5, 6, 7, 0, 1, 2]`, `target = 2` | `6` | Right side search. |
| Target bigger than all values | `nums = [5, 1, 3]`, `target = 9` | `-1` | Window empties. |
| Target at index 0 in a 3-element rotated array | `nums = [5, 1, 3]`, `target = 5` | `0` | Right half `[1..3]` is sorted and doesn't contain 5 → go left. |

---

## 12. Common Mistakes and Debugging

1. **Using `<` instead of `<=` in `nums[lo] <= nums[mid]`.** For `nums = [3, 1]`, `target = 1`: `lo = mid = 0`. With `<`, the code believes the right half `nums[0..1] = [3, 1]` is sorted, checks `3 < 1 <= 1` (false) and sets `hi = -1`, returning `-1` — wrong.
2. **Wrong boundary in the range check.** Using `nums[lo] < target` skips a target equal to `nums[lo]`. The ends of the sorted half must be inclusive (except `mid`, already tested).
3. **Deciding direction from `target` vs `nums[mid]` alone.** That is ordinary binary search and fails on rotated input.
4. **`while lo < hi` with `hi = mid - 1`.** You may exit with one unchecked element left. Use `lo <= hi` in this style.
5. **Returning the value instead of the index.**

**Debugging tip:** print `lo, hi, mid, nums[lo:hi+1]` and which half your code thinks is sorted. If the printed "sorted" half isn't actually sorted, the condition is wrong.

---

## 13. Practice Questions

**Q1. Trace the one-pass search on `nums = [6, 7, 8, 1, 2, 3, 4, 5]`, `target = 8`.**

<details><summary>Hint</summary>First `mid = 3`. Which half is sorted?</summary></details>

**Answer:** `lo=0, hi=7, mid=3` (value 1). `nums[0]=6 <= 1`? No → right half `[1..5]` sorted; `1 < 8 <= 5`? No → `hi = 2`. `lo=0, hi=2, mid=1` (value 7). Left half `[6..7]` sorted; `6 <= 8 < 7`? No → `lo = 2`. `mid = 2`, value 8 → return `2`.

**Q2. Duplicates allowed (LeetCode 81): return `True`/`False` for whether `target` exists.**

<details><summary>Hint</summary>When `nums[lo] == nums[mid] == nums[hi]` you can't tell which half is sorted. Shrink both ends by one.</summary></details>

**Answer:** Worst case becomes `O(n)` (e.g. `[1, 1, 1, 1, 0, 1, 1]`), but typical inputs are still fast.

```python
def search_with_duplicates(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return True
        if nums[lo] == nums[mid] == nums[hi]:
            lo += 1
            hi -= 1
        elif nums[lo] <= nums[mid]:
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return False


assert search_with_duplicates([2, 5, 6, 0, 0, 1, 2], 0) is True
assert search_with_duplicates([2, 5, 6, 0, 0, 1, 2], 3) is False
assert search_with_duplicates([1, 0, 1, 1, 1], 0) is True
assert search_with_duplicates([1, 1, 1, 1, 0, 1, 1], 0) is True
```

**Q3. Given a rotated sorted array of distinct values, return the value at "sorted position" `k` (0-based: `k = 0` is the smallest) in `O(log n)`.**

<details><summary>Hint</summary>Find the rotation point `pivot` (index of the minimum). Sorted position `k` lives at index `(pivot + k) % n`.</summary></details>

**Answer:**

```python
def kth_smallest_rotated(nums, k):
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] > nums[hi]:
            lo = mid + 1
        else:
            hi = mid
    return nums[(lo + k) % len(nums)]


assert kth_smallest_rotated([4, 5, 6, 7, 0, 1, 2], 0) == 0
assert kth_smallest_rotated([4, 5, 6, 7, 0, 1, 2], 3) == 4
assert kth_smallest_rotated([4, 5, 6, 7, 0, 1, 2], 6) == 7
assert kth_smallest_rotated([1, 2, 3], 1) == 2
```

**Q4. Why is `target < nums[mid]` (strict) used in the left-half check, while `nums[lo] <= target` is inclusive?**

<details><summary>Hint</summary>What do we already know about `nums[mid]` at that point?</summary></details>

**Answer:** We already returned if `nums[mid] == target`, so the target cannot equal `nums[mid]` — strict is enough there. But `nums[lo]` has not been compared with the target yet, so `nums[lo] == target` must still count as "inside the left half".

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** Modified binary search on a rotated sorted array.
- **Key idea:** one half around `mid` is always sorted (`nums[lo] <= nums[mid]` → left). If `target` is within that sorted half's ends, go there; otherwise go to the other half.
- **Time:** `O(log n)`.
- **Auxiliary space:** `O(1)`.
- **One-line memory hook:** *"Find the neat half; is my book in it? If not, it's on the other side."*

### Completion checklist

- [x] Problem requirements verified
- [x] Examples and constraints verified
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force solution written and tested
- [x] Optimized Python solution written and tested (`tools/tests/p008.py`), plus the pivot + bisect alternative
- [x] Line-by-line explanation written
- [x] Dry run completed with a real example
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
