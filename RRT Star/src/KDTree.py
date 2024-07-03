from Node import Node, NodeHeap


# KDTree implementation (2D) for Node class
# Reference: https://www.geeksforgeeks.org/search-and-insertion-in-k-dimensional-tree/
class KDTree:
    def __init__(self, nodes):
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
    

    def nearestNeighborRec(self, root, target, depth, best_node, best_distance):
        # Base Case
        if root == None:
            return best_node, best_distance
        
        # Recursive Case
        # check current node. Check if initializing recursion node, or if closer node (better distance)
        # also check if node overlaps target and skip
        distance = root.get_distance(target)
        if (best_node == None or distance < best_distance) and distance != 0:
            best_node, best_distance = root, distance

        # Traverse left or right
        # Calculate current dimension of comparison (either 0 or 1 indicating x axis or y axis comparison)
        cd = depth % 2

        if cd == 0:
            if target.x < root.x: # traverse left
                best_node, best_distance = self.nearestNeighborRec(root.left, target, depth + 1, best_node, best_distance)

                # check if other side is worth traversing as well
                if root.x - target.x < best_distance:
                    best_node, best_distance = self.nearestNeighborRec(root.right, target, depth + 1, best_node, best_distance)
            else: # traverse right
                best_node, best_distance = self.nearestNeighborRec(root.right, target, depth + 1, best_node, best_distance)
                if target.x - root.x < best_distance:
                    best_node, best_distance = self.nearestNeighborRec(root.left, target, depth + 1, best_node, best_distance)
        else:
            if target.y < root.y: # traverse left
                best_node, best_distance = self.nearestNeighborRec(root.left, target, depth + 1, best_node, best_distance)
                if root.y - target.y < best_distance:
                    best_node, best_distance = self.nearestNeighborRec(root.right, target, depth + 1, best_node, best_distance)
            else: # traverse right
                best_node, best_distance = self.nearestNeighborRec(root.right, target, depth + 1, best_node, best_distance)
                if target.y - root.y < best_distance:
                    best_node, best_distance = self.nearestNeighborRec(root.left, target, depth + 1, best_node, best_distance)

        return best_node, best_distance
    
    # returns the nearest node to the target (excluding the target itself) and its distance from the target
    def nearestNeighbor(self, target):
        return self.nearestNeighborRec(self.root, target, 0, None, 1)

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

    def kNearestNeighborsRec(self, root, target, depth, heap):
        # Base Case
        if root == None:
            return
        
        # Recursive Case
        # Check current node
        distance = root.get_distance(target)
        if distance < heap.peek_largest_dist() or not heap.is_full():
            heap.push(root, distance)

        # Traverse left or right
        # Calculate current dimension of comparison (either 0 or 1 indicating x axis or y axis comparison)
        cd = depth % 2

        if cd == 0:
            if target.x < root.x: # traverse left
                self.kNearestNeighborsRec(root.left, target, depth+1, heap)

                # check if other side is worth traversing as well
                if root.x - target.x < heap.peek_largest_dist() or not heap.is_full():
                    self.kNearestNeighborsRec(root.right, target, depth+1, heap)
            else: # traverse right
                self.kNearestNeighborsRec(root.right, target, depth+1, heap)
                if target.x - root.x < heap.peek_largest_dist() or not heap.is_full():
                    self.kNearestNeighborsRec(root.left, target, depth+1, heap)
        else:
            if target.y < root.y: # traverse left
                self.kNearestNeighborsRec(root.left, target, depth+1, heap)
                if root.y - target.y < heap.peek_largest_dist() or not heap.is_full():
                    self.kNearestNeighborsRec(root.right, target, depth+1, heap)
            else: # traverse right
                self.kNearestNeighborsRec(root.right, target, depth+1, heap)
                if target.y - root.y < heap.peek_largest_dist() or not heap.is_full():
                    self.kNearestNeighborsRec(root.left, target, depth+1, heap)

    
    # returns list of k nearest neighbors
    # Excludes overlapping nodes (nodes with same x and y as the target)
    def kNearestNeighbors(self, target, k):
        # makes a heap of maxsize k
        heap = NodeHeap(k)
        self.kNearestNeighborsRec(self.root, target, 0, heap)
        return heap.heap




if __name__ == "__main__":
    kdtree = KDTree()
    coords = [(3, 6), (17, 15), (3,6), (3,6), (13, 15), (6, 12), (9, 1), (2, 7), (10, 19), (5, 4)]

    for coord in coords:
        kdtree.insert(Node(coord[0], coord[1]))

    kdtree.root.display()

    print(kdtree.search(5,4).get_coord())
    if kdtree.search(9,0) == None:
        print("None detected")

    nearest_node, distance = kdtree.nearestNeighbor(Node(2,6))
    print("Nearest Node: (%s,%s)\nDistance: %s" %(nearest_node.x, nearest_node.y, distance))

    print("_________________________________________________")
    neighbors = kdtree.neighborsInRadius(Node(2,7), 2)
    for neighbor in neighbors:
        print("Neighbor: (%s,%s)\nDistance: %s" %(neighbor.x, neighbor.y, neighbor.get_distance(Node(2,7))))

    print("_________________________________________________")
    neighbors2 = kdtree.kNearestNeighbors(Node(6,5), 5)
    i = 0
    for neighbor in neighbors2:
        print("%s: Neighbor: (%s,%s)\nDistance: %s" %(i, neighbor[0].x, neighbor[0].y, neighbor[1]))
        i += 1