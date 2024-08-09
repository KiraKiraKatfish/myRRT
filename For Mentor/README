Node:
Represents coordinate points that RRT* samples
Contains
  x,y coordinates
  cost (AKA length to root)
  parent, children pointers (for RRT implementation)
  left, right pointers (for KDTree implementation)

HullNode:
Represents a Node that can be added to a Hull during bounding hull construction
Extends Node, and adds one new member variable
Note that you could just merge this with Node
Contains
  Node variables
  on_hull (indicates whether the node is on the bounding hull. i.e. a vertex on the hull)
  __lt__ override to make it so it comparison always results in false. (For heap logic. So comparing nodes is false, but comparing the area of potential merges is ok)

HullConstructor:
Constructs a bounding hull around the inputted solution points (Input=Node list)
Algorithm
  Convert input Node list into HullNode list
  For every HullNode, calculate a few points in a circle of radius r around the HullNode. Add those points to the HullNode list
  Construct convex hull around HullNode list. Leverage left,right pointers in HullNode to construct the hull as a circular linked list.(I used Jarvis March algo)
  (I use left,right member variables as left right pointers for HullNodes circular linked list)
  Cut algo **OPTIONAL** (converts convex hull to concave hull. Optional bc probably minimal run-time saved.)
    Iterate through each convex hull edge and cut depending on Density-Length condition and whether it intersects current hull
  Merge algo (reduces edges on hull until hull has desired number of edges)
    Define convex merge and concave merge (concave only if cut algo implemented. Merges concavities)
      Convex merge takes four adjacent points along a hull, and if the two angles are both <180 and the sum of both is >180,
      then it calculates the intersection of both line segments and adds to the hull, while getting rid of the obsolete ones. (Read source paper for better description with pictures)
      Concave merge takes three adjacent points along a hull, and if the angle is >180, take the middle point off of the hull.
    Construct min priority heap
    Iterate through hull, adding potential merges along with the area that would be added into the min priority heap
    While heap is not empty and desired # of edges is not met yet
      Pop off the minimum area merge off the heap. 
      If one or more of the points needed to merge is already off the hull, skip the merge and pop heap again
      Conduct the merge
      Recalculate potential merges of surrounding area and add to heap (check from two left to two right of all vertices involved in merge)
      (This recalculation process is why i made the hull a circular linked list)

  DONE. resulting hull should be concave or convex with the desired num edges, and also have the minimum possible area

HullSampler:
Defines a function that uniformly generates a random point within a hull
Algorithm
  Perform Constrained Delauney Triangulation on bounding hull
  Calculate triangleArea/hullArea ratio for each triangle
  
  Sample function
    Using the ratios as weights, uniformly choose a random triangle from the triangles
    Sample from the triangle

Note
  I was unable to find a easy to use library containing constrained triangulation algorithms
  The triangulation method I'm using currently is unstable after 7 points in the hull
  However, the problem goes away if you are just constructing convex hulls. Because a regular Delauney triangulation
  will suffice for a convex hull.

Map:
  Contains all variables and methods needed to keep track of the map and samples RRT* makes. As well as enough
  to visualize the results

RRT*:
  is RRT*. Uses KDTree

KDTree:
  is KDTree.
