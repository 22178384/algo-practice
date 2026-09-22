"""堆排序（由练习补充）。"""


def heap_sort(arr):
    import heapq
    heapq.heapify(arr)
    return [heapq.heappop(arr) for _ in range(len(arr))]


if __name__ == "__main__":
    print(heap_sort([5, 2, 9, 1, 5, 6]))
