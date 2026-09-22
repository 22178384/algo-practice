"""One test file for everything. Run from the repo root: pytest -q

The sorts get checked against Python's own `sorted()` on random input, which is
a much stronger test than any hand-written expected output. The rest get
hand-picked cases plus the edge cases that actually break them.
"""

from __future__ import annotations

import random

import pytest

from dp.coin_change import count_ways, min_coins, min_coins_with_path
from dp.lis import lis_dp, lis_len
from graph.bfs import bfs_distances, bfs_shortest_path
from graph.dijkstra import dijkstra, shortest_path
from sort.heap_sort import heap_sort
from sort.merge_sort import merge_sort
from sort.quick_sort import quick_sort
from string.kmp import find_first, kmp_search, prefix_function
from tree.lca import TreeNode, lca_binary_tree, lca_bst

ALL_SORTS = [merge_sort, quick_sort, heap_sort]

FIXED_CASES = [
    [],
    [1],
    [2, 1],
    [1, 1, 1],
    [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5],
    list(range(50)),                 # already sorted
    list(range(50, 0, -1)),          # reverse sorted
    [0, 0, 1, -1, 0, -1],            # duplicates + negatives
]


# --------------------------------------------------------------------------- #
# sorts
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("sort_fn", ALL_SORTS, ids=lambda f: f.__name__)
@pytest.mark.parametrize("data", FIXED_CASES, ids=lambda d: f"n={len(d)}")
def test_sort_fixed_cases(sort_fn, data):
    assert sort_fn(data) == sorted(data)


@pytest.mark.parametrize("sort_fn", ALL_SORTS, ids=lambda f: f.__name__)
def test_sort_random_matches_builtin(sort_fn):
    rng = random.Random(1234)
    for _ in range(20):
        data = [rng.randint(-100, 100) for _ in range(rng.randint(0, 200))]
        assert sort_fn(data) == sorted(data)


@pytest.mark.parametrize("sort_fn", ALL_SORTS, ids=lambda f: f.__name__)
def test_sort_does_not_mutate_input(sort_fn):
    data = [3, 1, 2]
    original = list(data)
    sort_fn(data)
    assert data == original


def test_quick_sort_handles_many_duplicates():
    # The whole reason for the 3-way partition. A 2-way version would be O(n^2)
    # here; we can't time it, but we can at least assert correctness.
    data = [7] * 500 + [1] * 500 + [7] * 500
    assert quick_sort(data) == sorted(data)


def test_merge_sort_is_stable():
    # (key, tag) pairs; equal keys must keep their original relative order.
    data = [(1, "a"), (0, "b"), (1, "c"), (0, "d"), (1, "e")]
    result = merge_sort(data)
    assert [tag for _, tag in result] == ["b", "d", "a", "c", "e"]


# --------------------------------------------------------------------------- #
# coin change
# --------------------------------------------------------------------------- #
def test_min_coins_basic():
    assert min_coins([1, 2, 5], 11) == 3
    assert min_coins([1, 2, 5], 0) == 0
    assert min_coins([2], 3) == -1
    assert min_coins([], 5) == -1
    assert min_coins([5], 5) == 1


def test_min_coins_negative_amount_rejected():
    with pytest.raises(ValueError):
        min_coins([1], -1)


def test_min_coins_with_path():
    path = min_coins_with_path([1, 2, 5], 11)
    assert path is not None
    assert sum(path) == 11
    assert len(path) == min_coins([1, 2, 5], 11)
    assert min_coins_with_path([2], 3) is None
    assert min_coins_with_path([1], 0) == []


def test_count_ways_counts_combinations_not_permutations():
    # [1,2] must count once, not as [1,2] and [2,1].
    assert count_ways([1, 2, 5], 5) == 4
    assert count_ways([2], 3) == 0
    assert count_ways([1], 0) == 1
    assert count_ways([1, 2], 3) == 2      # 1+1+1, 1+2


# --------------------------------------------------------------------------- #
# LIS
# --------------------------------------------------------------------------- #
def test_lis_len_basic():
    assert lis_len([10, 9, 2, 5, 3, 7, 101, 18]) == 4
    assert lis_len([]) == 0
    assert lis_len([5, 4, 3, 2]) == 1
    assert lis_len([1, 2, 3, 4]) == 4
    assert lis_len([2, 2, 2]) == 1          # strictly increasing


def test_lis_dp_returns_valid_increasing_subsequence():
    data = [10, 9, 2, 5, 3, 7, 101, 18]
    result = lis_dp(data)
    assert result == sorted(result)
    assert len(set(result)) == len(result)   # strictly increasing
    assert len(result) == lis_len(data)


@pytest.mark.parametrize("data", FIXED_CASES)
def test_lis_versions_agree(data):
    # The two implementations must agree on length for every case.
    assert len(lis_dp(data)) == lis_len(data)


# --------------------------------------------------------------------------- #
# BFS
# --------------------------------------------------------------------------- #
GRAPH = {
    "you": ["alice", "bob", "claire"],
    "bob": ["anuj", "peggy"],
    "alice": ["peggy"],
    "claire": ["thom", "jonny"],
    "anuj": [],
    "peggy": [],
    "thom": [],
    "jonny": [],
}


def test_bfs_path():
    assert bfs_shortest_path(GRAPH, "you", "thom") == ["you", "claire", "thom"]
    assert bfs_shortest_path(GRAPH, "you", "peggy") == ["you", "alice", "peggy"]
    assert bfs_shortest_path(GRAPH, "you", "nobody") is None


def test_bfs_start_equals_goal():
    assert bfs_shortest_path(GRAPH, "you", "you") == ["you"]


def test_bfs_path_is_actually_shortest():
    path = bfs_shortest_path(GRAPH, "you", "jonny")
    assert path == ["you", "claire", "jonny"]
    assert len(path) - 1 == bfs_distances(GRAPH, "you")["jonny"]


def test_bfs_distances():
    dist = bfs_distances(GRAPH, "you")
    assert dist["you"] == 0
    assert dist["claire"] == 1
    assert dist["thom"] == 2
    assert "nobody" not in dist


def test_bfs_handles_cycle():
    # a <-> b with a self-loop on c; must terminate.
    g = {"a": ["b", "c"], "b": ["a"], "c": ["c"]}
    assert bfs_shortest_path(g, "a", "c") == ["a", "c"]
    assert bfs_distances(g, "a") == {"a": 0, "b": 1, "c": 1}


# --------------------------------------------------------------------------- #
# Dijkstra
# --------------------------------------------------------------------------- #
WEIGHTED = {
    "a": [("b", 1), ("c", 4)],
    "b": [("c", 2), ("d", 5)],
    "c": [("d", 1)],
    "d": [],
}


def test_dijkstra_distances():
    dist, _ = dijkstra(WEIGHTED, "a")
    assert dist["a"] == 0
    assert dist["b"] == 1
    assert dist["c"] == 3        # a->b->c beats a->c (4)
    assert dist["d"] == 4        # a->b->c->d beats a->b->d (6)


def test_dijkstra_path():
    assert shortest_path(WEIGHTED, "a", "d") == ["a", "b", "c", "d"]
    assert shortest_path(WEIGHTED, "a", "a") == ["a"]
    assert shortest_path(WEIGHTED, "d", "a") is None   # directed, no way back


def test_dijkstra_unreachable_node_absent():
    g = {"a": [("b", 1)], "b": [], "island": [("x", 1)]}
    dist, _ = dijkstra(g, "a")
    assert "island" not in dist


def test_dijkstra_rejects_negative_weights():
    with pytest.raises(ValueError, match="negative edge"):
        dijkstra({"x": [("y", -1)], "y": []}, "x")


def test_dijkstra_stale_heap_entry_is_skipped():
    # Two routes to "c": a direct expensive one and a cheap one through b.
    # The heap will contain both; the stale entry must not corrupt the result.
    g = {"a": [("c", 10), ("b", 1)], "b": [("c", 1)], "c": []}
    dist, _ = dijkstra(g, "a")
    assert dist["c"] == 2


# --------------------------------------------------------------------------- #
# LCA
# --------------------------------------------------------------------------- #
def build_tree():
    #         3
    #       /   \
    #      5     1
    #     / \   / \
    #    6   2 0   8
    #       / \
    #      7   4
    return TreeNode(
        3,
        TreeNode(5, TreeNode(6), TreeNode(2, TreeNode(7), TreeNode(4))),
        TreeNode(1, TreeNode(0), TreeNode(8)),
    )


def test_lca_binary_tree():
    t = build_tree()
    assert lca_binary_tree(t, t.left, t.right).val == 3
    assert lca_binary_tree(t, t.left.left, t.left.right.right).val == 5
    assert lca_binary_tree(t, t.left.right.left, t.left.right.right).val == 2
    # A node is its own ancestor.
    assert lca_binary_tree(t, t.left, t.left.right.left).val == 5


def test_lca_bst():
    #         6
    #       /   \
    #      2     8
    #     / \   / \
    #    0   4 7   9
    #       / \
    #      3   5
    bst = TreeNode(
        6,
        TreeNode(2, TreeNode(0), TreeNode(4, TreeNode(3), TreeNode(5))),
        TreeNode(8, TreeNode(7), TreeNode(9)),
    )
    assert lca_bst(bst, bst.left, bst.right).val == 6
    assert lca_bst(bst, bst.left.right.left, bst.left.right.right).val == 4
    assert lca_bst(bst, bst.left.left, bst.left).val == 2


# --------------------------------------------------------------------------- #
# KMP
# --------------------------------------------------------------------------- #
def test_prefix_function():
    assert prefix_function("aabaa") == [0, 1, 0, 1, 2]
    assert prefix_function("abc") == [0, 0, 0]
    assert prefix_function("") == []
    assert prefix_function("a") == [0]
    assert prefix_function("aaaa") == [0, 1, 2, 3]


def test_kmp_search_basic():
    assert kmp_search("ababcababd", "ababd") == [5]
    assert kmp_search("hello world", "world") == [6]
    assert kmp_search("abc", "xyz") == []
    assert kmp_search("abc", "") == []


def test_kmp_finds_overlapping_matches():
    assert kmp_search("aaaa", "aa") == [0, 1, 2]
    assert kmp_search("abababa", "aba") == [0, 2, 4]


def test_kmp_matches_naive_search():
    rng = random.Random(99)
    alphabet = "ab"
    for _ in range(30):
        text = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 40)))
        pat = "".join(rng.choice(alphabet) for _ in range(rng.randint(1, 5)))
        expected = [i for i in range(len(text) - len(pat) + 1)
                    if text[i:i + len(pat)] == pat]
        assert kmp_search(text, pat) == expected, (text, pat)


def test_find_first():
    assert find_first("a needle in a haystack", "needle") == 2
    assert find_first("abc", "zzz") == -1
