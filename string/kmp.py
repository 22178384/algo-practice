"""Knuth-Morris-Pratt substring search.

Time:  O(n + m) where n = len(text), m = len(pattern). The naive search is
       O(n*m); KMP avoids re-examining characters by precomputing where to
       resume after a mismatch.
Space: O(m) for the prefix table.

The prefix function (also called the failure function or pi table) is the part
that's easy to get wrong. pi[i] = length of the longest proper prefix of
pattern[:i+1] that is also a suffix of pattern[:i+1]. "Proper" means not the
whole string. So for "aabaa", pi = [0, 1, 0, 1, 2].

The classic bug: on mismatch, after falling back to `pi[j-1]`, you must NOT
advance i and you must re-test the same text character. Writing `i += 1` in the
mismatch branch (because it feels symmetric) breaks it. I've done it twice.

On the fallback loop `while j > 0 and pattern[j] != pattern[i]`: this is the
"while", not an "if". A single fallback isn't enough; you may need several.

Search returns 0-based start indices of all non-overlapping... no, actually all
*overlapping* occurrences. That's usually what you want; callers that need
non-overlapping can filter.
"""

from __future__ import annotations


def prefix_function(pattern: str) -> list[int]:
    """Compute the KMP prefix table for `pattern`.

    pi[i] = length of the longest proper prefix of pattern[:i+1] that is also a
    suffix of pattern[:i+1].

    >>> prefix_function("aabaa")
    [0, 1, 0, 1, 2]
    >>> prefix_function("abc")
    [0, 0, 0]
    >>> prefix_function("")
    []
    """
    m = len(pattern)
    pi = [0] * m
    # j tracks the length of the current matched prefix; i scans the pattern.
    j = 0
    for i in range(1, m):
        # Fall back until we match or run out of prefix to fall back to.
        while j > 0 and pattern[i] != pattern[j]:
            j = pi[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
        pi[i] = j
    return pi


def kmp_search(text: str, pattern: str) -> list[int]:
    """Return all 0-based start indices where `pattern` occurs in `text`.

    Overlapping occurrences are all returned: kmp_search("aaa", "aa") -> [0, 1].
    An empty pattern returns [] (matching it everywhere would be useless and
    would break the indexing).

    >>> kmp_search("ababcababd", "ababd")
    [5]
    >>> kmp_search("aaaa", "aa")
    [0, 1, 2]
    >>> kmp_search("abc", "xyz")
    []
    """
    if not pattern or not text:
        return []

    pi = prefix_function(pattern)
    matches: list[int] = []
    j = 0  # how many pattern chars are currently matched

    for i, ch in enumerate(text):
        while j > 0 and ch != pattern[j]:
            j = pi[j - 1]      # fall back, but stay on this text char
        if ch == pattern[j]:
            j += 1
        if j == len(pattern):
            # Found one ending at i. Record the start index.
            matches.append(i - len(pattern) + 1)
            # Continue searching: fall back so overlapping matches are found.
            # Using pi[j-1] (not resetting j to 0) is what makes "aaaa"/"aa"
            # return [0, 1, 2].
            j = pi[j - 1]

    return matches


def find_first(text: str, pattern: str) -> int:
    """Index of the first occurrence, or -1. Convenience wrapper."""
    hits = kmp_search(text, pattern)
    return hits[0] if hits else -1


if __name__ == "__main__":
    print("prefix_function('aabaa') =", prefix_function("aabaa"))
    print("search 'ababd' in 'ababcababd':", kmp_search("ababcababd", "ababd"))
    print("overlapping 'aa' in 'aaaa':", kmp_search("aaaa", "aa"))
    print("first 'needle' in 'a needle in a haystack':",
          find_first("a needle in a haystack", "needle"))
