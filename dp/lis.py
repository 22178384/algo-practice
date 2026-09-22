"""Longest increasing subsequence (strictly increasing).

Two versions, because they're both worth knowing:

- lis_dp:  O(n^2) time, O(n) space. Easy to reason about, easy to reconstruct
           the actual subsequence.
- lis_len: O(n log n) time, O(n) space. The "patience sorting" trick. Gives you
           the *length* easily but reconstructing the subsequence needs extra
           bookkeeping, which I've added below.

"Subsequence" means you can skip elements but not reorder them. This is not the
same as "longest increasing subarray" (contiguous), which is a different and
much easier problem. People mix those up constantly.

The O(n log n) version: keep `tails`, where tails[i] is the smallest possible
tail of an increasing subsequence of length i+1. `tails` is always sorted, so we
binary search. The length of `tails` at the end is the answer. The subtlety is
that `tails` is NOT itself a valid subsequence in general — only its length is
meaningful. That trips people up when they try to print it.
"""

from __future__ import annotations

import bisect


def lis_len(seq: list[int]) -> int:
    """Length of the longest strictly increasing subsequence. O(n log n).

    >>> lis_len([10, 9, 2, 5, 3, 7, 101, 18])
    4
    >>> lis_len([])
    0
    >>> lis_len([5, 4, 3])
    1
    """
    # tails[k] = smallest tail value of any increasing subsequence of length k+1
    tails: list[int] = []
    for x in seq:
        # bisect_left for STRICTLY increasing. For non-decreasing (allow
        # equal), use bisect_right instead — that's the only change.
        pos = bisect.bisect_left(tails, x)
        if pos == len(tails):
            tails.append(x)
        else:
            tails[pos] = x
    return len(tails)


def lis_dp(seq: list[int]) -> list[int]:
    """Return one longest strictly increasing subsequence. O(n^2).

    Returns [] for an empty input. When there are ties it returns the one
    found first scanning left to right, which isn't necessarily unique.

    >>> lis_dp([10, 9, 2, 5, 3, 7, 101, 18])
    [2, 5, 7, 101]
    """
    n = len(seq)
    if n == 0:
        return []

    # dp[i] = length of the LIS ending exactly at index i.
    dp = [1] * n
    parent = [-1] * n

    for i in range(1, n):
        for j in range(i):
            if seq[j] < seq[i] and dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
                parent[i] = j

    # Rebuild by walking parents back from the best end index.
    best = max(range(n), key=lambda i: dp[i])
    path: list[int] = []
    i = best
    while i != -1:
        path.append(seq[i])
        i = parent[i]
    path.reverse()
    return path


if __name__ == "__main__":
    data = [10, 9, 2, 5, 3, 7, 101, 18]
    print("sequence:", data)
    print("O(n log n) length:", lis_len(data))
    print("O(n^2) one example:", lis_dp(data))
    print("all equal [2,2,2]:", lis_len([2, 2, 2]), lis_dp([2, 2, 2]))
