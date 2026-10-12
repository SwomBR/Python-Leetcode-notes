# 001. Two Sum

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Two Sum |
| **LeetCode number** | 1 |
| **Topic (source list)** | Array |
| **Also uses** | Hash Table |
| **Difficulty** | Easy |
| **LeetCode URL** | <https://leetcode.com/problems/two-sum/> |
| **Pattern** | Complement lookup with a hash map |

---

## 2. Problem Explanation

### What are we given?

- `nums` — a list of whole numbers (they can be negative, zero, or positive).
- `target` — one whole number.

### What must we return?

A list containing **two positions (indices)** `[i, j]` such that `nums[i] + nums[j] == target`.

### The rules

1. You must use **two different positions**. You may not use the same element twice (but two *different* positions may hold the same *value*, like `[3, 3]`).
2. The problem promises that **exactly one** correct pair exists, so you never have to handle "no answer" or choose between several answers.
3. The two indices may be returned in **any order** — `[0, 1]` and `[1, 0]` are both accepted.

### Examples

**Example 1**

```text
Input:  nums = [2, 7, 11, 15], target = 9
Output: [0, 1]
```

`nums[0] + nums[1] = 2 + 7 = 9`, which equals the target.

**Example 2**

```text
Input:  nums = [3, 2, 4], target = 6
Output: [1, 2]
```

`nums[1] + nums[2] = 2 + 4 = 6`. Note that `3 + 3` would also be 6, but there is only one `3`, and we cannot use the same position twice.

**Example 3**

```text
Input:  nums = [3, 3], target = 6
Output: [0, 1]
```

The two 3s sit at different positions, so using both is allowed.

### Constraints

- `2 <= nums.length <= 10^4`
- `-10^9 <= nums[i] <= 10^9`
- `-10^9 <= target <= 10^9`
- Only one valid answer exists.

**Follow-up:** Can you find an algorithm that runs faster than `O(n²)` time?

---

## 3. Everyday Analogy

> **Explain it like I'm five**

Imagine you have a row of toy blocks, and each block has a number painted on it. Your friend says: *"Find two blocks whose numbers add up to 9!"*

The slow way is to pick up the first block and hold it next to every other block, one at a time, then pick up the second block and do the same thing again… That takes forever when you have lots of blocks.

The clever way: walk along the row **once**. Each time you look at a block, ask yourself, *"What number would my partner need to be?"* If the block says 2 and the goal is 9, the partner must be 7. Then you check your **notebook**: "Have I already seen a 7?"

- If yes — you found the pair! Point at both blocks.
- If no — write "I saw a 2 at spot 0" in your notebook and keep walking.

The notebook lets you remember everything you've already seen, so you never have to walk back.

---

## 4. Step-by-Step Logic

Before writing code, reason it out:

1. **What makes a pair correct?** `nums[i] + nums[j] == target`.
2. **Rearrange the equation.** If I'm standing at `nums[j]`, the partner I need is `target - nums[j]`. This needed value is called the **complement**.
3. **Ask the key question.** "Have I already seen the complement at an earlier position?" If I can answer this instantly, I only need one pass over the list.
4. **Choose a tool for instant lookups.** A Python dictionary (hash map) answers "Is this value stored?" in about `O(1)` time. Store `value -> index`.
5. **Order matters.** Check for the complement *before* storing the current number. This stops a number from pairing with itself (for example, `nums = [3, 2, 4]`, `target = 6`: the first `3` must not match itself).
6. **Return as soon as a match appears.** The problem guarantees exactly one answer, so the first match is the answer.

---

## 5. Brute-Force Solution

### Algorithm

1. For every position `i`:
2. For every later position `j` (`j > i`):
3. If `nums[i] + nums[j] == target`, return `[i, j]`.

Starting `j` at `i + 1` ensures we never use the same position twice and never check the same pair twice.

### Python code

```python
from typing import List


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        n = len(nums)
        for i in range(n):
            for j in range(i + 1, n):
                if nums[i] + nums[j] == target:
                    return [i, j]
        return []  # unreachable: the problem guarantees one answer
```

### Explanation

- The outer loop chooses the first number of the pair.
- The inner loop tries every number after it as the second number.
- The first pair whose sum equals `target` is returned.
- The final `return []` only exists so the function always returns a list; with valid LeetCode input it never runs.

### Complexity

- **Time:** `O(n²)`. There are `n(n-1)/2` pairs. With `n = 10^4` that is about 50 million additions — accepted on LeetCode in some languages but slow in Python, and it does not satisfy the follow-up.
- **Auxiliary space:** `O(1)`. Only a few loop variables.

---

## 6. Optimized Solution

### Idea

Use a dictionary called `seen` that remembers `number -> index` for everything we've already passed. For each new number, compute its complement and look it up in `seen`.

### Algorithm

1. Create an empty dictionary `seen`.
2. Walk through the list with index `i` and value `num`.
3. Compute `complement = target - num`.
4. If `complement` is in `seen`, return `[seen[complement], i]`.
5. Otherwise store `seen[num] = i`.

### Python code (LeetCode-ready)

```python
from typing import List


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        seen = {}  # value -> index where we saw it

        for i, num in enumerate(nums):
            complement = target - num
            if complement in seen:
                return [seen[complement], i]
            seen[num] = i

        return []  # unreachable: the problem guarantees one answer
```

---

## 7. Line-by-Line Explanation

| Line | What it does | Why |
|---|---|---|
| `seen = {}` | Creates an empty dictionary. Keys are numbers, values are their indices. | We need fast "have I seen this number?" checks. |
| `for i, num in enumerate(nums):` | Loops over the list, giving both the index `i` and the value `num`. | We need the index for the answer and the value for the arithmetic. |
| `complement = target - num` | Computes the partner value that would complete the sum. | If `num + x == target`, then `x == target - num`. |
| `if complement in seen:` | Checks the dictionary in average `O(1)` time. | Only numbers at **earlier** positions are in `seen`, so a match is always a different position. |
| `return [seen[complement], i]` | Returns the earlier index and the current index. | That pair sums to `target`. |
| `seen[num] = i` | Records the current number for future iterations. | A later number may need this one as its partner. Storing it **after** the check prevents pairing a number with itself. |
| `return []` | Fallback. | Never reached for valid input; it keeps the return type consistent. |

**Why storing after checking matters with duplicates:** For `nums = [3, 3]`, `target = 6`:
- At `i = 0`, complement is `3`, `seen` is empty → store `{3: 0}`.
- At `i = 1`, complement is `3`, and `3` is in `seen` at index `0` → return `[0, 1]`. ✅

If two equal values were both stored before checking, the second would overwrite the first index — but because we check first, we find the match before overwriting.

---

## 8. Dry Run

**Input:** `nums = [2, 7, 11, 15]`, `target = 9`

| Step | `i` | `num` | `complement = 9 - num` | `seen` before the check | Is complement in `seen`? | Action |
|---|---|---|---|---|---|---|
| 1 | 0 | 2 | 7 | `{}` | No | Store `seen[2] = 0` |
| 2 | 1 | 7 | 2 | `{2: 0}` | **Yes**, at index 0 | Return `[0, 1]` |

**Result:** `[0, 1]` ✅

**Second dry run:** `nums = [3, 2, 4]`, `target = 6`

| Step | `i` | `num` | `complement` | `seen` before | Found? | Action |
|---|---|---|---|---|---|---|
| 1 | 0 | 3 | 3 | `{}` | No (3 is not stored yet, so it can't pair with itself) | Store `seen[3] = 0` |
| 2 | 1 | 2 | 4 | `{3: 0}` | No | Store `seen[2] = 1` |
| 3 | 2 | 4 | 2 | `{3: 0, 2: 1}` | **Yes**, at index 1 | Return `[1, 2]` |

**Result:** `[1, 2]` ✅

---

## 9. Concepts, Data Structures, and Patterns

- **Array traversal with `enumerate`:** gives index and value together, which is cleaner than `range(len(nums))`.
- **Hash map (Python `dict`):** stores key–value pairs. Checking `key in dict` and reading `dict[key]` take `O(1)` time on average because Python hashes the key to find its slot directly.
- **Complement pattern:** instead of searching for *pairs*, search for the *one missing value* each element needs. This turns a two-element search into a single lookup.
- **Trading space for time:** we use `O(n)` extra memory to save `O(n)` time per element.
- **Related patterns:**
  - *Two pointers* works if the array is **sorted** (see LeetCode 167, Two Sum II). Here the array is not sorted and we must return the *original* indices, so sorting would require tracking positions.
  - The same "complement in a hash map" idea appears in 3Sum ([009_3sum.md](009_3sum.md)), subarray-sum problems, and pair-counting problems.

---

## 10. Complexity Analysis

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Brute force | `O(n²)` | `O(1)` | Checks every pair. |
| Hash map (optimized) | `O(n)` average | `O(n)` | One pass; each dictionary lookup/insert is `O(1)` on average. In the worst case the dictionary holds `n - 1` entries before the match is found. |

**Why "average"?** Hash table operations are `O(1)` on average. Pathological hash collisions could make them slower, but with Python's integer hashing this does not happen in practice, and `O(n)` is the accepted answer.

---

## 11. Edge Cases

| Case | Example | Expected result | Why it works |
|---|---|---|---|
| Smallest input | `nums = [3, 3]`, `target = 6` | `[0, 1]` | Duplicate values at different positions are allowed. |
| Same value must not pair with itself | `nums = [3, 2, 4]`, `target = 6` | `[1, 2]` | We check before inserting, so `3` cannot match itself. |
| Negative numbers | `nums = [-3, 4, 3, 90]`, `target = 0` | `[0, 2]` | `-3 + 3 = 0`; complements work with negatives. |
| Zeros | `nums = [0, 4, 3, 0]`, `target = 0` | `[0, 3]` | The second 0 finds the first 0 in `seen`. |
| Answer at the very end | `nums = [1, 2, 3, 4]`, `target = 7` | `[2, 3]` | The loop runs to the end before matching. |
| Large values | `nums = [10^9, -10^9]`, `target = 0` | `[0, 1]` | Python integers do not overflow. |

---

## 12. Common Mistakes and Debugging

1. **Storing before checking.** `seen[num] = i` followed by `if complement in seen` lets `nums = [3, ...]`, `target = 6` match index 0 with itself. Always check first.
2. **Returning values instead of indices.** The problem asks for positions, not the numbers themselves.
3. **Sorting the array first.** Sorting changes the positions, so the returned indices would be wrong unless you store the original indices.
4. **Using `nums.index(complement)`.** `list.index` is an `O(n)` scan, turning your solution back into `O(n²)`; it can also return the current element's own index.
5. **Inner loop starting at 0.** In the brute force, `for j in range(n)` can pair `i` with itself. Start at `i + 1`.

**Debugging tip:** print `i, num, complement, seen` at the top of each loop iteration and compare against the dry-run table above.

---

## 13. Practice Questions

**Q1. What does the optimized solution return for `nums = [1, 5, 9, 12]`, `target = 14`?**

<details><summary>Hint</summary>Walk the loop: what complement does each number need?</summary></details>

**Answer:** `[1, 2]`. At `i = 0` (value 1) the complement 13 is unseen, so store `{1: 0}`. At `i = 1` (value 5) the complement 9 is unseen, so store `{1: 0, 5: 1}`. At `i = 2` (value 9) the complement 5 is in `seen` at index 1, so we return `[1, 2]` because 5 + 9 = 14. The loop stops before reaching 12.

**Q2. Why can't we simply sort and use two pointers here?**

<details><summary>Hint</summary>What does the output contain?</summary></details>

**Answer:** The output must be the **original** indices. Sorting moves the elements. You *could* sort a list of `(value, original_index)` pairs and then use two pointers, which costs `O(n log n)` time — slower than the `O(n)` hash map approach.

**Q3. Modify the idea: return `True` if *any* pair sums to `target`, otherwise `False`.**

<details><summary>Hint</summary>You don't need indices anymore, so what simpler structure can you use?</summary></details>

**Answer:** A set is enough.

```python
def has_pair_with_sum(nums, target):
    seen = set()
    for num in nums:
        if target - num in seen:
            return True
        seen.add(num)
    return False


assert has_pair_with_sum([1, 4, 6], 10) is True
assert has_pair_with_sum([1, 4, 6], 3) is False
```

**Q4. Count how many index pairs `(i < j)` sum to `target` (duplicates allowed).**

<details><summary>Hint</summary>Store a *count* of each value instead of a single index.</summary></details>

**Answer:** Each new number pairs with every earlier copy of its complement.

```python
def count_pairs(nums, target):
    counts = {}
    pairs = 0
    for num in nums:
        pairs += counts.get(target - num, 0)
        counts[num] = counts.get(num, 0) + 1
    return pairs


assert count_pairs([1, 1, 1], 2) == 3   # (0,1), (0,2), (1,2)
assert count_pairs([1, 5, 7, -1], 6) == 2  # (1,5) and (7,-1)
```

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** Hash map complement lookup.
- **Key idea:** For each number, ask "Have I already seen `target - num`?" Store `value -> index` *after* checking.
- **Time:** `O(n)` average.
- **Auxiliary space:** `O(n)`.
- **One-line memory hook:** *"Look back in the notebook for your partner, then write yourself down."*

### Completion checklist

- [x] Problem requirements verified
- [x] Examples and constraints verified
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force solution written and tested
- [x] Optimized Python solution written and tested (`tools/tests/p001.py`)
- [x] Line-by-line explanation written
- [x] Dry run completed with a real example
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
