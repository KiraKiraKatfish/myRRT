import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from Obstacle import Obstacle
from KDTree import KDTree

class Map:
    def __init__(self, nodes=[], obstacles=[], axis=[-20,20,-20,20]):
        self.nodes = nodes
        self.tree = KDTree(nodes)
        self.obstacles = obstacles
        self.axis = {'XMIN': axis[0], 'XMAX': axis[1], 'YMIN': axis[2], 'YMAX': axis[3]}
        self.start, self.goal = None, None
        self.fig, self.ax = plt.subplots()
        self.solution = []

    def set_start(self,node):
        self.start = node
        self.nodes = [node]
        self.tree = KDTree(self.nodes)

    def set_goal(self,node):
        self.goal = node
        self.goal.cost = 1000 # set to max
        self.nodes.append(node)
        self.tree.insert(node)

    def is_solved(self):
        if self.goal and self.goal.parent:
            return True
        return False
    
    # inserts node into node list and kd tree
    def add_node(self, node):
        self.nodes.append(node)
        self.tree.insert(node)

    # generates num random obstacles
    def generate_obstacles(self, num):
        # number of polygons to generate
        for i in range(num):
            obstacle_coords = []

            # number of verticies in a polygon
            for j in range(random.randint(3, 5)):
                obstacle_coords.append(self.random_coord())

            # connect end to start (close polygon)
            obstacle_coords.append(obstacle_coords[0])

            self.obstacles.append(Obstacle(obstacle_coords))
    
    def clear_obstacles(self):
        self.obstacles.clear()

    # returns whether the node is contained within an obstacle
    def node_in_obstacle(self, node):
        for obstacle in self.obstacles:
            if obstacle.contains_node(node):
                return True
        return False
    
    # returns whether there are any obstacles between the direct line segment through node1 and node2
    def obstacle_between_nodes(self, node1, node2):
        for obstacle in self.obstacles:
            if obstacle.intersects_path(node1, node2):
                return True
        return False
    
    # returns all the nodes within a r radius of the target node
    def findCloseNeighbors(self, target, r):
        return self.tree.neighborsInRadius(target, r)
    
    # compares target node's path to potential new paths using nodes in the list
    # reduces target node's path to the shortest possible path
    def reduce_path(self, target, nodes):
        shortest_path_parent = None
        shortest_path_cost = target.cost
        for node in nodes:
            new_path_cost = node.cost + target.get_distance(node)
            if new_path_cost < shortest_path_cost and not self.obstacle_between_nodes(node, target):
                shortest_path_parent = node
                shortest_path_cost = new_path_cost
        
        if shortest_path_parent != None:
            # Edge Case: target has no existing parent. (e.g. goal node)
            if target.parent:
                target.parent.children.remove(target)
            target.parent = shortest_path_parent
            shortest_path_parent.children.append(target)
            target.add_cost(shortest_path_cost - target.cost)


    # plots nodes and obstacles
    def plot(self):
        # plt.title("RRT*")
        self.ax.set_xlim(self.axis['XMIN'],self.axis['XMAX'])
        self.ax.set_ylim(self.axis['YMIN'],self.axis['YMAX'])

        self.plot_obstacles()
        self.plot_nodes()
        self.plot_solution()

        if self.start and self.goal:
            # plot the start and goal in different colors
            self.ax.plot(self.start.x,self.start.y, 'yo', markersize=10)
            self.ax.plot(self.goal.x,self.goal.y, 'go', markersize=10)

    def plot_solution(self):
        for node in self.solution:
            if node.parent != None:
                self.draw_edge(node, node.parent, 'r', 3)

        # hull = BetterHull(self.solution,7)

        # hull_list = hull.get_coord_list()
        # x,y = zip(*hull_list)
        # self.ax.plot(x,y,color='b', lw=3)
        # self.ax.plot([x[0],x[-1]],[y[0],y[-1]],color='b', lw=3)

        # plt.figtext(0.333, 0.01, "Solution Cost: " + str(self.goal.cost), wrap=True, horizontalalignment='center', fontsize=8)
        # plt.figtext(0.667, 0.01, "Convex Hull # vertices: " + str(hull.size), wrap=True, horizontalalignment='center', fontsize=8)

    def plot_obstacles(self):
        for obstacle in self.obstacles:
            patch = patches.PathPatch(obstacle.path, facecolor='steelblue', lw=0)
            self.ax.add_patch(patch)

    def plot_nodes(self):
        for node in self.nodes:
            #plot all the edges connecting to the node
            for child in node.children:
                self.draw_edge(node,child, 'tab:gray')

            #plot the node itself
            self.ax.plot(node.x, node.y, 'k', marker='.')

    def plot_hull(self, hull):
        x,y = zip(*hull)
        self.ax.plot(x,y, 'm',lw=1)
        self.ax.plot([x[0],x[-1]],[y[0],y[-1]], 'm',lw=1)

    def draw_edge(self, node1, node2, c, line_width=1):
        self.ax.plot([node1.x, node2.x], [node1.y,node2.y], color=c, lw=line_width)

    def show(self):
        plt.show()
                    

    def random_coord(self):
        x = random.uniform(self.axis['XMIN'],self.axis['XMAX'])
        y = random.uniform(self.axis['YMIN'],self.axis['YMAX'])
        return (x,y)