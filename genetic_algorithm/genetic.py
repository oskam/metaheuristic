import sys
import math
import random
from time import time

start = time()


def reproduction(parent1, parent2):
    x = random.randint(1, int(len(parent1) / 2))
    y = random.randint(x + 1, len(parent2) - 1)

    ox = [city for city in parent2[y:] + parent2[:y] if city not in parent1[x:y]]

    return ox[len(parent1) - y:] + parent1[x:y] + ox[:len(parent1) - y]


def mutation(route, probability):
    for i in range(0, len(route)):
        if probability > random.uniform(0, 1):
            x = random.randint(0, len(route) - 1)
            route[i], route[x] = route[x], route[i]
    return route


def cost(route):
    c = distance[0][route[0] - 1]
    for i in range(0, len(route) - 1):
        c += distance[route[i] - 1][route[i + 1] - 1]
    return c + distance[route[len(route) - 1] - 1][0]


def tournament(size):
    winner = (float('inf'), 0)
    for x in random.sample(range(0, POP_SIZE), size):
        c = cost(population[x])
        if c < winner[0]:
            winner = (c, x)
    return winner


def hill_climbing(route, rounds):
    route = [1] + route + [1]
    for _ in range(0, rounds):
        x = random.randint(1, int(len(route) / 2))
        y = random.randint(x + 1, len(route) - 2)

        xx = route[x] - 1
        xp = route[x + 1] - 1
        xm = route[x - 1] - 1
        yy = route[y] - 1
        yp = route[y + 1] - 1
        ym = route[y - 1] - 1

        if (y - x > 1 and (- distance[xx][xp]
                           - distance[xm][xx]
                           - distance[yy][yp]
                           - distance[ym][yy]
                           + distance[yy][xm]
                           + distance[yy][xp]
                           + distance[xx][ym]
                           + distance[xx][yp]) < 0) \
                or (- distance[xm][xx]
                    - distance[yy][yp]
                    + distance[yy][xm]
                    + distance[xx][yp]) < 0:
            route[x], route[y] = route[y], route[x]

    return route[1:len(route)-1]


def greedy_solution():
    left = [i + 1 for i in range(1, NUM_CITIES)]
    greedy = [1]
    while len(greedy) != NUM_CITIES:
        closest = (float('inf'), 0, 0)
        for i, v in enumerate(left):
            c = distance[greedy[len(greedy)-1]-1][v-1]
            if c < closest[0]:
                closest = (c, v, i)
        greedy += [closest[1]]
        left = left[:closest[2]] + left[closest[2]+1:]
    return greedy[1:]

in_data = sys.stdin.readlines()

NUM_CITIES = int(float(in_data[0]))
POP_SIZE = int(math.ceil(math.sqrt(NUM_CITIES)))

data = [[float(l) for l in line.split()[1:NUM_CITIES + 1]] for line in in_data[1:NUM_CITIES + 1]]
max_time = float(in_data[NUM_CITIES + 1])

distance = [[math.hypot(x2 - x1, y2 - y1) for (x2, y2) in data] for (x1, y1) in data]
data = None

# population = [random.shuffle([i+1 for i in range(1, n)]) for _ in range(0, pop_size)]
# sequence = [i + 1 for i in range(1, NUM_CITIES)]
# print(greedy_solution())

# population = [mutation(hill_climbing(random.sample(sequence, NUM_CITIES - 1), 1000), 0.01) for _ in range(0, POP_SIZE)]

greedy_sol = greedy_solution()
population = [mutation(list(greedy_sol), 0.005) for _ in range(0, POP_SIZE)]

span = int(math.ceil((NUM_CITIES - 1) / 10))
# span = 100

for i in range(0, POP_SIZE):
    s = (i*span) % (NUM_CITIES-1)
    e = ((i+1)*span) % (NUM_CITIES-1)
    if s < e:
        population[i][s:e] = random.sample(population[i][s:e], len(population[i][s:e]))
    else:
        population[i][s:] = random.sample(population[i][s:], len(population[i][s:]))
        population[i][:e] = random.sample(population[i][:e], len(population[i][:e]))

new_population = [None for _ in range(0, POP_SIZE)]
the_best = min(map(lambda x: (cost(population[x]), x), range(0, POP_SIZE)))

generation = 0

TOURNAMENT_SIZE = int(math.ceil(POP_SIZE * 0.1))
MAX_GENERATIONS = 1000
MUTATION_PROBABILITY = 0.01

while time() - start < max_time - 1 and generation < MAX_GENERATIONS:
    for i in range(0, POP_SIZE):
        index1 = tournament(TOURNAMENT_SIZE)[1]
        index2 = tournament(TOURNAMENT_SIZE)[1]

        offspring1 = mutation(reproduction(population[index2], population[index1]), MUTATION_PROBABILITY)
        offspring2 = mutation(reproduction(population[index1], population[index2]), MUTATION_PROBABILITY)

        if cost(offspring1) < cost(offspring2):
            new_population[i] = offspring1
        else:
            new_population[i] = offspring2

    population = list(new_population)
    generation += 1
    best = min(map(lambda x: (cost(population[x]), x), range(0, POP_SIZE)))

    if best[0] < the_best[0]:
        the_best = best
        print(str(the_best[0]) + "\t" + str(generation))

        # print(best_cost)
        # for k in best_route:
        #     sys.stderr.write(str(k) + " ")

        # end = time()
        # print(end - start)
