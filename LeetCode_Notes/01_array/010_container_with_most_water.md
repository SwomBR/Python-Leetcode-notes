# 010. Container With Most Water

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Container With Most Water |
| **LeetCode number** | 11 |
| **Topic (source list)** | Array |
| **Also uses** | Two Pointers, Greedy |
| **Difficulty** | Medium |
| **LeetCode URL** | <https://leetcode.com/problems/container-with-most-water/> |
| **Pattern** | Two pointers moving inward, always moving the shorter wall |

---

## 2. Problem Explanation

### What are we given?

`height` — a list of `n` non-negative integers. Think of each entry as a vertical wall standing on the ground: wall number `i` stands at x-position `i` and is `height[i]` tall.

### What must we return?

Choose **two** walls. Together with the ground they form a container (like the two sides of a fish tank). Return the **largest amount of water** any such container can hold.

### How much water does a pair of walls hold?

For walls at positions `i < j`:

```text
water = width × water level
      = (j - i) × min(height[i], height[j])
```

- **Width** is the distance between the walls: `j - i`.
- **Water level** is limited by the **shorter** wall — pour any higher and the water spills over that side.
- The container must stand straight; you can't tilt it to hold more. Walls between `i` and `j` don't matter — they don't block or add anything in this problem.

### Examples

**Example 1**

```text
Input:  height = [1, 8, 6, 2, 5, 4, 8, 3, 7]
Output: 49
```

Pick the wall of height 8 at position 1 and the wall of height 7 at position 8. Width `8 - 1 = 7`, water level `min(8, 7) = 7`, so the water is `7 × 7 = 49`. No other pair holds more.

**Example 2**

```text
Input:  height = [1, 1]
Output: 1
```

The only pair: width 1, level 1, water `1`.

### Constraints

- `n == height.length`
- `2 <= n <= 10^5`
- `0 <= height[i] <= 10^4`

---

## 3. Everyday Analogy

> **Explain it like I'm five**

You and a friend each hold up a wooden board to make the two sides of a pool for your toy boats. The pool is as long as the distance between you, and the water can only be as deep as the **shorter** board.

Start with you standing at the very left end and your friend at the very right end — the widest pool possible. Now you want to try other pools. Whoever has the **shorter** board steps inward to swap for the next board.

Why the shorter one? The shorter board is what's holding the water level down. If the taller person moves instead, the pool gets narrower and the water still can't rise above the short board — that can only make things worse. Moving the short one is the only move that *might* find a taller board and raise the water.

Keep stepping inward until you meet, and remember the biggest pool you ever made.

---

## 4. Step-by-Step Logic

1. **Area formula:** `area(i, j) = (j - i) × min(height[i], height[j])`.
2. **Start with the widest pair:** `left = 0`, `right = n - 1`. Width is as large as it can be.
3. **Which pointer to move?** Suppose `height[left] <= height[right]`. Any other pair that keeps `left` and uses some `right' < right` has:
   - a smaller width (`right' - left < right - left`), and
   - a level `min(height[left], height[right']) <= height[left]`.
   So it can never beat the area we just computed. **Every remaining pair that uses `left` is no better**, and we can throw `left` away: `left += 1`.
4. **Symmetric case:** if `height[right] < height[left]`, throw away `right`: `right -= 1`.
5. **Each step removes one wall** from consideration, so after `n - 1` steps the pointers meet and we've (implicitly) considered every useful pair.
6. **Ties:** if both walls are equal, moving either one is safe (the argument in step 3 works for both).

---

## 5. Brute-Force Solution

### Algorithm

Try every pair `i < j`, compute its area, keep the maximum.

### Python code

```python
from typing import List


class Solution:
    def maxArea(self, height: List[int]) -> int:
        n = len(height)
        best = 0
        for i in range(n):
            for j in range(i + 1, n):
                area = (j - i) * min(height[i], height[j])
                best = max(best, area)
        return best
```

### Explanation

- `j` starts at `i + 1`, so every pair of different walls is checked once.
- The area uses the shorter wall's height times the distance.
- `best` starts at 0, which is safe because areas are never negative (heights are `>= 0`).

### Complexity

- **Time:** `O(n²)` — about `n(n-1)/2 ≈ 5 × 10^9` pairs for `n = 10^5`. This **times out** on LeetCode.
- **Auxiliary space:** `O(1)`.

---

## 6. Optimized Solution

### Idea — two pointers, move the shorter wall

Start with the widest container. At each step, record its area, then move the pointer at the shorter wall inward, because that wall can't be part of any better container.

### Algorithm

1. `left = 0`, `right = n - 1`, `best = 0`.
2. While `left < right`:
   - `area = (right - left) × min(height[left], height[right])`; update `best`.
   - If `height[left] < height[right]`: `left += 1`; otherwise `right -= 1`.
3. Return `best`.

### Python code (LeetCode-ready)

```python
from typing import List


class Solution:
    def maxArea(self, height: List[int]) -> int:
        left, right = 0, len(height) - 1
        best = 0

        while left < right:
            width = right - left
            if height[left] < height[right]:
                best = max(best, width * height[left])
                left += 1            # the shorter wall can't do better with anyone else
            else:
                best = max(best, width * height[right])
                right -= 1

        return best
```

Inside each branch the shorter height is already known, so we multiply by it directly instead of calling `min`.

### Variant: skip walls that can't help

After moving past the shorter wall, any new wall that is **not taller** than the one we just left can't improve the area (narrower *and* no higher). This variant skips them in a tight loop. Same `O(n)` worst case, often fewer area computations.

```python
from typing import List


class Solution:
    def maxArea(self, height: List[int]) -> int:
        left, right = 0, len(height) - 1
        best = 0
        while left < right:
            h = min(height[left], height[right])
            best = max(best, (right - left) * h)
            while left < right and height[left] <= h:
                left += 1
            while left < right and height[right] <= h:
                right -= 1
        return best
```

Every wall skipped has height `<= h`, so any container using it is narrower than the current one and no taller — it cannot beat `best`.

---

## 7. Line-by-Line Explanation

(Main two-pointer version)

| Line | What it does | Why |
|---|---|---|
| `left, right = 0, len(height) - 1` | Pointers at the two outermost walls. | Starts with the maximum possible width. |
| `best = 0` | Largest area seen. | Areas are `>= 0`. |
| `while left < right:` | Continue while two different walls remain. | A container needs two walls. |
| `width = right - left` | Distance between the walls. | Part of the area formula. |
| `if height[left] < height[right]:` | Left wall is the shorter one. | The shorter wall sets the water level. |
| `best = max(best, width * height[left])` | Area with the left wall as the limit. | `min(...)` is `height[left]` here. |
| `left += 1` | Discard the left wall. | Every other partner for it is closer and gives a level no higher than `height[left]`. |
| `else:` | Right wall is shorter or equal. | — |
| `best = max(best, width * height[right])` | Area with the right wall as the limit. | `min(...)` is `height[right]`. |
| `right -= 1` | Discard the right wall. | Same argument; with a tie either side is safe to discard. |
| `return best` | Answer. | Every discarded wall had already reached its best possible container. |

---

## 8. Dry Run

**Input:** `height = [1, 8, 6, 2, 5, 4, 8, 3, 7]` (Example 1)

| Step | `left` | `right` | `height[left]` | `height[right]` | Width | Area = width × shorter | `best` | Move |
|---|---|---|---|---|---|---|---|---|
| 1 | 0 | 8 | 1 | 7 | 8 | 8 × 1 = 8 | 8 | left is shorter → `left = 1` |
| 2 | 1 | 8 | 8 | 7 | 7 | 7 × 7 = 49 | **49** | right is shorter → `right = 7` |
| 3 | 1 | 7 | 8 | 3 | 6 | 6 × 3 = 18 | 49 | `right = 6` |
| 4 | 1 | 6 | 8 | 8 | 5 | 5 × 8 = 40 | 49 | tie → `right = 5` |
| 5 | 1 | 5 | 8 | 4 | 4 | 4 × 4 = 16 | 49 | `right = 4` |
| 6 | 1 | 4 | 8 | 5 | 3 | 3 × 5 = 15 | 49 | `right = 3` |
| 7 | 1 | 3 | 8 | 2 | 2 | 2 × 2 = 4 | 49 | `right = 2` |
| 8 | 1 | 2 | 8 | 6 | 1 | 1 × 6 = 6 | 49 | `right = 1` → pointers meet |

**Result:** `49` ✅ — only 8 area computations instead of the brute force's 36.

**Example 2:** `height = [1, 1]` → width 1, area `1 × 1 = 1`; tie → `right = 0`, stop. **Result:** `1` ✅

---

## 9. Concepts, Data Structures, and Patterns

- **Two pointers (opposite ends):** start at both ends and move inward; each step permanently removes one candidate, giving `O(n)`.
- **Greedy elimination with a proof:** we don't try every pair — we prove that the discarded wall can't be in a better pair. This "exchange/elimination" argument is what makes two-pointer solutions correct.
- **Bottleneck (min) reasoning:** the answer depends on the *smaller* of two values, so improving it requires changing the smaller one.
- **Related notes:** the same inward two-pointer scan is the inner loop of [009_3sum.md](009_3sum.md). Trapping Rain Water (LeetCode 42) looks similar but counts water over *every* bar (see Q4).

---

## 10. Complexity Analysis

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Brute force | `O(n²)` | `O(1)` | Checks all `n(n-1)/2` pairs. |
| Two pointers (optimized) | `O(n)` | `O(1)` | Each iteration moves one pointer one step inward, so there are exactly `n - 1` iterations. Only a few integer variables are used. |
| Two pointers with skipping | `O(n)` | `O(1)` | Every inner `while` step also moves a pointer inward, so total pointer moves are still at most `n - 1`. |

---

## 11. Edge Cases

| Case | Example | Expected result | Why |
|---|---|---|---|
| Minimum length | `[1, 1]` | `1` | Official Example 2. |
| Zero heights | `[0, 0]` | `0` | No wall height, no water. |
| One zero wall | `[0, 5]` | `0` | Level is limited by the shorter wall (0). |
| Best pair is the outermost | `[4, 3, 2, 1, 4]` | `16` | Width 4 × level 4. |
| Middle wall is tallest | `[1, 2, 1]` | `2` | Outer pair gives `2 × 1 = 2`; no pair beats it. |
| Maximum heights | `[10000, 10000]` | `10000` | Width 1 × level 10000. |

---

## 12. Common Mistakes and Debugging

1. **Moving the taller wall.** On `[1, 8, 6, 2, 5, 4, 8, 3, 7]`, moving the taller side at step 1 discards the 7 at the right end and the 49 container is never seen. In fact the left pointer never moves (the 1 is never the taller wall), so you only ever measure containers using the height-1 wall and return 8.
2. **Using `max` instead of `min` for the level.** Water spills over the shorter wall.
3. **Forgetting the width or computing it as `right - left + 1`.** The distance between positions `i` and `j` is `j - i`.
4. **Confusing this with Trapping Rain Water.** Here only the two chosen walls matter; inner walls neither block nor add water.
5. **Moving both pointers on a tie in a way that skips walls** without justification. (It happens to be safe for equal walls, but beginners often also do it when the heights differ, which is wrong.)

**Debugging tip:** print `left, right, height[left], height[right], area, best` each iteration and compare with the dry-run table.

---

## 13. Practice Questions

**Q1. Trace the two-pointer algorithm on `[4, 3, 2, 1, 4]`.**

<details><summary>Hint</summary>The first container is already the widest and the outer walls are tall.</summary></details>

**Answer:** `left=0, right=4`: width 4, level 4 → 16 (best 16); tie → `right=3`. `(0,3)`: 3 × 1 = 3, `right=2`. `(0,2)`: 2 × 2 = 4, `right=1`. `(0,1)`: 1 × 3 = 3, `right=0`, stop. **Answer: 16.**

**Q2. Give an example showing that moving the taller wall can miss the answer.**

<details><summary>Hint</summary>Make the best container use the taller outer wall and a tall wall near the shorter side.</summary></details>

**Answer:** `height = [2, 10, 9]`. Start `(0, 2)`: area `2 × 2 = 4`. Moving the taller wall (index 2) leaves `(0, 1)`: `1 × 2 = 2` — and the best container `(1, 2)` with area `1 × 9 = 9` is never checked. Moving the shorter wall (index 0) gives `(1, 2)` = 9 ✅.

**Q3. Return the pair of indices `(i, j)` of one best container, not just the area.**

<details><summary>Hint</summary>Whenever the area improves, save the current `left` and `right`.</summary></details>

**Answer:**

```python
def best_container(height):
    left, right = 0, len(height) - 1
    best, best_pair = 0, (0, len(height) - 1)
    while left < right:
        area = (right - left) * min(height[left], height[right])
        if area > best:
            best, best_pair = area, (left, right)
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    return best, best_pair


assert best_container([1, 8, 6, 2, 5, 4, 8, 3, 7]) == (49, (1, 8))
assert best_container([1, 1]) == (1, (0, 1))
assert best_container([2, 10, 9]) == (9, (1, 2))
```

**Q4. Trapping Rain Water (LeetCode 42) also uses two pointers. Write it and explain the difference.**

<details><summary>Hint</summary>There, water sits on top of **every** bar: the water above bar `i` is `min(max on the left, max on the right) - height[i]`.</summary></details>

**Answer:** In Container With Most Water we pick **one** pair of walls and ignore everything between them. In Trapping Rain Water, every bar can hold water, and inner bars block water. Two pointers still work: process the side whose running maximum is smaller, because that maximum is the limiting level for that side.

```python
def trap(height):
    left, right = 0, len(height) - 1
    left_max = right_max = 0
    water = 0
    while left < right:
        if height[left] < height[right]:
            left_max = max(left_max, height[left])
            water += left_max - height[left]
            left += 1
        else:
            right_max = max(right_max, height[right])
            water += right_max - height[right]
            right -= 1
    return water


assert trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6
assert trap([4, 2, 0, 3, 2, 5]) == 9
assert trap([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 19   # not 49: a different question
```

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** Two pointers from both ends; greedy elimination.
- **Key idea:** area = `(right - left) × min(h[left], h[right])`; record it, then move the **shorter** wall inward — it can't be part of any better container.
- **Time:** `O(n)`.
- **Auxiliary space:** `O(1)`.
- **One-line memory hook:** *"The short board holds the water down — so the short board moves."*

### Completion checklist

- [x] Problem requirements verified
- [x] Examples and constraints verified
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force solution written and tested
- [x] Optimized Python solution written and tested (`tools/tests/p010.py`), plus the skipping variant
- [x] Line-by-line explanation written
- [x] Dry run completed with a real example
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
