# 011. Sum of Two Integers

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Sum of Two Integers |
| **LeetCode number** | 371 |
| **Topic (source list)** | Binary |
| **Also uses** | Bit Manipulation, Math |
| **Difficulty** | Medium |
| **LeetCode URL** | <https://leetcode.com/problems/sum-of-two-integers/> |
| **Pattern** | Binary addition with XOR (sum without carry) and AND + shift (carry), plus a 32-bit mask in Python |

---

## 2. Problem Explanation

### What are we given?

Two integers, `a` and `b`. Either one can be negative, zero, or positive.

### What must we return?

Their sum, `a + b`, as an integer.

### The rules

1. You are **not allowed to use the `+` or `-` operators** to compute the answer. The whole point of the problem is to build addition yourself out of bitwise operations.
2. Because Python's integers have no fixed size, we must be careful with negative numbers (explained in sections 4 and 9). This is a Python-specific difficulty; in Java or C++ the same code works without a mask because their `int` is already exactly 32 bits.

### Examples

**Example 1**

```text
Input:  a = 1, b = 2
Output: 3
```

In binary, `1` is `01` and `2` is `10`. They have no `1` bits in the same position, so the bits simply combine into `11`, which is 3. No carrying is needed.

**Example 2**

```text
Input:  a = 2, b = 3
Output: 5
```

In binary, `2` is `010` and `3` is `011`. Both have a `1` in the "2s" position, so that position produces a carry into the "4s" position, giving `101`, which is 5.

### Constraints

- `-1000 <= a, b <= 1000`

There is no follow-up for this problem.

---

## 3. Everyday Analogy

> **Explain it like I'm five**

Think about how you add `58 + 67` on paper. You do two separate jobs:

1. **Write down the digit for each column** (8 + 7 = 15, so write 5), and
2. **Carry the extra** into the next column (carry the 1).

Then you add the carries in, which might create *new* carries, and you repeat until nothing is left to carry.

Computers add binary numbers the same way, but binary is even simpler because each column only holds a 0 or a 1:

- **0 + 0** → write 0, carry nothing.
- **0 + 1** or **1 + 0** → write 1, carry nothing.
- **1 + 1** → write 0, **carry 1** to the next column on the left.

There are two magic tools that do these two jobs for *every column at once*:

- **XOR (`^`)** writes the digit without worrying about carries ("1 if exactly one of them is 1").
- **AND (`&`)** finds the columns where both are 1 — exactly the columns that create a carry. Shifting that left by one (`<< 1`) moves each carry into the next column.

So we keep doing "write the digits" + "collect the carries" until there are no carries left. That's addition, with no `+` in sight!

---

## 4. Step-by-Step Logic

1. **Split addition into two parts.** For binary numbers `a` and `b`:
   - `a ^ b` is the sum **ignoring carries**.
   - `(a & b) << 1` is the **carries**, already moved one column to the left.
   - Fact: `a + b == (a ^ b) + ((a & b) << 1)`.
2. **Repeat.** The right-hand side is again "a number plus a number", so we replace `a` with `a ^ b` and `b` with the carries, and repeat until the carry part `b` becomes 0. Then `a` alone is the answer.
3. **Why it stops (in a fixed-size world).** Each round, the carry is shifted left at least one more position. In a 32-bit world, after at most 32 rounds the carry is pushed out of the 32 bits and becomes 0.
4. **Python's problem: integers never run out of bits.** In Java, `-1` is stored as 32 ones. In Python, `-1` behaves like an *infinite* row of ones (`...11111`). If we add `-1 + 1` with the plain loop, the carry keeps moving left forever because there is always another `1` waiting to the left — an **infinite loop**.
5. **The fix: pretend to be a 32-bit machine.** After every step, keep only the lowest 32 bits using `& 0xFFFFFFFF` (`0xFFFFFFFF` is 32 ones in binary). Now carries that walk past bit 31 simply fall off, exactly like real 32-bit hardware.
6. **Convert back to a signed number.** The masked result is a number between `0` and `2^32 - 1`. In the 32-bit "two's complement" system, patterns whose top bit (bit 31) is 1 represent negative numbers. If the result is larger than `0x7FFFFFFF` (the largest positive 32-bit value), convert it back with `~(a ^ 0xFFFFFFFF)`.
7. **Do the inputs fit?** The constraints say `-1000 <= a, b <= 1000`, so the true sum is between `-2000` and `2000`, far inside the 32-bit range. The 32-bit simulation therefore always gives the exact answer.

---

## 5. Brute-Force Solution

There is no "obvious" slow way to add two numbers without `+` and `-` (counting up one by one would itself need `+ 1`). The most honest simple approach is to copy what you do on paper: a **ripple-carry adder** that walks through all 32 bit positions one at a time.

### Algorithm

1. Mask both numbers to their 32-bit patterns: `x = a & MASK`, `y = b & MASK`.
2. Start with `carry = 0` and `result = 0`.
3. For each bit position `i` from 0 to 31:
   - Read the bits: `bit_a = (x >> i) & 1`, `bit_b = (y >> i) & 1`.
   - The sum bit is `bit_a ^ bit_b ^ carry` (1 when an odd number of the three are 1).
   - The new carry is `1` if at least two of the three are 1: `(bit_a & bit_b) | (carry & (bit_a ^ bit_b))`.
   - Put the sum bit into position `i` of `result` with `result |= sum_bit << i`.
4. Ignore the final carry out of bit 31 (a real 32-bit adder throws it away too).
5. Convert `result` from a 32-bit pattern to a signed Python integer.

### Python code

```python
class Solution:
    def getSum(self, a: int, b: int) -> int:
        MASK = 0xFFFFFFFF        # 32 ones
        MAX_INT = 0x7FFFFFFF     # largest positive 32-bit signed value

        x, y = a & MASK, b & MASK    # 32-bit two's complement patterns
        carry = 0
        result = 0
        for i in range(32):          # one column at a time, right to left
            bit_a = (x >> i) & 1
            bit_b = (y >> i) & 1
            sum_bit = bit_a ^ bit_b ^ carry
            carry = (bit_a & bit_b) | (carry & (bit_a ^ bit_b))
            result |= sum_bit << i

        # Interpret the 32-bit pattern as a signed number.
        return result if result <= MAX_INT else ~(result ^ MASK)
```

### Explanation

- This is a "full adder" (the circuit inside every CPU) applied to each column in turn. A full adder takes two input bits plus an incoming carry and produces one output bit plus an outgoing carry.
- `range(32)` counts positions for us, so we never write `+` or `-` ourselves.
- The last line turns a 32-bit pattern back into a normal (possibly negative) Python integer — see section 7 for exactly why `~(result ^ MASK)` works.

### Complexity

- **Time:** `O(32)` = `O(1)`. It *always* processes all 32 bit positions, even for `1 + 2` where only two positions matter. Each step handles a single bit, so it does about 32 rounds of several operations every time. It is accepted on LeetCode (no time-out); it is "brute force" because it works one bit at a time instead of using whole-word operations.
- **Auxiliary space:** `O(1)` — a handful of integer variables.

---

## 6. Optimized Solution

### Idea

Instead of handling one column at a time, use whole-word bitwise operations so that **all 32 columns are processed in parallel**:

- `a ^ b` → every column's digit, ignoring carries.
- `(a & b) << 1` → every column's carry, shifted to where it must be added.

Repeat with these two new numbers until the carry is 0. Mask to 32 bits on every step so negative numbers behave like they do on a 32-bit machine.

### Algorithm

1. `MASK = 0xFFFFFFFF`, `MAX_INT = 0x7FFFFFFF`.
2. `a &= MASK`, `b &= MASK` (turn both into 32-bit patterns).
3. While `b != 0`:
   - `carry = (a & b) << 1`
   - `a = (a ^ b) & MASK`
   - `b = carry & MASK`
4. If `a <= MAX_INT`, it is a non-negative number: return `a`.
5. Otherwise it encodes a negative number: return `~(a ^ MASK)`.

### Python code (LeetCode-ready)

```python
class Solution:
    def getSum(self, a: int, b: int) -> int:
        MASK = 0xFFFFFFFF        # keeps the lowest 32 bits
        MAX_INT = 0x7FFFFFFF     # 2^31 - 1, largest positive 32-bit value

        a &= MASK
        b &= MASK
        while b != 0:
            carry = (a & b) << 1     # columns where both bits are 1, moved left
            a = (a ^ b) & MASK       # column sums without carries
            b = carry & MASK         # carries still to be added (drop bit 32)

        # Bit 31 set means the 32-bit pattern represents a negative number.
        return a if a <= MAX_INT else ~(a ^ MASK)
```

---

## 7. Line-by-Line Explanation

| Line | What it does | Why |
|---|---|---|
| `MASK = 0xFFFFFFFF` | A number whose binary form is 32 ones. | `x & MASK` keeps only the lowest 32 bits of `x`, simulating a 32-bit integer. |
| `MAX_INT = 0x7FFFFFFF` | `2^31 - 1 = 2147483647`: 0 followed by 31 ones. | Any 32-bit pattern above this has bit 31 set, which means "negative" in two's complement. |
| `a &= MASK` / `b &= MASK` | Converts each input into its 32-bit pattern. | For example `-3 & MASK` is `0xFFFFFFFD` (4294967293). Positive numbers below `2^31` are unchanged. |
| `while b != 0:` | Keeps going while there are carries left to add. | When `b` is 0, `a + 0 == a`, so `a` is the final pattern. |
| `carry = (a & b) << 1` | `a & b` marks the columns where both numbers have a 1; `<< 1` moves each such carry one column left. | `1 + 1` in a column produces a 1 in the next column. |
| `a = (a ^ b) & MASK` | Adds every column **without** carries. | XOR gives 1 exactly when one of the two bits is 1. The mask is harmless here but keeps the habit consistent. |
| `b = carry & MASK` | The carries become the new "second number". | The mask drops any carry that moved into bit 32, exactly like a real 32-bit adder. **Without this mask, negative inputs loop forever in Python.** |
| `return a if a <= MAX_INT else ~(a ^ MASK)` | Turns the 32-bit pattern back into a Python integer. | See the box below. |

**Why `~(a ^ MASK)` gives the negative value**

In 32-bit two's complement, a pattern `a` with bit 31 set means the number `a - 2^32`. We cannot write `-`, so we use two bit tricks:

1. `a ^ MASK` flips all 32 low bits. Because `a` fits in 32 bits, this equals `MASK - a`.
2. In Python, `~x` is defined as `-x - 1` (it flips *all* bits, including the infinite sign bits).

So `~(a ^ MASK) = -(MASK - a) - 1 = a - MASK - 1 = a - 2^32`. Exactly the signed value we want.

Example: `a = 0xFFFFFFFB` (4294967291). `a ^ MASK = 4`, and `~4 = -5`. ✅

---

## 8. Dry Run

**Input (Example 2):** `a = 2`, `b = 3`

Both are positive and small, so masking changes nothing. Binary is shown with 4 bits for readability.

| Round | `a` (binary) | `b` (binary) | `a & b` | `carry = (a & b) << 1` | new `a = a ^ b` | new `b = carry` |
|---|---|---|---|---|---|---|
| 1 | `0010` (2) | `0011` (3) | `0010` | `0100` (4) | `0001` (1) | `0100` (4) |
| 2 | `0001` (1) | `0100` (4) | `0000` | `0000` (0) | `0101` (5) | `0000` (0) |

`b` is now 0, so the loop stops. `a = 5 <= MAX_INT`, so we return **5** ✅.

**Example 1:** `a = 1` (`01`), `b = 2` (`10`). Round 1: `a & b = 0`, so `carry = 0`; `a = 01 ^ 10 = 11 = 3`; `b = 0`. Return **3** ✅ after a single round.

### Second dry run — two negative numbers

**Input:** `a = -3`, `b = -2` (expected `-5`). Patterns are shown in hexadecimal (each hex digit = 4 bits).

| Step | `a` | `b` | Notes |
|---|---|---|---|
| Mask inputs | `0xFFFFFFFD` | `0xFFFFFFFE` | `-3` and `-2` in 32-bit two's complement. |
| Round 1: `a & b` | — | — | `0xFFFFFFFC` |
| Round 1: `carry` | — | — | `0xFFFFFFFC << 1 = 0x1FFFFFFF8` (33 bits) |
| Round 1: update | `0xFFFFFFFD ^ 0xFFFFFFFE = 0x00000003` | `0x1FFFFFFF8 & MASK = 0xFFFFFFF8` | The mask drops bit 32. |
| Round 2: `a & b` | — | — | `0x3 & 0xFFFFFFF8 = 0` → `carry = 0` |
| Round 2: update | `0x3 ^ 0xFFFFFFF8 = 0xFFFFFFFB` | `0` | Loop ends. |
| Convert | `0xFFFFFFFB > 0x7FFFFFFF` | — | Negative: `~(0xFFFFFFFB ^ 0xFFFFFFFF) = ~4 = -5` |

**Result:** `-5` ✅

---

## 9. Concepts, Data Structures, and Patterns

### Mini primer: binary and bitwise operators

This primer is shared by all the notes in the Binary section ([012](012_number_of_1_bits.md), [013](013_counting_bits.md), [014](014_missing_number.md), [015](015_reverse_bits.md)).

**Binary representation.** Computers store numbers in base 2. Each position (bit) is worth a power of two, counted from the right starting at position 0:

```text
position:  3  2  1  0
value:     8  4  2  1
13      =  1  1  0  1   ->  8 + 4 + 1
```

In Python, `bin(13)` gives `'0b1101'`, `0b1101` is a literal for 13, and `0xFF` is a hexadecimal literal (each hex digit is 4 bits: `0xF` = `1111`).

**Bitwise operators** work on every bit position independently:

| Operator | Name | Rule per bit | Example (`a = 1100`, `b = 1010`) |
|---|---|---|---|
| `a & b` | AND | 1 if **both** are 1 | `1000` |
| `a \| b` | OR | 1 if **at least one** is 1 | `1110` |
| `a ^ b` | XOR | 1 if **exactly one** is 1 | `0110` |
| `~a` | NOT | flips every bit; in Python `~a == -a - 1` | `~12 == -13` |
| `a << k` | left shift | moves bits left by `k`; same as multiplying by `2^k` | `0011 << 2 = 1100` (3 → 12) |
| `a >> k` | right shift | moves bits right by `k`, dropping the lowest `k` bits; same as `a // 2^k` | `1101 >> 1 = 0110` (13 → 6) |

**Useful identities:** `x ^ x == 0`, `x ^ 0 == x`, `x & 1` is the lowest bit (1 if odd), `(x >> i) & 1` reads bit `i`, `x | (1 << i)` sets bit `i`.

**Two's complement (negative numbers).** In a 32-bit integer, the pattern for `-x` is "flip all bits of `x`, then add 1". So `-1` is 32 ones (`0xFFFFFFFF`) and `-5` is `0xFFFFFFFB`. Bit 31 acts as the sign bit. Python integers are **unbounded**: Python behaves as if a negative number had infinitely many 1s on the left. That is why this problem needs `& 0xFFFFFFFF` to chop numbers down to 32 bits and a final conversion back to a signed value.

### Concepts used in this problem

- **Half adder / full adder:** XOR produces a sum bit and AND produces a carry bit. Chaining full adders bit by bit gives the ripple-carry brute force.
- **Word-level parallelism:** the optimized loop applies XOR and AND to all 32 columns in one operation, so the number of rounds depends on how far carries travel, not on the number of bits.
- **Masking:** `& 0xFFFFFFFF` simulates fixed-width integer overflow in a language that has none.
- **Sign conversion:** `~(x ^ MASK)` converts an unsigned 32-bit pattern to a negative Python integer without using `-`.
- **Related notes:** counting the `1` bits of a number ([012_number_of_1_bits.md](012_number_of_1_bits.md)), XOR cancellation ([014_missing_number.md](014_missing_number.md)), and shifting bits one by one ([015_reverse_bits.md](015_reverse_bits.md)).

---

## 10. Complexity Analysis

Let `W = 32` be the word size we simulate.

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Ripple-carry adder (brute force) | `O(W)` = `O(1)` | `O(1)` | Always exactly 32 iterations, one per bit. |
| XOR / carry loop (optimized) | `O(W)` = `O(1)` worst case | `O(1)` | Each round, the lowest set bit of the carry moves at least one position left, so there are at most 32 rounds. Typical inputs need far fewer (Example 1 needs 1 round). |

**Why is it fine to call both `O(1)`?** The number of bits is fixed at 32 and does not grow with the input value, so the work is bounded by a constant. The difference is practical: the brute force always does 32 rounds of single-bit work, while the optimized loop processes all bits at once and stops as soon as no carries remain. A worst case for the optimized version is something like `-1 + 1`: the carry ripples through all 32 positions before falling off the top, so the loop runs 32 times.

---

## 11. Edge Cases

| Case | Example | Expected result | Why it works |
|---|---|---|---|
| Both zero | `a = 0, b = 0` | `0` | `b` is already 0, loop never runs. |
| Opposite numbers | `a = -1, b = 1` | `0` | The carry ripples through all 32 bits and falls off the top thanks to the mask. Without the mask this loops forever. |
| Both negative | `a = -3, b = -2` | `-5` | Result pattern `0xFFFFFFFB` has bit 31 set and is converted back. |
| Mixed signs, negative result | `a = 5, b = -8` | `-3` | Works the same way; only the final conversion differs. |
| Mixed signs, positive result | `a = -5, b = 8` | `3` | Final pattern `0x3` is below `MAX_INT`, returned unchanged. |
| Largest values | `a = 1000, b = 1000` | `2000` | Far below `2^31 - 1`. |
| Smallest values | `a = -1000, b = -1000` | `-2000` | Far above `-2^31`. |
| One operand zero | `a = -7, b = 0` | `-7` | Loop skipped; `0xFFFFFFF9` converts back to `-7`. |

---

## 12. Common Mistakes and Debugging

1. **Forgetting the mask in Python.** The plain loop `while b: a, b = a ^ b, (a & b) << 1` works in Java/C++ but **never ends** in Python for inputs like `-1, 1`, because Python's negative numbers have infinitely many leading 1s and the carry never falls off.
2. **Forgetting to convert back.** Returning the masked value gives `4294967291` instead of `-5`. Always check bit 31.
3. **Using `-` in the conversion.** `a - 2**32` is the natural formula but uses `-`. `~(a ^ MASK)` gives the same value with bit operations only.
4. **Computing the carry from the updated `a`.** Write `carry = (a & b) << 1` **before** you overwrite `a` with `a ^ b`, or use simultaneous assignment `a, b = a ^ b, (a & b) << 1`.
5. **"Cheating" with built-ins.** `sum([a, b])` or `operator.add(a, b)` technically avoid typing `+`, but they miss the point of the exercise and an interviewer will not accept them.
6. **Thinking `~a` means `-a`.** In Python `~a == -a - 1`. For example `~5 == -6`.

**Debugging tip:** print each round with fixed-width binary: `print(f"{a:032b} {b:032b}")`. You will see the carry bits move left each round; if they never disappear, the mask is missing.

---

## 13. Practice Questions

**Q1. Trace the optimized loop for `a = 5`, `b = 7`. How many rounds does it take?**

<details><summary>Hint</summary>Write 5 = `0101` and 7 = `0111`. Each round compute `a ^ b` and `(a & b) << 1`.</summary></details>

**Answer:** 3 rounds.

- Round 1: `a & b = 0101`, carry = `1010` (10); `a = 0101 ^ 0111 = 0010` (2); `b = 1010` (10).
- Round 2: `a & b = 0010`, carry = `0100` (4); `a = 0010 ^ 1010 = 1000` (8); `b = 0100` (4).
- Round 3: `a & b = 0000`, carry = 0; `a = 1000 ^ 0100 = 1100` (12); `b = 0`.

Result: `12` ✅

**Q2. Using only bitwise operators, write `subtract(a, b)` that returns `a - b`.**

<details><summary>Hint</summary>In two's complement, `-b` equals `~b + 1`. You already know how to add without `+`.</summary></details>

**Answer:** Negate `b` by flipping its bits and adding 1 (with our own adder), then add.

```python
def add32(a, b):
    MASK, MAX_INT = 0xFFFFFFFF, 0x7FFFFFFF
    a &= MASK
    b &= MASK
    while b:
        a, b = (a ^ b) & MASK, ((a & b) << 1) & MASK
    return a if a <= MAX_INT else ~(a ^ MASK)


def subtract(a, b):
    negative_b = add32(~b, 1)      # two's complement negation
    return add32(a, negative_b)


assert subtract(5, 3) == 2
assert subtract(3, 5) == -2
assert subtract(-1000, 1000) == -2000
assert subtract(0, -7) == 7
```

**Q3. Write `to_signed32(x)` that converts a 32-bit pattern (`0 <= x < 2^32`) into the signed number it represents. What is `to_signed32(0xFFFFFFF6)`?**

<details><summary>Hint</summary>Check bit 31. If it's set, flip the low 32 bits and apply Python's `~`.</summary></details>

**Answer:** `0xFFFFFFF6 ^ 0xFFFFFFFF = 9`, and `~9 = -10`, so the answer is `-10`.

```python
def to_signed32(x):
    return x if x <= 0x7FFFFFFF else ~(x ^ 0xFFFFFFFF)


assert to_signed32(0xFFFFFFF6) == -10
assert to_signed32(0xFFFFFFFF) == -1
assert to_signed32(0x80000000) == -2147483648
assert to_signed32(5) == 5
```

**Q4. Why is the optimized loop guaranteed to stop after at most 32 rounds?**

<details><summary>Hint</summary>Look at the lowest bit position where `b` can be 1 after each round.</summary></details>

**Answer:** The new `b` is `(a & b) << 1`. Shifting left by one means its lowest set bit is always at least one position higher than the lowest set bit of the old `b`. After round `k`, bits `0 .. k-1` of `b` are all 0. After 32 rounds all 32 kept bits are 0, and because we mask with `0xFFFFFFFF`, anything that moved past bit 31 is discarded. So `b` must be 0 by then.

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** Bitwise addition — XOR for the sum without carry, AND + left shift for the carry, repeat until the carry is 0.
- **Python twist:** mask with `0xFFFFFFFF` every round; at the end, if `a > 0x7FFFFFFF`, return `~(a ^ 0xFFFFFFFF)`.
- **Brute force:** ripple-carry full adder over all 32 bits.
- **Time:** `O(1)` (at most 32 rounds). **Auxiliary space:** `O(1)`.
- **One-line memory hook:** *"XOR writes the digits, AND passes the carries, the mask keeps Python honest."*

### Completion checklist

- [x] Problem requirements verified
- [x] Examples and constraints verified
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force solution written and tested
- [x] Optimized Python solution written and tested (`tools/tests/p011.py`)
- [x] Line-by-line explanation written
- [x] Dry run completed with a real example
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
