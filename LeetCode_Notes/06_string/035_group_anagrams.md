# 035. Group Anagrams

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Group Anagrams |
| **LeetCode number** | 49 |
| **Topic (source list)** | String |
| **Also uses** | Hash Table, Sorting, Counting |
| **Difficulty** | Medium |
| **LeetCode URL** | <https://leetcode.com/problems/group-anagrams/> |
| **Pattern** | Hash map keyed by a canonical form (sorted letters or letter counts) |

---

## 2. Problem Explanation

### What are we given?

`strs` — a list of strings made of lowercase English letters. Some strings may be empty (`""`), and the same string may appear more than once.

### What must we return?

A list of **groups** (each group is a list of strings) such that:

1. Two strings are in the **same group** exactly when they are **anagrams** of each other — the same letters with the same counts, possibly in a different order (see [034. Valid Anagram](034_valid_anagram.md)).
2. Every string from the input appears in exactly **one** group (duplicates included — if `"abc"` appears twice, both copies go into the group).

### Order does not matter

The groups may be returned in **any order**, and the strings inside a group may be in any order too. So for Example 1, `[["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]` and `[["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]` are both correct. (That's also why the tests for this note sort both levels before comparing.)

### Examples

**Example 1**

```text
Input:  strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
Output: [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]
```

- `"bat"` has no anagram partner in the list, so it is alone.
- `"nat"` and `"tan"` use the same letters (`a`, `n`, `t`).
- `"ate"`, `"eat"` and `"tea"` use the same letters (`a`, `e`, `t`).

**Example 2**

```text
Input:  strs = [""]
Output: [[""]]
```

One empty string forms one group.

**Example 3**

```text
Input:  strs = ["a"]
Output: [["a"]]
```

### Constraints

- `1 <= strs.length <= 10^4`
- `0 <= strs[i].length <= 100`
- `strs[i]` consists of lowercase English letters.

**Follow-up:** none in the statement.

---

## 3. Everyday Analogy

> **Explain it like I'm five**

You have a pile of word cards and want to put cards with the **same letters** into the same box.

Trick: for each card, write a **label** that ignores the order of letters — for example, the letters in alphabetical order. `"eat"`, `"tea"` and `"ate"` all get the label `"aet"`. `"tan"` and `"nat"` get the label `"ant"`.

Now you just need a shelf of boxes with labels:

- Read a card, make its label.
- If a box with that label exists, drop the card in.
- If not, make a new box with that label.

At the end, each box is one group. You looked at each card only once!

---

## 4. Step-by-Step Logic

1. **Anagram test for two words** is easy (Section 2 of [034](034_valid_anagram.md)), but comparing every word with every other word is slow.
2. **Find a "signature" (canonical key)** that is the **same for all anagrams** and **different for non-anagrams**. Then grouping = "put words with equal keys together".
3. **Key option A — sorted letters:** `"".join(sorted(word))`. `"eat"` → `"aet"`, `"tea"` → `"aet"`. Anagrams have identical sorted forms, and non-anagrams don't.
4. **Key option B — letter counts:** a tuple of 26 counts, e.g. `"eat"` → `(1, 0, 0, 0, 1, 0, …, 1, …)` (a=1, e=1, t=1). Anagrams have identical counts by definition.
5. **Keys must be hashable** to be used in a dictionary: strings and tuples are; lists are not. That's why we use `"".join(...)` or `tuple(...)`.
6. **Use a dictionary `key -> list of words`.** `defaultdict(list)` creates an empty list the first time a key is seen.
7. **Return the dictionary's values** as a list of lists.

---

## 5. Brute-Force Solution

### Algorithm

1. Keep a list of groups.
2. For each word, compare it with the **first word of each existing group** using an anagram check.
3. If it matches a group, append it there; otherwise start a new group.

Because "is an anagram of" is an equivalence relation (if A ~ B and B ~ C then A ~ C), comparing with one representative per group is enough.

### Python code

```python
from typing import List


class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        def same_letters(a: str, b: str) -> bool:
            if len(a) != len(b):
                return False
            counts = [0] * 26
            for x, y in zip(a, b):
                counts[ord(x) - ord('a')] += 1
                counts[ord(y) - ord('a')] -= 1
            return all(c == 0 for c in counts)

        groups = []
        for word in strs:
            for group in groups:
                if same_letters(group[0], word):   # compare with the representative
                    group.append(word)
                    break
            else:                                  # no group matched
                groups.append([word])
        return groups
```

### Explanation

- `same_letters` is the counting anagram check from [034](034_valid_anagram.md).
- The `for ... else` construct: the `else` block runs only when the inner loop finishes **without** `break`, i.e. no existing group matched.
- Duplicates and empty strings work naturally: `""` vs `""` has equal length 0 and all counts zero.

### Complexity

Let `n = len(strs)` and `k` = maximum word length.

- **Time:** `O(n² · k)` in the worst case (when every word is in its own group, each word is compared with up to `n` representatives, each comparison `O(k + 26)`). With `n = 10^4` and `k = 100` that's about 10¹⁰ steps → **times out**.
- **Auxiliary space:** `O(n)` for the group lists (they hold references to the input strings) plus `O(1)` per comparison.

---

## 6. Optimized Solution

### Idea

Compute a key for each word in `O(k)` and group with a hash map — one pass, no pairwise comparisons.

### Algorithm

1. `groups = defaultdict(list)`.
2. For each word: build `count = [0] * 26`, increment for each letter, convert to `tuple(count)` as the key, and append the word to `groups[key]`.
3. Return `list(groups.values())`.

### Python code (LeetCode-ready) — letter-count key

```python
from collections import defaultdict
from typing import List


class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        groups = defaultdict(list)     # key (26 counts) -> words with those counts

        for word in strs:
            count = [0] * 26
            for ch in word:
                count[ord(ch) - ord('a')] += 1
            groups[tuple(count)].append(word)   # tuples are hashable, lists are not

        return list(groups.values())
```

### Alternative — sorted-letters key (the most common interview answer)

```python
from collections import defaultdict
from typing import List


class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        groups = defaultdict(list)
        for word in strs:
            key = "".join(sorted(word))   # "eat" -> "aet"
            groups[key].append(word)
        return list(groups.values())
```

Shorter and very readable. Sorting each word costs `O(k log k)` instead of `O(k)`, but with `k ≤ 100` both are fast in practice.

---

## 7. Line-by-Line Explanation

(Letter-count version)

| Line | What it does | Why |
|---|---|---|
| `groups = defaultdict(list)` | Dictionary whose missing keys start as `[]`. | Lets us `append` without checking whether the key exists. |
| `for word in strs:` | Visits each word once. | One pass over the input. |
| `count = [0] * 26` | A fresh counter list for this word. | Must be new for every word, otherwise counts leak between words. |
| `for ch in word:` / `count[ord(ch) - ord('a')] += 1` | Counts each letter. | `ord(ch) - ord('a')` maps `'a'..'z'` to `0..25`. |
| `groups[tuple(count)].append(word)` | Uses the counts as the dictionary key and adds the word to its group. | Anagrams produce equal tuples → same group. Lists can't be dict keys because they are mutable (unhashable); tuples can. |
| `return list(groups.values())` | Collects all groups. | The problem accepts any order. (Since Python 3.7 dicts keep insertion order, so groups appear in order of first occurrence.) |

**Why the key is collision-free:** two words have the same 26-count tuple exactly when they contain the same number of each letter — the definition of an anagram. No two non-anagrams can share a key.

---

## 8. Dry Run

**Input:** `strs = ["eat", "tea", "tan", "ate", "nat", "bat"]` (Example 1).

The 26-count key is written compactly as its non-zero entries (e.g. `a1 e1 t1` means `count[a] = 1, count[e] = 1, count[t] = 1`, everything else 0). The sorted-letters key is shown alongside for comparison.

| Step | `word` | Count key (non-zero) | Sorted key | Key seen before? | `groups` after the step |
|---|---|---|---|---|---|
| 1 | `"eat"` | `a1 e1 t1` | `"aet"` | No → new group | `{aet: ["eat"]}` |
| 2 | `"tea"` | `a1 e1 t1` | `"aet"` | Yes | `{aet: ["eat", "tea"]}` |
| 3 | `"tan"` | `a1 n1 t1` | `"ant"` | No → new group | `{aet: ["eat", "tea"], ant: ["tan"]}` |
| 4 | `"ate"` | `a1 e1 t1` | `"aet"` | Yes | `{aet: ["eat", "tea", "ate"], ant: ["tan"]}` |
| 5 | `"nat"` | `a1 n1 t1` | `"ant"` | Yes | `{aet: [...3 words], ant: ["tan", "nat"]}` |
| 6 | `"bat"` | `a1 b1 t1` | `"abt"` | No → new group | `{aet: [...], ant: [...], abt: ["bat"]}` |

**Returned:** `[["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]`

This is the same grouping as the official output `[["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]`, just in a different order — which the problem allows ✅.

**Second dry run:** `strs = [""]` (Example 2)

| Step | `word` | Count key | Seen before? | `groups` |
|---|---|---|---|---|
| 1 | `""` | all 26 zeros | No → new group | `{(0,…,0): [""]}` |

**Returned:** `[[""]]` ✅ — the inner `for ch in word` loop simply doesn't run for an empty word.

---

## 9. Concepts, Data Structures, and Patterns

- **Canonical form / signature:** map every member of an equivalence class to one representative value. Here: sorted letters or letter counts. Grouping then becomes a dictionary lookup.
- **Hash map of lists (`defaultdict(list)`):** the standard "bucket things by key" tool.
- **Hashability:** dictionary keys must be immutable — `str` and `tuple` work, `list` doesn't.
- **Counting vs sorting trade-off:** counting is `O(k)` per word for a fixed alphabet; sorting is `O(k log k)` but works for any alphabet without changes.
- **Equivalence relations:** "is an anagram of" is reflexive, symmetric and transitive, which is why one representative per group is enough in the brute force.
- **Related notes:**
  - [034. Valid Anagram](034_valid_anagram.md) — the pairwise anagram test.
  - [033. Minimum Window Substring](033_minimum_window_substring.md) — counts used to compare multisets inside a window.
  - [001. Two Sum](../01_array/001_two_sum.md) and [003. Contains Duplicate](../01_array/003_contains_duplicate.md) — other hash-map lookups.
  - [074. Top K Frequent Elements](../10_heap/074_top_k_frequent_elements.md) — another "bucket by key, then post-process" problem.

---

## 10. Complexity Analysis

Let `n = len(strs)` and `k` = maximum length of a string (`k ≤ 100`). The alphabet has 26 letters.

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Brute force (compare with representatives) | `O(n² · k)` | `O(n)` | Up to `n` groups to check for each of `n` words; each check `O(k + 26)`. |
| Sorted-letters key | `O(n · k log k)` | `O(n · k)` | Sorting each word; the dictionary stores up to `n` keys of length up to `k`. |
| Letter-count key (optimized) | `O(n · (k + 26))`, i.e. `O(n · k)` for a fixed alphabet | `O(26 · n)` = `O(n)` | Counting each word plus building a 26-tuple; up to `n` keys, each a 26-tuple. |

In every approach the group lists hold **references** to the original strings (`O(n)` list slots). The returned list of groups is the output; together with the strings it holds it is `O(n · k)` in size, and is not counted as auxiliary space here.

---

## 11. Edge Cases

| Case | Example | Expected result (any order) | Why |
|---|---|---|---|
| Single empty string | `[""]` | `[[""]]` | Empty string has an all-zero key. |
| Several empty strings | `["", ""]` | `[["", ""]]` | Equal (all-zero) keys → same group. |
| Single word | `["a"]` | `[["a"]]` | One group. |
| Exact duplicates | `["abc", "abc", "cba"]` | `[["abc", "abc", "cba"]]` | Duplicates are kept, not merged away. |
| No anagrams at all | `["a", "b", "c"]` | `[["a"], ["b"], ["c"]]` | Every key is different. |
| Same letters, different counts | `["ab", "abb", "bba", "ba"]` | `[["ab", "ba"], ["abb", "bba"]]` | `"ab"` and `"abb"` share letters but not counts. |

---

## 12. Common Mistakes and Debugging

1. **Using a list as a dictionary key.** `groups[sorted(word)]` raises `TypeError: unhashable type: 'list'`. Use `"".join(sorted(word))` or `tuple(sorted(word))`.
2. **Using `set(word)` as the key.** `"ab"` and `"abb"` would wrongly share a group — counts matter.
3. **Building an ambiguous string key from counts without separators.** `"".join(map(str, count))` can collide: a word with `a×1, b×11` and a word with `a×11, b×1` both start with `"111"` (see Practice Q2). Use a tuple, or put a separator such as `"#"` between counts.
4. **Reusing one `count` list for all words.** Create it inside the loop.
5. **Comparing outputs in tests without normalizing.** The problem allows any order, so sort each group and then sort the list of groups before comparing.
6. **Dropping duplicates** by storing words in a `set`; each occurrence must appear in the output.

**Debugging tip:** print `dict(groups)` after the loop; every key should map to words that are anagrams of each other.

---

## 13. Practice Questions

**Q1. What are the sorted-letter keys of `"listen"`, `"silent"`, `"enlist"`, `"google"`, and how many groups do they form?**

<details><summary>Hint</summary>Sort each word's letters alphabetically.</summary></details>

**Answer:** `"listen"`, `"silent"`, `"enlist"` all become `"eilnst"`; `"google"` becomes `"eggloo"`. So there are **2 groups**: `["listen", "silent", "enlist"]` and `["google"]`.

**Q2. Show that `"".join(map(str, counts))` is an unsafe key, and fix it.**

<details><summary>Hint</summary>Find two words whose counts, written next to each other without separators, produce the same digits.</summary></details>

**Answer:** `"a" + "b" * 11` has counts `a=1, b=11` → digits `"1" + "11" + "0"*24`. `"a" * 11 + "b"` has `a=11, b=1` → `"11" + "1" + "0"*24`. Both are `"111000…0"`. A separator removes the ambiguity.

```python
def bad_key(word):
    counts = [0] * 26
    for ch in word:
        counts[ord(ch) - 97] += 1
    return "".join(map(str, counts))


def good_key(word):
    counts = [0] * 26
    for ch in word:
        counts[ord(ch) - 97] += 1
    return "#".join(map(str, counts))


w1 = "a" + "b" * 11
w2 = "a" * 11 + "b"
assert sorted(w1) != sorted(w2)          # not anagrams
assert bad_key(w1) == bad_key(w2)        # but the bad key collides
assert good_key(w1) != good_key(w2)      # separators fix it
```

**Q3. Return only the groups that contain at least two words, each group sorted, and the groups sorted by size (largest first, ties broken alphabetically by first word).**

<details><summary>Hint</summary>Group as usual, then filter and sort.</summary></details>

**Answer:**

```python
from collections import defaultdict


def anagram_families(strs):
    groups = defaultdict(list)
    for word in strs:
        groups["".join(sorted(word))].append(word)
    families = [sorted(g) for g in groups.values() if len(g) >= 2]
    families.sort(key=lambda g: (-len(g), g[0]))
    return families


assert anagram_families(["eat", "tea", "tan", "ate", "nat", "bat"]) == [
    ["ate", "eat", "tea"],
    ["nat", "tan"],
]
assert anagram_families(["a", "b"]) == []
```

**Q4. Group Shifted Strings (LeetCode 249, premium): group strings that can be turned into each other by shifting every letter forward by the same amount (wrapping `z` → `a`), e.g. `"abc"` → `"bcd"` → … → `"xyz"`.**

<details><summary>Hint</summary>Use a different canonical key: the differences between neighbouring letters, modulo 26.</summary></details>

**Answer:** Shifting every letter by the same amount keeps every neighbour gap (mod 26) the same, so the tuple of gaps is the key. Single letters all have the empty tuple as their key.

```python
from collections import defaultdict


def group_shifted(strings):
    groups = defaultdict(list)
    for word in strings:
        key = tuple((ord(word[i + 1]) - ord(word[i])) % 26 for i in range(len(word) - 1))
        groups[key].append(word)
    return sorted(sorted(g) for g in groups.values())


assert group_shifted(["abc", "bcd", "acef", "xyz", "az", "ba", "a", "z"]) == [
    ["a", "z"], ["abc", "bcd", "xyz"], ["acef"], ["az", "ba"],
]
```

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** Hash map keyed by a canonical form.
- **Key idea:** Anagrams share a signature — `tuple(26 counts)` or `"".join(sorted(word))`. Bucket words by signature with `defaultdict(list)`; return the buckets.
- **Time:** `O(n · k)` with count keys (`O(n · k log k)` with sorted keys).
- **Auxiliary space:** `O(n)` 26-tuples for count keys (`O(n · k)` for sorted keys), plus the group lists.
- **Testing note:** output order is free — normalize (sort inner lists, then the outer list) before comparing.
- **One-line memory hook:** *"Same label, same box."*

### Completion checklist

- [x] Problem requirements verified
- [x] Examples and constraints verified
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force solution written and tested
- [x] Optimized Python solution written and tested (`tools/tests/p035.py`), plus the sorted-key alternative
- [x] Line-by-line explanation written
- [x] Dry run completed with real examples
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
