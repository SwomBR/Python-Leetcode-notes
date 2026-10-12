# 037. Valid Palindrome

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Valid Palindrome |
| **LeetCode number** | 125 |
| **Topic (source list)** | String |
| **Also uses** | Two Pointers |
| **Difficulty** | Easy |
| **LeetCode URL** | <https://leetcode.com/problems/valid-palindrome/> |
| **Pattern** | Two pointers moving inward, skipping characters that don't count |

---

## 2. Problem Explanation

### What are we given?

`s` — a string of printable ASCII characters: letters, digits, spaces, punctuation and symbols.

### What must we return?

`True` if `s` is a palindrome under the special rules below, otherwise `False`.

### The rules

1. **Ignore everything that is not a letter or a digit.** Spaces, commas, colons, underscores, quotes and so on are thrown away. Letters (`a`–`z`, `A`–`Z`) and digits (`0`–`9`) are called **alphanumeric** characters, and only they count.
2. **Ignore upper/lower case.** Turn every uppercase letter into lowercase before comparing, so `A` and `a` are the same.
3. What remains must read **the same from left to right as from right to left**.
4. If nothing remains (the string had no letters or digits at all), the result is `True` — an empty string reads the same in both directions.

### Examples

**Example 1**

```text
Input:  s = "A man, a plan, a canal: Panama"
Output: true
```

After removing spaces/punctuation and lowercasing, we get `"amanaplanacanalpanama"`, which reads the same backwards.

**Example 2**

```text
Input:  s = "race a car"
Output: false
```

Cleaned, it is `"raceacar"`. Backwards that is `"racaecar"` — different.

**Example 3**

```text
Input:  s = " "
Output: true
```

The only character is a space, so the cleaned string is empty `""`, and an empty string is a palindrome.

### Constraints

- `1 <= s.length <= 2 * 10^5`
- `s` consists only of printable ASCII characters.

There is no follow-up for this problem.

---

## 3. Everyday Analogy

> **Explain it like I'm five**

Imagine a sentence written on a long strip of paper. Two friends stand at opposite ends: Lefty at the start and Righty at the end. They walk toward each other.

- If either friend is standing on a space or a comma or any symbol, they just **step over it** — it doesn't count.
- When both are standing on a real letter or number, they shout it out (both shouting in lowercase). If the two shouts are different, the sentence is **not** a palindrome and the game ends.
- If the shouts match, both take one step inward and repeat.

If they meet in the middle without ever disagreeing, the sentence **is** a palindrome.

---

## 4. Step-by-Step Logic

1. **What is a palindrome?** The first counted character equals the last, the second equals the second-to-last, and so on.
2. **Simple plan:** build the cleaned string (keep alphanumerics, lowercase them) and compare it with its reverse. Easy, but it builds extra strings of size up to `n`.
3. **Better plan:** we only ever compare a character from the left with a character from the right, so we can work on the **original** string with two indices, `left` and `right`.
4. **Skipping:** before comparing, move `left` forward past non-alphanumeric characters and `right` backward past them. Always keep the condition `left < right` while skipping so the pointers never cross or run off the string.
5. **Comparing:** compare `s[left].lower()` with `s[right].lower()`. Different → `False`. Same → move both inward.
6. **Stopping:** when `left >= right`, every pair has been checked → `True`. (A single middle character has no partner and never needs checking.)

---

## 5. Brute-Force Solution

### Algorithm

1. Build a new string containing only the alphanumeric characters of `s`, all lowercased.
2. Return whether it equals its own reverse.

### Python code

```python
class Solution:
    def isPalindrome(self, s: str) -> bool:
        cleaned = "".join(ch.lower() for ch in s if ch.isalnum())
        return cleaned == cleaned[::-1]
```

### Explanation

- `ch.isalnum()` is `True` for letters and digits only, so spaces and punctuation are dropped.
- `ch.lower()` makes the comparison case-insensitive (digits are unchanged by `lower()`).
- `cleaned[::-1]` is the reversed string; comparing the two decides the answer.
- For `" "`, `cleaned` is `""`, and `"" == ""` → `True`, matching Example 3.

### Complexity

- **Time:** `O(n)` — one pass to build `cleaned`, one to reverse it, one to compare. This easily passes LeetCode's limits; it is called "brute force" here only because it does the most direct thing and uses extra memory.
- **Auxiliary space:** `O(n)` — `cleaned` and its reversed copy can each be as long as `s`.

---

## 6. Optimized Solution

### Idea

Compare characters in place with two pointers, skipping non-alphanumeric characters as we go. No new strings are built, so the extra memory is constant.

### Algorithm

1. `left = 0`, `right = len(s) - 1`.
2. While `left < right`:
   - Move `left` right while `left < right` and `s[left]` is not alphanumeric.
   - Move `right` left while `left < right` and `s[right]` is not alphanumeric.
   - If `s[left].lower() != s[right].lower()`, return `False`.
   - Move both pointers one step inward.
3. Return `True`.

### Python code (LeetCode-ready)

```python
class Solution:
    def isPalindrome(self, s: str) -> bool:
        left, right = 0, len(s) - 1

        while left < right:
            # Skip characters that don't count (spaces, punctuation, ...).
            while left < right and not s[left].isalnum():
                left += 1
            while left < right and not s[right].isalnum():
                right -= 1

            if s[left].lower() != s[right].lower():
                return False

            left += 1
            right -= 1

        return True
```

---

## 7. Line-by-Line Explanation

| Line | What it does | Why |
|---|---|---|
| `left, right = 0, len(s) - 1` | Puts one pointer at each end. | A palindrome is checked from the outside in. |
| `while left < right:` | Keeps going while there is still a pair to compare. | When the pointers meet or cross, everything has been checked. |
| `while left < right and not s[left].isalnum(): left += 1` | Skips non-alphanumeric characters from the left. | They don't count. `left < right` stops the pointer from overtaking `right` (e.g. in `".,"`). |
| `while left < right and not s[right].isalnum(): right -= 1` | Skips them from the right. | Same reason. |
| `if s[left].lower() != s[right].lower(): return False` | Compares the two counted characters, ignoring case. | One mismatch is enough to fail. |
| `left += 1; right -= 1` | Moves both pointers inward. | That pair is confirmed; check the next one. |
| `return True` | No mismatch was found. | Also covers strings with no alphanumerics at all. |

**What if the skipping loops stop with `left == right`?** Then `s[left]` and `s[right]` are the same character, so the comparison trivially succeeds, the pointers cross, and we return `True`. This is why the case `".,"` (no alphanumerics) works.

---

## 8. Dry Run

**Input:** `s = "race a car"` (Example 2). Indices: `r0 a1 c2 e3 ␣4 a5 ␣6 c7 a8 r9` (␣ = space).

| Step | `left` | `right` | Skipping | Compare | Result |
|---|---|---|---|---|---|
| 1 | 0 | 9 | none | `r` vs `r` | equal → `left=1`, `right=8` |
| 2 | 1 | 8 | none | `a` vs `a` | equal → `left=2`, `right=7` |
| 3 | 2 | 7 | none | `c` vs `c` | equal → `left=3`, `right=6` |
| 4 | 3 | 6 → 5 | `right` skips the space at 6 | `e` vs `a` | **different** → return `False` |

**Result:** `False` ✅

**Second dry run:** `s = "A man, a plan, a canal: Panama"` (Example 1, length 30). Showing only the comparisons; skipped positions are spaces, commas and the colon.

| Compare # | `left` → char | `right` → char | Lowercased equal? |
|---|---|---|---|
| 1 | 0 `A` | 29 `a` | `a` = `a` ✓ |
| 2 | 2 `m` (skipped space at 1) | 28 `m` | ✓ |
| 3 | 3 `a` | 27 `a` | ✓ |
| 4 | 4 `n` | 26 `n` | ✓ |
| 5 | 7 `a` (skipped `,` and space) | 25 `a` | ✓ |
| 6 | 9 `p` (skipped space) | 24 `P` | `p` = `p` ✓ |
| 7 | 10 `l` | 21 `l` (skipped space at 23 and `:` at 22) | ✓ |
| 8 | 11 `a` | 20 `a` | ✓ |
| 9 | 12 `n` | 19 `n` | ✓ |
| 10 | 15 `a` (skipped `,` and space) | 18 `a` | ✓ |
| 11 | 17 `c` (skipped space at 16) | 17 `c` | same position ✓ |

After compare 11 the pointers cross (`left = 18`, `right = 16`), so the loop ends and we return **`True`** ✅. The cleaned string `amanaplanacanalpanama` has 21 characters; its middle character `c` (index 17 in `s`) is compared with itself.

---

## 9. Concepts, Data Structures, and Patterns

- **Two pointers (opposite ends):** one index from each side moving toward the middle. Classic for palindromes, reversing in place, and pair search in sorted arrays.
- **Filtering on the fly:** instead of building a cleaned copy, the pointers skip unwanted characters. This saves memory.
- **`str.isalnum()` and `str.lower()`:** built-in string methods. For ASCII input, `isalnum()` is `True` exactly for `a`–`z`, `A`–`Z`, `0`–`9`. (For non-ASCII text Python also counts letters from other alphabets, which doesn't matter here.)
- **Slicing `[::-1]`:** reverses a string in `O(n)` time and space.
- **Related notes:**
  - Palindromes are central to [038_longest_palindromic_substring.md](038_longest_palindromic_substring.md) and [039_palindromic_substrings.md](039_palindromic_substrings.md), where pointers expand **outward** from a centre instead of inward.
  - Two pointers from both ends also solve [010_container_with_most_water.md](../01_array/010_container_with_most_water.md) and [009_3sum.md](../01_array/009_3sum.md).
  - Outside this list: Valid Palindrome II (LeetCode 680) — allowed to delete one character.

---

## 10. Complexity Analysis

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Clean + reverse (brute force) | `O(n)` | `O(n)` | Builds the cleaned string and its reverse, each up to `n` characters. |
| Two pointers (optimized) | `O(n)` | `O(1)` | Every index is visited by at most one pointer once (the pointers only move inward and never revisit), so the total work across all loops is `O(n)`. Only two integer variables are stored. |

**Why are nested `while` loops still `O(n)`?** The inner loops don't restart; they continue moving the same two pointers. Together, `left` moves right at most `n` times and `right` moves left at most `n` times.

---

## 11. Edge Cases

| Case | Example | Expected result | Why |
|---|---|---|---|
| Only a space | `" "` | `True` | Nothing alphanumeric remains (official Example 3). |
| Only punctuation | `".,"` | `True` | Pointers skip everything and meet. |
| Single character | `"a"` | `True` | `left == right` from the start. |
| Digit vs letter | `"0P"` | `False` | `0` ≠ `p`; digits are not letters. |
| Mixed case | `"Aa"` | `True` | Case is ignored. |
| Underscore is not alphanumeric | `"ab_a"` | `True` | Cleaned string is `"aba"`. |
| Digits only | `"12"` | `False` | `1` ≠ `2`. |
| Apostrophes and spaces | `"No 'x' in Nixon"` | `True` | Cleaned string `noxinnixon` reads the same backwards. |

---

## 12. Common Mistakes and Debugging

1. **Forgetting digits count.** Using `isalpha()` instead of `isalnum()` drops digits, so `"0P"` would wrongly become `"p"` → `True`. The correct answer is `False`.
2. **Forgetting to lowercase.** `"Aa"` would fail.
3. **Skipping loops without `left < right`.** On `".,"` the left pointer would run past the end and raise `IndexError`.
4. **Using `if` instead of `while` to skip.** Only one junk character would be skipped, so for `",,a"` the left pointer stops on the second comma and compares `,` with `a` → wrongly `False` (the cleaned string is `"a"`, so the answer is `True`).
5. **Treating `_` as alphanumeric.** Some people use regex `\w`, which matches underscore. `"ab_a"` must be treated as `"aba"`.

**Debugging tip:** print `left, right, s[left], s[right]` right before each comparison.

---

## 13. Practice Questions

**Q1. What does the two-pointer solution return for `s = "Was it a car or a cat I saw?"`?**

<details><summary>Hint</summary>Write out the cleaned lowercase string and read it backwards.</summary></details>

**Answer:** The cleaned string is `wasitacaroracatisaw`, which reads the same backwards, so the result is `True`. The `?` at the end is skipped by the right pointer at the very first step.

**Q2. Valid Palindrome II: return `True` if `s` (lowercase letters only) can become a palindrome by deleting **at most one** character.**

<details><summary>Hint</summary>Use two pointers; at the first mismatch, try skipping the left character or skipping the right one, and check whether the rest is a palindrome.</summary></details>

**Answer:** At the first mismatch there are only two choices, and each check is `O(n)`, so the total is `O(n)`.

```python
def valid_palindrome_after_one_delete(s):
    def is_pal(i, j):
        while i < j:
            if s[i] != s[j]:
                return False
            i += 1
            j -= 1
        return True

    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return is_pal(left + 1, right) or is_pal(left, right - 1)
        left += 1
        right -= 1
    return True


assert valid_palindrome_after_one_delete("aba") is True
assert valid_palindrome_after_one_delete("abca") is True   # delete 'b' or 'c'
assert valid_palindrome_after_one_delete("abc") is False
```

**Q3. Check whether a *positive integer* is a palindrome without converting it to a string.**

<details><summary>Hint</summary>Build the reversed number digit by digit using `% 10` and `// 10`.</summary></details>

**Answer:**

```python
def is_number_palindrome(x):
    if x < 0:
        return False
    original, reversed_num = x, 0
    while x > 0:
        reversed_num = reversed_num * 10 + x % 10
        x //= 10
    return original == reversed_num


assert is_number_palindrome(121) is True
assert is_number_palindrome(123) is False
assert is_number_palindrome(7) is True
```

**Q4. Why does the optimized solution use `O(1)` space while the brute force uses `O(n)`? Is the brute force ever preferable?**

<details><summary>Hint</summary>Think about what each version stores, and about readability.</summary></details>

**Answer:** The two-pointer version stores only two integers; the brute force stores a cleaned copy and its reverse. Both are `O(n)` time. The one-liner is shorter, easier to read and in Python often similar in speed (its work runs in C), so it is perfectly fine in practice; in an interview, the two-pointer version shows you can avoid the extra memory.

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** Two pointers from both ends, skipping ignored characters.
- **Key idea:** Skip non-alphanumerics (while `left < right`), compare lowercase characters, move inward; any mismatch → `False`.
- **Time:** `O(n)`.
- **Auxiliary space:** `O(1)` (brute force `O(n)`).
- **One-line memory hook:** *"Lefty and Righty step over the junk and must shout the same letter."*

### Completion checklist

- [x] Problem requirements verified
- [x] Examples and constraints verified against the official statement
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force solution written and tested
- [x] Optimized Python solution written and tested (`tools/tests/p037.py`)
- [x] Line-by-line explanation written
- [x] Dry run completed with real examples
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
