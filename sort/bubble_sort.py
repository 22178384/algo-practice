"""冒泡排序（带测试）。"""


def bubble_sort(arr):
    a = list(arr)
    n = len(a)
    for i in range(n):
        for j in range(0, n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
    return a


if __name__ == "__main__":
    data = [5, 2, 9, 1, 5, 6]
    print("before:", data)
    print("after :", bubble_sort(data))
