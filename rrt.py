import random
import math
import matplotlib.pyplot as plt

#map boundaries
XMIN, XMAX, YMIN, YMAX = -20, 20, -20, 20

class Node:
    def __init__(self, x, y, children=None):
        self.x = x
        self.y = y
        self.children = []

def print_map(nodes):
    for node in nodes:
        #plot the node itself
        plt.plot(node.x, node.y, 'ko')

        #plot all the edges connecting to it
        for child in node.children:
            draw_edge(node,child)
    
    plt.plot(nodes[0].x, nodes[0].y, 'go')
    plt.plot(19, 19, 'ro')
    
    plt.title("RRT")
    plt.show()

def draw_edge(node1, node2):
    plt.plot([node1.x, node2.x], [node1.y,node2.y], 'k')

def collision_check():
    return False

def get_distance(node1, node2):
    L = math.sqrt((node1.x-node2.x)**2 + (node1.y-node2.y)**2)
    return L

def goal_reached(nodes, goal):
    for node in nodes:
        if get_distance(node, goal) <= 3:
           return True
    return False 

def RRT(start, goal):
    nodes = [start]
    i = 0

    while not goal_reached(nodes, goal):
        u = random_node()
        v = closest_node(nodes, u)
        v.children.append(u)
        nodes.append(u)
        i+=1

    print(i)
    return nodes

def random_node():
    x = random.uniform(XMIN,XMAX)
    y = random.uniform(YMIN,YMAX)
    return Node(x,y)

def closest_node(nodes, u):
    closest_node = nodes[0]
    smallest_dist = get_distance(nodes[0], u)

    for node in nodes:
        dist = get_distance(node,u)
        if dist < smallest_dist:
            closest_node = node
            smallest_dist = dist
    
    return closest_node


# #make n nodes with random coords
# def sample_nodes(nodes, n):
#     for i in range(n):


#     return



if __name__ == "__main__":
    start = Node(5,6)
    goal = Node(19,19)
    print_map(RRT(start, goal))