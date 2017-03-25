import sys
import math

in_data = sys.stdin.readlines()

n = int(float(in_data[0]))
data = [[float(l) for l in line.split()[1:]] for line in in_data[1:]]

# print(n)
# print(data)

distance = [[math.hypot(x2-x1, y2-y1) for (x2, y2) in data] for (x1, y1) in data]

# print(distance)

inf = float('inf')

current_route = [None]*(n+1)
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

# set current node to `current_route[0]` = 1
current_node = current_route[0]
# i is in range from 1 to n-1 because `current_route[0]` and `current_route[n]` are set to 1
for i in range(1, n):
    # set next visited node to index of node with minimum distance from last determined
    # `current_node-1` as python indexes from 0 when nodes are numbered from 1
    # increase calculated index by 1 for same reason as above
    current_route[i] = index_min(distance_copy, current_node-1) + 1
    # increase cost by distance from last to current node
    current_cost += distance[current_node-1][current_route[i]-1]
    # update `current_node` to one determined in this iteration
    current_node = current_route[i]
    # set distance from current node to node 1 to infinity to make sure we won't get back to 1 too soon
    distance_copy[current_node-1][0] = inf
    # for all nodes on route determined earlier set distance between current node and them to infinity
    # to make sure we won't visit one node more than one time
    for determined_route_node in range(i+1):
        distance_copy[int(current_node)-1][current_route[determined_route_node]-1] = inf

# increase cost by distance from last visited node to node 1 as we have to go back to start
current_cost += distance[current_route[n]-1][0]

print(current_route)
print(current_cost)

best_route = list(current_route)
best_cost = current_cost

# TSP TABU-SEARCH START
