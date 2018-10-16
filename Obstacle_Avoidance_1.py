# utility functions for dealing with square grids
def from_id_width(id, width):
    return (id % width, id // width)

def draw_tile(graph, id, style, width):
    r = "."
    if 'number' in style and id in style['number']: r = "%d" % style['number'][id]
    if 'point_to' in style and style['point_to'].get(id, None) is not None: # determines which direction the most optimal path is [see notes]
        (x1, y1) = id
        (x2, y2) = style['point_to'][id]
        if x2 == x1 + 1 and y2 == y1 + 1: r = "↘"
        elif x2 == x1 - 1 and y2 == y1 - 1: r = "↖"
        elif x2 == x1 + 1 and y2 == y1 - 1: r = "↗"
        elif x2 == x1 - 1 and y2 == y1 + 1: r = "↙"
        elif x2 == x1 + 1: r = "→"
        elif x2 == x1 - 1: r = "←"
        elif y2 == y1 + 1: r = "↓"
        elif y2 == y1 - 1: r = "↑"
    if 'start' in style and id == style['start']: r = "A" # marks the starting point with an A
    if 'goal' in style and id == style['goal']: r = "Z" # marks the goal point with a Z
    if 'path' in style and id in style['path']: r = "@" # marks 'path' with @
    if id in graph.walls: r = "#" * width # marks obstacles with a pound symbol
    return r

def draw_grid(graph, width=2, **style): # prints the graph to console
    for y in range(graph.height):
        for x in range(graph.width):
            print("%%-%ds" % width % draw_tile(graph, (x, y), style, width), end="")
        print()
        
# This class exists to define a two-dimensonal grid system.
class SquareGrid:
    def __init__(self, width, height): # Upon calling SquareGrid, a width and height must be initialized
        self.width = width
        self.height = height
        self.walls = []
    
    def in_bounds(self, id): # QA tester to see if inputted values are possible (e.g., not out of bounds)
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height
    
    def passable(self, id): # checks if the inputted point is a wall
        return id not in self.walls
    
    def neighbors(self, id):
        (x, y) = id
        results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1), (x+1, y+1), (x-1, y-1), (x+1, y-1), (x-1, y+1)]
        if (x + y) % 2 == 0: results.reverse() # aesthetics
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return results

class GridWithWeights(SquareGrid):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.weights = {}
    
    def cost(self, from_node, to_node):
        return self.weights.get(to_node, 1)

diagram4 = GridWithWeights(10, 10)
diagram4.walls = [(1, 7), (1, 8), (2, 7), (2, 8), (3, 7), (3, 8), (6,5), (5,5), (4,6)]

import heapq #https://docs.python.org/2/library/heapq.html

class PriorityQueue:
    def __init__(self):
        self.elements = [] # upon creating a PriorityQueue, array elements is created
    
    def empty(self): # returns true if self.elements is empty
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]

def dijkstra_search(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0
    
    while not frontier.empty(): # will run only if
        current = frontier.get()
        
        if current == goal: # if the testing point is the goal point, end the program
            break
        
        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost
                frontier.put(next, priority)
                came_from[next] = current
    
    return came_from, cost_so_far

# thanks to @m1sp <Jaiden Mispy> for this simpler version of
# reconstruct_path that doesn't have duplicate entries

def reconstruct_path(came_from, start, goal):
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start) # optional
    path.reverse() # optional
    return path

def heuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)

def a_star_search(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0
    
    while not frontier.empty():
        current = frontier.get()
        
        if current == goal:
            break
        
        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                frontier.put(next, priority)
                came_from[next] = current
    
    return came_from, cost_so_far

#from implementation import *
start, goal = (1, 4), (7, 8)
came_from, cost_so_far = a_star_search(diagram4, start, goal)
draw_grid(diagram4, width=3, point_to=came_from, start=start, goal=goal)
print()
draw_grid(diagram4, width=3, number=cost_so_far, start=start, goal=goal)
print()
