"""快速排序（由 @c991china 贡献）。"""


def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    mid = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + mid + quick_sort(right)


if __name__ == "__main__":
    data = [5, 2, 9, 1, 5, 6]
    print("after:", quick_sort(data))
