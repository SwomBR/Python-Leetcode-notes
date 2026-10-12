# 058. Longest Common Subsequence

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Longest Common Subsequence |
| **LeetCode number** | 1143 |
| **Topic (source list)** | Dynamic Programming |
| **Also uses** | String, Recursion + memoization |
| **Difficulty** | Medium |
| **LeetCode URL** | <https://leetcode.com/problems/longest-common-subsequence/> |
| **Pattern** | 2-D DP over two prefixes ("two-string DP") |

---

## 2. Problem Explanation

### What are we given?

Two strings, `text1` and `text2`, made of lowercase English letters.

### What must we return?

The **length** of their **longest common subsequence** (LCS). If they share no characters at all, return `0`.

### Key words

- A **subsequence** of a string is what remains after deleting **zero or more** characters, **without reordering** the rest. `"ace"` is a subsequence of `"abcde"` (delete `b` and `d`); `"aec"` is not (the order changed).
- A **common subsequence** is a string that is a subsequence of **both** inputs.
- We want the **longest** such string, but we only return its **length**.

### Examples

**Example 1**

```text
Input:  text1 = "abcde", text2 = "ace"
Output: 3
```

`"ace"` is a subsequence of both strings and nothing longer is, so the answer is 3.

**Example 2**

```text
Input:  text1 = "abc", text2 = "abc"
Output: 3
```

The strings are identical, so the whole string `"abc"` is common.

**Example 3**

```text
Input:  text1 = "abc", text2 = "def"
Output: 0
```

The strings share no letter, so the only common subsequence is the empty one (length 0).

### Constraints

- `1 <= text1.length, text2.length <= 1000`
- `text1` and `text2` consist of only lowercase English characters.

There is no official follow-up for this problem.

---

## 3. Everyday Analogy

> **Explain it like I'm five**

Two friends each wrote down the list of rides they went on at a theme park, in the order they rode them. You want to know: *"What's the longest list of rides they could both say they did **in the same order**?"* They may have done extra rides in between — that's fine, we skip those.

You put your finger at the start of each list and compare the two rides:

- **Same ride?** Great — that ride is part of the shared story. Move both fingers forward.
- **Different rides?** One of them isn't in the shared story at this spot. Try two possibilities: skip the ride on list 1, or skip the ride on list 2 — and keep whichever gives the longer story.

Trying every possibility by hand takes forever, so you build a **grid**: rows are "how much of list 1 I've used", columns are "how much of list 2 I've used". Each box stores "the longest shared story so far". Every box can be filled by looking at the box to its **left**, the box **above** it, or the box **diagonally up-left**. The bottom-right box is the answer.

---

## 4. Step-by-Step Logic

Follow the DP recipe.

1. **Look at the last characters.** Compare the last character of a prefix of `text1` with the last character of a prefix of `text2`.
   - If they are **equal**, that character can end the common subsequence: answer = 1 + LCS of both prefixes without it.
   - If they **differ**, at least one of them is not the last character of the LCS, so drop one and take the better result.
2. **State definition.** `dp[i][j]` = length of the LCS of `text1[:i]` (first `i` characters) and `text2[:j]` (first `j` characters).
3. **Recurrence.**

   ```text
   if text1[i-1] == text2[j-1]:  dp[i][j] = dp[i-1][j-1] + 1
   else:                          dp[i][j] = max(dp[i-1][j], dp[i][j-1])
   ```

4. **Base cases.** `dp[0][j] = 0` and `dp[i][0] = 0` — an empty string has nothing in common with anything. Using a table of size `(m+1) × (n+1)` with an extra row/column of zeros handles this without special cases.
5. **Iteration order.** Each cell needs the cells above, to the left and diagonally up-left, so fill rows top to bottom and each row left to right.
6. **Answer location.** `dp[m][n]` (bottom-right cell), where `m = len(text1)`, `n = len(text2)`.

**Why is taking the match always safe?** If `text1[i-1] == text2[j-1]`, matching them can never be worse than skipping one of them: any common subsequence that doesn't use this match can swap its last element for this pair without getting shorter.

---

## 5. Brute-Force Solution

### Algorithm

Write the recurrence as recursion on two indices `i` (in `text1`) and `j` (in `text2`), moving forward from the start:

- If either string is used up → 0.
- If `text1[i] == text2[j]` → `1 + lcs(i+1, j+1)`.
- Otherwise → `max(lcs(i+1, j), lcs(i, j+1))`.

### Python code

```python
class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        m, n = len(text1), len(text2)

        def lcs(i: int, j: int) -> int:
            if i == m or j == n:
                return 0
            if text1[i] == text2[j]:
                return 1 + lcs(i + 1, j + 1)
            return max(lcs(i + 1, j), lcs(i, j + 1))

        return lcs(0, 0)
```

### Explanation

- Each mismatch splits into **two** recursive calls, so the call tree doubles at each level.
- The same pair `(i, j)` is reached by many different paths (for example skip-in-1-then-skip-in-2 and skip-in-2-then-skip-in-1), which is pure repeated work.

### Complexity

- **Time:** `O(2^(m+n))` in the worst case (e.g. strings with no common characters, where every call branches). With lengths up to 1000 this **times out** immediately.
- **Auxiliary space:** `O(m + n)` recursion depth.

### The bridge: memoization

There are only `(m+1) × (n+1)` distinct `(i, j)` pairs. Caching `lcs(i, j)` (e.g. `@lru_cache` on the nested function) makes each pair cost `O(1)` after its first computation → `O(m × n)` time. In Python the recursion can be up to `m + n = 2000` deep, beyond the default limit of 1000, so the bottom-up table is the safer choice.

---

## 6. Optimized Solution

### Idea — bottom-up 2-D table

Build `dp` of size `(m+1) × (n+1)` with a zero row and zero column, then fill it row by row using the recurrence.

### Algorithm

1. `dp = [[0] * (n + 1) for _ in range(m + 1)]`.
2. For `i` in `1..m`, for `j` in `1..n`:
   - if `text1[i-1] == text2[j-1]`: `dp[i][j] = dp[i-1][j-1] + 1`
   - else: `dp[i][j] = max(dp[i-1][j], dp[i][j-1])`
3. Return `dp[m][n]`.

### Python code (LeetCode-ready)

```python
class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        m, n = len(text1), len(text2)
        # dp[i][j] = LCS length of text1[:i] and text2[:j]
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if text1[i - 1] == text2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1          # use the match
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])  # skip one char

        return dp[m][n]
```

### Space-optimized version (two rows)

Each row only reads the **previous** row and the current row, so we can keep just two rows. Making the shorter string the column string gives `O(min(m, n))` extra space.

```python
class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        if len(text1) < len(text2):
            text1, text2 = text2, text1          # text2 is now the shorter one
        n = len(text2)
        prev = [0] * (n + 1)                     # row i - 1

        for ch in text1:
            cur = [0] * (n + 1)                  # row i
            for j in range(1, n + 1):
                if ch == text2[j - 1]:
                    cur[j] = prev[j - 1] + 1
                else:
                    cur[j] = max(prev[j], cur[j - 1])
            prev = cur

        return prev[n]
```

(A single 1-D array also works if you save the old diagonal value `dp[j-1]` from the previous row in a temporary variable before overwriting it.)

---

## 7. Line-by-Line Explanation

(2-D table version)

| Line | What it does | Why |
|---|---|---|
| `m, n = len(text1), len(text2)` | Stores the lengths. | Table dimensions. |
| `dp = [[0] * (n + 1) for _ in range(m + 1)]` | Creates an `(m+1) × (n+1)` grid of zeros. | Row 0 and column 0 represent empty prefixes (base case 0). A list comprehension creates **independent** rows; `[[0] * (n+1)] * (m+1)` would share one row object. |
| `for i in range(1, m + 1):` | Row `i` = first `i` characters of `text1`. | Rows top to bottom so `dp[i-1][…]` is ready. |
| `for j in range(1, n + 1):` | Column `j` = first `j` characters of `text2`. | Left to right so `dp[i][j-1]` is ready. |
| `if text1[i - 1] == text2[j - 1]:` | Compares the **last** characters of the two prefixes. | Table index `i` ↔ string index `i - 1` because of the extra zero row. |
| `dp[i][j] = dp[i - 1][j - 1] + 1` | Diagonal + 1. | Both characters join the common subsequence. |
| `dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])` | Best of "drop the `text1` character" (above) and "drop the `text2` character" (left). | One of the two last characters is not part of the LCS. |
| `return dp[m][n]` | Bottom-right cell. | It describes the full strings. |

---

## 8. Dry Run

**Input:** `text1 = "abcde"`, `text2 = "ace"` (official Example 1). `m = 5`, `n = 3`.

### The full DP table

Rows are prefixes of `text1`, columns are prefixes of `text2`. `↖+1` marks a match (diagonal + 1); other cells take `max(above, left)`.

| `dp` | `""` (j=0) | `a` (j=1) | `c` (j=2) | `e` (j=3) |
|---|---|---|---|---|
| `""` (i=0) | 0 | 0 | 0 | 0 |
| `a` (i=1) | 0 | **1** ↖+1 | 1 | 1 |
| `b` (i=2) | 0 | 1 | 1 | 1 |
| `c` (i=3) | 0 | 1 | **2** ↖+1 | 2 |
| `d` (i=4) | 0 | 1 | 2 | 2 |
| `e` (i=5) | 0 | 1 | 2 | **3** ↖+1 |

### How some cells were computed

| Cell | Characters compared | Rule | Value |
|---|---|---|---|
| `dp[1][1]` | `a` vs `a` | match → `dp[0][0] + 1 = 0 + 1` | 1 |
| `dp[1][2]` | `a` vs `c` | `max(dp[0][2], dp[1][1]) = max(0, 1)` | 1 |
| `dp[2][1]` | `b` vs `a` | `max(dp[1][1], dp[2][0]) = max(1, 0)` | 1 |
| `dp[3][2]` | `c` vs `c` | match → `dp[2][1] + 1 = 1 + 1` | 2 |
| `dp[3][3]` | `c` vs `e` | `max(dp[2][3], dp[3][2]) = max(1, 2)` | 2 |
| `dp[4][3]` | `d` vs `e` | `max(dp[3][3], dp[4][2]) = max(2, 2)` | 2 |
| `dp[5][3]` | `e` vs `e` | match → `dp[4][2] + 1 = 2 + 1` | 3 |

**Result:** `dp[5][3] = 3` ✅. The three bold diagonal steps spell out `a`, `c`, `e` → the LCS `"ace"`.

**Second dry run (no common letters):** `text1 = "abc"`, `text2 = "def"` (Example 3). No characters ever match, so every cell is `max(above, left)` of zeros → the whole table is 0 and the answer is `0` ✅.

**Two-row version on Example 1:** `prev` goes `[0,0,0,0]` → after `a`: `[0,1,1,1]` → `b`: `[0,1,1,1]` → `c`: `[0,1,2,2]` → `d`: `[0,1,2,2]` → `e`: `[0,1,2,3]`. These are exactly the table rows, and `prev[3] = 3` ✅.

---

## 9. Concepts, Data Structures, and Patterns

- **Two-string DP:** state = (prefix of string 1, prefix of string 2). The same grid shape solves Edit Distance (72), Delete Operation for Two Strings (583), Shortest Common Supersequence (1092), and Distinct Subsequences (115).
- **Padding row/column:** an extra zero row and column turn the base cases into ordinary table cells.
- **Match → diagonal, mismatch → max(up, left):** the core LCS rule worth memorising.
- **Rolling arrays:** when a row depends only on the previous row, keep two rows (or one row plus a saved diagonal) to cut space from `O(m·n)` to `O(min(m, n))`.
- **Reconstruction by backtracking:** walk from `dp[m][n]` back to `dp[0][0]` to recover the actual subsequence (practice Q1).
- **Related notes:** [Longest Increasing Subsequence](057_longest_increasing_subsequence.md) (subsequence DP on one array — LIS of `nums` equals the LCS of `nums` and its sorted, de-duplicated copy), [Word Break](059_word_break_problem.md) (prefix DP on strings), [Longest Palindromic Substring](../06_string/038_longest_palindromic_substring.md) (2-D DP on one string).

---

## 10. Complexity Analysis

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Brute-force recursion | `O(2^(m+n))` | `O(m + n)` | Each mismatch branches twice; depth at most `m + n`. |
| Memoized recursion | `O(m × n)` | `O(m × n)` | `(m+1)(n+1)` states, `O(1)` each; cache plus `O(m+n)` stack. |
| Bottom-up 2-D table (optimized) | `O(m × n)` | `O(m × n)` | One pass over the grid; at the limits that is `10^6` cells. |
| Two-row table | `O(m × n)` | `O(min(m, n))` | Same work; only two rows of length `min(m, n) + 1` are kept. |

---

## 11. Edge Cases

| Case | Example | Expected result | Why |
|---|---|---|---|
| Identical strings | `"abc"`, `"abc"` | `3` | Everything matches. |
| No common letters | `"abc"`, `"def"` | `0` | Only the empty subsequence is common. |
| Single equal characters | `"a"`, `"a"` | `1` | One match. |
| Single different characters | `"a"`, `"b"` | `0` | No match. |
| One string is a subsequence of the other | `"ace"`, `"abcde"` | `3` | Order of arguments doesn't matter. |
| Reversed order | `"abc"`, `"cba"` | `1` | Any single letter; order prevents more. |
| Repeated letters | `"aaaa"`, `"aa"` | `2` | Limited by the shorter string. |
| Few shared letters spread out | `"bsbininm"`, `"jmjkbkjkv"` | `1` | Only one letter can be matched in order. |

---

## 12. Common Mistakes and Debugging

1. **Off-by-one between table and string indices.** `dp[i][j]` talks about `text1[i-1]` and `text2[j-1]`. Comparing `text1[i]` with `text2[j]` reads the wrong characters (or crashes at `i = m`).
2. **Creating rows with `[[0] * (n+1)] * (m+1)`.** All rows are the *same* list, so writing one row overwrites them all.
3. **Adding 1 on a mismatch** or taking `max` with the diagonal on a match. Match → diagonal + 1; mismatch → `max(up, left)`.
4. **Confusing subsequence with substring.** Longest common *substring* must be contiguous and uses a different rule (reset to 0 on mismatch — see practice Q3).
5. **Overwriting the diagonal in a 1-D array.** In the single-array optimization, `dp[j-1]` already holds the **new** row's value when you reach `j`; save the old one in a variable first, or use two rows.
6. **Expecting the actual string.** The function returns only a length; reconstruct separately if needed.

**Debugging tip:** print the table for a tiny input (`"abcde"`, `"ace"`) and compare it with the dry-run grid row by row.

---

## 13. Practice Questions

**Q1. Return one actual longest common subsequence string, not just its length.**

<details><summary>Hint</summary>Build the full table, then start at `(m, n)`. On a character match go diagonally and record the character; otherwise move toward the larger of `dp[i-1][j]` and `dp[i][j-1]`. Reverse at the end.</summary></details>

**Answer:**

```python
def lcs_string(text1, text2):
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    out = []
    i, j = m, n
    while i > 0 and j > 0:
        if text1[i - 1] == text2[j - 1]:
            out.append(text1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return "".join(reversed(out))


assert lcs_string("abcde", "ace") == "ace"
assert lcs_string("abc", "abc") == "abc"
assert lcs_string("abc", "def") == ""
assert len(lcs_string("abc", "cba")) == 1
```

**Q2. Delete Operation for Two Strings (LeetCode 583): the minimum number of single-character deletions (from either string) to make the two strings equal.**

<details><summary>Hint</summary>What survives the deletions in both strings?</summary></details>

**Answer:** The surviving string must be a common subsequence; to delete as little as possible, keep the **longest** one. Deletions = `m + n - 2 × LCS`.

```python
def min_distance_deletions(word1, word2):
    n = len(word2)
    prev = [0] * (n + 1)
    for ch in word1:
        cur = [0] * (n + 1)
        for j in range(1, n + 1):
            cur[j] = prev[j - 1] + 1 if ch == word2[j - 1] else max(prev[j], cur[j - 1])
        prev = cur
    return len(word1) + len(word2) - 2 * prev[n]


assert min_distance_deletions("sea", "eat") == 2        # LCS "ea"
assert min_distance_deletions("leetcode", "etco") == 4  # LCS "etco"
assert min_distance_deletions("abc", "abc") == 0
```

**Q3. Longest common *substring* (contiguous). What changes in the recurrence?**

<details><summary>Hint</summary>A contiguous run is broken by any mismatch.</summary></details>

**Answer:** On a match, `dp[i][j] = dp[i-1][j-1] + 1` (same as LCS). On a mismatch, `dp[i][j] = 0` (the run is broken), and the answer is the **maximum cell anywhere**, not `dp[m][n]`.

```python
def longest_common_substring(a, b):
    best = 0
    prev = [0] * (len(b) + 1)
    for i in range(1, len(a) + 1):
        cur = [0] * (len(b) + 1)
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                cur[j] = prev[j - 1] + 1
                best = max(best, cur[j])
        prev = cur
    return best


assert longest_common_substring("abcde", "ace") == 1     # LCS would be 3
assert longest_common_substring("xabcy", "zabcw") == 3   # "abc"
assert longest_common_substring("abc", "def") == 0
```

**Q4. Fill the table for `text1 = "abc"`, `text2 = "cba"`. Why is the answer only 1?**

<details><summary>Hint</summary>Look at which cells are matches and whether any two matches can be chained diagonally.</summary></details>

**Answer:** Rows `a, b, c`; columns `c, b, a`:

```text
      c  b  a
   0  0  0  0
a  0  0  0  1
b  0  0  1  1
c  0  1  1  1
```

Every match (`a`↔`a`, `b`↔`b`, `c`↔`c`) sits on the anti-diagonal, so none of them is diagonally below-right of another. Two letters appear in opposite orders in the two strings, so at most one letter can be kept → answer `1`.

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** 2-D DP over two prefixes.
- **State:** `dp[i][j]` = LCS of `text1[:i]` and `text2[:j]`.
- **Recurrence:** match → `dp[i-1][j-1] + 1`; mismatch → `max(dp[i-1][j], dp[i][j-1])`.
- **Base / order / answer:** zero row and column; fill row by row, left to right; answer `dp[m][n]`.
- **Time:** `O(m × n)`. **Auxiliary space:** `O(m × n)`, or `O(min(m, n))` with two rows.
- **One-line memory hook:** *"Match? Go diagonal and add one. Mismatch? Take the better of up and left."*

### Completion checklist

- [x] Problem requirements verified
- [x] Examples and constraints verified
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force solution written and tested
- [x] Optimized Python solution written and tested (`tools/tests/p058.py`), plus the two-row space-optimized version
- [x] Line-by-line explanation written
- [x] Dry run completed with a real example (full 2-D table)
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
