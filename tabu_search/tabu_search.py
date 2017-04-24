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
penalty_length = math.ceil(math.log10(n))

# node is not tabbed when iteration - tabu[x] >= penalty_length,
# so when iteration < penalty_length we make sure that every node is untabbed by default
tabu = [-penalty_length] * n

neighbor_route = [0] * (n + 1)
neighbor_cost = 0

best_neighbor_route = list(best_route)
best_neighbor_cost = best_cost

def is_tabbed(x, y, iteration):
    return (iteration - tabu[x]) < penalty_length and (iteration - tabu[y]) < penalty_length


def is_aspiring(cost):
    return cost < best_neighbor_cost


max_time = 0.08*n+10

# print(time() - start)

for i in range(0, iterations):

    current_route = list(best_neighbor_route)
    current_cost = best_neighbor_cost

    neighbor_set_copy = list(neighbor_set)
    shuffle(neighbor_set_copy)

    checked_allowed_moves = 0

    while checked_allowed_moves < int(math.ceil(neighbors_to_check)) and len(neighbor_set_copy) > 0:
        x, y = neighbor_set_copy.pop()

        xx = current_route[x] - 1
        xp = current_route[x + 1] - 1
        xm = current_route[x - 1] - 1
        yy = current_route[y] - 1
        yp = current_route[y + 1] - 1
        ym = current_route[y - 1] - 1

        if y - x > 1:
            neighbor_cost = current_cost \
                            - distance[xx][xp] \
                            - distance[xm][xx] \
                            - distance[yy][yp] \
                            - distance[ym][yy] \
                            + distance[yy][xm] \
                            + distance[yy][xp] \
                            + distance[xx][ym] \
                            + distance[xx][yp]
        else:
            neighbor_cost = current_cost \
                            - distance[xm][xx] \
                            - distance[yy][yp] \
                            + distance[yy][xm] \
                            + distance[xx][yp]

        if (not is_tabbed(xx, yy, i)) or is_aspiring(neighbor_cost):

            if neighbor_cost <= best_neighbor_cost or checked_allowed_moves == 0:
                best_neighbor_route = list(current_route) #we want to still look for neighbors of current_route, so we edit copy of it
                best_neighbor_route[x], best_neighbor_route[y] = best_neighbor_route[y], best_neighbor_route[x]
                best_neighbor_cost = neighbor_cost

            checked_allowed_moves += 1

        tabu[xx] = i
        tabu[yy] = i


    # for x, y in neighbor_set_copy:
    #     tabu[current_route[x] - 1] = i
    #     tabu[current_route[y] - 1] = i

    if best_neighbor_cost <= best_cost:
        best_route = list(best_neighbor_route)
        best_cost = best_neighbor_cost
    elif len(neighbor_set_copy) == 0:
        break

    if time() - start > max_time:
        break

# end = time()
# print(end - start)

print(best_cost)
for k in best_route:
    sys.stderr.write(str(k) + " ")
