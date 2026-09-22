"""Quick sort with a 3-way partition.

Time:  O(n log n) average, O(n^2) worst case (already sorted input with a bad
       pivot, unless you randomize).
Space: O(log n) expected recursion depth. O(n) worst case.
Stable: no. Quick sort swaps across the array, which destroys relative order.

The 3-way (Dutch national flag) partition is the important bit here. A plain
2-way partition degrades to O(n^2) on input with many duplicate keys, which is
extremely common in real data (e.g. sorting records by a boolean or a status
enum). With 3-way, an all-equal array is O(n).

I also randomize the pivot. Median-of-three is the textbook fix for sorted
input, but it still has adversarial inputs. Random pivot makes the worst case
probabilistically impossible, which is good enough.

Iterative on the larger side to bound recursion depth to O(log n): we recurse
into the smaller half and loop on the larger one.
"""

from __future__ import annotations

import random

from collections.abc import MutableSequence
from typing import TypeVar

T = TypeVar("T")


def _partition3(a: MutableSequence[T], lo: int, hi: int) -> tuple[int, int]:
    """3-way partition a[lo:hi] around a random pivot.

    Returns (lt, gt) such that:
        a[lo:lt] < pivot, a[lt:gt] == pivot, a[gt:hi] > pivot
    """
    # hi is exclusive, so the last element is hi - 1.
    pivot_idx = random.randrange(lo, hi)
    pivot = a[pivot_idx]

    lt = lo          # next position for an element < pivot
    i = lo           # current scan position
    gt = hi          # one past the last position for elements > pivot

    while i < gt:
        if a[i] < pivot:
            a[lt], a[i] = a[i], a[lt]
            lt += 1
            i += 1
        elif a[i] > pivot:
            gt -= 1
            a[gt], a[i] = a[i], a[gt]
            # Don't advance i: the element swapped in from gt hasn't been
            # examined yet. This is the line everyone gets wrong.
        else:
            i += 1

    return lt, gt


def quick_sort(items: list[T]) -> list[T]:
    """Return a new sorted list. Does not mutate the input.

    >>> quick_sort([3, 1, 2])
    [1, 2, 3]
    >>> quick_sort([2, 1, 2, 1, 2])
    [1, 1, 2, 2, 2]
    """
    a = list(items)
    if len(a) < 2:
        return a

    # Explicit stack of ranges. Push the larger range, handle the smaller one
    # in the loop, so the stack depth stays O(log n).
    stack: list[tuple[int, int]] = [(0, len(a))]

    while stack:
        lo, hi = stack.pop()
        if hi - lo < 2:
            continue

        lt, gt = _partition3(a, lo, hi)

        # a[lt:gt] is done. Sort the two remaining ranges.
        left_size = lt - lo
        right_size = hi - gt
        if left_size > right_size:
            if left_size > 1:
                stack.append((lo, lt))
            if right_size > 1:
                stack.append((gt, hi))
        else:
            if right_size > 1:
                stack.append((gt, hi))
            if left_size > 1:
                stack.append((lo, lt))

    return a


if __name__ == "__main__":
    print(quick_sort([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]))
    print(quick_sort([5] * 1000)[:3], "len:", len(quick_sort([5] * 1000)))
