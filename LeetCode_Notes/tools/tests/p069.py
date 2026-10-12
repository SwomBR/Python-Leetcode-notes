"""Tests for 069 Number of Islands (LeetCode 200). Grids are deep-copied before each call
because solutions are allowed to mutate (sink) the grid."""
import copy
import random


def _reference(grid):
    """Union-find over land cells (independent of the BFS/DFS solutions)."""
    m, n = len(grid), len(grid[0])
    parent = list(range(m * n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    land = sum(row.count("1") for row in grid)
    unions = 0
    for r in range(m):
        for c in range(n):
            if grid[r][c] != "1":
                continue
            for nr, nc in ((r + 1, c), (r, c + 1)):
                if nr < m and nc < n and grid[nr][nc] == "1":
                    a, b = find(r * n + c), find(nr * n + nc)
                    if a != b:
                        parent[a] = b
                        unions += 1
    return land - unions


def check(ns):
    def solve(g):
        return ns["Solution"]().numIslands(copy.deepcopy(g))

    ex1 = [["1", "1", "1", "1", "0"], ["1", "1", "0", "1", "0"],
           ["1", "1", "0", "0", "0"], ["0", "0", "0", "0", "0"]]
    ex2 = [["1", "1", "0", "0", "0"], ["1", "1", "0", "0", "0"],
           ["0", "0", "1", "0", "0"], ["0", "0", "0", "1", "1"]]
    assert solve(ex1) == 1
    assert solve(ex2) == 3
    assert solve([["0"]]) == 0
    assert solve([["1"]]) == 1
    assert solve([["1", "0", "1", "0", "1"]]) == 3
    assert solve([["1", "0"], ["0", "1"]]) == 2            # diagonal is NOT connected
    assert solve([["1"] * 20 for _ in range(20)]) == 1      # all land (moderate size)
    assert solve([["0"] * 7 for _ in range(5)]) == 0
    assert solve([["1", "1", "1"], ["0", "1", "0"], ["1", "1", "1"]]) == 1
    rng = random.Random(69)
    for _ in range(400):
        m, n = rng.randint(1, 8), rng.randint(1, 8)
        p = rng.random()
        g = [["1" if rng.random() < p else "0" for _ in range(n)] for _ in range(m)]
        assert solve(g) == _reference(g), g
