"""Coin change: two problems that look the same and are not.

Problem A (min_coins): fewest coins that sum to `amount`. Coins can repeat.
    dp[x] = min coins to make x.  dp[0] = 0, dp[x] = 1 + min(dp[x - c]) for c <= x.
    Unreachable states stay at infinity.

Problem B (count_ways): number of *combinations* that sum to `amount`.
    dp[x] = number of ways. dp[0] = 1 (the empty set), dp[x] += dp[x - c].
    Crucially, the coin loop must be OUTSIDE the amount loop. That's what makes
    it count combinations, not permutations. Swap the loops and
    amount=3, coins=[1,2] gives 3 (1+1+1, 1+2, 2+1) instead of 2.

I got B wrong in an interview once by swapping those loops. Never again.

Time:  O(amount * len(coins)) for both.
Space: O(amount) for both.
"""

from __future__ import annotations

INF = float("inf")


def min_coins(coins: list[int], amount: int) -> int:
    """Fewest coins summing to `amount`, or -1 if it can't be done.

    >>> min_coins([1, 2, 5], 11)
    3
    >>> min_coins([2], 3)
    -1
    >>> min_coins([], 0)
    0
    """
    if amount < 0:
        raise ValueError("amount must be non-negative")
    if amount == 0:
        return 0

    # dp[x] = min coins to reach x; INF means "not reachable yet".
    dp = [INF] * (amount + 1)
    dp[0] = 0

    for x in range(1, amount + 1):
        for c in coins:
            if c <= x and dp[x - c] + 1 < dp[x]:
                dp[x] = dp[x - c] + 1

    return -1 if dp[amount] == INF else int(dp[amount])


def count_ways(coins: list[int], amount: int) -> int:
    """Number of combinations of `coins` (reusable) summing to `amount`.

    Order doesn't matter: [1, 2] and [2, 1] count once.

    >>> count_ways([1, 2, 5], 5)
    4
    >>> count_ways([2], 3)
    0
    """
    if amount < 0:
        raise ValueError("amount must be non-negative")

    dp = [0] * (amount + 1)
    dp[0] = 1  # one way to make 0: use no coins

    # Coins outer, amount inner => combinations. Do not swap these loops.
    for c in coins:
        for x in range(c, amount + 1):
            dp[x] += dp[x - c]

    return dp[amount]


def min_coins_with_path(coins: list[int], amount: int) -> list[int] | None:
    """Same as min_coins but also returns one optimal coin multiset.

    Returns None if the amount is unreachable. Useful when you need to show
    the actual answer, not just its size.
    """
    if amount < 0:
        raise ValueError("amount must be non-negative")
    if amount == 0:
        return []

    dp = [INF] * (amount + 1)
    dp[0] = 0
    choice = [-1] * (amount + 1)  # which coin we used to reach x

    for x in range(1, amount + 1):
        for c in coins:
            if c <= x and dp[x - c] + 1 < dp[x]:
                dp[x] = dp[x - c] + 1
                choice[x] = c

    if dp[amount] == INF:
        return None

    path: list[int] = []
    x = amount
    while x > 0:
        c = choice[x]
        path.append(c)
        x -= c
    return sorted(path)


if __name__ == "__main__":
    coins, amount = [1, 2, 5], 11
    print(f"min coins for {amount} with {coins}: {min_coins(coins, amount)}")
    print("one such solution:", min_coins_with_path(coins, amount))
    print(f"ways to make 5 with {coins}: {count_ways(coins, 5)}")
    print("unreachable (coins=[2], amount=3):", min_coins([2], 3))
