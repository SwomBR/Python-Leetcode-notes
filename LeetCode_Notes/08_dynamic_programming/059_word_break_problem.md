# 059. Word Break

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Word Break (listed in the source as "Word Break Problem") |
| **LeetCode number** | 139 |
| **Topic (source list)** | Dynamic Programming |
| **Also uses** | String, Hash Set, Recursion + memoization (BFS and Trie are alternatives) |
| **Difficulty** | Medium |
| **LeetCode URL** | <https://leetcode.com/problems/word-break/> |
| **Pattern** | 1-D prefix DP: "can the first `i` characters be split?" |

---

## 2. Problem Explanation

### What are we given?

- `s` — a string of lowercase letters with no spaces, e.g. `"leetcode"`.
- `wordDict` — a list of distinct dictionary words.

### What must we return?

`True` if `s` can be cut into pieces so that **every piece is a dictionary word**, otherwise `False`.

### The rules

1. The pieces must cover **all** of `s`, in order, with nothing left over and no overlaps.
2. There must be **at least one** piece (always true, since `s` is non-empty).
3. A dictionary word may be **reused as many times as you like**.
4. We only answer yes/no — we don't return the split itself.

### Examples

**Example 1**

```text
Input:  s = "leetcode", wordDict = ["leet", "code"]
Output: true
```

`"leetcode"` = `"leet"` + `"code"`.

**Example 2**

```text
Input:  s = "applepenapple", wordDict = ["apple", "pen"]
Output: true
```

`"applepenapple"` = `"apple"` + `"pen"` + `"apple"` — the word `"apple"` is used twice, which is allowed.

**Example 3**

```text
Input:  s = "catsandog", wordDict = ["cats", "dog", "sand", "and", "cat"]
Output: false
```

`"cats" + "and"` or `"cat" + "sand"` both cover `"catsand"`, but the remaining `"og"` is not a word, and no other split works either.

### Constraints

- `1 <= s.length <= 300`
- `1 <= wordDict.length <= 1000`
- `1 <= wordDict[i].length <= 20`
- `s` and `wordDict[i]` consist of only lowercase English letters.
- All the strings of `wordDict` are unique.

There is no official follow-up for this problem.

---

## 3. Everyday Analogy

> **Explain it like I'm five**

Someone wrote a sentence but forgot all the spaces: `"applepenapple"`. You have a sticker book of allowed words. Can you put spaces back so that **every** chunk is a word from the sticker book?

You walk along the letters with a pencil. At certain spots you can say: *"Everything before this spot is already made of real words."* Mark those spots with a ✓. The very start gets a ✓ for free (nothing before it).

For every new spot, you look back at earlier ✓ spots and ask: *"Is the chunk from that ✓ to here a word in my sticker book?"* If yes, this spot gets a ✓ too.

If the spot **after the last letter** gets a ✓, the whole sentence can be split into words.

---

## 4. Step-by-Step Logic

Follow the DP recipe.

1. **Find the choice.** If `s` can be split, its **last word** is some dictionary word `s[j:n]`, and the part before it, `s[:j]`, must also be splittable.
2. **State definition.** `dp[i]` = `True` if the **prefix** `s[:i]` (the first `i` characters) can be split into dictionary words.
3. **Recurrence.**

   ```text
   dp[i] = True if there is some j < i with dp[j] == True and s[j:i] in words
   ```

4. **Base case.** `dp[0] = True` — the empty prefix needs zero words. This is what lets the *first* word start at index 0.
5. **Iteration order.** `dp[i]` depends on smaller `j`, so compute `i = 1, 2, …, n`.
6. **Answer location.** `dp[n]` (the whole string).
7. **Speed-ups.**
   - Put the words in a **set** so `s[j:i] in words` is an average `O(length)` hash lookup instead of a scan of up to 1000 words.
   - A word is at most `max_len ≤ 20` characters, so only `j` in `[i - max_len, i)` can work. That cuts the inner loop from `i` steps to at most 20.
   - As soon as one `j` works, `break` — we only need a yes.

**Why not greedy?** Taking the longest (or shortest) matching word first can fail: for `s = "goalspecial"` and words `["go", "goal", "goals", "special"]`, the longest first match is `"goals"`, leaving `"pecial"` (dead end), but `"goal" + "special"` works.

---

## 5. Brute-Force Solution

### Algorithm

`can(start)` asks "can `s[start:]` be split?". Try every end position; if `s[start:end]` is a word and `can(end)` is true, succeed. Reaching the end of `s` means success.

### Python code

```python
from typing import List


class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        words = set(wordDict)
        n = len(s)

        def can(start: int) -> bool:
            if start == n:
                return True                 # used up the whole string
            for end in range(start + 1, n + 1):
                if s[start:end] in words and can(end):
                    return True
            return False

        return can(0)
```

### Explanation

- Every way of cutting `s` is a sequence of cut positions; the recursion tries them all (pruned only by "the current piece must be a word").
- The same `can(start)` is recomputed whenever different word sequences reach the same `start`.

### Complexity

- **Time:** `O(2^n × n)` in the worst case. A string of `n` characters has `2^(n-1)` ways to place cuts. A classic bad input is `s = "aaaa…ab"` with words `["a", "aa", "aaa", …]`: every split of the `a`s is valid, and only at the end do we find that `"b"` breaks everything. With `n = 300` this **times out**.
- **Auxiliary space:** `O(n)` recursion depth (plus the slice being checked).

### The bridge: memoization

`can(start)` only has `n + 1` possible arguments. Remembering each answer (`@lru_cache` on the nested function, or a `memo` dict) makes the whole search `O(n²)` lookups. That's the top-down version of the table below.

```python
from typing import List
from functools import lru_cache


class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        words = set(wordDict)
        n = len(s)

        @lru_cache(maxsize=None)
        def can(start: int) -> bool:
            if start == n:
                return True
            for end in range(start + 1, n + 1):
                if s[start:end] in words and can(end):
                    return True
            return False

        return can(0)
```

Recursion depth is at most `n + 1 = 301`, which is safe in Python.

---

## 6. Optimized Solution

### Idea — bottom-up prefix DP with a word-length limit

Fill `dp[0..n]` left to right. For each end position `i`, only look back at most `max_len` characters.

### Algorithm

1. `words = set(wordDict)`, `max_len = longest word length`.
2. `dp = [False] * (n + 1)`, `dp[0] = True`.
3. For `end` in `1..n`:
   - For `start` in `max(0, end - max_len) .. end - 1`:
     - If `dp[start]` and `s[start:end] in words`: set `dp[end] = True` and stop checking this `end`.
4. Return `dp[n]`.

### Python code (LeetCode-ready)

```python
from typing import List


class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        words = set(wordDict)
        max_len = max(len(word) for word in words)
        n = len(s)

        dp = [False] * (n + 1)   # dp[i] = can s[:i] be split into words?
        dp[0] = True             # empty prefix

        for end in range(1, n + 1):
            for start in range(max(0, end - max_len), end):
                if dp[start] and s[start:end] in words:
                    dp[end] = True
                    break        # one way is enough

        return dp[n]
```

---

## 7. Line-by-Line Explanation

| Line | What it does | Why |
|---|---|---|
| `words = set(wordDict)` | Builds a hash set of the words. | Membership checks become average `O(L)` (hashing the slice) instead of scanning 1000 words. |
| `max_len = max(len(word) for word in words)` | Finds the longest word (at most 20). | A piece longer than this can't be a word, so we never check it. |
| `dp = [False] * (n + 1)` | One entry per prefix length `0..n`. | `dp[i]` describes `s[:i]`. |
| `dp[0] = True` | Base case. | The empty prefix is trivially "split" into zero words; it lets a word starting at index 0 count. |
| `for end in range(1, n + 1):` | Each prefix length in increasing order. | `dp[end]` needs `dp[start]` for smaller `start`. |
| `for start in range(max(0, end - max_len), end):` | Candidate start of the **last** word `s[start:end]`. | Only the last `max_len` positions can begin a word that ends at `end`; `max(0, …)` avoids negative indices. |
| `if dp[start] and s[start:end] in words:` | Prefix before the word is splittable **and** the piece is a word. | Checking `dp[start]` first is cheap and skips useless slicing. |
| `dp[end] = True` / `break` | Marks this prefix as splittable and stops. | We only need one valid split. |
| `return dp[n]` | Answer for the entire string. | `s[:n]` is `s`. |

---

## 8. Dry Run

**Input:** `s = "leetcode"`, `wordDict = ["leet", "code"]` (official Example 1). `max_len = 4`, `n = 8`.

Indices: `l(0) e(1) e(2) t(3) c(4) o(5) d(6) e(7)`.

| `end` | `start` range | `start` with `dp[start] = True` | piece `s[start:end]` | In words? | `dp[end]` |
|---|---|---|---|---|---|
| 0 | — | — | — | — | **True** (base) |
| 1 | 0..0 | 0 | `"l"` | no | False |
| 2 | 0..1 | 0 | `"le"` | no | False |
| 3 | 0..2 | 0 | `"lee"` | no | False |
| 4 | 0..3 | 0 | `"leet"` | **yes** | **True** |
| 5 | 1..4 | 4 | `"c"` | no | False |
| 6 | 2..5 | 4 | `"co"` | no | False |
| 7 | 3..6 | 4 | `"cod"` | no | False |
| 8 | 4..7 | 4 | `"code"` | **yes** | **True** |

Final table:

| `i` | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|---|
| `dp[i]` | T | F | F | F | T | F | F | F | T |

**Result:** `dp[8] = True` ✅ (`"leet" | "code"`)

**Second dry run (false case):** `s = "catsandog"`, `wordDict = ["cats", "dog", "sand", "and", "cat"]` (Example 3), `max_len = 4`.

| `i` | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| prefix ends with | — | c | a | t | s | a | n | d | o | g |
| `dp[i]` | T | F | F | T | T | F | F | T | F | F |
| reason | base | | | `"cat"` | `"cats"` | | | `"sand"` from 3, `"and"` from 4 | | |

- `dp[3]`: `dp[0]` and `"cat"` ✓. `dp[4]`: `dp[0]` and `"cats"` ✓.
- `dp[7]`: `dp[3]` and `s[3:7] = "sand"` ✓.
- `dp[8]`: candidates `start = 4..7`; the `True` ones are `dp[4]` and `dp[7]`, giving pieces `s[4:8] = "ando"` and `s[7:8] = "o"` — neither is a word → False.
- `dp[9]`: `start = 5..8`; only `dp[7]` is true, and `s[7:9] = "og"` is not a word → False.

**Result:** `dp[9] = False` ✅

---

## 9. Concepts, Data Structures, and Patterns

- **Prefix DP on strings:** `dp[i]` describes `s[:i]`; transitions try the **last piece**. The same idea powers [Decode Ways](063_decode_ways.md) and Palindrome Partitioning.
- **"Last choice" thinking:** like [Coin Change](056_coin_change.md), where the last coin is chosen; here the last word is chosen. Coins become words, and "amount" becomes "prefix length".
- **Hash set lookups:** `in` on a `set` is average `O(1)` per hash, but hashing a slice of length `L` costs `O(L)`.
- **Bounding the search with `max_len`:** a simple trick that turns `O(n²)` candidate pieces into `O(n × max_len)`.
- **Memoization ↔ tabulation:** `can(start)` (suffix-based, top-down) and `dp[end]` (prefix-based, bottom-up) are mirror images.
- **Graph / BFS view:** positions `0..n` are nodes; an edge `j → i` exists when `s[j:i]` is a word. The question is "is `n` reachable from `0`?" (practice Q2).
- **Trie (prefix tree) alternative:** walking a trie from each `start` finds all words beginning there in one pass, avoiding repeated slicing. See [Implement Trie](../07_tree/052_implement_trie_prefix_tree.md).
- **Related:** Word Break II (LeetCode 140) returns every sentence (practice Q1).

---

## 10. Complexity Analysis

Let `n = len(s)` (≤ 300), `L = max_len` (≤ 20), `W = len(wordDict)` (≤ 1000).

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Brute-force recursion | `O(2^n × n)` worst case | `O(n)` | Up to `2^(n-1)` cut patterns explored; each call slices and hashes pieces of length up to `n`. |
| Memoized recursion | `O(n³)` (or `O(n² × L)` with the length limit) | `O(n + W·L)` | `n + 1` states × up to `n` end positions × `O(n)` slice/hash; cache, stack and word set. |
| Bottom-up DP (optimized) | `O(n × L²)` (+ `O(W·L)` to build the set) | `O(n + W·L)` | For each `end`, at most `L` starts, each slicing/hashing `≤ L` characters. At the limits: `300 × 20 × 20 = 120 000` character operations. The set stores all words. |

---

## 11. Edge Cases

| Case | Example | Expected result | Why |
|---|---|---|---|
| Single letter that is a word | `"a"`, `["a"]` | `true` | One piece. |
| Single letter not in dict | `"a"`, `["b"]` | `false` | No piece fits. |
| Word reused | `"applepenapple"`, `["apple", "pen"]` | `true` | Reuse is allowed. |
| Greedy longest-match trap | `"goalspecial"`, `["go", "goal", "goals", "special"]` | `true` | `"goal" + "special"`; greedy `"goals"` would fail. |
| Two lengths combine | `"aaaaaaa"`, `["aaaa", "aaa"]` | `true` | `7 = 4 + 3`. |
| Dictionary word longer than `s` | `"ab"`, `["abc"]` | `false` | No piece can match. |
| Exponential trap for brute force | `"aaaaaaaaaaab"`, `["a", "aa", "aaa"]` | `false` | The final `"b"` is in no word; DP answers instantly. |
| Leftover tail | `"catsandog"`, `["cats", "dog", "sand", "and", "cat"]` | `false` | `"og"` can't be covered. |

---

## 12. Common Mistakes and Debugging

1. **Forgetting `dp[0] = True`.** Then no first word can ever be accepted and the answer is always `False`.
2. **Greedy matching.** Always taking the longest (or first) matching word misses splits like `"goal" + "special"`.
3. **Off-by-one in slices.** `dp[i]` is about `s[:i]`, so the last word is `s[start:end]` with `end` **exclusive**; the loop must go up to `n` inclusive (`range(1, n + 1)`).
4. **Searching the list instead of a set.** `piece in wordDict` scans up to 1000 words each time.
5. **Returning `dp[n-1]`.** That's the prefix missing the last character.
6. **Only checking `s.startswith(word)` once.** You must restart the search at every reachable position, not just at the beginning.

**Debugging tip:** print `dp` as a string of `T`/`F` under the characters of `s`; the `T` marks should sit exactly where valid word boundaries are.

---

## 13. Practice Questions

**Q1. Word Break II (LeetCode 140): return every way to split `s` into dictionary words, as space-separated sentences.**

<details><summary>Hint</summary>Memoize `sentences(start)` = list of all sentences for `s[start:]`. For each word that matches at `start`, prepend it to each sentence of the remainder.</summary></details>

**Answer:**

```python
from functools import lru_cache


def word_break_all(s, word_dict):
    words = set(word_dict)

    @lru_cache(maxsize=None)
    def sentences(start):
        if start == len(s):
            return [""]                      # one way: no more words
        result = []
        for end in range(start + 1, len(s) + 1):
            piece = s[start:end]
            if piece in words:
                for rest in sentences(end):
                    result.append(piece + (" " + rest if rest else ""))
        return result

    return sentences(0)


assert sorted(word_break_all("catsanddog", ["cat", "cats", "and", "sand", "dog"])) == [
    "cat sand dog", "cats and dog"]
assert word_break_all("catsandog", ["cats", "dog", "sand", "and", "cat"]) == []
assert word_break_all("aaa", ["a", "aa"]) == ["a a a", "a aa", "aa a"]
```

The number of sentences can be exponential, so Word Break II has no polynomial bound in general — but the memo still avoids recomputing shared suffixes.

**Q2. Solve Word Break with BFS. What are the nodes and edges?**

<details><summary>Hint</summary>Nodes are positions `0..n`. From position `i`, you can jump to `i + len(word)` whenever `s` continues with that word.</summary></details>

**Answer:**

```python
from collections import deque


def word_break_bfs(s, word_dict):
    queue = deque([0])
    visited = {0}
    while queue:
        start = queue.popleft()
        if start == len(s):
            return True
        for word in word_dict:
            end = start + len(word)
            if end not in visited and s.startswith(word, start):
                visited.add(end)
                queue.append(end)
    return False


assert word_break_bfs("leetcode", ["leet", "code"]) is True
assert word_break_bfs("applepenapple", ["apple", "pen"]) is True
assert word_break_bfs("catsandog", ["cats", "dog", "sand", "and", "cat"]) is False
```

Each position is visited once, so this is `O(n × W × L)` time — fine here, and it shows the problem is really "reachability".

**Q3. Return the minimum number of words needed to split `s` (or `-1` if impossible).**

<details><summary>Hint</summary>Same table, but store a number instead of a boolean, exactly like Coin Change: `dp[end] = min(dp[start] + 1)`.</summary></details>

**Answer:**

```python
def min_words(s, word_dict):
    words = set(word_dict)
    n = len(s)
    INF = n + 1
    dp = [0] + [INF] * n
    for end in range(1, n + 1):
        for start in range(end):
            if dp[start] + 1 < dp[end] and s[start:end] in words:
                dp[end] = dp[start] + 1
    return dp[n] if dp[n] != INF else -1


assert min_words("applepenapple", ["apple", "pen", "applepen"]) == 2   # "applepen" + "apple"
assert min_words("leetcode", ["leet", "code", "l", "e", "t"]) == 2
assert min_words("catsandog", ["cats", "dog", "sand", "and", "cat"]) == -1
```

**Q4. Trace the DP for `s = "goalspecial"`, words `["go", "goal", "goals", "special"]`. Which `dp` entries are `True`?**

<details><summary>Hint</summary>Mark every index where some word ends after a `True` index.</summary></details>

**Answer:** `dp[0]` (base), `dp[2]` (`"go"`), `dp[4]` (`"goal"`), `dp[5]` (`"goals"`) and `dp[11]` (`"special"` = `s[4:11]` after `dp[4]`). From `dp[5]` the remaining `"pecial"` matches nothing, but `dp[4]` saves the day, so the answer is `true` — something greedy longest-match would miss.

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** 1-D prefix DP on a string ("last word" choice).
- **State:** `dp[i]` = can `s[:i]` be split into words?
- **Recurrence:** `dp[i] = any(dp[j] and s[j:i] in words)` for `i - max_len <= j < i`.
- **Base / order / answer:** `dp[0] = True`; `i = 1 → n`; answer `dp[n]`.
- **Time:** `O(n × L²)` with a hash set and the word-length bound. **Auxiliary space:** `O(n)` for the table plus the word set.
- **One-line memory hook:** *"Tick every spot where real words end; the last spot must be ticked."*

### Completion checklist

- [x] Problem requirements verified
- [x] Examples and constraints verified
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force solution written and tested
- [x] Memoized (top-down) bridge solution written and tested
- [x] Optimized Python solution written and tested (`tools/tests/p059.py`)
- [x] Line-by-line explanation written
- [x] Dry run completed with a real example (DP table)
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
