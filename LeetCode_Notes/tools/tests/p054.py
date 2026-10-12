"""Tests for 054 Word Search II (LeetCode 212)."""
import copy
import random


def _exists(board, word):
    """Independent reference: plain DFS for one word using a visited set."""
    rows, cols = len(board), len(board[0])

    def dfs(r, c, k, seen):
        if board[r][c] != word[k]:
            return False
        if k == len(word) - 1:
            return True
        seen.add((r, c))
        found = False
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in seen:
                if dfs(nr, nc, k + 1, seen):
                    found = True
                    break
        seen.discard((r, c))
        return found

    return any(dfs(r, c, 0, set()) for r in range(rows) for c in range(cols))


def _call(solve, board, words):
    result = solve(copy.deepcopy(board), list(words))
    return sorted(result)


def check(ns):
    solve = ns["Solution"]().findWords
    board1 = [["o", "a", "a", "n"], ["e", "t", "a", "e"], ["i", "h", "k", "r"], ["i", "f", "l", "v"]]
    assert _call(solve, board1, ["oath", "pea", "eat", "rain"]) == ["eat", "oath"]
    assert _call(solve, [["a", "b"], ["c", "d"]], ["abcb"]) == []

    assert _call(solve, [["a"]], ["a"]) == ["a"]
    assert _call(solve, [["a"]], ["b", "aa"]) == []
    assert _call(solve, [["a", "a"]], ["aaa", "aa", "a"]) == ["a", "aa"]
    # a word and its prefixes both present
    assert _call(solve, [["a", "b"], ["c", "d"]], ["ab", "abd", "abdc", "abdca"]) == ["ab", "abd", "abdc"]
    # words sharing a prefix, only some present
    assert _call(solve, board1, ["oa", "oat", "oath", "oaths"]) == ["oa", "oat", "oath"]
    # a word that appears in several places is reported once
    assert _call(solve, [["a", "b"], ["b", "a"]], ["ab", "ba"]) == ["ab", "ba"]

    rng = random.Random(54)
    for _ in range(200):
        rows, cols = rng.randint(1, 4), rng.randint(1, 4)
        board = [[rng.choice("abc") for _ in range(cols)] for _ in range(rows)]
        words = sorted({"".join(rng.choice("abc") for _ in range(rng.randint(1, 6)))
                        for _ in range(rng.randint(1, 12))})
        rng.shuffle(words)
        expected = sorted(w for w in words if _exists(board, w))
        assert _call(solve, board, words) == expected, (board, words)
