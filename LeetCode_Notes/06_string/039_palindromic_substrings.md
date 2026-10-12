# 039. Palindromic Substrings

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Palindromic Substrings |
| **LeetCode number** | 647 |
| **Topic (source list)** | String |
| **Also uses** | Two Pointers, Dynamic Programming |
| **Difficulty** | Medium |
| **LeetCode URL** | <https://leetcode.com/problems/palindromic-substrings/> |
| **Pattern** | Expand around center (counting version) |

---

## 2. Problem Explanation

### What are we given?

`s` — a non-empty string of lowercase English letters.

### What must we return?

An integer: **how many substrings of `s` are palindromes**.

- A **substring** is a run of neighbouring characters (no skipping), with at least one character.
- A **palindrome** reads the same forwards and backwards.
- Substrings are counted **by position**, not by content. In `"aaa"`, the three single `"a"`s at positions 0, 1 and 2 are three different substrings, even though they look identical.

### Examples

**Example 1**

```text
Input:  s = "abc"
Output: 3
```

The palindromic substrings are `"a"`, `"b"` and `"c"`. Longer ones like `"ab"` or `"abc"` are not palindromes.

**Example 2**

```text
Input:  s = "aaa"
Output: 6
```

The six palindromic substrings are `"a"`, `"a"`, `"a"` (one per position), `"aa"`, `"aa"` (positions 0–1 and 1–2) and `"aaa"`.

### Constraints

- `1 <= s.length <= 1000`
- `s` consists of lowercase English letters.

There is no official follow-up.

---

## 3. Everyday Analogy

> **Explain it like I'm five**

This is the butterfly game from [038_longest_palindromic_substring.md](038_longest_palindromic_substring.md), but now instead of looking for the **biggest** butterfly, you are **counting all** the butterflies.

Stand on each letter (or between two neighbouring letters) and call it the butterfly's body. Open your arms one step at a time. **Every time** the letters under your two hands match, you have found one more butterfly — put a sticker on your chart. When the letters stop matching, no bigger butterfly can grow from that body, so move on to the next body.

At the end, count the stickers.

---

## 4. Step-by-Step Logic

1. **Brute idea:** check all `n(n+1)/2` substrings one by one → `O(n³)` because each check is `O(n)`.
2. **Every palindrome has a unique center.** An odd-length palindrome is centered on a character, an even-length one on the gap between two characters. So there are `2n - 1` possible centers, and every palindromic substring belongs to exactly **one** of them. Counting per center therefore counts each palindrome exactly once.
3. **Growing from a center:** if `s[l..r]` is a palindrome and `s[l-1] == s[r+1]`, then `s[l-1..r+1]` is also a palindrome. If they differ, **no** larger palindrome around this center exists (its inner part would already fail).
4. **So for each center:** expand while the ends match, adding 1 to the count for every successful step. Stop at the first mismatch or at the edge of the string.
5. **Total work:** `2n - 1` centers × at most `O(n)` expansion each → `O(n²)` time, `O(1)` extra space.

---

## 5. Brute-Force Solution

### Algorithm

1. For every start `i` and every end `j >= i`, take `s[i : j + 1]`.
2. If it equals its reverse, add 1 to the count.

### Python code

```python
class Solution:
    def countSubstrings(self, s: str) -> int:
        n = len(s)
        count = 0
        for i in range(n):
            for j in range(i, n):
                sub = s[i:j + 1]
                if sub == sub[::-1]:
                    count += 1
        return count
```

### Explanation

- The two loops generate every substring exactly once (by position).
- `sub[::-1]` is the reversed substring; equality means it is a palindrome.

### Complexity

- **Time:** `O(n³)` — `n(n+1)/2 ≈ 500,000` substrings for `n = 1000`, each sliced and reversed in up to `O(n)`. That is on the order of `10^8` character operations: **too slow for LeetCode's limits in Python** (it is likely to time out), though correct.
- **Auxiliary space:** `O(n)` for the temporary substring and its reverse.

---

## 6. Optimized Solution

### Idea — expand around center and count

For each of the `2n - 1` centers, expand outward; every matching step is one more palindrome.

### Algorithm

1. `count = 0`.
2. For each index `i`:
   - Expand from `(i, i)` (odd lengths) and from `(i, i + 1)` (even lengths).
   - While `left >= 0`, `right < n` and `s[left] == s[right]`: add 1 to `count`, then move `left -= 1`, `right += 1`.
3. Return `count`.

### Python code (LeetCode-ready)

```python
class Solution:
    def countSubstrings(self, s: str) -> int:
        n = len(s)
        count = 0

        for center in range(2 * n - 1):
            # Even "center" values sit on a character, odd ones between two.
            left = center // 2
            right = left + center % 2
            while left >= 0 and right < n and s[left] == s[right]:
                count += 1          # s[left..right] is a palindrome
                left -= 1
                right += 1

        return count
```

How the single loop covers both center types (for `n = 3`):

```text
center: 0      1      2      3      4
left:   0      0      1      1      2
right:  0      1      1      2      2
type:   odd    even   odd    even   odd
```

### Alternative — dynamic programming table (`O(n²)` time and space)

```python
class Solution:
    def countSubstrings(self, s: str) -> int:
        n = len(s)
        is_pal = [[False] * n for _ in range(n)]
        count = 0
        for i in range(n - 1, -1, -1):          # start, right to left
            for j in range(i, n):               # end
                # Ends match, and the inside (if any) is a palindrome.
                if s[i] == s[j] and (j - i < 2 or is_pal[i + 1][j - 1]):
                    is_pal[i][j] = True
                    count += 1
        return count
```

`is_pal[i + 1][j - 1]` is always computed before `is_pal[i][j]` because row `i + 1` is filled before row `i`. This is correct but stores an `n × n` table.

**Advanced note:** Manacher's algorithm can compute the palindrome radius at every center in `O(n)` time; summing those radii gives the count in `O(n)`. It is not needed for `n <= 1000` and is not implemented here.

---

## 7. Line-by-Line Explanation

(Expand-around-center version)

| Line | What it does | Why |
|---|---|---|
| `n = len(s)` | Stores the length. | Used for the bounds and the number of centers. |
| `count = 0` | Running total. | — |
| `for center in range(2 * n - 1):` | Visits every possible center exactly once. | `n` character centers + `n - 1` gap centers = `2n - 1`. |
| `left = center // 2` | Left starting index. | Pairs of center values share the same `left` (see the table above). |
| `right = left + center % 2` | Right starting index: same as `left` for odd-length centers, `left + 1` for even-length. | `center % 2` is 0 or 1. |
| `while left >= 0 and right < n and s[left] == s[right]:` | Keeps expanding while inside the string and the ends match. | Bounds first, so no out-of-range (or wrapped `s[-1]`) access. |
| `count += 1` | Counts `s[left..right]`. | Every successful step is a new, distinct palindromic substring. |
| `left -= 1; right += 1` | Widens by one character on each side. | Tries the next larger palindrome with the same center. |
| `return count` | Total over all centers. | Each palindrome has exactly one center, so nothing is double-counted. |

---

## 8. Dry Run

**Input:** `s = "aaa"` (Example 2). `n = 3`, centers `0..4`.

| `center` | Start `(left, right)` | Expansion steps | Palindromes counted | `count` after |
|---|---|---|---|---|
| 0 | `(0, 0)` | `(0,0)` a=a ✓ → `(-1,1)` out of range | `"a"`₀ | 1 |
| 1 | `(0, 1)` | `(0,1)` a=a ✓ → `(-1,2)` out of range | `"aa"`₀₋₁ | 2 |
| 2 | `(1, 1)` | `(1,1)` ✓ → `(0,2)` a=a ✓ → `(-1,3)` out | `"a"`₁, `"aaa"` | 4 |
| 3 | `(1, 2)` | `(1,2)` ✓ → `(0,3)` out of range | `"aa"`₁₋₂ | 5 |
| 4 | `(2, 2)` | `(2,2)` ✓ → `(1,3)` out of range | `"a"`₂ | 6 |

**Result:** `6` ✅ — exactly the six substrings listed in the official explanation.

**Second dry run:** `s = "abc"` (Example 1)

| `center` | Start | What happens | `count` after |
|---|---|---|---|
| 0 | `(0,0)` | `a` ✓, then out of range | 1 |
| 1 | `(0,1)` | `a ≠ b` → nothing | 1 |
| 2 | `(1,1)` | `b` ✓, then `(0,2)`: `a ≠ c` → stop | 2 |
| 3 | `(1,2)` | `b ≠ c` → nothing | 2 |
| 4 | `(2,2)` | `c` ✓, then `(1,3)` out of range | 3 |

**Result:** `3` ✅

---

## 9. Concepts, Data Structures, and Patterns

- **Expand around center:** identical machinery to [038_longest_palindromic_substring.md](038_longest_palindromic_substring.md); there we keep the **longest**, here we **count** every step.
- **Unique-center argument:** each palindromic substring has exactly one center, which is why counting per center neither misses nor double-counts.
- **Index trick `center // 2`, `center % 2`:** folds both odd and even centers into a single loop of `2n - 1` iterations.
- **Interval DP:** `is_pal[i][j]` from `is_pal[i + 1][j - 1]` (smaller interval inside). Fill order matters: `i` from right to left.
- **Counting by position:** equal-looking substrings at different positions count separately — so no set/deduplication is needed.
- **Related notes:** [037_valid_palindrome.md](037_valid_palindrome.md) (inward two pointers for one palindrome check); [058_longest_common_subsequence.md](../08_dynamic_programming/058_longest_common_subsequence.md) for another two-index string DP table.

---

## 10. Complexity Analysis

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Brute force | `O(n³)` | `O(n)` | `O(n²)` substrings, each sliced and reversed in `O(n)`. |
| Expand around center (optimized) | `O(n²)` | `O(1)` | `2n - 1` centers, each expanding at most `O(n)` steps. Worst case `"aaa…a"`: every substring is a palindrome, the answer itself is `n(n+1)/2`, and every one of those is one loop step. Only a few integers are stored. |
| DP table | `O(n²)` | `O(n²)` | One `O(1)` check per pair `(i, j)`; the `n × n` boolean table dominates memory. |
| Manacher (not implemented) | `O(n)` | `O(n)` | Linear-time palindrome radii. |

**Note:** the expansion cost is proportional to `n + (number of palindromic substrings)`, so it is fast on strings with few palindromes and reaches `O(n²)` only when the answer itself is about `n²/2`.

---

## 11. Edge Cases

| Case | Example | Expected result | Why |
|---|---|---|---|
| Single character | `"a"` | `1` | Just `"a"`. |
| Two equal letters | `"aa"` | `3` | `"a"`, `"a"`, `"aa"`. |
| Two different letters | `"ab"` | `2` | Only the single letters. |
| Odd palindrome | `"aba"` | `4` | `"a"`, `"b"`, `"a"`, `"aba"`. |
| Even palindrome | `"abba"` | `6` | 4 singles + `"bb"` + `"abba"`. |
| All the same | `"aaaa"` | `10` | Every substring: `4·5/2 = 10`. |
| Maximum, all same | `"a" * 1000` | `500500` | `1000·1001/2`. |
| All different | `"abc"` | `3` | Only singles (official Example 1). |

---

## 12. Common Mistakes and Debugging

1. **Only odd centers.** Skipping even centers misses `"aa"`, `"bb"`, `"abba"`, … → `"aaa"` would give 4 instead of 6.
2. **Counting distinct strings.** Using a set of palindromes gives 3 for `"aaa"` (`"a"`, `"aa"`, `"aaa"`), but positions matter → 6.
3. **Counting after the loop instead of inside it.** Adding 1 per center (instead of per successful step) only counts one palindrome per center.
4. **Wrong DP fill order.** Filling `i` from left to right reads `is_pal[i + 1][j - 1]` before it has been computed.
5. **Bounds checked after indexing.** `s[left] == s[right]` with `left = -1` silently compares with the last character in Python; check `left >= 0` first.

**Debugging tip:** print `center, left, right, count` inside the `while` loop and compare with the dry-run table.

---

## 13. Practice Questions

**Q1. How many palindromic substrings does `"abba"` have, and which centers produce them?**

<details><summary>Hint</summary>Run the 7 centers (`2·4 - 1`). Only one even center expands more than once.</summary></details>

**Answer:** `6`. The four odd centers each give one single letter (`a`, `b`, `b`, `a`) — the center on index 1 tries `(0,2)` = `a` vs `b` and stops, likewise index 2. The even center between indices 1 and 2 gives `"bb"` and then `(0,3)` = `a` = `a` gives `"abba"`. The even centers `(0,1)` and `(2,3)` give nothing. Total `4 + 2 = 6`.

**Q2. Count only the palindromic substrings of length at least 2.**

<details><summary>Hint</summary>Every single character is a palindrome, so how many does the original count include that you must remove?</summary></details>

**Answer:** Subtract the `n` single-letter palindromes from the full count.

```python
def count_long_palindromes(s):
    n = len(s)
    count = 0
    for center in range(2 * n - 1):
        left = center // 2
        right = left + center % 2
        while left >= 0 and right < n and s[left] == s[right]:
            count += 1
            left -= 1
            right += 1
    return count - n


assert count_long_palindromes("aaa") == 3     # "aa", "aa", "aaa"
assert count_long_palindromes("abc") == 0
assert count_long_palindromes("abba") == 2    # "bb", "abba"
```

**Q3. Count the *distinct* palindromic substrings (as strings).**

<details><summary>Hint</summary>Same expansion, but put each palindrome into a set instead of incrementing a counter.</summary></details>

**Answer:** Storing the strings costs extra memory (up to `O(n²)` strings), but the idea is the same.

```python
def count_distinct_palindromes(s):
    n = len(s)
    found = set()
    for center in range(2 * n - 1):
        left = center // 2
        right = left + center % 2
        while left >= 0 and right < n and s[left] == s[right]:
            found.add(s[left:right + 1])
            left -= 1
            right += 1
    return len(found)


assert count_distinct_palindromes("aaa") == 3     # "a", "aa", "aaa"
assert count_distinct_palindromes("abba") == 4    # "a", "b", "bb", "abba"
```

**Q4. Without running code: what does the optimized solution return for `"aab"`?**

<details><summary>Hint</summary>List singles first, then look for longer ones.</summary></details>

**Answer:** `4` — `"a"`, `"a"`, `"b"` and `"aa"`. `"ab"` and `"aab"` are not palindromes.

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** Expand around center, counting each successful expansion.
- **Key idea:** `2n - 1` centers (`left = c // 2`, `right = left + c % 2`); while ends match, `count += 1` and widen.
- **Time:** `O(n²)`.
- **Auxiliary space:** `O(1)` (DP alternative `O(n²)`).
- **One-line memory hook:** *"Every time the wings match, put a sticker on the chart."*

### Completion checklist

- [x] Problem requirements verified
- [x] Examples and constraints verified against the official statement
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force solution written and tested
- [x] Optimized Python solution written and tested (`tools/tests/p039.py`), plus the DP alternative
- [x] Line-by-line explanation written
- [x] Dry run completed with real examples
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
> Note: Manacher's algorithm (O(n)) is described earlier in this note for reference only; it is not implemented or tested here.
