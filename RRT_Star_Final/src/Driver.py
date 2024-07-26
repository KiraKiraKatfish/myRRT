from Map import Map
from Obstacle import Obstacle
from Node import Node
from RRTStar import RRTStar
import json

#map boundaries
XMIN, XMAX, YMIN, YMAX = -20, 20, -20, 20


# returns a map of id #
# available map ids:
# 0: zig-zag obstacles
# 1: maze obstacles
# 2: many circles
def make_map(id):
    obstacles = []

    if id == 0:
        # make zig zag obstacle course
        for i in range(-20,20,4):
            left,right = i,i+2
            if i % 8 == 0:
                top,bottom = YMAX, (1/5)* YMIN
            else:
                top,bottom = (1/5)* YMAX, YMIN
            obstacle_coords = [(left,top),(right,top),(right,bottom),(left,bottom),(left,top)]
            obstacles.append(Obstacle(obstacle_coords))

    map = Map([],obstacles,[XMIN,XMAX,YMIN,YMAX])
    map.set_start(Node(-18, 10))
    map.set_goal(Node(18, -10))
    return map

def generate_hulls():
    map1 = make_map(0)
    rrt = RRTStar(map1, 5)
    if rrt.run():
        with open('hulls/map1_hull.json', 'w') as f:
            json.dump(rrt.export_hull(30), f, indent=2)
        print("Success")
        return
    else:
        print("Failure")
        return
    
def get_hull(map_id):
    if map_id == 0:
        with open("hulls/map1_hull.json", 'r') as f:
            return json.load(f)
    return []



if __name__ == "__main__":
    # generate maps
    map1_no_hull = make_map(0)
    
    # Map 1 - No Hull
    rrt = RRTStar(map1_no_hull,3)
    rrt.run()
    rrt.plot_map()
    rrt.plot_time_to_length()

    # # Map 1 - Hull
    map1_with_hull = make_map(0)
    rrt = RRTStar(map1_with_hull,3,get_hull(0))
    rrt.run()
    rrt.plot_map()
    rrt.plot_time_to_length()


