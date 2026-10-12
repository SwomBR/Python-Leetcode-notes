# 034. Valid Anagram

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Valid Anagram |
| **LeetCode number** | 242 |
| **Topic (source list)** | String |
| **Also uses** | Hash Table, Sorting, Counting |
| **Difficulty** | Easy |
| **LeetCode URL** | <https://leetcode.com/problems/valid-anagram/> |
| **Pattern** | Frequency counting (fixed 26-letter array or hash map) |

---

## 2. Problem Explanation

### What are we given?

Two strings, `s` and `t`.

### What must we return?

`True` if `t` is an **anagram** of `s`, otherwise `False`.

### What is an anagram?

Two strings are anagrams when one can be turned into the other by **rearranging its letters**, using every letter exactly once. In other words, both strings contain **the same letters with the same counts**; only the order may differ.

- `"listen"` and `"silent"` → anagrams (each has one `l`, `i`, `s`, `t`, `e`, `n`).
- `"aab"` and `"abb"` → **not** anagrams (two `a`s vs one `a`).
- `"ab"` and `"a"` → **not** anagrams (different lengths, so the counts can't match).

### Examples

**Example 1**

```text
Input:  s = "anagram", t = "nagaram"
Output: true
```

Both strings have three `a`s and one each of `n`, `g`, `r`, `m`.

**Example 2**

```text
Input:  s = "rat", t = "car"
Output: false
```

`s` has a `t` that `t` doesn't have, and `t` has a `c` that `s` doesn't have.

(In Python the method returns `True` / `False`.)

### Constraints

- `1 <= s.length, t.length <= 5 * 10^4`
- `s` and `t` consist of lowercase English letters.

Note that the two lengths are constrained separately — they may differ.

**Follow-up:** What if the inputs contain Unicode characters? How would you adapt your solution to such a case? (Answered in Section 6 and Practice Q2.)

---

## 3. Everyday Analogy

> **Explain it like I'm five**

You and a friend each built a word out of letter tiles. Are your tile piles the **same**, just arranged differently?

Easy way to check: get 26 little boxes labelled `a` to `z`.

- For each of **your** tiles, drop a marble into its box.
- For each of your **friend's** tiles, take a marble **out** of its box.

If at the end every box is empty, you had exactly the same tiles. If any box still has marbles (or owes marbles), your piles were different.

---

## 4. Step-by-Step Logic

1. **Different lengths → impossible.** If `len(s) != len(t)`, return `False` immediately.
2. **What must match?** The count of every letter. Order is irrelevant.
3. **Option A — sort both.** Sorting puts letters in a fixed order, so anagrams become identical strings: `sorted("anagram") == sorted("nagaram")`. Simple, but `O(n log n)`.
4. **Option B — count.** Only 26 different letters can appear, so use a list of 26 counters. Add 1 for each letter of `s`, subtract 1 for each letter of `t`. Anagrams leave every counter at 0. This is `O(n)`.
5. **Why add-then-subtract instead of two tables?** It uses one table and one final check. Equivalent alternative: build two `Counter`s and compare them.
6. **Unicode (follow-up):** a 26-slot array only works for `a`–`z`. For arbitrary characters, use a hash map (`dict` / `Counter`) keyed by character.

---

## 5. Brute-Force Solution

### Algorithm

1. If the lengths differ, return `False`.
2. Put the letters of `t` in a list `remaining`.
3. For each letter of `s`, search `remaining` for a matching letter. If none is found, return `False`; otherwise remove that one copy.
4. If every letter of `s` found a partner, return `True` (lengths are equal, so `remaining` is now empty).

### Python code

```python
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False
        remaining = list(t)
        for ch in s:
            if ch in remaining:          # linear search
                remaining.remove(ch)     # remove ONE copy (also linear)
            else:
                return False
        return True
```

### Explanation

- This is the "pair up each tile by hand" method: every letter of `s` must be matched with its own copy in `t`.
- `list.remove` deletes only the **first** matching copy, so duplicates are handled correctly (`"aab"` vs `"abb"` fails when the second `a` finds nothing).

### Complexity

- **Time:** `O(n²)` — `n` letters, each causing a linear search and a linear removal. For `n = 5 × 10^4` that is on the order of 10⁹ basic steps in the worst case, so it would likely **time out** on LeetCode.
- **Auxiliary space:** `O(n)` for the `remaining` list.

---

## 6. Optimized Solution

### Idea

Count letters with a fixed 26-slot array: `+1` for `s`, `−1` for `t`, then check that everything is zero.

### Algorithm

1. If `len(s) != len(t)`, return `False`.
2. `counts = [0] * 26`.
3. For each pair of letters `(a, b)` at the same position in `s` and `t`: `counts[a] += 1`, `counts[b] -= 1`.
4. Return `True` if every count is 0.

### Python code (LeetCode-ready)

```python
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False

        counts = [0] * 26                     # one slot per letter 'a'..'z'
        for a, b in zip(s, t):
            counts[ord(a) - ord('a')] += 1    # tile from s goes in
            counts[ord(b) - ord('a')] -= 1    # tile from t comes out

        return all(c == 0 for c in counts)
```

### Alternative 1: sorting (`O(n log n)`)

```python
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        return sorted(s) == sorted(t)
```

Short and correct, but sorting costs `O(n log n)` time and `sorted` builds two new lists (`O(n)` space).

### Alternative 2: `Counter` — works for any characters (Unicode follow-up)

```python
from collections import Counter


class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        return len(s) == len(t) and Counter(s) == Counter(t)
```

### The Unicode follow-up

The 26-slot array depends on the fact that only `'a'`–`'z'` can appear. With Unicode input:

1. **Use a hash map instead of an array.** `Counter` (or a plain `dict`) can count *any* character, so Alternative 2 works unchanged. Time stays `O(n)`; space becomes `O(k)`, where `k` is the number of distinct characters, instead of a fixed 26. (An array indexed by code point would need over a million slots — wasteful.)
2. **Decide what "the same character" means.** Python strings are sequences of Unicode **code points**. Some visible characters can be written in more than one way: `"é"` can be the single code point `U+00E9`, or `"e"` followed by the combining accent `U+0301`. If the two strings might use different forms, **normalize** both first with `unicodedata.normalize("NFC", text)` so equivalent characters get the same code points (see Practice Q2).
3. **User-perceived characters (graphemes).** Some symbols that look like one character (for example an emoji with a skin-tone modifier, or a flag) are several code points. Counting code points treats them as several pieces. If your definition of "letter" is "what a person sees as one character", you need grapheme segmentation (a third-party library such as `regex` with `\X`), which goes beyond the standard library.
4. **Case and other rules are policy decisions.** The LeetCode problem compares characters exactly. Whether `"A"` should match `"a"` (use `str.casefold()`) or spaces/punctuation should be ignored depends on the application; the problem itself doesn't ask for this.

---

## 7. Line-by-Line Explanation

(26-slot array version)

| Line | What it does | Why |
|---|---|---|
| `if len(s) != len(t): return False` | Rejects different lengths immediately. | Different lengths can never have identical counts; also lets `zip` safely pair every character. |
| `counts = [0] * 26` | 26 counters, all zero. | Index 0 is `'a'`, 25 is `'z'`. |
| `for a, b in zip(s, t):` | Walks both strings together, one position at a time. | Equal lengths → `zip` covers every character of both. |
| `counts[ord(a) - ord('a')] += 1` | Adds the letter from `s`. | `ord` gives the character's code; subtracting `ord('a')` maps `'a'..'z'` to `0..25`. |
| `counts[ord(b) - ord('a')] -= 1` | Removes the letter from `t`. | Matching letters cancel out. |
| `return all(c == 0 for c in counts)` | `True` only if every counter is back at zero. | Zero everywhere ⇔ same multiset of letters. |

**Why one table is enough:** after the loop, `counts[x] = (count of x in s) − (count of x in t)`. This is zero for every `x` exactly when the two strings have the same letter counts.

---

## 8. Dry Run

**Input:** `s = "anagram"`, `t = "nagaram"` (Example 1). Only non-zero counters are shown.

| Position | `a` (from `s`) | `b` (from `t`) | Non-zero counters after the step |
|---|---|---|---|
| 0 | `a` | `n` | `{a: +1, n: −1}` |
| 1 | `n` | `a` | `{}` (both cancelled) |
| 2 | `a` | `g` | `{a: +1, g: −1}` |
| 3 | `g` | `a` | `{}` |
| 4 | `r` | `r` | `{}` |
| 5 | `a` | `a` | `{}` |
| 6 | `m` | `m` | `{}` |

All 26 counters are 0 → **`True`** ✅

**Second dry run:** `s = "rat"`, `t = "car"` (Example 2)

| Position | `a` (from `s`) | `b` (from `t`) | Non-zero counters after the step |
|---|---|---|---|
| 0 | `r` | `c` | `{r: +1, c: −1}` |
| 1 | `a` | `a` | `{r: +1, c: −1}` |
| 2 | `t` | `r` | `{c: −1, t: +1}` |

`counts[c] = −1` and `counts[t] = +1` are not zero → **`False`** ✅ (`s` has an extra `t`; `t` has an extra `c`.)

---

## 9. Concepts, Data Structures, and Patterns

- **Frequency counting:** describe a string by "how many of each character" — its **multiset**. Two strings are anagrams ⇔ equal multisets.
- **Fixed-size counting array:** when the alphabet is small and known (26 lowercase letters), a list indexed by `ord(ch) - ord('a')` is fast and uses constant memory.
- **Hash map counting (`collections.Counter`):** works for any alphabet, including Unicode; `Counter(a) == Counter(b)` compares all counts.
- **Canonical form by sorting:** sorting turns every arrangement of the same letters into one standard string. This is the key idea behind [035. Group Anagrams](035_group_anagrams.md).
- **Early exit on length:** a cheap `O(1)` check that rules out many inputs.
- **Unicode basics:** code points vs. user-perceived characters, and normalization with `unicodedata.normalize`.
- **Related notes:** [033. Minimum Window Substring](033_minimum_window_substring.md) and [032. Longest Repeating Character Replacement](032_longest_repeating_character_replacement.md) use the same character-count tables inside a sliding window; [003. Contains Duplicate](../01_array/003_contains_duplicate.md) and [001. Two Sum](../01_array/001_two_sum.md) also rely on hash-based lookups.

---

## 10. Complexity Analysis

Let `n` be the length of the strings (after the length check they're equal) and `k` the number of distinct characters.

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Brute force (match and remove) | `O(n²)` | `O(n)` | Each of `n` letters does a linear search and a linear removal in a list of size up to `n`. |
| Sorting | `O(n log n)` | `O(n)` | `sorted` creates two new lists of length `n`. |
| 26-slot counting array (optimized) | `O(n)` | `O(1)` | One pass plus a 26-step check; the array size does not grow with `n`. |
| `Counter` / dict (Unicode-ready) | `O(n)` average | `O(k)` | Hash map with one entry per distinct character; `k ≤ 26` here, but unbounded alphabets need `O(k)`. |

If the lengths differ, every approach returns after the `O(1)` length check (the sorting one-liner still sorts — add a length check if you care).

---

## 11. Edge Cases

| Case | Example | Expected result | Why |
|---|---|---|---|
| Single equal letters | `s = "a"`, `t = "a"` | `True` | Same single letter. |
| Single different letters | `s = "a"`, `t = "b"` | `False` | Counts differ. |
| Different lengths | `s = "ab"`, `t = "a"` | `False` | Rejected by the length check. |
| Same letters, different counts | `s = "aab"`, `t = "abb"` | `False` | `a` count 2 vs 1. |
| Same length, different multiset | `s = "aacc"`, `t = "ccac"` | `False` | `a`: 2 vs 1; `c`: 2 vs 3. |
| Identical strings | `s = "abc"`, `t = "abc"` | `True` | Zero rearrangement is still a valid arrangement. |
| Classic anagram | `s = "listen"`, `t = "silent"` | `True` | Same counts, different order. |

---

## 12. Common Mistakes and Debugging

1. **Comparing sets instead of counts.** `set("aab") == set("abb")` is `True`, but they are not anagrams. Duplicates matter.
2. **Forgetting the length check** in the `zip` version. `zip` stops at the shorter string, so `s = "a"`, `t = "ab"` would wrongly return `True` without it.
3. **Hard-coding 26 for Unicode input.** `ord('é') - ord('a')` is `136`, far outside `0..25`, and raises `IndexError`. Worse, an uppercase `'Z'` gives `90 − 97 = −7`, a *valid* negative Python index, so it silently corrupts slot 19 (`'t'`). Use a `Counter` for general characters.
4. **Using `str.replace(ch, "", 1)` in a loop as the brute force** — correct but `O(n²)`, creating a new string each time.
5. **Checking only that every letter of `s` occurs in `t`** (e.g. `all(ch in t for ch in s)`). This ignores counts: `"aa"` vs `"ab"` would pass that check.

**Debugging tip:** print `{chr(i + 97): c for i, c in enumerate(counts) if c}` after the loop to see exactly which letters don't balance.

---

## 13. Practice Questions

**Q1. Why is the length check required in the `zip` version, but optional for the `Counter(s) == Counter(t)` version?**

<details><summary>Hint</summary>What does `zip` do when one string is longer?</summary></details>

**Answer:** `zip` stops at the shorter input, so the extra characters of the longer string are never counted — `s = "a"`, `t = "ab"` would leave all counters at 0 and return `True`. Comparing two full `Counter`s looks at *every* character of both strings, so different lengths automatically give different counters. The length check there is just a fast early exit.

**Q2. Unicode follow-up: write `is_anagram_unicode(s, t)` that treats canonically equivalent characters (such as `"é"` written as one code point or as `"e"` + combining accent) as the same.**

<details><summary>Hint</summary>Normalize both strings with `unicodedata.normalize("NFC", ...)` before counting with a `Counter`.</summary></details>

**Answer:**

```python
import unicodedata
from collections import Counter


def is_anagram_unicode(s, t):
    s = unicodedata.normalize("NFC", s)
    t = unicodedata.normalize("NFC", t)
    return len(s) == len(t) and Counter(s) == Counter(t)


composed = "été"            # "été" with precomposed é
decomposed = "été"        # same word, e + combining accent
assert is_anagram_unicode(composed, "téé") is True
assert is_anagram_unicode(composed, decomposed) is True       # equal after NFC
assert Counter(composed) != Counter(decomposed)               # but not before
assert is_anagram_unicode("日本語", "語日本") is True
assert is_anagram_unicode("ab", "aé") is False
```

**Q3. Find All Anagrams in a String (LeetCode 438): return every start index `i` where `s[i : i + len(p)]` is an anagram of `p`.**

<details><summary>Hint</summary>Fixed-size sliding window of length `len(p)` with a 26-slot count array; compare with `p`'s counts after each slide.</summary></details>

**Answer:**

```python
def find_anagrams(s, p):
    if len(p) > len(s):
        return []
    need = [0] * 26
    window = [0] * 26
    for ch in p:
        need[ord(ch) - 97] += 1
    result = []
    for right, ch in enumerate(s):
        window[ord(ch) - 97] += 1
        if right >= len(p):
            window[ord(s[right - len(p)]) - 97] -= 1   # char that slid out
        if window == need:
            result.append(right - len(p) + 1)
    return result


assert find_anagrams("cbaebabacd", "abc") == [0, 6]
assert find_anagrams("abab", "ab") == [0, 1, 2]
assert find_anagrams("a", "ab") == []
```

Each slide costs `O(26)` for the comparison → `O(26 · len(s))` time, `O(1)` space.

**Q4. Minimum Number of Steps to Make Two Strings Anagram (LeetCode 1347): `s` and `t` have equal length; in one step you may replace any character of `t`. Return the minimum number of steps.**

<details><summary>Hint</summary>Every letter that `t` has *too few* of must be produced by one replacement.</summary></details>

**Answer:** Compute `counts[x] = count in s − count in t`. The positive entries add up to the number of letters `t` is missing, and each replacement fixes exactly one of them.

```python
def min_steps(s, t):
    counts = [0] * 26
    for a, b in zip(s, t):
        counts[ord(a) - 97] += 1
        counts[ord(b) - 97] -= 1
    return sum(c for c in counts if c > 0)


assert min_steps("bab", "aba") == 1
assert min_steps("leetcode", "practice") == 5
assert min_steps("anagram", "mangaar") == 0
```

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** Frequency counting.
- **Key idea:** Anagrams ⇔ same length and same count for every character. `+1` for `s`, `−1` for `t`, all zero ⇒ `True`.
- **Time:** `O(n)`.
- **Auxiliary space:** `O(1)` with a 26-slot array; `O(k)` with a `Counter` for general/Unicode input.
- **Unicode:** use a hash map; normalize (NFC) if equivalent characters may be encoded differently.
- **One-line memory hook:** *"Marbles in for one word, marbles out for the other — empty boxes mean anagram."*

### Completion checklist

- [x] Problem requirements verified
- [x] Examples and constraints verified
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force solution written and tested
- [x] Optimized Python solution written and tested (`tools/tests/p034.py`), plus the sorting and `Counter` alternatives
- [x] Line-by-line explanation written
- [x] Dry run completed with real examples
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Unicode follow-up answered with tested code
- [x] Practice questions with worked answers added
- [x] Final review completed
