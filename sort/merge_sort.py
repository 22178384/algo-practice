"""Merge sort.

Time:  O(n log n) in all cases (best, average, worst).
Space: O(n) auxiliary for the merged output.
Stable: yes — equal elements keep their relative order, because when merging we
        take from the left run on ties (`<=`).

Why it's worth knowing: it's the one comparison sort with a guaranteed n log n
worst case *and* stability. Python's `sorted()` uses Timsort, which is a
merge-sort variant, for exactly these reasons.

The classic mistake is allocating a new list at every merge. That's still
O(n log n) but with a much worse constant. The version below merges into a
single reusable buffer and copies back, which is what you'd write if you cared.
"""

from __future__ import annotations

from collections.abc import MutableSequence
from typing import TypeVar

T = TypeVar("T")

# Below this size, insertion sort beats the merge overhead. 16 is a common
# cutoff (Timsort uses 32-64). Set to 0 to always recurse.
INSERTION_CUTOFF = 16


def _insertion_sort(a: MutableSequence[T], lo: int, hi: int) -> None:
    """Sort a[lo:hi] in place. Stable, O(k^2) for k = hi - lo."""
    for i in range(lo + 1, hi):
        key = a[i]
        j = i - 1
        while j >= lo and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key


def merge_sort(items: list[T]) -> list[T]:
    """Return a new sorted list. Does not mutate the input.

    >>> merge_sort([3, 1, 2])
    [1, 2, 3]
    """
    a = list(items)          # copy so the caller's list is untouched
    n = len(a)
    if n < 2:
        return a

    buf = [None] * n         # single scratch buffer, reused at every level

    def _sort(lo: int, hi: int) -> None:
        if hi - lo <= INSERTION_CUTOFF:
            _insertion_sort(a, lo, hi)
            return
        mid = (lo + hi) // 2
        _sort(lo, mid)
        _sort(mid, hi)
        # Already ordered? Skip the merge. This makes nearly-sorted input O(n).
        if a[mid - 1] <= a[mid]:
            return
        _merge(lo, mid, hi)

    def _merge(lo: int, mid: int, hi: int) -> None:
        buf[lo:hi] = a[lo:hi]
        i, j, k = lo, mid, lo
        while i < mid and j < hi:
            # <= keeps it stable.
            if buf[i] <= buf[j]:
                a[k] = buf[i]
                i += 1
            else:
                a[k] = buf[j]
                j += 1
            k += 1
        # Only the left run can have leftovers; the right run is already in
        # place at the tail of a[lo:hi] when i reaches mid.
        if i < mid:
            a[k:hi] = buf[i:mid]

    _sort(0, n)
    return a


if __name__ == "__main__":
    import random

    data = [random.randint(0, 100) for _ in range(20)]
    original = list(data)
    result = merge_sort(data)
    print("before:", data)
    print("after: ", result)
    print("sorted correctly:", result == sorted(original))
    print("input untouched:", data == original)
