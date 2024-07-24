import numpy as np
import math
import random

class Node:
    def __init__(self, x, y, cost=0, children=None, parent=None):
        self.x = x
        self.y = y
        self.cost = cost
        self.children = []
        self.parent = None
        self.left, self.right = None, None
        self.left2, self.right2 = None, None

    # def __eq__(self, node):
    #     return self.x == node.x and self.y == node.y

    def __repr__(self):
        return f'({self.x},{self.y})'
    
    def __str__(self):
        return self.__repr__()

    # returns a node of distance epsilon from itself to the argument node
    def calc_w(self, sample_node, epsilon):
        # create vectors
        node1 = np.array([self.x,self.y])
        node2 = np.array([sample_node.x, sample_node.y])

        #calculate direction vector 
        direction_vector = node2 - node1

        #normalize direction vector
        direction_vector = direction_vector / self.get_distance(sample_node)

        #multiply epsilon scalar
        direction_vector = direction_vector * epsilon

        #add initial coordinates to get w
        w = direction_vector + node1

        return Node(w[0], w[1])
    
    # returns distance to node
    def get_distance(self, node):
        distance = math.sqrt((node.x-self.x)**2 + (node.y-self.y)**2)
        return distance
    
    def get_coord(self):
        return (self.x, self.y)
    
    # OLD/OBSOLETE
    # returns the closest node to itself
    # precondition: self node is not in nodes list
    def closest_node(self, nodes):
        closest_node = nodes[0]
        smallest_dist = self.get_distance(nodes[0])

        for node in nodes:
            dist = self.get_distance(node)
            if dist < smallest_dist:
                closest_node = node
                smallest_dist = dist
    
        return closest_node
    
    # recursively adds a constant to all nodes in the tree
    def add_cost(self, diff_const):
        if diff_const == 0:
            return
        else:
            self.cost = self.cost + diff_const
            for child in self.children:
                child.add_cost(diff_const)
        return

    def get_coord_list(self):
        return [self.x, self.y]
    
    # prints the kd tree
    # reference: https://stackoverflow.com/questions/34012886/print-binary-tree-level-by-level-in-python
    def display(self):
        lines, *_ = self._display_aux()
        for line in lines:
            print(line)

    def _display_aux(self):
        """Returns list of strings, width, height, and horizontal coordinate of the root."""
        # No child.
        if self.right is None and self.left is None:
            line = '(%s,%s)' % (self.x, self.y)
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if self.right is None:
            lines, n, p, x = self.left._display_aux()
            s = '(%s,%s)' % (self.x, self.y)
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if self.left is None:
            lines, n, p, x = self.right._display_aux()
            s = '(%s,%s)' % (self.x, self.y)
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = self.left._display_aux()
        right, m, q, y = self.right._display_aux()
        s = '(%s,%s)' % (self.x, self.y)
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2
    
    def equals(self,a,b):
        if a.x == b.x and a.y == b.y:
            return True
        return False

# simple list implementation of a heap (as such, meant for small heaps)
class NodeHeap:
    def __init__(self, size):
        self.heap = [] # [(Node,distance),(Node,distance),(Node,distance)]
        self.size = size

    def push(self, node, distance):
        # find spot to insert and insert
        insert_point = 0
        for element in self.heap:
            if distance > element[1]:
                insert_point += 1
        self.heap.insert(insert_point, (node,distance))
        
        # if heap exceeds the heap size, pop off the largest node tuple (rightmost)
        if len(self.heap) > self.size:
            self.heap.pop()

    # returns the largest distance in the heap
    def peek_largest_dist(self):
        if len(self.heap) <= 0:
            return 0
        return self.heap[-1][1]
    
    def is_full(self):
        return len(self.heap) >= self.size
    
    def print(self):
        list_string = "["
        for element in self.heap:
            list_string = list_string + "((" + str(element[0].x) + "," + str(element[0].y) + ")," + str(element[1]) + "),"
        list_string = list_string[:-1] + "]"
        print("Heap: ", list_string)

if __name__ == "__main__":
    print("***************Testing NodeHeap***************")
    heap = NodeHeap(5)
    heap.print()

    values = [
        (Node(1, 1), 1),
        (Node(2, 2), 2),
        (Node(3, 3), 3),
        (Node(4, 4), 4),
        (Node(5, 5), 5),
        (Node(6, 6), 6),
        (Node(7, 7), 7),
        (Node(8, 8), 8),
    ]

    for i in range(10):
        value = random.choice(values)
        print("Pushing: ", value[1])

        heap.push(value[0], value[1])
        heap.print()

