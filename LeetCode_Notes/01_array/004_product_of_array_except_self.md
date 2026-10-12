# 004. Product of Array Except Self

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Product of Array Except Self |
| **LeetCode number** | 238 |
| **Topic (source list)** | Array |
| **Also uses** | Prefix Sum (prefix/suffix products) |
| **Difficulty** | Medium |
| **LeetCode URL** | <https://leetcode.com/problems/product-of-array-except-self/> |
| **Pattern** | Prefix and suffix products |

---

## 2. Problem Explanation

### What are we given?

`nums` — a list of integers.

### What must we return?

A new list `answer` of the same length where `answer[i]` is the **product of every element except `nums[i]`**.

### The rules

1. The solution must run in **`O(n)` time**.
2. You may **not use division**. (Dividing the total product by `nums[i]` is off-limits — and it would break when `nums[i]` is 0 anyway.)
3. The problem guarantees that the product of any prefix or suffix of `nums` fits in a 32-bit integer.

### Examples

**Example 1**

```text
Input:  nums = [1, 2, 3, 4]
Output: [24, 12, 8, 6]
```

- `answer[0] = 2 × 3 × 4 = 24`
- `answer[1] = 1 × 3 × 4 = 12`
- `answer[2] = 1 × 2 × 4 = 8`
- `answer[3] = 1 × 2 × 3 = 6`

**Example 2**

```text
Input:  nums = [-1, 1, 0, -3, 3]
Output: [0, 0, 9, 0, 0]
```

Every product except the one that skips the `0` (index 2) contains the 0, so it is 0. `answer[2] = (-1) × 1 × (-3) × 3 = 9`.

### Constraints

- `2 <= nums.length <= 10^5`
- `-30 <= nums[i] <= 30`
- Every `answer[i]` is guaranteed to fit in a 32-bit integer (the statement also guarantees that every prefix and suffix product fits).

**Follow-up:** Can you solve it with `O(1)` extra space? (The output list does **not** count as extra space.)

---

## 3. Everyday Analogy

> **Explain it like I'm five**

Kids are standing in a line, each holding a number card. For each kid, we want to know: *"What do you get if you multiply everyone's card **except yours**?"*

Here's a trick. Every kid's answer is made of two parts:

1. **Everything to their left** (multiplied together), and
2. **Everything to their right** (multiplied together).

So we walk down the line from left to right carrying a "left basket" — a running product. We tell each kid what's in the basket *before* adding their own card. Then we walk back from right to left with a "right basket" and do the same thing. Each kid multiplies the two basket values they heard, and that's their answer — and nobody ever had to divide!

---

## 4. Step-by-Step Logic

1. **Split the product.** For position `i`:
   `answer[i] = (product of nums[0..i-1]) × (product of nums[i+1..n-1])`
   = **prefix product before `i`** × **suffix product after `i`**.
2. **Prefix products** can be built left to right: `prefix_before[i] = prefix_before[i-1] × nums[i-1]`, starting with `prefix_before[0] = 1` (nothing to the left).
3. **Suffix products** can be built right to left: `suffix_after[i] = suffix_after[i+1] × nums[i+1]`, with `suffix_after[n-1] = 1`.
4. **Multiply them** to get each answer.
5. **Save space:** store the prefix products directly in `answer`, then sweep from the right with a single variable `suffix`, multiplying it into `answer[i]` as we go. No extra arrays needed.
6. **Zeros need no special handling** because we never divide.

---

## 5. Brute-Force Solution

### Algorithm

For each position `i`, multiply all elements at positions `j != i`.

### Python code

```python
from typing import List


class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        n = len(nums)
        answer = []
        for i in range(n):
            product = 1
            for j in range(n):
                if j != i:
                    product *= nums[j]
            answer.append(product)
        return answer
```

### Explanation

- The outer loop chooses which element to skip.
- The inner loop multiplies all the other elements.
- No division is used, so zeros are handled naturally.

### Complexity

- **Time:** `O(n²)` — for `n = 10^5` this is 10 billion multiplications, which **times out** and violates the `O(n)` requirement.
- **Auxiliary space:** `O(1)` besides the output list.

---

## 6. Optimized Solution

### Idea

Two passes:

1. **Left pass:** `answer[i]` = product of everything to the left of `i`.
2. **Right pass:** multiply `answer[i]` by the product of everything to the right of `i`, using a running variable.

### Algorithm

1. Create `answer = [1] * n`.
2. `prefix = 1`. For `i` from `0` to `n-1`: set `answer[i] = prefix`, then `prefix *= nums[i]`.
3. `suffix = 1`. For `i` from `n-1` down to `0`: set `answer[i] *= suffix`, then `suffix *= nums[i]`.
4. Return `answer`.

### Python code (LeetCode-ready)

```python
from typing import List


class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        n = len(nums)
        answer = [1] * n

        # Left pass: answer[i] = product of nums[0..i-1]
        prefix = 1
        for i in range(n):
            answer[i] = prefix
            prefix *= nums[i]

        # Right pass: multiply in the product of nums[i+1..n-1]
        suffix = 1
        for i in range(n - 1, -1, -1):
            answer[i] *= suffix
            suffix *= nums[i]

        return answer
```

---

## 7. Line-by-Line Explanation

| Line | What it does | Why |
|---|---|---|
| `n = len(nums)` | Stores the length. | Used by both loops. |
| `answer = [1] * n` | Creates the output list filled with 1s. | 1 is the neutral value for multiplication. |
| `prefix = 1` | Product of the elements to the left of the current index. | Before index 0 there is nothing, and an empty product is 1. |
| `for i in range(n):` | Left-to-right sweep. | Builds prefix products in order. |
| `answer[i] = prefix` | Saves "product of everything before `i`". | We store it **before** including `nums[i]`, so `nums[i]` is excluded. |
| `prefix *= nums[i]` | Includes `nums[i]` in the running product. | Prepares the value for index `i + 1`. |
| `suffix = 1` | Product of the elements to the right of the current index. | After the last index there is nothing → 1. |
| `for i in range(n - 1, -1, -1):` | Right-to-left sweep from `n-1` down to `0`. | Builds suffix products in order. |
| `answer[i] *= suffix` | Multiplies the left product by the right product. | Now `answer[i]` = left × right = everything except `nums[i]`. |
| `suffix *= nums[i]` | Includes `nums[i]` in the right product. | Prepares the value for index `i - 1`. |
| `return answer` | Returns the finished list. | Each entry is complete. |

---

## 8. Dry Run

**Input:** `nums = [1, 2, 3, 4]`

### Left pass

| `i` | `nums[i]` | `prefix` before | `answer[i] = prefix` | `prefix` after (`× nums[i]`) | `answer` |
|---|---|---|---|---|---|
| 0 | 1 | 1 | 1 | 1 | `[1, 1, 1, 1]` |
| 1 | 2 | 1 | 1 | 2 | `[1, 1, 1, 1]` |
| 2 | 3 | 2 | 2 | 6 | `[1, 1, 2, 1]` |
| 3 | 4 | 6 | 6 | 24 | `[1, 1, 2, 6]` |

After the left pass, `answer = [1, 1, 2, 6]` — the product of everything to the **left** of each position.

### Right pass

| `i` | `nums[i]` | `suffix` before | `answer[i] × suffix` | `suffix` after | `answer` |
|---|---|---|---|---|---|
| 3 | 4 | 1 | 6 × 1 = 6 | 4 | `[1, 1, 2, 6]` |
| 2 | 3 | 4 | 2 × 4 = 8 | 12 | `[1, 1, 8, 6]` |
| 1 | 2 | 12 | 1 × 12 = 12 | 24 | `[1, 12, 8, 6]` |
| 0 | 1 | 24 | 1 × 24 = 24 | 24 | `[24, 12, 8, 6]` |

**Result:** `[24, 12, 8, 6]` ✅

**With a zero:** for `nums = [-1, 1, 0, -3, 3]`, the left pass gives `[1, -1, -1, 0, 0]`, the right-side products are `[0, 0, -9, 3, 1]`, and multiplying gives `[0, 0, 9, 0, 0]` ✅.

---

## 9. Concepts, Data Structures, and Patterns

- **Prefix products / suffix products:** the multiplication version of prefix sums. Precompute "everything before" and "everything after" each position.
- **Two-pass array technique:** a left-to-right pass and a right-to-left pass, each `O(n)`.
- **Reusing the output array:** storing intermediate results in `answer` meets the `O(1)` extra-space follow-up.
- **Why no division?** Division fails with zeros (`0 / 0` is undefined) and the problem explicitly forbids it.
- **Identity element:** 1 for multiplication (like 0 for addition) — used to initialize empty products.
- **Related problems:** Maximum Product Subarray ([006_maximum_product_subarray.md](006_maximum_product_subarray.md)), Trapping Rain Water (prefix max / suffix max), Range Sum Query (prefix sums).

---

## 10. Complexity Analysis

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Brute force | `O(n²)` | `O(1)` | For each index, multiply `n - 1` numbers. |
| Prefix + suffix arrays | `O(n)` | `O(n)` | Two extra lists of length `n`. |
| Optimized (output reuse) | `O(n)` | `O(1)` | Two passes; only `prefix` and `suffix` variables besides the required output. |

---

## 11. Edge Cases

| Case | Example | Expected result | Why |
|---|---|---|---|
| Minimum length | `[2, 3]` | `[3, 2]` | Each answer is the other element. |
| One zero | `[0, 4, 5]` | `[20, 0, 0]` | Only the position of the zero has a non-zero product. |
| Two or more zeros | `[0, 0]` | `[0, 0]` | Every product includes at least one zero. |
| Negative numbers | `[-1, 1, 0, -3, 3]` | `[0, 0, 9, 0, 0]` | Signs are handled by ordinary multiplication. |
| All ones | `[1, 1, 1]` | `[1, 1, 1]` | Neutral values. |

---

## 12. Common Mistakes and Debugging

1. **Using division.** `total // nums[i]` is forbidden and crashes when `nums[i] == 0`.
2. **Including `nums[i]` in its own product.** In the left pass, assign `answer[i] = prefix` **before** `prefix *= nums[i]`. Swapping the two lines includes the element itself.
3. **Wrong reverse range.** `range(n - 1, -1, -1)` goes from `n - 1` down to `0`. Writing `range(n - 1, 0, -1)` skips index 0.
4. **Initializing with 0 instead of 1.** Any product starting at 0 stays 0.
5. **Overwriting `answer[i]` in the right pass** (`answer[i] = suffix`) instead of multiplying (`answer[i] *= suffix`) throws away the left product.

**Debugging tip:** print `answer` after the left pass. It should equal the products of the elements to the left (e.g. `[1, 1, 2, 6]` for `[1, 2, 3, 4]`).

---

## 13. Practice Questions

**Q1. What does `answer` look like after the left pass for `nums = [2, 3, 4, 5]`? What's the final answer?**

<details><summary>Hint</summary>The left pass stores the running product **before** each element.</summary></details>

**Answer:** After the left pass: `[1, 2, 6, 24]`. Suffix products after each index: `[60, 20, 5, 1]`. Final: `[60, 40, 30, 24]`.

**Q2. Write the version with two explicit arrays `left` and `right` (easier to understand, `O(n)` extra space).**

<details><summary>Hint</summary>`left[i]` = product before `i`; `right[i]` = product after `i`.</summary></details>

**Answer:**

```python
def product_except_self_two_arrays(nums):
    n = len(nums)
    left = [1] * n
    right = [1] * n
    for i in range(1, n):
        left[i] = left[i - 1] * nums[i - 1]
    for i in range(n - 2, -1, -1):
        right[i] = right[i + 1] * nums[i + 1]
    return [left[i] * right[i] for i in range(n)]


assert product_except_self_two_arrays([1, 2, 3, 4]) == [24, 12, 8, 6]
assert product_except_self_two_arrays([-1, 1, 0, -3, 3]) == [0, 0, 9, 0, 0]
```

**Q3. If division *were* allowed, how would you handle zeros correctly?**

<details><summary>Hint</summary>Count the zeros and compute the product of the non-zero elements.</summary></details>

**Answer:** Let `zeros` be the number of zeros and `p` the product of all non-zero elements.
- `zeros >= 2`: every answer is 0.
- `zeros == 1`: the zero's position gets `p`; all others get 0.
- `zeros == 0`: `answer[i] = p // nums[i]` (exact, since `nums[i]` divides `p`).

```python
def product_with_division(nums):
    zeros = nums.count(0)
    p = 1
    for x in nums:
        if x != 0:
            p *= x
    if zeros >= 2:
        return [0] * len(nums)
    if zeros == 1:
        return [p if x == 0 else 0 for x in nums]
    return [p // x for x in nums]


assert product_with_division([1, 2, 3, 4]) == [24, 12, 8, 6]
assert product_with_division([-1, 1, 0, -3, 3]) == [0, 0, 9, 0, 0]
assert product_with_division([0, 0, 2]) == [0, 0, 0]
```

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** Prefix and suffix products.
- **Key idea:** `answer[i]` = (product left of `i`) × (product right of `i`). Fill lefts in `answer`, then multiply in rights with a running `suffix`.
- **Time:** `O(n)`.
- **Auxiliary space:** `O(1)` (output not counted).
- **One-line memory hook:** *"Left basket on the way out, right basket on the way back."*

### Completion checklist

- [x] Problem requirements verified
- [x] Examples and constraints verified
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force solution written and tested
- [x] Optimized Python solution written and tested (`tools/tests/p004.py`)
- [x] Line-by-line explanation written
- [x] Dry run completed with a real example
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
