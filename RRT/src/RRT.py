import random
import matplotlib.pyplot as plt
from Node import Node
from Map import Map

#map boundaries
XMIN, XMAX, YMIN, YMAX = -20, 20, -20, 20
#constants
EPSILON = 2
NUM_OBSTACLES = 2

def goal_reached(nodes, goal):
    for node in nodes:
        if node.get_distance(goal) <= EPSILON:
           return True
    return False 

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
        v = u.closest_node(map.nodes)
        if v.get_distance(u) > EPSILON:
            w = v.calc_w(u, EPSILON)
        else:
            w = u

        # check if sample is safe
        if not (map.node_in_obstacle(w) or map.obstacle_between_nodes(w, v)):
            v.children.append(w)
            w.parent = v
            map.nodes.append(w)
            success_counter+=1

    print(success_counter)

    # plot the map
    map.plot()

    # plot solution if solution found
    if goal_reached(map.nodes, goal):
        last_node = goal.closest_node(map.nodes)
        last_node.children.append(goal)
        goal.parent = last_node
        map.nodes.append(goal)

        map.plot_solution(trace_back(start, goal))
        print("Solution Found")
    else:
        print("Solution Not Found")

    # plot the start and goal points
    map.plot_single_node(start, 'go', 10)
    map.plot_single_node(goal, 'yo', 10)

    map.show()

    return

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
    
    