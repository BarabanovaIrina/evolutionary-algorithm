import random
import statistics


def fitness(args):
    x, y = args
    return x ** 2 + y ** 2


def crossover(generation):
    while True:
        sr = random.SystemRandom()
        parent_1 = sr.choice(generation)
        parent_2 = sr.choice(generation)
        if parent_1 != parent_2:
            break
    return parent_1[0], parent_2[1]


def mutation(generation, delta):
    sr = random.SystemRandom()
    sign = sr.choice([-1, 1])
    parent = sr.choice(generation)
    child = (parent[0] + sign * delta, parent[1] + sign * delta)
    return child


def new_offspring(generation, retain_num, cross_num, mutation_num, delta):
    temp = [generation[x] for x in range(retain_num)]
    for _ in range(cross_num):
        temp.append(crossover(generation))
    for _ in range(mutation_num):
        temp.append(mutation(generation, delta))
    return temp


def optimization(retain_rate, crossover_rate, mutation_rate, delta, number_of_generations):
    number_of_individuals = 10
    generation = [(random.randint(1, 10), random.randint(1, 10),) for _ in range(number_of_individuals)]

    retain_num = int(len(generation) * retain_rate)
    cross_num = int(len(generation) * crossover_rate)
    mutation_num = int(len(generation) * mutation_rate)

    list_of_mins = []
    list_of_averages = []
    for _ in range(number_of_generations):
        fitness_values = list(map(fitness, generation))
        local_minimum = min(fitness_values)
        local_avg = statistics.mean(fitness_values)
        list_of_mins.append(local_minimum)
        list_of_averages.append(local_avg)
        sorted_generation = [x for _, x in sorted(zip(fitness_values, generation))]

        new_generation = new_offspring(sorted_generation, retain_num, cross_num, mutation_num, delta)
        generation = new_generation

    global_min = min(list_of_mins)
    global_avg = statistics.mean(list_of_averages)

    return {'list_of_mins': list_of_mins,
            'list_of_averages': list_of_averages,
            'global_min': global_min,
            'global_avg': global_avg,
            }

