"""Tests for 047 Subtree of Another Tree."""
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


def random_tree(rng, n, values, TreeNode):
    root = TreeNode(rng.choice(values))
    nodes = [root]
    slots = [(root, "left"), (root, "right")]
    for _ in range(n - 1):
        parent, side = slots.pop(rng.randrange(len(slots)))
        child = TreeNode(rng.choice(values))
        setattr(parent, side, child)
        nodes.append(child)
        slots.append((child, "left"))
        slots.append((child, "right"))
    return root, nodes


def copy(node, TreeNode):
    if node is None:
        return None
    return TreeNode(node.val, copy(node.left, TreeNode), copy(node.right, TreeNode))


def shape(node):
    """Canonical nested-tuple form; independent reference."""
    if node is None:
        return None
    return (node.val, shape(node.left), shape(node.right))


def reference(root, sub):
    target = shape(sub)
    stack = [root]
    while stack:
        node = stack.pop()
        if node is None:
            continue
        if shape(node) == target:
            return True
        stack.append(node.left)
        stack.append(node.right)
    return False


def check(ns):
    TreeNode = ns["TreeNode"]

    def solve(a, b):
        return ns["Solution"]().isSubtree(build(a, TreeNode), build(b, TreeNode))

    # official examples
    assert solve([3, 4, 5, 1, 2], [4, 1, 2]) is True
    assert solve([3, 4, 5, 1, 2, None, None, None, None, 0], [4, 1, 2]) is False
    # whole tree is a subtree of itself
    assert solve([1, 2, 3], [1, 2, 3]) is True
    assert solve([1], [1]) is True
    assert solve([1], [2]) is False
    # the "2 vs 12" delimiter pitfall
    assert solve([12], [2]) is False
    assert solve([2], [12]) is False
    assert solve([22], [2]) is False
    assert solve([-2], [2]) is False
    assert solve([1, 12], [2]) is False
    assert solve([1, 2], [2]) is True
    assert solve([12, None, 3], [2, None, 3]) is False
    assert solve([1, 23, 4], [3]) is False
    assert solve([1, 2, 3], [2, None, 3]) is False
    # same values, different structure
    assert solve([1, 2], [1, None, 2]) is False
    assert solve([1, None, 1, None, 1], [1, None, 1]) is True
    assert solve([1, 1], [1]) is True
    # subRoot matches the top part of a node, but that node has extra descendants
    assert solve([4, 1, 2, 0], [4, 1, 2]) is False
    # value limits
    assert solve([-10000, 10000], [10000]) is True
    assert solve([10000, -10000], [10000]) is False
    rng = random.Random(47)
    for trial in range(500):
        vals = rng.choice([[1, 2], [1, 2, 12, 21], [-1, 1, -12, 12, 2]])
        root, nodes = random_tree(rng, rng.randint(1, 30), vals, TreeNode)
        if trial % 2 == 0:
            sub = copy(rng.choice(nodes), TreeNode)
        else:
            sub, _ = random_tree(rng, rng.randint(1, 5), vals, TreeNode)
        expected = reference(root, sub)
        assert ns["Solution"]().isSubtree(root, sub) is expected
