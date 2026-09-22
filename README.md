# algo-practice

Implementations of the algorithms I keep forgetting. I write them out from
scratch every so often so I can reason about the edge cases, then run the test
suite to make sure I haven't gotten sloppy.

These are not optimized for production. They're optimized for being readable and
correct. If you need a sort, use `sorted()`. This repo exists so I can explain
why `sorted()` is fine.

## What's here

```
sort/     merge_sort, quick_sort, heap_sort
dp/       coin_change (min coins + ways), lis (O(n^2) and O(n log n))
graph/    bfs (shortest path in unweighted), dijkstra (weighted)
tree/     lca (binary tree + BST)
string/   kmp (prefix function + substring search)
tests/    pytest suite covering all of the above
notes/    complexity cheatsheet and the bits I always get wrong
```

## Running the tests

```bash
pip install pytest
pytest -q
```

The tests import modules by their path (`from sort.merge_sort import merge_sort`),
so run pytest from the repo root. There's a `conftest.py` there to put the root
on `sys.path` — without it, `import string.kmp` would pick up the *stdlib*
`string` module instead, which took me a while to figure out.

## What each file gives you

- `sort/merge_sort.py` — stable, O(n log n) guaranteed, O(n) extra space.
- `sort/quick_sort.py` — in-place, 3-way partition so duplicate-heavy input
  doesn't degrade to O(n^2).
- `sort/heap_sort.py` — in-place, O(n log n) worst case, not stable.
- `dp/coin_change.py` — both "fewest coins" and "number of ways". Different
  base cases, easy to mix up.
- `dp/lis.py` — longest increasing subsequence, the O(n log n) patience version
  and the O(n^2) DP version for comparison.
- `graph/bfs.py` — shortest path in an unweighted graph, with path
  reconstruction.
- `graph/dijkstra.py` — weighted shortest paths with a binary heap. No negative
  edges; it silently gives wrong answers if you feed it one.
- `tree/lca.py` — lowest common ancestor for a plain binary tree (recursive) and
  a BST (iterative, O(h)).
- `string/kmp.py` — KMP. The failure function is the part everyone gets wrong.

## Gotchas

- **Dijkstra with a negative edge is silently wrong.** It doesn't raise. I
  mention it in the docstring because I've seen people ship it.
- **`heapq` is a min-heap.** For a max-heap you push negated values, which I do
  in `heap_sort.py` by using a custom comparison instead — cleaner than
  sprinkling minus signs.
- **`lca` for a plain binary tree assumes nodes are unique.** Duplicate values
  break the equality check. Real interview questions usually guarantee
  uniqueness; real data doesn't.
- **Python recursion limit.** `merge_sort` and the tree functions recurse. On a
  degenerate tree (a linked list) with >1000 nodes you'll hit
  `RecursionError`. Raise the limit or convert to iterative; I left the
  recursive versions because they're the ones you're asked to write on a
  whiteboard.

## Notes

`notes/complexity.md` has the table and the "why" behind each bound, including
the ones I had wrong for years. Start there if you're reviewing.

MIT. See LICENSE.
