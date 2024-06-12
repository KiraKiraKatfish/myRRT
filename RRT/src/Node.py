import numpy as np
import math

class Node:
    def __init__(self, x, y, cost=0, children=None, parent=None):
        self.x = x
        self.y = y
        self.cost = cost
        self.children = []
        self.parent = None

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
