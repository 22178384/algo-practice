"""Dijkstra's algorithm with a binary heap.

Time:  O((V + E) log V).
Space: O(V).

WARNING: Dijkstra assumes all edge weights are >= 0. With a negative edge it
does not raise, it just returns wrong distances. If you need negatives, use
Bellman-Ford (O(VE)) or Johnson's algorithm. I'm spelling this out because the
silent wrongness is the trap.

Graph representation: dict[str, list[tuple[str, int]]] — node -> [(neighbor,
weight), ...]. Weights can be ints or floats.

The lazy-deletion trick: we never decrease a key in the heap. Instead we push a
new (dist, node) entry whenever we find a shorter path, and skip stale entries
when we pop them (`if d > dist[node]: continue`). That check is what makes the
algorithm correct despite the heap containing duplicates. Remove it and you'll
get subtly wrong answers.
"""

from __future__ import annotations

import heapq

Graph = dict[str, list[tuple[str, float]]]

INF = float("inf")


def dijkstra(graph: Graph, start: str) -> tuple[dict[str, float], dict[str, str | None]]:
    """Return (distances, parents) from `start`.

    distances: {node: shortest distance}. Unreachable nodes are absent.
    parents:   {node: predecessor on the shortest path}, start maps to None.

    >>> g = {"a": [("b", 1), ("c", 4)], "b": [("c", 2)], "c": []}
    >>> dist, _ = dijkstra(g, "a")
    >>> dist["c"]
    3
    """
    dist: dict[str, float] = {start: 0.0}
    parent: dict[str, str | None] = {start: None}
    heap: list[tuple[float, str]] = [(0.0, start)]

    while heap:
        d, node = heapq.heappop(heap)

        # Stale entry: we already found a shorter route to `node`. Skip it.
        # This is the lazy-deletion check, don't remove it.
        if d > dist.get(node, INF):
            continue

        for neighbor, weight in graph.get(node, ()):
            if weight < 0:
                raise ValueError(
                    f"negative edge weight {weight} ({node} -> {neighbor}); "
                    "Dijkstra requires non-negative weights"
                )
            candidate = d + weight
            if candidate < dist.get(neighbor, INF):
                dist[neighbor] = candidate
                parent[neighbor] = node
                heapq.heappush(heap, (candidate, neighbor))

    return dist, parent


def shortest_path(graph: Graph, start: str, goal: str) -> list[str] | None:
    """Return the cheapest path from start to goal, or None if unreachable.

    >>> g = {"a": [("b", 1), ("c", 4)], "b": [("c", 2)], "c": []}
    >>> shortest_path(g, "a", "c")
    ['a', 'b', 'c']
    """
    if start == goal:
        return [start]

    dist, parent = dijkstra(graph, start)
    if goal not in dist:
        return None

    path = [goal]
    node = parent[goal]
    while node is not None:
        path.append(node)
        node = parent[node]
    path.reverse()
    return path


if __name__ == "__main__":
    graph: Graph = {
        "a": [("b", 1), ("c", 4)],
        "b": [("c", 2), ("d", 5)],
        "c": [("d", 1)],
        "d": [],
    }
    dist, _ = dijkstra(graph, "a")
    print("distances from a:", {k: dist[k] for k in sorted(dist)})
    print("cheapest a -> d:", shortest_path(graph, "a", "d"))

    try:
        dijkstra({"x": [("y", -1)], "y": []}, "x")
    except ValueError as exc:
        print("negative weight caught:", exc)
