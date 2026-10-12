"""Tests for 043 Invert Binary Tree."""
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


def ref_invert(values):
    root = build(values, _N)

    def mirror(node):
        if node is not None:
            node.left, node.right = mirror(node.right), mirror(node.left)
        return node
    return to_list(mirror(root))


def check(ns):
    T = ns["TreeNode"]
    solve = lambda vals: to_list(ns["Solution"]().invertTree(build(vals, T)))
    assert solve([4, 2, 7, 1, 3, 6, 9]) == [4, 7, 2, 9, 6, 3, 1]
    assert solve([2, 1, 3]) == [2, 3, 1]
    assert solve([]) == []
    assert ns["Solution"]().invertTree(None) is None
    assert solve([1]) == [1]
    assert solve([1, 2]) == [1, None, 2]
    assert solve([1, None, 2, None, 3]) == [1, 2, None, 3]
    # inverting twice gives back the original tree
    vals = [5, 3, 8, 1, None, 7, 9, None, 2]
    sol = ns["Solution"]()
    assert to_list(sol.invertTree(sol.invertTree(build(vals, T)))) == vals
    # LeetCode compares the returned tree; in-place or a fresh copy both pass
    root = build([4, 2, 7], T)
    assert to_list(sol.invertTree(root)) == [4, 7, 2]
    rng = random.Random(43)
    for _ in range(300):
        vals = random_tree_list(rng, rng.randint(0, 40), -100, 100)
        assert solve(vals) == ref_invert(vals), vals
