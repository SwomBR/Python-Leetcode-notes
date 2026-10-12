# 036. Valid Parentheses

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Valid Parentheses |
| **LeetCode number** | 20 |
| **Topic (source list)** | String |
| **Also uses** | Stack, Hash Table |
| **Difficulty** | Easy |
| **LeetCode URL** | <https://leetcode.com/problems/valid-parentheses/> |
| **Pattern** | Matching pairs with a stack (last opened, first closed) |

---

## 2. Problem Explanation

### What are we given?

`s` — a string made **only** of the six bracket characters `(`, `)`, `[`, `]`, `{` and `}`.

### What must we return?

`True` if the brackets in `s` are **properly balanced**, otherwise `False`.

### The rules

A string counts as valid when all three of these hold:

1. **Same type.** Every opening bracket is closed by a closing bracket of the *same kind*: `(` with `)`, `[` with `]`, `{` with `}`.
2. **Correct order (nesting).** Brackets must close in the reverse order they were opened. If you open `(` and then `[`, the `[` must be closed before the `(`. So `([])` is fine, but `([)]` is not.
3. **No strays.** Every closing bracket must have a matching opening bracket before it. A leftover opening bracket at the end (like in `((`) also makes the string invalid.

### Examples

**Example 1**

```text
Input:  s = "()"
Output: true
```

One round pair, opened then closed.

**Example 2**

```text
Input:  s = "()[]{}"
Output: true
```

Three separate pairs sitting side by side; each one is closed before the next opens.

**Example 3**

```text
Input:  s = "(]"
Output: false
```

A round bracket is opened but a square bracket tries to close it — wrong type.

**Example 4**

```text
Input:  s = "([])"
Output: true
```

The square pair sits completely inside the round pair, so the nesting is correct.

**Example 5**

```text
Input:  s = "([)]"
Output: false
```

`(` opens, then `[` opens. The next character `)` tries to close the round bracket while the square bracket is still open — the order is wrong.

### Constraints

- `1 <= s.length <= 10^4`
- `s` consists of parentheses only `'()[]{}'`.

There is no follow-up for this problem.

---

## 3. Everyday Analogy

> **Explain it like I'm five**

Imagine stacking plates. Each time you see an **opening** bracket, you put a plate of that colour on top of the pile: a red plate for `(`, a blue plate for `[`, a green plate for `{`.

Each time you see a **closing** bracket, you must take a plate off the **top** of the pile — and its colour has to match. A `)` needs a red plate on top. You are not allowed to dig into the middle of the pile.

- If the pile is empty when you need a plate → something is wrong (a closing bracket with no partner).
- If the top plate is the wrong colour → wrong type or wrong order.
- When you reach the end, the pile must be **empty**. Any plates left over are brackets that were never closed.

That pile of plates is exactly what programmers call a **stack**.

---

## 4. Step-by-Step Logic

1. **What does "correct order" really mean?** The bracket that was opened **most recently** must be the **first** one to close. "Last in, first out" is the definition of a stack.
2. **Opening bracket:** we can't decide anything yet, so remember it by pushing it onto the stack.
3. **Closing bracket:** it must match the most recent unclosed opener — the top of the stack.
   - Stack empty → no opener to match → invalid.
   - Top is a different type → invalid.
   - Top matches → pop it; that pair is done.
4. **End of the string:** leftover openers mean some brackets were never closed → valid only if the stack is empty.
5. **Quick shortcut:** a valid string always has an even length (brackets come in pairs), so an odd length can return `False` immediately. This is optional; the stack check catches it anyway.
6. **Lookup table:** a dictionary `closing -> opening` (`')' -> '('` and so on) lets us find the expected partner in one step.

---

## 5. Brute-Force Solution

### Algorithm

A valid string always contains at least one **adjacent** pair `()`, `[]` or `{}` (the innermost pair). Removing it leaves a string that is valid if and only if the original was. So:

1. While the string contains `"()"`, `"[]"` or `"{}"`, delete those pairs.
2. When nothing more can be removed, the string was valid exactly when it has become empty.

### Python code

```python
class Solution:
    def isValid(self, s: str) -> bool:
        while True:
            shorter = s.replace("()", "").replace("[]", "").replace("{}", "")
            if shorter == s:          # nothing could be removed this round
                break
            s = shorter
        return s == ""
```

### Explanation

- Each round removes every adjacent matching pair currently visible.
- `([])` → remove `[]` → `()` → remove `()` → `""` → valid.
- `([)]` has no adjacent matching pair at all, so nothing is removed and the non-empty string means invalid.
- The loop stops as soon as a round changes nothing, so it always ends.

### Complexity

- **Time:** `O(n²)` in the worst case. A deeply nested string like `((((...))))` only exposes **one** removable pair per round, so there can be `n/2` rounds, and each `replace` scans and copies the whole string (`O(n)`). For `n = 10^4` that is `5 * 10^3` rounds; the string shrinks by 2 characters each round, so the rounds scan about `10^4 + 9998 + … + 2 ≈ 2.5 * 10^7` characters in total (times the three `replace` calls). Python's `replace` is implemented in C, so this usually still passes, but it is clearly worse than the one-pass stack.
- **Auxiliary space:** `O(n)` — each `replace` builds a new string.

---

## 6. Optimized Solution

### Idea

Walk through the string once with a stack of unmatched opening brackets. Every closing bracket must match the top of the stack.

### Algorithm

1. Create a dictionary `pairs = {')': '(', ']': '[', '}': '{'}`.
2. Create an empty list `stack`.
3. For each character `ch`:
   - If `ch` is a closing bracket (a key of `pairs`):
     - If the stack is empty or its top is not `pairs[ch]`, return `False`.
     - Otherwise pop the top.
   - Otherwise (an opening bracket) push `ch`.
4. Return `True` only if the stack is empty.

### Python code (LeetCode-ready)

```python
class Solution:
    def isValid(self, s: str) -> bool:
        if len(s) % 2 == 1:                 # odd length can never be balanced
            return False

        pairs = {")": "(", "]": "[", "}": "{"}  # closing -> its opening partner
        stack = []                           # unmatched opening brackets

        for ch in s:
            if ch in pairs:                  # closing bracket
                if not stack or stack[-1] != pairs[ch]:
                    return False
                stack.pop()                  # matched: this pair is finished
            else:                            # opening bracket
                stack.append(ch)

        return not stack                     # leftovers were never closed
```

---

## 7. Line-by-Line Explanation

| Line | What it does | Why |
|---|---|---|
| `if len(s) % 2 == 1: return False` | Rejects odd-length strings immediately. | Every valid string is made of pairs, so its length is even. Optional speed-up. |
| `pairs = {")": "(", ...}` | Maps each closing bracket to the opening bracket it needs. | Lets us check a match with one dictionary lookup instead of a chain of `if`s. |
| `stack = []` | A Python list used as a stack. | `append` pushes onto the top and `pop` removes from the top, both `O(1)`. |
| `for ch in s:` | Visits every character once, left to right. | The order of brackets matters, so we read them in order. |
| `if ch in pairs:` | Is this a closing bracket? | Only closing brackets are keys of `pairs`. |
| `if not stack or stack[-1] != pairs[ch]:` | Fails if there is nothing to match, or the most recent opener is the wrong type. | `not stack` is checked **first**, so `stack[-1]` is never read on an empty list (which would raise `IndexError`). |
| `return False` | Stops early. | One bad bracket is enough to make the whole string invalid. |
| `stack.pop()` | Removes the matched opener. | That pair is complete; the next closer must match whatever is now on top. |
| `else: stack.append(ch)` | Pushes an opening bracket. | It waits for its partner. |
| `return not stack` | `True` if the stack is empty, `False` otherwise. | Leftover openers (e.g. `"(("`) were never closed. |

---

## 8. Dry Run

**Input:** `s = "([])"` (Example 4). Length 4 is even, so we continue.

| Step | `ch` | Closing? | Stack before | Check | Stack after |
|---|---|---|---|---|---|
| 1 | `(` | No | `[]` | — | `['(']` |
| 2 | `[` | No | `['(']` | — | `['(', '[']` |
| 3 | `]` | Yes, needs `[` | `['(', '[']` | top is `[` ✓ | `['(']` |
| 4 | `)` | Yes, needs `(` | `['(']` | top is `(` ✓ | `[]` |

End of string: stack is empty → **`True`** ✅

**Second dry run:** `s = "([)]"` (Example 5)

| Step | `ch` | Closing? | Stack before | Check | Result |
|---|---|---|---|---|---|
| 1 | `(` | No | `[]` | — | push → `['(']` |
| 2 | `[` | No | `['(']` | — | push → `['(', '[']` |
| 3 | `)` | Yes, needs `(` | `['(', '[']` | top is `[` ✗ | return **`False`** |

**Result:** `False` ✅ — the square bracket was still open when the round one tried to close.

**Third (tiny) dry run:** `s = "(]"` → push `(`; then `]` needs `[` but the top is `(` → `False` ✅.

---

## 9. Concepts, Data Structures, and Patterns

- **Stack (LIFO — last in, first out):** the natural tool whenever "the most recent unfinished thing must be finished first". In Python, a plain `list` with `append` / `pop` / `[-1]` is a stack; all three operations are `O(1)`.
- **Hash map for pairing:** the `pairs` dictionary turns "what opener does this closer need?" into one lookup and makes it easy to add new bracket types.
- **Early exit:** returning `False` at the first mismatch avoids useless work.
- **Invariant:** at every moment, the stack holds exactly the opening brackets that have not been closed yet, in the order they were opened. A closer can only legally match the top.
- **Reduction idea (brute force):** repeatedly removing an innermost adjacent pair is a classic way to *reason* about balanced strings, even though it is slower.
- **Related problems and notes:**
  - Stacks of "unfinished work" also appear in iterative tree traversals, e.g. [050_kth_smallest_element_in_a_bst.md](../07_tree/050_kth_smallest_element_in_a_bst.md).
  - Other string-scanning notes in this section: [037_valid_palindrome.md](037_valid_palindrome.md) (two pointers), [034_valid_anagram.md](034_valid_anagram.md) (counting characters).
  - Outside this list: Generate Parentheses (LeetCode 22), Minimum Remove to Make Valid Parentheses (LeetCode 1249), Longest Valid Parentheses (LeetCode 32).

---

## 10. Complexity Analysis

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Brute force (remove pairs) | `O(n²)` | `O(n)` | Up to `n/2` rounds, each scanning/copying the string in `O(n)`; each round creates a new string. |
| Stack (optimized) | `O(n)` | `O(n)` | Each character is pushed and popped at most once (`O(1)` each). In the worst case (e.g. `"(((((("` of even length) every character is pushed, so the stack holds up to `n` items. The `pairs` dictionary has a fixed 3 entries, `O(1)`. |

---

## 11. Edge Cases

| Case | Example | Expected result | Why |
|---|---|---|---|
| Single character | `"("` | `False` | Odd length / opener never closed. |
| Starts with a closer | `")("` | `False` | First `)` finds an empty stack. |
| Only openers | `"(("` | `False` | Stack not empty at the end. |
| Only closers | `"))"` | `False` | Empty stack on the first `)`. |
| Deep nesting | `"(((())))"` | `True` | Each closer matches the most recent opener. |
| Mixed nesting | `"{[]}"` | `True` | Inner square pair closes before the outer curly pair. |
| Crossed pairs | `"([)]"` | `False` | Wrong closing order. |
| One extra closer at the end | `"())"` | `False` | Third character finds an empty stack. |
| One extra opener at the start | `"(()"` | `False` | Odd length (and one `(` left over). |

---

## 12. Common Mistakes and Debugging

1. **Only counting brackets.** Checking "number of `(` equals number of `)`" accepts `")("` and `"([)]"`. Order matters, which is why we need a stack.
2. **Forgetting the empty-stack check.** `stack[-1]` on an empty list raises `IndexError` (for input like `"]"`). Test `not stack` first — Python's `or` short-circuits, so the second part is skipped.
3. **Returning `True` at the end without checking the stack.** Input `"(("` never fails during the loop, but it is invalid. Return `not stack`.
4. **Mapping the wrong direction.** If the dictionary maps openers to closers, the closing-bracket lookup has to be reversed. Keeping `closing -> opening` makes the check `stack[-1] != pairs[ch]` read naturally.
5. **Popping before checking.** `stack.pop() != pairs[ch]` works only if you checked the stack is non-empty; mixing up the order is a common source of crashes.

**Debugging tip:** print `ch` and `stack` at the start of each iteration and compare with the dry-run tables.

---

## 13. Practice Questions

**Q1. Trace the stack for `s = "{[()]}"`. What is the largest the stack gets, and what is returned?**

<details><summary>Hint</summary>Push the three openers first, then watch them pop in reverse order.</summary></details>

**Answer:** Pushes give `['{']`, `['{', '[']`, `['{', '[', '(']` — the maximum size is **3**. Then `)` pops `(`, `]` pops `[`, `}` pops `{`, leaving an empty stack, so the result is `True`.

**Q2. If the string contains only `(` and `)`, can you check validity with `O(1)` extra space?**

<details><summary>Hint</summary>With a single bracket type, the stack only ever contains `(`, so you only need to know how many there are.</summary></details>

**Answer:** Keep a counter `open_count`. Add 1 for `(`; for `)` subtract 1 and fail if the counter goes negative. At the end the counter must be 0. This does not work with several bracket types, because a counter can't remember *which* type is on top.

```python
def is_valid_round_only(s):
    open_count = 0
    for ch in s:
        if ch == "(":
            open_count += 1
        else:
            open_count -= 1
            if open_count < 0:      # a ')' with nothing to close
                return False
    return open_count == 0


assert is_valid_round_only("(())()") is True
assert is_valid_round_only(")(") is False
assert is_valid_round_only("(()") is False
```

**Q3. Return the minimum number of brackets you must insert to make a string of `(` and `)` valid (LeetCode 921).**

<details><summary>Hint</summary>Count unmatched `)` while scanning (each needs a `(` inserted), and whatever `(` remain open at the end.</summary></details>

**Answer:** Every `)` that arrives when no `(` is open needs one insertion; every `(` still open at the end needs one insertion.

```python
def min_add_to_make_valid(s):
    open_count = 0
    insertions = 0
    for ch in s:
        if ch == "(":
            open_count += 1
        elif open_count > 0:
            open_count -= 1
        else:
            insertions += 1          # unmatched ')' needs a '(' before it
    return insertions + open_count   # unmatched '(' need a ')' after them


assert min_add_to_make_valid("())") == 1
assert min_add_to_make_valid("(((") == 3
assert min_add_to_make_valid("()") == 0
assert min_add_to_make_valid("()))((") == 4
```

**Q4. Extend the stack solution so that it ignores any non-bracket characters (e.g. `"a(b[c]d)e"` is valid).**

<details><summary>Hint</summary>Only react to characters that are openers or closers; skip everything else.</summary></details>

**Answer:**

```python
def is_valid_with_text(s):
    pairs = {")": "(", "]": "[", "}": "{"}
    openers = set(pairs.values())
    stack = []
    for ch in s:
        if ch in openers:
            stack.append(ch)
        elif ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
        # any other character is ignored
    return not stack


assert is_valid_with_text("a(b[c]d)e") is True
assert is_valid_with_text("x(y]z") is False
assert is_valid_with_text("no brackets") is True
```

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** Stack for matching pairs.
- **Key idea:** Push openers; each closer must match and pop the top; at the end the stack must be empty.
- **Time:** `O(n)`.
- **Auxiliary space:** `O(n)`.
- **One-line memory hook:** *"Last plate on the pile is the first plate off — and the colours must match."*

### Completion checklist

- [x] Problem requirements verified
- [x] Examples and constraints verified against the official statement
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force solution written and tested
- [x] Optimized Python solution written and tested (`tools/tests/p036.py`)
- [x] Line-by-line explanation written
- [x] Dry run completed with real examples
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
