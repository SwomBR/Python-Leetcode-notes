# 033. Minimum Window Substring

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Minimum Window Substring |
| **LeetCode number** | 76 |
| **Topic (source list)** | String |
| **Also uses** | Hash Table, Sliding Window |
| **Difficulty** | Hard |
| **LeetCode URL** | <https://leetcode.com/problems/minimum-window-substring/> |
| **Pattern** | Variable-size sliding window — expand until valid, then shrink while still valid |

---

## 2. Problem Explanation

### What are we given?

- `s` — the string we search in (length `m`).
- `t` — the string of characters we must cover (length `n`).

Both contain only uppercase and lowercase English letters.

### What must we return?

The **shortest substring of `s`** (a contiguous block, returned as a string) that contains **every character of `t`, with multiplicity**. If no such block exists, return the empty string `""`.

### The rules

1. **Duplicates count.** If `t = "aa"`, the window must contain at least **two** `a`s. One is not enough.
2. **Extra characters are fine.** The window may contain other letters, or more copies than needed.
3. **Order does not matter.** The characters of `t` may appear in any order inside the window.
4. **Case matters.** `'a'` and `'A'` are different characters.
5. **Uniqueness:** the statement promises that test cases are generated so the answer is **unique**, so you never have to choose between two different minimum windows on LeetCode. (For other inputs there could be ties; our solutions return the **leftmost** shortest window.)
6. If no window works (for example `t` is longer than `s`, or `s` lacks some letter), return `""`.

### Examples

**Example 1**

```text
Input:  s = "ADOBECODEBANC", t = "ABC"
Output: "BANC"
```

`"BANC"` contains `A`, `B` and `C`, and no shorter block of `s` contains all three. (`"ADOBEC"` also contains them, but it is longer.)

**Example 2**

```text
Input:  s = "a", t = "a"
Output: "a"
```

The whole string is the smallest window.

**Example 3**

```text
Input:  s = "a", t = "aa"
Output: ""
```

`t` needs two `a`s, but `s` only has one, so no window works.

### Constraints

- `m == s.length`
- `n == t.length`
- `1 <= m, n <= 10^5`
- `s` and `t` consist of uppercase and lowercase English letters.

**Follow-up:** Could you find an algorithm that runs in `O(m + n)` time?

---

## 3. Everyday Analogy

> **Explain it like I'm five**

You have a shopping list (`t`): "one apple, one banana, one carrot." In front of you is a long conveyor belt of items (`s`). You want to pick up the **shortest stretch** of the belt that has everything on your list.

- You stretch your arms to the **right**, grabbing items, until you finally hold everything on the list.
- Now you try to let go of items on the **left**, one by one, as long as you *still* have everything. Every time your stretch is still complete, you measure it — maybe it's the shortest yet!
- The moment you drop something you needed, you stop letting go and start reaching right again.

At the end of the belt, the shortest complete stretch you measured is the answer.

---

## 4. Step-by-Step Logic

1. **Coverage check.** A window covers `t` when, for every character `c`, `count of c in window >= count of c in t`.
2. **Expand** `right` (one character at a time) until the window `s[left..right]` covers `t`.
3. **Shrink** `left` **while the window still covers `t`**, recording the length each time. This finds the shortest valid window ending at `right`.
   - Compare with [031](031_longest_substring_without_repeating_characters.md) and [032](032_longest_repeating_character_replacement.md): there we shrank while the window was **invalid** to find the *longest* valid window. Here we shrink while the window is **valid** to find the *shortest*.
4. **Why `left` never needs to go back:** if `s[left..right]` doesn't cover `t`, any window starting even later and ending at `right` can't either; and once we've measured the shortest window ending at `right`, starting earlier can only make windows longer.
5. **Checking coverage in `O(1)`.** Comparing whole count tables each step would cost up to 52 checks. Instead keep:
   - `need[c]` = how many more copies of `c` the window still needs (it goes **negative** when the window has spare copies);
   - `missing` = total number of characters of `t` (counting duplicates) not yet covered.
   The window covers `t` exactly when `missing == 0`.
6. **Updating `missing`:** when a character enters and `need[c] > 0` before the decrement, it was genuinely needed → `missing -= 1`. When a character leaves and `need[c] > 0` after the increment, we just lost a needed copy → `missing += 1`.

---

## 5. Brute-Force Solution

### Algorithm

1. Count the characters of `t` once.
2. For every start index `i`, move the end `j` rightwards, counting characters and tracking how many required characters are still missing.
3. The first `j` that makes the window complete gives the **shortest** valid window starting at `i`; compare it with the best so far, then `break` (longer windows from `i` are pointless).
4. Return the best window, or `""`.

### Python code

```python
from collections import Counter, defaultdict


class Solution:
    def minWindow(self, s: str, t: str) -> str:
        need = Counter(t)
        best_start, best_len = 0, float("inf")

        for i in range(len(s)):
            have = defaultdict(int)
            missing = len(t)
            for j in range(i, len(s)):
                ch = s[j]
                have[ch] += 1
                if have[ch] <= need[ch]:     # this copy was still required
                    missing -= 1
                if missing == 0:             # s[i..j] covers t
                    if j - i + 1 < best_len:
                        best_start, best_len = i, j - i + 1
                    break                    # longer windows from i are worse

        return "" if best_len == float("inf") else s[best_start:best_start + best_len]
```

### Explanation

- `need` is a `Counter`, so `need[ch]` is `0` for characters not in `t` (and reading it does not add a key).
- `have[ch] <= need[ch]` is true exactly when this copy of `ch` fills a still-open slot of `t`; spare copies don't reduce `missing`.
- Because the inner loop stops at the first complete window, each start `i` contributes its shortest window. The strict `<` keeps the **leftmost** shortest window.

### Complexity

- **Time:** `O(n + m²)` — counting `t` is `O(n)`, then up to `m` starts, each scanning up to `m` characters. For `m = 10^5` that is about 5 × 10⁹ steps → **times out** on LeetCode, and it does not meet the follow-up.
- **Auxiliary space:** `O(k)`, where `k` is the number of distinct characters in `s` and `t` (at most 52 letters here, so `O(1)` for this problem's alphabet).

---

## 6. Optimized Solution

### Idea

One sliding window. Expand `right` until `missing == 0`, then shrink `left` as far as possible while `missing` stays `0`, recording the smallest window.

### Algorithm

1. `need = Counter(t)`, `missing = len(t)`, `left = 0`, best = none.
2. For each `right` with character `ch`:
   1. If `need[ch] > 0`: `missing -= 1`. Then `need[ch] -= 1`.
   2. While `missing == 0`:
      - If `right - left + 1` is smaller than the best, record it.
      - Remove `s[left]`: `need[s[left]] += 1`; if `need[s[left]] > 0`, `missing += 1`.
      - `left += 1`.
3. Return the recorded window, or `""` if none.

### Python code (LeetCode-ready)

```python
from collections import Counter


class Solution:
    def minWindow(self, s: str, t: str) -> str:
        need = Counter(t)      # how many more of each char the window still needs
        missing = len(t)       # total chars of t not yet covered
        left = 0
        best_start, best_len = 0, float("inf")

        for right, ch in enumerate(s):
            # Expand: s[right] enters the window
            if need[ch] > 0:
                missing -= 1
            need[ch] -= 1

            # Shrink while the window still covers t
            while missing == 0:
                if right - left + 1 < best_len:
                    best_start, best_len = left, right - left + 1
                left_ch = s[left]
                need[left_ch] += 1
                if need[left_ch] > 0:        # we just dropped a required copy
                    missing += 1
                left += 1

        return "" if best_len == float("inf") else s[best_start:best_start + best_len]
```

### Alternative: two count tables + "formed" (the textbook form)

Some people find it clearer to keep the window's counts separately and count how many **distinct** characters are fully satisfied.

```python
from collections import Counter, defaultdict


class Solution:
    def minWindow(self, s: str, t: str) -> str:
        target = Counter(t)
        required = len(target)          # distinct characters that must be satisfied
        window = defaultdict(int)
        formed = 0                      # distinct characters currently satisfied
        left = 0
        best = (float("inf"), 0, 0)     # (length, start, end)

        for right, ch in enumerate(s):
            window[ch] += 1
            if ch in target and window[ch] == target[ch]:
                formed += 1

            while formed == required:
                if right - left + 1 < best[0]:
                    best = (right - left + 1, left, right)
                left_ch = s[left]
                window[left_ch] -= 1
                if left_ch in target and window[left_ch] < target[left_ch]:
                    formed -= 1
                left += 1

        return "" if best[0] == float("inf") else s[best[1]:best[2] + 1]
```

Both versions do the same window movements; they only differ in how they remember "is the window complete?".

---

## 7. Line-by-Line Explanation

(Main optimized version)

| Line | What it does | Why |
|---|---|---|
| `need = Counter(t)` | `need[c]` = copies of `c` still required. | Starts as the counts of `t`. It goes negative when the window has spare copies; characters not in `t` simply become negative when they enter. |
| `missing = len(t)` | How many required characters (with duplicates) are not yet in the window. | `missing == 0` ⇔ the window covers `t`. |
| `left = 0` | Left edge of the window. | Window is `s[left..right]`. |
| `best_start, best_len = 0, float("inf")` | Best window found so far. | Infinity means "none found yet". |
| `for right, ch in enumerate(s):` | Moves the right edge. | Each character enters once. |
| `if need[ch] > 0: missing -= 1` | If `ch` was still required, one fewer is missing. | Checked **before** decrementing so spare copies don't count. |
| `need[ch] -= 1` | Records that the window now holds one more `ch`. | Keeps `need` exact. |
| `while missing == 0:` | The window covers `t` — try to shrink it. | Shrinking while **valid** finds the shortest window ending at `right`. |
| `if right - left + 1 < best_len:` | Is this the shortest so far? | Strict `<` keeps the leftmost on ties. |
| `left_ch = s[left]` / `need[left_ch] += 1` | Removes the leftmost character. | The window now needs one more of it (or has one fewer spare). |
| `if need[left_ch] > 0: missing += 1` | Did we just lose a required copy? | If `need` went from 0 to 1, the window no longer covers `t`; the `while` ends. |
| `left += 1` | Moves the left edge. | — |
| `return "" if ... else s[...]` | Slices the best window, or returns `""`. | Slicing once at the end avoids building strings inside the loop. |

---

## 8. Dry Run

**Input:** `s = "ADOBECODEBANC"`, `t = "ABC"` (Example 1). Start: `need = {A:1, B:1, C:1}`, `missing = 3`.

Indices: `A0 D1 O2 B3 E4 C5 O6 D7 E8 B9 A10 N11 C12`. The `need` column shows only `A`, `B`, `C` (other letters just go negative and never affect `missing`).

| `right` | `ch` | `need` (A,B,C) after expand | `missing` | Shrink phase (window checked → action) | `left` after | Window after | Best |
|---|---|---|---|---|---|---|---|
| 0 | A | 0, 1, 1 | 2 | — | 0 | `"A"` | — |
| 1 | D | 0, 1, 1 | 2 | — | 0 | `"AD"` | — |
| 2 | O | 0, 1, 1 | 2 | — | 0 | `"ADO"` | — |
| 3 | B | 0, 0, 1 | 1 | — | 0 | `"ADOB"` | — |
| 4 | E | 0, 0, 1 | 1 | — | 0 | `"ADOBE"` | — |
| 5 | C | 0, 0, 0 | **0** | `"ADOBEC"` (6) → **record**; drop `A` → need A = 1, missing = 1 | 1 | `"DOBEC"` | `"ADOBEC"` |
| 6 | O | 1, 0, 0 | 1 | — | 1 | `"DOBECO"` | `"ADOBEC"` |
| 7 | D | 1, 0, 0 | 1 | — | 1 | `"DOBECOD"` | `"ADOBEC"` |
| 8 | E | 1, 0, 0 | 1 | — | 1 | `"DOBECODE"` | `"ADOBEC"` |
| 9 | B | 1, −1, 0 | 1 | — (second `B` is a spare, `missing` unchanged) | 1 | `"DOBECODEB"` | `"ADOBEC"` |
| 10 | A | 0, −1, 0 | **0** | `"DOBECODEBA"` (10) drop D; `"OBECODEBA"` (9) drop O; `"BECODEBA"` (8) drop B → need B = 0, still covered; `"ECODEBA"` (7) drop E; `"CODEBA"` (6, not < 6) drop C → need C = 1, missing = 1 | 6 | `"ODEBA"` | `"ADOBEC"` |
| 11 | N | 0, 0, 1 | 1 | — | 6 | `"ODEBAN"` | `"ADOBEC"` |
| 12 | C | 0, 0, 0 | **0** | `"ODEBANC"` (7) drop O; `"DEBANC"` (6) drop D; `"EBANC"` (5) → **record**, drop E; `"BANC"` (4) → **record**, drop B → need B = 1, missing = 1 | 10 | `"ANC"` | **`"BANC"`** |

**Result:** `"BANC"` ✅

Things to notice:

- At step 9 the extra `B` made `need[B] = −1`. That's why at step 10 we could drop the first `B` (index 3) without breaking coverage.
- At step 10 the window `"CODEBA"` has length 6, equal to the best, so it is not recorded (strict `<`).

**Second dry run:** `s = "a"`, `t = "aa"` (Example 3). Start: `need = {a:2}`, `missing = 2`.

| `right` | `ch` | `need[a]` before | `missing` after | `need[a]` after | Covered? |
|---|---|---|---|---|---|
| 0 | a | 2 | 1 | 1 | No |

The loop ends with `missing = 1`, so no window was ever recorded: `best_len` is still infinity → return `""` ✅.

---

## 9. Concepts, Data Structures, and Patterns

- **Sliding window, "shrink while valid" variant:** used to find the **minimum** window satisfying a condition. Template:

  ```text
  for right in range(len(s)):
      add s[right]
      while window is valid:
          update answer with the window
          remove s[left]; left += 1
  ```

  Compare with the "shrink while invalid" variant for the **maximum** window in [031](031_longest_substring_without_repeating_characters.md) and [032](032_longest_repeating_character_replacement.md).
- **Frequency counting with `collections.Counter`:** returns 0 for missing keys, which keeps the code short. Same counting idea as [034. Valid Anagram](034_valid_anagram.md).
- **A single "deficit" counter (`missing`):** turns an expensive "compare two tables" check into an `O(1)` integer check. This idea — maintain an aggregate incrementally instead of recomputing it — appears in many window problems.
- **Amortized analysis:** each index is added once by `right` and removed at most once by `left` → `O(m)` window moves in total.
- **Multiset coverage:** "window contains `t`" is a multiset ⊇ relationship, not a set relationship — duplicates matter.
- **Related problems:** Permutation in String (LeetCode 567) and Find All Anagrams in a String (LeetCode 438) use a **fixed-size** window with the same counting idea (see Practice Q2); [035. Group Anagrams](035_group_anagrams.md) uses character counts as keys.

---

## 10. Complexity Analysis

Let `m = len(s)`, `n = len(t)`, and `k` = number of distinct characters appearing in `s` and `t` (here at most 52, since only English letters are allowed).

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Brute force | `O(n + m²)` | `O(k)` | Count `t`, then for each start scan right until coverage. |
| Sliding window with `missing` | `O(m + n)` | `O(k)` | `O(n)` to build `need`; `right` and `left` each move at most `m` times with `O(1)` work per move. Meets the follow-up. |
| Two tables + `formed` | `O(m + n)` | `O(k)` | Same movements; two dictionaries instead of one. |

The final slice `s[best_start:best_start + best_len]` costs `O(best_len) ≤ O(m)` and creates the output string, which is not counted as auxiliary space. Because `k ≤ 52` for this problem, the auxiliary space is also `O(1)` in terms of `m` and `n`.

---

## 11. Edge Cases

| Case | Example | Expected result | Why |
|---|---|---|---|
| Single matching character | `s = "a"`, `t = "a"` | `"a"` | Whole string. |
| Duplicates not available | `s = "a"`, `t = "aa"` | `""` | Needs two `a`s. |
| Character absent | `s = "a"`, `t = "b"` | `""` | `missing` never reaches 0. |
| `t` longer than `s` | `s = "abc"`, `t = "abcd"` | `""` | Impossible to cover. |
| Case sensitivity | `s = "aA"`, `t = "A"` | `"A"` | `'a'` does not count as `'A'`. |
| Answer at the end | `s = "ab"`, `t = "b"` | `"b"` | Shrinking drops the `a`. |
| Duplicates needed | `s = "aa"`, `t = "aa"` | `"aa"` | Both copies are required. |
| Spare copies to drop | `s = "bba"`, `t = "ab"` | `"ba"` | The first `b` is spare and is dropped while shrinking. |
| Longer mixed example | `s = "cabwefgewcwaefgcf"`, `t = "cae"` | `"cwae"` | Shortest block containing `c`, `a`, `e`. |

---

## 12. Common Mistakes and Debugging

1. **Ignoring duplicates.** Using a `set(t)` makes `s = "a"`, `t = "aa"` return `"a"` instead of `""`.
2. **Decrementing `need` before checking it.** Write `if need[ch] > 0: missing -= 1` **then** `need[ch] -= 1`. Reversed, a spare copy can look "needed".
3. **Recording the window after shrinking past validity.** Record **inside** the `while missing == 0` loop, *before* removing `s[left]`. Recording after the loop measures a window that no longer covers `t`.
4. **Shrinking with `if` instead of `while`.** One removal may not be enough to reach the shortest window (step 12 above removes four characters).
5. **Building the answer string inside the loop** (`best = s[left:right+1]` every time). That costs `O(length)` per update and can make the algorithm much slower; store indices and slice once.
6. **Using `0` as "no answer yet" for `best_len`.** Then `right - left + 1 < best_len` is never true. Use infinity (or `None` with an explicit check).

**Debugging tip:** print `right, left, s[left:right + 1], missing, {c: need[c] for c in set(t)}` after each expand and each shrink, and compare with the dry-run table.

---

## 13. Practice Questions

**Q1. Run the optimized algorithm on `s = "bba"`, `t = "ab"`. What gets recorded?**

<details><summary>Hint</summary>The second `b` is a spare copy, so `need[b]` goes to −1.</summary></details>

**Answer:** Start `need = {a:1, b:1}`, `missing = 2`. `right = 0` (`b`): `missing = 1`, `need[b] = 0`. `right = 1` (`b`): spare, `need[b] = −1`, `missing = 1`. `right = 2` (`a`): `missing = 0`. Shrink: `"bba"` (3) → record; drop `b` → `need[b] = 0`, still covered. `"ba"` (2) → record; drop `b` → `need[b] = 1`, `missing = 1`, stop. **Answer: `"ba"`.**

**Q2. Permutation in String (LeetCode 567): return `True` if some substring of `s2` is a permutation of `s1`.**

<details><summary>Hint</summary>A permutation of `s1` has exactly `len(s1)` characters, so use a **fixed-size** window of that length and compare counts.</summary></details>

**Answer:** Slide a window of length `len(s1)`; add the right character, remove the one that falls off the left, and compare 26-slot counts.

```python
def check_inclusion(s1, s2):
    if len(s1) > len(s2):
        return False
    need = [0] * 26
    window = [0] * 26
    for ch in s1:
        need[ord(ch) - 97] += 1
    for right, ch in enumerate(s2):
        window[ord(ch) - 97] += 1
        if right >= len(s1):                       # drop the char that left
            window[ord(s2[right - len(s1)]) - 97] -= 1
        if window == need:
            return True
    return False


assert check_inclusion("ab", "eidbaooo") is True
assert check_inclusion("ab", "eidboaoo") is False
assert check_inclusion("abc", "ab") is False
```

**Q3. Return only the *length* of the minimum window (0 if none), and explain why the strict `<` matters only for *which* window is returned, not for its length.**

<details><summary>Hint</summary>Ties have the same length by definition.</summary></details>

**Answer:** Keep `best_len` only. With `<` the first (leftmost) shortest window is kept; with `<=` the last one would be kept — but both have the same length.

```python
from collections import Counter


def min_window_length(s, t):
    need = Counter(t)
    missing = len(t)
    left = 0
    best = float("inf")
    for right, ch in enumerate(s):
        if need[ch] > 0:
            missing -= 1
        need[ch] -= 1
        while missing == 0:
            best = min(best, right - left + 1)
            need[s[left]] += 1
            if need[s[left]] > 0:
                missing += 1
            left += 1
    return 0 if best == float("inf") else best


assert min_window_length("ADOBECODEBANC", "ABC") == 4
assert min_window_length("a", "aa") == 0
assert min_window_length("abab", "ab") == 2
```

**Q4. Why is the optimized solution `O(m + n)` and not `O(m²)`?**

<details><summary>Hint</summary>How many times can `left += 1` run in total?</summary></details>

**Answer:** `left` only moves forward and never passes `right + 1`, so the `while` body runs at most `m` times **in total** over the whole algorithm. The `for` loop runs `m` times and building `need` costs `O(n)`. Every operation inside is `O(1)` dictionary work. Total: `O(m + n)`.

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** Sliding window — expand until valid, shrink while valid (minimum-window variant).
- **Key idea:** `need[c]` = copies still required (negative = spare); `missing` = total still required. Valid ⇔ `missing == 0`. Record inside the shrink loop.
- **Time:** `O(m + n)`.
- **Auxiliary space:** `O(k)` distinct characters (≤ 52 → `O(1)` for this alphabet).
- **One-line memory hook:** *"Reach right until the list is complete; let go on the left until it isn't — measure every complete stretch."*

### Completion checklist

- [x] Problem requirements verified
- [x] Examples and constraints verified
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force solution written and tested
- [x] Optimized Python solution written and tested (`tools/tests/p033.py`), including the two-table alternative
- [x] Line-by-line explanation written
- [x] Dry run completed with real examples
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
