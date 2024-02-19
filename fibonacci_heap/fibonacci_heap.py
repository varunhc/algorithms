# explanations for member functions are provided in requirements.py
from __future__ import annotations


class FibNode:
    def __init__(self, val: int):
        self.val = val
        self.parent = None
        self.children = []
        self.flag = False

    def get_value_in_node(self):
        return self.val

    def get_children(self):
        return self.children

    def get_flag(self):
        return self.flag

    def __eq__(self, other: FibNode):
        return self.val == other.val


class FibHeap:
    def __init__(self):
        # you may define any additional member variables you need
        self.roots = []
        self.minVal = None
        self.totalNodes = 0

    def get_roots(self) -> list:
        return self.roots

    def insert(self, val: int) -> FibNode:
        self.totalNodes += 1
        node = FibNode(val=val)
        self.roots.append(node)
        if not self.minVal or val < self.minVal.val:
            self.minVal = node
        return node

    def delete_min(self) -> None:
        self.totalNodes -= 1
        self.roots.pop(self.roots.index(self.minVal))
        self.promote_min_children()
        self.restructure()
        self.update_min()

    def update_min(self):
        self.minVal = None
        for root in self.roots:
            if not self.minVal or root.val < self.minVal.val:
                self.minVal = root

    def promote_min_children(self):
        queue = self.minVal.children
        while queue:
            curr = queue.pop(0)
            curr.flag = False
            if curr.parent == self.minVal:
                curr.parent = None
                self.roots.append(curr)
            queue.extend(curr.children)

    def restructure(self):
        node_degree = [None for _ in range(self.totalNodes)]
        i = 0
        while i < len(self.roots):
            curr = self.roots[i]
            currTotalChildren = len(curr.children)
            equalDegreeVal = node_degree[currTotalChildren]
            if equalDegreeVal and equalDegreeVal != curr:
                a, b = curr, equalDegreeVal
                if a.val > b.val: a, b = b, a
                a.children.append(b)
                b.parent = a
                self.roots.pop(self.roots.index(b))
                i = 0
                node_degree[currTotalChildren] = None
            else:
                i += 1
                node_degree[currTotalChildren] = curr

    def find_min(self) -> FibNode:
        return self.minVal

    def promote_parent(self, node: FibNode):
        if node.flag == True:
            if node not in self.roots:
                parent = node.parent
                if parent:
                    parent.children.pop(parent.children.index(node))
                    self.roots.append(node)
                    node.parent = None
                    self.promote_parent(parent)
        else:
            if node not in self.roots:
                node.flag = True

    def decrease_priority(self, node: FibNode, new_val: int) -> None:
        parent = node.parent
        if parent:
            self.promote_parent(node.parent)
            parent.children.pop(parent.children.index(node))
        node.parent = None
        node.val = new_val
        if node not in self.roots:
            self.roots.append(node)
        if not self.minVal or self.minVal.val > node.val:
            self.minVal = node
