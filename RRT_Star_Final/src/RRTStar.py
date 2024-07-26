from Samplers import Sampler, HullSampler
from HullConstructor import HullConstructor
from Node import Node
import matplotlib.pyplot as plt
import time

class RRTStar:
    def __init__(self,map,time_limit,hull = []):
        self.map = map
        self.time_limit = time_limit
        self.hull = hull
        if hull:
            self.sampler = HullSampler(hull)
        else:
            self.sampler = Sampler(map.axis)
        self.epsilon = 2
        self.data = [] # data vector. [[time,length],[time,length],...]

    def set_epsilon(self, num):
        self.epsilon = num

    def run(self):
        tstart = time.time()
        tend = time.time() + self.time_limit
        num_iter = 0
        
        while time.time() < tend:
        # for i in range(1000):
            x, y = self.sampler.sample()
            u = Node(x,y)
            # nearest neighbors excluding the goal node. Prevent cheating by getting the goal
            v, dist = self.map.tree.nearestNeighbor(u,self.map.goal)
            if dist > self.epsilon:
                w = v.calc_w(u, self.epsilon)
            else:
                w = u

            # check if sample is safe
            if not (self.map.node_in_obstacle(w) or self.map.obstacle_between_nodes(w, v)):
                # attach sample to tree
                v.children.append(w)
                w.parent = v
                w.cost = v.cost + v.get_distance(w)
                
                # compare to neighbors for shorter path
                neighbors = self.map.findCloseNeighbors(w,self.epsilon)
                self.map.reduce_path(w,neighbors)
                self.map.add_node(w)

                # compare neighbors to new path for potential shorter path
                for neighbor in neighbors:
                    self.map.reduce_path(neighbor,[w])

            # record data every 10 nodes added
            if num_iter%10 == 0:
                self.data.append([time.time()-tstart, self.map.goal.cost])
            num_iter += 1

        if self.calculate_solution():
            # solution found
            return True
        
        # solution not found
        return False

    def calculate_solution(self):
        solution = []

        if self.map.goal.parent:
            pointer = self.map.goal
            while pointer.parent:
                solution.append(pointer)
                pointer = pointer.parent
            solution.append(pointer)

        self.map.solution = solution
        return solution
    
    def plot_time_to_length(self):
        x,y = zip(*self.data)
        plt.plot(x,y)
        plt.show()

    def plot_map(self):
        self.map.plot()
        if self.hull:
            self.map.plot_hull(self.hull)
        plt.show()

    def export_hull(self, size):
        if self.map.solution:
            hull = HullConstructor(self.map.solution, size)
            return hull.get_coord_list()
        return []