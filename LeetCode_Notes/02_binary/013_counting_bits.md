# 013. Counting Bits

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Counting Bits |
| **LeetCode number** | 338 |
| **Topic (source list)** | Binary |
| **Also uses** | Dynamic Programming, Bit Manipulation |
| **Difficulty** | Easy |
| **LeetCode URL** | <https://leetcode.com/problems/counting-bits/> |
| **Pattern** | DP over numbers: reuse the answer for `i >> 1` (or `i & (i - 1)`) |

---

## 2. Problem Explanation

### What are we given?

One integer `n` (zero or larger).

### What must we return?

A list `ans` with `n + 1` entries — one for every number from `0` up to and including `n`. Entry `ans[i]` is how many `1`s appear in the binary form of `i`.

### The rules

1. The list must have length `n + 1` (positions `0, 1, …, n`).
2. You should **not** rely on a built-in "count the bits" function (the statement names C++'s `__builtin_popcount`; the Python equivalents are `int.bit_count()` and `bin(i).count("1")`). The goal is to compute the counts yourself.

### Examples

**Example 1**

```text
Input:  n = 2
Output: [0, 1, 1]
```

| `i` | binary | number of 1s |
|---|---|---|
| 0 | `0` | 0 |
| 1 | `1` | 1 |
| 2 | `10` | 1 |

**Example 2**

```text
Input:  n = 5
Output: [0, 1, 1, 2, 1, 2]
```

| `i` | binary | number of 1s |
|---|---|---|
| 0 | `0` | 0 |
| 1 | `1` | 1 |
| 2 | `10` | 1 |
| 3 | `11` | 2 |
| 4 | `100` | 1 |
| 5 | `101` | 2 |

### Constraints

- `0 <= n <= 10^5`

**Follow-up:** An `O(n log n)` solution is easy to find. Can you do it in linear time `O(n)`, ideally in a single pass?

---

## 3. Everyday Analogy

> **Explain it like I'm five**

Imagine a staircase of numbers, and on each step you must write how many 1s its binary form has.

You could stop at every step and count from scratch. But there's a shortcut: **every number is its "half" with one extra digit stuck on the right end.**

- 5 is `101`. Chop off the last digit and you get `10`, which is 2 — and you already wrote down the answer for 2 on an earlier step!
- So the count for 5 is "the count for 2" plus "is the chopped digit a 1?" → `1 + 1 = 2`.

Because the half of any number is always a *smaller* number, its answer is already on a lower step. You just look down, read it, and add 0 or 1. No counting from scratch ever again.

---

## 4. Step-by-Step Logic

1. **Easy approach:** for each `i`, count its bits one by one. A number up to `n` has about `log2(n)` bits, so this costs `O(n log n)`.
2. **Find a relationship between numbers.** Shifting right by one (`i >> 1`) removes the last binary digit. The removed digit is `i & 1`.
3. **So:** `bits(i) = bits(i >> 1) + (i & 1)`.
   - Example: `6 = 110`. `6 >> 1 = 3 = 11` has 2 ones; the removed digit `6 & 1 = 0`. So `bits(6) = 2 + 0 = 2`. ✅
4. **The half is always smaller** (`i >> 1 < i` for `i >= 1`), so if we fill the list from left to right, `ans[i >> 1]` is already known when we need it. This is **dynamic programming**: build each answer from smaller answers.
5. **Base case:** `ans[0] = 0` (zero has no 1 bits).
6. **One pass:** loop `i` from 1 to `n`, fill `ans[i]`. Each entry takes constant work, so the total is `O(n)`.

---

## 5. Brute-Force Solution

### Algorithm

1. For every `i` from 0 to `n`:
   - Copy `i` into `x` and set `count = 0`.
   - While `x > 0`: add `x & 1` to `count`, then shift `x` right by one.
   - Append `count` to the answer.
2. Return the answer.

### Python code

```python
from typing import List


class Solution:
    def countBits(self, n: int) -> List[int]:
        ans = []
        for i in range(n + 1):
            x = i
            count = 0
            while x:
                count += x & 1   # add the lowest bit
                x >>= 1          # drop the lowest bit
            ans.append(count)
        return ans
```

### Explanation

- The inner loop is the "count the bits of one number" routine from [012_number_of_1_bits.md](012_number_of_1_bits.md), written without any built-in popcount.
- It runs once per binary digit of `i`, i.e. about `log2(i) + 1` times.

### Complexity

- **Time:** `O(n log n)`. For `n = 10^5`, each number has at most 17 bits, so about 1.7 million inner iterations — this is actually **accepted** on LeetCode, but it does not meet the `O(n)` follow-up.
- **Auxiliary space:** `O(1)` besides the output list.

---

## 6. Optimized Solution

### Idea — DP with the right shift

`ans[i] = ans[i >> 1] + (i & 1)`: the count for `i` equals the count for `i` without its last digit, plus that last digit.

### Algorithm

1. Create `ans = [0] * (n + 1)`. (`ans[0] = 0` is already correct.)
2. For `i` from 1 to `n`: `ans[i] = ans[i >> 1] + (i & 1)`.
3. Return `ans`.

### Python code (LeetCode-ready)

```python
from typing import List


class Solution:
    def countBits(self, n: int) -> List[int]:
        ans = [0] * (n + 1)
        for i in range(1, n + 1):
            ans[i] = ans[i >> 1] + (i & 1)   # half's count + last bit
        return ans
```

### Alternative one-pass DP — drop the lowest set bit

From [Number of 1 Bits](012_number_of_1_bits.md) we know `i & (i - 1)` is `i` with its lowest set bit removed. It is smaller than `i` and has exactly one fewer `1`:

```python
from typing import List


class Solution:
    def countBits(self, n: int) -> List[int]:
        ans = [0] * (n + 1)
        for i in range(1, n + 1):
            ans[i] = ans[i & (i - 1)] + 1    # one fewer set bit, plus that bit
        return ans
```

Both versions are single-pass `O(n)` solutions.

---

## 7. Line-by-Line Explanation

(Right-shift version)

| Line | What it does | Why |
|---|---|---|
| `ans = [0] * (n + 1)` | Makes a list of `n + 1` zeros. | One slot per number `0..n`. Slot 0 stays 0, which is the correct base case. |
| `for i in range(1, n + 1):` | Visits `1, 2, …, n` in increasing order. | `range` stops *before* its end value, so we need `n + 1` to include `n`. Increasing order guarantees smaller answers are filled first. |
| `i >> 1` | `i` with its last binary digit removed (same as `i // 2`). | This smaller number's count is already stored in `ans`. |
| `i & 1` | The removed last digit: 1 if `i` is odd, 0 if even. | Adds back the bit that the shift threw away. |
| `ans[i] = ans[i >> 1] + (i & 1)` | Stores the count for `i`. | Total ones = ones in the rest + the last bit. |
| `return ans` | Returns the finished list. | — |

---

## 8. Dry Run

**Input (Example 2):** `n = 5`. Start: `ans = [0, 0, 0, 0, 0, 0]`.

| `i` | binary | `i >> 1` (binary) | `ans[i >> 1]` | `i & 1` | `ans[i]` | `ans` after |
|---|---|---|---|---|---|---|
| 1 | `1` | 0 (`0`) | 0 | 1 | 1 | `[0, 1, 0, 0, 0, 0]` |
| 2 | `10` | 1 (`1`) | 1 | 0 | 1 | `[0, 1, 1, 0, 0, 0]` |
| 3 | `11` | 1 (`1`) | 1 | 1 | 2 | `[0, 1, 1, 2, 0, 0]` |
| 4 | `100` | 2 (`10`) | 1 | 0 | 1 | `[0, 1, 1, 2, 1, 0]` |
| 5 | `101` | 2 (`10`) | 1 | 1 | 2 | `[0, 1, 1, 2, 1, 2]` |

**Result:** `[0, 1, 1, 2, 1, 2]` ✅

### Second dry run — the `i & (i - 1)` version, same input

| `i` | binary | `i & (i - 1)` | `ans[i & (i - 1)] + 1` |
|---|---|---|---|
| 1 | `1` | `1 & 0 = 0` | 0 + 1 = 1 |
| 2 | `10` | `10 & 01 = 0` | 0 + 1 = 1 |
| 3 | `11` | `11 & 10 = 2` | 1 + 1 = 2 |
| 4 | `100` | `100 & 011 = 0` | 0 + 1 = 1 |
| 5 | `101` | `101 & 100 = 4` | 1 + 1 = 2 |

**Result:** `[0, 1, 1, 2, 1, 2]` ✅

**Example 1:** `n = 2` gives the first three entries of the table above: `[0, 1, 1]` ✅.

---

## 9. Concepts, Data Structures, and Patterns

- **Bit primer:** see the [mini primer in note 011](011_sum_of_two_integers.md#9-concepts-data-structures-and-patterns). Used here: `i >> 1` (remove last digit, same as `i // 2`), `i & 1` (last digit), `i & (i - 1)` (remove lowest set bit).
- **Dynamic programming (DP):** define `ans[i]` in terms of answers for smaller indices, fill a table in an order where those smaller answers are ready. Here the "recurrence" is `ans[i] = ans[i >> 1] + (i & 1)` and the base case is `ans[0] = 0`. More DP problems live in the `08_dynamic_programming` folder of this project.
- **Reusing earlier work:** the brute force recomputes each count from scratch; the DP reads one earlier result in `O(1)`.
- **Other valid recurrences:**
  - `ans[i] = ans[i & (i - 1)] + 1` (drop the lowest set bit).
  - `ans[i] = ans[i - offset] + 1`, where `offset` is the largest power of two `<= i` (drop the highest set bit).
- **Related notes:** single-number popcount ([012_number_of_1_bits.md](012_number_of_1_bits.md)); the 256-entry lookup table in note 012 is built with exactly this recurrence.

---

## 10. Complexity Analysis

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Count each number's bits (brute force) | `O(n log n)` | `O(1)` | `n + 1` numbers, each with up to `⌊log2 n⌋ + 1` bits. |
| DP with `i >> 1` (optimized) | `O(n)` | `O(1)` | One pass, constant work per index. |
| DP with `i & (i - 1)` | `O(n)` | `O(1)` | Same, different recurrence. |

The output list of size `n + 1` is required by the problem and is not counted as auxiliary space.

---

## 11. Edge Cases

| Case | Example | Expected result | Why |
|---|---|---|---|
| Smallest input | `n = 0` | `[0]` | The loop `range(1, 1)` is empty; only the base case remains. |
| One | `n = 1` | `[0, 1]` | `ans[1] = ans[0] + 1`. |
| Power of two at the end | `n = 8` | `[0, 1, 1, 2, 1, 2, 2, 3, 1]` | 7 = `111` has 3 ones, 8 = `1000` has 1. |
| Largest input | `n = 100000` | list of 100001 counts; `ans[100000] = 6` | 100000 = `11000011010100000` has 6 ones. Runs in linear time. |

---

## 12. Common Mistakes and Debugging

1. **Wrong list length.** The answer needs `n + 1` entries (`0` through `n`). `[0] * n` causes an `IndexError` at `ans[n]`.
2. **`range(1, n)` instead of `range(1, n + 1)`.** Leaves the last entry as 0.
3. **Operator precedence.** `ans[i >> 1] + i & 1` means `(ans[i >> 1] + i) & 1` because `+` binds tighter than `&` in Python. Always write `(i & 1)` in parentheses.
4. **Using built-ins.** `bin(i).count("1")` or `i.bit_count()` would pass the tests but ignores the rule in the statement.
5. **Filling in the wrong order.** If you loop from `n` down to 1, `ans[i >> 1]` has not been computed yet.

**Debugging tip:** print `i, bin(i), ans[i]` for `i` up to 16 and check against the pattern: every power of two has count 1, and `2^k - 1` has count `k`.

---

## 13. Practice Questions

**Q1. Using the recurrence, compute `ans[13]` given `ans[6] = 2`.**

<details><summary>Hint</summary>`13 >> 1 = 6`. Is 13 odd?</summary></details>

**Answer:** `13 = 1101`, `13 >> 1 = 6 = 110`, and `13 & 1 = 1`. So `ans[13] = ans[6] + 1 = 2 + 1 = 3`, which matches the three 1s in `1101`.

**Q2. Write the "drop the highest set bit" DP: `ans[i] = ans[i - offset] + 1`, where `offset` is the largest power of two not exceeding `i`.**

<details><summary>Hint</summary>Keep a variable `offset`; whenever `offset * 2 == i`, double it.</summary></details>

**Answer:** When `i` reaches the next power of two, update `offset`. Subtracting `offset` removes the leading `1`.

```python
def count_bits_msb(n):
    ans = [0] * (n + 1)
    offset = 1
    for i in range(1, n + 1):
        if offset * 2 == i:
            offset *= 2
        ans[i] = ans[i - offset] + 1
    return ans


assert count_bits_msb(5) == [0, 1, 1, 2, 1, 2]
assert count_bits_msb(0) == [0]
assert count_bits_msb(8) == [0, 1, 1, 2, 1, 2, 2, 3, 1]
```

**Q3. Using the DP table, return the total number of 1 bits written when listing all numbers from 0 to `n`.**

<details><summary>Hint</summary>Build the table, then sum it.</summary></details>

**Answer:** For `n = 5` the table is `[0, 1, 1, 2, 1, 2]`, whose sum is 7.

```python
def total_set_bits(n):
    ans = [0] * (n + 1)
    for i in range(1, n + 1):
        ans[i] = ans[i >> 1] + (i & 1)
    return sum(ans)


assert total_set_bits(5) == 7
assert total_set_bits(0) == 0
assert total_set_bits(7) == 12   # 0+1+1+2+1+2+2+3
```

**Q4. Why is `ans[i >> 1]` always computed before `ans[i]` in the loop?**

<details><summary>Hint</summary>Compare `i >> 1` with `i` for `i >= 1`.</summary></details>

**Answer:** For every `i >= 1`, `i >> 1` equals `i // 2`, which is strictly less than `i`. The loop visits indices in increasing order, so every smaller index — including `i >> 1` — has already been filled.

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** Dynamic programming over integers using bit relationships.
- **Key idea:** `ans[i] = ans[i >> 1] + (i & 1)` — the count for `i` is the count for its "half" plus its last bit. Alternative: `ans[i] = ans[i & (i - 1)] + 1`.
- **Brute force:** count each number's bits separately, `O(n log n)`.
- **Time:** `O(n)`, single pass. **Auxiliary space:** `O(1)` (output not counted).
- **One-line memory hook:** *"Chop off the last digit, look up the rest, add the digit back."*

### Completion checklist

- [x] Problem requirements verified
- [x] Examples and constraints verified
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force solution written and tested
- [x] Optimized Python solution written and tested (`tools/tests/p013.py`)
- [x] Alternative `i & (i - 1)` solution written and tested
- [x] Line-by-line explanation written
- [x] Dry run completed with a real example
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
