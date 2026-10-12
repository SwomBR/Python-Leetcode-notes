"""Tests for 042 Same Tree."""
import random
from collections import deque


def build(values, TreeNode):
    """Build a fresh tree from a LeetCode-style level-order list."""
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = deque([root])
    i = 1
    while queue and i < len(values):
        node = queue.popleft()
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1
    return root


def to_list(root):
    """Convert a tree back to a LeetCode-style level-order list."""
    out, queue = [], deque([root])
    while queue:
        node = queue.popleft()
        if node is None:
            out.append(None)
            continue
        out.append(node.val)
        queue.append(node.left)
        queue.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


class _N:
    def __init__(self, val):
        self.val, self.left, self.right = val, None, None


def random_tree_list(rng, n, lo, hi):
    """Random tree shape with n nodes, returned as a level-order list."""
    if n == 0:
        return []
    nodes = [_N(rng.randint(lo, hi))]
    for _ in range(n - 1):
        while True:
            parent = rng.choice(nodes)
            side = rng.choice(("left", "right"))
            if getattr(parent, side) is None:
                child = _N(rng.randint(lo, hi))
                setattr(parent, side, child)
                nodes.append(child)
                break
    return to_list(nodes[0])


def check(ns):
    T = ns["TreeNode"]
    solve = lambda a, b: ns["Solution"]().isSameTree(build(a, T), build(b, T))
    assert solve([1, 2, 3], [1, 2, 3]) is True
    assert solve([1, 2], [1, None, 2]) is False
    assert solve([1, 2, 1], [1, 1, 2]) is False
    assert solve([], []) is True
    assert solve([1], []) is False
    assert solve([], [1]) is False
    assert solve([1], [2]) is False
    assert solve([0], [0]) is True
    assert solve([12, 3], [1, 23]) is False      # trap for naive string joining
    assert solve([1, None, 2, 3], [1, None, 2, None, 3]) is False
    rng = random.Random(42)
    for _ in range(400):
        a = random_tree_list(rng, rng.randint(0, 12), -2, 2)
        mode = rng.randint(0, 2)
        if mode == 0:
            b = list(a)                                   # identical
        elif mode == 1 and a:
            b = list(a)                                   # change one value
            idx = rng.choice([i for i, v in enumerate(b) if v is not None])
            b[idx] = b[idx] + rng.choice((-1, 1))
        else:
            b = random_tree_list(rng, rng.randint(0, 12), -2, 2)
        assert solve(a, b) is (a == b), (a, b)
