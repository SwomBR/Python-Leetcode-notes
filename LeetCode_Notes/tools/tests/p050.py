"""Tests for 050 Kth Smallest Element in a BST."""
import random
from collections import deque


def build(values, TreeNode):
    if not values or values[0] is None:
        return None
    it = iter(values)
    root = TreeNode(next(it))
    queue = deque([root])
    while queue:
        node = queue.popleft()
        for side in ("left", "right"):
            try:
                v = next(it)
            except StopIteration:
                return root
            if v is not None:
                child = TreeNode(v)
                setattr(node, side, child)
                queue.append(child)
    return root


def bst_from(values, TreeNode):
    """Build a BST by inserting values one by one (iteratively)."""
    root = None
    for v in values:
        new = TreeNode(v)
        if root is None:
            root = new
            continue
        cur = root
        while True:
            if v < cur.val:
                if cur.left is None:
                    cur.left = new
                    break
                cur = cur.left
            else:
                if cur.right is None:
                    cur.right = new
                    break
                cur = cur.right
    return root


def check(ns):
    TreeNode = ns["TreeNode"]

    def solve(values, k):
        return ns["Solution"]().kthSmallest(build(values, TreeNode), k)

    # official examples
    assert solve([3, 1, 4, None, 2], 1) == 1
    assert solve([5, 3, 6, 2, 4, None, None, 1], 3) == 3
    # every k on the official trees
    assert [solve([3, 1, 4, None, 2], k) for k in range(1, 5)] == [1, 2, 3, 4]
    assert [solve([5, 3, 6, 2, 4, None, None, 1], k) for k in range(1, 7)] == [1, 2, 3, 4, 5, 6]
    assert solve([0], 1) == 0
    assert solve([10000], 1) == 10000
    assert solve([2, 1], 2) == 2
    assert solve([1, None, 2], 1) == 1
    rng = random.Random(50)
    for _ in range(400):
        n = rng.randint(1, 40)
        values = rng.sample(range(0, 10001), n)
        root = bst_from(values, TreeNode)
        k = rng.randint(1, n)
        assert ns["Solution"]().kthSmallest(root, k) == sorted(values)[k - 1]
    # sorted insertion -> 400-node chains (below CPython's default recursion limit)
    values = list(range(400))
    for order in (values, values[::-1]):
        root = bst_from(order, TreeNode)
        for k in (1, 200, 400):
            assert ns["Solution"]().kthSmallest(root, k) == k - 1
