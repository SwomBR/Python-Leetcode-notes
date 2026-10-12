# 040. Encode and Decode Strings (LeetCode Premium)

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Encode and Decode Strings |
| **LeetCode number** | 271 (Premium) |
| **Topic (source list)** | String |
| **Also uses** | Design, Array |
| **Difficulty** | Medium |
| **LeetCode URL** | <https://leetcode.com/problems/encode-and-decode-strings/> |
| **Free practice** | LintCode 659 — Encode and Decode Strings |
| **Pattern** | Length-prefix encoding (a tiny serialization format) |

---

## 2. Problem Explanation

> ⚠️ **Caveat:** This is a LeetCode Premium problem. The official statement could not be checked for these notes; the examples and constraints below are the commonly published ones — confirm them on LeetCode if you have Premium access.

### What are we given?

A class `Codec` with two methods to implement:

- `encode(self, strs: List[str]) -> str` — receives a **list of strings** and must squash it into **one single string**.
- `decode(self, s: str) -> List[str]` — receives that single string and must rebuild the **original list exactly**.

### What must we guarantee?

For every valid input list `strs`:

```text
decode(encode(strs)) == strs
```

Same number of strings, same order, every character identical — including **empty strings** and strings that contain digits, `#`, commas, backslashes, spaces, newlines or any other of the 256 ASCII characters.

### The rules (as commonly published)

1. Think of `encode` running on one machine and `decode` on another; only the encoded string travels between them. The commonly published driver is:

   ```text
   Machine 1:  encoder = Codec();  msg = encoder.encode(strs)
   Machine 1  ---- msg ---->  Machine 2
   Machine 2:  decoder = Codec();  result = decoder.decode(msg)
   ```

   So the two methods may run on **different** `Codec` objects: `encode` must not store anything in the object (or in globals) for `decode` to read later. Everything `decode` needs must be inside the string.
2. Do not lean on a built-in serializer (such as `eval`, `pickle` or `json`) — design the format yourself.
3. Because the strings may contain **any** character, there is no "safe" separator character you can simply split on.

### Examples (commonly published)

**Example 1**

```text
Input:  dummy_input = ["Hello", "World"]
Output: ["Hello", "World"]
```

`encode(["Hello", "World"])` produces some string; `decode` of that string must give back `["Hello", "World"]`.

**Example 2**

```text
Input:  dummy_input = [""]
Output: [""]
```

A list with a single **empty** string must come back as a list with a single empty string — not as `[]`.

### Constraints (commonly published)

- `1 <= strs.length <= 200`
- `0 <= strs[i].length <= 200`
- `strs[i]` contains any possible characters out of 256 valid ASCII characters.

**Follow-up:** Could you write a generalized algorithm to work on any possible set of characters?

---

## 3. Everyday Analogy

> **Explain it like I'm five**

You want to mail several notes to a friend, but the post office only lets you send **one long strip of paper**. If you just glue the notes together, your friend can't tell where one note ends and the next begins.

You might try writing a `#` between notes — but what if a note itself contains a `#`? Your friend would cut it in the wrong place.

The clever trick: before each note, write **how many letters it has**, then a `#`, then the note. For example `5#Hello5#World`. Your friend reads the number `5`, skips the `#`, then counts out exactly 5 letters — `Hello` — **without even looking at what those letters are**. Then the next number, and so on. Even if a note is full of `#`s and digits, the counting never gets confused.

An empty note is just `0#` — "zero letters follow".

---

## 4. Step-by-Step Logic

1. **Why simple joining fails.** `"".join(strs)` loses the boundaries: `["ab", "c"]` and `["a", "bc"]` both become `"abc"`.
2. **Why a separator fails.** `"#".join(strs)` and `split("#")` break as soon as a string contains `#`: `["a#b"]` encodes to `"a#b"` and decodes to `["a", "b"]`. Also `[]` and `[""]` both encode to `""`, so they can't be told apart.
3. **Two classic fixes:**
   - **Escaping:** mark every special character inside the data so it can't be mistaken for a separator (like `\,` in CSV-style formats). Correct, but decoding must look at every character.
   - **Length prefix:** write each string's length before it. The decoder reads the length, then **jumps** over exactly that many characters. The contents are never interpreted, so any character is safe.
4. **Reading the length.** The length has a variable number of digits (`0` to `200`), so we end it with a marker `#`. The decoder reads digits until the first `#` **at the current position**. That `#` can't be confused with a `#` inside a string, because the decoder always starts reading a header exactly where the previous string ended, and the header itself only contains digits.
5. **Decoding loop:** `i` points at the start of a header. Find the `#` at position `j`; `length = int(s[i:j])`; the string is `s[j + 1 : j + 1 + length]`; move `i` to `j + 1 + length`. Repeat until `i` reaches the end.

---

## 5. Brute-Force Solution

The "naive" idea of joining with a separator is **broken** (it is not a valid solution), shown here only to see what goes wrong:

```text
encode: "#".join(strs)          decode: s.split("#")

["a#b"]       -> "a#b"          -> ["a", "b"]     (wrong: 2 strings)
[]            -> ""             -> [""]           (wrong: invented a string)
[""]          -> ""             -> [""]           (only works by luck)
```

### Simple correct approach — escaping + terminator

### Algorithm

1. **Encode:** for each string, double every backslash (`\` → `\\`) and put a backslash before every comma (`,` → `\,`). Then end the string with a bare `,` as a terminator.
2. **Decode:** scan character by character:
   - `\` → the **next** character is literal data; take it and skip both.
   - bare `,` → the current string is finished; save it and start a new one.
   - anything else → ordinary data.

Using a terminator *after* every string (instead of a separator *between* strings) makes `[]` → `""` and `[""]` → `","` different.

### Python code

```python
from typing import List


class Codec:
    def encode(self, strs: List[str]) -> str:
        """Encodes a list of strings to a single string."""
        parts = []
        for word in strs:
            escaped = word.replace("\\", "\\\\").replace(",", "\\,")
            parts.append(escaped + ",")          # bare comma ends each string
        return "".join(parts)

    def decode(self, s: str) -> List[str]:
        """Decodes a single string to a list of strings."""
        result, current = [], []
        i = 0
        while i < len(s):
            ch = s[i]
            if ch == "\\":                       # escaped character follows
                current.append(s[i + 1])
                i += 2
            elif ch == ",":                      # end of one string
                result.append("".join(current))
                current = []
                i += 1
            else:
                current.append(ch)
                i += 1
        return result
```

### Explanation

- Backslashes are escaped **first**; otherwise the backslashes added for commas would be doubled again.
- After encoding, a **bare** comma (one not preceded by an escaping backslash) can only be a terminator, and every backslash starts a two-character escape. So decoding is unambiguous.
- `["a,b", ""]` → `"a\,b,"` + `","` → `"a\,b,,"` → decoded back to `["a,b", ""]`.

### Complexity

Let `N` = total number of characters in all strings, `k` = number of strings.

- **Time:** `O(N + k)` for both methods — every character is handled a constant number of times. This easily fits the limits; it is the "simple first try" rather than a slow brute force.
- **Auxiliary space:** `O(N + k)` — the escaped pieces in `encode` and the `current` character list in `decode`.
- **Downsides:** the encoded string can be up to about **twice** as long (`2N + k`) if the data is full of commas/backslashes, and the decoder must inspect every single character in a Python loop.

---

## 6. Optimized Solution

### Idea — length prefix

Write each string as `<length>#<string>`. The decoder reads the length and jumps straight over the content using slicing.

### Algorithm

**Encode:** `"".join(f"{len(word)}#{word}" for word in strs)`.

**Decode:**

1. `i = 0`, `result = []`.
2. While `i < len(s)`:
   - Find `j`, the first `#` at or after `i` (only digits lie between `i` and `j`).
   - `length = int(s[i:j])`.
   - Append `s[j + 1 : j + 1 + length]`.
   - `i = j + 1 + length`.
3. Return `result`.

### Python code (LeetCode-ready)

```python
from typing import List


class Codec:
    def encode(self, strs: List[str]) -> str:
        """Encodes a list of strings to a single string."""
        return "".join(f"{len(word)}#{word}" for word in strs)

    def decode(self, s: str) -> List[str]:
        """Decodes a single string to a list of strings."""
        result = []
        i = 0
        while i < len(s):
            j = s.find("#", i)                    # end of the length header
            length = int(s[i:j])
            result.append(s[j + 1:j + 1 + length])
            i = j + 1 + length                   # jump to the next header
        return result
```

**Why `s.find("#", i)` is safe:** at position `i` we are always at the start of a header, and a header consists only of digits followed by `#`. So the first `#` at or after `i` is the header's own `#`; the search never reaches the string content, where other `#` characters may live.

**Follow-up (any character set):** this format never looks inside the content, so it works for any characters at all (any Unicode text), as long as `len` counts the same units on both sides (in Python, `len` counts characters).

---

## 7. Line-by-Line Explanation

| Line | What it does | Why |
|---|---|---|
| `return "".join(f"{len(word)}#{word}" for word in strs)` | Builds `length#content` for each string and glues them together. | `join` builds the final string in one go (`O(total length)`), avoiding repeated `+=` copying. |
| `result = []` | The decoded strings. | Returned at the end. |
| `i = 0` | Current reading position — always the start of a header. | The format is read strictly left to right. |
| `while i < len(s):` | Repeats until the whole message is consumed. | For `strs = []`, the message is `""`, the loop never runs, and `[]` is returned. |
| `j = s.find("#", i)` | Position of the `#` that ends the header. | Only digits sit between `i` and `j`. |
| `length = int(s[i:j])` | Converts the digit characters into a number. | E.g. `"12"` → `12`. |
| `result.append(s[j + 1:j + 1 + length])` | Cuts out exactly `length` characters after the `#`. | The content is copied blindly — `#`, digits, anything. For `length = 0` this is `""`. |
| `i = j + 1 + length` | Jumps past the content. | The next header starts right there. |
| `return result` | The rebuilt list. | Same strings, same order. |

---

## 8. Dry Run

**Input:** `strs = ["Hello", "World"]` (commonly published Example 1)

**Encode:** `"5#Hello"` + `"5#World"` → `s = "5#Hello5#World"` (14 characters, indices 0–13).

**Decode:**

| Step | `i` | `j = s.find("#", i)` | `s[i:j]` → `length` | Slice `s[j+1 : j+1+length]` | Appended | New `i` |
|---|---|---|---|---|---|---|
| 1 | 0 | 1 | `"5"` → 5 | `s[2:7]` = `"Hello"` | `"Hello"` | 7 |
| 2 | 7 | 8 | `"5"` → 5 | `s[9:14]` = `"World"` | `"World"` | 14 |
| — | 14 | — | loop ends (`14 == len(s)`) | — | — | — |

**Result:** `["Hello", "World"]` ✅

**Second dry run (tricky contents):** `strs = ["", "3#a"]`

**Encode:** `"0#"` + `"3#3#a"` → `s = "0#3#3#a"` (indices `0:'0' 1:'#' 2:'3' 3:'#' 4:'3' 5:'#' 6:'a'`).

| Step | `i` | `j` | `length` | Slice | Appended | New `i` |
|---|---|---|---|---|---|---|
| 1 | 0 | 1 | 0 | `s[2:2]` = `""` | `""` | 2 |
| 2 | 2 | 3 | 3 | `s[4:7]` = `"3#a"` | `"3#a"` | 7 |

**Result:** `["", "3#a"]` ✅ — the `#` and the digit inside `"3#a"` were never mistaken for a header, because the decoder jumped over them.

**Example 2:** `[""]` → `"0#"` → one header with length 0 → `[""]` ✅.

---

## 9. Concepts, Data Structures, and Patterns

- **Serialization:** turning a structure into a flat string and back. The format must be **unambiguous** — every encoded string must decode to exactly one list.
- **Length-prefix framing:** used by real network protocols (and HTTP "chunked" transfer encoding) for exactly this reason: content never needs escaping.
- **Escaping:** the alternative used by CSV, JSON strings and C string literals; correct but inflates the data and forces character-by-character parsing.
- **Terminator vs separator:** a terminator after every item keeps `[]` and `[""]` distinct; a separator between items does not.
- **Stateless design:** `encode` and `decode` may run on different objects/machines, so all information must live in the message.
- **String building:** `"".join(...)` is linear; repeated `+=` in a loop can be quadratic in some Python implementations.
- **Related notes:** [046_serialize_and_deserialize_binary_tree.md](../07_tree/046_serialize_and_deserialize_binary_tree.md) applies the same encode/decode idea to a tree; [036_valid_parentheses.md](036_valid_parentheses.md) is another left-to-right string scanner.

---

## 10. Complexity Analysis

Let `N` = total characters across all strings, `k` = number of strings.

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Escaping + terminator | `O(N + k)` | `O(N + k)` | Every character is copied/inspected a constant number of times; encoded size up to `2N + k`. |
| Length prefix (optimized) | `O(N + k)` | `O(N + k)` for `encode`'s temporary pieces; `O(1)` extra in `decode` besides the output list | Each header has at most 3 digits here (lengths ≤ 200), so the encoded size is at most `N + 4k`. `find` only scans the short header; slicing copies each string once. |

**Header length in general:** a length `L` needs about `log10(L) + 1` digits, so the encoded size is `N + O(k · log L)` — still linear in practice.

---

## 11. Edge Cases

| Case | Example `strs` | Encoded (length prefix) | Decoded | Why it works |
|---|---|---|---|---|
| Single empty string | `[""]` | `"0#"` | `[""]` | Length 0 → empty slice. |
| Several empty strings | `["", ""]` | `"0#0#"` | `["", ""]` | Each header is read separately. |
| Contains `#` | `["#"]` | `"1##"` | `["#"]` | Header `1#`, then one character `#`. |
| Looks like a header | `["3#abc"]` | `"5#3#abc"` | `["3#abc"]` | Content is skipped, never parsed. |
| Long string | `["a" * 200]` | `"200#aaa…"` | same | Multi-digit header. |
| Control / extended ASCII | `["\x00", "\xff", "\n"]` | `"1#\x001#\xff1#\n"` | same | Content is copied blindly. |
| Empty list (beyond the commonly published constraints) | `[]` | `""` | `[]` | Loop never runs. Tested as a robustness check. |

---

## 12. Common Mistakes and Debugging

1. **Splitting on a separator.** Any separator character can appear inside the data. Use length prefixes (or proper escaping).
2. **Writing the length without a marker.** `"5Hello12abc…"` — the decoder can't tell where the number stops if the content begins with a digit (`["1", "2"]` → `"1112"`). Use a `#` after the number, or a fixed-width header.
3. **Searching for `#` from the wrong place.** `s.find("#")` without the start index `i` always finds the first `#` in the whole string.
4. **Escaping commas before backslashes.** The backslashes added for commas then get doubled, corrupting the data. Escape `\` first.
5. **Storing state in the object.** Saving `strs` in `self` and returning it from `decode` fails when encode and decode run on separate `Codec` objects.
6. **Mixing up `[]` and `[""]`.** Formats that use separators between items can't distinguish them; test both.

**Debugging tip:** print `repr(encoded)` — `repr` shows invisible characters like `\n` and `\x00` — and then print `i, j, length` in each decode step.

---

## 13. Practice Questions

**Q1. What does the optimized `encode` produce for `["12", "", "#"]`, and how is it decoded?**

<details><summary>Hint</summary>Write `len#content` for each string, then decode by reading a header and jumping.</summary></details>

**Answer:** `"2#12"` + `"0#"` + `"1##"` = `"2#120#1##"`. Decoding: header `2` → take `"12"`, `i = 4`; header `0` → take `""`, `i = 6`; header `1` → take `"#"`, `i = 9` = end. Result `["12", "", "#"]`.

**Q2. Use a fixed-width 3-digit header instead of `#` (lengths are at most 200).**

<details><summary>Hint</summary>`f"{len(word):03d}"` pads with zeros; the decoder always reads exactly 3 characters.</summary></details>

**Answer:** With a fixed width, no marker is needed — the decoder knows the header is always 3 characters long.

```python
def encode_fixed(strs):
    return "".join(f"{len(word):03d}{word}" for word in strs)


def decode_fixed(s):
    result, i = [], 0
    while i < len(s):
        length = int(s[i:i + 3])
        result.append(s[i + 3:i + 3 + length])
        i += 3 + length
    return result


for sample in (["Hello", "World"], [""], ["007", "#", ""], []):
    assert decode_fixed(encode_fixed(sample)) == sample
assert encode_fixed(["Hi", ""]) == "002Hi000"
```

The trade-off: a fixed width wastes space on short strings and has a maximum length (999 here); the `#` version adapts to any length.

**Q3. Show that the naive `"#".join` / `split("#")` codec is ambiguous by finding two different lists that encode to the same string.**

<details><summary>Hint</summary>Put a `#` inside one of the strings.</summary></details>

**Answer:** `["a#b"]` and `["a", "b"]` both encode to `"a#b"`, so no decoder can know which one was meant. The length-prefix codec gives `"3#a#b"` and `"1#a1#b"` — different.

```python
def naive_encode(strs):
    return "#".join(strs)


def prefix_encode(strs):
    return "".join(f"{len(w)}#{w}" for w in strs)


assert naive_encode(["a#b"]) == naive_encode(["a", "b"])        # collision
assert prefix_encode(["a#b"]) != prefix_encode(["a", "b"])      # no collision
assert naive_encode([]) == naive_encode([""])                   # another collision
```

**Q4. Could `decode` use `s.split("#")` together with the lengths? Why is that a bad idea?**

<details><summary>Hint</summary>What happens to strings that contain `#`?</summary></details>

**Answer:** `split` cuts at **every** `#`, including those inside the content, so the pieces no longer correspond to headers and strings. You would have to glue pieces back together using the lengths — more complex and error-prone than simply reading the header and slicing.

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** Length-prefix serialization (`len#content`).
- **Key idea:** The decoder reads digits up to `#`, then jumps exactly `length` characters — it never interprets the content, so any character (and empty strings) are safe.
- **Time:** `O(N + k)` for encode and decode.
- **Auxiliary space:** `O(N + k)` temporary pieces in `encode`; `O(1)` extra in `decode` besides the output.
- **One-line memory hook:** *"Say how long the note is, then read exactly that much."*

### Completion checklist

- [x] Problem requirements written from the commonly published description (Premium; official text unavailable)
- [ ] Examples and constraints verified against official statement — **not done**: this is a LeetCode Premium problem and the official statement could not be fetched; the examples and constraints above are the commonly published ones
- [x] Beginner-friendly analogy and logic written
- [x] Simple correct (escaping) solution written and tested
- [x] Optimized Python solution written and tested (`tools/tests/p040.py`: round-trips over `chr(0)`–`chr(255)`, empty strings, `#`, digits, and `[]`)
- [x] Line-by-line explanation written
- [x] Dry run completed with the commonly published example
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
