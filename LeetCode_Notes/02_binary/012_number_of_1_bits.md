# 012. Number of 1 Bits

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Number of 1 Bits |
| **LeetCode number** | 191 |
| **Topic (source list)** | Binary |
| **Also uses** | Bit Manipulation, Divide and Conquer (lookup-table follow-up) |
| **Difficulty** | Easy |
| **LeetCode URL** | <https://leetcode.com/problems/number-of-1-bits/> |
| **Pattern** | Clear the lowest set bit with `n & (n - 1)` (Brian Kernighan's trick) |

---

## 2. Problem Explanation

### What are we given?

`n` — a **positive** integer. In Python, LeetCode passes it as an ordinary `int` (not a string of 0s and 1s).

### What must we return?

How many `1`s appear when `n` is written in binary. This count is also called the **Hamming weight** or **population count** ("popcount"). A bit that is `1` is called a **set bit**.

### The rules

1. `n` is always at least 1 and at most `2^31 - 1`, so it fits in 31 bits and is never negative or zero.
2. Only the count matters — not where the 1s are.

### Examples

**Example 1**

```text
Input:  n = 11
Output: 3
```

11 is `1011` in binary (8 + 2 + 1). Three of the positions hold a 1.

**Example 2**

```text
Input:  n = 128
Output: 1
```

128 is `10000000` in binary — it is a power of two, so exactly one bit is set.

**Example 3**

```text
Input:  n = 2147483645
Output: 30
```

2147483645 is `1111111111111111111111111111101` (31 digits). That is 31 ones with a single 0 in the "2s" position, so 30 bits are set.

### Constraints

- `1 <= n <= 2^31 - 1`

**Follow-up:** If this function is called many times, how would you optimize it?

---

## 3. Everyday Analogy

> **Explain it like I'm five**

Imagine a row of 32 light switches on a wall. Some are ON, some are OFF, and you want to know how many are ON.

- **The slow way:** walk past every single switch, all 32 of them, and count the ON ones. You always walk the whole wall, even if only one switch is ON.
- **The clever way:** you have a magic button that, every time you press it, turns **off the right-most switch that is ON** — and nothing else. Keep pressing it and count the presses. When every switch is OFF, the number of presses equals the number of switches that were ON. If only one switch was ON, you press just once!

That magic button is `n & (n - 1)`.

---

## 4. Step-by-Step Logic

1. **Reading one bit.** `n & 1` is the lowest bit of `n` (1 if `n` is odd). `(n >> i) & 1` is bit `i`.
2. **Simple plan.** Look at every bit position from 0 to 31 and add up the bits. That always costs 32 steps.
3. **Look closer at `n - 1`.** Subtracting 1 turns the lowest set bit into 0 and every 0 below it into 1. Everything above stays the same:

   ```text
   n       = 1011 0100
   n - 1   = 1011 0011
   n & (n-1) = 1011 0000   <- the lowest 1 of n has vanished
   ```

4. **So `n & (n - 1)` removes exactly one set bit** — the lowest one. Repeating it until `n` becomes 0 takes exactly as many steps as there are set bits.
5. **Count the steps.** That count is the answer. For `n = 128` this loops only once, instead of 32 times.
6. **Follow-up (many calls).** Precompute the popcount of all 256 possible bytes once, then answer each query by looking up its 4 bytes and adding the 4 results. Each call is then 4 table lookups.

---

## 5. Brute-Force Solution

### Algorithm

1. `count = 0`.
2. For each bit position `i` from 0 to 31: if bit `i` of `n` is 1, add 1 to `count`.
3. Return `count`.

### Python code

```python
class Solution:
    def hammingWeight(self, n: int) -> int:
        count = 0
        for i in range(32):          # check every one of the 32 positions
            if (n >> i) & 1:         # is bit i set?
                count += 1
        return count
```

### Explanation

- `n >> i` slides bit `i` down to position 0, and `& 1` keeps only that bit.
- We check 32 positions because the input fits in a 32-bit integer (in fact in 31 bits, so bit 31 is always 0 here — checking it is harmless).
- This is correct and fast enough for LeetCode; it is "brute force" because it inspects every position, including all the zeros.

### Complexity

- **Time:** `O(32)` = `O(1)` — always exactly 32 iterations.
- **Auxiliary space:** `O(1)`.

---

## 6. Optimized Solution

### Idea — Brian Kernighan's trick

`n & (n - 1)` deletes the lowest set bit of `n`. Keep deleting and count how many times you can do it before `n` reaches 0.

### Algorithm

1. `count = 0`.
2. While `n != 0`:
   - `n &= n - 1` (remove the lowest set bit).
   - `count += 1`.
3. Return `count`.

### Python code (LeetCode-ready)

```python
class Solution:
    def hammingWeight(self, n: int) -> int:
        count = 0
        while n:
            n &= n - 1      # drop the lowest set bit
            count += 1
        return count
```

### Follow-up: called many times — byte lookup table

If the function is called millions of times, do the expensive work **once**. Precompute how many 1 bits each byte value (0–255) has, then split every 32-bit number into 4 bytes and add 4 table entries.

```python
class Solution:
    # Built once when the class is created: BYTE_BITS[b] = popcount of b.
    BYTE_BITS = [0] * 256
    for _b in range(1, 256):
        BYTE_BITS[_b] = BYTE_BITS[_b >> 1] + (_b & 1)

    def hammingWeight(self, n: int) -> int:
        table = self.BYTE_BITS
        return (table[n & 0xFF]
                + table[(n >> 8) & 0xFF]
                + table[(n >> 16) & 0xFF]
                + table[(n >> 24) & 0xFF])
```

The table costs 256 integers of memory (a constant), and every call does a fixed 4 lookups, regardless of how many bits are set. The table-building rule `BYTE_BITS[b] = BYTE_BITS[b >> 1] + (b & 1)` is the same idea as the next problem, [Counting Bits](013_counting_bits.md).

**Python shortcuts:** `bin(n).count("1")` and, in Python 3.10+, `n.bit_count()` both return the popcount. They are fine in real code, but interviewers usually want to see one of the bit-manipulation approaches above.

---

## 7. Line-by-Line Explanation

(Kernighan version)

| Line | What it does | Why |
|---|---|---|
| `count = 0` | Starts the counter. | No set bits removed yet. |
| `while n:` | Loops while `n` still has at least one set bit. | `0` is the only value with no set bits, and Python treats `0` as false. |
| `n &= n - 1` | Replaces `n` with `n & (n - 1)`. | `n - 1` flips the lowest set bit to 0 and the zeros below it to 1; ANDing with `n` keeps everything above unchanged and wipes out that lowest 1 (the newly created low 1s are ANDed with 0s from `n`). |
| `count += 1` | Counts the bit we just removed. | One loop iteration = one set bit. |
| `return count` | Returns the number of removed bits. | All set bits have been removed exactly once. |

---

## 8. Dry Run

**Input (Example 1):** `n = 11` (Kernighan version)

| Iteration | `n` before (binary) | `n - 1` (binary) | `n & (n - 1)` | `count` after |
|---|---|---|---|---|
| 1 | `1011` (11) | `1010` (10) | `1010` (10) | 1 |
| 2 | `1010` (10) | `1001` (9) | `1000` (8) | 2 |
| 3 | `1000` (8) | `0111` (7) | `0000` (0) | 3 |

`n` is now 0, so the loop stops. **Result:** `3` ✅

**Example 2:** `n = 128` = `10000000`. One iteration: `128 & 127 = 10000000 & 01111111 = 0`, `count = 1`. **Result:** `1` ✅ — the brute force would have checked all 32 positions to reach the same answer.

### Second dry run — brute force on `n = 11`

| `i` | `n >> i` (binary) | `(n >> i) & 1` | `count` |
|---|---|---|---|
| 0 | `1011` | 1 | 1 |
| 1 | `101` | 1 | 2 |
| 2 | `10` | 0 | 2 |
| 3 | `1` | 1 | 3 |
| 4 … 31 | `0` | 0 | 3 |

**Result:** `3` ✅

---

## 9. Concepts, Data Structures, and Patterns

- **Bit primer:** binary representation and the operators `&`, `|`, `^`, `~`, `<<`, `>>` are explained in the [mini primer in note 011](011_sum_of_two_integers.md#9-concepts-data-structures-and-patterns). The ones used here:
  - `x & 1` — the lowest bit of `x`.
  - `x >> i` — shifts right, so bit `i` lands in position 0.
  - `x & (x - 1)` — `x` with its lowest set bit cleared.
- **Kernighan's trick in other problems:**
  - "Is `x` a power of two?" → `x > 0 and x & (x - 1) == 0` (a power of two has exactly one set bit).
  - Counting bits for all numbers: `ans[i] = ans[i & (i - 1)] + 1` ([013_counting_bits.md](013_counting_bits.md)).
- **Lookup tables (precomputation):** trading a small fixed amount of memory for faster repeated queries — the standard answer to "what if this is called many times?". The same follow-up appears in [015_reverse_bits.md](015_reverse_bits.md).
- **Hamming distance:** the number of positions where two numbers differ equals `hammingWeight(a ^ b)`.

---

## 10. Complexity Analysis

Let `k` be the number of set bits in `n` (here `1 <= k <= 31`).

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Check all 32 bits (brute force) | `O(32)` = `O(1)` | `O(1)` | Always 32 iterations. |
| Kernighan `n & (n - 1)` (optimized) | `O(k)` ≤ `O(31)` = `O(1)` | `O(1)` | One iteration per set bit; very fast for sparse numbers such as powers of two. |
| Byte lookup table (follow-up) | `O(1)` per call: 4 lookups | `O(256)` = `O(1)` | Table built once in 256 steps; each call is a fixed 4 lookups and 3 additions. |

All three are constant time because the input is bounded to 32 bits; the differences are in the constant (32 vs `k` vs 4).

---

## 11. Edge Cases

| Case | Example | Expected result | Why |
|---|---|---|---|
| Smallest input | `n = 1` | `1` | Single set bit. |
| Power of two | `n = 128` | `1` | Kernighan loop runs once. |
| Largest input | `n = 2147483647` (`2^31 - 1`) | `31` | All 31 low bits are set — Kernighan's worst case. |
| One zero among ones | `n = 2147483645` | `30` | Official example 3. |
| Alternating bits | `n = 0b1010101` (85) | `4` | Ones at positions 0, 2, 4, 6. |
| Two highest-ish bits | `n = 3 << 29` (1610612736) | `2` | Bits 29 and 30 only. |

---

## 12. Common Mistakes and Debugging

1. **Treating the input as a string.** On LeetCode's Python version, `n` is an `int`. Calling `n.count("1")` crashes; use `bin(n).count("1")` if you want the string approach.
2. **Writing `n & n - 1` and worrying about precedence.** In Python, `-` binds tighter than `&`, so `n & n - 1` already means `n & (n - 1)`. Adding parentheses is still clearer.
3. **Infinite loop with negative numbers.** If you ever reuse this code with negative Python integers, `while n:` with `n >>= 1` never ends (negative numbers keep their infinite leading 1s). Mask first with `n &= 0xFFFFFFFF`. The constraints here guarantee `n >= 1`, so it is not an issue for this problem.
4. **Off-by-one in the brute force.** `range(30)` stops at bit 29 and misses bit 30, which is set for every `n >= 2^30` (for example `2147483647` would give 30 instead of 31). Use `range(32)` (or loop `while n:` with `n >>= 1`).
5. **Using `n.bit_count()` on an old Python.** It exists only from Python 3.10.

**Debugging tip:** print `f"{n:032b}"` inside the loop; each iteration of the Kernighan loop should remove exactly the right-most `1`.

---

## 13. Practice Questions

**Q1. How many iterations does the Kernighan loop take for `n = 96`? List the values of `n`.**

<details><summary>Hint</summary>96 = 64 + 32. How many set bits is that?</summary></details>

**Answer:** 96 is `1100000`, which has 2 set bits, so 2 iterations: `96 & 95 = 1100000 & 1011111 = 1000000 = 64`, then `64 & 63 = 0`. The loop returns `2`.

**Q2. Write `is_power_of_two(x)` in one line using the same trick.**

<details><summary>Hint</summary>A power of two has exactly one set bit. What does `x & (x - 1)` become?</summary></details>

**Answer:** Removing the only set bit leaves 0. We also need `x > 0`, because 0 and negative numbers are not powers of two.

```python
def is_power_of_two(x):
    return x > 0 and x & (x - 1) == 0


assert is_power_of_two(1) is True
assert is_power_of_two(128) is True
assert is_power_of_two(96) is False
assert is_power_of_two(0) is False
```

**Q3. The Hamming distance between two integers is the number of bit positions where they differ. Compute it for `x = 1`, `y = 4`.**

<details><summary>Hint</summary>XOR marks exactly the positions that differ.</summary></details>

**Answer:** `1 ^ 4 = 001 ^ 100 = 101`, which has 2 set bits, so the distance is 2.

```python
def hamming_distance(x, y):
    diff = x ^ y
    count = 0
    while diff:
        diff &= diff - 1
        count += 1
    return count


assert hamming_distance(1, 4) == 2
assert hamming_distance(3, 1) == 1
assert hamming_distance(7, 7) == 0
```

**Q4. Count set bits using right shifts only (`n & 1` and `n >>= 1`), stopping as soon as `n` becomes 0.**

<details><summary>Hint</summary>Unlike the brute force, the loop condition is `while n`, so leading zeros are skipped.</summary></details>

**Answer:** This loops once per bit up to the highest set bit (for example 4 times for `11 = 1011`).

```python
def popcount_shift(n):
    count = 0
    while n:
        count += n & 1
        n >>= 1
    return count


assert popcount_shift(11) == 3
assert popcount_shift(128) == 1
assert popcount_shift(2147483645) == 30
```

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** Clear the lowest set bit with `n & (n - 1)`; count how many times until `n == 0`.
- **Brute force:** check all 32 positions with `(n >> i) & 1`.
- **Follow-up (many calls):** precomputed 256-entry byte table, 4 lookups per call.
- **Time:** `O(k)` where `k` = number of set bits (≤ 31), so `O(1)`. **Auxiliary space:** `O(1)`.
- **One-line memory hook:** *"`n & (n - 1)` switches off the right-most light."*

### Completion checklist

- [x] Problem requirements verified
- [x] Examples and constraints verified
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force solution written and tested
- [x] Optimized Python solution written and tested (`tools/tests/p012.py`)
- [x] Follow-up (lookup table) solution written and tested
- [x] Line-by-line explanation written
- [x] Dry run completed with a real example
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
