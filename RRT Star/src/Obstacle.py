from Node import Node
from matplotlib.path import Path

class Obstacle:
    def __init__(self, coords, r=0):
        # make polygon
        if r == 0:
            self.path = Path(coords)
        # make circle
        else:
            self.path = Path.circle(coords, r)

    # returns whether node is contained within obstacle
    def contains_node(self, node):
        if self.path.contains_points([node.get_coord()]):
            return True
        return False
    
    # returns whether the object is in the middle of the line between node1 and node2
    def intersects_path(self, node1, node2):
        line_seg = Path([node1.get_coord(), node2.get_coord()])
        if line_seg.intersects_path(self.path):
            return True
        return False
    