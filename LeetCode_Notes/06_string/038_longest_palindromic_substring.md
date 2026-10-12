# 038. Longest Palindromic Substring

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Longest Palindromic Substring |
| **LeetCode number** | 5 |
| **Topic (source list)** | String |
| **Also uses** | Two Pointers, Dynamic Programming |
| **Difficulty** | Medium |
| **LeetCode URL** | <https://leetcode.com/problems/longest-palindromic-substring/> |
| **Pattern** | Expand around center |

---

## 2. Problem Explanation

### What are we given?

`s` — a non-empty string made of digits and English letters.

### What must we return?

The **longest substring of `s` that is a palindrome**, as a string.

- A **substring** is a block of characters that sit next to each other in `s` (no skipping). In `"babad"`, `"bab"` is a substring but `"bbd"` is not.
- A **palindrome** reads the same forwards and backwards, e.g. `"aba"`, `"bb"`, `"a"`.
- Comparison is **exact**: uppercase and lowercase letters are different characters here (`"Aa"` is *not* a palindrome).
- If several palindromic substrings share the maximum length, **any one of them** is accepted.
- Every single character is a palindrome, so there is always an answer of length at least 1.

### Examples

**Example 1**

```text
Input:  s = "babad"
Output: "bab"
```

`"aba"` is also a correct answer — both have length 3, and no palindrome of length 4 or 5 exists in `"babad"`.

**Example 2**

```text
Input:  s = "cbbd"
Output: "bb"
```

`"bb"` (positions 1–2) is the only palindrome longer than one character.

### Constraints

- `1 <= s.length <= 1000`
- `s` consist of only digits and English letters.

There is no official follow-up.

---

## 3. Everyday Analogy

> **Explain it like I'm five**

Think of a palindrome like a butterfly: the left wing is a mirror image of the right wing, and there is a **body in the middle**.

To find the biggest butterfly hidden in a row of letters, stand on each spot and pretend it is the body. Then open your arms one step at a time: look one letter to the left and one to the right. If they are the same, the wings can grow — open your arms another step. As soon as the two letters differ (or you run out of letters), the wings stop growing. Measure that butterfly.

Some butterflies have a body that is **two identical letters** wide (like `"abba"`, whose middle is `"bb"`), so you also try standing *between* every pair of neighbours.

After trying every possible body, the biggest butterfly you measured is the answer.

---

## 4. Step-by-Step Logic

1. **Brute idea:** list every substring, check whether it is a palindrome, keep the longest. There are about `n²/2` substrings and each check costs up to `n`, so `O(n³)` — too slow for `n = 1000`.
2. **Key observation:** every palindrome has a **center**. Shrinking a palindrome by removing its first and last characters still leaves a palindrome around the same center. So, starting from a center, we can grow outward while the two ends match, and we know exactly when it stops being a palindrome.
3. **How many centers?**
   - **Odd length** palindromes (`"aba"`) are centered **on** a character → `n` centers.
   - **Even length** palindromes (`"abba"`) are centered **between** two characters → `n - 1` centers.
   - So `2n - 1` centers in total.
4. **Expand:** from a center `(left, right)`, while `left >= 0`, `right < n` and `s[left] == s[right]`, move `left` one step left and `right` one step right. When it stops, the palindrome is `s[left + 1 : right]` (the last pair that *did* match).
5. **Track the best:** remember the start and end of the longest palindrome found.
6. **Cost:** each expansion is at most `O(n)`, there are `O(n)` centers → `O(n²)` time, but only `O(1)` extra memory — much better than `O(n³)`.

---

## 5. Brute-Force Solution

### Algorithm

1. For every start index `i` and every end index `j >= i`:
2. Take the substring `s[i : j + 1]`; if it equals its reverse and is longer than the best so far, remember it.
3. Return the best substring.

### Python code

```python
class Solution:
    def longestPalindrome(self, s: str) -> str:
        n = len(s)
        best = s[0]                      # any single character is a palindrome
        for i in range(n):
            for j in range(i + len(best), n):   # only lengths that could beat best
                candidate = s[i:j + 1]
                if candidate == candidate[::-1]:
                    best = candidate
        return best
```

### Explanation

- `best` starts as the first character, which is always a valid answer of length 1.
- The inner loop starts at `j = i + len(best)`, so every candidate has length `len(best) + 1` or more — we never waste time on substrings that couldn't beat the current best. Because `j` grows, any palindrome found is automatically longer than `best`.
- `candidate == candidate[::-1]` checks the palindrome property by comparing with the reversed copy.

### Complexity

- **Time:** `O(n³)` in the worst case — `O(n²)` substrings, and slicing plus reversing each one costs up to `O(n)`. For `n = 1000` that is on the order of `10^8` character operations, which is **too slow for LeetCode's limits in Python** (it is likely to time out). It is correct and useful as a reference.
- **Auxiliary space:** `O(n)` for the temporary substring and its reverse.

---

## 6. Optimized Solution

### Idea — expand around center

Try all `2n - 1` centers (each character, and each gap between neighbours). From each center, grow outward while the characters on both sides match. Keep the longest.

### Algorithm

1. Write a helper `expand(left, right)` that grows while `s[left] == s[right]` and returns the bounds `(left + 1, right - 1)` of the palindrome it found.
2. For each index `i`:
   - Odd-length: `expand(i, i)`.
   - Even-length: `expand(i, i + 1)`.
   - If either result is longer than the best, store it.
3. Return `s[start : end + 1]`.

### Python code (LeetCode-ready)

```python
class Solution:
    def longestPalindrome(self, s: str) -> str:
        n = len(s)

        def expand(left: int, right: int) -> tuple:
            # Grow while both ends exist and match.
            while left >= 0 and right < n and s[left] == s[right]:
                left -= 1
                right += 1
            # The loop overshot by one step on each side.
            return left + 1, right - 1

        start, end = 0, 0          # bounds (inclusive) of the best palindrome
        for i in range(n):
            for lo, hi in (expand(i, i), expand(i, i + 1)):   # odd, even
                if hi - lo > end - start:
                    start, end = lo, hi

        return s[start:end + 1]
```

### Alternative — dynamic programming table (`O(n²)` time, `O(n²)` space)

`is_pal[i][j]` is `True` when `s[i..j]` is a palindrome. A substring is a palindrome when its two end characters match **and** the inside is a palindrome (or the inside has length 0 or 1).

```python
class Solution:
    def longestPalindrome(self, s: str) -> str:
        n = len(s)
        is_pal = [[False] * n for _ in range(n)]
        start, best_len = 0, 1

        # Fill by increasing i from the right so is_pal[i + 1][j - 1] is ready.
        for i in range(n - 1, -1, -1):
            for j in range(i, n):
                if s[i] == s[j] and (j - i < 2 or is_pal[i + 1][j - 1]):
                    is_pal[i][j] = True
                    if j - i + 1 > best_len:
                        start, best_len = i, j - i + 1

        return s[start:start + best_len]
```

This is correct and avoids the `O(n³)` of the brute force, but the table needs `n² = 10^6` booleans for `n = 1000`, so the center-expansion version is preferred.

### Advanced — Manacher's algorithm (`O(n)`)

Manacher's algorithm reuses the mirror symmetry of palindromes already found so that each center does not have to restart expanding from scratch. It finds the longest palindromic substring in `O(n)` time and `O(n)` space. It is rarely expected in interviews and is not implemented in these notes; with `n <= 1000`, the `O(n²)` center expansion is fast enough.

---

## 7. Line-by-Line Explanation

(Expand-around-center version)

| Line | What it does | Why |
|---|---|---|
| `n = len(s)` | Stores the length. | Used for the bounds check in `expand`. |
| `def expand(left, right):` | Helper that grows a palindrome from a center. | The same logic serves odd centers `(i, i)` and even centers `(i, i + 1)`. |
| `while left >= 0 and right < n and s[left] == s[right]:` | Keeps growing while both pointers are inside the string and the characters match. | The bounds checks come **first** so we never index outside the string. |
| `left -= 1; right += 1` | Widens the window by one character on each side. | Tries the next bigger palindrome around the same center. |
| `return left + 1, right - 1` | Returns the last bounds that matched. | The loop stopped one step *past* the palindrome. For an even center that fails immediately (`s[i] != s[i+1]`), this returns `(i + 1, i)`, i.e. length 0. |
| `start, end = 0, 0` | Best palindrome so far is `s[0]`. | Every string has at least one character, which is a palindrome. |
| `for i in range(n):` | Visits every character as a potential center. | — |
| `for lo, hi in (expand(i, i), expand(i, i + 1)):` | Tries the odd center on `i` and the even center between `i` and `i + 1`. | Covers all `2n - 1` centers. When `i = n - 1`, `expand(i, i + 1)` stops at once because `right = n` is out of range. |
| `if hi - lo > end - start:` | Compares lengths (`hi - lo + 1` vs `end - start + 1`; the `+1`s cancel). | Strict `>` keeps the **first** longest palindrome found. |
| `return s[start:end + 1]` | Slices the answer. | `end` is inclusive, Python slices are exclusive at the end. |

---

## 8. Dry Run

**Input:** `s = "babad"` (Example 1). Indices: `b0 a1 b2 a3 d4`.

| `i` | Center | Matching pairs while expanding | Returned `(lo, hi)` | Palindrome | Best after this step |
|---|---|---|---|---|---|
| 0 | odd `(0,0)` | `(0,0)` b=b; next `(-1,1)` out of range | `(0, 0)` | `"b"` | `"b"` |
| 0 | even `(0,1)` | `b ≠ a` → none | `(1, 0)` | `""` | `"b"` |
| 1 | odd `(1,1)` | `(1,1)` a=a; `(0,2)` b=b; next `(-1,3)` out of range | `(0, 2)` | `"bab"` | **`"bab"`** (3 > 1) |
| 1 | even `(1,2)` | `a ≠ b` → none | `(2, 1)` | `""` | `"bab"` |
| 2 | odd `(2,2)` | `(2,2)` b=b; `(1,3)` a=a; `(0,4)` b ≠ d → stop | `(1, 3)` | `"aba"` | `"bab"` (3 is not > 3) |
| 2 | even `(2,3)` | `b ≠ a` → none | `(3, 2)` | `""` | `"bab"` |
| 3 | odd `(3,3)` | `(3,3)` a=a; `(2,4)` b ≠ d → stop | `(3, 3)` | `"a"` | `"bab"` |
| 3 | even `(3,4)` | `a ≠ d` → none | `(4, 3)` | `""` | `"bab"` |
| 4 | odd `(4,4)` | `(4,4)` d=d; next `(3,5)` out of range | `(4, 4)` | `"d"` | `"bab"` |
| 4 | even `(4,5)` | `right = 5` out of range → none | `(5, 4)` | `""` | `"bab"` |

**Result:** `"bab"` ✅ (`"aba"` was found too, but the strict `>` keeps the first one; both are accepted).

**Second dry run:** `s = "cbbd"` (Example 2)

| `i` | Center | What happens | Palindrome | Best |
|---|---|---|---|---|
| 0 | odd / even | `"c"`; `c ≠ b` | `"c"` | `"c"` |
| 1 | odd `(1,1)` | `(1,1)` b=b; `(0,2)` c ≠ b | `"b"` | `"c"` |
| 1 | even `(1,2)` | `(1,2)` b=b; `(0,3)` c ≠ d → stop | `"bb"` | **`"bb"`** |
| 2 | odd / even | `"b"`; `b ≠ d` | `"b"` | `"bb"` |
| 3 | odd / even | `"d"`; out of range | `"d"` | `"bb"` |

**Result:** `"bb"` ✅ — only the even center between the two `b`s finds it, which is why both center types are needed.

---

## 9. Concepts, Data Structures, and Patterns

- **Palindromes have centers:** odd palindromes center on a character, even ones between two characters → `2n - 1` centers.
- **Expand around center (two pointers moving outward):** the mirror image of the inward two pointers used in [037_valid_palindrome.md](037_valid_palindrome.md).
- **Dynamic programming on intervals:** `is_pal[i][j]` depends on `is_pal[i + 1][j - 1]` (a shorter interval). Interval DP also appears in many substring/subsequence problems; compare with [058_longest_common_subsequence.md](../08_dynamic_programming/058_longest_common_subsequence.md).
- **Inclusive vs exclusive bounds:** we store inclusive `(start, end)` and slice with `end + 1`.
- **Manacher's algorithm:** the `O(n)` specialist algorithm for palindromic substrings (mentioned, not required).
- **Related notes:** [039_palindromic_substrings.md](039_palindromic_substrings.md) uses the *same* center expansion but **counts** palindromes instead of keeping the longest.

---

## 10. Complexity Analysis

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Brute force | `O(n³)` | `O(n)` | `O(n²)` substrings × `O(n)` to slice and reverse each. Too slow for `n = 1000` in Python. |
| Expand around center (optimized) | `O(n²)` | `O(1)` | `2n - 1` centers; each expansion takes at most `O(n)` steps. Worst case is a string like `"aaaa…a"`, where every center expands to the edge — about `n²/2` steps in total. Only a few integers are stored (the final slice is the output, not extra working memory). |
| DP table | `O(n²)` | `O(n²)` | One `O(1)` check per pair `(i, j)`, but the `n × n` table must be stored. |
| Manacher (not implemented) | `O(n)` | `O(n)` | Reuses mirrored information so total expansion work is linear. |

---

## 11. Edge Cases

| Case | Example | Expected result | Why |
|---|---|---|---|
| Single character | `"a"` | `"a"` | The only substring. |
| No repeated neighbours | `"ac"` | `"a"` or `"c"` | Only single characters are palindromes; any is accepted (the code returns `"a"`). |
| All the same character | `"aaaa"` | `"aaaa"` | The whole string; found by the even center between indices 1 and 2. |
| Whole string is a palindrome | `"racecar"` | `"racecar"` | Found by the odd center at index 3. |
| Even-length answer | `"cbbd"` | `"bb"` | Needs the even center. |
| Case matters | `"aAa"` | `"aAa"` | `a` = `a` on both sides; the center `A` matches itself. But `"Aa"` would give `"A"` or `"a"`. |
| Answer at the end | `"abb"` | `"bb"` | Even center at `(1, 2)`. |
| Tie between two palindromes | `"babad"` | `"bab"` or `"aba"` | Either is accepted. |

---

## 12. Common Mistakes and Debugging

1. **Forgetting even-length centers.** Only calling `expand(i, i)` returns `"c"` instead of `"bb"` for `"cbbd"`.
2. **Off-by-one after expanding.** The loop exits *after* a failed step, so the palindrome is `s[left + 1 : right]`, not `s[left : right + 1]`.
3. **Checking `s[left] == s[right]` before the bounds.** `s[-1]` is valid Python (the last character!), so a missing `left >= 0` check silently compares with the wrong character instead of crashing. Always test the bounds first.
4. **Confusing substring with subsequence.** Longest Palindromic *Subsequence* (LeetCode 516) may skip characters and needs a different DP (see Practice Q3).
5. **Testing against one fixed answer.** When several longest palindromes exist, any one is correct; tests should check *length* and *palindrome-ness*, not one exact string.

**Debugging tip:** inside the main loop print `i, lo, hi, s[lo:hi + 1]` and compare with the dry-run table.

---

## 13. Practice Questions

**Q1. For `s = "aaaa"`, which center first produces the final answer, and what are its bounds?**

<details><summary>Hint</summary>Odd centers can only produce odd lengths. Go through `i = 0, 1, …` and watch when length 4 first appears.</summary></details>

**Answer:** `i = 0`: odd gives `"a"` (1), even `(0,1)` gives `"aa"` (2). `i = 1`: odd `(1,1)` gives `"aaa"` (0..2, length 3), even `(1,2)` expands `(1,2)` → `(0,3)` → `(-1,4)` out of range, so it returns `(0, 3)` = `"aaaa"` (length 4). The **even center between indices 1 and 2** produces the answer with bounds `(0, 3)`.

**Q2. Return only the *length* of the longest palindromic substring.**

<details><summary>Hint</summary>Have `expand` return `right - left - 1` (the length) instead of the bounds.</summary></details>

**Answer:** After the loop stops, the palindrome spans `left + 1 .. right - 1`, whose length is `(right - 1) - (left + 1) + 1 = right - left - 1`.

```python
def longest_palindrome_length(s):
    n = len(s)

    def expand(left, right):
        while left >= 0 and right < n and s[left] == s[right]:
            left -= 1
            right += 1
        return right - left - 1

    return max(max(expand(i, i), expand(i, i + 1)) for i in range(n))


assert longest_palindrome_length("babad") == 3
assert longest_palindrome_length("cbbd") == 2
assert longest_palindrome_length("a") == 1
```

**Q3. Longest Palindromic *Subsequence* (LeetCode 516): characters may be skipped. Return its length.**

<details><summary>Hint</summary>`dp[i][j]` = answer for `s[i..j]`. If `s[i] == s[j]`, use both ends: `dp[i+1][j-1] + 2`; otherwise drop one end: `max(dp[i+1][j], dp[i][j-1])`.</summary></details>

**Answer:** Fill `i` from right to left so the shorter intervals are ready.

```python
def longest_palindromic_subsequence(s):
    n = len(s)
    dp = [[0] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        dp[i][i] = 1
        for j in range(i + 1, n):
            if s[i] == s[j]:
                dp[i][j] = dp[i + 1][j - 1] + 2   # inner part is 0 when j == i + 1
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])
    return dp[0][n - 1]


assert longest_palindromic_subsequence("bbbab") == 4   # "bbbb"
assert longest_palindromic_subsequence("cbbd") == 2    # "bb"
assert longest_palindromic_subsequence("babad") == 3
```

`O(n²)` time and space. Note the difference: the longest palindromic *substring* of `"bbbab"` is `"bbb"` (length 3), but the longest *subsequence* is `"bbbb"` (length 4).

**Q4. Why is the worst case of center expansion `O(n²)` and not `O(n)`? Give a worst-case input.**

<details><summary>Hint</summary>How far does each center expand on a string where every character is the same?</summary></details>

**Answer:** In `"aaaa…a"` (length `n`) the center at position `k` expands until it hits the nearer edge, about `min(k, n - k)` steps. Summing over all centers gives roughly `n²/4` steps per center type → `O(n²)`. Manacher's algorithm avoids this by reusing the mirrored lengths.

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** Expand around center (`2n - 1` centers: on each character and between neighbours).
- **Key idea:** From each center, grow while `s[left] == s[right]`; the palindrome is `s[left + 1 : right]`; keep the longest.
- **Time:** `O(n²)`.
- **Auxiliary space:** `O(1)` (DP alternative: `O(n²)`; Manacher: `O(n)` time).
- **One-line memory hook:** *"Every butterfly has a body — try every body, one or two letters wide, and open the wings."*

### Completion checklist

- [x] Problem requirements verified
- [x] Examples and constraints verified against the official statement
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force solution written and tested
- [x] Optimized Python solution written and tested (`tools/tests/p038.py`), plus the DP alternative
- [x] Line-by-line explanation written
- [x] Dry run completed with real examples
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
> Note: Manacher's algorithm (O(n)) is described earlier in this note for reference only; it is not implemented or tested here.
