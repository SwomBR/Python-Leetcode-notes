"""Tests for 066 Clone Graph (LeetCode 133)."""
import random


def _build(Node, adj):
    """Build a graph from a 1-indexed adjacency list; return (node 1 or None, all nodes)."""
    if not adj:
        return None, []
    nodes = [Node(i + 1) for i in range(len(adj))]
    for i, nbrs in enumerate(adj):
        nodes[i].neighbors = [nodes[j - 1] for j in nbrs]
    return nodes[0], nodes


def _serialize(start):
    """Return (adjacency list ordered by val, list of node objects) reachable from start."""
    if start is None:
        return [], []
    seen = {id(start)}
    order = [start]
    i = 0
    while i < len(order):
        cur = order[i]
        i += 1
        for nb in cur.neighbors:
            if id(nb) not in seen:
                seen.add(id(nb))
                order.append(nb)
    by_val = {}
    for node in order:
        assert node.val not in by_val, "two distinct node objects share a value"
        by_val[node.val] = [nb.val for nb in node.neighbors]
    n = len(order)
    assert sorted(by_val) == list(range(1, n + 1))
    return [by_val[v] for v in range(1, n + 1)], order


def _run(ns, adj):
    Node = ns["Node"]
    solve = ns["Solution"]().cloneGraph
    start, originals = _build(Node, adj)
    clone = solve(start)
    if not adj:
        assert clone is None
        return
    assert clone is not None and clone is not start
    assert clone.val == 1
    got, clone_nodes = _serialize(clone)
    assert got == [list(x) for x in adj], (adj, got)
    original_ids = {id(x) for x in originals}
    for node in clone_nodes:
        assert id(node) not in original_ids, "clone shares a node with the original"
    # the original graph must be left untouched
    again, _ = _serialize(start)
    assert again == [list(x) for x in adj]


def _random_connected(rng, n):
    edges = set()
    for v in range(2, n + 1):           # random spanning tree keeps it connected
        u = rng.randint(1, v - 1)
        edges.add((u, v))
    for _ in range(rng.randint(0, n * 2)):
        a, b = rng.randint(1, n), rng.randint(1, n)
        if a != b:
            edges.add((min(a, b), max(a, b)))
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a - 1].append(b)
        adj[b - 1].append(a)
    for lst in adj:
        rng.shuffle(lst)
    return adj


def check(ns):
    _run(ns, [[2, 4], [1, 3], [2, 4], [1, 3]])    # Example 1
    _run(ns, [[]])                                # Example 2
    _run(ns, [])                                  # Example 3
    _run(ns, [[2], [1]])                          # two nodes
    _run(ns, [[2, 3], [1, 3], [1, 2]])            # triangle (cycle)
    _run(ns, [[2], [1, 3], [2, 4], [3]])          # path
    _run(ns, [[2, 3, 4, 5], [1], [1], [1], [1]])  # star
    rng = random.Random(66)
    for _ in range(200):
        _run(ns, _random_connected(rng, rng.randint(1, 12)))
    _run(ns, _random_connected(rng, 100))         # maximum size
