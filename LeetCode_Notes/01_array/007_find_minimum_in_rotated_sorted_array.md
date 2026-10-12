# 007. Find Minimum in Rotated Sorted Array

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Find Minimum in Rotated Sorted Array |
| **LeetCode number** | 153 |
| **Topic (source list)** | Array |
| **Also uses** | Binary Search |
| **Difficulty** | Medium |
| **LeetCode URL** | <https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/> |
| **Pattern** | Binary search on a rotated sorted array (compare the middle with the right end) |

---

## 2. Problem Explanation

### What are we given?

`nums` — a list of **distinct** integers that was originally sorted from smallest to largest and was then **rotated**.

### What does "rotated" mean?

Rotating once takes the **last** element and moves it to the **front**:

```text
[a0, a1, a2, ..., a(n-1)]  --rotate once-->  [a(n-1), a0, a1, ..., a(n-2)]
```

The array has been rotated somewhere between 1 and `n` times. Rotating `n` times brings it all the way back to the original sorted order. Starting from `[0, 1, 2, 4, 5, 6, 7]`:

- 4 rotations give `[4, 5, 6, 7, 0, 1, 2]`;
- 7 rotations (that's `n`) give `[0, 1, 2, 4, 5, 6, 7]` again.

So the result always looks like **two sorted runs glued together** — a "high" run followed by a "low" run — or a single fully sorted run.

### What must we return?

The **smallest value** in `nums`.

### The rules

1. All values are different (no duplicates).
2. Your algorithm **must run in `O(log n)` time** — so simply scanning every element is not what the problem is asking for.

### Examples

**Example 1**

```text
Input:  nums = [3, 4, 5, 1, 2]
Output: 1
```

This is `[1, 2, 3, 4, 5]` rotated 3 times. The smallest value, 1, sits right where the high run `3, 4, 5` ends.

**Example 2**

```text
Input:  nums = [4, 5, 6, 7, 0, 1, 2]
Output: 0
```

The sorted array `[0, 1, 2, 4, 5, 6, 7]` was rotated 4 times; 0 is at the start of the low run.

**Example 3**

```text
Input:  nums = [11, 13, 15, 17]
Output: 11
```

Rotating a 4-element array 4 times returns it to sorted order, so the minimum is simply the first element.

### Constraints

- `n == nums.length`
- `1 <= n <= 5000`
- `-5000 <= nums[i] <= 5000`
- All the integers of `nums` are unique.
- `nums` is sorted and rotated between 1 and `n` times.

---

## 3. Everyday Analogy

> **Explain it like I'm five**

Picture a staircase that goes **up, up, up**… then someone cut it and moved the top part to the front. Now you walk: up, up, up, **big drop** down to the floor, then up, up again. The lowest step is right after the drop.

You're blindfolded and can only peek at a few steps. Here's the trick: peek at the **middle step** and at the **last step**.

- If the middle step is **higher** than the last step, the drop must be somewhere **after** the middle (you have to fall down at some point to end lower). Look in the right half.
- If the middle step is **lower** than the last step, everything from the middle to the end climbs steadily, so the lowest step is the middle one **or somewhere before it**. Look in the left half (keep the middle).

Each peek throws away half the staircase, so even a staircase with 5000 steps needs only about 13 peeks.

---

## 4. Step-by-Step Logic

1. **Picture the shape.** A rotated sorted array is a rising run of large values followed by a rising run of small values (or just one rising run). The minimum is the first element of the second run.
2. **Use the last element as a reference.** Every value in the low run is `<= nums[-1]`; every value in the high run is `> nums[-1]`. So comparing any element with the right end tells you which run it belongs to.
3. **Binary search with `lo` and `hi`.** Keep the invariant "the minimum is inside `nums[lo..hi]`".
4. **Look at `mid`:**
   - `nums[mid] > nums[hi]` → `mid` is in the high run; the minimum is strictly to the right: `lo = mid + 1`.
   - `nums[mid] < nums[hi]` → `mid..hi` is sorted, so the minimum is at `mid` or to its left: `hi = mid` (do **not** skip `mid`; it might be the answer).
   - Equality can't happen while `lo < hi` because `mid < hi` and values are distinct.
5. **Stop when `lo == hi`.** One candidate remains — it is the minimum.

---

## 5. Brute-Force Solution

### Algorithm

Look at every element and keep the smallest one. (Python's `min(nums)` does the same thing.)

### Python code

```python
from typing import List


class Solution:
    def findMin(self, nums: List[int]) -> int:
        smallest = nums[0]
        for num in nums:
            if num < smallest:
                smallest = num
        return smallest
```

### Explanation

- It ignores the rotated-sorted structure completely and just compares every value.
- It is correct for any list, rotated or not.

### Complexity

- **Time:** `O(n)`. With `n <= 5000` it would actually run fast enough on LeetCode, but it **does not meet the required `O(log n)`**, so it is not an acceptable interview answer.
- **Auxiliary space:** `O(1)`.

---

## 6. Optimized Solution

### Idea — binary search against the right end

Compare the middle element with the element at `hi`. That single comparison tells us which half still contains the "drop" (the minimum).

### Algorithm

1. `lo = 0`, `hi = len(nums) - 1`.
2. While `lo < hi`:
   - `mid = (lo + hi) // 2`.
   - If `nums[mid] > nums[hi]`: `lo = mid + 1`.
   - Else: `hi = mid`.
3. Return `nums[lo]`.

### Python code (LeetCode-ready)

```python
from typing import List


class Solution:
    def findMin(self, nums: List[int]) -> int:
        lo, hi = 0, len(nums) - 1

        while lo < hi:
            mid = (lo + hi) // 2
            if nums[mid] > nums[hi]:
                lo = mid + 1      # mid is in the high run; min is to the right
            else:
                hi = mid          # mid..hi is sorted; min is mid or to its left

        return nums[lo]
```

### Variant with an early exit

If the current window `nums[lo..hi]` is already sorted (`nums[lo] < nums[hi]`), its first element is the minimum. This is the same algorithm with a shortcut; it is still `O(log n)`.

```python
from typing import List


class Solution:
    def findMin(self, nums: List[int]) -> int:
        lo, hi = 0, len(nums) - 1
        while lo < hi:
            if nums[lo] < nums[hi]:   # window is not rotated
                return nums[lo]
            mid = (lo + hi) // 2
            if nums[mid] >= nums[lo]:
                lo = mid + 1          # mid is in the high run (left part)
            else:
                hi = mid              # mid is in the low run
        return nums[lo]
```

In this variant the window is known to be rotated when we reach `mid`, so `nums[mid] >= nums[lo]` means `mid` is still on the high run. (`>=` matters when `mid == lo`.)

---

## 7. Line-by-Line Explanation

(Main binary-search version)

| Line | What it does | Why |
|---|---|---|
| `lo, hi = 0, len(nums) - 1` | The search window is the whole array. | The minimum is somewhere in `nums[0..n-1]`. |
| `while lo < hi:` | Loop while more than one candidate remains. | When `lo == hi`, the single remaining index is the answer. Using `<` (not `<=`) avoids an infinite loop with `hi = mid`. |
| `mid = (lo + hi) // 2` | Middle index, rounded down. | Rounding down guarantees `mid < hi`, so `nums[mid]` and `nums[hi]` are different elements. |
| `if nums[mid] > nums[hi]:` | Is `mid` in the high run? | A value bigger than the right end must come before the drop. |
| `lo = mid + 1` | Discard `lo..mid`. | None of those can be the minimum: they're all in the high run (and `nums[hi]` is smaller). |
| `else: hi = mid` | Discard `mid+1..hi`. | `nums[mid..hi]` is increasing, so `nums[mid]` is the smallest there; keep `mid`. |
| `return nums[lo]` | Return the last candidate. | The invariant guarantees it is the minimum. |

---

## 8. Dry Run

**Input:** `nums = [4, 5, 6, 7, 0, 1, 2]` (Example 2)

| Step | `lo` | `hi` | `mid` | `nums[mid]` | `nums[hi]` | Comparison | Action |
|---|---|---|---|---|---|---|---|
| 1 | 0 | 6 | 3 | 7 | 2 | 7 > 2 | `lo = 4` |
| 2 | 4 | 6 | 5 | 1 | 2 | 1 < 2 | `hi = 5` |
| 3 | 4 | 5 | 4 | 0 | 1 | 0 < 1 | `hi = 4` |
| — | 4 | 4 | — | — | — | `lo == hi` | stop |

**Result:** `nums[4] = 0` ✅ — three comparisons for seven elements.

**Example 1:** `nums = [3, 4, 5, 1, 2]`

| Step | `lo` | `hi` | `mid` | `nums[mid]` | `nums[hi]` | Action |
|---|---|---|---|---|---|---|
| 1 | 0 | 4 | 2 | 5 | 2 | 5 > 2 → `lo = 3` |
| 2 | 3 | 4 | 3 | 1 | 2 | 1 < 2 → `hi = 3` |

**Result:** `nums[3] = 1` ✅

**Example 3 (not rotated):** `nums = [11, 13, 15, 17]` → `mid = 1` (13 < 17, `hi = 1`), `mid = 0` (11 < 13, `hi = 0`). **Result:** `11` ✅

---

## 9. Concepts, Data Structures, and Patterns

- **Binary search:** repeatedly halve a search window using a test that tells you which half contains the answer. It needs `O(log n)` steps.
- **Binary search on a property, not a value:** we are not looking for a known number; we're looking for the boundary where "element `> nums[-1]`" turns into "element `<= nums[-1]`". This "find the first index where a condition becomes true" template is very common.
- **Loop invariant:** "the minimum is always in `nums[lo..hi]`". Each update keeps it true, and the loop ends with a single candidate.
- **`lo < hi` with `hi = mid`** vs **`lo <= hi` with `hi = mid - 1`:** use the first form when `mid` itself might be the answer.
- **Related notes:** [008_search_in_rotated_sorted_array.md](008_search_in_rotated_sorted_array.md) uses the same "which half is sorted?" reasoning to find a target. Find Minimum in Rotated Sorted Array II (LeetCode 154) allows duplicates (see Q3 below).

---

## 10. Complexity Analysis

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Linear scan (brute force) | `O(n)` | `O(1)` | Looks at every element once. |
| Binary search (optimized) | `O(log n)` | `O(1)` | Every iteration shrinks the window `hi - lo + 1` to about half; for `n = 5000` that is at most about 13 iterations. Only `lo`, `hi`, `mid` are stored. |
| Early-exit variant | `O(log n)` | `O(1)` | Same halving, sometimes finishing sooner. |

---

## 11. Edge Cases

| Case | Example | Expected result | Why |
|---|---|---|---|
| Single element | `[1]` | `1` | Loop never runs; return `nums[0]`. |
| Not rotated (rotated `n` times) | `[11, 13, 15, 17]` | `11` | Always `nums[mid] < nums[hi]`, so `hi` walks down to 0. |
| Two elements, rotated | `[2, 1]` | `1` | `mid = 0`, `2 > 1` → `lo = 1`. |
| Two elements, sorted | `[1, 2]` | `1` | `mid = 0`, `1 < 2` → `hi = 0`. |
| Minimum at the last index | `[2, 3, 4, 5, 1]` | `1` | Each step moves `lo` right. |
| Minimum at index 1 | `[5, 1, 2, 3, 4]` | `1` | `mid` lands in the low run, so `hi` moves left until `lo` jumps past the 5. |
| Negative values | `[-1, -5000, -3]` (that is `[-5000, -3, -1]` rotated once) | `-5000` | Comparisons work the same for negatives. |

---

## 12. Common Mistakes and Debugging

1. **Comparing `mid` with `lo` in the basic loop.** `nums[mid] > nums[lo]` does not tell you where the minimum is when the window is already sorted (e.g. `[1, 2, 3]` would move `lo` right and miss 1). Comparing with `nums[hi]` works in every case.
2. **Writing `hi = mid - 1`.** `mid` might be the minimum (e.g. `[4, 5, 1, 2, 3]`: `mid = 2`, value 1). Skipping it loses the answer.
3. **Using `while lo <= hi` together with `hi = mid`.** When `lo == hi`, `mid == hi`, the `else` branch sets `hi = mid` again — an infinite loop.
4. **Returning `nums[mid]` instead of `nums[lo]`.** After the loop, `mid` may be stale.
5. **Assuming the array is always rotated.** Rotating `n` times gives the original sorted array; the code must handle it (it does).

**Debugging tip:** print `lo, hi, mid, nums[lo:hi+1]` each iteration. The minimum must always remain inside the printed slice.

---

## 13. Practice Questions

**Q1. Trace the binary search on `[6, 7, 1, 2, 3, 4, 5]`.**

<details><summary>Hint</summary>Compare `nums[mid]` with `nums[hi]` each time.</summary></details>

**Answer:** `lo=0, hi=6, mid=3`: `2 < 5` → `hi = 3`. `lo=0, hi=3, mid=1`: `7 > 2` → `lo = 2`. `lo=2, hi=3, mid=2`: `1 < 2` → `hi = 2`. Stop: `nums[2] = 1`.

**Q2. Return how many times the sorted array was rotated (a number from `0` to `n - 1`, where `0` means "sorted order").**

<details><summary>Hint</summary>The rotation count equals the index of the minimum.</summary></details>

**Answer:** Run the same search but return `lo` instead of `nums[lo]`.

```python
def rotation_count(nums):
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] > nums[hi]:
            lo = mid + 1
        else:
            hi = mid
    return lo


assert rotation_count([3, 4, 5, 1, 2]) == 3
assert rotation_count([4, 5, 6, 7, 0, 1, 2]) == 4
assert rotation_count([11, 13, 15, 17]) == 0   # rotated n times = sorted
```

(For Example 3 the statement says "rotated 4 times"; modulo `n = 4` that's 0.)

**Q3. What changes if duplicates are allowed (LeetCode 154)?**

<details><summary>Hint</summary>What can you conclude when `nums[mid] == nums[hi]`?</summary></details>

**Answer:** When `nums[mid] == nums[hi]` you cannot tell which side the drop is on (`[3, 3, 1, 3]` vs `[3, 1, 3, 3]`). But you can safely drop `hi`, because `nums[mid]` has the same value and stays in the window. Worst-case time becomes `O(n)` (e.g. all equal values).

```python
def find_min_with_duplicates(nums):
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] > nums[hi]:
            lo = mid + 1
        elif nums[mid] < nums[hi]:
            hi = mid
        else:
            hi -= 1          # equal: discard one copy safely
    return nums[lo]


assert find_min_with_duplicates([2, 2, 2, 0, 1]) == 0
assert find_min_with_duplicates([3, 3, 1, 3]) == 1
assert find_min_with_duplicates([3, 1, 3, 3]) == 1
assert find_min_with_duplicates([1, 3, 5]) == 1
```

**Q4. Why does `mid = (lo + hi) // 2` guarantee `mid < hi` inside the loop, and why does that matter?**

<details><summary>Hint</summary>Inside the loop, `lo < hi`.</summary></details>

**Answer:** With `lo < hi`, `lo + hi < 2·hi`, so `(lo + hi) // 2 < hi`. That means `nums[mid]` and `nums[hi]` are two different elements, so with distinct values they can never be equal, and both branches strictly shrink the window (`lo = mid + 1 > lo` or `hi = mid < hi`). The loop always terminates.

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** Binary search for a boundary.
- **Key idea:** if `nums[mid] > nums[hi]`, the minimum is right of `mid` (`lo = mid + 1`); otherwise it is at `mid` or left (`hi = mid`). Loop while `lo < hi`; answer `nums[lo]`.
- **Time:** `O(log n)`.
- **Auxiliary space:** `O(1)`.
- **One-line memory hook:** *"Middle higher than the end? The drop is to the right."*

### Completion checklist

- [x] Problem requirements verified
- [x] Examples and constraints verified
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force solution written and tested
- [x] Optimized Python solution written and tested (`tools/tests/p007.py`), plus the early-exit variant
- [x] Line-by-line explanation written
- [x] Dry run completed with a real example
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
