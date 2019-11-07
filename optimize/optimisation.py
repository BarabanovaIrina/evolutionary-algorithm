import random
import statistics
import pandas as pd
from collections import namedtuple
import numpy as np
from numpy.random import uniform, power
from optimize.visualization import three_d_scatter


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


def k_point_crossover(generation, random_seed=None):
    while True:
        random.seed(random_seed)
        first_parent = random.choice(generation)
        second_parent = random.choice(generation)
        if first_parent != second_parent:
            break

    first_child, second_child = list(), list()

    number_of_points = random.randint(1, 3)
    point_indices = []
    for _ in range(number_of_points):
        point_indices.append(random.randint(1, len(first_parent)-1))
    point_indices = list(set(sorted(point_indices)))

    first_child.extend(first_parent[:point_indices[0]])
    second_child.extend(second_parent[:point_indices[0]])
    for i in range(len(point_indices)):
        if i % 2 != 0:
            first_child.extend(first_parent[point_indices[i]:point_indices[i + 1]])
            second_child.extend(second_parent[point_indices[i]:point_indices[i + 1]])
        else:
            first_child.extend(second_parent[point_indices[i]:point_indices[i + 1]])
            second_child.extend(first_parent[point_indices[i]:point_indices[i + 1]])
    if len(point_indices) % 2 != 0:
        first_child.extend(second_parent[point_indices[-1]:])
        second_child.extend(first_parent[point_indices[-1]:])
    else:
        first_child.extend(first_parent[point_indices[-1]:])
        second_child.extend(second_parent[point_indices[-1]:])
    return tuple(first_child)


# TODO: second_child in all crossovers
def arithmetic_crossover(generation, random_seed=None):
    while True:
        random.seed(random_seed)
        first_parent = random.choice(generation)
        second_parent = random.choice(generation)
        if first_parent != second_parent:
            break

    first_child, second_child = list(), list()
    for index in range(len(first_parent)):
        alpha = uniform(low=0, high=1)
        first_child.append(alpha * first_parent[index] + (1 - alpha) * second_parent[index])
        second_child.append(alpha * second_parent[index] + (1 - alpha) * first_parent[index])
    return tuple(first_child)


def uniform_crossover(generation, random_seed=None):
    while True:
        random.seed(random_seed)
        first_parent = random.choice(generation)
        second_parent = random.choice(generation)
        if first_parent != second_parent:
            break

    first_child, second_child = list(), list()
    for index in range(len(first_parent)):
        coin = random.randint(0, 1)
        if coin == 1:
            first_child.append(first_parent[index])
            second_child.append(second_parent[index])
        else:
            first_child.append(second_parent[index])
            second_child.append(first_parent[index])
    return tuple(first_child)


def laplace_crossover(generation, random_seed=None):
    while True:
        random.seed(random_seed)
        first_parent = random.choice(generation)
        second_parent = random.choice(generation)
        if first_parent != second_parent:
            break

    first_child, second_child = list(), list()
    a = 0
    b = 0.5
    alpha = uniform(low=0, high=1)
    if alpha <= 0.5:
        beta = a - b*np.log(alpha)
    else:
        beta = a + b*np.log(alpha)
    for index in range(len(first_parent)):
        first_child.append(first_parent[index]+beta*abs(first_parent[index]-second_parent[index]))
        second_child.append(second_parent[index]+beta*abs(first_parent[index]-second_parent[index]))
    return tuple(first_child)


def heuristic_crossover(generation, fitness_func, random_seed=None):
    while True:
        random.seed(random_seed)
        first_parent = np.array(random.choice(generation))
        second_parent = np.array(random.choice(generation))
        if first_parent != second_parent and fitness_func(second_parent) >= fitness_func(first_parent):
            break
    alpha = uniform(low=0, high=1)
    child = alpha*(second_parent-first_parent)+second_parent
    return child


def mutation(generation, delta, random_seed=None):
    random.seed(random_seed)
    sign = random.choice([-1, 1])
    parent = random.choice(generation)
    child = (parent[0] + sign * delta, parent[1] + sign * delta)
    return child


# TODO: check lower and upper bounds
def mpt_mutation(generation, random_seed=None):
    random.seed(random_seed)
    parent = random.choice(generation)
    child = list()
    r_param = uniform(low=0, high=1)
    b_param = 1
    for gen in parent:
        lower_bound = random.randint(0, 5)
        upper_bound = random.randint(0, 5)
        t = (gen - lower_bound) / (upper_bound - lower_bound)
        if r_param < t:
            modified_t = t-t*((t-r_param)/t)**b_param
        elif r_param > t:
            modified_t = t+(1-t)*((r_param-t)/(1-t))
        else:
            modified_t = t
        child.append((1 - modified_t) * lower_bound + modified_t * upper_bound)
    return tuple(child)


def power_mutation(generation, random_seed=None):
    random.seed(random_seed)
    parent = random.choice(generation)
    child = list()
    s = power(0.5)
    alpha = uniform(low=0, high=1)
    for gen in parent:
        lower_bound = random.randint(0, 5)
        upper_bound = random.randint(0, 5)
        t = (gen - lower_bound) / (upper_bound - lower_bound)
        if t < alpha:
            child.append(gen - s * (gen - lower_bound))
        else:
            child.append(gen + s * (upper_bound - gen))

    return tuple(child)


def non_uniform_mutation(generation, random_seed=None):
    pass


# TODO: include number_of_gens
def init_generation(number_of_individuals, number_of_gens):
    return [(random.randint(1, 10), random.randint(1, 10)) for _ in range(number_of_individuals)]


# TODO: include number_of_gens
def init_uniform_generation(number_of_individuals, number_of_gens):
    return [tuple(uniform(low=0, high=1, size=2)) for _ in range(number_of_individuals)]


def new_offspring(select_func, fitness_func, crossover_func, mutation_func, generation, meta_data):
    print('start to creat new offspring')
    temp = select_func(generation, fitness_func, meta_data.retain_num)
    cross_pull = select_func(generation, fitness_func, len(generation))
    mutate_pull = select_func(generation, fitness_func, len(generation))
    for _ in range(meta_data.cross_num):
        print('start to crossover')
        temp.append(crossover_func(cross_pull))
    for _ in range(meta_data.mutation_num):
        print('start to mutate')
        temp.append(mutation_func(mutate_pull, meta_data.delta))
    return temp


def roulette_wheel_selection(generation, fitness_func, num, random_seed=None):
    random.seed(random_seed)
    fitness_values = list(map(fitness_func, generation))
    sum_of_fit_vals = sum(fitness_values)
    fit_prob = [f_v/sum_of_fit_vals for f_v in fitness_values]
    prob_intervals = [sum(fit_prob[:i+1]) for i in range(len(fit_prob))]
    offspring = list()
    temp=list()
    while True:
        alpha = random.random()
        for index, individual in enumerate(prob_intervals):
            if alpha < individual:
                offspring.append(generation[index])
                temp.append(individual)
        sorted_offspring = [x for _, x in sorted(zip(temp, offspring))]
        if len(sorted_offspring) >= num+1:
            break
    return offspring[:num+1]


def tournament_selection(generation, fitness_func, random_seed=None):
    random.seed(random_seed)
    offspring = list()
    for _ in range(len(generation)):
        k = random.randint(1, 8)
        tournament_table = [random.choice(generation) for _ in range(k)]
        fit_tournament = list(map(fitness_func, tournament_table))
        winner_index = fit_tournament.index(max(fit_tournament))
        offspring.append(tournament_table[winner_index])

    return offspring


# TODO: check sorted_generations (generator vs generator)
def optimization(select_func, init_generation, fitness_function, crossover_function, mutation_function, meta_data_for_optimization):
    generation = init_generation(meta_data_for_optimization.number_of_individuals,
                                 meta_data_for_optimization.number_of_gens)

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
    for i in range(meta_data_for_optimization.number_of_generations):
        fitness_values = list(map(fitness_function, generation))
        local_minimum = min(fitness_values)
        local_avg = statistics.mean(fitness_values)
        result_data['list_of_mins'].append(local_minimum)
        result_data['list_of_averages'].append(local_avg)
        sorted_generation = [x for _, x in sorted(zip(fitness_values, generation))]

        print(i)
        new_generation = new_offspring(select_func,
                                       fitness_function,
                                       crossover_function,
                                       mutation_function,
                                       sorted_generation,
                                       meta_data_for_new_offspring)
        three_d_scatter(new_generation)
        generation = new_generation

    result_data['global_min'] = min(result_data['list_of_mins'])
    result_data['global_avg'] = statistics.mean(result_data['list_of_averages'])

    return result_data


def convert_data_for_boxplot(data):
    return pd.DataFrame(data).T
