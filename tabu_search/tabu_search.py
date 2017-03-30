import sys
import math
from random import randint

in_data = sys.stdin.readlines()

n = int(float(in_data[0]))
data = [[float(l) for l in line.split()[1:]] for line in in_data[1:]]

# print(n)
# print(data)

distance = [[math.hypot(x2 - x1, y2 - y1) for (x2, y2) in data] for (x1, y1) in data]

#print(distance)

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

    for determined_route_node in range(i + 1):
        distance_copy[int(current_node) - 1][current_route[determined_route_node] - 1] = inf

for j in range(0, len(current_route) - 1):
    # increase cost by distance from last to current node
    current_cost += distance[current_route[j] - 1][current_route[j + 1] - 1]

# current_cost += distance[current_route[n]-1][0]

#print(current_route)
print(current_cost)

best_route = list(current_route)
best_cost = current_cost

neighbor_set = [(x, y) for x in range(1, len(current_route) - 3) for y in (x + 1, len(current_route) - 2)]


# TSP TABU-SEARCH START
iterations = 100
checks = (math.sqrt(len(neighbor_set)))
p = 10

tabu = [-p] * n

neighbor_route = [0] * (n + 1)
neighbor_cost = 0

best_neighbor_route = list(best_route)
best_neighbor_cost = best_cost


def random_indexes(neighbor):
    x = randint(0, len(neighbor) - 1)
    return neighbor.pop(x)


def is_tabbed(x, y):
    return iterations - tabu[x] < p or iterations - tabu[y] < p


def swap(current, x, y):
    perm = list(current)
    perm[x], perm[y] = current[y], current[x]
    perm[y] = current[x]
    return perm


def count_cost(new_perm):
    cost = 0
    for x in range(0, len(new_perm)-1):
        cost += distance[new_perm[x] - 1][new_perm[x + 1] - 1]
    return cost


for i in range(0, iterations):

    current_route = list(best_neighbor_route)
    current_cost = best_neighbor_cost

    neighbor_set_copy = list(neighbor_set)

    checked = 0

    while checked < int(math.ceil(checks)) and len(neighbor_set_copy)>0:
        x, y = random_indexes(neighbor_set_copy)
        x, y = int(x), int(y)

        if not is_tabbed(current_route[x]-1, current_route[y]-1):
            checked += 1
            neighbor_route = list(current_route)
            neighbor_route[x], neighbor_route[y] = neighbor_route[y], neighbor_route[x]
            neighbor_cost = count_cost(neighbor_route)

            if neighbor_cost <= best_neighbor_cost:
                best_neighbor_route = list(neighbor_route)
                best_neighbor_cost = neighbor_cost

            tabu[current_route[x]-1] = i
            tabu[current_route[y]-1] = i
                # musimy dodać do tabu pozostałe sąsiedztwo obecnie badanego rozwiazania
                # for (x, y) in Ncopy:
                # zaktualizuj liste tabu dla current_route[x], current_route[y]

    if best_neighbor_cost <= best_cost:
        best_route = list(best_neighbor_route)
        best_cost = best_neighbor_cost

#print(best_route)
print(best_cost)
