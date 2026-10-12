"""Tests for 044 Binary Tree Maximum Path Sum."""
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


def ref_max_path(values):
    """Independent reference: treat the tree as an undirected graph and sum
    the unique path from every start node to every node (start included)."""
    root = build(values, _N)
    adj, stack, nodes = {root: []}, [root], []
    while stack:
        node = stack.pop()
        nodes.append(node)
        for child in (node.left, node.right):
            if child is not None:
                adj[node].append(child)
                adj[child] = [node]
                stack.append(child)
    best = None
    for start in nodes:
        todo = [(start, None, start.val)]
        while todo:
            node, parent, total = todo.pop()
            best = total if best is None else max(best, total)
            for nxt in adj[node]:
                if nxt is not parent:
                    todo.append((nxt, node, total + nxt.val))
    return best


def check(ns):
    T = ns["TreeNode"]
    solve = lambda vals: ns["Solution"]().maxPathSum(build(vals, T))
    assert solve([1, 2, 3]) == 6
    assert solve([-10, 9, 20, None, None, 15, 7]) == 42
    assert solve([-3]) == -3
    assert solve([-2, -1]) == -1
    assert solve([-1, -2, -3]) == -1
    assert solve([2, -1]) == 2
    assert solve([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1]) == 48
    assert solve([1, -2, 3]) == 4
    rng = random.Random(44)
    for _ in range(300):
        vals = random_tree_list(rng, rng.randint(1, 25), -20, 20)
        assert solve(vals) == ref_max_path(vals), vals
    for _ in range(50):
        vals = random_tree_list(rng, rng.randint(1, 15), -1000, -1)
        assert solve(vals) == max(v for v in vals if v is not None), vals
