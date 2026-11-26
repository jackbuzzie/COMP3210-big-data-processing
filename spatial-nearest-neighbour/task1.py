# shop.txt

# Imports

from math import sqrt
from time import perf_counter

# Load data

query_file = "query_points.txt"
shop_file = "shop.txt"

def load_points(path):
    points = []
    with open(path, "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 3: # skip malformed lines
                p_id = int(parts[0])
                x = float(parts[1])
                y = float(parts[2])
                points.append((p_id, x, y)) # store as tuple
    return points # return list of tuples

queries = load_points(query_file)
shops = load_points(shop_file)

# Distance (Euclidean)

def distance(p1, p2):
    return sqrt((p1[1] - p2[1])**2 + (p1[2] - p2[2])**2)

# Sequential Scan Based Method

def sequential_scan(queries, dataset):
    start = perf_counter()
    results = []

    for q in queries:
        nearest = None
        best_dist = float("inf") # initialise best distance as infinity

        for p in dataset:
            d = distance(q, p)
            if d < best_dist: # if this shop is closer than the current best
                best_dist = d # update the best distance
                nearest = p # update the nearest shop

        results.append((q[0], nearest))

    elapsed = perf_counter() - start
    return results, elapsed

# R Tree

class RTreeNode:
    def __init__(self, points=None, children=None):
        self.points = points or [] # points stored at this node (leaf nodes)
        self.children = children or [] # child nodes
        self.leaf = len(self.children) == 0 # node is a leaf if it has no children

        # calculate MBR from
        xs = [p[1] for p in self.points] if self.leaf else [ # 1) points if leaf
            c.mbr[0] for c in self.children # 2) children's MBR if internal
        ] + [c.mbr[2] for c in self.children]        

        ys = [p[2] for p in self.points] if self.leaf else [
            c.mbr[1] for c in self.children
        ] + [c.mbr[3] for c in self.children]

        self.mbr = (min(xs), min(ys), max(xs), max(ys))

def build_rtree(points, leaf_size=50):
    points = sorted(points, key = lambda p: p[1]) # sort points by x coordiantes

    # create leaf nodes, each with at most 50 points
    nodes = []
    for i in range(0, len(points), leaf_size):
        nodes.append(RTreeNode(points=points[i:i+leaf_size]))

    # group nodes into parent nodes until one root remains
    while len(nodes) > 1:
        parents = []
        for i in range(0, len(nodes), leaf_size):
            group = nodes[i:i+leaf_size]
            if len(group) == 1:
                parents.append(group[0])
            else:
                parents.append(RTreeNode(children=group))
        nodes = parents
    
    return nodes[0] # return the root node

def min_dist_to_mbr(query, mbr):
    x, y = query[1], query[2]
    xmin, ymin, xmax, ymax = mbr

    dx = max(xmin - x, 0, x - xmax) # horizontal distance to MBR, 0 if inside
    dy = max(ymin - y, 0, y - ymax) # vertical distance to MBR, 0 if inside

    return sqrt(dx*dx + dy*dy)

# Branch-and-Bound (BaB) Algorithm

def bab_search(root, query):
    best_point = None
    best_dist = float("inf") # initalise best distance as infinity

    stack = [root] # use stack to iteratively traverse the R-tree

    while stack:
        node = stack.pop() # take the next node to explore

        # prune if closest min dist to mbr is further than current best dist
        if min_dist_to_mbr(query, node.mbr) >= best_dist:
            continue

        if node.leaf:
            for p in node.points: # check every point in leaf
                d = distance(query, p)
                if d < best_dist: # update best point if necessary
                    best_dist = d
                    best_point = p
        
        else:
            # sort children by MBR distance so closest regions are explored fist
            children = sorted(
                node.children,
                key=lambda c: min_dist_to_mbr(query, c.mbr)
            )
            stack.extend(reversed(children)) # closest child last so it's popped first
    
    return best_point

def bab_algorithm(queries, dataset):
    start = perf_counter()
    root = build_rtree(dataset) # build R-tree over all shop points
    results = []
    # start = perf_counter()

    for q in queries:
        nearest = bab_search(root, q)
        results.append((q[0], nearest))

    elapsed = perf_counter() - start
    return results, elapsed

# BaB with Divide-and-Conquer

def bab_divide_and_conquer(queries, dataset):
    start = perf_counter()
    dataset_sorted = sorted(dataset, key=lambda p: p[1]) # sort dataset by x coordinates
    mid = len(dataset_sorted) // 2 # find the midpoint index
    split_x = dataset_sorted[mid][1] # x value of the partition

    left = dataset_sorted[:mid] # left half = points with smaller x values
    right = dataset_sorted[mid:] # right half = points with larger  x values

    left_tree = build_rtree(left) # build R-tree for left half
    right_tree = build_rtree(right) # build R-tree for right half

    results = []

    # start = perf_counter()

    for q in queries:
        # search the half the query is in first
        if q[1] <= split_x: # query is in the left half
            nearest = bab_search(left_tree, q) # search the left tree first
            if abs(q[1] - split_x) < distance(q, nearest):
                candidate = bab_search(right_tree, q) # search right tree if boundary is better than current best
                if distance(q, candidate) < distance(q, nearest):
                    nearest = candidate
                   
        else: # query is in the right half
            nearest = bab_search(right_tree, q) # search the right tree first
            if abs(q[1] - split_x) < distance(q, nearest): 
                candidate = bab_search(left_tree, q) # search left tree if boundary is closer than current best
                if distance(q, candidate) < distance(q, nearest):
                    nearest = candidate
                    
        results.append((q[0], nearest))

    elapsed = perf_counter() - start
    return results, elapsed

# Run
seq_results, seq_time = sequential_scan(queries, shops)
bab_results, bab_time = bab_algorithm(queries, shops)
dac_results, dac_time = bab_divide_and_conquer(queries, shops)

# Write
output_path = "task1_results.txt"

with open(output_path, "w") as f:
    # Sequential Scan
    f.write("SEQUENTIAL SCAN\n")
    for q, p in seq_results:
        f.write(
            f"id={p[0]}, x={p[1]:.2f}, y={p[2]:.2f} for query {q}\n"
        )
    f.write(f"\nTotal running time: {seq_time:.6f} seconds\n\n")

    # BaB
    f.write("BRANCH AND BOUND\n")
    for q, p in bab_results:
        f.write(
            f"id={p[0]}, x={p[1]:.2f}, y={p[2]:.2f} for query {q}\n"
        )
    f.write(f"\nTotal running time: {bab_time:.6f} seconds\n\n")

    # Divide and Conquer BaB
    f.write("DIVIDE AND CONQUER BAB\n")
    for q, p in dac_results:
        f.write(
            f"id={p[0]}, x={p[1]:.2f}, y={p[2]:.2f} for query {q}\n"
        )
    f.write(f"\nTotal running time: {dac_time:.6f} seconds\n")