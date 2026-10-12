"""Tests for 030 Word Search."""
import copy
import random


def _reference(board, word):
    # Independent method: iterative DFS carrying the set of used cells explicitly.
    m, n = len(board), len(board[0])
    for r in range(m):
        for c in range(n):
            if board[r][c] != word[0]:
                continue
            stack = [(r, c, 0, frozenset([(r, c)]))]
            while stack:
                i, j, k, used = stack.pop()
                if k == len(word) - 1:
                    return True
                for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    a, b = i + di, j + dj
                    if (0 <= a < m and 0 <= b < n and (a, b) not in used
                            and board[a][b] == word[k + 1]):
                        stack.append((a, b, k + 1, used | {(a, b)}))
    return False


def _run(ns, board, word):
    grid = copy.deepcopy(board)
    result = ns["Solution"]().exist(grid, word)
    assert grid == board, "board must be restored after the search"
    return result


def check(ns):
    board = [["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]]
    assert _run(ns, board, "ABCCED") is True
    assert _run(ns, board, "SEE") is True
    assert _run(ns, board, "ABCB") is False
    assert _run(ns, board, "ABCESEEDASFC") is True
    assert _run(ns, [["a"]], "a") is True
    assert _run(ns, [["a"]], "b") is False
    assert _run(ns, [["a"]], "aa") is False
    assert _run(ns, [["a", "a"]], "aaa") is False
    assert _run(ns, [["a", "b"], ["c", "d"]], "abdc") is True
    assert _run(ns, [["a", "b"], ["c", "d"]], "abcd") is False
    assert _run(ns, [["A", "a"]], "AA") is False
    assert _run(ns, [["a"] * 4 for _ in range(4)], "a" * 9 + "b") is False
    assert _run(ns, [["a"] * 4 for _ in range(4)], "b" + "a" * 9) is False
    assert _run(ns, [["a"] * 4 for _ in range(4)], "a" * 16) is True
    assert _run(ns, [["a"] * 2 for _ in range(2)], "a" * 5) is False
    assert _run(ns, [["a", "b"], ["b", "a"]], "abab") is True
    rng = random.Random(30)
    for _ in range(400):
        m, n = rng.randint(1, 4), rng.randint(1, 4)
        letters = rng.choice(["ab", "abc", "aB"])
        board = [[rng.choice(letters) for _ in range(n)] for _ in range(m)]
        if rng.random() < 0.5:
            # Build the word from a real path so many cases are True.
            r, c = rng.randrange(m), rng.randrange(n)
            used = {(r, c)}
            word = board[r][c]
            for _ in range(rng.randint(0, 6)):
                options = [(r + a, c + b) for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))
                           if 0 <= r + a < m and 0 <= c + b < n and (r + a, c + b) not in used]
                if not options:
                    break
                r, c = rng.choice(options)
                used.add((r, c))
                word += board[r][c]
        else:
            word = "".join(rng.choice(letters) for _ in range(rng.randint(1, 7)))
        assert _run(ns, board, word) == _reference(board, word), (board, word)
