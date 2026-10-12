"""Tests for 048 Construct Binary Tree from Preorder and Inorder Traversal."""
import random
from collections import deque


def to_list(root):
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


def random_tree(rng, values, TreeNode):
    root = TreeNode(values[0])
    slots = [(root, "left"), (root, "right")]
    for v in values[1:]:
        parent, side = slots.pop(rng.randrange(len(slots)))
        child = TreeNode(v)
        setattr(parent, side, child)
        slots.append((child, "left"))
        slots.append((child, "right"))
    return root


def traversals(root):
    """Iterative preorder and inorder (independent reference)."""
    pre, stack = [], [root]
    while stack:
        node = stack.pop()
        if node:
            pre.append(node.val)
            stack.append(node.right)
            stack.append(node.left)
    ino, stack, node = [], [], root
    while stack or node:
        while node:
            stack.append(node)
            node = node.left
        node = stack.pop()
        ino.append(node.val)
        node = node.right
    return pre, ino


def check(ns):
    TreeNode = ns["TreeNode"]

    def solve(pre, ino):
        return to_list(ns["Solution"]().buildTree(list(pre), list(ino)))

    # official examples
    assert solve([3, 9, 20, 15, 7], [9, 3, 15, 20, 7]) == [3, 9, 20, None, None, 15, 7]
    assert solve([-1], [-1]) == [-1]
    # left-only and right-only chains
    assert solve([1, 2, 3], [3, 2, 1]) == [1, 2, None, 3]
    assert solve([1, 2, 3], [1, 2, 3]) == [1, None, 2, None, 3]
    assert solve([1, 2], [2, 1]) == [1, 2]
    assert solve([1, 2], [1, 2]) == [1, None, 2]
    assert solve([-3000, 3000, 0], [3000, -3000, 0]) == [-3000, 3000, 0]
    rng = random.Random(48)
    for _ in range(400):
        n = rng.randint(1, 40)
        values = rng.sample(range(-3000, 3001), n)
        root = random_tree(rng, values, TreeNode)
        pre, ino = traversals(root)
        assert solve(pre, ino) == to_list(root), (pre, ino)
    # a moderately deep zig-zag tree (below CPython's default recursion limit)
    values = rng.sample(range(-3000, 3001), 300)
    root = TreeNode(values[0])
    node = root
    for i, v in enumerate(values[1:]):
        child = TreeNode(v)
        if i % 2:
            node.left = child
        else:
            node.right = child
        node = child
    pre, ino = traversals(root)
    assert solve(pre, ino) == to_list(root)
    big = random_tree(rng, rng.sample(range(-3000, 3001), 3000), TreeNode)
    pre, ino = traversals(big)
    assert solve(pre, ino) == to_list(big)
