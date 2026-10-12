# 056. Coin Change

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Coin Change |
| **LeetCode number** | 322 |
| **Topic (source list)** | Dynamic Programming |
| **Also uses** | Recursion + memoization, Breadth-First Search (alternative view) |
| **Difficulty** | Medium |
| **LeetCode URL** | <https://leetcode.com/problems/coin-change/> |
| **Pattern** | 1-D DP over amounts ("unbounded knapsack", minimize count) |

---

## 2. Problem Explanation

### What are we given?

- `coins` — a list of coin values (denominations), for example `[1, 2, 5]`.
- `amount` — the total amount of money we want to pay.

### What must we return?

The **smallest number of coins** whose values add up to exactly `amount`. If no combination of coins can reach `amount` exactly, return `-1`.

### The rules

1. You have an **unlimited supply** of every coin value. Using the same coin many times is fine.
2. The coins must add up to **exactly** `amount` — not more, not less.
3. Paying an amount of `0` needs **zero coins**, so the answer for `amount = 0` is `0`.
4. Only the **count** of coins is returned, not which coins were used.

### Examples

**Example 1**

```text
Input:  coins = [1, 2, 5], amount = 11
Output: 3
```

`11 = 5 + 5 + 1` uses 3 coins. No way with 2 coins exists (the biggest 2-coin total is `5 + 5 = 10`).

**Example 2**

```text
Input:  coins = [2], amount = 3
Output: -1
```

Only 2-coins exist, so every total is even. 3 is odd, so it can never be made.

**Example 3**

```text
Input:  coins = [1], amount = 0
Output: 0
```

Nothing to pay, so no coins are needed.

### Constraints

- `1 <= coins.length <= 12`
- `1 <= coins[i] <= 2^31 - 1`
- `0 <= amount <= 10^4`

There is no official follow-up for this problem.

---

## 3. Everyday Analogy

> **Explain it like I'm five**

You're at a shop and must pay exactly 11 cents. Your piggy bank has a never-ending pile of 1-cent, 2-cent and 5-cent coins. You want to hand over as **few coins as possible** because counting coins is boring.

Grabbing the biggest coin first ("greedy") works with these coins, but not always. With 1, 3 and 4-cent coins and a price of 6, greedy gives `4 + 1 + 1` (3 coins), while `3 + 3` needs only 2.

So instead, you make a **cheat sheet**. You write the numbers 0, 1, 2, …, 11 on a piece of paper. Next to each one you write "the fewest coins to pay this much". You start with the easy ones (0 cents needs 0 coins) and work upward. For each new price you ask: *"If the last coin I hand over is a 1, a 2 or a 5, how many coins did the rest need?"* — and you just **read that from the sheet**, because you already filled in the smaller prices. Pick the best choice, write it down, move on.

When you reach 11, the cheat sheet tells you the answer.

---

## 4. Step-by-Step Logic

This is a classic **dynamic programming (DP)** problem. Let's follow the DP recipe.

1. **Find the choice.** To pay `a`, some coin must be the **last coin** you add. If that coin is `c`, the rest of the payment is `a - c`, and it should itself be paid as cheaply as possible.
2. **State definition.** `dp[a]` = the fewest coins needed to make exactly `a` (or "impossible").
3. **Recurrence.** Try every coin as the last coin:

   ```text
   dp[a] = 1 + min(dp[a - c])   over every coin c with c <= a
   ```

   If none of those `dp[a - c]` are possible, `dp[a]` is impossible too.
4. **Base case.** `dp[0] = 0` — zero coins pay zero.
5. **Iteration order.** `dp[a]` needs smaller amounts only, so fill `a = 1, 2, …, amount` from small to large.
6. **Answer location.** `dp[amount]`; translate "impossible" into `-1`.
7. **Representing "impossible".** Use a sentinel bigger than any real answer. The worst real answer uses `amount` coins (all 1s), so `amount + 1` works as "infinity" and stays a small integer.

**Why not greedy?** The greedy "take the largest coin that fits" rule ignores the future. Some coin systems (like real-world euros) happen to make greedy optimal, but the problem allows **any** coin values, e.g. `[1, 3, 4]`.

---

## 5. Brute-Force Solution

### Algorithm

Write the recurrence as a plain recursive function: `fewest(remaining)` tries every coin as the next coin and keeps the best result. When `remaining` hits 0, zero more coins are needed.

### Python code

```python
from typing import List


class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        INF = float("inf")

        def fewest(remaining: int) -> float:
            if remaining == 0:
                return 0
            best = INF
            for coin in coins:
                if coin <= remaining:
                    best = min(best, 1 + fewest(remaining - coin))
            return best

        result = fewest(amount)
        return -1 if result == INF else result
```

### Explanation

- `fewest(remaining)` returns the minimum number of coins for `remaining`, or infinity if it's impossible.
- Each call branches into up to `len(coins)` smaller calls, so the same sub-amounts are solved **again and again**. For example, `fewest(9)` is reached via `11 → 10 → 9`, `11 → 9`, and many other paths.
- The answer is correct because it literally tries every ordered sequence of coins.

### Complexity

- **Time:** exponential — roughly `O(k^(amount / min_coin))` where `k = len(coins)`. With `coins = [1, 2, 5]` and `amount = 10^4` the number of calls is astronomically large, so this **times out** at LeetCode limits.
- **Auxiliary space:** `O(amount / min_coin)` for the recursion stack (the deepest path uses the smallest coin every time). Deep recursion would also exceed Python's default recursion limit of 1000.

### The bridge: memoization (top-down DP)

The repeated work disappears if we **remember** each `fewest(remaining)` the first time we compute it. There are only `amount + 1` different arguments, so each is solved once.

```python
from typing import List
from functools import lru_cache


class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        INF = float("inf")

        @lru_cache(maxsize=None)
        def fewest(remaining: int) -> float:
            if remaining == 0:
                return 0
            best = INF
            for coin in coins:
                if coin <= remaining:
                    best = min(best, 1 + fewest(remaining - coin))
            return best

        result = fewest(amount)
        return -1 if result == INF else result
```

This runs in `O(amount × k)` time, but for `coins = [1]` and `amount = 10^4` the recursion is 10 000 calls deep, which crashes with `RecursionError` in Python unless you raise the limit. The bottom-up table below has the same complexity **without** recursion.

---

## 6. Optimized Solution

### Idea — bottom-up DP table

Fill `dp[0..amount]` from small amounts to large ones. Each entry looks back at `dp[a - coin]` for every coin.

### Algorithm

1. `INF = amount + 1` (an impossible coin count).
2. `dp = [0, INF, INF, …, INF]` (length `amount + 1`).
3. For `a` from `1` to `amount`:
   - For each `coin` with `coin <= a`: `dp[a] = min(dp[a], dp[a - coin] + 1)`.
4. Return `dp[amount]` if it is not `INF`, otherwise `-1`.

### Python code (LeetCode-ready)

```python
from typing import List


class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        INF = amount + 1                 # more coins than any real answer
        dp = [0] + [INF] * amount        # dp[a] = fewest coins to make a

        for a in range(1, amount + 1):
            for coin in coins:
                if coin <= a and dp[a - coin] + 1 < dp[a]:
                    dp[a] = dp[a - coin] + 1

        return dp[amount] if dp[amount] != INF else -1
```

---

## 7. Line-by-Line Explanation

| Line | What it does | Why |
|---|---|---|
| `INF = amount + 1` | Chooses a sentinel value for "impossible". | A real answer never exceeds `amount` (all 1-coins), so `amount + 1` can't be confused with a real answer. Using an `int` keeps the list numeric. |
| `dp = [0] + [INF] * amount` | Creates the table of length `amount + 1`. | `dp[0] = 0` is the base case; every other amount starts as "impossible" until we find a way. |
| `for a in range(1, amount + 1):` | Visits amounts in increasing order. | `dp[a]` depends only on smaller amounts, which are already final. |
| `for coin in coins:` | Tries each coin as the **last** coin. | The best payment of `a` ends with *some* coin. |
| `if coin <= a and dp[a - coin] + 1 < dp[a]:` | Checks the coin fits and the new count is better. | `coin <= a` keeps the index non-negative (and skips huge coins like `2^31 - 1`). If `dp[a - coin]` is `INF`, then `INF + 1` is never smaller than `dp[a]`, which is at most `INF`, so impossible paths are ignored automatically. |
| `dp[a] = dp[a - coin] + 1` | Records the improvement. | Pay `a - coin` optimally, then add one coin. |
| `return dp[amount] if dp[amount] != INF else -1` | Converts the sentinel into the required `-1`. | The problem wants `-1` for impossible amounts. |

---

## 8. Dry Run

**Input:** `coins = [1, 2, 5]`, `amount = 11` (official Example 1). `INF = 12`.

Each row computes `dp[a]` from the three candidates `dp[a-1]+1`, `dp[a-2]+1`, `dp[a-5]+1` ("—" means the coin is too big).

| `a` | via coin 1: `dp[a-1]+1` | via coin 2: `dp[a-2]+1` | via coin 5: `dp[a-5]+1` | `dp[a]` | One best payment |
|---|---|---|---|---|---|
| 0 | — | — | — | **0** | (base case) |
| 1 | 0+1 = 1 | — | — | **1** | 1 |
| 2 | 1+1 = 2 | 0+1 = 1 | — | **1** | 2 |
| 3 | 1+1 = 2 | 1+1 = 2 | — | **2** | 2+1 |
| 4 | 2+1 = 3 | 1+1 = 2 | — | **2** | 2+2 |
| 5 | 2+1 = 3 | 2+1 = 3 | 0+1 = 1 | **1** | 5 |
| 6 | 1+1 = 2 | 2+1 = 3 | 1+1 = 2 | **2** | 5+1 |
| 7 | 2+1 = 3 | 1+1 = 2 | 1+1 = 2 | **2** | 5+2 |
| 8 | 2+1 = 3 | 2+1 = 3 | 2+1 = 3 | **3** | 5+2+1 |
| 9 | 3+1 = 4 | 2+1 = 3 | 2+1 = 3 | **3** | 5+2+2 |
| 10 | 3+1 = 4 | 3+1 = 4 | 1+1 = 2 | **2** | 5+5 |
| 11 | 2+1 = 3 | 3+1 = 4 | 2+1 = 3 | **3** | 5+5+1 |

Final table: `dp = [0, 1, 1, 2, 2, 1, 2, 2, 3, 3, 2, 3]`.

**Result:** `dp[11] = 3` ✅

**Second dry run (impossible):** `coins = [2]`, `amount = 3`, `INF = 4`.

| `a` | via coin 2 | `dp[a]` |
|---|---|---|
| 0 | — | 0 |
| 1 | — (2 > 1) | 4 (`INF`) |
| 2 | `dp[0]+1 = 1` | 1 |
| 3 | `dp[1]+1 = 5`, not `< 4` | 4 (`INF`) |

`dp[3]` is still `INF`, so we return `-1` ✅.

---

## 9. Concepts, Data Structures, and Patterns

- **Dynamic programming recipe:** state → recurrence → base case → iteration order → answer location. This note uses it explicitly; every DP note in this folder follows the same steps.
- **Optimal substructure:** an optimal payment of `a` that ends with coin `c` contains an optimal payment of `a - c`. That is what lets `dp[a]` be built from smaller entries.
- **Overlapping subproblems:** the brute force solves the same `remaining` many times; memoization or a table removes the repeats.
- **Top-down vs bottom-up:** memoized recursion (`lru_cache`) and the table loop compute the same values. The table avoids Python's recursion limit.
- **Unbounded knapsack:** each item (coin) may be used any number of times; here we minimize the item count.
- **Sentinel "infinity":** `amount + 1` acts as infinity and keeps arithmetic safe.
- **BFS view:** amounts are graph nodes, each coin is an edge, and the answer is the shortest path from `amount` to `0`. BFS also runs in `O(amount × k)`.
- **Related notes:** [Climbing Stairs](055_climbing_stairs.md) (count ways instead of minimizing), [Combination Sum IV](060_combination_sum.md) (counts *ordered* ways to reach a total — same loop shape, `+=` instead of `min`), [Word Break](059_word_break_problem.md) (same "last piece" thinking on strings).

---

## 10. Complexity Analysis

Let `k = len(coins)` (at most 12) and `A = amount` (at most `10^4`).

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Brute-force recursion | Exponential, about `O(k^(A / min_coin))` | `O(A / min_coin)` | Each call branches up to `k` ways; the stack depth is the longest coin sequence. |
| Memoized recursion | `O(A × k)` | `O(A)` | `A + 1` distinct states, each loops over `k` coins once; cache + stack are `O(A)`. |
| Bottom-up DP (optimized) | `O(A × k)` | `O(A)` | Two nested loops: `A` amounts × `k` coins, constant work each. The `dp` list has `A + 1` entries. At the limits that is about `1.2 × 10^5` steps. |

---

## 11. Edge Cases

| Case | Example | Expected result | Why |
|---|---|---|---|
| Amount is zero | `coins = [1]`, `amount = 0` | `0` | Base case `dp[0] = 0`. |
| Impossible (parity) | `coins = [2]`, `amount = 3` | `-1` | Only even totals are reachable. |
| Every coin too big | `coins = [5]`, `amount = 3` | `-1` | No coin fits; `dp[3]` stays `INF`. |
| Huge coin value | `coins = [2147483647]`, `amount = 2` | `-1` | The `coin <= a` check skips it without indexing errors. |
| Greedy fails | `coins = [1, 3, 4]`, `amount = 6` | `2` | `3 + 3` beats greedy `4 + 1 + 1`. |
| One coin type repeated | `coins = [3, 7]`, `amount = 14` | `2` | `7 + 7`. |
| Largest amount with only 1-coins | `coins = [1]`, `amount = 10000` | `10000` | Bottom-up handles it; recursion would overflow the stack. |
| Classic tricky test | `coins = [186, 419, 83, 408]`, `amount = 6249` | `20` | Large mixed denominations; greedy fails here too. |

---

## 12. Common Mistakes and Debugging

1. **Using a greedy algorithm.** Taking the largest coin first fails for `[1, 3, 4]`, `6`. Always use DP when coin values are arbitrary.
2. **Forgetting the base case `dp[0] = 0`.** If every entry starts at `INF`, nothing can ever be built.
3. **Returning `INF` instead of `-1`.** Convert the sentinel at the end.
4. **Negative indices.** Without `coin <= a`, `dp[a - coin]` with a negative index silently reads from the **end** of the Python list — a nasty bug that gives wrong answers instead of an error.
5. **Using `float("inf")` and then returning it.** Fine internally, but returning `inf` (a float) instead of `-1` fails the judge.
6. **Allocating `dp` of size `max(coins)`.** Coins can be up to `2^31 - 1`; the table must be indexed by **amount**, not by coin value.
7. **Deep memoized recursion in Python.** `amount = 10^4` with a 1-coin recurses 10 000 deep → `RecursionError`. Prefer the bottom-up table.

**Debugging tip:** print the whole `dp` list for a small input such as `coins = [1, 2, 5]`, `amount = 11` and compare it with the dry-run table: `[0, 1, 1, 2, 2, 1, 2, 2, 3, 3, 2, 3]`.

---

## 13. Practice Questions

**Q1. Fill the DP table for `coins = [1, 3, 4]`, `amount = 6`. What is the answer, and what does greedy return?**

<details><summary>Hint</summary>Compute `dp[a] = 1 + min(dp[a-1], dp[a-3], dp[a-4])` for `a = 1..6`.</summary></details>

**Answer:** `dp = [0, 1, 2, 1, 1, 2, 2]`.
- `dp[5] = 1 + min(dp[4], dp[2], dp[1]) = 1 + 1 = 2` (4+1).
- `dp[6] = 1 + min(dp[5], dp[3], dp[2]) = 1 + 1 = 2` (3+3).

The answer is `2`. Greedy takes 4, then 1, then 1 → `3` coins, which is wrong.

**Q2. Coin Change II (LeetCode 518): count how many different *combinations* (order doesn't matter) make `amount`.**

<details><summary>Hint</summary>Put the **coin loop outside** and the amount loop inside, so each combination is built in one fixed coin order and counted once.</summary></details>

**Answer:** `ways[a]` = number of combinations using the coins processed so far.

```python
def coin_change_ii(amount, coins):
    ways = [0] * (amount + 1)
    ways[0] = 1                       # one way to make 0: use nothing
    for coin in coins:                # coins outside -> order ignored
        for a in range(coin, amount + 1):
            ways[a] += ways[a - coin]
    return ways[amount]


assert coin_change_ii(5, [1, 2, 5]) == 4      # 5, 2+2+1, 2+1+1+1, 1*5
assert coin_change_ii(3, [2]) == 0
assert coin_change_ii(10, [10]) == 1
assert coin_change_ii(0, [7]) == 1
```

Compare with [Combination Sum IV](060_combination_sum.md), where swapping the loops counts *ordered* sequences instead.

**Q3. Return the actual list of coins used in one optimal answer (or `[]` if impossible).**

<details><summary>Hint</summary>Alongside `dp[a]`, remember which coin produced the best value (`last[a]`). Walk back from `amount` using it.</summary></details>

**Answer:**

```python
def coin_change_with_coins(coins, amount):
    INF = amount + 1
    dp = [0] + [INF] * amount
    last = [0] * (amount + 1)          # last coin used to reach dp[a]
    for a in range(1, amount + 1):
        for coin in coins:
            if coin <= a and dp[a - coin] + 1 < dp[a]:
                dp[a] = dp[a - coin] + 1
                last[a] = coin
    if dp[amount] == INF:
        return []
    used = []
    a = amount
    while a > 0:
        used.append(last[a])
        a -= last[a]
    return used


assert sorted(coin_change_with_coins([1, 2, 5], 11)) == [1, 5, 5]
assert sorted(coin_change_with_coins([1, 3, 4], 6)) == [3, 3]
assert coin_change_with_coins([2], 3) == []
assert coin_change_with_coins([1], 0) == []
```

**Q4. Solve the problem with BFS instead of a table. Why does BFS give the minimum?**

<details><summary>Hint</summary>Each "level" of BFS adds exactly one coin. The first time you reach 0 is at the smallest level.</summary></details>

**Answer:** BFS explores all totals reachable with 1 coin, then 2 coins, and so on. The first level that hits exactly `amount` is the fewest coins.

```python
from collections import deque


def coin_change_bfs(coins, amount):
    if amount == 0:
        return 0
    seen = {0}
    queue = deque([0])
    steps = 0
    while queue:
        steps += 1
        for _ in range(len(queue)):          # one BFS level = one more coin
            total = queue.popleft()
            for coin in coins:
                nxt = total + coin
                if nxt == amount:
                    return steps
                if nxt < amount and nxt not in seen:
                    seen.add(nxt)
                    queue.append(nxt)
    return -1


assert coin_change_bfs([1, 2, 5], 11) == 3
assert coin_change_bfs([2], 3) == -1
assert coin_change_bfs([1], 0) == 0
assert coin_change_bfs([1, 3, 4], 6) == 2
```

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** 1-D DP over amounts (unbounded knapsack, minimize).
- **State:** `dp[a]` = fewest coins to make `a`.
- **Recurrence:** `dp[a] = 1 + min(dp[a - c])` over coins `c <= a`.
- **Base case:** `dp[0] = 0`; everything else starts at `INF = amount + 1`.
- **Order / answer:** `a = 1 → amount`; answer `dp[amount]` or `-1`.
- **Time:** `O(amount × len(coins))`. **Auxiliary space:** `O(amount)`.
- **One-line memory hook:** *"Which coin did I hand over last? Read the rest from the cheat sheet."*

### Completion checklist

- [x] Problem requirements verified
- [x] Examples and constraints verified
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force solution written and tested
- [x] Memoized (top-down) bridge solution written and tested
- [x] Optimized Python solution written and tested (`tools/tests/p056.py`)
- [x] Line-by-line explanation written
- [x] Dry run completed with a real example (full DP table)
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
