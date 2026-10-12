# 014. Missing Number

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Missing Number |
| **LeetCode number** | 268 |
| **Topic (source list)** | Binary |
| **Also uses** | Array, Math, Hash Table, Bit Manipulation |
| **Difficulty** | Easy |
| **LeetCode URL** | <https://leetcode.com/problems/missing-number/> |
| **Pattern** | XOR cancellation (`x ^ x = 0`); alternative: Gauss sum formula |

---

## 2. Problem Explanation

### What are we given?

`nums` — a list of `n` **different** integers. Every value is between `0` and `n` (inclusive).

### What must we return?

The range `0, 1, 2, …, n` contains `n + 1` numbers, but the list only has `n` of them. Exactly one number from the range is absent — return it.

### The rules

1. `n` is the **length of the list**, not the largest value in it.
2. All values are distinct, so exactly one number of the range is missing.
3. The list is **not sorted**.
4. The missing number can be anything from `0` to `n`, including `0` itself or `n` itself.

### Examples

**Example 1**

```text
Input:  nums = [3, 0, 1]
Output: 2
```

The list has 3 elements, so the full range is `0..3` = `{0, 1, 2, 3}`. The list contains 0, 1 and 3 — only 2 is absent.

**Example 2**

```text
Input:  nums = [0, 1]
Output: 2
```

Length 2 → range `0..2`. Both 0 and 1 are present, so the missing number is the top of the range, 2.

**Example 3**

```text
Input:  nums = [9, 6, 4, 2, 3, 5, 7, 0, 1]
Output: 8
```

Length 9 → range `0..9`. Every value from 0 to 9 appears except 8.

### Constraints

- `n == nums.length`
- `1 <= n <= 10^4`
- `0 <= nums[i] <= n`
- All the numbers of `nums` are unique.

**Follow-up:** Can you solve it using only `O(1)` extra space and `O(n)` time?

---

## 3. Everyday Analogy

> **Explain it like I'm five**

Imagine you have socks numbered 0 to 3, and each number should come as a **pair**: one sock in the "should have" box and one in the "actually have" box.

- The "should have" box gets one sock for every number: 0, 1, 2, 3.
- The "actually have" box gets one sock for every number in the list: 3, 0, 1.

Now dump both boxes on the floor and throw away every **matching pair**. The 0s pair up, the 1s pair up, the 3s pair up… and one lonely sock is left: **2**. That's the missing number!

XOR (`^`) is exactly this "throw away matching pairs" machine: `x ^ x = 0`, so every number that appears twice disappears, and only the unpaired one survives.

---

## 4. Step-by-Step Logic

1. **What do we know?** The full range `0..n` and the list differ by exactly one number.
2. **Simple idea:** for each candidate `0..n`, check whether it is in the list. Correct, but checking `in` on a list is a full scan → `O(n²)`.
3. **Faster idea with memory:** put the list into a set (`O(1)` lookups) → `O(n)` time but `O(n)` extra space. The follow-up wants `O(1)` space.
4. **Use arithmetic instead of memory.** If we combine all numbers `0..n` and "un-combine" all list numbers, the only thing left is the missing number. Two operations can undo themselves:
   - **Sum:** `(0 + 1 + … + n) - sum(nums)` = missing. The full sum is `n(n+1)/2` (Gauss).
   - **XOR:** `(0 ^ 1 ^ … ^ n) ^ (nums[0] ^ … ^ nums[n-1])` = missing, because XOR is order-independent and `x ^ x = 0`.
5. **One loop does it all.** Start with `missing = n` (the one index that never appears in `range(n)`). For each position `i`, XOR in both `i` and `nums[i]`. Every number that appears both as an index/`n` and as a value cancels out.
6. **Why XOR is the "Binary" answer:** it never grows beyond the size of the numbers (no overflow worries in languages with fixed-size integers) and uses only bit operations.

---

## 5. Brute-Force Solution

### Algorithm

1. For each candidate `x` from `0` to `n`:
2. If `x` is not in `nums`, return `x`.

### Python code

```python
from typing import List


class Solution:
    def missingNumber(self, nums: List[int]) -> int:
        n = len(nums)
        for candidate in range(n + 1):
            if candidate not in nums:   # linear scan of the list each time
                return candidate
        return -1  # unreachable: exactly one number is always missing
```

### Explanation

- We simply test every number of the range in order and return the first one that the list does not contain.
- `candidate not in nums` scans the list from the start every time, which is what makes this slow.

### Complexity

- **Time:** `O(n²)`. In the worst case (missing number near the end) we do `n + 1` scans; a present candidate is found on average halfway through the list, so the total is about `n²/2` — roughly 5 × 10^7 element comparisons for `n = 10^4`. Python's `in` on a list is implemented in C, so this may scrape through on LeetCode, but it is far slower than necessary and does not meet the follow-up.
- **Auxiliary space:** `O(1)`.

---

## 6. Optimized Solution

### Idea — XOR everything

XOR together every index `0..n-1`, the number `n`, and every value in `nums`. Each present number shows up twice (once as an index/`n`, once as a value) and cancels; the missing number shows up only once and remains.

### Algorithm

1. `missing = n` (covers the number `n`, which is not an index).
2. For each index `i` with value `num`: `missing ^= i ^ num`.
3. Return `missing`.

### Python code (LeetCode-ready)

```python
from typing import List


class Solution:
    def missingNumber(self, nums: List[int]) -> int:
        missing = len(nums)              # include n itself
        for i, num in enumerate(nums):
            missing ^= i ^ num           # pairs cancel out: x ^ x == 0
        return missing
```

### Alternative — Gauss sum formula

```python
from typing import List


class Solution:
    def missingNumber(self, nums: List[int]) -> int:
        n = len(nums)
        expected = n * (n + 1) // 2      # 0 + 1 + ... + n
        return expected - sum(nums)
```

Also `O(n)` time and `O(1)` space. In Python, integers never overflow, so this is completely safe. In languages with 32-bit integers, the sum could overflow for large `n` (not with these constraints, but it is a common interview talking point), which is one reason the XOR version is popular.

---

## 7. Line-by-Line Explanation

(XOR version)

| Line | What it does | Why |
|---|---|---|
| `missing = len(nums)` | Starts the running XOR with `n`. | Indices only go up to `n - 1`, so `n` must be added separately to cover the full range `0..n`. |
| `for i, num in enumerate(nums):` | Loops over indices `0..n-1` and values together. | The indices give us `0..n-1` for free — no second loop needed. |
| `missing ^= i ^ num` | XORs in one number from the range (`i`) and one number from the list (`num`). | XOR is commutative and associative, so the order does not matter; equal numbers cancel wherever they appear. |
| `return missing` | Returns the survivor. | Everything else appeared exactly twice and became 0; `0 ^ x == x`. |

**Why it works, written out:** the final value is
`n ^ 0 ^ 1 ^ … ^ (n-1) ^ nums[0] ^ … ^ nums[n-1]`.
The first part contains every number of `0..n` once. The second part contains every number of `0..n` once **except the missing one**. Every present number therefore appears twice and cancels, leaving only the missing number.

---

## 8. Dry Run

**Input (Example 1):** `nums = [3, 0, 1]`, so `n = 3`.

| Step | `i` | `num` | `i ^ num` | `missing` before | `missing` after |
|---|---|---|---|---|---|
| start | — | — | — | — | 3 (`11`) |
| 1 | 0 | 3 | `00 ^ 11 = 11` (3) | 3 (`11`) | `11 ^ 11 = 00` (0) |
| 2 | 1 | 0 | `01 ^ 00 = 01` (1) | 0 (`00`) | `00 ^ 01 = 01` (1) |
| 3 | 2 | 1 | `10 ^ 01 = 11` (3) | 1 (`01`) | `01 ^ 11 = 10` (2) |

**Result:** `2` ✅

Seen as pairs: we combined `{3, 0, 1, 2}` (the start value and indices) with `{3, 0, 1}` (the values). 3, 0 and 1 each appear twice and cancel; 2 is alone.

### Second dry run — Example 2

`nums = [0, 1]`, `n = 2`: `missing = 2`; `i = 0`: `2 ^ (0 ^ 0) = 2`; `i = 1`: `2 ^ (1 ^ 1) = 2`. **Result:** `2` ✅ — the missing number is `n` itself, which is why we start with `missing = n`.

**Gauss check for Example 3:** `n = 9`, expected sum `9 × 10 / 2 = 45`, actual sum `9+6+4+2+3+5+7+0+1 = 37`, difference `8` ✅.

---

## 9. Concepts, Data Structures, and Patterns

- **Bit primer:** see the [mini primer in note 011](011_sum_of_two_integers.md#9-concepts-data-structures-and-patterns).
- **XOR properties used here:**
  - `x ^ x = 0` (a number cancels itself),
  - `x ^ 0 = x` (zero changes nothing),
  - commutative and associative (`a ^ b ^ c` can be regrouped and reordered freely).
  Together these mean: XOR a collection of numbers, and anything that appears an even number of times vanishes.
- **Using indices as data:** the positions `0..n-1` *are* most of the range we need, so one loop covers both sides.
- **Gauss's formula:** `0 + 1 + … + n = n(n+1)/2`.
- **Hash set approach:** `set(nums)` then find the absent value — `O(n)` time but `O(n)` space; the same "membership check" tool used in [Contains Duplicate](../01_array/003_contains_duplicate.md).
- **Related patterns:** "Single Number" (every number appears twice except one → XOR everything), "Find the Duplicate Number", and "First Missing Positive" (harder; uses the array itself as a hash table).

---

## 10. Complexity Analysis

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Check each candidate with `in` (brute force) | `O(n²)` | `O(1)` | Up to `n + 1` linear scans of the list. |
| Sort then scan | `O(n log n)` | `O(n)` | `sorted(nums)` makes a copy; the first index where `sorted_nums[i] != i` is the answer (or `n` if none). |
| Hash set | `O(n)` average | `O(n)` | Build a set, check `0..n`. |
| XOR (optimized) | `O(n)` | `O(1)` | One pass, one integer variable. |
| Gauss sum | `O(n)` | `O(1)` | One pass to sum the list. |

---

## 11. Edge Cases

| Case | Example | Expected result | Why |
|---|---|---|---|
| Smallest list, 0 missing | `[1]` | `0` | `missing = 1 ^ (0 ^ 1) = 0`. |
| Smallest list, `n` missing | `[0]` | `1` | `missing = 1 ^ (0 ^ 0) = 1`. |
| Missing number is `n` | `[0, 1]` | `2` | Covered by starting with `missing = n`. |
| Missing number is 0 | `[3, 1, 2]` | `0` | Works the same; 0 just never appears as a value. |
| Unsorted input | `[9, 6, 4, 2, 3, 5, 7, 0, 1]` | `8` | Order does not matter for XOR or sums. |
| Largest input | `n = 10^4` | the one absent value | Still one linear pass. |

---

## 12. Common Mistakes and Debugging

1. **Forgetting `n` itself.** Looping XOR only over indices `0..n-1` and values misses the number `n`; for `[0, 1]` you would return 0 instead of 2. Start with `missing = len(nums)`.
2. **Assuming the list is sorted.** `nums[i] != i` checks only work after sorting.
3. **Using the maximum value as `n`.** `n` is `len(nums)`. In `[0, 1]` the maximum is 1 but `n` is 2.
4. **Integer division.** Write `n * (n + 1) // 2`; `/` gives a float like `6.0`, and `6.0 - 4` returns `2.0` instead of `2`.
5. **Brute force with `nums.index`.** Calling `nums.index(x)` raises `ValueError` for the missing number; use `in` or a set.

**Debugging tip:** print `missing` in binary after each step (`f"{missing:b}"`). When you finish, check that `missing` is not in `nums` and lies in `0..n`.

---

## 13. Practice Questions

**Q1. Run the XOR solution on `nums = [1, 2]` and show each value of `missing`.**

<details><summary>Hint</summary>`n = 2`. Start at 2, then XOR in `0 ^ 1`, then `1 ^ 2`.</summary></details>

**Answer:** `missing = 2`; step `i = 0, num = 1`: `2 ^ 0 ^ 1 = 3`; step `i = 1, num = 2`: `3 ^ 1 ^ 2 = 0`. The answer is `0`, which is indeed the number absent from `{0, 1, 2}`.

**Q2. Single Number: every element appears twice except one. Find it in `O(n)` time and `O(1)` space.**

<details><summary>Hint</summary>Same cancellation idea, but there is no range to XOR in — just the list.</summary></details>

**Answer:** XOR all values; pairs cancel and the single one remains.

```python
def single_number(nums):
    result = 0
    for num in nums:
        result ^= num
    return result


assert single_number([2, 2, 1]) == 1
assert single_number([4, 1, 2, 1, 2]) == 4
assert single_number([7]) == 7
```

**Q3. Write the hash-set version of Missing Number. What does it cost?**

<details><summary>Hint</summary>Put the list in a set and test `0..n`.</summary></details>

**Answer:** `O(n)` average time, `O(n)` extra space.

```python
def missing_number_set(nums):
    seen = set(nums)
    for x in range(len(nums) + 1):
        if x not in seen:
            return x
    return -1  # unreachable for valid input


assert missing_number_set([3, 0, 1]) == 2
assert missing_number_set([0, 1]) == 2
assert missing_number_set([9, 6, 4, 2, 3, 5, 7, 0, 1]) == 8
```

**Q4. Two numbers are missing from `0..n` (the list has `n - 1` distinct values). How could XOR help find both?**

<details><summary>Hint</summary>XOR everything to get `a ^ b`. Any set bit of `a ^ b` is a bit where `a` and `b` differ — use it to split all numbers into two groups.</summary></details>

**Answer:** XOR the range and the list to get `x = a ^ b`. Pick its lowest set bit `low = x & -x`. Split the range numbers and the list numbers into "has this bit" and "doesn't"; XOR each group separately. Each group contains exactly one of the missing numbers, and everything else cancels.

```python
def two_missing(nums):
    n = len(nums) + 1          # range is 0..n
    x = 0
    for v in range(n + 1):
        x ^= v
    for v in nums:
        x ^= v                 # x == a ^ b
    low = x & -x               # a bit where a and b differ
    a = 0
    for v in range(n + 1):
        if v & low:
            a ^= v
    for v in nums:
        if v & low:
            a ^= v
    return sorted([a, a ^ x])


assert two_missing([0, 2, 4]) == [1, 3]
assert two_missing([1, 2]) == [0, 3]
assert two_missing([0]) == [1, 2]
```

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** XOR cancellation (pairs vanish, the odd one out survives).
- **Key idea:** `missing = n`, then `missing ^= i ^ nums[i]` for every index. Alternative: `n(n+1)//2 - sum(nums)`.
- **Brute force:** test each candidate with `in`, `O(n²)`.
- **Time:** `O(n)`. **Auxiliary space:** `O(1)` — meets the follow-up.
- **One-line memory hook:** *"Pair up every sock; the lonely one is missing."*

### Completion checklist

- [x] Problem requirements verified
- [x] Examples and constraints verified
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force solution written and tested
- [x] Optimized Python solution written and tested (`tools/tests/p014.py`)
- [x] Alternative Gauss-sum solution written and tested
- [x] Line-by-line explanation written
- [x] Dry run completed with a real example
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
