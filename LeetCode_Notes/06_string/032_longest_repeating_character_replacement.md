# 032. Longest Repeating Character Replacement

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Longest Repeating Character Replacement |
| **LeetCode number** | 424 |
| **Topic (source list)** | String |
| **Also uses** | Hash Table / frequency counting, Sliding Window |
| **Difficulty** | Medium |
| **LeetCode URL** | <https://leetcode.com/problems/longest-repeating-character-replacement/> |
| **Pattern** | Variable-size sliding window with "window length − most frequent count ≤ k" |

---

## 2. Problem Explanation

### What are we given?

- `s` — a string of uppercase English letters (`'A'` to `'Z'`).
- `k` — how many single-character changes you are allowed to make.

### What must we return?

The length of the longest block of **identical letters** you can create, if you may change **at most `k`** characters of `s` into any other uppercase letter.

### The rules

1. One operation = pick one position and change its letter to any uppercase letter. You may do this **at most `k` times** (fewer is fine, including zero).
2. The block must be a **substring** — contiguous positions of `s`.
3. Only the **length** is returned.

### Restating it as a window question

Pick a substring (window). Inside it, keep the letter that appears the most and change all the others. That costs

```text
changes needed = window length − (count of the most frequent letter in the window)
```

The window can be turned into one repeated letter exactly when `changes needed <= k`. So the problem becomes: **find the longest window where `length − most_frequent_count <= k`.**

### Examples

**Example 1**

```text
Input:  s = "ABAB", k = 2
Output: 4
```

Change both `A`s into `B`s (or both `B`s into `A`s) to get `"BBBB"` (or `"AAAA"`). Length 4.

**Example 2**

```text
Input:  s = "AABABBA", k = 1
Output: 4
```

Change the `A` at index 3 into `B`: `"AABBBBA"` contains `"BBBB"`, length 4. Other choices also reach 4 (for example, change index 2 to get `"AAAA"` from `"AABA"`), but nothing reaches 5 with only one change.

### Constraints

- `1 <= s.length <= 10^5`
- `s` consists of only uppercase English letters.
- `0 <= k <= s.length`

**Follow-up:** none in the statement.

---

## 3. Everyday Analogy

> **Explain it like I'm five**

You have a row of coloured socks and **`k` cans of paint**. You want the longest run of socks next to each other that are all the same colour. One can of paint repaints one sock.

Look at any stretch of socks. The cheapest plan is to keep the colour you have **most** of and paint all the others. If the "others" are no more than your paint cans, the stretch works!

So you hold a **frame** over the row:

- Slide its right edge out to include one more sock.
- If you'd need more paint than you have, slide the left edge in by one sock.
- Remember the widest frame that ever worked.

---

## 4. Step-by-Step Logic

1. **Cost of a window** = `length − max_count`, where `max_count` is how often the most common letter appears in it.
2. **Valid window** ⇔ `length − max_count <= k`.
3. **Expand** with `right`: add `s[right]` to a `counts` table (26 letters).
4. **Shrink** with `left` when the window is too expensive.
5. **Record** the window length.
6. **Monotonic idea:** if a window is invalid, every larger window that contains it is also invalid (adding a letter increases length by 1 and `max_count` by at most 1, so the cost never drops). That's why moving `left` only forwards is safe.
7. **The famous shortcut (`max_count` never decreases):** recomputing the true `max_count` after every shrink would cost up to 26 steps. The standard solution instead keeps `max_count` as the **largest single-letter count ever seen in any window so far** and never lowers it. Section 6 explains exactly why this still gives the right answer.

---

## 5. Brute-Force Solution

### Algorithm

1. For every start `i`, extend the end `j` to the right, updating a 26-slot `counts` table and the window's most-frequent count `most`.
2. If `(j - i + 1) - most <= k`, the window is valid: update `best`.
3. Otherwise `break`: extending the end can only keep the cost the same or raise it (length +1, `most` at most +1), so no longer window from `i` can be valid.

### Python code

```python
class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        n = len(s)
        best = 0
        for i in range(n):
            counts = [0] * 26
            most = 0
            for j in range(i, n):
                idx = ord(s[j]) - ord('A')
                counts[idx] += 1
                most = max(most, counts[idx])    # true max for s[i..j]
                if (j - i + 1) - most <= k:
                    best = max(best, j - i + 1)
                else:
                    break                        # longer windows from i also fail
        return best
```

### Explanation

- `ord(ch) - ord('A')` maps `'A'..'Z'` to `0..25`.
- Inside a fixed start `i`, counts only increase, so `most = max(most, counts[idx])` is the exact maximum for `s[i..j]`.
- The `break` is safe because of the monotonic idea in Section 4, step 6.

### Complexity

- **Time:** `O(n²)` in the worst case (e.g. a large `k` lets every inner loop run to the end). For `n = 10^5` that is about 5 billion steps → **times out** on LeetCode.
- **Auxiliary space:** `O(1)` — a 26-slot list.

---

## 6. Optimized Solution

### Idea

Sliding window with a `max_count` that is **never decreased**.

### Algorithm

1. `counts = [0] * 26`, `left = 0`, `max_count = 0`, `best = 0`.
2. For each `right`:
   1. `counts[s[right]] += 1`; `max_count = max(max_count, counts[s[right]])`.
   2. While `(right - left + 1) - max_count > k`: `counts[s[left]] -= 1`, `left += 1`.
   3. `best = max(best, right - left + 1)`.
3. Return `best`.

### Python code (LeetCode-ready)

```python
class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        counts = [0] * 26
        left = 0
        max_count = 0    # largest single-letter count seen in any window so far
        best = 0

        for right in range(len(s)):
            idx = ord(s[right]) - ord('A')
            counts[idx] += 1                          # expand
            max_count = max(max_count, counts[idx])

            while (right - left + 1) - max_count > k: # too many changes needed
                counts[ord(s[left]) - ord('A')] -= 1  # shrink
                left += 1

            best = max(best, right - left + 1)

        return best
```

(With this `max_count` rule the `while` runs **at most once** per step, so you will often see it written as `if`. Both are correct.)

### Why `max_count` never needs to decrease — stated precisely

When `left` moves, the true most-frequent count of the window may drop, but we keep the old, larger `max_count`. Call it **stale**. Here is the exact claim and why it is safe:

**Claim.** `best` (the returned value) is always the length of some window that is *genuinely* valid, and it reaches the true optimum.

1. **Invariant.** Before the first shrink ever happens, `left = 0` and `max_count` is the exact maximum for the window. Once shrinking starts, the window length is always exactly `max_count + k` (a shrink happens only when the length hits `max_count + k + 1`, and it removes one character). So the window **never shrinks below** its previous length — it either **slides** (same length) or **grows**.
2. **Growth only happens for real.** After the first shrink, the window can only grow when `max_count` itself increases, and `max_count` only increases when the letter just added reaches a **new record count inside the current window**. At that moment `max_count` is the *true* count of a letter in the window, and `length − max_count = k`, so this window is **genuinely valid**. Before the first shrink, the window is valid by the exact count. Therefore every length that `best` records was achieved by a genuinely valid window.
3. **Stale windows are harmless.** While `max_count` is stale, the current window may actually need more than `k` changes — but it is only sliding at a length we have **already** proved achievable, so `best` does not increase because of it.
4. **We never miss a longer answer.** Intuition: to beat the current length `L = max_count + k`, a window of length `L + 1` needs some letter with count at least `L + 1 − k = max_count + 1` — strictly more than any count seen so far. Lowering `max_count` would never help us detect that; only a new record can, and `max(max_count, counts[idx])` catches it. Rigorous version: let `s[a..b]` be a best valid window. Two small facts: (i) `max_count` is always ≥ the true maximum count of the current window (each letter's count was at least its current value when that letter was last added), and (ii) any piece `s[a..r]` of a valid window is also valid (removing characters from the right end lowers the length by at least as much as it lowers any letter's count). Now, while `right ≤ b`, could the code shrink with `left = a`? That would require `len(s[a..right]) − max_count > k`, i.e. `len > max_count + k ≥ true max + k`, which contradicts (ii). So `left` never passes `a` before `right` reaches `b`, and at that moment the window covers `s[a..b]` — its length, and so `best`, is at least the optimum.

So the precise statement is: *`max_count` is the largest single-letter count seen in any window so far; it may over-estimate the current window's true maximum, but the answer can only improve when some letter beats that record, so keeping the old value never produces a wrong answer.* It does **not** mean "the current window is always valid" — it might not be.

### Alternative: recompute the true maximum (easier to trust, `O(26 · n)`)

```python
class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        counts = [0] * 26
        left = 0
        best = 0
        for right in range(len(s)):
            counts[ord(s[right]) - ord('A')] += 1
            while (right - left + 1) - max(counts) > k:  # exact max, 26 checks
                counts[ord(s[left]) - ord('A')] -= 1
                left += 1
            best = max(best, right - left + 1)
        return best
```

Here every window kept after the `while` is genuinely valid. It costs 26 extra checks per step, which is still linear for a fixed alphabet.

---

## 7. Line-by-Line Explanation

(Main optimized version)

| Line | What it does | Why |
|---|---|---|
| `counts = [0] * 26` | One counter per uppercase letter. | Fixed alphabet → a list is simpler and faster than a dict. |
| `left = 0` | Left edge of the window. | Window is `s[left..right]`. |
| `max_count = 0` | Record single-letter count seen so far. | Used to compute the cost without scanning 26 counters. |
| `best = 0` | Longest window recorded. | Updated after every step. |
| `for right in range(len(s)):` | Moves the right edge across `s`. | Each character enters the window once. |
| `idx = ord(s[right]) - ord('A')` | Converts the letter to `0..25`. | Index into `counts`. |
| `counts[idx] += 1` | Adds the new letter to the window. | **Expand** step. |
| `max_count = max(max_count, counts[idx])` | Raises the record if this letter just beat it. | Only the newly added letter's count changed, so it is the only candidate for a new record. |
| `while (right - left + 1) - max_count > k:` | Window needs more than `k` changes (according to `max_count`). | **Shrink** condition. |
| `counts[ord(s[left]) - ord('A')] -= 1` | Removes the leftmost letter. | Keeps `counts` exact for the window. (`max_count` is deliberately *not* lowered.) |
| `left += 1` | Moves the left edge. | Window shrinks by one. |
| `best = max(best, right - left + 1)` | Records the current window length. | By the claim in Section 6, this never exceeds a genuinely achievable length. |
| `return best` | Answer. | — |

---

## 8. Dry Run

**Input:** `s = "AABABBA"`, `k = 1` (Example 2). Indices: `A0 A1 B2 A3 B4 B5 A6`.

"Len before" is the window length right after adding `s[right]`; "cost" is `len before − max_count`.

| `right` | `ch` | `counts` after add | `max_count` | Len before | Cost | Shrink? | `left` | Window after | `counts` after | `best` |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | A | `{A:1}` | 1 | 1 | 0 | no | 0 | `"A"` | `{A:1}` | 1 |
| 1 | A | `{A:2}` | 2 | 2 | 0 | no | 0 | `"AA"` | `{A:2}` | 2 |
| 2 | B | `{A:2, B:1}` | 2 | 3 | 1 | no | 0 | `"AAB"` | `{A:2, B:1}` | 3 |
| 3 | A | `{A:3, B:1}` | 3 | 4 | 1 | no | 0 | `"AABA"` | `{A:3, B:1}` | **4** |
| 4 | B | `{A:3, B:2}` | 3 | 5 | 2 > 1 | remove `A` (idx 0) | 1 | `"ABAB"` | `{A:2, B:2}` | 4 |
| 5 | B | `{A:2, B:3}` | 3 | 5 | 2 > 1 | remove `A` (idx 1) | 2 | `"BABB"` | `{A:1, B:3}` | 4 |
| 6 | A | `{A:2, B:3}` | 3 | 5 | 2 > 1 | remove `B` (idx 2) | 3 | `"ABBA"` | `{A:2, B:2}` | 4 |

**Result:** `4` ✅

**Look at step 4 — the stale `max_count` in action.** After the shrink the window is `"ABAB"`, whose true most-frequent count is 2, so it really needs 2 changes (more than `k = 1`). The code still believes `max_count = 3`. That's fine: the window is merely sliding at length 4, which was already proven achievable by `"AABA"` at step 3. At step 5 the window `"BABB"` (true max 3 for `B`) is genuinely valid again. `best` never went above 4.

**Second dry run:** `s = "ABAB"`, `k = 2` (Example 1)

| `right` | `ch` | `counts` | `max_count` | Len | Cost | Shrink? | `left` | Window | `best` |
|---|---|---|---|---|---|---|---|---|---|
| 0 | A | `{A:1}` | 1 | 1 | 0 | no | 0 | `"A"` | 1 |
| 1 | B | `{A:1, B:1}` | 1 | 2 | 1 | no | 0 | `"AB"` | 2 |
| 2 | A | `{A:2, B:1}` | 2 | 3 | 1 | no | 0 | `"ABA"` | 3 |
| 3 | B | `{A:2, B:2}` | 2 | 4 | 2 | no (2 ≤ 2) | 0 | `"ABAB"` | **4** |

**Result:** `4` ✅

---

## 9. Concepts, Data Structures, and Patterns

- **Sliding window (variable size):** expand right, shrink left while invalid. Same skeleton as [031. Longest Substring Without Repeating Characters](031_longest_substring_without_repeating_characters.md).
- **Reframing the goal:** "longest block after ≤ k replacements" ⇔ "longest window with `length − max_count ≤ k`". Turning an operation-based question into a property of a window is the key insight.
- **Fixed-alphabet counting array:** `counts = [0] * 26` with `ord(ch) - ord('A')` indexing — the same trick used in [034. Valid Anagram](034_valid_anagram.md).
- **Monotonic / "never shrink the answer" window:** because we only care about the *maximum* length, the window is allowed to slide while invalid; it only needs to grow when a genuinely better window appears.
- **Amortized analysis:** `left` only moves forward, so all shrink steps together cost `O(n)`.
- **Related notes:** [033. Minimum Window Substring](033_minimum_window_substring.md) (sliding window for the *shortest* valid window).

---

## 10. Complexity Analysis

Let `n = len(s)` and the alphabet size be 26 (fixed by the constraints).

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Brute force | `O(n²)` | `O(1)` (26 counters) | Every start index, extending until the cost exceeds `k`. |
| Sliding window, stale `max_count` | `O(n)` | `O(1)` (26 counters) | Each character enters once and leaves at most once; each step does `O(1)` work. |
| Sliding window, exact `max(counts)` | `O(26 · n)` = `O(n)` | `O(1)` | Same window moves, but each check scans 26 counters. For a general alphabet of size `a` this would be `O(a · n)` time and `O(a)` space. |

---

## 11. Edge Cases

| Case | Example | Expected result | Why |
|---|---|---|---|
| Single character | `"A"`, `k = 0` | `1` | Already one repeated letter. |
| `k` larger than needed | `"A"`, `k = 1` | `1` | You can't exceed the string length. |
| No changes allowed | `"AAABBC"`, `k = 0` | `3` | Longest existing run `"AAA"`. |
| All distinct, `k = 0` | `"ABCD"`, `k = 0` | `1` | Every longer window needs a change. |
| `k = len(s)` | `"ABCD"`, `k = 4` | `4` | Whole string can be repainted. |
| Already uniform | `"AAAA"`, `k = 0` | `4` | Cost 0 for the whole string. |
| Odd letters at both ends | `"BAAAB"`, `k = 2` | `5` | Change both `B`s. |
| Best window at the end | `"ABBB"`, `k = 2` | `4` | Whole string; cost is 1. |

---

## 12. Common Mistakes and Debugging

1. **Thinking `max_count` must be recomputed after every shrink.** Not required (Section 6) — but if you're unsure in an interview, the `max(counts)` version is also linear for 26 letters and easy to defend.
2. **Over-claiming about the stale version.** It is *not* true that "the current window is always valid". The correct claim is that `best` never exceeds a genuinely achievable length.
3. **Using `len(set(window))` or the number of distinct letters** instead of `length − max_count`. Cost depends on how many letters are *not* the majority letter, not on how many kinds there are.
4. **Using `>=` instead of `>`** in the shrink condition: a window with exactly `k` changes needed is allowed.
5. **Forgetting to decrement `counts` when `left` moves**, so counts describe characters that are no longer in the window.
6. **Returning `max_count + k`.** That can exceed `len(s)` (e.g. `"A"`, `k = 1` would give 2). Return a real window length.

**Debugging tip:** print `right, left, s[left:right + 1], max_count, max(counts)` each step. When `max_count > max(counts)` you're looking at a stale (sliding) window — that's expected.

---

## 13. Practice Questions

**Q1. Trace the optimized solution on `s = "AAABBC"`, `k = 0`. When does the first shrink happen, and what is the answer?**

<details><summary>Hint</summary>With `k = 0`, the window must be all one letter (according to `max_count`).</summary></details>

**Answer:** Steps 0–2 build `"AAA"` with `max_count = 3`, `best = 3`. At `right = 3` (`B`) the length is 4 and cost `4 − 3 = 1 > 0`, so the **first shrink** removes `A` → window `"AAB"` (stale: true max is 2). At `right = 4` (`B`) the cost is again 1 → remove `A` → `"ABB"`. At `right = 5` (`C`) → remove `A` → `"BBC"`. `max_count` never exceeds 3, so the window never grows past 3. **Answer: `3`.**

**Q2. Solve it a different way: for each letter `c`, find the longest window containing at most `k` letters that are *not* `c`.**

<details><summary>Hint</summary>For a fixed target letter, this is a sliding window where the "bad" count must stay ≤ `k`.</summary></details>

**Answer:** Try all 26 targets; each is a simple window. Total `O(26 · n)`.

```python
def char_replacement_per_letter(s, k):
    best = 0
    for target in set(s):
        left = bad = 0
        for right, ch in enumerate(s):
            if ch != target:
                bad += 1
            while bad > k:
                if s[left] != target:
                    bad -= 1
                left += 1
            best = max(best, right - left + 1)
    return best


assert char_replacement_per_letter("ABAB", 2) == 4
assert char_replacement_per_letter("AABABBA", 1) == 4
assert char_replacement_per_letter("A", 0) == 1
```

**Q3. Max Consecutive Ones III (LeetCode 1004):** given a binary list `nums` and `k`, return the longest run of 1s if you may flip at most `k` zeros.

<details><summary>Hint</summary>It's Q2 with only one target letter (1).</summary></details>

**Answer:**

```python
def longest_ones(nums, k):
    left = zeros = best = 0
    for right, x in enumerate(nums):
        if x == 0:
            zeros += 1
        while zeros > k:
            if nums[left] == 0:
                zeros -= 1
            left += 1
        best = max(best, right - left + 1)
    return best


assert longest_ones([1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0], 2) == 6
assert longest_ones([0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1], 3) == 10
assert longest_ones([0, 0], 0) == 0
```

**Q4. In the main optimized solution, why does the `while` loop run at most once per `right`?**

<details><summary>Hint</summary>Compare the window length with `max_count + k` before and after adding one character.</summary></details>

**Answer:** Before adding `s[right]`, the window satisfies `length − max_count ≤ k`. Adding one character raises `length` by exactly 1 and `max_count` by 0 or 1, so the cost rises by at most 1 — to at most `k + 1`. One removal lowers `length` by 1 while `max_count` stays the same, bringing the cost back to at most `k`. So one shrink always suffices, and `if` works just as well as `while`.

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** Sliding window; valid ⇔ `window length − max_count ≤ k`.
- **Key idea:** Keep the most common letter and repaint the rest. `max_count` is the record count seen so far and never needs to drop: the answer can only improve when some letter beats that record.
- **Time:** `O(n)`.
- **Auxiliary space:** `O(1)` (26 counters).
- **One-line memory hook:** *"Keep the majority, paint the rest; the frame only grows when a colour sets a new record."*

### Completion checklist

- [x] Problem requirements verified
- [x] Examples and constraints verified
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force solution written and tested
- [x] Optimized Python solution written and tested (`tools/tests/p032.py`), including the exact-`max(counts)` alternative
- [x] Line-by-line explanation written
- [x] Dry run completed with real examples
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
