"""Breadth-first search on an unweighted graph.

Time:  O(V + E).
Space: O(V).

BFS gives you shortest paths in edge count, which is the whole point. If the
graph is weighted you need Dijkstra (see dijkstra.py). BFS on a weighted graph
gives you the path with the fewest *edges*, which is usually not what you want.

Graph representation: dict[str, list[str]]. Missing keys are treated as nodes
with no outgoing edges, so you don't have to list leaf nodes explicitly.

`deque.popleft()` is O(1). Using `list.pop(0)` instead makes the whole thing
O(V^2) because every pop shifts the rest of the list. I've seen that shipped.
"""

from __future__ import annotations

from collections import deque


def bfs_shortest_path(
    graph: dict[str, list[str]], start: str, goal: str
) -> list[str] | None:
    """Return the fewest-edges path from start to goal, or None.

    Includes both endpoints. A start == goal returns [start].

    >>> g = {"a": ["b", "c"], "b": ["d"], "c": ["d"], "d": []}
    >>> bfs_shortest_path(g, "a", "d")
    ['a', 'b', 'd']
    """
    if start == goal:
        return [start]

    # parent[x] = the node we came from when we first reached x. The first time
    # we see a node is via a shortest path, so we never need to overwrite it.
    parent: dict[str, str | None] = {start: None}
    queue: deque[str] = deque([start])

    while queue:
        node = queue.popleft()
        for neighbor in graph.get(node, ()):
            if neighbor in parent:
                continue  # already visited, and via a path no longer than ours
            parent[neighbor] = node
            if neighbor == goal:
                return _reconstruct(parent, goal)
            queue.append(neighbor)

    return None


def bfs_distances(graph: dict[str, list[str]], start: str) -> dict[str, int]:
    """Return {node: edge count from start} for every reachable node.

    Unreachable nodes are simply absent from the result. If you need them as
    -1, fill in the difference at the call site.
    """
    dist = {start: 0}
    queue: deque[str] = deque([start])

    while queue:
        node = queue.popleft()
        for neighbor in graph.get(node, ()):
            if neighbor not in dist:
                dist[neighbor] = dist[node] + 1
                queue.append(neighbor)

    return dist


def _reconstruct(parent: dict[str, str | None], goal: str) -> list[str]:
    path = [goal]
    node = parent[goal]
    while node is not None:
        path.append(node)
        node = parent[node]
    path.reverse()
    return path


if __name__ == "__main__":
    graph = {
        "you": ["alice", "bob", "claire"],
        "bob": ["anuj", "peggy"],
        "alice": ["peggy"],
        "claire": ["thom", "jonny"],
        "anuj": [],
        "peggy": [],
        "thom": [],
        "jonny": [],
    }
    print("path to thom:", bfs_shortest_path(graph, "you", "thom"))
    print("path to peggy:", bfs_shortest_path(graph, "you", "peggy"))
    print("path to nobody:", bfs_shortest_path(graph, "you", "nobody"))
    print("distances:", bfs_distances(graph, "you"))
