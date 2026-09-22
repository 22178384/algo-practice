"""Heap sort.

Time:  O(n log n) in all cases.
Space: O(1) — sorts in place, no auxiliary array.
Stable: no. The sift-down swaps long-distance elements.

The two things worth remembering:

1. Build-heap is O(n), not O(n log n), even though it looks like it should be.
   The number of sift-down steps is bounded by sum of heights, which converges
   to 2n. This is a favorite interview question.

2. Heap sort has terrible cache behavior compared to quick sort. It jumps
   around the array, so despite the same big-O it's usually 2-3x slower in
   practice. Use it when you need a hard O(n log n) worst case *and* O(1) space;
   otherwise `sorted()` is better.

Indices use the 0-based convention: children of i are 2i+1 and 2i+2, parent is
(i-1)//2. Mixing up 0-based and 1-based is the usual source of off-by-one bugs.
"""

from __future__ import annotations

from collections.abc import MutableSequence
from typing import TypeVar

T = TypeVar("T")


def _sift_down(a: MutableSequence[T], start: int, end: int) -> None:
    """Restore the max-heap property in a[start:end].

    Assumes both subtrees of `start` are already heaps. `end` is exclusive.
    """
    root = start
    while True:
        child = 2 * root + 1
        if child >= end:
            return
        # Pick the larger child. Check `child + 1 < end` first so we don't read
        # past the heap when there's only a left child.
        if child + 1 < end and a[child] < a[child + 1]:
            child += 1
        if a[root] < a[child]:
            a[root], a[child] = a[child], a[root]
            root = child
        else:
            return  # heap property restored, we can stop early


def heap_sort(items: list[T]) -> list[T]:
    """Return a new sorted list. Does not mutate the input.

    >>> heap_sort([3, 1, 2])
    [1, 2, 3]
    """
    a = list(items)
    n = len(a)
    if n < 2:
        return a

    # Phase 1: build a max-heap bottom-up. Start from the last non-leaf node
    # (n // 2 - 1) and sift down toward the root. Leaves are trivially heaps.
    for i in range(n // 2 - 1, -1, -1):
        _sift_down(a, i, n)

    # Phase 2: repeatedly swap the max (index 0) to the end and shrink the heap.
    for end in range(n - 1, 0, -1):
        a[0], a[end] = a[end], a[0]
        _sift_down(a, 0, end)

    return a


if __name__ == "__main__":
    print(heap_sort([3, 1, 4, 1, 5, 9, 2, 6]))
    import random

    data = [random.randint(0, 50) for _ in range(15)]
    assert heap_sort(data) == sorted(data)
    print("ok:", heap_sort(data))
