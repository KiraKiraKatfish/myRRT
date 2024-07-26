import numpy as np
from triangle import triangulate
from matplotlib.path import Path
import random

class Sampler:
    def __init__(self,axis):
        # axis given in {'XMIN': axis[0], 'XMAX': axis[1], 'YMIN': axis[2], 'YMAX': axis[3]}
        self.axis = axis
    
    def sample(self):
        x = random.uniform(self.axis['XMIN'],self.axis['XMAX'])
        y = random.uniform(self.axis['YMIN'],self.axis['YMAX'])
        return x,y


class HullSampler():
    # Input: 2d numpy array of points describing a hull. ex: [[0,0],[0,1.1],[1,0],[1,1]]
    def __init__(self, points):
        self.points = np.array(points)
        segments = points
        segments.append(points[0])
        border = Path(segments)
        self.tri = triangulate({'vertices': points, 'segments': segments})
        self.triangles = self.tri['triangles'].tolist()
        self.triangles = [x for x in self.triangles if self.in_hull(x,border)]

        # tri_weights is the percentage area each triangle covers out of the whole polygon
        self.tri_weights = []
        for tri_points in self.points[self.triangles]:
            area = 0.5*abs(tri_points[0][0]*tri_points[1][1]+tri_points[1][0]*tri_points[2][1]+tri_points[2][0]*tri_points[0][1]-tri_points[0][0]*tri_points[2][1]-tri_points[1][0]*tri_points[0][1]-tri_points[2][0]*tri_points[1][1])
            self.tri_weights.append(area.item())

        total_area = sum(self.tri_weights)
        self.tri_weights = [x/total_area for x in self.tri_weights]


    def in_hull(self,points,border):
        x, y = zip(*self.points[points])

        # Formula to calculate centroid 
        x = round(sum(x) / 3, 2)
        y = round(sum(y) / 3, 2)
        if not border.contains_points([(x,y)]):
            return False
        return True

    # Output: a uniformly sampoled random coordinate pair in a list [x,y] from within the hull
    # Source: https://stackoverflow.com/questions/68493050/sample-uniformly-random-points-within-a-triangle
    def sample(self):
        # select random triangle index weighted proportionally to size and size of whole polygon
        x = random.choices(range(len(self.triangles)), weights=self.tri_weights)     
        triangle = self.points[self.triangles][x][0]
            
        # get the sample
        sample = self.sample_triangle(triangle)
            
        return sample[0], sample[1]
    
    def sample_triangle(self,triangle):
        # transform triangle so a is at origin
        A = triangle[0] - triangle[0]
        B = triangle[1] - triangle[0]
        C = triangle[2] - triangle[0]

        s = random.random()
        t = random.random()
        in_triangle = s + t <= 1
        p = s*B + t*C if in_triangle else (1-s)*B + (1-t)*C
        return p + triangle[0]