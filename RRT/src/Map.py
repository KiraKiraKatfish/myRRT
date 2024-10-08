import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from Obstacle import Obstacle

class Map:
    def __init__(self, nodes=[], obstacles=[], axis=[-20,20,-20,20]):
        self.nodes = nodes
        self.obstacles = [] #obstacles
        self.axis = {'XMIN': axis[0], 'XMAX': axis[1], 'YMIN': axis[2], 'YMAX': axis[3]}
        self.fig, self.ax = plt.subplots()


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
    
    # plots nodes and obstacles
    def plot(self):
        plt.title("RRT")
        self.ax.set_xlim(self.axis['XMIN'],self.axis['XMAX'])
        self.ax.set_ylim(self.axis['YMIN'],self.axis['YMAX'])

        self.plot_obstacles()
        self.plot_nodes()

    def plot_solution(self, nodes):
        for node in nodes:
            if node.parent != None:
                self.draw_edge(node, node.parent, 'r', 3)

    def plot_obstacles(self):
        for obstacle in self.obstacles:
            patch = patches.PathPatch(obstacle.path, facecolor='blue', lw=0)
            self.ax.add_patch(patch)

    def plot_nodes(self):
        for node in self.nodes:
            #plot the node itself
            self.ax.plot(node.x, node.y, 'ko')

            #plot all the edges connecting to it
            for child in node.children:
                self.draw_edge(node,child, 'k')

    def plot_single_node(self, node, color, markersize=None):
        if(markersize==None):
            self.ax.plot(node.x, node.y, color)
        else:
            self.ax.plot(node.x, node.y, color, markersize=markersize)

    def show(self):
        plt.show()

    # (TO BE REPLACED WHEN EDGES ARE IMPLEMENTED)
    def draw_edge(self, node1, node2, color, line_width=1):
        self.ax.plot([node1.x, node2.x], [node1.y,node2.y], color, lw=line_width)
        
            

    def random_coord(self):
        x = random.uniform(self.axis['XMIN'],self.axis['XMAX'])
        y = random.uniform(self.axis['YMIN'],self.axis['YMAX'])
        return (x,y)
    
if __name__ == "__main__":
    map = Map()
    map.generate_obstacles(2)
    map.plot()
    plt.show()