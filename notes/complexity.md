# Complexity cheatsheet

The table, then the parts I actually got wrong for years.

## Sorts

| Algorithm  | Best       | Average    | Worst      | Space    | Stable |
|------------|------------|------------|------------|----------|--------|
| merge sort | O(n log n) | O(n log n) | O(n log n) | O(n)     | yes    |
| quick sort | O(n log n) | O(n log n) | O(n^2)     | O(log n) | no     |
| heap sort  | O(n log n) | O(n log n) | O(n log n) | O(1)     | no     |
| insertion  | O(n)       | O(n^2)     | O(n^2)     | O(1)     | yes    |
| Python's `sorted` (Timsort) | O(n) | O(n log n) | O(n log n) | O(n) | yes |

Notes:

- Quick sort's O(n^2) worst case comes from picking a bad pivot (e.g. first
  element on sorted input). Random pivot or median-of-three makes it
  probabilistically O(n log n).
- Quick sort's O(log n) space is the recursion stack. If you always recurse into
  the larger side you get O(n) stack depth; recurse into the smaller side and
  loop on the larger one instead.
- Heap sort has the best worst-case guarantees but the worst constants of the
  three, because it jumps around memory and kills the cache. In practice it's
  usually slower than quick sort despite identical big-O.
- Timsort is a merge sort that detects existing runs, so nearly-sorted data is
  close to O(n). It's also stable.

## Graph

| Algorithm   | Time              | Space | Use when |
|-------------|-------------------|-------|----------|
| BFS         | O(V + E)          | O(V)  | unweighted shortest path |
| DFS         | O(V + E)          | O(V)  | connectivity, cycles, topo sort |
| Dijkstra    | O((V + E) log V)  | O(V)  | non-negative weights |
| Bellman-Ford| O(V * E)          | O(V)  | negative weights, or detect negative cycles |

The `log V` in Dijkstra is the heap. The naive version is O(V^2), which is
actually better for dense graphs (E close to V^2). Python's `heapq` gives you the
log V version, which is right for sparse graphs.

**Dijkstra with a negative edge is silently wrong.** It doesn't raise, it just
returns distances that are too large. Bellman-Ford is the fix, or Johnson's if
you need all pairs.

## Dynamic programming

| Problem      | Time          | Space | Notes |
|--------------|---------------|-------|-------|
| coin change (min)  | O(amount * k) | O(amount) | k = number of coin types |
| coin change (count)| O(amount * k) | O(amount) | loops must be ordered coin-outer |
| LIS (DP)     | O(n^2)        | O(n)  | easy to reconstruct the answer |
| LIS (patience)| O(n log n)   | O(n)  | length is easy, reconstruction needs a parent array |
| edit distance| O(n * m)      | O(min(n,m)) | can roll the 2D table down to one row |

## Things I got wrong for a while

**1. Build-heap is O(n), not O(n log n).**

It looks like n sift-downs of O(log n) each. But most nodes are near the bottom
and sift down only a little. The sum of heights over all nodes is ~2n, so
build-heap is linear. Heap sort is still O(n log n) because of the n extraction
steps.

**2. Hash map lookup is O(1) *amortized*, and only on average.**

Worst case is O(n) when everything collides. Python dicts also resize, which is
an occasional O(n) operation spread across insertions. This is why people say
"amortized" — it's not a lie, it's just not the whole story. Adversarial input
can still degrade a dict, which is why some languages randomize hash seeds.

**3. BFS on a weighted graph is not "shortest path".**

It's fewest *edges*. On a graph where every edge costs the same, that's the same
thing. Otherwise it's not. People write BFS, test on a graph where all weights
are 1, ship it, and then get a bug report.

**4. Space complexity of quick sort is not O(1).**

It sorts in place, but the recursion uses stack. The usual answer is O(log n)
expected, O(n) worst case. Saying O(1) is a common interview mistake.

**5. `list.pop(0)` is O(n), `deque.popleft()` is O(1).**

Using a list as a queue makes BFS O(V^2) instead of O(V + E). This is the single
most common way to accidentally wreck a BFS.

**6. Amortized vs average are different words.**

Amortized: worst-case total over a sequence of operations, divided by the number
of operations. Guaranteed. Example: dynamic array append.
Average: expected cost given a distribution of inputs. Not guaranteed.
Example: hash table lookup.
Interviewers notice when you use these interchangeably.

**7. `sorted()` on a list of tuples sorts lexicographically.**

`[(1, 'b'), (1, 'a')]` sorts to `[(1, 'a'), (1, 'b')]`. Handy for tie-breaking
without a key function. Also: `sorted` is stable, so if you sort by a secondary
key first and then by the primary key, ties keep the secondary order. That's the
"decorate-sort-undecorate" trick without the decorating.

## Reading complexity off the code

- One loop over n: O(n).
- Loop over n with a loop over n inside: O(n^2). Unless the inner loop is
  bounded by something independent of n.
- Halving the input each step: O(log n).
- Recursion that splits into 2 halves and does O(n) work to combine: O(n log n).
- Recursion with two branches of size n-1: O(2^n). This is why naive Fibonacci
  is exponential.
- Sorting inside a loop over n: O(n^2 log n).

## Not everything is about big-O

Big-O hides constants and cache behavior. `heap_sort` and `merge_sort` are both
O(n log n); on real data merge sort is usually much faster because it reads
memory sequentially. A hash map with a bad hash function can lose to a sorted
array with binary search for small n. When n is under ~50, insertion sort beats
everything, which is why real libraries switch to it below a threshold.
