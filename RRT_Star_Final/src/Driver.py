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
        
        course_map = Map([],obstacles,[XMIN,XMAX,YMIN,YMAX])
        course_map.set_start(Node(-18, 10))
        course_map.set_goal(Node(18, -10))
        return course_map

    elif id == 1:
        # make maze obstacle course
        obstacle_lists = []
        obstacle_lists.append([(0,0),(11,0),(11,3),(10,3),(10,1),(5,1),(5,3),(4,3),(4,1),(1,1),(1,4),(2,4),(2,2),(3,2),(3,4),(6,4),(6,2),(7,2),(7,4),
               (8,4),(8,2),(9,2),(9,5),(0,5),(0,0)])
        obstacle_lists.append([(12,0),(12,1),(20,1),(20,4),(19,4),(19,2),(18,2),(18,4),(17,4),(17,2),(14,2),(14,4),(13,4),(13,2),(12,2),(12,4),(10,4),(10,7),
         (11,7),(11,5),(12,5),(12,7),(13,7),(13,5),(14,5),(14,8),(12,8),(12,11),(13,11),(13,9),(14,9),(14,11),(15,11),(15,3),(16,3),
         (16,7),(17,7),(17,5),(18,5),(18,7),(19,7),(19,5),(21,5),(21,0),(12,0)])
        obstacle_lists.append([(8,5),(8,8),(7,8),(7,6),(6,6),(6,9),(10,9),(10,14),(8,14),(8,15),(13,15),(13,14),(11,14),(11,8),(9,8),(9,5),(8,5)])
        obstacle_lists.append([(20,5),(20,8),(18,8),(18,9),(20,9),(20,12),(19,12),(19,10),(18,10),(18,13),(20,13),(20,14),(18,14),(18,15),(20,15),(20,20),
         (19,20),(19,16),(18,16),(18,20),(17,20),(17,18),(15,18),(15,15),(16,15),(16,17),(17,17),(17,8),(16,8),(16,14),(15,14),(15,12),
         (12,12),(12,13),(14,13),(14,18),(13,18),(13,16),(12,16),(12,19),(16,19),(16,20),(11,20),(11,16),(10,16),(10,18),(9,18),(9,16),
         (8,16),(8,19),(10,19),(10,20),(8,20),(8,21),(21,21),(21,5),(20,5)])
        obstacle_lists.append([(0,5),(0,21),(7,21),(7,18),(6,18),(6,20),(1,20),(1,15),(2,15),(2,19),(3,19),(3,17),(4,17),(4,19),(5,19),(5,17),(7,17),(7,16),
         (5,16),(5,15),(7,15),(7,14),(5,14),(5,13),(9,13),(9,10),(8,10),(8,12),(5,12),(5,11),(7,11),(7,10),(4,10),(4,16),(3,16),
         (3,14),(1,14),(1,13),(3,13),(3,9),(5,9),(5,8),(2,8),(2,12),(1,12),(1,5),(0,5)])
        obstacle_lists.append([(4,5),(4,6),(2,6),(2,7),(5,7),(5,5),(4,5)])

        for coord_list in obstacle_lists:
            result_list = map(lambda point: (point[0]*2,point[1]*2), coord_list)
            obstacles.append(Obstacle(list(result_list)))
        
        course_map = Map([],obstacles,[0,42,0,42])
        course_map.set_start(Node(23, 1))
        course_map.set_goal(Node(15, 41))

        return course_map

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
    # # generate maps
    # map1_no_hull = make_map(0)
    
    # # Map 1 - No Hull
    # rrt = RRTStar(map1_no_hull,3)
    # rrt.run()
    # rrt.plot_map()
    # rrt.plot_time_to_length()

    # # # Map 1 - Hull
    # map1_with_hull = make_map(0)
    # rrt = RRTStar(map1_with_hull,3,get_hull(0))
    # rrt.run()
    # rrt.plot_map()
    # rrt.plot_time_to_length()


    # testing map
    map2_no_hull = make_map(1)
    rrt = RRTStar(map2_no_hull,3)
    # rrt.run()
    # rrt.plot_map()
    # rrt.plot_time_to_length()
    map2_no_hull.plot()
    map2_no_hull.show()

