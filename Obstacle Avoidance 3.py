import math
import operator
import numpy
start, goal = (0, 2), (8, 3)
points = [start, goal]

def from_id_width(id, width):
    return (id % width, id // width)

def draw_tile(graph, id, style, width):
    r = "."
    if 'number' in style and id in style['number'] and id in points: r = "%d" % style['number'][id]
    elif 'point_to' in style and style['point_to'].get(id, None) is not None and id in points:
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
    elif 'start' in style and id == style['start']: r = "A"
    elif 'goal' in style and id == style['goal']: r = "Z"
    elif 'path' in style and id in style['path'] and id in points: r = "@"
    elif id in graph.walls: 
        r = "#"
        m = tuple(map(operator.add, id, (1,0)))
        n = tuple(map(operator.add, id, (0,1)))
        o = tuple(map(operator.add, id, (-1,0)))
        p = tuple(map(operator.add, id, (0,-1)))
        points.append(tuple((m)))
        points.append(tuple((n)))
        points.append(tuple((o)))
        points.append(tuple((p)))
    return r

def draw_grid(graph, width=2, **style):
    for y in range(graph.height):
        for x in range(graph.width):
            print("%%-%ds" % width % draw_tile(graph, (x, y), style, width), end="")
        print()

class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = []
    
    def in_bounds(self, id):
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height
    
    def passable(self, id):
        return id not in self.walls
    
    def neighbors(self, id):
        (x, y) = id
        results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1), (x+1, y+1), (x-1, y-1), (x+1, y-1), (x-1, y+1)]
        if (x + y) % 2 == 0: results.reverse() # aesthetics
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return results

class GridWithWeights(Grid):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.weights = {}
    
    def cost(self, from_node, to_node):
        if to_node == tuple(numpy.add((from_node), (1,1))) or to_node == tuple(numpy.add((from_node), (-1,-1))) or to_node == tuple(numpy.add((from_node), (-1,1))) or to_node == tuple(numpy.add((from_node), (1,-1))):
            return self.weights.get(to_node, 1.4)
        else:
            return self.weights.get(to_node, 1)

diagram4 = GridWithWeights(10, 10)
diagram4.walls = [(2,2), (2,3), (2,1), (7, 3), (7,4)]

import heapq

class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self):
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
    
    while not frontier.empty():
        current = frontier.get()
        
        if current == goal:
            break
        
        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost
                frontier.put(next, priority)
                came_from[next] = current
    
    return came_from, cost_so_far


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
    return math.sqrt((x2-x1)**2+(y2-y1)**2)

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

came_from, cost_so_far = a_star_search(diagram4, start, goal)
draw_grid(diagram4, width=3, point_to=came_from, start=start, goal=goal)
print()
draw_grid(diagram4, width=3, number=cost_so_far, start=start, goal=goal)
print()
draw_grid(diagram4, width=3, path=reconstruct_path(came_from, start=start, goal=goal))
print()
path=reconstruct_path(came_from, start=start, goal=goal)
print()
