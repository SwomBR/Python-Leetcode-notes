# 067. Course Schedule

## 1. Problem Overview

| Field | Details |
|---|---|
| **Problem** | Course Schedule |
| **LeetCode number** | 207 |
| **Topic (source list)** | Graph |
| **Also uses** | Topological Sort, Breadth-First Search, Depth-First Search |
| **Difficulty** | Medium |
| **LeetCode URL** | <https://leetcode.com/problems/course-schedule/> |
| **Pattern** | Cycle detection in a directed graph (Kahn's algorithm / DFS colouring) |

---

## 2. Problem Explanation

### Graph refresher

If graphs are new to you, read the primer in [066_clone_graph.md](066_clone_graph.md) first. This problem adds two new ideas:

- **Directed edge:** an arrow `b → a` that only goes one way. Here it means "course `b` must come before course `a`".
- **In-degree:** the number of arrows pointing **into** a node — for a course, the number of prerequisites it still needs.
- **Cycle:** a path of arrows that leads back to where it started, e.g. `0 → 1 → 0`.

```text
prerequisites = [[1,0]]           prerequisites = [[1,0],[0,1]]

     0 ───► 1                          0 ───► 1
                                       ▲      │
  take 0, then 1: possible             └──────┘
                                    each waits for the other: impossible
```

### What are we given?

- `numCourses` — the number of courses, labelled `0` to `numCourses - 1`.
- `prerequisites` — a list of pairs `[a, b]`. The pair means: **to take course `a`, you must already have finished course `b`.** (Careful: the course comes first, its prerequisite second.)

### What must we return?

`True` if there is some order in which you can take **all** the courses, otherwise `False`.

### The key insight

You can finish everything **exactly when the prerequisite graph has no cycle**.

- If there is a cycle, every course on it is waiting for another course on it, so none of them can ever be first.
- If there is no cycle (the graph is a **DAG** — directed acyclic graph), there is always at least one course with no unfinished prerequisites; take it, remove it, and repeat. This ordering is called a **topological order**.

### Examples

**Example 1**

```text
Input:  numCourses = 2, prerequisites = [[1,0]]
Output: true
```

Course 1 needs course 0. Take 0, then 1.

**Example 2**

```text
Input:  numCourses = 2, prerequisites = [[1,0],[0,1]]
Output: false
```

Course 1 needs course 0 and course 0 needs course 1. Neither can be taken first.

### Constraints

- `1 <= numCourses <= 2000`
- `0 <= prerequisites.length <= 5000`
- `prerequisites[i].length == 2`
- `0 <= ai, bi < numCourses`
- All the pairs `prerequisites[i]` are unique.

Note that the constraints do **not** forbid a pair like `[0, 0]` (a course that requires itself). That is a cycle of length 1, and the answer must then be `False`. All solutions below handle it.

There is no follow-up. (LeetCode 210, Course Schedule II, asks you to return the actual order — see Q3 below.)

---

## 3. Everyday Analogy

> **Explain it like I'm five**

Imagine a stack of toy boxes where some boxes have a sticky note saying *"Open box 3 before me!"*.

The easy plan: look for any box with **no sticky notes left**. Open it. Then go through the other boxes and tear off every note that mentioned the box you just opened. Some boxes now have no notes — open those next. Keep going.

If you open every box, you win. If you get stuck with boxes that still have notes — for example box A says "open B first" and box B says "open A first" — those boxes are stuck forever. That is a **cycle**.

---

## 4. Step-by-Step Logic

1. **Model it as a graph.** One node per course. For each pair `[a, b]`, draw an arrow `b → a` ("b unlocks a").
2. **Count prerequisites.** `indegree[a]` = how many arrows point into `a` = how many courses `a` still waits for.
3. **Start with free courses.** Every course with `indegree == 0` can be taken right now. Put them in a queue.
4. **Take a course, unlock others.** Pop a course, count it as taken, and for each course it unlocks, decrease that course's in-degree by 1. If it drops to 0, that course is now free — push it.
5. **Finish.** When the queue is empty, if we took `numCourses` courses, there is no cycle → `True`. Otherwise some courses never reached in-degree 0, which only happens when they are on (or behind) a cycle → `False`.

This is **Kahn's algorithm**, a BFS-based topological sort.

---

## 5. Brute-Force Solution

### Algorithm (repeated scanning)

Simulate a student who keeps re-reading the whole course catalogue:

1. Build `needs[course]` = list of that course's prerequisites.
2. Repeat rounds. In each round, scan every course; if it is not taken yet and **all** of its prerequisites are taken, take it.
3. Stop when a full round takes nothing new.
4. Return whether every course was taken.

### Python code

```python
from typing import List


class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        needs = [[] for _ in range(numCourses)]
        for course, pre in prerequisites:
            needs[course].append(pre)

        taken = [False] * numCourses
        taken_count = 0
        progress = True
        while progress:                 # keep scanning while something changes
            progress = False
            for course in range(numCourses):
                if not taken[course] and all(taken[p] for p in needs[course]):
                    taken[course] = True
                    taken_count += 1
                    progress = True

        return taken_count == numCourses
```

### Explanation

- A course becomes "taken" only when every prerequisite is already taken, so the simulation never cheats.
- If there is no cycle, each round takes at least one new course (a DAG always has a free course), so eventually everything is taken.
- If there is a cycle, the courses on it never become free, a round eventually takes nothing, and we return `False`.

### Complexity

- **One round** looks at all `V = numCourses` courses and, in the worst case, every prerequisite list once: `O(V + E)`, where `E = len(prerequisites)`.
- **Number of rounds:** each productive round takes at least one course, so there are at most `V + 1` rounds. The worst case really happens: with a chain where course `i` needs course `i + 1`, the scan from `0` upward can only take one course per round.
- **Time:** `O(V · (V + E))` — up to about `2000 × 7000 = 1.4·10^7` basic steps at the limits. That is a lot slower than linear, but still feasible here; the optimized algorithm does the same work in **one** pass.
- **Auxiliary space:** `O(V + E)` for `needs` and `taken`.

The waste is clear: every round re-checks courses whose situation has not changed. Kahn's algorithm only looks at a course when one of its prerequisites has just been finished.

---

## 6. Optimized Solution

### Idea — Kahn's algorithm (BFS topological sort)

Keep a counter of remaining prerequisites (`indegree`) for every course and a queue of courses whose counter is 0. Taking a course decrements the counters of the courses it unlocks.

### Algorithm

1. Build the adjacency list `graph[pre]` = courses that `pre` unlocks, and `indegree[course]`.
2. Push every course with `indegree == 0` into a queue.
3. While the queue is not empty: pop a course, increase `taken`, decrement each unlocked course's in-degree, and push any that reach 0.
4. Return `taken == numCourses`.

### Python code (LeetCode-ready, recommended)

```python
from collections import deque
from typing import List


class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        graph = [[] for _ in range(numCourses)]   # pre -> courses it unlocks
        indegree = [0] * numCourses               # unfinished prerequisites
        for course, pre in prerequisites:
            graph[pre].append(course)
            indegree[course] += 1

        queue = deque(c for c in range(numCourses) if indegree[c] == 0)
        taken = 0
        while queue:
            current = queue.popleft()
            taken += 1
            for nxt in graph[current]:
                indegree[nxt] -= 1
                if indegree[nxt] == 0:
                    queue.append(nxt)

        return taken == numCourses
```

### Alternative — DFS with three colours

Colour every course:

- **WHITE (0):** not visited yet.
- **GRAY (1):** on the current DFS path (we are "inside" it).
- **BLACK (2):** fully explored; proven to lead to no cycle.

Reaching a **GRAY** node means we followed arrows back onto our own path — a cycle. Reaching a BLACK node is safe and needs no more work.

```python
import sys
from typing import List


class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        # A chain of 2000 courses means recursion 2000 deep; CPython's default
        # limit is 1000, so raise it (2000 frames is safe for the real stack).
        if sys.getrecursionlimit() < 10000:
            sys.setrecursionlimit(10000)

        WHITE, GRAY, BLACK = 0, 1, 2
        graph = [[] for _ in range(numCourses)]
        for course, pre in prerequisites:
            graph[pre].append(course)
        color = [WHITE] * numCourses

        def has_cycle(u: int) -> bool:
            color[u] = GRAY                       # u is on the current path
            for v in graph[u]:
                if color[v] == GRAY:              # back to our own path
                    return True
                if color[v] == WHITE and has_cycle(v):
                    return True
            color[u] = BLACK                      # finished, no cycle through u
            return False

        for c in range(numCourses):
            if color[c] == WHITE and has_cycle(c):
                return False
        return True
```

Why two "visited" colours instead of one? A plain visited set cannot tell "I'm on this path right now" (a cycle) from "I finished this node earlier through a different path" (perfectly fine, e.g. the diamond `0 → 1 → 3` and `0 → 2 → 3`).

**Which to use?** Both are `O(V + E)`. Kahn's algorithm is iterative (no recursion-limit worries) and also gives the course order for free, so it is the one recommended here.

---

## 7. Line-by-Line Explanation

For Kahn's algorithm:

| Line | What it does | Why |
|---|---|---|
| `graph = [[] for _ in range(numCourses)]` | One empty list per course. | Adjacency list: `graph[pre]` will hold the courses that `pre` unlocks. |
| `indegree = [0] * numCourses` | One counter per course. | Counts how many prerequisites each course still waits for. |
| `for course, pre in prerequisites:` | Unpacks each pair `[a, b]` as `course = a`, `pre = b`. | The pair order is "course, then prerequisite". |
| `graph[pre].append(course)` | Adds the arrow `pre → course`. | When `pre` is finished, we must visit `course`. |
| `indegree[course] += 1` | One more prerequisite for `course`. | |
| `queue = deque(c for ... if indegree[c] == 0)` | Queue of courses with no prerequisites. | These can be taken immediately. |
| `taken = 0` | Counts the courses we manage to take. | Compared with `numCourses` at the end. |
| `current = queue.popleft()` | Takes the next free course. | Any free course is fine; BFS order is just convenient. |
| `taken += 1` | Records it. | |
| `for nxt in graph[current]:` | Looks at each course `current` unlocks. | Only these counters can change. |
| `indegree[nxt] -= 1` | One prerequisite of `nxt` is now done. | |
| `if indegree[nxt] == 0: queue.append(nxt)` | `nxt` has become free. | It reaches 0 exactly once, so it is pushed at most once. |
| `return taken == numCourses` | All courses taken ⇔ no cycle. | Courses on a cycle never reach in-degree 0. |

---

## 8. Dry Run

### Example 1 — `numCourses = 2`, `prerequisites = [[1,0]]`

Setup: `graph = [[1], []]`, `indegree = [0, 1]`, `queue = [0]`.

| Step | Pop | `taken` | Unlocked course | `indegree` after | `queue` after |
|---|---|---|---|---|---|
| 1 | 0 | 1 | 1 → in-degree 1 − 1 = 0, push | `[0, 0]` | `[1]` |
| 2 | 1 | 2 | — (none) | `[0, 0]` | `[]` |

`taken = 2 == numCourses` → **`True`** ✅

### Example 2 — `numCourses = 2`, `prerequisites = [[1,0],[0,1]]`

Setup: `graph = [[1], [0]]`, `indegree = [1, 1]`. No course has in-degree 0, so `queue = []`.

The loop never runs; `taken = 0 != 2` → **`False`** ✅

### A richer example — `numCourses = 4`, `prerequisites = [[1,0],[2,0],[3,1],[3,2]]`

```text
        ┌──► 1 ──┐
    0 ──┤        ├──► 3
        └──► 2 ──┘
```

Setup: `graph = [[1, 2], [3], [3], []]`, `indegree = [0, 1, 1, 2]`, `queue = [0]`.

| Step | Pop | `taken` | Updates | `indegree` after | `queue` after |
|---|---|---|---|---|---|
| 1 | 0 | 1 | 1: 1→0 push; 2: 1→0 push | `[0, 0, 0, 2]` | `[1, 2]` |
| 2 | 1 | 2 | 3: 2→1 | `[0, 0, 0, 1]` | `[2]` |
| 3 | 2 | 3 | 3: 1→0 push | `[0, 0, 0, 0]` | `[3]` |
| 4 | 3 | 4 | — | `[0, 0, 0, 0]` | `[]` |

`taken = 4` → **`True`**; the order taken was `0, 1, 2, 3`.

### DFS-colour version on Example 2

`graph = [[1], [0]]`. `has_cycle(0)`: colour 0 GRAY → neighbour 1 is WHITE → `has_cycle(1)`: colour 1 GRAY → neighbour 0 is **GRAY** → cycle → return `True` all the way up → `canFinish` returns **`False`** ✅

---

## 9. Concepts, Data Structures, and Patterns

- **Directed graph and adjacency list** built from an edge list.
- **In-degree counting** — the core bookkeeping of Kahn's algorithm.
- **Topological sort:** an ordering of a DAG's nodes where every arrow points forward. It exists **if and only if** the graph has no directed cycle.
- **Kahn's algorithm (BFS):** repeatedly remove nodes with in-degree 0.
- **DFS three-colour cycle detection:** a GRAY → GRAY edge is a "back edge", which means a cycle.
- **Queue (`collections.deque`)** for `O(1)` `popleft`.
- **Related problems in this project:**
  - Clone Graph (graph primer, traversal + hash map): [066_clone_graph.md](066_clone_graph.md)
  - Alien Dictionary — a topological sort over letters: [071_alien_dictionary_leetcode_premium.md](071_alien_dictionary_leetcode_premium.md)
  - Graph Valid Tree — cycle detection in an **undirected** graph: [072_graph_valid_tree_leetcode_premium.md](072_graph_valid_tree_leetcode_premium.md)
  - Detect Cycle in a Linked List — cycle detection in the simplest "graph": [../04_linked_list/022_detect_cycle_in_a_linked_list.md](../04_linked_list/022_detect_cycle_in_a_linked_list.md)

---

## 10. Complexity Analysis

`V = numCourses`, `E = len(prerequisites)`.

| Approach | Time | Auxiliary space | Explanation |
|---|---|---|---|
| Brute force (repeated scanning) | `O(V · (V + E))` | `O(V + E)` | Up to `V + 1` rounds, each scanning all courses and their prerequisite lists. |
| Kahn's algorithm (optimized) | `O(V + E)` | `O(V + E)` | Building the graph is `O(V + E)`; each course is popped once and each edge is relaxed once. The adjacency list holds `E` entries; `indegree` and the queue hold up to `V`. |
| DFS three colours | `O(V + E)` | `O(V + E)` | Each node turns GRAY and BLACK once; each edge is examined once. Adjacency list `O(E)`, colours `O(V)`, recursion stack up to `V` deep. |

---

## 11. Edge Cases

| Case | Input | Expected | Why |
|---|---|---|---|
| No prerequisites | `numCourses = 3`, `[]` | `True` | Every course is free from the start. |
| Single course | `numCourses = 1`, `[]` | `True` | Smallest valid input. |
| Self-dependency | `numCourses = 1`, `[[0,0]]` | `False` | Cycle of length 1: in-degree of 0 never reaches 0. |
| Three-course cycle | `3`, `[[1,0],[2,1],[0,2]]` | `False` | `0 → 1 → 2 → 0`. |
| Diamond (shared prerequisite) | `4`, `[[1,0],[2,0],[3,1],[3,2]]` | `True` | Course 3 is reachable twice but there is no cycle — the case that breaks a one-colour DFS. |
| Cycle in one component only | `5`, `[[1,0],[0,1],[3,2],[4,3]]` | `False` | Courses 2, 3, 4 are fine, but 0 and 1 block each other. |
| Long chain | `2000`, `[[1,0],[2,1],…,[1999,1998]]` | `True` | Deepest possible DFS (2000 levels) — why the DFS version raises the recursion limit. |

All of these are in `tools/tests/p067.py`, plus 400 random cases compared against a transitive-closure reference.

---

## 12. Common Mistakes and Debugging

1. **Reversing the pair.** `[a, b]` means "`b` before `a`". Getting the arrow backwards still gives the right True/False for cycle detection (reversing every arrow keeps cycles as cycles), but it gives the **wrong order** in Course Schedule II — build the habit of `graph[b].append(a)` now.
2. **Using a single `visited` set in DFS.** It reports a false cycle on the diamond graph. You need "on current path" (GRAY) separately from "done" (BLACK).
3. **Getting the "finished" colour wrong.** If you forget `color[u] = BLACK`, `u` stays GRAY forever and the diamond graph reports a false cycle. If you instead reset `u` to WHITE (backtracking style), the answer is correct but shared sub-graphs are re-explored again and again — exponential time in the worst case.
4. **Only starting from course 0.** The graph can be disconnected; Kahn's starts from *all* zero-in-degree courses, and the DFS loops over *every* course.
5. **Recursion depth.** A 2000-course chain makes a recursive DFS 2000 calls deep, over CPython's default limit of 1000 → `RecursionError`. Raise the limit or use Kahn's algorithm.
6. **Using `list.pop(0)` as a queue.** It is `O(n)` per pop; use `collections.deque`.

**Debugging tip:** print `indegree` after building the graph and the queue after each pop. If the run ends early, the courses whose in-degree is still above 0 are exactly the ones on or behind a cycle.

---

## 13. Practice Questions

**Q1. For `numCourses = 3`, `prerequisites = [[1,0],[2,1],[1,2]]`, what does Kahn's algorithm return and which courses get taken?**

<details><summary>Hint</summary>Compute the in-degrees first: who starts in the queue?</summary></details>

**Answer:** `graph = [[1], [2], [1]]`, `indegree = [0, 2, 1]`. Only course 0 is free. Taking it lowers course 1 to in-degree 1 — not 0, because course 1 also waits for course 2, and course 2 waits for course 1. The loop stops with `taken = 1`, so the answer is `False`. Course 0 was takeable; courses 1 and 2 form the cycle `1 → 2 → 1`.

**Q2. Why does "every course reached in-degree 0" prove there is no cycle?**

<details><summary>Hint</summary>Think about the first course of a cycle that the algorithm would take.</summary></details>

**Answer:** Suppose a cycle existed and Kahn's algorithm still took every course. Look at the first cycle course that was taken. Its predecessor on the cycle is also a prerequisite, and it had not been taken yet (ours was the first), so our course's in-degree could not have been 0 at that moment — contradiction. Conversely, if there is no cycle, a DAG always has a node with in-degree 0, and removing it leaves another DAG, so the algorithm never gets stuck.

**Q3. Course Schedule II (LeetCode 210): return one valid order, or `[]` if impossible.**

<details><summary>Hint</summary>Kahn's algorithm already pops courses in a valid order — just record them.</summary></details>

**Answer:**

```python
from collections import deque


def find_order(num_courses, prerequisites):
    graph = [[] for _ in range(num_courses)]
    indegree = [0] * num_courses
    for course, pre in prerequisites:
        graph[pre].append(course)
        indegree[course] += 1
    queue = deque(c for c in range(num_courses) if indegree[c] == 0)
    order = []
    while queue:
        cur = queue.popleft()
        order.append(cur)
        for nxt in graph[cur]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
    return order if len(order) == num_courses else []


assert find_order(2, [[1, 0]]) == [0, 1]
assert find_order(4, [[1, 0], [2, 0], [3, 1], [3, 2]]) == [0, 1, 2, 3]
assert find_order(2, [[1, 0], [0, 1]]) == []
```

**Q4. Return the courses that can never be taken (those on a cycle or depending on one), in increasing order.**

<details><summary>Hint</summary>Run Kahn's algorithm and report what is left.</summary></details>

**Answer:**

```python
from collections import deque


def stuck_courses(num_courses, prerequisites):
    graph = [[] for _ in range(num_courses)]
    indegree = [0] * num_courses
    for course, pre in prerequisites:
        graph[pre].append(course)
        indegree[course] += 1
    queue = deque(c for c in range(num_courses) if indegree[c] == 0)
    while queue:
        cur = queue.popleft()
        for nxt in graph[cur]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
    return [c for c in range(num_courses) if indegree[c] > 0]


assert stuck_courses(2, [[1, 0]]) == []
assert stuck_courses(4, [[1, 0], [0, 1], [2, 1]]) == [0, 1, 2]   # 2 depends on the cycle
assert stuck_courses(3, [[1, 2], [2, 1]]) == [1, 2]
```

---

## 14. Revision Summary and Completion Checklist

### Revision card

- **Pattern:** Directed-graph cycle detection / topological sort.
- **Key idea:** `[a, b]` is the arrow `b → a`. Repeatedly take courses with in-degree 0 (Kahn's). All taken ⇔ no cycle. DFS alternative: GRAY → GRAY edge means a cycle.
- **Time:** `O(V + E)`.
- **Auxiliary space:** `O(V + E)`.
- **One-line memory hook:** *"Open boxes with no sticky notes, tear notes off the rest; stuck boxes mean a loop."*

### Completion checklist

- [x] Problem requirements verified against the official statement
- [x] Examples and constraints verified
- [x] Beginner-friendly analogy and logic written
- [x] Brute-force (repeated scanning) solution written and tested
- [x] Optimized Kahn's solution and DFS three-colour alternative written and tested (`tools/tests/p067.py`)
- [x] Line-by-line explanation written
- [x] Dry run completed with both official examples (plus a richer example)
- [x] Complexity verified
- [x] Edge cases listed with expected results
- [x] Practice questions with worked answers added
- [x] Final review completed
