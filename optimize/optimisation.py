import random
import statistics
import pandas as pd
from collections import namedtuple


def fitness(args):
    x, y = args
    return x ** 2 + y ** 2


def fitness_booth_function(args):
    x, y = args
    return (x+2*y-7)**2+(2*x+y-5)


def fitness_matyas_function(args):
    x, y = args
    return 0.26*(x ** 2 + y ** 2)-0.48*x*y


def crossover(generation, random_seed=None):
    while True:
        random.seed(random_seed)
        first_parent = random.choice(generation)
        second_parent = random.choice(generation)
        if first_parent != second_parent:
            break
    return first_parent[0], second_parent[1]


def mutation(generation, delta, random_seed=None):
    random.seed(random_seed)
    sign = random.choice([-1, 1])
    parent = random.choice(generation)
    child = (parent[0] + sign * delta, parent[1] + sign * delta)
    return child


def init_generation(number_of_individuals):
    return [(random.randint(1, 10), random.randint(1, 10),) for _ in range(number_of_individuals)]


def init_uniform_generation():
    pass


def new_offspring(crossover_func, mutation_func, generation, meta_data):
    temp = [generation[x] for x in range(meta_data.retain_num)]
    for _ in range(meta_data.cross_num):
        temp.append(crossover_func(generation))
    for _ in range(meta_data.mutation_num):
        temp.append(mutation_func(generation, meta_data.delta))
    return temp


def optimization(init_generation, fitness_function, crossover_function, mutation_function, meta_data_for_optimization):
    generation = init_generation(meta_data_for_optimization.number_of_individuals)

    meta_data = namedtuple('meta_data_for_new_offspring', ['retain_num',
                                                           'cross_num',
                                                           'mutation_num',
                                                           'delta',
                                                           ])

    meta_data_for_new_offspring = meta_data(int(len(generation) * meta_data_for_optimization.retain_rate),
                                            int(len(generation) * meta_data_for_optimization.crossover_rate),
                                            int(len(generation) * meta_data_for_optimization.mutation_rate),
                                            meta_data_for_optimization.delta_for_mutation,
                                            )

    result_data = dict(list_of_mins=[], list_of_averages=[], global_min=None, global_avg=None)
    for _ in range(meta_data_for_optimization.number_of_generations):
        fitness_values = list(map(fitness_function, generation))
        local_minimum = min(fitness_values)
        local_avg = statistics.mean(fitness_values)
        result_data['list_of_mins'].append(local_minimum)
        result_data['list_of_averages'].append(local_avg)
        sorted_generation = [x for _, x in sorted(zip(fitness_values, generation))]

        new_generation = new_offspring(crossover_function,
                                       mutation_function,
                                       sorted_generation,
                                       meta_data_for_new_offspring)
        generation = new_generation

    result_data['global_min'] = min(result_data['list_of_mins'])
    result_data['global_avg'] = statistics.mean(result_data['list_of_averages'])

    return result_data


def convert_data_for_boxplot(data):
    return pd.DataFrame(data).T
