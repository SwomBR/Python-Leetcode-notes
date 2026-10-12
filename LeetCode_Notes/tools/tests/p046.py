"""Tests for 046 Serialize and Deserialize Binary Tree (design: class Codec)."""
import random
from collections import deque

TARGET = "Codec"


def build(values, TreeNode):
    """Build a tree from a LeetCode-style level-order list."""
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


def to_list(root):
    """Level-order list with trailing Nones removed (LeetCode output format)."""
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


def same(a, b):
    """Iterative structural equality check."""
    stack = [(a, b)]
    while stack:
        x, y = stack.pop()
        if x is None and y is None:
            continue
        if x is None or y is None or x.val != y.val:
            return False
        stack.append((x.left, y.left))
        stack.append((x.right, y.right))
    return True


def random_tree(rng, n, lo, hi, TreeNode):
    if n == 0:
        return None
    root = TreeNode(rng.randint(lo, hi))
    slots = [(root, "left"), (root, "right")]
    for _ in range(n - 1):
        parent, side = slots.pop(rng.randrange(len(slots)))
        child = TreeNode(rng.randint(lo, hi))
        setattr(parent, side, child)
        slots.append((child, "left"))
        slots.append((child, "right"))
    return root


def roundtrip(ns, root):
    # LeetCode uses two separate objects: ser = Codec(); deser = Codec()
    ser, deser = ns["Codec"](), ns["Codec"]()
    data = ser.serialize(root)
    assert isinstance(data, str), type(data)
    return deser.deserialize(data)


def check(ns):
    TreeNode = ns["TreeNode"]
    examples = [
        [1, 2, 3, None, None, 4, 5],   # official example 1
        [],                            # official example 2
        [1],
        [-1000],
        [1000, -1000, None, 12, None, -1],
        [1, None, 2, None, 3, None, 4],
        [1, 2, None, 3, None, 4],
        [0, 0, 0, None, 0, 0],
        [-1, -12, 12, -2, 2, None, None, 21],
    ]
    for values in examples:
        root = build(values, TreeNode)
        result = roundtrip(ns, root)
        assert to_list(result) == values, (values, to_list(result))
        assert same(result, root), values
    assert roundtrip(ns, None) is None
    # a moderately deep chain (kept below CPython's default recursion limit)
    chain = TreeNode(0)
    node = chain
    for i in range(1, 400):
        node.right = TreeNode(-i if i % 2 else i)
        node = node.right
    assert same(roundtrip(ns, chain), chain)
    rng = random.Random(46)
    for _ in range(400):
        root = random_tree(rng, rng.randint(0, 40), -1000, 1000, TreeNode)
        before = to_list(root)
        result = roundtrip(ns, root)
        assert same(result, root), before
        assert to_list(root) == before  # original tree untouched
    big = random_tree(rng, 3000, -1000, 1000, TreeNode)
    assert same(roundtrip(ns, big), big)
