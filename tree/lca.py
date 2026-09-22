"""Lowest common ancestor (LCA).

Two problems with the same name:

1. Binary tree (not necessarily a BST): no ordering to exploit, so it's a
   recursive DFS. O(n) time, O(h) space on the stack (h = height; O(log n) if
   balanced, O(n) if it's a linked list).

2. Binary search tree: use the ordering and walk down iteratively. O(h) time,
   O(1) space.

The recursive version has one detail worth internalizing: if the two targets end
up in different subtrees, the current node is the LCA. That's the base case
people miss — they try to return something from the children instead.

Assumes node values are unique. Duplicates break the `node is a or node is b`
comparison silently, giving a wrong answer rather than an error.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TreeNode:
    val: int
    left: "TreeNode | None" = None
    right: "TreeNode | None" = None


def lca_binary_tree(root: TreeNode | None, a: TreeNode, b: TreeNode) -> TreeNode | None:
    """LCA of two nodes in a plain binary tree. O(n) time, O(h) space.

    Returns None if either node isn't in the tree. This version assumes both
    nodes ARE present, which is the usual interview setup; for the "might be
    missing" case you need to track found flags, which doubles the code.

    >>> root = TreeNode(3, TreeNode(5, TreeNode(6), TreeNode(2, TreeNode(7), TreeNode(4))), TreeNode(1, TreeNode(0), TreeNode(8)))
    >>> lca_binary_tree(root, root.left, root.right).val
    3
    >>> lca_binary_tree(root, root.left, root.left.right.left).val
    5
    """
    if root is None:
        return None

    # Found one of the targets: report it upward. Note this also handles
    # root being the ancestor of the other target.
    if root is a or root is b:
        return root

    left = lca_binary_tree(root.left, a, b)
    right = lca_binary_tree(root.right, a, b)

    # Both sides found something => a and b are in different subtrees, so the
    # split point is right here.
    if left is not None and right is not None:
        return root

    # Otherwise the answer is whichever side found something (may be None).
    return left if left is not None else right


def lca_bst(root: TreeNode | None, a: TreeNode, b: TreeNode) -> TreeNode | None:
    """LCA in a binary search tree. O(h) time, O(1) space.

    Walks down from the root. The first node whose value lies between a and b
    (inclusive) is the LCA, because from there the two targets go different
    ways. No recursion, no stack.

    >>> root = TreeNode(6, TreeNode(2, TreeNode(0), TreeNode(4, TreeNode(3), TreeNode(5))), TreeNode(8, TreeNode(7), TreeNode(9)))
    >>> lca_bst(root, root.left, root.right).val
    6
    >>> lca_bst(root, root.left.right.left, root.left.right.right).val
    4
    """
    lo, hi = sorted((a.val, b.val))
    node = root

    while node is not None:
        if node.val < lo:
            node = node.right          # both targets are in the right subtree
        elif node.val > hi:
            node = node.left           # both are in the left subtree
        else:
            return node                # lo <= node.val <= hi: this is the LCA
    return None


if __name__ == "__main__":
    # Plain tree
    #          3
    #        /   \
    #       5     1
    #      / \   / \
    #     6   2 0   8
    #        / \
    #       7   4
    tree = TreeNode(
        3,
        TreeNode(5, TreeNode(6), TreeNode(2, TreeNode(7), TreeNode(4))),
        TreeNode(1, TreeNode(0), TreeNode(8)),
    )
    print("LCA(5, 1) =", lca_binary_tree(tree, tree.left, tree.right).val)          # 3
    print("LCA(6, 4) =", lca_binary_tree(tree, tree.left.left,
                                          tree.left.right.right).val)               # 5
    print("LCA(7, 4) =", lca_binary_tree(tree, tree.left.right.left,
                                          tree.left.right.right).val)               # 2

    # BST
    #          6
    #        /   \
    #       2     8
    #      / \   / \
    #     0   4 7   9
    #        / \
    #       3   5
    bst = TreeNode(
        6,
        TreeNode(2, TreeNode(0), TreeNode(4, TreeNode(3), TreeNode(5))),
        TreeNode(8, TreeNode(7), TreeNode(9)),
    )
    print("BST LCA(0, 8) =", lca_bst(bst, bst.left.left, bst.right).val)            # 6
    print("BST LCA(3, 5) =", lca_bst(bst, bst.left.right.left,
                                     bst.left.right.right).val)                     # 4
