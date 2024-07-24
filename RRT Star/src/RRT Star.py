import random
import matplotlib.pyplot as plt
from Node import Node
from Map import Map
from JarvisMarch import *

#map boundaries
XMIN, XMAX, YMIN, YMAX = -20, 20, -20, 20
#constants
EPSILON = 2
NUM_OBSTACLES = 2

def RRT(start, goal, num_iter):
    map = Map([start], [], [XMIN,XMAX,YMIN,YMAX])
    success_counter = 0

    # generate obstacles that don't cover start and goal
    map.generate_obstacles(NUM_OBSTACLES)
    while map.node_in_obstacle(start) or map.node_in_obstacle(goal):
        map.clear_obstacles()
        map.generate_obstacles(NUM_OBSTACLES)

    # sample num_iter # of points
    for i in range(num_iter):
        u = random_node()
        v, dist = map.tree.nearestNeighbor(u)
        if dist > EPSILON:
            w = v.calc_w(u, EPSILON)
        else:
            w = u

        # check if sample is safe
        if not (map.node_in_obstacle(w) or map.obstacle_between_nodes(w, v)):
            # attach sample to tree
            v.children.append(w)
            w.parent = v
            w.cost = v.cost + v.get_distance(w)
            
            # compare to neighbors for shorter path
            neighbors = map.findCloseNeighbors(w,5)
            map.reduce_path(w,neighbors)
            map.add_node(w)
            success_counter+=1

            # compare neighbors to new path for potential shorter path
            for neighbor in neighbors:
                map.reduce_path(neighbor,[w])

    print(success_counter)

    # plot the map
    map.plot()

    # plot solution if solution found
    # check if the closest node to the goal is within acceptable range
    near_goal_node, dist = map.tree.nearestNeighbor(goal)
    ## ADD CHECK FOR OBSTACLE IN BETWEEN NODE AND GOAL ##
    if dist <= EPSILON:
        near_goal_node.children.append(goal)
        goal.parent = near_goal_node
        goal.cost = near_goal_node.cost + dist
        map.add_node(goal)

        map.solution = trace_back(start, goal)
        map.plot_solution()
        print("Solution Found! Cost: ", goal.cost)
    else:
        print("Solution Not Found")

    # plot the start and goal points
    map.plot_single_node(start, 'go', 10)
    map.plot_single_node(goal, 'yo', 10)

    map.show()

    return map

def trace_back(start, goal):
    node = goal
    shortest_path = [goal]

    while node != start:
        node = node.parent
        shortest_path.append(node)

    return shortest_path

def random_node():
    x = random.uniform(XMIN,XMAX)
    y = random.uniform(YMIN,YMAX)
    return Node(x,y)

if __name__ == "__main__":
    start = Node(-15,-15)
    goal = Node(15,15)
    map = RRT(start, goal, 1000)

    if map.solution != []:
        for node in map.solution:
            print("Node(%s,%s),"%(node.x, node.y))

        print("Now printing DP")

        for node in map.solution:
            neighbors = map.tree.neighborsInRadius(node, 2)
            for neighbor in neighbors:
                print("Node(%s,%s),"%(neighbor.x, neighbor.y))

    plt.show()
    
    