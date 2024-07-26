from Node import Node

# KDTree implementation (2D) for Node class
# Reference: https://www.geeksforgeeks.org/search-and-insertion-in-k-dimensional-tree/
class KDTree:
    def __init__(self, nodes=[]):
        self.root = None
        for node in nodes:
            self.insert(node)
    
    # recursive insert. Used by insert()
    def insertRec(self, root, node, depth):
        # Base Case
        if root == None:
            return node
    
        # Calculate current dimension of comparison (either 0 or 1 indicating x axis or y axis comparison)
        cd = depth % 2

        # Recursive Case
        if cd == 0:
            if node.x < root.x:
                root.left = self.insertRec(root.left, node, depth + 1)
            else:
                root.right = self.insertRec(root.right, node, depth + 1)           
        else:
            if node.y < root.y:
                root.left = self.insertRec(root.left, node, depth + 1)
            else:
                root.right = self.insertRec(root.right, node, depth + 1)   

        return root
    
    # insert a node into the kd tree
    def insert(self,node):
        if self.root == None:
            self.root = node
        else:
            self.insertRec(self.root, node, 0)

    # recursive search. used by search()
    def searchRec(self, root, x,y, depth):
        # Base Case
        if root == None or (root.x == x and root.y == y):
            return root
        
        # Calculate current dimension of comparison (either 0 or 1 indicating x axis or y axis comparison)
        cd = depth % 2

        # Recursive Case
        if cd == 0:
            if x < root.x:
                return self.searchRec(root.left, x,y, depth + 1)
            else:
                return self.searchRec(root.right, x,y, depth + 1)
        else:
            if y < root.y:
                return self.searchRec(root.left, x,y, depth + 1)
            else:
                return self.searchRec(root.right, x,y, depth + 1)
    
    # returns the node of (x,y) if it is in the tree
    # else returns None
    def search(self, x, y):
        return self.searchRec(self.root, x, y, 0)
    

    def nearestNeighborRec(self, root, target, depth, best_node, best_distance, excluding_node):
        # Base Case
        if root == None:
            return best_node, best_distance
        
        # Recursive Case
        # check current node. Check if initializing recursion node, or if closer node (better distance)
        # also check if node overlaps target and skip
        distance = root.get_distance(target)
        if (best_node == None or distance < best_distance) and distance != 0 and root != excluding_node:
            best_node, best_distance = root, distance

        # Traverse left or right
        # Calculate current dimension of comparison (either 0 or 1 indicating x axis or y axis comparison)
        cd = depth % 2

        if cd == 0:
            if target.x < root.x: # traverse left
                best_node, best_distance = self.nearestNeighborRec(root.left, target, depth + 1, best_node, best_distance, excluding_node)

                # check if other side is worth traversing as well
                if root.x - target.x < best_distance:
                    best_node, best_distance = self.nearestNeighborRec(root.right, target, depth + 1, best_node, best_distance, excluding_node)
            else: # traverse right
                best_node, best_distance = self.nearestNeighborRec(root.right, target, depth + 1, best_node, best_distance, excluding_node)
                if target.x - root.x < best_distance:
                    best_node, best_distance = self.nearestNeighborRec(root.left, target, depth + 1, best_node, best_distance, excluding_node)
        else:
            if target.y < root.y: # traverse left
                best_node, best_distance = self.nearestNeighborRec(root.left, target, depth + 1, best_node, best_distance, excluding_node)
                if root.y - target.y < best_distance:
                    best_node, best_distance = self.nearestNeighborRec(root.right, target, depth + 1, best_node, best_distance, excluding_node)
            else: # traverse right
                best_node, best_distance = self.nearestNeighborRec(root.right, target, depth + 1, best_node, best_distance, excluding_node)
                if target.y - root.y < best_distance:
                    best_node, best_distance = self.nearestNeighborRec(root.left, target, depth + 1, best_node, best_distance, excluding_node)

        return best_node, best_distance
    
    # returns the nearest node to the target (excluding the target itself) and its distance from the target
    def nearestNeighbor(self, target, excluding_node):
        return self.nearestNeighborRec(self.root, target, 0, None, 1, excluding_node)

    # recursively traverses tree and adds nodes within radius r of the target to the neighbors list parameter
    def neighborsInRadiusRec(self, root, target, depth, r, neighbors):
        # Base case
        if root == None:
            return
        
        # Recursive case
        # Check current node
        if root.get_distance(target) <= r:
            neighbors.append(root)

        # print("Current Root: (%s,%s)" %(root.x,root.y))
        # Traverse left or right
        # Calculate current dimension of comparison (either 0 or 1 indicating x axis or y axis comparison)
        cd = depth % 2

        if cd == 0:
            if target.x < root.x: # traverse left
                self.neighborsInRadiusRec(root.left, target, depth + 1, r, neighbors)

                # check if other side is worth traversing as well
                if root.x - target.x <= r:
                    self.neighborsInRadiusRec(root.right, target, depth + 1, r, neighbors)
            else: # traverse right
                self.neighborsInRadiusRec(root.right, target, depth + 1, r, neighbors)
                if target.x - root.x <= r:
                    self.neighborsInRadiusRec(root.left, target, depth + 1, r, neighbors)
        else:
            if target.y < root.y: # traverse left
                self.neighborsInRadiusRec(root.left, target, depth + 1, r, neighbors)
                if root.y - target.y <= r:
                    self.neighborsInRadiusRec(root.right, target, depth + 1, r, neighbors)
            else: # traverse right
                self.neighborsInRadiusRec(root.right, target, depth + 1, r, neighbors)
                if target.y - root.y <= r:
                    self.neighborsInRadiusRec(root.left, target, depth + 1, r, neighbors)


    # returns list of neighbors within a radius r
    # Includes overlapping nodes (nodes with same x and y as the target)
    def neighborsInRadius(self, target, r):
        neighbors = []
        self.neighborsInRadiusRec(self.root, target, 0, r, neighbors)
        return neighbors