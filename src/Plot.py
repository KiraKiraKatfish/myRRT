import matplotlib.pyplot as plt
from Node import Node

#Plots nodes
#Note: to display results, call plt.show()
def plot_map(nodes):
    for node in nodes:
        #plot the node itself
        plt.plot(node.x, node.y, 'ko')

        #plot all the edges connecting to it
        for child in node.children:
            draw_edge(node,child, 'k')
    
    plt.plot(nodes[0].x, nodes[0].y, 'go')
    plt.plot(19, 19, 'ro')
    
    plt.title("RRT")

#Plots path between nodes
def plot_path(nodes):
    for node in nodes:
        if node.parent != None:
            draw_edge(node, node.parent, 'r')

def draw_edge(node1, node2, color):
    plt.plot([node1.x, node2.x], [node1.y,node2.y], color)