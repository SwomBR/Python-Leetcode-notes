# 031. Longest Substring Without Repeating Characters

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Longest Substring Without Repeating Characters |
| **LeetCode number** | 3 |
| **Topic (source list)** | String |
| **Also uses** | Hash Table, Sliding Window |
| **Difficulty** | Medium |
| **LeetCode URL** | <https://leetcode.com/problems/longest-substring-without-repeating-characters/> |
| **Pattern** | Variable-size sliding window (expand right, shrink left) |

---

## 2. Problem Explanation

### What are we given?

`s` — a string. It may be empty, and it can contain English letters, digits, symbols and spaces.

### What must we return?

A single integer: the **length** of the longest **substring** of `s` in which **no character appears twice**.

### The rules

1. A **substring** is a block of characters that sit **next to each other** in `s`. You may not skip characters. For `s = "pwwkew"`, `"wke"` is a substring, but `"pwke"` is not (it skips the second `w`) — that would be a *subsequence*.
2. "Without repeating characters" means every character inside the block is different. Characters are compared exactly: `'a'` and `'A'` are different, and a space `' '` is a character too.
3. We only return the **length**, not the substring itself. If several substrings tie, it doesn't matter which one you think of.
4. The empty string has no characters, so the answer for `""` is `0`.

### Examples

**Example 1**

```text
Input:  s = "abcabcbb"
Output: 3
```

`"abc"` has 3 different characters. `"bca"` and `"cab"` also have length 3. Nothing longer works: any block of 4 characters here contains a repeat.

**Example 2**

```text
Input:  s = "bbbbb"
Output: 1
```

Every block of 2 or more characters is `"bb..."`, which repeats `b`. The best is a single `"b"`.

**Example 3**

```text
Input:  s = "pwwkew"
Output: 3
```

`"wke"` has length 3. `"pwke"` would be 4, but it is not a substring because it is not contiguous.

### Constraints

- `0 <= s.length <= 10^5`
- `s` consists of English letters, digits, symbols and spaces.

**Follow-up:** none in the statement.

---

## 3. Everyday Analogy

> **Explain it like I'm five**

You are threading beads onto a string, one at a time, from a long box of beads lined up in order. Your rule: **no two beads on your string may be the same colour.**

- You keep adding the next bead on the **right** end.
- If the new bead's colour is **already** on your string, you slide beads off the **left** end, one by one, until the old bead of that colour falls off. Now the colours are all different again.
- After each new bead, you measure your string and remember the **longest** it has ever been.

You never go back to the start of the box, and every bead is put on once and taken off at most once. The longest string you ever measured is the answer.

---

## 4. Step-by-Step Logic

1. **The answer is a contiguous block**, so describe a block with two positions: `left` (where it starts) and `right` (where it ends). The block `s[left..right]` is called the **window**.
2. **Expand:** move `right` forward one character at a time, adding `s[right]` to the window.
3. **Is the window still valid?** It is valid when no character inside appears twice. Adding `s[right]` can only break this for **one** character: `s[right]` itself.
4. **Shrink:** while `s[right]` appears more than once in the window, remove `s[left]` and move `left` forward. Eventually the earlier copy of `s[right]` leaves and the window is valid again.
5. **Record:** the valid window has length `right - left + 1`; keep the maximum.
6. **Why it's safe to never move `left` backwards:** if `s[left..right]` contains a repeat, then any window that starts *earlier* and ends at `right` also contains that repeat. So once a start position is ruled out for `right`, it is ruled out for every later `right` as well.
7. **Fast "is it in the window?" checks:** keep a dictionary `counts` of how many times each character appears in the window. Each update is `O(1)`.

This "expand on the right, shrink on the left while the window is broken" loop is the general **sliding window** template you will reuse in [032](032_longest_repeating_character_replacement.md) and [033](033_minimum_window_substring.md).

---

## 5. Brute-Force Solution

### Algorithm

1. For every start index `i`:
2. Walk an end index `j` from `i` to the right, adding `s[j]` to a set `seen`.
3. As soon as `s[j]` is already in `seen`, stop — every longer block starting at `i` would contain this repeat too.
4. Otherwise update the best length with `j - i + 1`.

### Python code

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        best = 0
        n = len(s)
        for i in range(n):
            seen = set()
            for j in range(i, n):
                if s[j] in seen:
                    break            # s[i..j] has a repeat; longer blocks would too
                seen.add(s[j])
                best = max(best, j - i + 1)
        return best
```

### Explanation

- Each start `i` gets a fresh empty set.
- The inner loop grows the block one character at a time and stops at the first repeated character.
- The `break` is an important small optimization, but it does not change the worst case much.
- For `s = ""`, `n = 0`, neither loop runs and we return `0`.

### Complexity

- **Time:** `O(n · min(n, a))`, where `a` is the number of distinct characters that can appear. The inner loop can run at most `min(n, a) + 1` times before it must hit a repeat (pigeonhole principle). With printable characters (`a` ≈ 95) this is fast in practice, but for a general alphabet it is `O(n²)` — with `n = 10^5` and many distinct characters it could be billions of steps, so treat it as the slow approach.
- **Auxiliary space:** `O(min(n, a))` for the set.

---

## 6. Optimized Solution

### Idea

Use the sliding window from Section 4. Each character enters the window once (when `right` reaches it) and leaves at most once (when `left` passes it), so the total work is linear.

### Algorithm

1. `counts = {}`, `left = 0`, `best = 0`.
2. For each `right` from `0` to `n - 1`:
   1. Add `s[right]`: `counts[s[right]] += 1`.
   2. While `counts[s[right]] > 1`: decrease `counts[s[left]]` and move `left` forward.
   3. `best = max(best, right - left + 1)`.
3. Return `best`.

### Python code (LeetCode-ready)

```python
from collections import defaultdict


class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        counts = defaultdict(int)   # character -> how many times it is in the window
        left = 0
        best = 0

        for right, ch in enumerate(s):
            counts[ch] += 1                 # expand: s[right] joins the window

            while counts[ch] > 1:           # shrink until ch is unique again
                counts[s[left]] -= 1
                left += 1

            best = max(best, right - left + 1)

        return best
```

### Alternative: jump `left` directly (last-seen index)

Instead of removing characters one by one, remember the **last index** where each character was seen. When `s[right]` was last seen **inside** the current window, jump `left` to just after that position.

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        last_seen = {}   # character -> most recent index
        left = 0
        best = 0

        for right, ch in enumerate(s):
            if ch in last_seen and last_seen[ch] >= left:
                left = last_seen[ch] + 1    # skip past the previous copy
            last_seen[ch] = right
            best = max(best, right - left + 1)

        return best
```

The check `last_seen[ch] >= left` is essential: an old position that is already **outside** the window must not move `left` backwards (try `s = "abba"`).

---

## 7. Line-by-Line Explanation

(Counting version)

| Line | What it does | Why |
|---|---|---|
| `counts = defaultdict(int)` | A dictionary whose missing keys start at `0`. | Lets us write `counts[ch] += 1` without first checking whether `ch` exists. |
| `left = 0` | The window starts at index 0. | Initially the window is empty (`right` hasn't moved yet). |
| `best = 0` | Longest valid length found so far. | Correct answer for an empty string. |
| `for right, ch in enumerate(s):` | Moves the right edge across the string, one character at a time. | Every possible end position is visited once. |
| `counts[ch] += 1` | Puts `ch` into the window. | This is the **expand** step. |
| `while counts[ch] > 1:` | Is `ch` now duplicated? | Only the newly added character can be the duplicate — the window was valid before this step. |
| `counts[s[left]] -= 1` | Takes the leftmost character out of the window. | This is the **shrink** step. |
| `left += 1` | Moves the left edge forward. | The window is now `s[left..right]`. The loop repeats until the earlier copy of `ch` has been removed. |
| `best = max(best, right - left + 1)` | Records the current window's length. | After the `while`, the window has no repeats, so it is a valid candidate. |
| `return best` | Returns the answer. | — |

**Why the total work is `O(n)` even with a loop inside a loop:** `left` only moves forward and never passes `right`, so across the **whole run** the `while` body executes at most `n` times in total. Together with the `n` iterations of the `for`, that is at most `2n` steps.

---

## 8. Dry Run

**Input:** `s = "abcabcbb"` (Example 1), counting version.

`counts` is shown after the step (characters with count 0 are omitted for readability).

| `right` | `ch` | Expand: `counts` after adding | Shrink steps (removed chars) | `left` | Window `s[left..right]` | `counts` after shrink | Length | `best` |
|---|---|---|---|---|---|---|---|---|
| 0 | `a` | `{a:1}` | — | 0 | `"a"` | `{a:1}` | 1 | 1 |
| 1 | `b` | `{a:1, b:1}` | — | 0 | `"ab"` | `{a:1, b:1}` | 2 | 2 |
| 2 | `c` | `{a:1, b:1, c:1}` | — | 0 | `"abc"` | `{a:1, b:1, c:1}` | 3 | **3** |
| 3 | `a` | `{a:2, b:1, c:1}` | remove `a` | 1 | `"bca"` | `{a:1, b:1, c:1}` | 3 | 3 |
| 4 | `b` | `{a:1, b:2, c:1}` | remove `b` | 2 | `"cab"` | `{a:1, b:1, c:1}` | 3 | 3 |
| 5 | `c` | `{a:1, b:1, c:2}` | remove `c` | 3 | `"abc"` | `{a:1, b:1, c:1}` | 3 | 3 |
| 6 | `b` | `{a:1, b:2, c:1}` | remove `a`, remove `b` | 5 | `"cb"` | `{b:1, c:1}` | 2 | 3 |
| 7 | `b` | `{b:2, c:1}` | remove `c`, remove `b` | 7 | `"b"` | `{b:1}` | 1 | 3 |

**Result:** `3` ✅

Notice step 6: the duplicate `b` was at index 4, so `left` had to move past both `a` (index 3) and `b` (index 4).

**Second dry run:** `s = "pwwkew"` (Example 3)

| `right` | `ch` | Removed | `left` | Window | `counts` | Length | `best` |
|---|---|---|---|---|---|---|---|
| 0 | `p` | — | 0 | `"p"` | `{p:1}` | 1 | 1 |
| 1 | `w` | — | 0 | `"pw"` | `{p:1, w:1}` | 2 | 2 |
| 2 | `w` | `p`, `w` | 2 | `"w"` | `{w:1}` | 1 | 2 |
| 3 | `k` | — | 2 | `"wk"` | `{w:1, k:1}` | 2 | 2 |
| 4 | `e` | — | 2 | `"wke"` | `{w:1, k:1, e:1}` | 3 | **3** |
| 5 | `w` | `w` | 3 | `"kew"` | `{k:1, e:1, w:1}` | 3 | 3 |

**Result:** `3` ✅

**Jump version on `"abcabcbb"`:** `left` goes `0, 0, 0, 1, 2, 3, 5, 7` — exactly the same windows as above, but each jump happens in one step instead of a `while` loop.

---

## 9. Concepts, Data Structures, and Patterns

- **Sliding window (variable size):** two indices `left` and `right` move only forward. `right` grows the window; `left` shrinks it when a rule is broken. Pattern template:

  ```text
  for right in range(n):
      add s[right] to window state
      while window is invalid:
          remove s[left] from window state
          left += 1
      update answer using the (now valid) window
  ```

- **Hash map / frequency counter:** `counts` (or `last_seen`) answers "how many of `ch` are in the window?" in `O(1)` average time.
- **Monotonic pointers / amortized analysis:** because `left` never moves backwards, the inner loop's total cost over the whole run is `O(n)`, even though it sits inside a `for` loop.
- **Substring vs subsequence:** substrings are contiguous; subsequences may skip characters.
- **`collections.defaultdict(int)`:** a dictionary that returns `0` for missing keys.
- **Related notes in this project:**
  - [032. Longest Repeating Character Replacement](032_longest_repeating_character_replacement.md) — same window, different validity rule.
  - [033. Minimum Window Substring](033_minimum_window_substring.md) — the window is shrunk while it is *valid*, to find the *shortest*.
  - [003. Contains Duplicate](../01_array/003_contains_duplicate.md) — the "have I seen this before?" set idea used in the brute force.
  - [001. Two Sum](../01_array/001_two_sum.md) — another hash-map-remembers-the-past problem.

---

## 10. Complexity Analysis

Let `n = len(s)` and `a` = the number of distinct characters that can appear (for this problem, printable ASCII, so `a` is a small constant ≈ 95).

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Brute force | `O(n · min(n, a))` (`O(n²)` for a general alphabet) | `O(min(n, a))` | Every start index; each inner walk stops after at most `min(n, a) + 1` characters. |
| Sliding window with counts | `O(n)` | `O(min(n, a))` | Each character is added once and removed at most once. The dictionary holds only characters currently in the window, and the window never has more than `a` distinct characters. |
| Jump with last-seen index | `O(n)` | `O(min(n, a))` | One pass; the dictionary stores one index per distinct character seen. |

Since `a` is bounded for this problem's character set, the space can also be described as `O(1)` (at most ~95 entries) — but `O(min(n, a))` is the more informative answer.

---

## 11. Edge Cases

| Case | Example | Expected result | Why |
|---|---|---|---|
| Empty string | `""` | `0` | No characters at all; the loop never runs. |
| Single space | `" "` | `1` | A space is a valid character. |
| All the same | `"bbbbb"` | `1` | Every window longer than 1 repeats `b`. |
| All different | `"abcdefghijklmnopqrstuvwxyz"` | `26` | The whole string is valid. |
| Repeat that is outside the window | `"abba"` | `2` | At the last `a`, the old `a` (index 0) is already outside the window `"b"`; the jump version must not move `left` back to 1. |
| Answer in the middle | `"dvdf"` | `3` | `"vdf"`; `left` must move only past the first `d`, not reset to `right`. |
| Duplicate far apart | `"tmmzuxt"` | `5` | `"mzuxt"`; the final `t` repeats index 0, which is already outside the window. |
| Mixed symbols and spaces | `"a b!a"` | `4` | `"a b!"` or `" b!a"`. |

---

## 12. Common Mistakes and Debugging

1. **Resetting `left = right` on a repeat.** For `"dvdf"`, when the second `d` arrives, jumping `left` to index 2 loses `"vdf"`. You must move `left` to **just after the previous copy**, which may be much earlier than `right`.
2. **Moving `left` backwards** in the jump version. Without `last_seen[ch] >= left` (or `left = max(left, last_seen[ch] + 1)`), `"abba"` gives `3` instead of `2`.
3. **Updating `best` before shrinking.** Then you measure a window that still contains a repeat.
4. **Using a set but forgetting to remove from it.** If the window state isn't updated when `left` moves, characters that already left still look "inside".
5. **Confusing substring with subsequence.** Counting distinct characters in the whole string (`len(set(s))`) gives `4` for `"pwwkew"`, but the answer is `3`.
6. **Off-by-one in the length.** The window `s[left..right]` (both inclusive) has `right - left + 1` characters.

**Debugging tip:** print `right, ch, left, s[left:right + 1], dict(counts)` after the shrink loop and compare it with the dry-run table above.

---

## 13. Practice Questions

**Q1. Trace the counting version on `s = "dvdf"`. What is `left` after each step, and what's the answer?**

<details><summary>Hint</summary>When the second `d` arrives, only the first `d` needs to leave the window.</summary></details>

**Answer:** `right = 0` (`d`): window `"d"`, `left = 0`, best 1. `right = 1` (`v`): `"dv"`, best 2. `right = 2` (`d`): `counts[d] = 2`, remove `d` → `left = 1`, window `"vd"`, best 2. `right = 3` (`f`): `"vdf"`, best **3**. Answer: `3`.

**Q2. Return the longest substring itself (the first one found if there's a tie), not just its length.**

<details><summary>Hint</summary>Whenever `best` improves, remember where the window starts.</summary></details>

**Answer:** Save `best_start` whenever the length strictly improves, then slice.

```python
def longest_unique_substring(s):
    last_seen = {}
    left = best_start = best_len = 0
    for right, ch in enumerate(s):
        if ch in last_seen and last_seen[ch] >= left:
            left = last_seen[ch] + 1
        last_seen[ch] = right
        if right - left + 1 > best_len:
            best_len = right - left + 1
            best_start = left
    return s[best_start:best_start + best_len]


assert longest_unique_substring("abcabcbb") == "abc"
assert longest_unique_substring("pwwkew") == "wke"
assert longest_unique_substring("bbbbb") == "b"
assert longest_unique_substring("") == ""
```

**Q3. Longest substring with at most `k` distinct characters** (LeetCode 340, a premium problem). For `s = "eceba"`, `k = 2` the answer is `3` (`"ece"`).

<details><summary>Hint</summary>Same template; the window is invalid when `len(counts) > k`. Delete a key when its count drops to 0.</summary></details>

**Answer:** Only the validity rule changes.

```python
from collections import defaultdict


def longest_at_most_k_distinct(s, k):
    counts = defaultdict(int)
    left = best = 0
    for right, ch in enumerate(s):
        counts[ch] += 1
        while len(counts) > k:
            counts[s[left]] -= 1
            if counts[s[left]] == 0:
                del counts[s[left]]      # so len(counts) = number of distinct chars
            left += 1
        best = max(best, right - left + 1)
    return best


assert longest_at_most_k_distinct("eceba", 2) == 3
assert longest_at_most_k_distinct("aa", 1) == 2
assert longest_at_most_k_distinct("abc", 0) == 0
```

**Q4. Why is the counting version `O(n)` and not `O(n²)`, even though it has a `while` loop inside a `for` loop?**

<details><summary>Hint</summary>Count how many times `left += 1` can run in total.</summary></details>

**Answer:** `left` starts at 0, only increases, and never goes beyond `right + 1 <= n`. So `left += 1` runs at most `n` times **over the entire algorithm**, not per iteration. The `for` loop runs `n` times. Total work: at most `2n` window updates → `O(n)`. This style of reasoning is called **amortized analysis**.

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** Variable-size sliding window + hash map.
- **Key idea:** Expand with `right`; while `s[right]` is duplicated, shrink from `left`; record `right - left + 1`.
- **Shortcut version:** `left = max(left, last_seen[ch] + 1)`.
- **Time:** `O(n)`.
- **Auxiliary space:** `O(min(n, a))` (`a` = character set size).
- **One-line memory hook:** *"New bead on the right; if its colour's already there, slide beads off the left until it isn't."*

### Completion checklist

- [x] Problem requirements verified
- [x] Examples and constraints verified
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force solution written and tested
- [x] Optimized Python solution written and tested (`tools/tests/p031.py`), including the last-seen-index alternative
- [x] Line-by-line explanation written
- [x] Dry run completed with real examples
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
