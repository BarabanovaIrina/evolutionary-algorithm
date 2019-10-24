from optimize import optimisation
import random
import pytest
import pandas as pd
import time
from collections import namedtuple


@pytest.fixture()
def generation_for_test():
    return [(3, 7), (9, 4), (10, 4), (5, 2), (7, 2), (7, 5), (8, 2), (8, 7), (2, 2), (6, 7)]


@pytest.fixture()
def generation_for_test_7():
    return ([1, 2, 3, 4, 5, 6, 7], [8,9,10,11,12,13,14], [15,16,17,18,19,20,21])


@pytest.fixture()
def meta_data_for_test_optimization():
    return namedtuple('meta_data_for_optimization',
                      ['retain_rate',
                       'crossover_rate',
                       'mutation_rate',
                       'delta_for_mutation',
                       'number_of_generations',
                       'number_of_individuals',
                       'number_of_gens',])


def test_fitness_correct():
    assert optimisation.fitness((1, 3)) == 10


def test_mutation_correct(generation_for_test):
    random.seed(1)
    delta = 10 ** (-3)
    sign = random.choice([-1, 1])
    parent = random.choice(generation_for_test)
    child = (parent[0] + sign * delta, parent[1] + sign * delta)
    assert optimisation.mutation(generation_for_test, delta, random_seed=1) == child


def test_crossover_correct(generation_for_test):
    random.seed(1)
    first_parent = random.choice(generation_for_test)
    second_parent = random.choice(generation_for_test)
    assert optimisation.crossover(generation_for_test, random_seed=1) == (first_parent[0], second_parent[1])


def test_init_generation_correct():
    assert len(optimisation.init_generation(10, 2)) == 10


def test_new_offspring(generation_for_test):
    meta_data = namedtuple('meta_data_for_new_offspring', ['retain_num',
                                                           'cross_num',
                                                           'mutation_num',
                                                           'delta',
                                                           ])
    cross_func = optimisation.crossover
    mutation_func = optimisation.mutation

    meta_data_for_offspring = meta_data(int(len(generation_for_test) * 0.2),
                                        int(len(generation_for_test) * 0.4),
                                        int(len(generation_for_test) * 0.4),
                                        10 ** (-3),
                                        )

    assert len(
        optimisation.new_offspring(cross_func, mutation_func, generation_for_test, meta_data_for_offspring)) == 10


def test_convert_data_to_dataframe():
    dict_data = dict()
    for index in range(10):
        dict_data[f'history{index}'] = [random.randint(1, 10) for _ in range(10)]
    assert optimisation.convert_data_for_boxplot(dict_data).size == pd.DataFrame(dict_data).T.size


def test_optimization_fitness(meta_data_for_test_optimization):
    meta_data_tuple = meta_data_for_test_optimization
    meta_data = meta_data_tuple(0.2, 0.4, 0.4, 10 ** (-3), 100, 10, 2)

    start_time = time.time()
    result = optimisation.optimization(optimisation.init_generation,
                                       optimisation.fitness,
                                       optimisation.crossover,
                                       optimisation.mutation,
                                       meta_data)
    end_time = time.time()
    assert end_time - start_time <= 1
    # assert result['global_min'] < 20


def test_optimization_booth_function(meta_data_for_test_optimization):
    meta_data_structure = meta_data_for_test_optimization
    meta_data = meta_data_structure(0.2, 0.4, 0.4, 10 ** (-3), 100, 10, 2)
    result = optimisation.optimization(optimisation.init_generation,
                                       optimisation.fitness_booth_function,
                                       optimisation.crossover,
                                       optimisation.mutation,
                                       meta_data)

    assert result['global_min'] < 10


def test_optimization_matyas_function(meta_data_for_test_optimization):
    meta_data_structure = meta_data_for_test_optimization
    meta_data = meta_data_structure(0.2, 0.4, 0.4, 10 ** (-3), 100, 10, 2)
    result = optimisation.optimization(optimisation.init_generation,
                                       optimisation.fitness_matyas_function,
                                       optimisation.crossover,
                                       optimisation.mutation,
                                       meta_data)
    assert result['global_min'] < 2


def test_optimization_init_uniform(meta_data_for_test_optimization):
    meta_data_structure = meta_data_for_test_optimization
    meta_data = meta_data_structure(0.2, 0.4, 0.4, 10 ** (-3), 100, 10, 2)
    result = optimisation.optimization(optimisation.init_uniform_generation,
                                       optimisation.fitness_matyas_function,
                                       optimisation.crossover,
                                       optimisation.mutation,
                                       meta_data)
    assert result['global_min'] < 1


def test_uniform_crossover(generation_for_test_7):
    random_seed = 1
    while True:
        random.seed(random_seed)
        first_parent = random.choice(generation_for_test_7)
        second_parent = random.choice(generation_for_test_7)
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

    assert tuple(first_child) == optimisation.uniform_crossover(generation_for_test_7, random_seed=1)


def test_roulette_wheel_selection(generation_for_test):
    random.seed(1)
    fitness_values = list((map(lambda x: x[0]**2+x[1]**2, generation_for_test)))
    f_sum = sum(fitness_values)
    prob = [f/f_sum for f in fitness_values]
    prob_intervals = [sum(prob[:i+1]) for i in range(len(prob))]
    offspring = list()
    r_number = random.random()
    for i, individual in enumerate(generation_for_test):
        if r_number < prob_intervals[i]:
            offspring.append(individual)
    assert offspring == optimisation.roulette_wheel_selection(generation_for_test, optimisation.fitness, random_seed=1)


def test_tournament_selection(generation_for_test):
    random.seed(1)
    offspring = list()
    for _ in range(len(generation_for_test)):
        k = random.randint(1,8)
        table = [random.choice(generation_for_test) for _ in range(k)]
        f_table = list(map(lambda x: x[0]**2+x[1]**2, table))
        winner_i = f_table.index(max(f_table))
        offspring.append(table[winner_i])

    assert offspring == optimisation.tournament_selection(generation_for_test, optimisation.fitness, random_seed=1)
