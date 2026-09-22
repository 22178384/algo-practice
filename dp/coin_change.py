"""零钱兑换（动态规划）。"""

from functools import lru_cache


def coin_change(coins, amount):
    @lru_cache(None)
    def min_coins(rem):
        if rem == 0:
            return 0
        if rem < 0:
            return float("inf")
        return 1 + min(min_coins(rem - c) for c in coins)

    ans = min_coins(amount)
    return ans if ans != float("inf") else -1


if __name__ == "__main__":
    print(coin_change([1, 2, 5], 11))  # 3
