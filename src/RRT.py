import random
import matplotlib.pyplot as plt
from Node import Node
from Plot import *

#map boundaries
XMIN, XMAX, YMIN, YMAX = -20, 20, -20, 20
#constants
EPSILON = 2

def collision_check():
    return False

def goal_reached(nodes, goal):
    for node in nodes:
        if node.get_distance(goal) <= 1:
           return True
    return False 

def RRT(start, goal):
    nodes = [start]
    i = 0

    while not goal_reached(nodes, goal):
        u = random_node()
        v = u.closest_node(nodes)
        if v.get_distance(u) > EPSILON:
            w = v.calc_w(u, EPSILON)
        else:
            w = u
        v.children.append(w)
        w.parent = v
        nodes.append(w)
        i+=1

    print(i)
    return nodes

def trace_back(nodes, start, goal):
    node = goal.closest_node(nodes)
    shortest_path = [node]

    while node != start:
        node = node.parent
        shortest_path.append(node)

    return shortest_path

def random_node():
    x = random.uniform(XMIN,XMAX)
    y = random.uniform(YMIN,YMAX)
    return Node(x,y)

if __name__ == "__main__":
    start = Node(5,6)
    goal = Node(19,19)
    map = RRT(start, goal)
    
    plot_map(map)
    plot_path(trace_back(map, start, goal))
    plt.show()