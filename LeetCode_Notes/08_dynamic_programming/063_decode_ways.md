# 063. Decode Ways

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Decode Ways |
| **LeetCode number** | 91 |
| **Topic (source list)** | Dynamic Programming |
| **Also uses** | String, Recursion + Memoization |
| **Difficulty** | Medium |
| **LeetCode URL** | <https://leetcode.com/problems/decode-ways/> |
| **Pattern** | 1-D counting DP over string prefixes (Fibonacci-like, with validity checks) |

---

## 2. Problem Explanation

### What are we given?

`s` — a string made only of digit characters `'0'`–`'9'`. It may even start with `'0'`.

### What is the code?

Letters were turned into numbers: `A → "1"`, `B → "2"`, …, `Z → "26"`. Then all the numbers were written next to each other with no separators. So `"12"` might mean `1, 2` (`"AB"`) or `12` (`"L"`).

### What must we return?

The **number of different ways** to split `s` into pieces where **every piece is a valid code**. If no split works, return `0`.

### What counts as a valid piece? (Be precise about zeros!)

- A **one-digit** piece is valid if it is `"1"`–`"9"`. The piece `"0"` on its own is **invalid** — no letter has code 0.
- A **two-digit** piece is valid if it is between `"10"` and `"26"`.
  - `"10"` (J) and `"20"` (T) are valid — this is the **only** way a `'0'` can be used.
  - `"30"`, `"40"`, …, `"90"` are invalid (greater than 26).
  - `"06"`, `"01"`, … are invalid: a piece **cannot start with `'0'`**. `"06"` is not the same as `"6"`.
  - `"27"`–`"99"` are invalid (greater than 26).
- No piece is longer than two digits (the largest code, 26, has two digits).

For instance, the statement shows that `"11106"` splits validly as `(1, 1, 10, 6)` → `"AAJF"` and `(11, 10, 6)` → `"KJF"`, while `(1, 11, 06)` is invalid because of `"06"`. So `"11106"` has 2 decodings.

### Examples

**Example 1**

```text
Input:  s = "12"
Output: 2
```

`(1, 2)` → `"AB"` and `(12)` → `"L"`.

**Example 2**

```text
Input:  s = "226"
Output: 3
```

`(2, 26)` → `"BZ"`, `(22, 6)` → `"VF"`, `(2, 2, 6)` → `"BBF"`.

**Example 3**

```text
Input:  s = "06"
Output: 0
```

The first piece would have to be `"0"` (invalid) or `"06"` (invalid — leading zero). No decoding exists.

### Constraints

- `1 <= s.length <= 100`
- `s` contains only digits and may contain leading zero(s).
- The test cases are generated so that the answer fits in a **32-bit integer**. (Python integers never overflow, but this tells you the count is at most `2^31 - 1`.)

There is no follow-up in the official statement.

---

## 3. Everyday Analogy

> **Explain it like I'm five**

You have a long strip of number stickers and a pair of scissors. You must cut the strip into small pieces, and every piece must be a "real letter number" from 1 to 26 — one sticker or two stickers long. A piece starting with a 0 sticker is not allowed, and a lonely 0 is not allowed either.

How many different ways can you cut the strip?

Think about the **last cut**. The last piece is either the last **one** sticker, or the last **two** stickers. So:

> ways to cut the whole strip = (ways to cut everything except the last sticker, *if* the last sticker is a valid piece) + (ways to cut everything except the last two stickers, *if* those two form a valid piece).

You work from the left, writing the number of ways for each prefix on a little card. Each new card only needs the two cards before it.

---

## 4. Step-by-Step Logic

We follow the **DP recipe**.

1. **State definition.** `dp[i]` = number of ways to decode the **first `i` characters** `s[0:i]`. (Using prefix *length* `i` makes the empty prefix easy to express.)
2. **Recurrence.** The last piece of `s[0:i]` is either:
   - **one digit** `s[i-1]` — valid if it is not `'0'` → add `dp[i-1]`;
   - **two digits** `s[i-2:i]` — valid if `10 <= int(s[i-2:i]) <= 26` (this automatically rejects `"06"` because `6 < 10`, and rejects `"30"`) → add `dp[i-2]`.

   `dp[i] = (dp[i-1] if s[i-1] != '0' else 0) + (dp[i-2] if 10 <= int(s[i-2:i]) <= 26 else 0)`
3. **Base cases.**
   - `dp[0] = 1`: the empty prefix has exactly one decoding — "decode nothing". This is what makes `"12"` count the whole-string piece `12` once.
   - `dp[1] = 1` if `s[0] != '0'`, else `0`.
4. **Iteration order.** `dp[i]` depends on `dp[i-1]` and `dp[i-2]`, so go `i = 2, 3, …, n`.
5. **Answer location.** `dp[n]`.
6. **A zero kills things.** If `dp` ever becomes 0 (for example after `"00"` or `"30"`), every later value built from it stays 0 in that branch — the string cannot be decoded through that point.
7. **Memory.** Only two previous values are used → two variables.

---

## 5. Brute-Force Solution

### Algorithm (plain recursion)

`count(i)` = number of ways to decode the suffix `s[i:]`.

- If `i == n` → `1` (we used every character successfully).
- If `s[i] == '0'` → `0` (no piece may start with `'0'`).
- Otherwise: take one digit → `count(i + 1)`; and if `s[i:i+2]` exists and is `<= 26`, also take two digits → `count(i + 2)`.

### Python code

```python
class Solution:
    def numDecodings(self, s: str) -> int:
        n = len(s)

        def count(i: int) -> int:
            if i == n:                 # reached the end: one complete decoding
                return 1
            if s[i] == "0":            # a piece can never start with '0'
                return 0
            ways = count(i + 1)        # one-digit piece s[i]
            if i + 1 < n and int(s[i:i + 2]) <= 26:
                ways += count(i + 2)   # two-digit piece s[i:i+2], 10..26
            return ways

        return count(0)
```

### Explanation

- Because `s[i] != '0'` at that point, the two-digit piece is between `10` and `99`; the check `<= 26` keeps exactly `10..26`.
- It explores every possible way to cut the string, so it is correct.
- For a string like `"1111…1"` both branches are always valid, so the call tree doubles almost every level (Fibonacci growth).

### Complexity

- **Time:** exponential, about `1.618^n` calls in the worst case (`O(2^n)` as a simple bound). For `n = 100` that would **time out** on LeetCode.
- **Auxiliary space:** `O(n)` recursion depth.

### The bridge — memoization

`count(i)` depends only on `i`, so there are just `n + 1` different subproblems:

```python
from functools import lru_cache


class Solution:
    def numDecodings(self, s: str) -> int:
        n = len(s)

        @lru_cache(maxsize=None)
        def count(i: int) -> int:
            if i == n:
                return 1
            if s[i] == "0":
                return 0
            ways = count(i + 1)
            if i + 1 < n and int(s[i:i + 2]) <= 26:
                ways += count(i + 2)
            return ways

        return count(0)
```

`O(n)` time and `O(n)` space. The bottom-up version below computes the same numbers starting from the left end (prefixes) instead of the right end (suffixes).

---

## 6. Optimized Solution

### Idea — bottom-up DP over prefixes, two rolling variables

`prev2 = dp[i-2]`, `prev1 = dp[i-1]`; compute `dp[i]` from them.

### Algorithm

1. `prev2 = 1` (`dp[0]`, empty prefix), `prev1 = 1 if s[0] != '0' else 0` (`dp[1]`).
2. For `i` from 2 to `n`:
   - `current = 0`.
   - If `s[i-1] != '0'`: `current += prev1`.
   - If `10 <= int(s[i-2:i]) <= 26`: `current += prev2`.
   - `prev2, prev1 = prev1, current`.
3. Return `prev1` (`dp[n]`).

### Python code (LeetCode-ready)

```python
class Solution:
    def numDecodings(self, s: str) -> int:
        prev2 = 1                          # dp[0]: empty prefix, one way
        prev1 = 0 if s[0] == "0" else 1    # dp[1]: first character alone

        for i in range(2, len(s) + 1):
            current = 0
            if s[i - 1] != "0":                     # last piece = one digit
                current += prev1
            if 10 <= int(s[i - 2:i]) <= 26:         # last piece = two digits
                current += prev2
            prev2, prev1 = prev1, current

        return prev1
```

### Version with the full DP table

```python
class Solution:
    def numDecodings(self, s: str) -> int:
        n = len(s)
        dp = [0] * (n + 1)
        dp[0] = 1
        dp[1] = 0 if s[0] == "0" else 1
        for i in range(2, n + 1):
            if s[i - 1] != "0":
                dp[i] += dp[i - 1]
            if 10 <= int(s[i - 2:i]) <= 26:
                dp[i] += dp[i - 2]
        return dp[n]
```

---

## 7. Line-by-Line Explanation

(Rolling-variable solution)

| Line | What it does | Why |
|---|---|---|
| `prev2 = 1` | `dp[0] = 1`. | One way to decode the empty prefix: do nothing. Needed so a two-digit piece covering the whole start (like `"12"` as `L`) is counted once. |
| `prev1 = 0 if s[0] == "0" else 1` | `dp[1]`. | A single `'0'` is not a letter; any other single digit is. |
| `for i in range(2, len(s) + 1):` | `i` is the prefix length being solved. | Builds `dp[2] … dp[n]` in order. For `n = 1` the loop does not run and `dp[1]` is returned. |
| `current = 0` | Start counting decodings of `s[0:i]`. | We add the two possible "last piece" options. |
| `if s[i - 1] != "0": current += prev1` | Last piece is one digit `s[i-1]`. | Valid only for `1..9`; the rest `s[0:i-1]` can be decoded in `dp[i-1]` ways. |
| `if 10 <= int(s[i - 2:i]) <= 26: current += prev2` | Last piece is two digits. | `>= 10` rejects a leading zero (`"06"` → 6); `<= 26` rejects `"27"`–`"99"`, including `"30"`. The rest `s[0:i-2]` decodes in `dp[i-2]` ways. |
| `prev2, prev1 = prev1, current` | Slide the window. | Next iteration needs `dp[i-1]` and `dp[i]`. |
| `return prev1` | `dp[n]`. | Number of decodings of the whole string. |

---

## 8. Dry Run

**Input:** `s = "226"` (Example 2), `n = 3`.

Start: `prev2 = dp[0] = 1`, `prev1 = dp[1] = 1` (`'2'` is valid).

| `i` | One digit `s[i-1]` | Valid? | Adds `prev1` | Two digits `s[i-2:i]` | Valid (10..26)? | Adds `prev2` | `current` = dp[i] | `prev2`, `prev1` after |
|---|---|---|---|---|---|---|---|---|
| 2 | `'2'` | yes | +1 | `"22"` | yes | +1 | 2 | 1, 2 |
| 3 | `'6'` | yes | +2 | `"26"` | yes | +1 | **3** | 2, 3 |

DP table: `dp = [1, 1, 2, 3]`.

**Result:** `3` ✅ (`2 2 6`, `22 6`, `2 26`)

**Second dry run — zeros:** `s = "11106"` (from the statement's explanation), `n = 5`.

Start: `dp[0] = 1`, `dp[1] = 1`.

| `i` | `s[i-1]` | +dp[i-1]? | `s[i-2:i]` | +dp[i-2]? | dp[i] |
|---|---|---|---|---|---|
| 2 | `'1'` | +1 | `"11"` ✓ | +1 | 2 |
| 3 | `'1'` | +2 | `"11"` ✓ | +1 | 3 |
| 4 | `'0'` | no (`'0'` alone) | `"10"` ✓ | +2 (dp[2]) | 2 |
| 5 | `'6'` | +2 | `"06"` ✗ (leading zero) | no | **2** |

**Result:** `2` ✅ (`1 1 10 6` and `11 10 6`). Notice how the `'0'` at index 3 forces the `"10"` piece: `dp[4]` comes *only* from `dp[2]`.

**Third check:** `s = "06"` → `dp[1] = 0` (`'0'` alone is invalid); at `i = 2`: `'6'` adds `dp[1] = 0`, `"06"` is invalid → `dp[2] = 0` ✅.

---

## 9. Concepts, Data Structures, and Patterns

- **DP recipe:** state `dp[i]` = ways to decode the first `i` characters; recurrence = sum over the two possible last pieces; base `dp[0] = 1`; left-to-right; answer `dp[n]`.
- **Counting DP:** we **add** the counts of the cases (instead of taking a `max`) because different last pieces give different decodings — the cases never overlap.
- **The empty-prefix base case (`dp[0] = 1`):** a standard trick in counting DPs ("one way to make nothing").
- **Fibonacci connection:** for a string of only `1`s, both pieces are always valid, so `dp[i] = dp[i-1] + dp[i-2]` — exactly Fibonacci. Compare [055_climbing_stairs.md](055_climbing_stairs.md) (steps of size 1 or 2).
- **Validity checks as "gates":** each term is added only when its piece is valid. Zeros close the one-digit gate; numbers outside `10..26` close the two-digit gate.
- **String slicing:** `s[i-2:i]` takes exactly two characters; `int()` converts it.
- **Related:** [059_word_break_problem.md](059_word_break_problem.md) — "can the prefix be split into valid pieces?" (a yes/no version of the same prefix DP); Decode Ways II (LeetCode 639) adds a `'*'` wildcard.

---

## 10. Complexity Analysis

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Plain recursion | `O(1.618^n)` (exponential) | `O(n)` | Up to two branches per character; recursion depth `n`. |
| Memoization | `O(n)` | `O(n)` | `n + 1` states, `O(1)` work each; cache + stack. |
| DP table | `O(n)` | `O(n)` | One pass, list of `n + 1` counts. |
| Rolling variables (optimized) | `O(n)` | `O(1)` | One pass; each step does an `O(1)` two-character slice and comparison. |

---

## 11. Edge Cases

| Case | Example | Expected result | Why |
|---|---|---|---|
| Single zero | `"0"` | `0` | `'0'` is not a letter. |
| Single digit | `"1"` | `1` | `A`. |
| Leading zero | `"06"` | `0` | `"06"` is not `"6"`. |
| `"10"` | `"10"` | `1` | Only `J`; `1, 0` fails because of the lone `0`. |
| `"20"` | `"20"` | `1` | Only `T`. |
| `"30"` | `"30"` | `0` | `30 > 26` and `'0'` alone is invalid. |
| Two zeros | `"100"` | `0` | The second `0` can't be alone and `"00"` is invalid. |
| Zero in the middle | `"101"` | `1` | `10, 1` only. |
| Just above 26 | `"27"` | `1` | Only `2, 7`. |
| Exactly 26 | `"26"` | `2` | `2, 6` and `26`. |
| `"2101"` | `"2101"` | `1` | `2, 10, 1` only (`21, 0, …` fails). |
| All ones | `"1111"` | `5` | Fibonacci: 1, 1, 2, 3, 5. |

---

## 12. Common Mistakes and Debugging

1. **Treating `"0"` as a valid single piece.** It maps to no letter. Always check `s[i-1] != '0'` before adding `dp[i-1]`.
2. **Accepting `"06"` as 6.** `int("06") == 6`, so a check like `int(two) <= 26` alone accepts it. Use `10 <= int(two) <= 26` (or check `two[0] != '0'`).
3. **Accepting `"30"`, `"40"`…** A `'0'` can only be part of `"10"` or `"20"`.
4. **`dp[0] = 0`.** Then `"12"` would return 1 instead of 2 — the "whole prefix is one piece" option needs `dp[0] = 1`.
5. **Returning early with `if s[0] == '0': return 0` but then mishandling inner zeros.** The DP handles all zeros uniformly; a special case is unnecessary.
6. **Checking two-digit validity with string comparison carelessly.** `"10" <= two <= "26"` actually works for two-character digit strings, but mixing lengths breaks it — `int()` is clearer.

**Debugging tip:** print the full `dp` list for `"11106"` and compare with the dry-run table (`[1, 1, 2, 3, 2, 2]`).

---

## 13. Practice Questions

**Q1. How many decodings does `"1111"` have? Show the DP table.**

<details><summary>Hint</summary>Every one-digit piece and every two-digit piece (`"11"`) is valid.</summary></details>

**Answer:** `dp = [1, 1, 2, 3, 5]`, so `5`: `1 1 1 1`, `11 1 1`, `1 11 1`, `1 1 11`, `11 11`.

**Q2. List every decoding as an actual letter string.**

<details><summary>Hint</summary>Same recursion as the brute force, but build strings instead of counting. Use `chr(ord('A') + code - 1)`.</summary></details>

**Answer:**

```python
def all_decodings(s):
    results = []

    def build(i, letters):
        if i == len(s):
            results.append("".join(letters))
            return
        if s[i] == "0":
            return
        letters.append(chr(ord("A") + int(s[i]) - 1))
        build(i + 1, letters)
        letters.pop()
        if i + 1 < len(s) and int(s[i:i + 2]) <= 26:
            letters.append(chr(ord("A") + int(s[i:i + 2]) - 1))
            build(i + 2, letters)
            letters.pop()

    build(0, [])
    return results


assert sorted(all_decodings("226")) == ["BBF", "BZ", "VF"]
assert sorted(all_decodings("11106")) == ["AAJF", "KJF"]
assert all_decodings("06") == []
```

**Q3. Write a small helper that says whether a two-character piece is a valid code, and test the tricky zero cases.**

<details><summary>Hint</summary>Think about which two-digit strings map to a letter: only `"10"` through `"26"`.</summary></details>

**Answer:**

```python
def valid_two(piece):
    return 10 <= int(piece) <= 26


def valid_one(piece):
    return piece != "0"


assert valid_two("10") and valid_two("20") and valid_two("26")
assert not valid_two("06") and not valid_two("30") and not valid_two("27")
assert not valid_one("0") and valid_one("9")
```

**Q4. Can the answer be 0 when `s` contains no `'0'` at all?**

<details><summary>Hint</summary>Look at which characters are allowed.</summary></details>

**Answer:** It can't. If `s` has no `'0'`, every character is `1..9`, so splitting into single digits always works — the answer is at least 1. A result of 0 always comes from a `'0'` that is not preceded by `'1'` or `'2'` (like `"30"`, `"00"`, or a leading `"0"`).

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** 1-D counting DP over prefixes (Fibonacci with gates).
- **State:** `dp[i]` = decodings of `s[0:i]`; `dp[0] = 1`.
- **Recurrence:** `dp[i] = [s[i-1] != '0'] · dp[i-1] + [10 <= int(s[i-2:i]) <= 26] · dp[i-2]`.
- **Zeros:** `"0"` alone ✗, `"06"` ✗, `"10"`/`"20"` ✓, `"30"`+ ✗.
- **Time:** `O(n)`. **Auxiliary space:** `O(1)`.
- **One-line memory hook:** *"The last piece is one or two digits — add the ways for whatever is left, if the piece is a real letter."*

### Completion checklist

- [x] Problem requirements verified
- [x] Examples and constraints verified (including the 32-bit answer guarantee)
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force (recursion) and memoized solutions written and tested
- [x] Optimized Python solution (rolling variables) and DP-table version written and tested (`tools/tests/p063.py`)
- [x] Line-by-line explanation written
- [x] Dry run completed with real examples
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
