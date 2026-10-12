"""Tests for 051 Lowest Common Ancestor of a Binary Search Tree (LeetCode 235)."""
import random


def _build_level_order(ns, values):
    """Build a tree from a LeetCode-style level-order list; return (root, nodes_by_value)."""
    TreeNode = ns["TreeNode"]
    nodes = [None if v is None else TreeNode(v) for v in values]
    by_value = {n.val: n for n in nodes if n is not None}
    kids = nodes[::-1]
    root = kids.pop()
    for node in nodes:
        if node is None:
            continue
        if kids:
            node.left = kids.pop()
        if kids:
            node.right = kids.pop()
    return root, by_value


def _build_bst(ns, insert_order):
    TreeNode = ns["TreeNode"]
    root = None
    by_value = {}
    for v in insert_order:
        node = TreeNode(v)
        by_value[v] = node
        if root is None:
            root = node
            continue
        cur = root
        while True:
            if v < cur.val:
                if cur.left is None:
                    cur.left = node
                    break
                cur = cur.left
            else:
                if cur.right is None:
                    cur.right = node
                    break
                cur = cur.right
    return root, by_value


def _reference_lca(root, p, q):
    """Independent reference: collect p's ancestors via parent pointers, climb from q."""
    parent = {root: None}
    stack = [root]
    while stack:
        node = stack.pop()
        for child in (node.left, node.right):
            if child is not None:
                parent[child] = node
                stack.append(child)
    ancestors = set()
    node = p
    while node is not None:
        ancestors.add(node)
        node = parent[node]
    node = q
    while node not in ancestors:
        node = parent[node]
    return node


def check(ns):
    solve = ns["Solution"]().lowestCommonAncestor
    level = [6, 2, 8, 0, 4, 7, 9, None, None, 3, 5]

    root, nodes = _build_level_order(ns, level)
    assert solve(root, nodes[2], nodes[8]) is nodes[6]
    root, nodes = _build_level_order(ns, level)
    assert solve(root, nodes[2], nodes[4]) is nodes[2]
    root, nodes = _build_level_order(ns, [2, 1])
    assert solve(root, nodes[2], nodes[1]) is nodes[2]

    # extra edge cases on the example-1 tree
    root, nodes = _build_level_order(ns, level)
    assert solve(root, nodes[3], nodes[5]) is nodes[4]
    assert solve(root, nodes[0], nodes[5]) is nodes[2]
    assert solve(root, nodes[7], nodes[9]) is nodes[8]
    assert solve(root, nodes[3], nodes[9]) is nodes[6]
    assert solve(root, nodes[5], nodes[3]) is nodes[4]       # p and q swapped
    assert solve(root, nodes[8], nodes[2]).val == 6
    # two-node tree with a right child
    root, nodes = _build_level_order(ns, [1, None, 2])
    assert solve(root, nodes[1], nodes[2]) is nodes[1]
    # negative and extreme values
    root, nodes = _build_bst(ns, [0, -10**9, 10**9, -5, 5])
    assert solve(root, nodes[-5], nodes[5]) is nodes[0]
    assert solve(root, nodes[-10**9], nodes[-5]) is nodes[-10**9]
    # skewed chain (moderate depth so recursive versions stay within the default limit)
    root, nodes = _build_bst(ns, list(range(300)))
    assert solve(root, nodes[150], nodes[299]) is nodes[150]

    rng = random.Random(51)
    for _ in range(300):
        size = rng.randint(2, 40)
        values = rng.sample(range(-100, 101), size)
        root, nodes = _build_bst(ns, values)
        p_val, q_val = rng.sample(values, 2)
        expected = _reference_lca(root, nodes[p_val], nodes[q_val])
        got = solve(root, nodes[p_val], nodes[q_val])
        assert got is expected, (values, p_val, q_val)
