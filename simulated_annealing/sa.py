import sys
import math
from random import shuffle
from time import time

start = time()
in_data = sys.stdin.readlines()

n = int(float(in_data[0]))
data = [[float(l) for l in line.split()[1:]] for line in in_data[1:]]

distance = [[math.hypot(x2 - x1, y2 - y1) for (x2, y2) in data] for (x1, y1) in data]

inf = float('inf')

current_route = [0] * (n + 1)
current_cost = 0

current_route[0] = 1
current_route[n] = 1

distance_copy = list()
for i in range(0, len(distance)):
    distance_copy.append(list(distance[i]))

for i, _ in enumerate(distance_copy):
    distance_copy[i][i] = inf

# returns index of minimum value in row `k` of `matrix`
def index_min(matrix, k):
    minimum = inf
    index = -1
    for ii, val in enumerate(matrix[k]):
        if val < minimum:
            minimum = val
            index = ii
    return index


current_node = current_route[0]

for i in range(1, len(current_route) - 1):

    current_route[i] = index_min(distance_copy, int(current_node) - 1) + 1
    current_node = current_route[i]
    distance_copy[int(current_node) - 1][0] = inf

    #forbid returns in next step to nodes already visited
    for determined_route_node in range(i + 1):
        distance_copy[int(current_node) - 1][current_route[determined_route_node] - 1] = inf

for j in range(0, len(current_route) - 1):
    current_cost += distance[current_route[j] - 1][current_route[j + 1] - 1]

# print(current_cost)

best_route = list(current_route)
best_cost = current_cost

neighbor_set = [(x, y) for x in range(1, len(current_route) - 3) for y in range(x + 1, len(current_route) - 2)]

iterations = int(n)
neighbors_to_check = (math.sqrt(len(neighbor_set)))


neighbor_route = [0] * (n + 1)
neighbor_cost = 0

best_neighbor_route = list(best_route)
best_neighbor_cost = best_cost


max_time = 0.08*n+10

# print(time() - start)



# end = time()
# print(end - start)

print(best_cost)
for k in best_route:
    sys.stderr.write(str(k) + " ")
