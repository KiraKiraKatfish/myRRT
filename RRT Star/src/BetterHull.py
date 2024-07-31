from Node import Node
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import Delaunay
import math
import heapq
import random
from triangle import triangulate
import json
from matplotlib.path import Path

class HullNode(Node):
    def __init__(self,node, on_hull):
        super().__init__(node.x,node.y)
        ## attributes included ##
        # self.x
        # self.y
        # self.left
        # self.right
        self.on_hull = on_hull

    def __lt__(self,other):
        return False

# Describes a concave hull around a path
# 4-step process:
# 1. Convert path to a dot pattern (DP)
# 2. Construct a Convex Hull around DP. Using Jarvis March
# 3. Recursively "cut" Convex Hull until it accurately describes concavities in the DP (Concave Hull)
# 4. Merge edges prioritizing merges adding the smallest area to the Hull. Merge until k desired edges are left in Hull, where k >= 3
class BetterHull():
    def __init__(self,path, k):
        self.root = None
        self.size = 0
        self.target_size = k
        self.path = [HullNode(x,False) for x in path]
        self.DP = None

        # step 1. Convert path to a dot pattern (DP)
        self.DP = self.path_to_DP(self.path, 1)

        # step 2. Construct a Convex Hull around DP
        self.jarvis_march()

        # step 3. "cut" Convex Hull until it accurately describes concavities in the DP (Concave Hull)
        self.make_concave()

        # step 4. Merge edges prioritizing merges adding the smallest area to the Hull. Merge until k desired edges are left in Hull, where k >= 3
        #self.merge_until_ksize(k)

    def add_node(self,node):
        node.on_hull = True
        if self.root == None:
            self.root = node
        else:
            i = self.root
            while i.right:
                i = i.right
            self.link_nodes(i, node)
        self.size += 1

    # Input: node to be removed from the hull
    # Precondition: node is on the hull. hull size > 3
    # Postcondition: 
    def remove_node(self,node):
        node.on_hull = False

        # Edge Case: removing root
        if node == self.root:
            self.root = self.root.right

        self.link_nodes(node.left,node.right)
        self.size -= 1
        


    def link_nodes(self, node_a, node_b):
        node_a.right = node_b
        node_b.left = node_a

    # Input: a list of nodes forming a path
    # Output: a DP (dot pattern) of HullNodes tracing the path. Method is drawing circles of radius r around path points 
    # Use-case: to transform a linear path into a DP such that a minimum hull can be calculated
    def path_to_DP(self,path,r):
        # pre-processing
        # add more nodes along path if needed
        path_adjusted = []
        for node_a, node_b in zip(path, path[1:]):
            path_adjusted.append(node_a)
            v = [node_b.x - node_a.x, node_b.y - node_a.y]
            v_magnitude = math.sqrt(v[0]**2 + v[1]**2)
            v_unit = [v[0]/v_magnitude, v[1]/v_magnitude]
            for i in range(1,math.floor(node_a.get_distance(node_b) / (r))):
                path_adjusted.append(HullNode(Node(node_a.x+v_unit[0]*i, node_a.y+v_unit[1]*i),False))
            path_adjusted.append(node_b)

        self.path = path_adjusted
        DP = []
        theta = 0

        for node in path_adjusted:
            DP.append(node)
            while theta <= 360:
                DP.append(HullNode(Node(node.x + math.cos(math.radians(theta))*r, node.y + math.sin(math.radians(theta))*r), False))
                theta += 45
            theta = 0
        
        return DP
    
    # Pre-condition: self.DP contains a list of nodes.
    # Output: The convex hull, sorted clockwise stored in linked list starting at self.root.
    # Time Complexity: O(nh), where n is the # of nodes, h is the # of nodes in the convex hull
    # Reference: https://www.youtube.com/watch?v=nBvCZi34F_o
    def jarvis_march(self):
        # find the leftmost node
        on_hull = self.DP[0]
        for node in self.DP: # O(n)
            if node.x < on_hull.x:
                on_hull = node

        # construct convex hull
        while True:
            self.add_node(on_hull)
            next_node = self.DP[0]
            for node in self.DP:
                o = self.orientation(on_hull,next_node,node)
                if next_node == on_hull or o == 1 or (o == 0 and on_hull.get_distance(node) > on_hull.get_distance(next_node)):
                    next_node = node
            if next_node == self.root:
                self.link_nodes(on_hull,self.root)
            on_hull = next_node
            if on_hull == self.root:
                break

    def make_concave(self):
        i = self.root
        j = i.right
        while j != self.root:
            if self.cut(i,j):
                j = i.right
            else:
                i = j
                j = j.right
        
        # cut the connecting edge (from tail to root)
        while i != self.root:
            if self.cut(i,j):
                j = i.right
            else:
                i = j
                j = j.right

    def merge_until_ksize(self,k):
        heap = self.potential_merges(self.root,self.root)
        heapq.heapify(heap)
        
        # while heap:
        #     print("Area: %s"%(heapq.heappop(heap)[0]))

        while self.size > k and len(heap) != 0:
            new_merges = self.merge(heapq.heappop(heap))

            for tuple in new_merges:
                heapq.heappush(heap, tuple)

        return

    # Input: start and end nodes
    # Postcondition: returns a list of tuples (Area, True, (n1,n2,n3)) or (Area, False, (n1,n2,n3,n4,n5)). Tuple type depends on concave or convex merge
    #                True/False value in tuple[1] indicates concave/convex respectively
    #                tuples describe all potential adjacent merges between the start and end nodes
    def potential_merges(self,start,end):
        potential_merges = []
        head = start.right.right
        tail = start

        prev_angle = None
        curr_angle = self.get_angle(tail,tail.right,head)

        # iterate through all nodes between start and end (inclusive)
        while head != end.right:
            # indicates concave merge
            if curr_angle >= 180:
                area = self.get_triangle_area(tail,tail.right,head)
                potential_merges.append((area, True, (tail,tail.right,head)))

            # indicates convex merge
            elif prev_angle and prev_angle < 180 and curr_angle < 180 and prev_angle + curr_angle > 180:
                new_node = self.intersect_point(tail.left,tail,tail.right,head)
                area = self.get_triangle_area(tail,new_node,tail.right)
                potential_merges.append((area, False, (tail.left,tail,new_node,tail.right,head)))

            tail = tail.right
            head = head.right
            prev_angle = curr_angle
            curr_angle = self.get_angle(tail,tail.right,head)
            
        return potential_merges
    
    # Input: tuple containing area, concave/convex, and included nodes
    # Postcondition: merge reflected in hull. new potential local merges returned (should take and add to heap)
    def merge(self, tuple):
        # indicates concave merge
        if tuple[1]:
            # check if tuple is still valid
            # i.e. all nodes are still on_hull
            for node in tuple[2]:
                if not node.on_hull:
                    return []

            # do the merge
            self.remove_node(tuple[2][1])

            # update local area
            return self.potential_merges(tuple[2][0].left.left,tuple[2][2].right.right)
        
        # indicates convex merge
        else:
            # check if tuple is still valid
            # i.e. all nodes but tuple[2][2] (node to be added) are still on_hull
            for node in tuple[2]:
                if not node.on_hull and node != tuple[2][2]:
                    return []            

            # Note: tuple[2][2] is the new intersection node to be added
            # Following code removes nodes adjacent to tuple[2][2], then adds tuple[2][2] into the linked list
            self.remove_node(tuple[2][1])
            self.remove_node(tuple[2][3])
            self.link_nodes(tuple[2][0], tuple[2][2])
            self.link_nodes(tuple[2][2], tuple[2][4])
            tuple[2][2].on_hull = True
            self.size += 1

            # update local area
            return self.potential_merges(tuple[2][0].left.left,tuple[2][4].right.right)

    # Input: adjacent nodes a and b already in the hull
    # Postcondition: cut is made (i.e. new concavity describing node inserted into hull) if possible. Returns True or False whether successful
    def cut(self, a, b):
        if self.density_length(a,b):
            # get point c with the shortest perpendicular distance from ab
            # on the positive side (left)
            best_node = None
            best_d = 0

            # iterate over all nodes not already on the hull for minimum perpendicular distance
            for node in [x for x in self.DP if not x.on_hull and self.within_range(a,b,x)]:
                # check if on the positive side. AKA counter clockwise orientation
                # also check if angle is too steep.

                angle = self.get_angle(a,node,b)
                if angle >= 180:

                    # find minimum perpendicular distance
                    d = self.perpendicular_distance(a,b,node)
                    # if best_node == None:
                    #     best_node, best_d = node, d
                    if best_node == None or d < best_d:
                        # check if it crosses the existing hull, or the solution path
                        # checking hull
                        i = self.root
                        j = self.root.right
                        insertable = True
                        while j != self.root:
                            # do not check edges a or b are a part of (they will always intersect)
                            if not (i == a or i == b or j == a or j == b):
                                if self.intersect(a,node,i,j) or self.intersect(node,b,i,j):
                                    insertable = False
                            i = j
                            j = j.right
                            
                        # checking path
                        for node_a,node_b in zip(self.path, self.path[1:]):
                            # do not check edge if any nodes are a part of it (they will always intersect)
                            if (node_a != a and node_a != b and node_b != a and node_b != b):
                                if self.intersect(a,node,node_a,node_b) or self.intersect(node,b,node_a,node_b):
                                    insertable = False

                        # if insertable flag still True insert the node
                        if insertable == True:
                            best_node, best_d = node, d

            if best_node:
                ## Perform the Cut ##
                # insert the new node in between a and b
                best_node.on_hull = True
                self.link_nodes(a,best_node)
                self.link_nodes(best_node, b)
                self.size += 1

                return True
        return False

    # Input: two adjacent nodes a and b already in hull
    # Postcondition: returns True or False whether a cut should be made between a and b
    #                AKA whether a and b pass the density_length condition
    def density_length(self, a, b):
        d = 0
        
        # get min sorted distances from each node not in hull to a and b
        a_heap = []
        b_heap = []
        for node in [x for x in self.DP if not x.on_hull]:
            heapq.heappush(a_heap, a.get_distance(node))
            heapq.heappush(b_heap, b.get_distance(node))

        # calculate the sum of the 3 minimum distances
        # to obtain the average distance d
        d = sum(heapq.nsmallest(3, a_heap))+sum(heapq.nsmallest(3, b_heap))/6

        # test density-length condition
        if 1 * d < a.get_distance(b):
            return True

        return False
    
    # Input: three nodes, a b c
    # Output: Whether the angle abc is counterclockwise
    #           1 = counterclockwise
    #           -1 = clockwise
    #           0 = collinear
    def orientation(self,a,b,c):
        d = (c.y-b.y)*(b.x-a.x) - (b.y-a.y)*(c.x-b.x)
        if d > 0:
            return 1
        if d < 0:
            return -1
        if d == 0:
            return 0
        
    def get_angle(self,a,b,c):
        ang = math.degrees(math.atan2(c.y-b.y, c.x-b.x) - math.atan2(a.y-b.y, a.x-b.x))
        return ang + 360 if ang < 0 else ang   
    
    def within_range(self,node_a,node_b,target):
        # get perpendicular slope
        if (node_b.x-node_a.x) == 0:
            m = 10000
        else:
            m = (node_b.y-node_a.y)/(node_b.x-node_a.x)
            if m == 0:
                m = 0.0001
        m = (m ** -1) * -1

        # get y-intercepts of perpendicular lines through line segment points 
        b1 = node_a.y - node_a.x * m
        b2 = node_b.y - node_b.x * m
        target_b = target.y - target.x * m
        
        if b2 < b1:
            temp = b1
            b1 = b2
            b2 = temp
        # check if target is above line y = mx + b1 and below line y = mx + b2
        if target_b >= b1 and target_b <= b2:
            return True
        
        return False
        
    
    # Input: points a and b of a line segment. point c some distance d from the line
    #        note that all points are given as nodes
    # Output: the perpendicular distance d of c from the line segment ab
    def perpendicular_distance(self,a,b,c):
        if (b.x-a.x) == 0:
            m = 10000
        else:
            m = (b.y-a.y)/(b.x-a.x)
        C = -(b.y-(m*b.x))
        A = -m
        B = 1

        # compute perpendicular distance d
        d = abs(A*c.x + B*c.y + C) / math.sqrt(A*A + B*B)
        return d
    
    # from https://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/
    # Line Segment Intersection Algorithm
    def ccw(self, A,B,C):
        return (C.y-A.y)*(B.x-A.x) > (B.y-A.y)*(C.x-A.x)
    def intersect(self,A,B,C,D):
        return self.ccw(A,C,D) != self.ccw(B,C,D) and self.ccw(A,B,C) != self.ccw(A,B,D)
    
    # Input: points a,b on line ab. points c,d on line cd. All as nodes
    # Output: node at intersection
    # Source: https://www.geeksforgeeks.org/program-for-point-of-intersection-of-two-lines/
    def intersect_point(self,A,B,C,D):
        # Line AB represented as a1x + b1y = c1
        a1 = B.y - A.y
        b1 = A.x - B.x
        c1 = a1*(A.x) + b1*(A.y)
    
        # Line CD represented as a2x + b2y = c2
        a2 = D.y - C.y
        b2 = C.x - D.x
        c2 = a2*(C.x) + b2*(C.y)
    
        determinant = a1*b2 - a2*b1
    
        if (determinant == 0):
            # The lines are parallel.
            return None
        else:
            x = (b2*c1 - b1*c2)/determinant
            y = (a1*c2 - a2*c1)/determinant
            return HullNode(Node(x, y),False)
    
    def get_triangle_area(self,a,b,c):
        return 0.5*abs(a.x*b.y+b.x*c.y+c.x*a.y-a.x*c.y-b.x*a.y-c.x*b.y)

    # Output: list of all nodes in hull. in coord format. ex: [[0,0],[0,1.1],[1,0],[1,1],...,[1,0]] 
    def get_coord_list(self):
        list = []
        i = self.root

        while i != self.root.left:
            list.append([i.x,i.y])
            i = i.right
        list.append([i.x,i.y])
        return list



    ## DEBUGGING TOOLS ##
        # Input: None
    # Output: plots DP and hull onto matplotlib
    def plot(self):
        # plot DP
        for node in self.DP:
            plt.plot(node.x,node.y,'k', marker='.')
        
        # plot solution
        for node_a,node_b in zip(self.path,self.path[1:]):
            self.plot_edge(node_a,node_b,'r')

        # plot convex hull
        i = self.root
        j = self.root.right
        while j != self.root:
            self.plot_edge(i,j,'r')
            i = j
            j = j.right
        self.plot_edge(i,j,'r')

    def plot_edge(self, node_a,node_b,color):
        plt.plot([node_a.x,node_b.x], [node_a.y,node_b.y], color)

class HullSampler():
    # Input: 2d numpy array of points describing a hull. ex: [[0,0],[0,1.1],[1,0],[1,1]]
    def __init__(self, points):
        self.points = np.array(points)
        segments = points
        segments.append(points[0])
        border = Path(segments)
        self.tri = triangulate({'vertices': points, 'segments': segments})
        self.triangles = self.tri['triangles'].tolist()
        self.triangles = [x for x in self.triangles if self.in_hull(x,border)]

        # tri_weights is the percentage area each triangle covers out of the whole polygon
        self.tri_weights = []
        for tri_points in self.points[self.triangles]:
            area = 0.5*abs(tri_points[0][0]*tri_points[1][1]+tri_points[1][0]*tri_points[2][1]+tri_points[2][0]*tri_points[0][1]-tri_points[0][0]*tri_points[2][1]-tri_points[1][0]*tri_points[0][1]-tri_points[2][0]*tri_points[1][1])
            self.tri_weights.append(area.item())

        total_area = sum(self.tri_weights)
        self.tri_weights = [x/total_area for x in self.tri_weights]


    def in_hull(self,points,border):
        x, y = zip(*self.points[points])

        # Formula to calculate centroid 
        x = round(sum(x) / 3, 2)
        y = round(sum(y) / 3, 2)
        if not border.contains_points([(x,y)]):
            return False
        return True

    # Output: a uniformly sampoled random coordinate pair in a list [x,y] from within the hull
    # Source: https://stackoverflow.com/questions/68493050/sample-uniformly-random-points-within-a-triangle
    def sample(self):
        for i in range(1000):
            # select random triangle index weighted proportionally to size and size of whole polygon
            x = random.choices(range(len(self.triangles)), weights=self.tri_weights)     
            triangle = self.points[self.triangles][x][0]
            
            # get the sample
            sample = self.sample_triangle(triangle)
            plt.plot(sample[0],sample[1],'go')
            
        return 
    
    def sample_triangle(self,triangle):
        # transform triangle so a is at origin
        A = triangle[0] - triangle[0]
        B = triangle[1] - triangle[0]
        C = triangle[2] - triangle[0]

        s = random.random()
        t = random.random()
        in_triangle = s + t <= 1
        p = s*B + t*C if in_triangle else (1-s)*B + (1-t)*C
        return p + triangle[0]
    
    def plot(self):
        plt.triplot(self.points[:,0],self.points[:,1],self.triangles)
        plt.plot(self.points[:,0],self.points[:,1], 'ro')


if __name__ == "__main__":
    # test if convex hull can be constructed
    sample_path = [
        Node(15,15),
        Node(14.792803759398225,14.726587764628071),
        Node(13.591207731977605,16.470970960781727),
        Node(10.826754048513582,16.09285688763859),
        Node(6.292029205399618,15.357679270237764),
        Node(5.946866012354862,13.387688820979914),
        Node(3.9209405336170207,9.348790153395093),
        Node(0.4958074266092467,5.854199960436265),
        Node(-0.4973338782958052,4.680164627414598),
        Node(-1.5669402466990903,2.7743168627222694),
        Node(-3.5248253701174193,-1.0810713465399644),
        Node(-5.422623833865456,-4.437354575130508),
        Node(-7.006552287239444,-7.458001010154586),
        Node(-6.101886846904448,-11.310177188582696),
        Node(-9.18638603381256,-15.125514548629493),
        Node(-11.257834136985814,-14.90667494732798),
        Node(-15,-15)]
    
    my_hull = BetterHull(sample_path, 7)
    

    my_hull.plot()

    # array = []
    # with open("../../RRT_Star_Final/src/hulls/map1_hull.json", 'r') as f:
    #     array = json.load(f)
    # my_hull_sampler = HullSampler(array)
    # my_hull_sampler.plot()  
    # my_hull_sampler.sample()

    plt.show()