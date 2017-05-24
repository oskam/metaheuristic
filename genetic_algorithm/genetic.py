import sys
import math
import random
from time import time

start = time()
in_data = sys.stdin.readlines()

n = int(float(in_data[0]))
data = [[float(l) for l in line.split()[1:n+1]] for line in in_data[1:n+1]]
max_time = float(in_data[n+1])

distance = [[math.hypot(x2 - x1, y2 - y1) for (x2, y2) in data] for (x1, y1) in data]

    # if time() - start > max_time - 1:
    #     break


print(best_cost)
for k in best_route:
    sys.stderr.write(str(k) + " ")

# end = time()
# print(end - start)