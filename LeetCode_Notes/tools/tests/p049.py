"""Tests for 049 Validate Binary Search Tree."""
import random
from collections import deque

LO, HI = -2**31, 2**31 - 1


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


def reference(root):
    """Iterative inorder must be strictly increasing."""
    vals, stack, node = [], [], root
    while stack or node:
        while node:
            stack.append(node)
            node = node.left
        node = stack.pop()
        vals.append(node.val)
        node = node.right
    return all(a < b for a, b in zip(vals, vals[1:]))


def random_bst(rng, n, lo, hi, TreeNode):
    """Insert random values; duplicates go right (which makes the tree invalid)."""
    root = None
    nodes = []
    for _ in range(n):
        v = rng.randint(lo, hi)
        new = TreeNode(v)
        nodes.append(new)
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
    return root, nodes


def check(ns):
    TreeNode = ns["TreeNode"]

    def solve(values):
        return ns["Solution"]().isValidBST(build(values, TreeNode))

    # official examples
    assert solve([2, 1, 3]) is True
    assert solve([5, 1, 4, None, None, 3, 6]) is False
    # equal values are not allowed on either side
    assert solve([1, 1]) is False
    assert solve([1, None, 1]) is False
    assert solve([2, 2, 2]) is False
    # the "only compare with direct children" trap
    assert solve([5, 4, 6, None, None, 3, 7]) is False
    assert solve([10, 5, 15, None, None, 6, 20]) is False
    assert solve([3, 1, 5, 0, 4]) is False
    assert solve([3, 1, 5, 0, 2, 4, 6]) is True
    # integer limits
    assert solve([LO]) is True
    assert solve([HI]) is True
    assert solve([LO, None, HI]) is True
    assert solve([HI, LO]) is True
    assert solve([HI, HI]) is False
    assert solve([LO, None, LO]) is False
    assert solve([LO, LO]) is False
    assert solve([0, LO, HI]) is True
    assert solve([0, None, HI, LO]) is False
    rng = random.Random(49)
    for trial in range(500):
        n = rng.randint(1, 30)
        if trial % 3 == 0:
            root, nodes = random_bst(rng, n, LO, HI, TreeNode)
        else:
            root, nodes = random_bst(rng, n, -5, 5, TreeNode)
        if trial % 2 == 0:
            rng.choice(nodes).val = rng.choice([LO, HI, rng.randint(-6, 6)])
        assert ns["Solution"]().isValidBST(root) is reference(root)
    # long valid chain (below CPython's default recursion limit)
    root = TreeNode(0)
    node = root
    for i in range(1, 400):
        node.right = TreeNode(i)
        node = node.right
    assert ns["Solution"]().isValidBST(root) is True
    node.right = TreeNode(5)
    assert ns["Solution"]().isValidBST(root) is False
