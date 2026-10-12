"""Tests for 041 Maximum Depth of Binary Tree."""
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


def ref_depth(values):
    root = build(values, _N)

    def depth(node):
        return 0 if node is None else 1 + max(depth(node.left), depth(node.right))
    return depth(root)


def check(ns):
    T = ns["TreeNode"]
    solve = lambda vals: ns["Solution"]().maxDepth(build(vals, T))
    assert solve([3, 9, 20, None, None, 15, 7]) == 3
    assert solve([1, None, 2]) == 2
    assert solve([]) == 0
    assert solve([0]) == 1
    assert solve([1, 2, None, 3, None, 4]) == 4
    assert solve([1, 2, 3, 4, 5, 6, 7]) == 3
    # right-skewed chain of 500 nodes (kept below Python's default recursion limit)
    chain = [1]
    for _ in range(499):
        chain += [None, 1]
    assert solve(chain) == 500
    rng = random.Random(41)
    for _ in range(300):
        vals = random_tree_list(rng, rng.randint(0, 40), -100, 100)
        assert solve(vals) == ref_depth(vals), vals
