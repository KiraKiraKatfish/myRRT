import matplotlib.pyplot as plt
import copy
import math
from Node import Node
from KDTree import KDTree
import heapq

global_nodes = []
class Triangle:
    def __init__(self,a,b,c,d=None, e=None):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e

        if d == None or e == None:
            self.is_concave = True
        else:
            self.is_concave = False
        
        if self.b != None:
            self.area = 0.5*abs(a.x*b.y+b.x*c.y+c.x*a.y-a.x*c.y-b.x*a.y-c.x*b.y)
            self.is_null = False
        else:
            self.area = 100000
            self.is_null = True

        # left and right pointers for linked list
        self.left, self.right = None, None

    def __lt__(self, other):
        return self.area < other.area
    
    def __repr__(self):
        return str(self.area)
    
    def __str__(self):
        return self.__repr__()
    
    # Output: list of nodes used in triangle and triangle calculation.
    #         Concave = 3 nodes. Convex = 5 nodes. Null triangle = 4 nodes
    def get_nodes(self):
        if self.is_concave:
            return [self.a,self.b,self.c]
        elif self.is_null:
            return [self.a,self.d,self.e,self.c]
        else:
            return [self.a,self.d,self.e,self.c]



# A concave/convex hull of a given path. Where path is a list of nodes.
class Hull:
    def __init__(self,path, DP=[]):
        self.path = path
        if DP == []:
            self.DP = self.path_to_DP(path)
        else:
            self.DP = DP
        self.tree = KDTree(self.DP)
        self.hull = []

        # self.jarvis_march

        # self.MalevolentShrine(5)

    # Pre-condition: self.DP contains a list of nodes.
    # Output: The convex hull, sorted clockwise stored in self.hull.
    # Time Complexity: O(nh), where n is the # of nodes, h is the # of nodes in the convex hull
    # Reference: https://www.youtube.com/watch?v=nBvCZi34F_o
    def jarvis_march(self):
        # find the leftmost node
        on_hull = self.DP[0]
        for node in self.DP: # O(n)
            if node.x < on_hull.x:
                on_hull = node

        while True:
            self.hull.append(on_hull)
            next_node = self.DP[0]
            for node in self.DP:
                o = self.orientation(on_hull,next_node,node)
                if next_node == on_hull or o == 1 or (o == 0 and on_hull.get_distance(node) > on_hull.get_distance(next_node)):
                    next_node = node
            on_hull = next_node
            if on_hull == self.hull[0]:
                break
    
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

    # Input: a list of nodes forming a path
    # Output: a DP (dot pattern) tracing the path
    # Use-case: to transform a linear path into a DP such that a minimum hull can be calculated
    def path_to_DP(self,path):
        DP = copy.deepcopy(path)
        d = 1
        orientations = [
            (1, 0),
            (.7, .7),
            (0, 1),
            (-.7, .7),
            (-1, 0),
            (.7, -.7),
            (0, -1),
            (-.7, -.7),
        ]

        # add 8 points for each solution node, such that the 8 points encircle the node
        for node in path:
            for x, y in orientations:
                DP.append(Node(node.x + x, node.y + y))
        
        return DP
    
    # Input: None. self.hull should be a convex hull though
    # Output: modifies self.hull to be a concave/convex hull of the DP with specified num edges
    def MalevolentShrine(self, num_edges):
        i = 0
        while(i < len(self.hull)-1):
            c = self.dismantle(self.hull[i],self.hull[i+1])
            if c != None:
                self.hull.insert(i+1,c)
                i -= 1
            i += 1

        # # set linked list pointers for the hull
        # for i in range(len(self.hull-1)):
        #     if i > 0:
        #         self.hull[i].left2 = self.hull[i-1]
        #     self.hull[i].right2 = self.hull[i+1]

        # self.hull[-1].left2 = self.hull[-2]
        # self.hull[-1].right2 = self.hull[0]
        # self.hull[0].left2 = self.hull[-1]

        heap = []
        head, tail = self.construct_triangles(heap, self.hull)

        # passing tail end of the hull, connecting end of hull to start
        head_ex, tail_ex = self.construct_triangles(heap, self.hull[-2:]+self.hull[:2])

        # connecting the head of the triangle hull to the tail
        head.left = tail_ex
        tail_ex.right = head
        tail.right = head_ex
        head_ex.left = tail

        for i in range(0):
            popped = self.pop(heap)
            if popped == None:
                print("Error Popping")
                return
            
            # print("A(%s,%s)B(%s,%s)C(%s,%s)"%(popped.a.x,popped.a.y,popped.b.x,popped.b.y,popped.c.x,popped.c.y))
            
            self.merge(heap, popped)

        # if(popped.is_concave):
        #     plt.plot(popped.a.x,popped.a.y, "yo")
        #     plt.plot(popped.b.x,popped.b.y, "yo")
        #     plt.plot(popped.c.x,popped.c.y, "yo")
        # else:
        #     plt.plot(popped.a.x,popped.a.y, "yo")
        #     plt.plot(popped.b.x,popped.b.y, "yo")
        #     plt.plot(popped.c.x,popped.c.y, "yo")
        #     plt.plot(popped.d.x,popped.d.y, "go")
        #     plt.plot(popped.e.x,popped.e.y, "go")
        self.plot_triangles(heap)
        return
    
    def dismantle(self, a, b):
        if self.density_length(a,b):
            # get point c with the shortest perpendicular distance from ab
            # on the positive side (left)
            best_node = None
            best_d = 0

            for node in self.DP:
                # check if on the positive side
                # AKA counter clockwise orientation
                if self.orientation(a,node,b) == 1 and (self.get_angle(a,node,b) > 20 and self.get_angle(a,node,b) < 340)and not (node.equals(node,a) or node.equals(node,b)):
                    # check if already on the existing hull
                    on_hull = False
                    for hull_node in self.hull:
                        if node.equals(node,hull_node):
                            on_hull = True
                            break

                    # if not on the hull, compare the perpendicular distance to the minimum
                    if on_hull == False:
                        d = self.perpendicular_distance(a,b,node)
                        if best_node == None:
                            best_node, best_d = node, d
                        else:
                            if d < best_d:
                                best_node, best_d = node, d

            if best_node != None:
                # check if ac and bc intersect the hull
                edges = zip(self.hull, self.hull[1:])
                for edge in edges:
                    if edge[0] == a or edge[0] == b or edge[1] == a or edge[1] == b:
                        break
                    if self.intersect(a,best_node,edge[0],edge[1]) or self.intersect(best_node,b,edge[0],edge[1]):
                        return None

            return best_node
        return None

    # Fix later. Very inefficient
    def density_length(self, a, b):
        sum = 0
        
        # make more efficient
        # get the three nearest neighbors for a and b each
        a_neighbors = []
        for neighbor in self.tree.kNearestNeighbors(a, 20):
            in_hull = False
            for solution_node in self.hull:
                if neighbor == solution_node:
                    in_hull = True
            if in_hull == False:    
                a_neighbors.append(neighbor)
        b_neighbors = []
        for neighbor in self.tree.kNearestNeighbors(b, 20):
            in_hull = False
            for solution_node in self.hull:
                if neighbor == solution_node:
                    in_hull = True
            if in_hull == False:    
                b_neighbors.append(neighbor)
        a_neighbors = a_neighbors[:3]
        b_neighbors = b_neighbors[:3]

        # calculate the average distance d
        for neighbor in a_neighbors:
            if neighbor != None:
                sum += a.get_distance(neighbor)
        for neighbor in b_neighbors:
            if neighbor != None:
                sum += b.get_distance(neighbor)
        d = sum / 6

        # test density-length condition
        if 5 * d < a.get_distance(b):
            return True

        return False


    # creates triangles from a list of nodes and adds them to the heap
    # Output: head and tail of constructed triangle linked list
    def construct_triangles(self, heap, nodes):
        head = None
        tail = None
        previous_triangle = None
        previous_angle = None
        tri = None

        angles = []
        groups_of_3 = list(zip(nodes, nodes[1:], nodes[2:]))
        for group in groups_of_3:
            angles.append((self.get_angle(group[0],group[1],group[2]),) + group)


        # iterate over angles checking criteria to make triangles
        for angle in angles:
            # make Concave Triangle
            if angle[0] >= 180:
                tri = Triangle(angle[1],angle[2],angle[3], True)
                tri.left = previous_triangle
                
                # check for root of linked list
                if previous_triangle == None:
                    head = tri
                else:
                    previous_triangle.right = tri
                
                # add to heap and move forward
                heapq.heappush(heap,tri)
                previous_triangle = tri

            # make Convex Triangle
            elif previous_angle != None and angle[0] < 180 and previous_angle[0] < 180:
                new_point = self.intersect_point(previous_angle[1],previous_angle[2],angle[3],angle[2])

                # Convex Triangle additional check (avoids parallel)
                if angle[0] + previous_angle[0] > 180 and new_point != None:
                    tri = Triangle(previous_angle[1],new_point, angle[3], angle[1],angle[2])
                    tri.left = previous_triangle


                # None Triangle
                else:
                    tri = Triangle(previous_angle[1],None, angle[3], angle[1],angle[2])
                    tri.left = previous_triangle
            
                # check for root of linked list
                if previous_triangle == None:
                    head = tri
                else:
                    previous_triangle.right = tri
                
                # add to heap and move forward
                heapq.heappush(heap,tri)
                previous_triangle = tri

            previous_angle = angle

        tail = previous_triangle

        return head, tail

    # Input: heapq heap of triangles
    # Output: Pops triangles until valid triangle found and returns triangle
    #         returns None in case of error
    def pop(self, heap):
        # Edge Case: heap is empty
        if not heap:
            return None

        popped = heapq.heappop(heap)
        while(heap and popped.is_null):
            popped = heapq.heappop(heap)
        
        # Edge Case: final popped triangle is null
        if not heap and popped.is_null:
            return None
        
        return popped
        
    def merge(self, heap, triangle):
        if triangle.is_concave:
            self.merge_concave(heap, triangle)
        else:
            self.merge_convex(heap, triangle)
        

    def merge_concave(self, heap, triangle):
        self.hull.remove(triangle.b)

        #list of all nodes that must be reevaluated for triangles, excluding the node removed in the merge
        nodes = triangle.left.get_nodes() + triangle.right.get_nodes()
        nodes = list(filter((triangle.b).__ne__,nodes))
        nodes_no_repeat = []
        nodes_no_repeat =  
        
        head, tail = self.construct_triangles(heap, nodes_no_repeat)
        # insert new triangles into linked list, replacing old
        triangle.left.left.right = head
        head.left = triangle.left.left
        triangle.right.right.left = tail
        tail.right = triangle.right.right

        # mark old triangles as null
        triangle.left.is_null, triangle.is_null, triangle.right.is_null = True,True,True

        return
    
    def merge_convex(self, heap, triangle):
        # replace obsolete nodes with new node, triangle.b
        self.hull = [triangle.b if x==triangle.d else x for x in self.hull]
        self.hull.remove(triangle.e)

        #list of all nodes that must be reevaluated for triangles, excluding the node removed in the merge
        nodes = triangle.left.get_nodes() + [triangle.b] + triangle.right.get_nodes()
        nodes = list(filter((triangle.d).__ne__,nodes))
        nodes = list(filter((triangle.e).__ne__,nodes))
        nodes_no_repeat = []
        nodes_no_repeat = [nodes_no_repeat.append(x) for x in nodes if x not in nodes_no_repeat]

        global global_nodes
        global_nodes = list(filter((triangle.d).__ne__,list(filter((triangle.e).__ne__,triangle.right.get_nodes()))))

        head, tail = self.construct_triangles(heap, nodes_no_repeat)
        # insert new triangles into linked list, replacing old
        triangle.left.left.right = head
        head.left = triangle.left.left
        triangle.right.right.left = tail
        tail.right = triangle.right.right

        # mark old triangles as null
        triangle.left.is_null, triangle.is_null, triangle.right.is_null = True,True,True

        return


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
            return Node(x, y)

    # Input: points a and b of a line segment. point c some distance d from the line
    #        note that all points are given as nodes
    # Output: the perpendicular distance d of c from the line segment ab
    def perpendicular_distance(self,a,b,c):
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

    # Input: None
    # Output: plots DP and hull onto matplotlib
    def plot(self):
        # plot DP
        for node in self.DP:
            plt.plot(node.x,node.y,'k', marker='.')

        # plot solution over DP
        for node in self.path:
            plt.plot(node.x, node.y, 'k','.')

        # plot convex hull
        for node_a, node_b in zip(self.hull, self.hull[1:]):
            self.plot_edge(node_a,node_b,'r')
            self.plot_edge(self.hull[0], self.hull[-1], 'r')

    def plot_edge(self, node_a,node_b,color):
        plt.plot([node_a.x,node_b.x], [node_a.y,node_b.y], color)

    def plot_triangles(self, triangles):
        for triangle in triangles:
            if not triangle.is_null:
                if triangle.is_concave:
                    self.plot_edge(triangle.c, triangle.a, 'g')

                else: 
                    self.plot_edge(triangle.a, triangle.b, 'g')
                    self.plot_edge(triangle.b, triangle.c, 'g')

    
if __name__ == "__main__":
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
    
    sample_path_2 = [
        Node(15,15),
        Node(15.50036155216836,14.94114900352417),
        Node(13.33348443361573,13.667140125438479),
        Node(9.634273316374909,10.97259813728816),
        Node(6.1204777436375295,8.605073783632939),
        Node(3.2748035650812355,6.717479003141786),
        Node(-0.7374655040179761,4.192861313652418),
        Node(-4.497993997774522,1.2490354083806565),
        Node(-6.670729620624504,-0.657519069782609),
        Node(-9.39596042050078,-4.723250351660834),
        Node(-10.436525601500888,-6.473596798505037),
        Node(-12.369639756247805,-9.835925197531118),
        Node(-14.18999550649021,-13.412805852326542),
        Node(-15,-15)
    ]

    sample_DP_2 = [
        Node(15.50036155216836,14.94114900352417),
        Node(13.747162469569119,15.167002876373658),
        Node(15,15),
        Node(14.799943843967327,16.144402487896407),
        Node(15.270944623193913,16.250968914437294),
        Node(15.430294279493431,16.76931896505554),
        Node(15.99203903973418,15.903225731630506),
        Node(14.14995210903961,14.13709186656223),
        Node(13.403243761789419,14.503579350671274),
        Node(14.7738204555394,14.242836276188363),
        Node(13.327177472427834,14.88666404031585),
        Node(13.115701044812013,14.84656561717005),
        Node(15.881559941567296,13.399077449291106),
        Node(16.253256517422116,15.28190585806091),
        Node(16.170404295943392,13.056727946139588),
        Node(15.50036155216836,14.94114900352417),
        Node(15.486780716401466,16.941102893217597),
        Node(15.99203903973418,15.903225731630506),
        Node(13.747162469569119,15.167002876373658),
        Node(15,15),
        Node(15.270944623193913,16.250968914437294),
        Node(15.430294279493431,16.76931896505554),
        Node(14.799943843967327,16.144402487896407),
        Node(14.14995210903961,14.13709186656223),
        Node(14.7738204555394,14.242836276188363),
        Node(15.881559941567296,13.399077449291106),
        Node(16.253256517422116,15.28190585806091),
        Node(12.060765152346386,12.73419459053012),
        Node(13.494705736700013,12.802681942605084),
        Node(12.748422613304314,14.705265210196131),
        Node(14.14995210903961,14.13709186656223),
        Node(13.33348443361573,13.667140125438479),
        Node(13.403243761789419,14.503579350671274),
        Node(13.327177472427834,14.88666404031585),
        Node(13.115701044812013,14.84656561717005),
        Node(14.7738204555394,14.242836276188363),
        Node(13.747162469569119,15.167002876373658),
        Node(11.478835564264006,13.359808439168646),
        Node(13.344693203641647,11.90893630073155),
        Node(13.854526285379151,12.333448439371246),
        Node(11.812509481240589,12.667297540311743),
        Node(8.445399501162402,10.219164214047213),
        Node(9.750499382583369,11.734655652332162),
        Node(9.178357233222705,11.504309913162437),
        Node(10.588693269501654,10.45152709159209),
        Node(10.378358393171212,10.890657330878714),
        Node(10.647929308935051,11.423072428618859),
        Node(10.2341902348469,11.436325532264874),
        Node(9.634273316374909,10.97259813728816),
        Node(10.600809163802118,11.599168848572006),
        Node(10.903928297422745,11.053793893865517),
        Node(8.549729439832742,10.840302148357459),
        Node(7.788951299257917,10.938927370516566),
        Node(10.16532330183436,12.095993845209698),
        Node(9.643312740789831,11.974826510998753),
        Node(8.611324781611845,12.035966332878232),
        Node(11.34412788671274,11.800628298675125),
        Node(11.021354120849441,11.97485112952922),
        Node(10.229171832661144,9.314644303056003),
        Node(9.935021974687753,9.326713542264788),
        Node(8.50072515166245,9.46020107013787),
        Node(9.56962329544293,10.169075797440659),
        Node(10.583286290789339,9.919097521105606),
        Node(5.840355743570488,7.403371993215089),
        Node(6.726820191743896,9.196185642796275),
        Node(4.65013455770919,8.926213758122131),
        Node(4.391304165375281,8.507262398888301),
        Node(6.65172295865797,7.874749423275233),
        Node(5.579228552178471,7.9834711291877305),
        Node(6.1204777436375295,8.605073783632939),
        Node(5.004366972001279,8.5482875352705),
        Node(5.373734984650454,7.4844627568962),
        Node(4.34464148316728,9.184987731999506),
        Node(4.970694127139726,9.629669319899318),
        Node(7.919394385838704,9.033420780056183),
        Node(7.333258950531931,7.7470888856895925),
        Node(7.279003478850669,7.6296654584352765),
        Node(7.295555009785126,10.185611792090718),
        Node(5.239816504380119,7.390515152568181),
        Node(4.836172022764025,7.3463937008002205),
        Node(7.285825243695481,7.0706460200644905),
        Node(2.998869791104172,6.796405612138492),
        Node(4.9985435961302915,6.8325258764282415),
        Node(3.977787264544645,6.244388137120286),
        Node(3.1632535428923703,6.476967260537162),
        Node(3.2748035650812355,6.717479003141786),
        Node(5.140279316490005,6.508666594622458),
        Node(4.578359641504363,5.494064437117618),
        Node(4.438628056414071,6.123880618558783),
        Node(3.830734826220599,5.071690490488287),
        Node(4.858584151100818,5.609468874472199),
        Node(1.9127582953474302,6.982480058977984),
        Node(2.242445823825051,5.134841150123847),
        Node(4.836172022764025,7.3463937008002205),
        Node(3.330442112341675,8.618369719953787),
        Node(2.281770300224352,8.126283456603495),
        Node(2.446109648182979,7.490014427961853),
        Node(-0.7374655040179761,4.192861313652418),
        Node(-1.1977491142933943,4.251247039484376),
        Node(-1.2937507083495632,3.1338770186000744),
        Node(0.30483692420979835,2.824404305157273),
        Node(-1.1737546699911974,2.7754116255677665),
        Node(-0.6583705302445537,2.7692623964824),
        Node(-1.1563443302145568,5.242248891451616),
        Node(0.6507594146611666,4.914744102280647),
        Node(-1.2679016637569553,5.559210288232052),
        Node(-2.5663722271951173,4.8136645971422425),
        Node(-3.321623469066669,2.5037411355288626),
        Node(-4.497993997774522,1.2490354083806565),
        Node(-3.95438451948392,1.7701849266334158),
        Node(-4.3886305920858035,2.1662268026648164),
        Node(-4.396222505254981,2.2026156579124248),
        Node(-5.3580301033365565,2.7521938158388046),
        Node(-4.8960598272120315,0.7430803504388841),
        Node(-4.5786036020620635,-0.1366047454234689),
        Node(-5.06509088582909,-0.18601151660055493),
        Node(-5.198681954943121,-0.07325630052502063),
        Node(-3.1098085006329192,2.528029337555772),
        Node(-5.68811817404522,-0.23994153667119633),
        Node(-2.6866627606022853,1.8868144134141929),
        Node(-6.216151635874147,-2.605173776289978),
        Node(-6.670729620624504,-0.657519069782609),
        Node(-7.147086244126404,1.2849238166997374),
        Node(-6.751379903784688,0.7976040580800685),
        Node(-6.6431938138838476,0.3166156577920276),
        Node(-6.683138240272735,0.504551119478144),
        Node(-6.445334195957688,-0.2763504228182114),
        Node(-7.872232086425459,0.6286920560637341),
        Node(-7.83867522718452,-0.055798881450421334),
        Node(-7.293168649780885,-0.3297594370254302),
        Node(-7.690049829318056,0.9585057300844753),
        Node(-8.260189396380886,-0.39053352682926956),
        Node(-8.298011343734672,0.1369378853115606),
        Node(-6.719692865882907,-1.2853817529283695),
        Node(-8.547588179427077,-1.3016328575814669),
        Node(-6.157289613538474,-0.4467982050294417),
        Node(-5.68811817404522,-0.23994153667119633),
        Node(-5.538904802949354,-0.5097919202297909),
        Node(-5.06509088582909,-0.18601151660055493),
        Node(-5.198681954943121,-0.07325630052502063),
        Node(-9.424015739954202,-4.9413504985229455),
        Node(-7.967811961473677,-3.570412660567102),
        Node(-7.720699835746437,-4.780434162058738),
        Node(-8.040647599432095,-5.207305655610387),
        Node(-9.39596042050078,-4.723250351660834),
        Node(-9.269991146274691,-4.197739363363361),
        Node(-9.00871885380143,-4.980756387024723),
        Node(-8.897737436843371,-3.7556362163501156),
        Node(-8.545490655987429,-5.403069182629512),
        Node(-9.325125420870023,-5.423063550486585),
        Node(-8.546820154769268,-3.0440037006548764),
        Node(-7.901442812192272,-3.5184569779845987),
        Node(-10.153759004225083,-3.5568951481340925),
        Node(-10.353925306247449,-4.188989255918463),
        Node(-11.12342814421601,-3.886837587155284),
        Node(-10.662909397366398,-7.63289501463347),
        Node(-10.436525601500888,-6.473596798505037),
        Node(-10.716359698817413,-6.358254738609311),
        Node(-10.419502127045174,-6.619879909073237),
        Node(-11.463213132556431,-7.284704376018553),
        Node(-11.230251336591435,-6.202989961150745),
        Node(-11.567500224029192,-5.43125355925072),
        Node(-8.822976136597063,-6.848901649920017),
        Node(-9.424015739954202,-4.9413504985229455),
        Node(-10.100342503827427,-6.7289284494095725),
        Node(-9.325125420870023,-5.423063550486585),
        Node(-8.743163270161673,-7.20389367736554),
        Node(-9.104205077097518,-7.777758101867885),
        Node(-9.415643950848365,-7.49540366882654),
        Node(-12.369639756247805,-9.835925197531118),
        Node(-12.851154905027883,-7.9157105656020565),
        Node(-11.595625868708414,-9.826856924431041),
        Node(-12.176261019726677,-8.324002791618522),
        Node(-12.927565896508542,-9.450203696330597),
        Node(-11.333078013342393,-11.244034988233427),
        Node(-11.017054861619178,-10.275103746639935),
        Node(-13.295917865798152,-10.60936427750141),
        Node(-11.757176416710804,-10.517959599141573),
        Node(-12.961627929551636,-10.218063139421396),
        Node(-12.078528891322193,-9.941376634341573),
        Node(-12.571744880807557,-10.053306292447445),
        Node(-12.940400324187497,-10.335012000496647),
        Node(-11.166420802516633,-11.222726842646328),
        Node(-10.939324814452007,-10.883665303905836),
        Node(-14.219450239227296,-9.461047499981149),
        Node(-15,-15),
        Node(-13.76616753852998,-13.425942359053254),
        Node(-14.187602826609535,-12.682519095733786),
        Node(-14.18999550649021,-13.412805852326542),
        Node(-14.384414021249526,-11.496685427721062),
        Node(-13.665979401466263,-12.529355528063352),
        Node(-14.953579097978572,-13.264881447726221),
        Node(-14.629041675364522,-12.258265544422056),
        Node(-12.532654046417075,-12.462560214577337),
        Node(-13.126102914428039,-11.738650280616657),
        Node(-14.472789679298188,-13.899833004290008),
        Node(-13.69168892203116,-13.708588812994492),
        Node(-13.691499335229945,-14.598003125811555),
        Node(-14.649582310338696,-14.422779861376164),
        Node(-14.938588248923544,-15.166574271028775),
        Node(-13.189944946267001,-13.567421570317283),
        Node(-13.308461319018527,-14.549303799569806),
        Node(-13.311233457577284,-14.992926376760334),
        Node(-15.332837399750613,-14.701181941200288),
        Node(-15.47054857737367,-13.803209240874388),
        Node(-15,-15),
        Node(-14.472789679298188,-13.899833004290008),
        Node(-13.576876774340203,-15.508274661972035),
        Node(-14.942156406079237,-15.27809850997453),
        Node(-14.99314616152278,-16.099268867996443),
        Node(-13.691499335229945,-14.598003125811555),
        Node(-14.795060909609678,-16.814450237211226),
        Node(-14.938588248923544,-15.166574271028775),
        Node(-14.028443414603116,-15.779774076737425),
        Node(-14.649582310338696,-14.422779861376164),
        Node(-13.69168892203116,-13.708588812994492),
        Node(-13.308461319018527,-14.549303799569806),
        Node(-13.311233457577284,-14.992926376760334),
        Node(-13.488390962313247,-16.232933884065037),
        Node(-14.953579097978572,-13.264881447726221),
        Node(-14.18999550649021,-13.412805852326542),
        Node(-16.063347543143827,-14.689890072902436),
        Node(-15.332837399750613,-14.701181941200288),
        Node(-15.719554488588777,-15.582081022778556),
        Node(-15.47054857737367,-13.803209240874388),
        Node(-16.715402469435723,-14.3773694707801),
        Node(-16.512005092826612,-13.851941136153947),
        Node(-16.203237872649897,-13.481952456800514)
    ]
    
    sample_path_3 = [
        Node(15,15),
        Node(14.762709798723883,15.503853150695917),
        Node(14.398734674064272,10.904557674432414),
        Node(14.144814698888133,7.8487941026778465),
        Node(13.967982829248221,2.989917291753109),
        Node(13.391070969391187,-1.7644248013484578),
        Node(13.150548754569094,-6.2075086787215294),
        Node(12.818092330460665,-8.476388705262266),
        Node(12.649255281829582,-12.291454371005056),
        Node(12.360860587006506,-15.356249730846177),
        Node(12.092406190563032,-16.164435440626583),
        Node(9.219761340017996,-16.897491764565224),
        Node(5.674608372316857,-17.78043218619208),
        Node(3.7302607232948723,-17.53677207297929),
        Node(-0.7356193361352581,-16.977417341304463),
        Node(-4.3664888509959034,-16.493265009265997),
        Node(-8.236674656146272,-15.925178123224999),
        Node(-10.253942609236834,-15.642090000028768),
        Node(-15,-15)]
    sample_DP_3 = [
        Node(16.38524890300937,14.539126044248905),
        Node(14.368937691814352,15.17104371969537),
        Node(16.3331829791277,14.898048540796516),
        Node(15,15),
        Node(15.893899922247535,14.513015749357429),
        Node(13.162732788011823,15.129880705201238),
        Node(13.692410228792099,14.572260213598028),
        Node(13.21891621042159,14.862541783867762),
        Node(13.272868202405874,14.931396480821341),
        Node(13.539051944268273,14.61308197875919),
        Node(15.414982889861875,14.318193090190952),
        Node(15.720106535642095,15.284569158868536),
        Node(16.507120974053677,14.758698991215532),
        Node(16.395747624299744,14.401219868729783),
        Node(14.42242446428347,14.155302878272227),
        Node(15.65191214689294,13.572078275963875),
        Node(15.21107850761269,13.205736641773655),
        Node(15.010490493723992,13.382565453988917),
        Node(15.900385238451221,15.49458282493022),
        Node(13.874388838603593,15.417543294413903),
        Node(13.934010240002685,15.375935076026657),
        Node(15.29713235876217,15.47673289015075),
        Node(13.84505434651345,15.577845053690403),
        Node(14.762709798723883,15.503853150695917),
        Node(14.30814445627084,16.152035228831167),
        Node(16.66221825799856,15.80716569199),
        Node(16.64025919732412,15.679452041915475),
        Node(16.119702335284586,15.787654710929928),
        Node(14.794130556921651,16.14870519838601),
        Node(15.597921712548057,15.91615366522214),
        Node(15.083067040898207,15.876832097783485),
        Node(15.205476226395518,16.432501788048974),
        Node(14.435211785126306,15.9805859122975),
        Node(14.556756914694681,16.514834808285272),
        Node(16.19107550312917,16.564754307866934),
        Node(15.471465004574192,16.63352989794791),
        Node(15.63993689653028,16.65432992454143),
        Node(13.84586538186521,15.662427576780573),
        Node(13.659715451129273,15.672306020549172),
        Node(14.10860300239397,15.985299468560463),
        Node(15.900385238451221,15.49458282493022),
        Node(13.84505434651345,15.577845053690403),
        Node(14.762709798723883,15.503853150695917),
        Node(13.874388838603593,15.417543294413903),
        Node(13.934010240002685,15.375935076026657),
        Node(15.29713235876217,15.47673289015075),
        Node(14.30814445627084,16.152035228831167),
        Node(16.66221825799856,15.80716569199),
        Node(16.64025919732412,15.679452041915475),
        Node(16.119702335284586,15.787654710929928),
        Node(14.794130556921651,16.14870519838601),
        Node(14.435211785126306,15.9805859122975),
        Node(15.597921712548057,15.91615366522214),
        Node(15.083067040898207,15.876832097783485),
        Node(15.205476226395518,16.432501788048974),
        Node(14.556756914694681,16.514834808285272),
        Node(16.19107550312917,16.564754307866934),
        Node(15.471465004574192,16.63352989794791),
        Node(14.564269551348616,17.145350574802414),
        Node(15.63993689653028,16.65432992454143),
        Node(13.84586538186521,15.662427576780573),
        Node(13.659715451129273,15.672306020549172),
        Node(12.891411041779754,15.7856186200543),
        Node(13.55148448819078,16.740985572585494),
        Node(14.10860300239397,15.985299468560463),
        Node(13.981531459571734,16.891965771385337),
        Node(14.304406852715019,17.389470959098155),
        Node(14.242174020935025,17.09419832961381),
        Node(16.38524890300937,14.539126044248905),
        Node(15.720106535642095,15.284569158868536),
        Node(14.368937691814352,15.17104371969537),
        Node(16.3331829791277,14.898048540796516),
        Node(15,15),
        Node(15.893899922247535,14.513015749357429),
        Node(13.162732788011823,15.129880705201238),
        Node(13.692410228792099,14.572260213598028),
        Node(13.21891621042159,14.862541783867762),
        Node(13.272868202405874,14.931396480821341),
        Node(13.539051944268273,14.61308197875919),
        Node(15.414982889861875,14.318193090190952),
        Node(16.507120974053677,14.758698991215532),
        Node(16.395747624299744,14.401219868729783),
        Node(14.42242446428347,14.155302878272227),
        Node(13.927102130226451,11.228024735677916),
        Node(13.971525643321314,10.52036921705676),
        Node(14.398734674064272,10.904557674432414),
        Node(14.807551766453663,10.524538798063546),
        Node(14.166430362999435,10.177011220522878),
        Node(15.340278195719321,10.475156805336333),
        Node(14.707646157565549,10.440339447108702),
        Node(14.397704757403233,9.81288957291595),
        Node(14.935780568262842,9.244407045300889),
        Node(13.808635358165454,10.217852265149698),
        Node(12.532278213804908,11.215533638343569),
        Node(13.195601420337802,11.079471366331326),
        Node(13.217954145619409,10.997341102126082),
        Node(12.97863383124087,11.662201085169663),
        Node(13.061929125622193,11.456982912164719),
        Node(13.226960652703532,11.431737444218776),
        Node(13.733135990051252,9.53961910235687),
        Node(15.877498067986565,10.641378925221815),
        Node(15.651911773269617,11.740258501974882),
        Node(15.399741036125874,9.75434392604674),
        Node(15.211020164076295,11.926871710320587),
        Node(13.955550859502921,12.342670374714999),
        Node(13.447989546937883,12.41812040561512),
        Node(13.961073083900047,12.752996784102855),
        Node(12.325263982035793,7.257026185592709),
        Node(15.350610699005227,7.543290268234595),
        Node(12.990655800463443,8.481302822684516),
        Node(12.586921256256488,8.106831782099334),
        Node(13.407740332941408,8.148219437012706),
        Node(14.513031440351845,7.2836749215140095),
        Node(12.762167754946468,7.607337178831358),
        Node(14.144814698888133,7.8487941026778465),
        Node(14.094363025404697,7.564718726907724),
        Node(14.923853655673852,7.974881476819089),
        Node(15.165917678846213,7.903960107922387),
        Node(13.17212926552974,8.355440059238607),
        Node(12.51152464230966,7.5373108607637995),
        Node(14.091898604283202,8.622085319408448),
        Node(14.54341612401754,8.876449802977945),
        Node(14.397704757403233,9.81288957291595),
        Node(14.935780568262842,9.244407045300889),
        Node(13.245316883970403,9.223001963785048),
        Node(13.733135990051252,9.53961910235687),
        Node(15.356513092373511,8.106280842484193),
        Node(15.723822538237954,7.40500025128236),
        Node(15.809803001957391,8.59558753981899),
        Node(13.960447096303895,6.105428954433972),
        Node(14.86316462111165,6.677960069673343),
        Node(14.37358431250393,6.996357542936991),
        Node(14.491108980759961,6.226584517260164),
        Node(14.830458761503408,6.046618015433751),
        Node(14.479092535763002,6.013164380091538),
        Node(14.003957872883596,6.940732974168668),
        Node(13.855938373129455,6.770047689461414),
        Node(12.819355226394919,7.081991289458479),
        Node(13.226453804007086,6.71592524280959),
        Node(14.347958354337829,4.1433293073984405),
        Node(14.19006924634617,3.569023827684074),
        Node(14.066851933569751,1.7353295539974098),
        Node(13.967982829248221,2.989917291753109),
        Node(13.988746636735748,1.9275197725752058),
        Node(14.167923878481126,1.9407599374782905),
        Node(14.11588292491922,1.8663870844801451),
        Node(14.35220286592385,3.3517360428323606),
        Node(14.764241027611604,3.9604504851591535),
        Node(15.144946988536908,2.1038893380701573),
        Node(15.680290070215065,2.992168912378826),
        Node(15.29001812128125,2.490831249753029),
        Node(15.661879685042244,3.1261373307564178),
        Node(15.516959553119435,3.940107383564083),
        Node(14.953061293910672,4.145041471409403),
        Node(14.642121222994284,4.237074879403444),
        Node(14.961801515662053,4.414815605484467),
        Node(12.672152081754968,3.0516913927161324),
        Node(12.864812587576921,1.7998597590763623),
        Node(13.64274160465699,1.1326207173982965),
        Node(13.645937788748476,1.7247411964365078),
        Node(13.71709157719392,2.1137103009296645),
        Node(13.623786798946533,1.9192405879207008),
        Node(13.488138142015508,2.2396578050006255),
        Node(13.180871214034681,2.606947303992932),
        Node(12.387094060720145,1.7854192216794402),
        Node(12.70320482429382,2.904496736113721),
        Node(12.685931531642673,2.763847586271204),
        Node(12.974639743799216,4.317149049222504),
        Node(12.963331671018487,3.27686082744982),
        Node(12.172812974142012,3.2281168916028236),
        Node(13.291448143711463,3.7726401134737273),
        Node(13.157943145516008,3.737927544329473),
        Node(12.83631131898425,3.7375091769278157),
        Node(13.18562885781381,3.897945288498768),
        Node(12.123406618941658,3.5935298985953814),
        Node(13.212254368076934,4.644692991237754),
        Node(13.43594211434008,4.8808626377421405),
        Node(13.150293487995155,-1.079927112016375),
        Node(13.414654834940983,-2.708800239304768),
        Node(13.391070969391187,-1.7644248013484578),
        Node(13.231799784273115,-2.496850816155984),
        Node(13.243463083283551,-2.1581603011871664),
        Node(13.25202125777502,-1.7054119328138562),
        Node(13.082537627825552,-2.055045198202002),
        Node(13.23232324362192,-3.5879523794598747),
        Node(13.728616957878572,-1.8663208922210544),
        Node(13.779766470222143,-1.654510022390351),
        Node(13.885190230189728,-3.1059495636682932),
        Node(13.887349464219099,-3.003836291451279),
        Node(12.97302553556154,-3.602916548153125),
        Node(12.973385872753425,-3.40778823078573),
        Node(13.486774982958934,-1.0653396217048652),
        Node(13.7615745702307,-0.0039244150615758144),
        Node(12.385092382537096,-0.2882247677399441),
        Node(12.789901307712299,-2.7697188537808906),
        Node(12.837868265104973,-2.056122990134874),
        Node(12.10015665385066,-0.9155255892306293),
        Node(12.771502826720138,-3.2117466203547274),
        Node(12.344253210285096,-0.7036485038693776),
        Node(12.781980821971644,-0.07465347687248425),
        Node(15.076815663921122,-1.6170605271615126),
        Node(15.054888768055584,-2.0047388245200928),
        Node(14.55848850062813,-0.16816618348600088),
        Node(14.546887992475746,-2.008756874453013),
        Node(14.435103451764853,-1.5386947537290574),
        Node(14.735077184739943,-1.4902646661286525),
        Node(14.658895865749372,-0.6046279591617747),
        Node(15.30058306600965,-2.024689185742446),
        Node(13.03309063899544,-5.682115654845742),
        Node(13.704636270058984,-7.486962795441382),
        Node(13.458043415086436,-5.232967977440147),
        Node(13.177148431455016,-7.464428696078471),
        Node(13.375076581651236,-4.665229036848203),
        Node(13.365504132612777,-7.095045592214909),
        Node(13.150548754569094,-6.2075086787215294),
        Node(13.275905476827475,-6.7759703168791585),
        Node(13.561162252422918,-6.930067152123428),
        Node(13.572791221685236,-5.913647525435755),
        Node(13.605617756610243,-5.965872870437465),
        Node(13.5198899637804,-6.511267533727221),
        Node(13.806719147679615,-4.796071943843261),
        Node(13.946134263124215,-5.106724324805612),
        Node(13.548882119526631,-7.987466415359279),
        Node(13.15413672514724,-7.634187897904905),
        Node(13.733198507491139,-7.679054045188938),
        Node(12.9415662498592,-7.042421140506541),
        Node(12.986232730350224,-6.785671789540988),
        Node(12.990743238889507,-4.521722608076285),
        Node(12.85151468500311,-7.309822768362512),
        Node(12.832613991855666,-6.834396462942394),
        Node(12.64442004475584,-6.6415308839716225),
        Node(14.391049499286199,-4.983509942800439),
        Node(14.050574493202028,-5.935464147866778),
        Node(13.977168686503951,-4.966961033700642),
        Node(14.124603459708283,-5.0067228111281015),
        Node(14.309596377660995,-5.254529650768301),
        Node(14.149133431883037,-6.5612004567562785),
        Node(14.23498510367849,-5.247458143343366),
        Node(14.317374463471587,-4.96607142895639),
        Node(14.64832706969031,-6.966892974836097),
        Node(14.697804577944488,-6.103631307146351),
        Node(15.053887863988976,-6.700307391865369),
        Node(14.464986401637226,-6.513199172207425),
        Node(14.577959963500327,-5.999016748540335),
        Node(14.69057505961949,-7.097867836002889),
        Node(12.85151468500311,-7.309822768362512),
        Node(12.832613991855666,-6.834396462942394),
        Node(12.818092330460665,-8.476388705262266),
        Node(12.572283365281585,-8.20763719619952),
        Node(12.702463785142363,-9.005294849905576),
        Node(12.64442004475584,-6.6415308839716225),
        Node(12.682581792538748,-8.91412396130255),
        Node(12.572374026841985,-9.933810448731727),
        Node(12.781618688567853,-9.573278446870974),
        Node(12.560407080141964,-10.107984667300718),
        Node(12.9415662498592,-7.042421140506541),
        Node(12.986232730350224,-6.785671789540988),
        Node(13.704636270058984,-7.486962795441382),
        Node(13.548882119526631,-7.987466415359279),
        Node(13.08565627575154,-8.278969914399088),
        Node(13.443357915429559,-9.666690133819333),
        Node(13.15413672514724,-7.634187897904905),
        Node(13.733198507491139,-7.679054045188938),
        Node(13.177148431455016,-7.464428696078471),
        Node(13.365504132612777,-7.095045592214909),
        Node(13.275905476827475,-6.7759703168791585),
        Node(13.561162252422918,-6.930067152123428),
        Node(13.99759148966077,-8.036624971532863),
        Node(13.984332092462829,-10.036581018146375),
        Node(14.012717450424155,-8.809564396406682),
        Node(13.995573141264515,-8.394453947984832),
        Node(14.359547551657712,-9.316895873322096),
        Node(14.163048058908416,-8.849427758340283),
        Node(14.435279794988702,-8.32889960875777),
        Node(14.468288083443156,-9.012640157374264),
        Node(14.598993934466321,-9.080947154211533),
        Node(13.090636120907476,-12.123223975737186),
        Node(13.863712242940657,-12.472233796756855),
        Node(12.940707876796942,-12.432476160057648),
        Node(12.649255281829582,-12.291454371005056),
        Node(13.799369690489762,-12.611412415320654),
        Node(12.459345700268237,-10.589703630284113),
        Node(12.904436488320606,-11.499192630282291),
        Node(13.772429983518336,-11.071024701477633),
        Node(13.197424394871334,-12.007178594972988),
        Node(13.57285554077692,-11.485115313914038),
        Node(13.382096095449,-11.351900830871502),
        Node(13.600440873699114,-10.686625725628364),
        Node(14.29561843601806,-11.865670860920625),
        Node(13.615588732645577,-12.847808421376396),
        Node(13.383031972740682,-12.756860305356623),
        Node(12.417607142660131,-13.295776196336316),
        Node(13.57088556151443,-13.272979123207174),
        Node(14.428392338749937,-13.08575703993052),
        Node(13.902522682670536,-13.653321628581935),
        Node(12.530146556458263,-13.617825869511368),
        Node(13.48411239235017,-13.913660533209086),
        Node(12.736415726827701,-13.898518157281092),
        Node(13.965924601153986,-13.451859117163064),
        Node(12.95742399455743,-14.232565333275158),
        Node(12.862755403659998,-15.275259370006738),
        Node(13.10745199349207,-15.409488366885661),
        Node(12.360860587006506,-15.356249730846177),
        Node(14.327551065966773,-15.505174364022656),
        Node(13.249667350137557,-15.262253059568206),
        Node(13.274442035020137,-15.116144674553041),
        Node(12.69452120513305,-14.59104715459372),
        Node(14.03987610835511,-14.708532937751526),
        Node(11.246793070545028,-16.453675993257455),
        Node(14.024043836323152,-16.25950362732848),
        Node(10.555611148153702,-16.133048147577732),
        Node(12.092406190563032,-16.164435440626583),
        Node(11.012785961934313,-16.049333143740515),
        Node(11.25124651807393,-15.94576836472255),
        Node(12.376089331990563,-16.429631125671214),
        Node(11.341056461924182,-16.188961155846258),
        Node(11.012539455069785,-16.27599029641242),
        Node(13.453066652116036,-16.174886645078516),
        Node(11.418925469086325,-16.79081881525597),
        Node(12.897413402493164,-16.76835638293936),
        Node(11.946699147540624,-16.714323098005032),
        Node(11.009664302934766,-16.669509402754038),
        Node(12.00514091184806,-17.067487631174068),
        Node(12.95742399455743,-14.232565333275158),
        Node(12.839835103630094,-14.33945707110789),
        Node(12.647809071216301,-14.569280087387298),
        Node(13.48411239235017,-13.913660533209086),
        Node(12.736415726827701,-13.898518157281092),
        Node(12.530146556458263,-13.617825869511368),
        Node(11.246793070545028,-16.453675993257455),
        Node(14.024043836323152,-16.25950362732848),
        Node(10.555611148153702,-16.133048147577732),
        Node(12.092406190563032,-16.164435440626583),
        Node(11.012785961934313,-16.049333143740515),
        Node(11.25124651807393,-15.94576836472255),
        Node(12.376089331990563,-16.429631125671214),
        Node(11.341056461924182,-16.188961155846258),
        Node(11.012539455069785,-16.27599029641242),
        Node(13.453066652116036,-16.174886645078516),
        Node(10.509475137097482,-16.267328573738098),
        Node(11.418925469086325,-16.79081881525597),
        Node(12.897413402493164,-16.76835638293936),
        Node(11.946699147540624,-16.714323098005032),
        Node(11.009664302934766,-16.669509402754038),
        Node(10.437880019415125,-16.941917002846694),
        Node(12.00514091184806,-17.067487631174068),
        Node(11.40045420583343,-17.265437623000924),
        Node(12.931392221025085,-17.31052955047376),
        Node(10.920393356211747,-17.290763320335696),
        Node(13.150237257727781,-17.64804841882288),
        Node(13.015554733345581,-17.6208657497913),
        Node(12.157718891612049,-17.55863766584345),
        Node(12.69334607240004,-17.967470090610526),
        Node(12.862755403659998,-15.275259370006738),
        Node(13.10745199349207,-15.409488366885661),
        Node(12.360860587006506,-15.356249730846177),
        Node(13.249667350137557,-15.262253059568206),
        Node(13.274442035020137,-15.116144674553041),
        Node(12.69452120513305,-14.59104715459372),
        Node(12.839835103630094,-14.33945707110789),
        Node(12.647809071216301,-14.569280087387298),
        Node(9.219761340017996,-16.897491764565224),
        Node(9.782286058285798,-16.975148696632342),
        Node(9.981958435439978,-16.924778407152434),
        Node(10.437880019415125,-16.941917002846694),
        Node(11.009664302934766,-16.669509402754038),
        Node(10.920393356211747,-17.290763320335696),
        Node(8.820341347777813,-17.03245052501915),
        Node(7.41175322408775,-16.683943145724186),
        Node(9.81679037228442,-16.495889790542616),
        Node(7.287492313444915,-16.409853030938287),
        Node(9.726908610829224,-15.715639459465521),
        Node(10.555611148153702,-16.133048147577732),
        Node(9.367570795175663,-16.43836245810407),
        Node(8.279101712679768,-15.893012857518428),
        Node(9.773923418188645,-16.287229825835333),
        Node(10.509475137097482,-16.267328573738098),
        Node(9.31228816684343,-15.948734444398006),
        Node(8.935770220573204,-16.16236685241202),
        Node(9.156310356124052,-16.079080620262076),
        Node(8.733256570131989,-16.131974995914753),
        Node(9.699798812896937,-15.731142343956677),
        Node(7.612619221591366,-15.975798421993247),
        Node(11.012539455069785,-16.27599029641242),
        Node(11.012785961934313,-16.049333143740515),
        Node(10.059862013347601,-15.701493038376864),
        Node(9.493906364924829,-15.641454999388223),
        Node(7.656307088950009,-17.510487383511013),
        Node(9.597649852052449,-17.381992179216674),
        Node(7.347738709059101,-17.469239977966073),
        Node(8.272373797471918,-18.04003116905587),
        Node(8.51416169917735,-17.952554652818446),
        Node(8.315688287172591,-17.96236975648555),
        Node(9.707082312656969,-18.04076278388875),
        Node(7.7476164370311125,-18.184155904360644),
        Node(8.451262808225035,-18.171960638603657),
        Node(10.177557938852114,-18.17745893588586),
        Node(9.471872625261696,-18.32033292992729),
        Node(8.831985414595636,-18.739230961490417),
        Node(9.711308818941244,-18.53485808642732),
        Node(7.927081501657477,-15.528901852320667),
        Node(9.859428031024464,-15.0131142114806),
        Node(9.727969082255008,-15.153473379942422),
        Node(7.840433804651212,-15.511134684615877),
        Node(8.298184965160267,-15.220352628189193),
        Node(9.69196033623636,-15.493694847100588),
        Node(9.551624812610061,-15.149896548232755),
        Node(10.083099790187738,-15.423383882976612),
        Node(5.674608372316857,-17.78043218619208),
        Node(7.656307088950009,-17.510487383511013),
        Node(6.628685592829953,-18.978777539364575),
        Node(5.9087860582489,-18.95834398037494),
        Node(7.276410863267422,-18.683993245826187),
        Node(7.347738709059101,-17.469239977966073),
        Node(4.174550804969076,-18.469387848792827),
        Node(5.104520871731012,-18.312903675088087),
        Node(4.8963573515613135,-17.894743473535215),
        Node(3.7302607232948723,-17.53677207297929),
        Node(3.9597729765974456,-17.547494736059427),
        Node(4.283513665398637,-18.584511025029983),
        Node(5.447228059728303,-18.85920347633622),
        Node(4.338676146496894,-18.592813777269086),
        Node(5.332843823602399,-19.18628784320225),
        Node(5.10258239707121,-19.410821179000553),
        Node(4.165330976605081,-16.468151064330808),
        Node(4.416228493879618,-17.334673684275934),
        Node(4.5113758777485025,-17.361913702194837),
        Node(7.122496303757334,-16.508718316820183),
        Node(4.154762480491897,-16.50698729065408),
        Node(5.484634356225175,-15.965792719743991),
        Node(6.726163223518228,-16.097186977859682),
        Node(5.455330306703527,-16.149258347068567),
        Node(5.674608372316857,-17.78043218619208),
        Node(4.174550804969076,-18.469387848792827),
        Node(3.0385416074316005,-17.726823191717244),
        Node(3.7302607232948723,-17.53677207297929),
        Node(3.231901530644187,-17.56213771038963),
        Node(3.9597729765974456,-17.547494736059427),
        Node(3.480548500367572,-17.72257320699444),
        Node(2.4417769205156716,-17.385792481371062),
        Node(1.7742260196535184,-17.570782898105964),
        Node(5.104520871731012,-18.312903675088087),
        Node(1.9070934658616459,-18.28188176687935),
        Node(4.8963573515613135,-17.894743473535215),
        Node(3.6004316239028356,-18.503665130813825),
        Node(4.283513665398637,-18.584511025029983),
        Node(2.2055258140002145,-18.58944869295728),
        Node(2.4825281707114533,-18.889521800452318),
        Node(3.7259404688395534,-18.823869020916646),
        Node(4.338676146496894,-18.592813777269086),
        Node(3.7898289729390626,-19.416653879909788),
        Node(3.1377555971410622,-19.433306470200634),
        Node(4.201660445865375,-19.229187594885154),
        Node(4.165330976605081,-16.468151064330808),
        Node(4.416228493879618,-17.334673684275934),
        Node(2.3691762810154735,-16.89273654682529),
        Node(2.600902259143119,-17.264786971222847),
        Node(2.5504181047216434,-17.269575845118098),
        Node(1.948988325196769,-17.09369018262589),
        Node(2.531953333273499,-16.95076362557232),
        Node(2.9774006282385983,-16.732031547029635),
        Node(4.154762480491897,-16.50698729065408),
        Node(2.2084745834840014,-16.706387080521758),
        Node(4.5113758777485025,-17.361913702194837),
        Node(2.910397141357155,-16.198588567157053),
        Node(3.602933927026733,-16.271042535137376),
        Node(3.715046472898919,-16.220675812574736),
        Node(3.352037298298228,-16.0924793840676),
        Node(3.4620911166247197,-16.188360246059087),
        Node(2.731891443457716,-16.03871848445867),
        Node(4.276570563519826,-15.813163446878903),
        Node(-0.793276197151508,-15.633722415118514),
        Node(0.20095482229103567,-17.36909115978872),
        Node(-0.8072431838124352,-16.606430719694654),
        Node(0.4969840892953883,-17.041479746922338),
        Node(-0.7356193361352581,-16.977417341304463),
        Node(0.8661566666676777,-16.96505930017849),
        Node(0.5324613441051511,-17.002871619681834),
        Node(1.1732784306390407,-17.359751504771506),
        Node(-0.10536547274203656,-16.641495082633032),
        Node(-0.6040469937469766,-16.4208199776266),
        Node(-0.018576050099561314,-16.06232719516131),
        Node(0.5288789446625195,-16.048817839857136),
        Node(0.646573327513785,-15.71244823727251),
        Node(0.6309142031301143,-15.751712679484386),
        Node(-1.9194763281071623,-17.139450594848775),
        Node(-1.7651107714514183,-17.305350532170785),
        Node(-1.8384278459932268,-16.887424571578713),
        Node(-2.6499176164669755,-16.99555056236985),
        Node(-2.268974227550231,-17.096454758048232),
        Node(-2.631937588366867,-17.119177294481723),
        Node(-2.706341294361664,-17.18438623582596),
        Node(-2.3032324289426107,-15.837038713272516),
        Node(-1.3707289781163468,-16.347808491633696),
        Node(-1.7282688762385625,-16.239970190133455),
        Node(-0.3435896804919345,-17.77000934370234),
        Node(1.024203535860515,-17.485152563087347),
        Node(0.716452967099741,-17.429156246541957),
        Node(-0.6763427304191758,-17.944109907625286),
        Node(-1.0905085380594848,-18.261346378727232),
        Node(-0.9613176495393319,-17.817925951776203),
        Node(-1.434407239066843,-18.418234368672852),
        Node(-1.3091778287106592,-18.344843777366705),
        Node(0.19845327288329884,-18.19922549226005),
        Node(0.1601437885725865,-18.133540857633346),
        Node(-0.13618150058637113,-18.800801954967117),
        Node(-0.21112084050818325,-18.615746538170264),
        Node(-0.3369182727249189,-15.596170281618683),
        Node(-0.0936325380631331,-15.333491397352358),
        Node(-0.5579333917154692,-15.33021063811621),
        Node(-0.23754420725715164,-15.319792511321637),
        Node(-0.9375430838754184,-15.169036000926251),
        Node(-4.990810854956464,-16.860831448118184),
        Node(-5.974425349109772,-16.65076646205229),
        Node(-4.134196398036778,-16.54467788719),
        Node(-5.769357195774987,-16.06270752192004),
        Node(-4.3664888509959034,-16.493265009265997),
        Node(-4.4690205690031135,-16.418466197594995),
        Node(-4.798946692101399,-16.026143431130993),
        Node(-5.848313385238892,-16.341545426778463),
        Node(-5.859984122377192,-15.866224016767232),
        Node(-4.3173142278026475,-16.74063891003606),
        Node(-4.227503929533221,-16.723077462080475),
        Node(-5.999649584035517,-16.2385407522329),
        Node(-2.842843543801216,-15.645874907196028),
        Node(-3.078256723115235,-15.795116918358762),
        Node(-3.34955990012557,-15.749620671543724),
        Node(-2.6499176164669755,-16.99555056236985),
        Node(-2.8972373798819717,-16.93867401122994),
        Node(-4.493726064399013,-16.979115781111858),
        Node(-2.631937588366867,-17.119177294481723),
        Node(-3.5850541358579946,-17.33908032394652),
        Node(-5.64216987532895,-17.20303855925477),
        Node(-3.6354750751175935,-17.220487374205486),
        Node(-4.266276549146539,-17.234354562954294),
        Node(-2.706341294361664,-17.18438623582596),
        Node(-4.916648165738238,-18.167576692616414),
        Node(-3.9146223385819567,-17.618369402185472),
        Node(-3.82196176984014,-17.96162283397058),
        Node(-4.52370912785296,-18.190351620804925),
        Node(-3.9595443301097966,-18.21396955365701),
        Node(-5.762107808415994,-17.81451453966617),
        Node(-5.483766671690532,-18.080989337130045),
        Node(-5.5355809379132825,-17.810036625775094),
        Node(-2.711328967486235,-15.628725284343084),
        Node(-4.500722885520734,-14.932682969918606),
        Node(-3.7419869348088994,-15.434587183480959),
        Node(-5.188911510291913,-15.487424088983023),
        Node(-5.517938629166537,-15.049853053767794),
        Node(-4.603010335247134,-15.310005452755146),
        Node(-3.2211619206507116,-15.271643717245919),
        Node(-3.2590403848147496,-15.074391555376522),
        Node(-4.472364112851203,-14.704615458991528),
        Node(-3.78916822292906,-14.644724897245682),
        Node(-8.236674656146272,-15.925178123224999),
        Node(-6.923725790233188,-15.959218232456912),
        Node(-6.709240507896222,-15.974136764035709),
        Node(-6.994357651713576,-16.39669160144125),
        Node(-7.944034763261104,-16.138652608509815),
        Node(-7.45734310652821,-16.60157963586896),
        Node(-7.091354311525739,-16.485585056227073),
        Node(-6.49118431607449,-16.70576895836713),
        Node(-10.073268642390207,-16.03491267078381),
        Node(-9.600967744048038,-16.460520410563376),
        Node(-9.948320359625278,-16.252808923376),
        Node(-9.35752218672809,-15.85922305145813),
        Node(-8.323150011032858,-16.31224685181963),
        Node(-9.89585833558337,-16.710815477558167),
        Node(-7.832313282934287,-16.987697965958194),
        Node(-8.364808978354272,-17.037493277363392),
        Node(-6.7388371102734546,-17.071799017000128),
        Node(-6.799417923300437,-17.094793017791616),
        Node(-9.11233779358058,-17.365827888773218),
        Node(-8.843158753632352,-17.51961923335636),
        Node(-8.801886561717422,-15.586110380009668),
        Node(-7.166780108524446,-15.098833592193678),
        Node(-8.121069416069929,-15.579419218784691),
        Node(-7.5181862812773215,-15.0377510957793),
        Node(-8.710724182152521,-15.231462008219761),
        Node(-6.924713199330759,-15.545604173396939),
        Node(-6.845406294665221,-14.997286373561742),
        Node(-8.36549406574093,-14.743553295527274),
        Node(-7.896579846522345,-14.874645620939875),
        Node(-7.970843789935294,-14.600589426449183),
        Node(-9.300051852232718,-14.664340660712547),
        Node(-9.373368510916693,-15.184584582273398),
        Node(-9.594646425335647,-14.726656078206517),
        Node(-7.602232802937699,-14.251609379598174),
        Node(-9.15768794678755,-14.466779385219022),
        Node(-8.486848518995785,-14.348432990603417),
        Node(-8.661079891714557,-14.369174913885892),
        Node(-9.29122547352402,-14.302154106855323),
        Node(-7.337039162635506,-14.187527450527973),
        Node(-8.0441615198324,-14.174074210915165),
        Node(-11.110018923800169,-15.098907679671141),
        Node(-10.253942609236834,-15.642090000028768),
        Node(-10.073268642390207,-16.03491267078381),
        Node(-10.499764123839505,-16.03799602796274),
        Node(-9.600967744048038,-16.460520410563376),
        Node(-9.948320359625278,-16.252808923376),
        Node(-9.35752218672809,-15.85922305145813),
        Node(-9.89585833558337,-16.710815477558167),
        Node(-10.199210549005674,-17.249942004351816),
        Node(-10.293596330955523,-17.359007184654974),
        Node(-10.563233307987815,-17.00371524539659),
        Node(-10.403191649884974,-17.069494070228256),
        Node(-9.787439812891293,-17.241196758392704),
        Node(-10.861496245044844,-16.491494212201133),
        Node(-10.719250777769691,-15.994009484158198),
        Node(-10.78153105407977,-16.962804480427653),
        Node(-8.801886561717422,-15.586110380009668),
        Node(-9.300051852232718,-14.664340660712547),
        Node(-10.599408151909216,-15.262587237531417),
        Node(-9.373368510916693,-15.184584582273398),
        Node(-9.594646425335647,-14.726656078206517),
        Node(-10.949738291270986,-14.719830659320706),
        Node(-11.052664693441873,-14.873420869830802),
        Node(-10.688003422819921,-15.311778735388248),
        Node(-9.86287973544265,-14.648389143634075),
        Node(-8.710724182152521,-15.231462008219761),
        Node(-11.662599109843027,-17.0210562530111),
        Node(-11.349271637279866,-15.104316169642814),
        Node(-11.199759250408983,-15.255985942619326),
        Node(-12.154466887407969,-15.073450734690459),
        Node(-11.331590767262426,-15.093856477440436),
        Node(-11.711029791819616,-16.583046280674168),
        Node(-11.111657241894072,-16.142307874015476),
        Node(-11.181197495550975,-16.02643156685781),
        Node(-11.329227189713261,-17.18324178740419),
        Node(-11.807544256965038,-14.463629493394965),
        Node(-9.982707355469639,-14.114314906254585),
        Node(-10.502124336253482,-14.435308242863139),
        Node(-10.60096756638291,-14.367214521869105),
        Node(-11.400679398210443,-14.416808290306577),
        Node(-10.931469243367484,-14.125545425696098),
        Node(-11.396928652280444,-14.053292491638011),
        Node(-9.15768794678755,-14.466779385219022),
        Node(-9.29122547352402,-14.302154106855323),
        Node(-9.894942927940399,-13.879556484594442),
        Node(-15,-15),
        Node(-13.043235496254706,-14.58639067118544),
        Node(-14.531964024658745,-14.592729615766075),
        Node(-14.744616363919757,-14.810959844801253),
        Node(-14.723399132012212,-14.931360127826142),
        Node(-14.81951439897541,-16.5991974527044),
        Node(-14.915608610542304,-16.74521462519163),
        Node(-13.157644342834063,-14.68210499493626),
        Node(-13.559929406346424,-14.618814448712723),
        Node(-13.789614224300726,-15.818172385945308),
        Node(-13.54660800106907,-15.018631285656081),
        Node(-13.221462505342867,-14.766777882884274),
        Node(-13.631715302189772,-15.703174646509698),
        Node(-13.10255097795122,-14.881859209878057),
        Node(-14.019617597449834,-16.421656372527487),
        Node(-14.48830235541125,-16.72217221445676),
        Node(-14.274653255607742,-13.858939885640096),
        Node(-14.640216155669389,-13.85959887994941),
        Node(-14.727205530983515,-14.036788687030581),
        Node(-14.795594754016808,-13.930479204870544),
        Node(-14.776077001544138,-13.898389695430362),
        Node(-13.76808721980796,-14.05066189173672),
        Node(-13.240834512751253,-14.455236375797638),
        Node(-13.858151765462443,-13.891303382239396),
        Node(-14.096133235964459,-13.361225391134868),
        Node(-13.933987296285185,-13.425089877732873),
        Node(-15.722360137258724,-13.135007819828845),
        Node(-16.058771084497035,-13.662841718179862),
        Node(-15.782412505845077,-16.769990945529194),
        Node(-16.01914637839776,-14.07460449488557),
        Node(-15.179288944465096,-15.442611244012285),
        Node(-15.838491069112344,-14.24922831214185),
        Node(-15.672462669792463,-14.605874573555692),
        Node(-15.388751882227396,-15.092419169305868),
        Node(-15.593626977354106,-14.415564617556198),
        Node(-15.04493136522048,-13.166146613283214),
        Node(-15.458418275564885,-14.022692313123347),
        Node(-15.799766305285079,-16.12280267268719),
        Node(-15.595433637766508,-15.666833565703424),
        Node(-15.046702825430236,-16.200756309069536),
        Node(-15.54092976875662,-15.826110262714845),
        Node(-16.05469340719374,-16.448212696463568),
        Node(-16.72396472436011,-15.991272763980025),
        Node(-16.552764237193372,-14.455048569197544),
        Node(-16.36819690963261,-14.31588839840221),
        Node(-16.066841018213402,-15.098689840556872),
        Node(-16.246798111298034,-15.465377746378554),
        Node(-16.408422314423568,-14.86313283525099),
        Node(-16.347887148499602,-14.911916204315506),
        Node(-16.136705142647152,-16.101390661330267),
        Node(-15.136059315700464,-13.115737293891435)
    ]

    basic_path = [Node(-1,0),Node(1,0)]
    basic_DP = [Node(-1,0),Node(0,-1),Node(1,0)]

    advanced_path = [
        (10, 0), (9.51, 3.09), (8.09, 5.88), (5.88, 8.09), (3.09, 9.51), (0, 10), (-3.09, 9.51), (-5.88, 8.09), (-8.09, 5.88), (-9.51, 3.09), (-10, 0), (-9.51, -3.09), (-8.09, -5.88+5), (-5.88, -8.09+6), (-3.09, -9.51+7), (0, -10+8), (3.09, -9.51+7), (5.88, -8.09+6), (8.09, -5.88+5), (9.51, -3.09)
    ]
    advanced_DP = [(8.66, 1.5), (8.14, 3.09), (7.29, 4.64), (6.13, 6.0), (4.71, 7.07), (3.08, 7.81), (1.33, 8.2), (-0.47, 8.23), (-2.26, 7.89), (-3.94, 7.21), (-5.48, 6.23), (-6.84, 4.99), (-7.97, 3.52), (-8.83, 1.87), (-9.4, 0.11), (-9.66, -1.67), (-9.6, -3.43), (-9.23, -5.14), (-8.56, -6.73), (-7.6, -8.12)]

    for i in range(len(advanced_DP)):
        advanced_DP[i] = Node(advanced_DP[i][0],advanced_DP[i][1])

    for i in range(len(advanced_path)):
        advanced_path[i] = Node(advanced_path[i][0],advanced_path[i][1]) 
        advanced_DP.append(advanced_path[i])
    
    my_hull = Hull(sample_path)


    
    my_hull.jarvis_march()
    my_hull.MalevolentShrine(5)


    print("Printing resulting hull")

    # testing
    print(my_hull.density_length(my_hull.hull[0],my_hull.hull[1]))
    my_hull.plot()

    plt.plot(my_hull.hull[0].x,my_hull.hull[0].y, 'g')

    for node in global_nodes:
        print("plt.plot(%s,%s,\"go\",\".\")"%(node.x,node.y))

    
    # for node in my_hull.hull:
    #     if node.equals(node,Node(15.7,15.7)):
    #         plt.plot(15.7,15.7,"go")
    # plt.plot(10.826754048513582,17.09285688763859,"m",marker='.')
    # plt.plot(13.591207731977605,17.470970960781727,"m",marker='.')
    # plt.plot(16.520883789038184,16.215395507755762,"m",marker='.')
    plt.plot(15.7,15.7,"m",marker='.')
    plt.plot(15.35161339468575,13.487097920933417,"m",marker='.')
    plt.plot(14.092803759398226,14.026587764628072,"m",marker='.')
    

    plt.xlim(-20,20)
    plt.ylim(-20,20)
    plt.show()

    n1,n2,n3 = Node(-3,-2), Node(3,5), Node(6,-4)
    k1,k2,k3 = Node(0,0),Node(0,1),Node(1,0)
    t1 = Triangle(n1,n2,n3,True)
    t2 = Triangle(k1,k2,k3,True)

    heap = []
    heapq.heappush(heap,t2)
    heapq.heappush(heap, t1)

    l1 = [0,1,2,3,4,5]

    i = 1
    a,b,c = l1[i:i+3]

    print(a)
    print(b)
    print(c)


    nod = [Node(0,0),Node(0,-1),Node(1,0)]

    heap2 = []
    for i in range(len(nod)-2):
        if my_hull.get_angle(nod[i],nod[i+1],nod[i+2]) > 180:
            # Concave Triangle
            heapq.heappush(heap2, Triangle(nod[i],nod[i+1],nod[i+2],True))

    print(heapq.heappop(heap2))
