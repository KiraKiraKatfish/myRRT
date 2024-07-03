import random
import matplotlib.pyplot as plt
from Node import Node

# Input: A list of nodes forming a DP
# Output: The convex hull, sorted counter-clockwise
# Time Complexity: O(nh), where n is the # of nodes, h is the # of nodes in the convex hull
# Reference: https://www.youtube.com/watch?v=nBvCZi34F_o
def JarvisMarch(nodes):
    hull = []

    # find the leftmost node
    on_hull = nodes[0]
    for node in nodes: # O(n)
        if node.x < on_hull.x:
            on_hull = node

    while True:
        hull.append(on_hull)
        next_node = nodes[0]
        for node in nodes:
            o = orientation(on_hull,next_node,node)
            if next_node == on_hull or o == 1 or (o == 0 and on_hull.get_distance(node) > on_hull.get_distance(next_node)):
                next_node = node
        on_hull = next_node
        if on_hull == hull[0]:
            break
    return hull

# Input: three nodes, a b c
# Output: Whether the angle abc is counterclockwise
#           1 = counterclockwise
#           -1 = clockwise
#           0 = collinear
def orientation(a,b,c):
    d = (c.y-b.y)*(b.x-a.x) - (b.y-a.y)*(c.x-b.x)
    if d > 0:
        return 1
    if d < 0:
        return -1
    if d == 0:
        return 0

def MalevolentShrine(solution):
    DP = []
    d = 1
    orientations = [
        (1, 0),
        (1, 1),
        (0, 1),
        (-1, 1),
        (-1, 0),
        (1, -1),
        (0, -1),
        (-1, -1),
    ]

    # add 8 points for each solution node, such that the 8 points encircle the node
    for node in solution:
        for x, y in orientations:
            DP.append(Node(node.x + x, node.y + y))

    ## print all DP nodes ##
    # for node in DP:
    #     plt.plot(node.x, node.y, "ko")

    return JarvisMarch(DP)


def random_node():
    x = random.uniform(-10,10)
    y = random.uniform(-10,10)
    return Node(x,y)

def plot_edge(node_a,node_b,color):
    plt.plot([node_a.x,node_b.x], [node_a.y,node_b.y], color)

if __name__ == "__main__":
    # make test DP
    DP = []
    for i in range(100):
        DP.append(random_node())

    # Call Jarvis March algorithm
    ConvexHull = JarvisMarch(DP)

    # Plot DP and resulting convex hull
    for node_a, node_b in zip(ConvexHull, ConvexHull[1:]):
        plot_edge(node_a,node_b,'r')
    plot_edge(ConvexHull[0], ConvexHull[-1], 'r')
    for node in DP:
        plt.plot(node.x, node.y, 'ko')

    plt.xlim(-20,20)
    plt.ylim(-20,20)
    plt.show()
