# 057. Longest Increasing Subsequence

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Longest Increasing Subsequence |
| **LeetCode number** | 300 |
| **Topic (source list)** | Dynamic Programming |
| **Also uses** | Binary Search (`bisect`), Greedy |
| **Difficulty** | Medium |
| **LeetCode URL** | <https://leetcode.com/problems/longest-increasing-subsequence/> |
| **Pattern** | DP "best ending at `i`" (`O(n²)`) → patience sorting with binary search (`O(n log n)`) |

---

## 2. Problem Explanation

### What are we given?

`nums` — a list of integers.

### What must we return?

The **length** of the longest **strictly increasing subsequence** of `nums`.

### Key words

- A **subsequence** keeps some of the elements (possibly all) **in their original order**, but is allowed to **skip** elements. For `[10, 9, 2, 5]`, `[10, 5]` and `[2, 5]` are subsequences; `[5, 2]` is not (order changed).
- **Strictly increasing** means every element is **bigger** than the one before it. Equal neighbours are not allowed: `[7, 7]` is *not* strictly increasing.
- Only the **length** is returned, not the subsequence itself.

### Examples

**Example 1**

```text
Input:  nums = [10, 9, 2, 5, 3, 7, 101, 18]
Output: 4
```

One longest increasing subsequence is `[2, 3, 7, 101]` (another is `[2, 5, 7, 18]`). Both have length 4.

**Example 2**

```text
Input:  nums = [0, 1, 0, 3, 2, 3]
Output: 4
```

For example `[0, 1, 2, 3]` (indices 0, 1, 4, 5).

**Example 3**

```text
Input:  nums = [7, 7, 7, 7, 7, 7, 7]
Output: 1
```

All values are equal, so no two of them can be in a *strictly* increasing subsequence. A single element counts as length 1.

### Constraints

- `1 <= nums.length <= 2500`
- `-10^4 <= nums[i] <= 10^4`

**Follow-up:** Can you come up with an algorithm that runs in `O(n log n)` time?

---

## 3. Everyday Analogy

> **Explain it like I'm five**

Imagine kids arriving one at a time to line up for a photo, and you want the **longest line where each kid is taller than the one before them**, keeping the order in which they arrived.

You keep a little notebook with one entry per possible line length:

- "Shortest last kid of any line of length 1 I've seen so far"
- "Shortest last kid of any line of length 2 so far"
- …

Why remember the **shortest** last kid? Because a line ending with a short kid is easier to extend — more future kids are taller than a short kid.

When a new kid arrives:
- If they're taller than the last kid of your longest line, they **extend** it → your best length grows by one.
- Otherwise, find the first entry in the notebook whose last kid is at least as tall as the new kid and **replace** it with the new kid. The line of that length now ends lower, which can only help later.

The number of entries in the notebook is the answer. (Careful: the notebook entries together are **not** necessarily a real line — see section 6.)

---

## 4. Step-by-Step Logic

### The DP recipe (`O(n²)` version)

1. **State definition.** `dp[i]` = length of the longest strictly increasing subsequence that **ends exactly at index `i`** (so `nums[i]` is its last element).
2. **Recurrence.** The element before `nums[i]` in that subsequence is some `nums[j]` with `j < i` and `nums[j] < nums[i]`. So

   ```text
   dp[i] = 1 + max(dp[j] for j < i if nums[j] < nums[i])     (or 1 if there is no such j)
   ```

3. **Base case.** Every element alone is an increasing subsequence: `dp[i]` starts at `1`.
4. **Iteration order.** `dp[i]` needs `dp[j]` for smaller `j`, so go `i = 0, 1, …, n-1`.
5. **Answer location.** The LIS can end anywhere, so the answer is `max(dp)` — **not** `dp[n-1]`.

### From `O(n²)` to `O(n log n)`

6. Instead of asking "what's the best length ending at each index?", ask: **"for each length `L`, what is the smallest possible last value of an increasing subsequence of length `L`?"** Call this list `tails`: `tails[L-1]` = smallest tail of any increasing subsequence of length `L` seen so far.
7. `tails` is always **sorted strictly increasing** (a length-`L+1` subsequence contains a length-`L` one ending at a smaller value).
8. Because `tails` is sorted, finding where a new number belongs is a **binary search**: the first position with `tails[pos] >= num` (`bisect_left`).
   - `pos == len(tails)`: `num` is bigger than every tail → it extends the longest subsequence → append.
   - Otherwise: `num` can end a subsequence of length `pos + 1` with a smaller tail than before → replace `tails[pos]`.
9. `len(tails)` is the LIS length.

---

## 5. Brute-Force Solution

### Algorithm

For each element, decide **take it or skip it**. You may take `nums[i]` only if it's bigger than the last element you took. Recursively try both and return the longer result.

### Python code

```python
from typing import List


class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        n = len(nums)

        def best(i: int, prev: int) -> int:
            # Longest increasing subsequence using nums[i:], where the last
            # chosen element is nums[prev] (prev == -1 means nothing chosen).
            if i == n:
                return 0
            skip = best(i + 1, prev)
            take = 0
            if prev == -1 or nums[i] > nums[prev]:
                take = 1 + best(i + 1, i)
            return max(skip, take)

        return best(0, -1)
```

### Explanation

- `best(i, prev)` explores both choices for `nums[i]`.
- The strict `>` comparison enforces "strictly increasing".
- Every subsequence is explored, so the answer is correct — but there are up to `2^n` of them.

### Complexity

- **Time:** `O(2^n)` — every element is taken or skipped. For `n = 2500` this is hopeless and **times out**.
- **Auxiliary space:** `O(n)` recursion depth.

### The bridge: memoization

`best(i, prev)` has only `n × (n + 1)` different argument pairs. Caching them (for example with `@lru_cache` on the nested function) gives `O(n²)` time and `O(n²)` memory — but `n = 2500` means millions of cache entries and a recursion depth of 2500, which exceeds Python's default limit. The bottom-up `dp[i]` table below has the same `O(n²)` time with only `O(n)` memory.

### Alternative: bottom-up `O(n²)` DP

```python
from typing import List


class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        n = len(nums)
        dp = [1] * n                      # dp[i] = LIS length ending at i

        for i in range(n):
            for j in range(i):
                if nums[j] < nums[i] and dp[j] + 1 > dp[i]:
                    dp[i] = dp[j] + 1

        return max(dp)
```

About `n² / 2 ≈ 3.1 million` comparisons for `n = 2500` — usually accepted, but slow in Python. The follow-up asks for better.

---

## 6. Optimized Solution

### Idea — patience sorting with `bisect`

Keep `tails`, where `tails[k]` is the **smallest possible last value** of a strictly increasing subsequence of length `k + 1` among the elements processed so far. Each new number either extends `tails` or lowers one entry, found by binary search.

> ⚠️ **`tails` is not itself an increasing subsequence.** It is a list of "best tail per length", and its values can come from different subsequences. For `nums = [3, 4, 5, 1]`, the final `tails` is `[1, 4, 5]` — but `1` appears **after** `5` in `nums`, so `[1, 4, 5]` is not a subsequence at all. Only its **length** (3, from `[3, 4, 5]`) is meaningful.

### Algorithm

1. `tails = []`.
2. For each `num` in `nums`:
   - `pos = bisect_left(tails, num)` — first index with `tails[pos] >= num`.
   - If `pos == len(tails)`: append `num`.
   - Else: `tails[pos] = num`.
3. Return `len(tails)`.

### Python code (LeetCode-ready)

```python
from typing import List
from bisect import bisect_left


class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        tails = []  # tails[k] = smallest tail of an increasing subsequence of length k + 1

        for num in nums:
            pos = bisect_left(tails, num)   # first tail >= num
            if pos == len(tails):
                tails.append(num)           # num extends the longest subsequence
            else:
                tails[pos] = num            # num is a smaller tail for length pos + 1

        return len(tails)
```

---

## 7. Line-by-Line Explanation

(Patience sorting version)

| Line | What it does | Why |
|---|---|---|
| `from bisect import bisect_left` | Imports Python's binary search on sorted lists. | `tails` is always sorted, so binary search applies. |
| `tails = []` | Starts with no subsequences. | No elements processed yet. |
| `for num in nums:` | Processes elements in their original order. | Subsequences must respect order. |
| `pos = bisect_left(tails, num)` | Finds the first index whose tail is `>= num`, in `O(log n)`. | Every tail before `pos` is `< num`, so `num` can extend the subsequence of length `pos` (ending at `tails[pos-1]`) to length `pos + 1`. |
| `if pos == len(tails):` | `num` is larger than every tail. | It extends the longest subsequence found so far. |
| `tails.append(num)` | The LIS length grows by one. | A new, longer length is now achievable. |
| `tails[pos] = num` | Replaces a tail with a smaller-or-equal value. | We found a length-`pos + 1` subsequence ending at `num <= tails[pos]`; a lower tail is easier to extend later. If `num == tails[pos]`, nothing changes — correct, because equal values can't extend each other. |
| `return len(tails)` | Returns the number of lengths achieved. | The longest achievable length is the answer. |

**Why `bisect_left` and not `bisect_right`?** With duplicates, `bisect_right` would put an equal number **after** its twin and append it, counting `[7, 7]` as increasing. `bisect_left` lands on the equal value and replaces it, keeping the subsequence **strictly** increasing.

---

## 8. Dry Run

**Input:** `nums = [10, 9, 2, 5, 3, 7, 101, 18]` (official Example 1)

### `O(n²)` DP table

| `i` | `nums[i]` | Earlier `j` with `nums[j] < nums[i]` (their `dp[j]`) | `dp[i]` |
|---|---|---|---|
| 0 | 10 | none | 1 |
| 1 | 9 | none | 1 |
| 2 | 2 | none | 1 |
| 3 | 5 | `j=2` (1) | 2 |
| 4 | 3 | `j=2` (1) | 2 |
| 5 | 7 | `j=2` (1), `j=3` (2), `j=4` (2) | 3 |
| 6 | 101 | all of `j=0..5` (best is `j=5`, 3) | 4 |
| 7 | 18 | `j=0..5` (best is `j=5`, 3) | 4 |

`dp = [1, 1, 1, 2, 2, 3, 4, 4]`, `max(dp) = 4` ✅

### Patience sorting with `tails`

| Step | `num` | `tails` before | `bisect_left` → `pos` | Action | `tails` after |
|---|---|---|---|---|---|
| 1 | 10 | `[]` | 0 (= len) | append | `[10]` |
| 2 | 9 | `[10]` | 0 | replace `10` → `9` | `[9]` |
| 3 | 2 | `[9]` | 0 | replace `9` → `2` | `[2]` |
| 4 | 5 | `[2]` | 1 (= len) | append | `[2, 5]` |
| 5 | 3 | `[2, 5]` | 1 | replace `5` → `3` | `[2, 3]` |
| 6 | 7 | `[2, 3]` | 2 (= len) | append | `[2, 3, 7]` |
| 7 | 101 | `[2, 3, 7]` | 3 (= len) | append | `[2, 3, 7, 101]` |
| 8 | 18 | `[2, 3, 7, 101]` | 3 | replace `101` → `18` | `[2, 3, 7, 18]` |

**Result:** `len(tails) = 4` ✅

(Here `[2, 3, 7, 18]` happens to be a real LIS, but that is luck — see the `[3, 4, 5, 1]` warning in section 6.)

**Second dry run with duplicates:** `nums = [0, 1, 0, 3, 2, 3]` (Example 2)

| `num` | `pos` | `tails` after |
|---|---|---|
| 0 | 0 | `[0]` |
| 1 | 1 | `[0, 1]` |
| 0 | 0 (equal to `tails[0]`) | `[0, 1]` (replace 0 with 0) |
| 3 | 2 | `[0, 1, 3]` |
| 2 | 2 | `[0, 1, 2]` |
| 3 | 3 | `[0, 1, 2, 3]` |

**Result:** `4` ✅. For Example 3 (`[7, 7, …]`) every `7` lands on `pos = 0`, so `tails = [7]` and the answer is `1` ✅.

---

## 9. Concepts, Data Structures, and Patterns

- **DP recipe ("best ending at `i`")**: state `dp[i]`, recurrence over earlier `j`, base `1`, left-to-right order, answer `max(dp)`. Same shape as Kadane's "best ending here" in [Maximum Subarray](../01_array/005_maximum_subarray.md), but each state looks at *all* earlier indices.
- **Subsequence vs subarray:** subsequences may skip elements; subarrays may not.
- **Greedy + binary search (patience sorting):** keeping the smallest tail per length is a greedy choice that never hurts; binary search on the sorted `tails` makes each step `O(log n)`.
- **`bisect_left` vs `bisect_right`:** strict vs non-strict increase.
- **Invariant thinking:** "`tails` is sorted and `tails[k]` is the minimum tail for length `k + 1`" is the invariant that proves correctness.
- **Related notes:** [Longest Common Subsequence](058_longest_common_subsequence.md) (2-D subsequence DP), [Coin Change](056_coin_change.md) (1-D DP), [Find Minimum in Rotated Sorted Array](../01_array/007_find_minimum_in_rotated_sorted_array.md) (binary search). Related LeetCode problems: Number of LIS (673), Russian Doll Envelopes (354).

---

## 10. Complexity Analysis

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Brute force (take/skip) | `O(2^n)` | `O(n)` | Two choices per element; recursion depth `n`. |
| Memoized recursion | `O(n²)` | `O(n²)` | `n × (n+1)` states `(i, prev)`, `O(1)` work each; the cache stores them all. |
| Bottom-up DP | `O(n²)` | `O(n)` | Double loop over `j < i`; one `dp` list. |
| Patience sorting (optimized) | `O(n log n)` | `O(n)` | `n` binary searches on a list of length at most `n`; `tails` can grow to `n` (fully increasing input). |

---

## 11. Edge Cases

| Case | Example | Expected result | Why |
|---|---|---|---|
| Single element | `[5]` | `1` | One element is an increasing subsequence. |
| All equal | `[7, 7, 7, 7, 7, 7, 7]` | `1` | Strictly increasing forbids equal neighbours. |
| Already increasing | `[1, 2, 3, 4, 5]` | `5` | Take everything. |
| Strictly decreasing | `[5, 4, 3, 2, 1]` | `1` | No pair increases. |
| `tails` is not an LIS | `[3, 4, 5, 1]` | `3` | `tails` ends as `[1, 4, 5]`, but only its length matters. |
| Duplicates inside | `[4, 10, 4, 3, 8, 9]` | `3` | e.g. `[4, 8, 9]`; the second 4 must not extend the first. |
| Extreme values | `[-10000, 10000]` | `2` | Negative numbers need no special handling. |

---

## 12. Common Mistakes and Debugging

1. **Returning `dp[n-1]` instead of `max(dp)`.** The LIS doesn't have to end at the last element (`[1, 2, 0]` → `dp[-1] = 1`, answer 2).
2. **Using `<=` instead of `<`** (or `bisect_right`). That counts non-decreasing subsequences and returns 7 for `[7, 7, 7, 7, 7, 7, 7]`.
3. **Thinking `tails` is the subsequence.** It isn't (see `[3, 4, 5, 1]`). To recover an actual LIS you need parent pointers (practice Q2).
4. **Sorting `nums` first.** Subsequences must keep the original order; sorting destroys it.
5. **Initializing `dp` with 0.** Each element alone has length 1, so start at 1.
6. **Writing your own binary search with off-by-one bugs.** Prefer `bisect_left`; if you hand-roll it, search for the first index with `tails[mid] >= num`.

**Debugging tip:** print `num, pos, tails` on every iteration and compare with the dry-run table.

---

## 13. Practice Questions

**Q1. Trace `tails` for `nums = [3, 4, 5, 1, 2]`. What's the answer, and is the final `tails` a real subsequence?**

<details><summary>Hint</summary>Use `bisect_left` at every step; then check whether the final values appear in that order in `nums`.</summary></details>

**Answer:** `[3]` → `[3, 4]` → `[3, 4, 5]` → `1` replaces 3: `[1, 4, 5]` → `2` replaces 4: `[1, 2, 5]`. The answer is `3` (e.g. `[3, 4, 5]`). The final `tails = [1, 2, 5]` is **not** a subsequence, because 5 comes before 1 and 2 in `nums`.

**Q2. Return one actual longest increasing subsequence (not just its length).**

<details><summary>Hint</summary>In the `O(n²)` DP, also store `parent[i]` = the `j` that gave `dp[i]` its value. Start from the index with the largest `dp` and follow parents backwards.</summary></details>

**Answer:**

```python
def longest_increasing_subsequence(nums):
    n = len(nums)
    dp = [1] * n
    parent = [-1] * n
    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i] and dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
                parent[i] = j
    i = max(range(n), key=lambda k: dp[k])   # end of one longest subsequence
    result = []
    while i != -1:
        result.append(nums[i])
        i = parent[i]
    return result[::-1]


seq = longest_increasing_subsequence([10, 9, 2, 5, 3, 7, 101, 18])
assert len(seq) == 4 and all(a < b for a, b in zip(seq, seq[1:]))
assert longest_increasing_subsequence([3, 4, 5, 1]) == [3, 4, 5]
assert longest_increasing_subsequence([7, 7, 7]) == [7]
```

**Q3. Longest *non-decreasing* subsequence (equal neighbours allowed). What single change makes the `O(n log n)` code work?**

<details><summary>Hint</summary>Think about where an equal value should go in `tails`.</summary></details>

**Answer:** Use `bisect_right`. An equal value now goes **after** its twin, so it can extend a subsequence ending with the same value.

```python
from bisect import bisect_right


def longest_non_decreasing(nums):
    tails = []
    for num in nums:
        pos = bisect_right(tails, num)   # first tail > num
        if pos == len(tails):
            tails.append(num)
        else:
            tails[pos] = num
    return len(tails)


assert longest_non_decreasing([7, 7, 7, 7]) == 4
assert longest_non_decreasing([0, 1, 0, 3, 2, 3]) == 4
assert longest_non_decreasing([3, 1, 2, 2, 1]) == 3
```

**Q4. Why is it safe to *replace* `tails[pos]` with a smaller number, even though it "breaks" the stored subsequence?**

<details><summary>Hint</summary>What does `tails[pos]` promise, and does the replacement keep that promise?</summary></details>

**Answer:** `tails[pos]` only promises "**some** increasing subsequence of length `pos + 1` ends with this value". After the replacement that is still true: the subsequence of length `pos` ending at `tails[pos-1] < num` (which appeared before `num`) plus `num` itself. A smaller tail makes it easier for future numbers to extend that length, and the **lengths** (the size of `tails`) never shrink, so no information needed for the answer is lost.

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** DP "best ending at `i`" → patience sorting + binary search.
- **`O(n²)` DP:** `dp[i] = 1 + max(dp[j] | j < i, nums[j] < nums[i])`, base 1, answer `max(dp)`.
- **`O(n log n)`:** `tails[k]` = smallest tail of an increasing subsequence of length `k+1`; `bisect_left`, append or replace; answer `len(tails)`.
- **Warning:** `tails` is **not** an LIS — only its length is.
- **Time:** `O(n log n)`. **Auxiliary space:** `O(n)`.
- **One-line memory hook:** *"Keep the lowest tail for every length; extend at the end, otherwise lower a tail."*

### Completion checklist

- [x] Problem requirements verified
- [x] Examples and constraints verified
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force solution written and tested
- [x] Alternative `O(n²)` DP written and tested
- [x] Optimized Python solution written and tested (`tools/tests/p057.py`)
- [x] Line-by-line explanation written
- [x] Dry run completed with a real example (DP table and `tails` table)
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
