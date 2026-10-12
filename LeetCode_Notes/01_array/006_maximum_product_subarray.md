# 006. Maximum Product Subarray

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Maximum Product Subarray |
| **LeetCode number** | 152 |
| **Topic (source list)** | Array |
| **Also uses** | Dynamic Programming |
| **Difficulty** | Medium |
| **LeetCode URL** | <https://leetcode.com/problems/maximum-product-subarray/> |
| **Pattern** | Kadane-style DP that tracks both the maximum and the minimum product |

---

## 2. Problem Explanation

### What are we given?

`nums` — a list of integers. Values can be negative, zero or positive.

### What must we return?

The **largest product** you can get by multiplying together the elements of one **subarray**.

A **subarray** is a **contiguous, non-empty** slice: the elements must sit next to each other and you must take at least one. For `[2, 3, -2]`:
- `[2, 3]`, `[3, -2]`, `[-2]` and `[2, 3, -2]` are subarrays.
- `[2, -2]` is **not** (it skips the `3`).

### The rules

1. A subarray with just one element has that element as its product (so `[-2]` has product `-2`).
2. You return only the product, not the subarray itself.
3. The test data is built so that the answer — and in fact the product of **any** subarray — fits in a 32-bit signed integer.

### Why is this harder than Maximum Subarray (sum)?

With sums, a negative running total is always bad, so you drop it. With products, a **negative** running product can suddenly become the **best** one: multiply it by another negative number and it flips to a large positive value. Zeros also wipe out everything they touch. So the "drop the bad part" rule from Kadane's sum algorithm does not work directly.

### Examples

**Example 1**

```text
Input:  nums = [2, 3, -2, 4]
Output: 6
```

`[2, 3]` multiplies to 6. Including the `-2` makes the product negative, and `[4]` alone is only 4, so 6 is the best.

**Example 2**

```text
Input:  nums = [-2, 0, -1]
Output: 0
```

You might hope for `(-2) × (-1) = 2`, but those two numbers are not next to each other — the `0` sits between them — so `[-2, -1]` is not a subarray. The best real choice is `[0]` (or any subarray containing the zero), which gives 0.

### Constraints

- `1 <= nums.length <= 2 * 10^4`
- `-10 <= nums[i] <= 10`
- The product of any subarray of `nums` is guaranteed to fit in a 32-bit integer.

---

## 3. Everyday Analogy

> **Explain it like I'm five**

Imagine a magic machine with a row of buttons. Each button multiplies your score by its number. A "−" button flips your score from happy (positive) to sad (negative) or back again. A "0" button breaks the machine and your score becomes 0.

You may press one **unbroken run** of neighbouring buttons. Which run gives the biggest score?

While walking along the buttons you keep **two** notes in your pocket:

- 😀 **the biggest score** you could have if your run ends right here, and
- 😢 **the smallest (most negative) score** you could have if your run ends right here.

Why keep the sad note? Because when the next button is a "−" button, the saddest score flips into the happiest one! A score of −12 times −2 becomes +24.

At each button you look at three options — start fresh with just this button, extend the happy run, or extend the sad run — and update both notes. You also write down the best happy score you have ever seen. That record is the answer.

---

## 4. Step-by-Step Logic

1. **Every subarray ends somewhere.** Focus on subarrays that end exactly at index `i`.
2. **What's the largest product ending at `i`?** It is one of:
   - `nums[i]` by itself (start fresh),
   - (largest product ending at `i - 1`) × `nums[i]` — good when `nums[i]` is positive,
   - (smallest product ending at `i - 1`) × `nums[i]` — good when `nums[i]` is negative, because negative × negative is positive.
3. **What's the smallest product ending at `i`?** The minimum of the same three candidates. We need it for the *next* step.
4. **So keep two running values**, `cur_max` and `cur_min`, and update them together from the **old** values (compute both before overwriting either).
5. **Zeros are handled automatically.** If `nums[i] == 0`, all three candidates are 0, so both running values become 0; on the next step the "start fresh" candidate `nums[i+1]` lets us continue past the zero.
6. **Answer** = the largest `cur_max` seen at any index. Start it at `nums[0]` (not 0), because the subarray must be non-empty — for `[-2]` the answer is `-2`.

---

## 5. Brute-Force Solution

### Algorithm

For every start index `i`, extend the end index `j` one step at a time while keeping a running product of `nums[i..j]`, and remember the largest product seen.

### Python code

```python
from typing import List


class Solution:
    def maxProduct(self, nums: List[int]) -> int:
        n = len(nums)
        best = nums[0]
        for start in range(n):
            product = 1
            for end in range(start, n):
                product *= nums[end]        # product of nums[start..end]
                best = max(best, product)
        return best
```

### Explanation

- Each pair `(start, end)` describes one subarray, and every subarray is visited exactly once.
- Re-multiplying the whole slice each time would cost `O(n³)`. Extending the running `product` by one element keeps it at `O(n²)`.
- `best` starts at `nums[0]`, which is itself a valid subarray product, so single negative numbers are handled.
- Zeros are fine: once `product` hits 0 it stays 0 for that start index, which is the correct product of those longer slices.

### Complexity

- **Time:** `O(n²)` — about `n(n+1)/2 ≈ 2 × 10^8` multiplications for `n = 2 × 10^4`. That is far too slow in Python and **would time out** on LeetCode.
- **Auxiliary space:** `O(1)` — a few variables.

---

## 6. Optimized Solution

### Idea — Kadane with a max **and** a min

Walk once through the array. At each position keep:

- `cur_max` — the largest product of a subarray ending here,
- `cur_min` — the smallest product of a subarray ending here,
- `best` — the largest `cur_max` seen so far.

### Algorithm

1. `cur_max = cur_min = best = nums[0]`.
2. For each `num` after the first:
   - Compute three candidates: `num`, `cur_max * num`, `cur_min * num`.
   - `cur_max` = the largest candidate, `cur_min` = the smallest candidate (both from the old values).
   - `best = max(best, cur_max)`.
3. Return `best`.

### Python code (LeetCode-ready)

```python
from typing import List


class Solution:
    def maxProduct(self, nums: List[int]) -> int:
        cur_max = cur_min = best = nums[0]

        for i in range(1, len(nums)):
            num = nums[i]
            candidates = (num, cur_max * num, cur_min * num)
            cur_max = max(candidates)   # best product ending at i
            cur_min = min(candidates)   # worst product ending at i
            best = max(best, cur_max)

        return best
```

### Alternative: prefix and suffix products (`O(n)`, `O(1)`)

A different, very short idea. Inside a stretch with no zeros, the best product is always a **prefix** or a **suffix** of that stretch: if the stretch has an even number of negatives, take all of it; if odd, drop everything up to and including the first negative (keep a suffix) or from the last negative onward (keep a prefix). So scan products from the left and from the right, restarting after each zero.

```python
from typing import List


class Solution:
    def maxProduct(self, nums: List[int]) -> int:
        n = len(nums)
        best = nums[0]
        prefix = suffix = 0
        for i in range(n):
            # "or 1" restarts the running product after a zero (or at the start)
            prefix = (prefix or 1) * nums[i]
            suffix = (suffix or 1) * nums[n - 1 - i]
            best = max(best, prefix, suffix)
        return best
```

`prefix or 1` evaluates to `1` when `prefix` is `0`, so a zero ends the current stretch and the next element starts a new one. The zero itself still gets compared with `best` (when `prefix` becomes 0), which is how `[-2, 0, -1]` returns 0.

---

## 7. Line-by-Line Explanation

(Max/min DP version)

| Line | What it does | Why |
|---|---|---|
| `cur_max = cur_min = best = nums[0]` | All three start at the first element. | The only subarray ending at index 0 is `[nums[0]]`. Starting `best` at `nums[0]` (not 0 or 1) handles inputs like `[-2]`. |
| `for i in range(1, len(nums)):` | Visits every remaining index. | Index 0 is already processed. |
| `num = nums[i]` | Current value. | Short name for readability. |
| `candidates = (num, cur_max * num, cur_min * num)` | The three ways a subarray can end at `i`. | Start fresh, extend the biggest, or extend the smallest (which may flip sign). Built from the **old** `cur_max`/`cur_min`. |
| `cur_max = max(candidates)` | Largest product ending at `i`. | Needed for the answer and for the next step. |
| `cur_min = min(candidates)` | Smallest product ending at `i`. | A large negative may become a large positive at the next negative number. Because `candidates` was computed first, the new `cur_max` does not leak into this line. |
| `best = max(best, cur_max)` | Updates the overall record. | The best subarray can end at any index. |
| `return best` | Returns the answer. | — |

---

## 8. Dry Run

**Input:** `nums = [2, 3, -2, 4]` (Example 1)

| `i` | `num` | `cur_max × num` | `cur_min × num` | New `cur_max` | New `cur_min` | `best` |
|---|---|---|---|---|---|---|
| 0 | 2 | — | — | 2 | 2 | 2 |
| 1 | 3 | 2 × 3 = 6 | 2 × 3 = 6 | max(3, 6, 6) = 6 | min(3, 6, 6) = 3 | **6** |
| 2 | -2 | 6 × -2 = -12 | 3 × -2 = -6 | max(-2, -12, -6) = -2 | min(-2, -12, -6) = -12 | 6 |
| 3 | 4 | -2 × 4 = -8 | -12 × 4 = -48 | max(4, -8, -48) = 4 | min(4, -8, -48) = -48 | 6 |

**Result:** `6` ✅ (reached at `i = 1`, the subarray `[2, 3]`).

**Example 2:** `nums = [-2, 0, -1]`

| `i` | `num` | `cur_max × num` | `cur_min × num` | New `cur_max` | New `cur_min` | `best` |
|---|---|---|---|---|---|---|
| 0 | -2 | — | — | -2 | -2 | -2 |
| 1 | 0 | 0 | 0 | 0 | 0 | **0** |
| 2 | -1 | 0 | 0 | max(-1, 0, 0) = 0 | min(-1, 0, 0) = -1 | 0 |

**Result:** `0` ✅ — the zero blocked `-2` and `-1` from pairing up.

**Why `cur_min` matters:** `nums = [-2, 3, -4]` (expected 24, the whole array).

| `i` | `num` | `cur_max × num` | `cur_min × num` | New `cur_max` | New `cur_min` | `best` |
|---|---|---|---|---|---|---|
| 0 | -2 | — | — | -2 | -2 | -2 |
| 1 | 3 | -6 | -6 | 3 | -6 | 3 |
| 2 | -4 | -12 | **24** | 24 | -12 | **24** |

The `-6` kept in `cur_min` turned into `24`. If we only tracked the maximum we would answer 3.

---

## 9. Concepts, Data Structures, and Patterns

- **Kadane's algorithm, extended:** the same "best answer ending here" idea as [005_maximum_subarray.md](005_maximum_subarray.md), but multiplication needs two states because a sign flip swaps "best" and "worst".
- **Dynamic programming with constant space:** `max_end[i]` and `min_end[i]` depend only on index `i - 1`, so two variables replace two arrays.
- **Sign reasoning:** negative × negative = positive; anything × 0 = 0. Tracking the extremes on both sides covers every sign case.
- **Prefix/suffix scanning:** the alternative solution uses running products from both ends, a cousin of the prefix/suffix products in [004_product_of_array_except_self.md](004_product_of_array_except_self.md).
- **Related problems:** Maximum Subarray (sum version), Maximum Product of Three Numbers (LeetCode 628), Subarray Product Less Than K (LeetCode 713).

---

## 10. Complexity Analysis

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Brute force | `O(n²)` | `O(1)` | Every start/end pair, with a running product so each pair costs `O(1)`. |
| Max/min DP (optimized) | `O(n)` | `O(1)` | One pass; each step does a constant amount of work (three multiplications, a `max` and a `min` over three values). Only a few variables are stored (the `candidates` tuple always has 3 items). |
| Prefix/suffix scan | `O(n)` | `O(1)` | One loop doing two multiplications per index. |

Because the problem guarantees that every subarray product fits in 32 bits, and `cur_max`/`cur_min` are always products of real subarrays, the numbers stay small. (Python integers would not overflow anyway.)

---

## 11. Edge Cases

| Case | Example | Expected result | Why |
|---|---|---|---|
| Single negative element | `[-2]` | `-2` | The subarray must be non-empty. |
| Single zero | `[0]` | `0` | Only one subarray. |
| Zero separating two negatives | `[-2, 0, -1]` | `0` | `[-2, -1]` is not contiguous. |
| Even number of negatives | `[-2, 3, -4]` | `24` | Two negatives cancel; the whole array wins. |
| Odd negatives, best is a suffix | `[2, -5, -2, -4, 3]` | `24` | `[-2, -4, 3]` — dropping the prefix `2, -5` removes one negative. |
| Zero before positives | `[0, 2]` | `2` | The "start fresh" candidate restarts after the zero. |
| Two negatives | `[-1, -1]` | `1` | `(-1) × (-1) = 1`. |
| Several zero-separated stretches | `[-2, -3, 0, -4]` | `6` | Best is `[-2, -3]` in the first stretch. |

---

## 12. Common Mistakes and Debugging

1. **Tracking only the maximum.** Copying the sum version (`cur = max(num, cur * num)`) fails on `[-2, 3, -4]` (returns 3 instead of 24).
2. **Updating `cur_max` before computing `cur_min` from the old value.**
   ```text
   cur_max = max(num, cur_max * num, cur_min * num)
   cur_min = min(num, cur_max * num, cur_min * num)   # BUG: uses the NEW cur_max
   ```
   Compute both from the old values (a tuple of candidates, or a temporary variable, or `cur_max, cur_min = ..., ...` in one statement).
3. **Starting `best` at 0 or 1.** For `[-2]` you would return 0 or 1, which are not products of any subarray.
4. **Resetting to 1 at a zero and forgetting the zero itself.** In `[-2, 0, -1]`, the answer *is* 0, so the zero must be compared with `best`.
5. **Assuming "take everything with an even number of negatives" without handling zeros.** Zeros split the array into independent stretches.

**Debugging tip:** print `num, cur_max, cur_min, best` each iteration and compare with the dry-run tables above.

---

## 13. Practice Questions

**Q1. What does the max/min algorithm return for `[2, -5, -2, -4, 3]`? Trace `cur_max` and `cur_min`.**

<details><summary>Hint</summary>At each step the candidates are `num`, `cur_max × num`, `cur_min × num`.</summary></details>

**Answer:**

| `num` | candidates | `cur_max` | `cur_min` | `best` |
|---|---|---|---|---|
| 2 | — | 2 | 2 | 2 |
| -5 | -5, -10, -10 | -5 | -10 | 2 |
| -2 | -2, 10, 20 | 20 | -2 | 20 |
| -4 | -4, -80, 8 | 8 | -80 | 20 |
| 3 | 3, 24, -240 | 24 | -240 | **24** |

The answer is `24`, from `[-2, -4, 3]`.

**Q2. Why can't we simply skip all negative numbers?**

<details><summary>Hint</summary>Try `[-2, -3]`.</summary></details>

**Answer:** Two negatives multiply to a positive. In `[-2, -3]` the best product is `6`, which uses both negatives. Skipping them would also break contiguity for numbers on either side.

**Q3. Write `min_product_subarray(nums)` — the smallest product of any subarray.**

<details><summary>Hint</summary>The same two running values work; you just keep the record of the minimum instead of the maximum.</summary></details>

**Answer:**

```python
def min_product_subarray(nums):
    cur_max = cur_min = worst = nums[0]
    for num in nums[1:]:
        candidates = (num, cur_max * num, cur_min * num)
        cur_max, cur_min = max(candidates), min(candidates)
        worst = min(worst, cur_min)
    return worst


assert min_product_subarray([2, 3, -2, 4]) == -48     # whole array
assert min_product_subarray([-2, 0, -1]) == -2
assert min_product_subarray([1, 2, 3]) == 1
assert min_product_subarray([-1, -1]) == -1
```

**Q4. Return the maximum product together with the `(start, end)` indices of one subarray that achieves it.**

<details><summary>Hint</summary>Besides each running value, remember where its subarray starts. When a candidate "starts fresh", its start is `i`; otherwise it inherits the start of the run it extends.</summary></details>

**Answer:**

```python
import math


def max_product_with_indices(nums):
    cur_max = cur_min = best = nums[0]
    max_start = min_start = 0
    best_range = (0, 0)
    for i in range(1, len(nums)):
        num = nums[i]
        options = [(num, i), (cur_max * num, max_start), (cur_min * num, min_start)]
        cur_max, max_start = max(options)
        cur_min, min_start = min(options)
        if cur_max > best:
            best, best_range = cur_max, (max_start, i)
    return best, best_range


for arr in ([2, 3, -2, 4], [-2, 3, -4], [2, -5, -2, -4, 3], [-2, 0, -1], [-2]):
    value, (s, e) = max_product_with_indices(arr)
    assert math.prod(arr[s:e + 1]) == value
assert max_product_with_indices([2, 3, -2, 4])[0] == 6
assert max_product_with_indices([-2, 3, -4]) == (24, (0, 2))
```

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** Kadane-style DP with two states (max and min product ending here).
- **Key idea:** candidates = `num`, `cur_max × num`, `cur_min × num`; new max = largest, new min = smallest; `best = max(best, cur_max)`.
- **Time:** `O(n)`.
- **Auxiliary space:** `O(1)`.
- **One-line memory hook:** *"Keep your saddest score — one minus sign can make it the happiest."*

### Completion checklist

- [x] Problem requirements verified
- [x] Examples and constraints verified
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force solution written and tested
- [x] Optimized Python solution written and tested (`tools/tests/p006.py`), plus the prefix/suffix alternative
- [x] Line-by-line explanation written
- [x] Dry run completed with a real example
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
