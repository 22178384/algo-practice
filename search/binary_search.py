"""二分查找（要求有序数组）。"""


def binary_search(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        if arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


if __name__ == "__main__":
    a = [1, 3, 5, 7, 9, 11]
    for t in (5, 8):
        print(f"target {t} -> index {binary_search(a, t)}")
