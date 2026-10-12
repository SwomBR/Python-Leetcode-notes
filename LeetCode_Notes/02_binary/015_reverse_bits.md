# 015. Reverse Bits

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Reverse Bits |
| **LeetCode number** | 190 |
| **Topic (source list)** | Binary |
| **Also uses** | Bit Manipulation, Divide and Conquer (follow-up) |
| **Difficulty** | Easy |
| **LeetCode URL** | <https://leetcode.com/problems/reverse-bits/> |
| **Pattern** | Pop bits from the right of `n`, push them onto the right of `result` (32 times) |

---

## 2. Problem Explanation

### What are we given?

`n` — an integer. In Python, LeetCode passes it as an ordinary `int` (not a binary string). We must think of it as exactly **32 bits**, including all the leading zeros.

### What must we return?

The integer you get when you write `n` as 32 binary digits and then **read those digits in reverse order** (bit 0 becomes bit 31, bit 1 becomes bit 30, …, bit 31 becomes bit 0).

### The rules

1. Always use all **32** positions. Leading zeros matter: `2` is `000…0010` (32 digits), and reversing it moves that single `1` near the top, giving `2^30`.
2. `n` is non-negative and **even** (see constraints). Because the lowest bit of an even number is 0, the reversed number's highest bit (bit 31) is 0. So the answer always fits in a signed 32-bit integer and is never negative.

### Examples

**Example 1**

```text
Input:  n = 43261596
Output: 964176192
```

```text
43261596  -> 00000010100101000001111010011100
964176192 -> 00111001011110000010100101000000
```

Read the first 32-digit string from right to left and you get the second string.

**Example 2**

```text
Input:  n = 2147483644
Output: 1073741822
```

```text
2147483644 -> 01111111111111111111111111111100
1073741822 -> 00111111111111111111111111111110
```

The pattern "one 0, twenty-nine 1s, two 0s" reversed becomes "two 0s, twenty-nine 1s, one 0".

### Constraints

- `0 <= n <= 2^31 - 2`
- `n` is even.

**Follow-up:** If this function is called many times, how would you optimize it?

---

## 3. Everyday Analogy

> **Explain it like I'm five**

Imagine a tube of 32 coloured beads, and you want them in the opposite order in a second tube.

You pull a bead out of the **right end** of the first tube and push it into the **right end** of the second tube. Each time you push a new bead in, the beads already in the second tube slide one place to the left.

- The first bead you pulled (the right-most one) gets pushed further and further left by every bead after it. After all 32 beads, it is at the **far left**.
- The last bead you pulled ends up at the **far right**.

That's exactly a reversal! In code, "pull from the right" is `n & 1` then `n >>= 1`, and "push in on the right" is `result = (result << 1) | bit`.

---

## 4. Step-by-Step Logic

1. **Reading the right-most bit:** `n & 1`.
2. **Removing it:** `n >>= 1` (shift everything right by one, the old lowest bit falls off).
3. **Adding a bit to the right of `result`:** `result = (result << 1) | bit` — shift `result` left to make room, then put `bit` into the empty lowest position.
4. **Do this exactly 32 times** — not "until `n` becomes 0". Even when `n` runs out of 1s, the remaining zeros still need to be pushed into `result`, because each push moves the earlier bits one step further left. Stopping early would leave the bits in the wrong positions.
5. **Why it reverses:** the bit taken in step `i` (original position `i`) is shifted left by the `31 - i` later pushes, so it ends at position `31 - i`. That is the definition of reversal.
6. **Follow-up idea (many calls):** instead of moving bits one at a time, swap whole blocks: swap the two 16-bit halves, then the bytes inside each half, then the 4-bit nibbles, then bit pairs, then single bits. Five fixed steps reverse all 32 bits. Another option is a precomputed table of reversed bytes.

---

## 5. Brute-Force Solution

### Algorithm

1. Convert `n` to a 32-character binary string with leading zeros: `format(n, "032b")`.
2. Reverse the string with slicing: `[::-1]`.
3. Convert back to an integer with `int(text, 2)`.

### Python code

```python
class Solution:
    def reverseBits(self, n: int) -> int:
        bits = format(n, "032b")      # e.g. '00000010100101000001111010011100'
        reversed_bits = bits[::-1]    # read the characters backwards
        return int(reversed_bits, 2)  # parse as a base-2 number
```

### Explanation

- `format(n, "032b")` means "binary, padded with zeros to width 32". Without the `032`, leading zeros would be lost and the reversal would be wrong.
- This is the most direct translation of the problem statement. It is correct and accepted on LeetCode, but it creates two 32-character strings per call and parses text, which is slower than pure bit operations and does not show bit-manipulation skill.

### Complexity

- **Time:** `O(32)` = `O(1)` — a fixed 32 characters are formatted, reversed and parsed.
- **Auxiliary space:** `O(32)` = `O(1)` for the temporary strings.

---

## 6. Optimized Solution

### Idea

Move the bits one by one with shifts — no strings at all.

### Algorithm

1. `result = 0`.
2. Repeat 32 times:
   - `result = (result << 1) | (n & 1)` — push the lowest bit of `n` into `result`.
   - `n >>= 1` — discard that bit from `n`.
3. Return `result`.

### Python code (LeetCode-ready)

```python
class Solution:
    def reverseBits(self, n: int) -> int:
        result = 0
        for _ in range(32):
            result = (result << 1) | (n & 1)   # push n's lowest bit into result
            n >>= 1                            # drop that bit from n
        return result
```

### Follow-up: called many times — divide and conquer with masks

Swap bigger blocks first, then smaller ones. Each line uses a mask to pick out half the bits, moves them, and recombines:

```python
class Solution:
    def reverseBits(self, n: int) -> int:
        n = ((n >> 16) | (n << 16)) & 0xFFFFFFFF                 # swap 16-bit halves
        n = ((n & 0xFF00FF00) >> 8) | ((n & 0x00FF00FF) << 8)    # swap bytes
        n = ((n & 0xF0F0F0F0) >> 4) | ((n & 0x0F0F0F0F) << 4)    # swap nibbles (4 bits)
        n = ((n & 0xCCCCCCCC) >> 2) | ((n & 0x33333333) << 2)    # swap bit pairs
        n = ((n & 0xAAAAAAAA) >> 1) | ((n & 0x55555555) << 1)    # swap single bits
        return n
```

- `0xFF00FF00` = `11111111 00000000 11111111 00000000`: the upper byte of each 16-bit half.
- `0xF0F0F0F0` = `11110000` repeated: the upper nibble of each byte.
- `0xCCCCCCCC` = `1100` repeated; `0x33333333` = `0011` repeated.
- `0xAAAAAAAA` = `1010` repeated (odd positions); `0x55555555` = `0101` repeated (even positions).

Five constant steps instead of a 32-step loop. The `& 0xFFFFFFFF` on the first line is needed only in Python, to chop off the bits that `n << 16` pushes above bit 31 (Python integers do not overflow). After that line every value stays within 32 bits, because each later line shifts a masked half by exactly the amount that keeps it inside.

A second common answer to the follow-up is a **lookup table**: precompute the reversed value of every byte (256 entries) once, then reverse a 32-bit number by reversing its 4 bytes and placing them in opposite order (see Practice Question 3).

---

## 7. Line-by-Line Explanation

(Bit-by-bit loop)

| Line | What it does | Why |
|---|---|---|
| `result = 0` | Starts with 32 zero bits. | Bits will be pushed in from the right. |
| `for _ in range(32):` | Runs exactly 32 times. | Every one of the 32 positions, including leading zeros of `n`, must be processed. `_` means we don't need the loop counter. |
| `n & 1` | Reads the lowest bit of `n` (0 or 1). | This is the next bit to move, starting from original position 0. |
| `result << 1` | Shifts `result` left by one. | Makes an empty slot at position 0 and moves earlier bits one step closer to the top. |
| `(result << 1) \| (n & 1)` | Puts the bit into that empty slot. | OR with 0 or 1 sets only position 0. |
| `n >>= 1` | Shifts `n` right by one. | The next original bit becomes the new lowest bit. |
| `return result` | Returns the reversed number. | Original bit `i` has been shifted left `31 - i` times, so it sits at position `31 - i`. |

---

## 8. Dry Run

### Small example: `n = 6` (even, within the constraints)

`6` = `000…00110` (32 bits). Expected: bits 1 and 2 move to positions 30 and 29 → `2^30 + 2^29 = 1610612736`.

| Iteration | `n` before (low bits) | `n & 1` | `result` after (binary) |
|---|---|---|---|
| 1 | `110` | 0 | `0` |
| 2 | `11` | 1 | `1` |
| 3 | `1` | 1 | `11` |
| 4 – 32 | `0` | 0 | each of the 29 remaining pushes adds a 0 on the right: `11` followed by 29 zeros |

**Result:** `11` followed by 29 zeros = `3 × 2^29` = `1610612736` ✅. This shows why we must loop all 32 times: after iteration 3, `n` is already 0, but `result` is only 3 — the 29 extra pushes are what move the bits into the correct high positions.

### Official Example 1: `n = 43261596`

`n` = `00000010 10010100 00011110 10011100`. The loop takes bits from the right: the first 8 bits taken are `0, 0, 1, 1, 1, 0, 0, 1` (the last byte `10011100` read right to left).

| After iteration | Bits pushed in this group (in order) | `result` in binary | `result` (decimal) |
|---|---|---|---|
| 8 | `00111001` | `111001` | 57 |
| 16 | `01111000` | `00111001 01111000` | 14712 |
| 24 | `00101001` | `00111001 01111000 00101001` | 3766313 |
| 32 | `01000000` | `00111001 01111000 00101001 01000000` | 964176192 |

Each group of 8 pushed bits is one byte of `n` read backwards (`10011100` → `00111001`, `00011110` → `01111000`, `10010100` → `00101001`, `00000010` → `01000000`), and the bytes come out in reverse order.

**Result:** `964176192` ✅

**Example 2** (`2147483644` → `1073741822`) is verified by the test file.

---

## 9. Concepts, Data Structures, and Patterns

- **Bit primer:** see the [mini primer in note 011](011_sum_of_two_integers.md#9-concepts-data-structures-and-patterns). Used here: `n & 1`, `n >> 1`, `x << 1`, `|`, and masks such as `0xFF`.
- **"Pop from one number, push onto another":** the same shape as reversing the decimal digits of a number (`digit = x % 10`, `x //= 10`, `rev = rev * 10 + digit`) — in base 2, `% 2` becomes `& 1`, `// 2` becomes `>> 1`, and `* 2 +` becomes `<< 1 |`.
- **Fixed-width thinking:** a reversal is only defined relative to a width (here 32). That's why the loop count is fixed and the string version pads with `032b`.
- **Masks:** constants like `0x55555555` select every other bit. Masking + shifting lets you move many bits in parallel (the divide-and-conquer follow-up).
- **Precomputation for repeated calls:** a 256-entry table of reversed bytes — same idea as the byte popcount table in [012_number_of_1_bits.md](012_number_of_1_bits.md).
- **Related notes:** [011_sum_of_two_integers.md](011_sum_of_two_integers.md) (32-bit masking in Python), [013_counting_bits.md](013_counting_bits.md).

---

## 10. Complexity Analysis

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| String reverse (brute force) | `O(32)` = `O(1)` | `O(32)` = `O(1)` | Formats, slices and parses a 32-character string. |
| Bit-by-bit loop (optimized) | `O(32)` = `O(1)` | `O(1)` | Exactly 32 iterations of a few bit operations, two integer variables. |
| Divide and conquer masks (follow-up) | `O(log 32)` = 5 steps = `O(1)` | `O(1)` | Each step halves the block size: 16, 8, 4, 2, 1. |
| Byte lookup table (follow-up) | `O(1)` per call: 4 lookups | `O(256)` = `O(1)` | Table built once; each call reverses 4 bytes by lookup. |

All are constant time because the width is fixed at 32 bits. In general, for a `W`-bit word the loop is `O(W)` and the mask method is `O(log W)`.

---

## 11. Edge Cases

| Case | Example | Expected result | Why |
|---|---|---|---|
| Zero | `n = 0` | `0` | All 32 bits are 0. |
| Smallest non-zero even | `n = 2` | `1073741824` (`2^30`) | Bit 1 moves to bit 30. |
| Largest allowed | `n = 2147483646` (`2^31 - 2`) | `2147483646` | Bits 1–30 are set; the pattern `0 1…1 0` is its own mirror image. |
| Official example 2 | `n = 2147483644` | `1073741822` | Leading 0 and trailing `00` swap ends. |
| Small value with leading zeros | `n = 6` | `1610612736` | Shows why all 32 iterations are needed. |
| Palindromic bit pattern | `n = 0b0110 << 14` (`98304`) | `98304` | `00000000000000011000000000000000` reads the same both ways. |

---

## 12. Common Mistakes and Debugging

1. **Stopping when `n` becomes 0.** `while n:` instead of `for _ in range(32)` leaves the bits too low (for `n = 6` you'd return 3). Always loop 32 times.
2. **Using `bin(n)[::-1]`.** `bin` gives `'0b110'` with no leading zeros and with the `'0b'` prefix; reversing that is wrong. Use `format(n, "032b")`.
3. **Shifting in the wrong order.** `result = result | (n & 1)` followed by `result <<= 1` shifts one extra time at the end, producing a 33-bit value. Shift first, then OR (or remember to skip the final shift).
4. **Forgetting the 32-bit mask in the divide-and-conquer version.** In Python, `n << 16` keeps the high bits, so without `& 0xFFFFFFFF` the result can be larger than 32 bits.
5. **Precedence of `|` and `<<`.** `result << 1 | n & 1` actually works (`<<` and `&` bind tighter than `|`), but parentheses make the intent obvious.

**Debugging tip:** compare `format(n, "032b")` and `format(result, "032b")` side by side; the second must be the first read backwards.

---

## 13. Practice Questions

**Q1. What does `reverseBits(8)` return? Explain without running code.**

<details><summary>Hint</summary>8 is `1000`, i.e. only bit 3 is set. Where does bit 3 go?</summary></details>

**Answer:** Bit 3 moves to position `31 - 3 = 28`, so the answer is `2^28 = 268435456`.

**Q2. Reverse the decimal digits of a non-negative integer (e.g. `1230 → 321`) using the same pop/push pattern.**

<details><summary>Hint</summary>Pop with `% 10` and `// 10`; push with `* 10 +`.</summary></details>

**Answer:**

```python
def reverse_digits(x):
    result = 0
    while x:
        result = result * 10 + x % 10
        x //= 10
    return result


assert reverse_digits(1230) == 321
assert reverse_digits(7) == 7
assert reverse_digits(0) == 0
```

Here we *can* stop when `x` reaches 0, because decimal reversal does not keep leading zeros — unlike the fixed 32-bit reversal.

**Q3. Implement the lookup-table follow-up: precompute the reversal of every byte, then reverse a 32-bit number with 4 lookups.**

<details><summary>Hint</summary>The lowest byte of `n` becomes the highest byte of the answer, after being reversed itself.</summary></details>

**Answer:** Build `REV[b]` (8-bit reversal of `b`) once. Byte `k` of `n` (from the right) goes to byte `3 - k` of the result.

```python
def reverse_byte(b):
    r = 0
    for _ in range(8):
        r = (r << 1) | (b & 1)
        b >>= 1
    return r


REV = [reverse_byte(b) for b in range(256)]


def reverse_bits_table(n):
    return ((REV[n & 0xFF] << 24)
            | (REV[(n >> 8) & 0xFF] << 16)
            | (REV[(n >> 16) & 0xFF] << 8)
            | REV[(n >> 24) & 0xFF])


assert reverse_bits_table(43261596) == 964176192
assert reverse_bits_table(2147483644) == 1073741822
assert reverse_bits_table(0) == 0
assert REV[0b00000001] == 0b10000000
```

**Q4. Why is the answer always non-negative and below `2^31` for inputs allowed by the constraints?**

<details><summary>Hint</summary>Which original bit ends up in position 31?</summary></details>

**Answer:** Position 31 of the result receives original bit 0. Every allowed `n` is even, so bit 0 is 0, which means bit 31 of the answer is 0. A 32-bit value with bit 31 clear is at most `2^31 - 1` and is non-negative even when read as a signed integer.

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** Pop the lowest bit of `n`, push it onto the right of `result`, exactly 32 times.
- **Key line:** `result = (result << 1) | (n & 1); n >>= 1`.
- **Brute force:** `int(format(n, "032b")[::-1], 2)`.
- **Follow-up:** swap halves → bytes → nibbles → pairs → bits with masks (5 steps), or a 256-entry byte-reversal table.
- **Time:** `O(1)` (32 iterations). **Auxiliary space:** `O(1)`.
- **One-line memory hook:** *"Beads out the right of one tube, into the right of the other — all 32 of them."*

### Completion checklist

- [x] Problem requirements verified
- [x] Examples and constraints verified
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force solution written and tested
- [x] Optimized Python solution written and tested (`tools/tests/p015.py`)
- [x] Follow-up (divide and conquer) solution written and tested
- [x] Line-by-line explanation written
- [x] Dry run completed with a real example
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
