# 002. Best Time to Buy and Sell Stock

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Best Time to Buy and Sell Stock |
| **LeetCode number** | 121 |
| **Topic (source list)** | Array |
| **Also uses** | Dynamic Programming (running minimum) |
| **Difficulty** | Easy |
| **LeetCode URL** | <https://leetcode.com/problems/best-time-to-buy-and-sell-stock/> |
| **Pattern** | One pass with a running minimum |

---

## 2. Problem Explanation

### What are we given?

`prices` — a list where `prices[i]` is the price of one stock on day `i`.

### What must we return?

The **largest profit** you can make by doing **one buy** followed by **one sell** on a **later** day. Profit = sell price − buy price.

### The rules

1. You buy exactly once and sell exactly once.
2. The sell day must come **after** the buy day — you cannot sell before you buy.
3. If no trade makes money, you simply don't trade, and the answer is `0`. (The answer is never negative.)

### Examples

**Example 1**

```text
Input:  prices = [7, 1, 5, 3, 6, 4]
Output: 5
```

Buy on day index 1 (price 1) and sell on day index 4 (price 6): profit `6 - 1 = 5`. (LeetCode counts days from 1, so it calls these day 2 and day 5; this note counts from 0 to match Python indices.) Buying at 1 and selling at 7 is not allowed, because the 7 happens *before* the 1.

**Example 2**

```text
Input:  prices = [7, 6, 4, 3, 1]
Output: 0
```

The price only goes down, so every trade loses money. Best choice: don't trade → `0`.

### Constraints

- `1 <= prices.length <= 10^5`
- `0 <= prices[i] <= 10^4`

---

## 3. Everyday Analogy

> **Explain it like I'm five**

You're selling lemonade cups, but first you have to buy lemons. Each day the lemon shop shows a price on a board. You can buy lemons on one day, and later trade them back on another day.

You walk past the board every day with a little sticky note. On the note you write **"cheapest price I've seen so far."** Every day you ask:

> "If I had bought on my cheapest day, and I sell **today**, how much would I earn?"

If that's the best amount you've ever calculated, you remember it. Then, if today's price is even cheaper than your sticky note, you update the sticky note.

You never need to walk backwards, because the sticky note already remembers the best buying day behind you.

---

## 4. Step-by-Step Logic

1. **What decides profit?** A buy day `i` and a later sell day `j`: profit `= prices[j] - prices[i]`.
2. **Fix the sell day.** If I decide to sell on day `j`, the best buy day is simply the **cheapest day before `j`**.
3. **So keep track of the cheapest price so far.** As we move from left to right, keep `min_price` = the minimum of everything we've passed.
4. **At each day,** the best profit if we sell today is `price - min_price`. Keep the best of these in `best_profit`.
5. **Update `min_price`** with today's price for future days.
6. **Start `best_profit` at 0**, which automatically handles the "don't trade" case.

---

## 5. Brute-Force Solution

### Algorithm

Try every buy day `i` and every later sell day `j`, and keep the largest `prices[j] - prices[i]`, never going below 0.

### Python code

```python
from typing import List


class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        best_profit = 0
        n = len(prices)
        for buy in range(n):
            for sell in range(buy + 1, n):
                best_profit = max(best_profit, prices[sell] - prices[buy])
        return best_profit
```

### Explanation

- The outer loop chooses the buy day.
- The inner loop starts at `buy + 1`, so the sell day is always later.
- `best_profit` starts at 0, so losing trades never become the answer.

### Complexity

- **Time:** `O(n²)` — about `n²/2` pairs. With `n = 10^5` that's about 5 billion operations, which **times out** on LeetCode.
- **Auxiliary space:** `O(1)`.

---

## 6. Optimized Solution

### Idea

Scan once. Keep the lowest price seen so far and the best profit seen so far.

### Algorithm

1. `min_price = infinity`, `best_profit = 0`.
2. For each `price`:
   - If `price < min_price`, set `min_price = price` (a better buy day).
   - Otherwise compute `price - min_price` and update `best_profit` if it is larger.
3. Return `best_profit`.

### Python code (LeetCode-ready)

```python
from typing import List


class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        min_price = float("inf")  # cheapest price seen so far
        best_profit = 0           # best profit seen so far (0 = don't trade)

        for price in prices:
            if price < min_price:
                min_price = price
            elif price - min_price > best_profit:
                best_profit = price - min_price

        return best_profit
```

---

## 7. Line-by-Line Explanation

| Line | What it does | Why |
|---|---|---|
| `min_price = float("inf")` | Starts the cheapest price at infinity. | Any real price will be smaller, so the first day becomes the first buy candidate. |
| `best_profit = 0` | Starts the answer at 0. | Represents "make no trade"; the answer can never go below this. |
| `for price in prices:` | Visits each day in time order. | Time order guarantees buy-before-sell. |
| `if price < min_price:` | Found a new cheapest day. | Selling today at a price below every earlier price cannot make a profit, so we only update the buy candidate. |
| `min_price = price` | Remember the new cheapest buy price. | Future days will compare against it. |
| `elif price - min_price > best_profit:` | Would selling today beat our record? | `min_price` is from an **earlier** (or the same) day, so this is a legal trade. |
| `best_profit = price - min_price` | Save the new record. | Keep the maximum. |
| `return best_profit` | Return the best profit found. | 0 if prices never rose. |

**Why `elif` is safe:** if `price < min_price`, then `price - min_price` would be negative, which can never beat `best_profit ≥ 0`. So we can skip the profit check on those days.

---

## 8. Dry Run

**Input:** `prices = [7, 1, 5, 3, 6, 4]`

| Day | `price` | `min_price` before | Branch taken | `price - min_price` | `min_price` after | `best_profit` after |
|---|---|---|---|---|---|---|
| 0 | 7 | ∞ | new minimum | — | 7 | 0 |
| 1 | 1 | 7 | new minimum | — | 1 | 0 |
| 2 | 5 | 1 | profit check | 4 | 1 | **4** |
| 3 | 3 | 1 | profit check | 2 (not better) | 1 | 4 |
| 4 | 6 | 1 | profit check | 5 | 1 | **5** |
| 5 | 4 | 1 | profit check | 3 (not better) | 1 | 5 |

**Result:** `5` ✅ (buy at 1 on day 1, sell at 6 on day 4)

**Second dry run:** `prices = [7, 6, 4, 3, 1]` — every day sets a new minimum, the profit branch never runs, and the answer stays `0` ✅.

---

## 9. Concepts, Data Structures, and Patterns

- **Running minimum (prefix minimum):** a value that summarizes "the best of everything to the left" so you don't have to look back.
- **Greedy / one-pass scan:** at each step we make the locally best decision (sell today against the cheapest earlier day) and keep the global best.
- **Dynamic programming view:** let `best[i]` be the best profit using days `0..i`. Then `best[i] = max(best[i-1], prices[i] - min(prices[0..i]))`. We only need the previous value, so it compresses to two variables.
- **Kadane connection:** If you build a list of day-to-day changes `diff[i] = prices[i] - prices[i-1]`, the answer is the maximum subarray sum of `diff` (or 0). See [005_maximum_subarray.md](005_maximum_subarray.md).
- **Python tip:** `float("inf")` is a convenient "bigger than anything" starting value.

---

## 10. Complexity Analysis

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Brute force | `O(n²)` | `O(1)` | Every (buy, sell) pair. |
| One pass (optimized) | `O(n)` | `O(1)` | Each price is visited once; only two variables are stored. |

---

## 11. Edge Cases

| Case | Example | Expected result | Why |
|---|---|---|---|
| Only one day | `[5]` | `0` | No later day to sell. |
| Strictly decreasing | `[7, 6, 4, 3, 1]` | `0` | Every trade loses money. |
| All prices equal | `[3, 3, 3]` | `0` | Profit is always 0. |
| Two days rising | `[1, 2]` | `1` | Buy day 0, sell day 1. |
| Minimum appears after the best trade | `[2, 4, 1]` | `2` | The final 1 is a new minimum but no later day exists; earlier best (2→4) stays. |
| Price 0 | `[0, 10]` | `10` | 0 is a valid price. |

---

## 12. Common Mistakes and Debugging

1. **Using `max(prices) - min(prices)`.** This ignores time order. For `[7, 1]` it gives 6, but the correct answer is 0 because the 7 comes first.
2. **Allowing negative answers.** Starting `best_profit` at `-infinity` or at `prices[1] - prices[0]` can return negative profit. Start at 0.
3. **Worrying about update order.** Writing `min_price = min(min_price, price)` *before* `best_profit = max(best_profit, price - min_price)` is also correct: on a new-minimum day the profit is `price - price = 0` (a same-day trade), which never beats `best_profit ≥ 0`. Either order works; just keep both updates inside the loop.
4. **Confusing this with Stock II (LeetCode 122)** where you may trade many times. Here you get exactly one transaction.

**Debugging tip:** print `(day, price, min_price, best_profit)` each iteration and compare to the dry-run table.

---

## 13. Practice Questions

**Q1. What is the answer for `prices = [3, 8, 1, 4]`?**

<details><summary>Hint</summary>The new minimum (1) appears after the big jump. Does it help?</summary></details>

**Answer:** `5`. Buy at 3, sell at 8. Later, `min_price` becomes 1 and selling at 4 gives only 3, which doesn't beat 5.

**Q2. Return the buy and sell *days* instead of just the profit (return `(-1, -1)` if no profitable trade).**

<details><summary>Hint</summary>Store the index of the minimum, not just its value.</summary></details>

**Answer:**

```python
def best_days(prices):
    min_day = 0
    best = (0, -1, -1)  # (profit, buy_day, sell_day)
    for day in range(1, len(prices)):
        if prices[day] < prices[min_day]:
            min_day = day
        elif prices[day] - prices[min_day] > best[0]:
            best = (prices[day] - prices[min_day], min_day, day)
    return (best[1], best[2])


assert best_days([7, 1, 5, 3, 6, 4]) == (1, 4)
assert best_days([7, 6, 4, 3, 1]) == (-1, -1)
```

**Q3. Solve it using Kadane's algorithm on daily differences.**

<details><summary>Hint</summary>Selling on day `j` after buying on day `i` earns the sum of the daily changes from `i+1` to `j`.</summary></details>

**Answer:**

```python
def max_profit_kadane(prices):
    best = current = 0
    for i in range(1, len(prices)):
        current = max(0, current + prices[i] - prices[i - 1])
        best = max(best, current)
    return best


assert max_profit_kadane([7, 1, 5, 3, 6, 4]) == 5
assert max_profit_kadane([7, 6, 4, 3, 1]) == 0
```

`current` is the best profit if we sell today; resetting to 0 means "buy today instead."

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** One pass with a running minimum.
- **Key idea:** The best buy day for selling today is the cheapest earlier day. Track `min_price` and `best_profit`.
- **Time:** `O(n)`.
- **Auxiliary space:** `O(1)`.
- **One-line memory hook:** *"Remember the cheapest day behind you; ask every day what selling now would earn."*

### Completion checklist

- [x] Problem requirements verified
- [x] Examples and constraints verified
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force solution written and tested
- [x] Optimized Python solution written and tested (`tools/tests/p002.py`)
- [x] Line-by-line explanation written
- [x] Dry run completed with a real example
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
