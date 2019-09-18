from optimize import optimisation
import random
import pytest
import pandas as pd
import time


@pytest.fixture()
def t_generation():
    return [(3, 7), (9, 4), (10, 4), (5, 2), (7, 2), (7, 5), (8, 2), (8, 7), (2, 2), (6, 7)]


def test_fitness_correct():
    assert optimisation.fitness((1, 3)) == 10


def test_mutation_correct(t_generation):
    random.seed(1)
    delta = 10 ** (-3)
    sign = random.choice([-1, 1])
    parent = random.choice(t_generation)
    child = (parent[0] + sign * delta, parent[1] + sign * delta)
    assert optimisation.mutation(t_generation, delta, random_seed=1) == child


def test_crossover_correct(t_generation):
    random.seed(1)
    parent_1 = random.choice(t_generation)
    parent_2 = random.choice(t_generation)
    assert optimisation.crossover(t_generation, random_seed=1) == (parent_1[0], parent_2[1])


def test_init_generation_correct():
    assert len(optimisation.init_generation(10)) == 10


def test_new_offspring(t_generation):
    delta = 10 ** (-3)
    retain_num = int(len(t_generation) * 0.2)
    crossover_num = int(len(t_generation) * 0.4)
    mutation_num = int(len(t_generation) * 0.4)
    assert len(optimisation.new_offspring(t_generation, retain_num, crossover_num, mutation_num, delta)) == 10


def test_convert_data_to_dataframe():
    dict_data = dict()
    for index in range(10):
        dict_data[f'history{index}'] = [random.randint(1, 10) for _ in range(10)]
    assert optimisation.convert_data_for_boxplot(dict_data).size == pd.DataFrame(dict_data).T.size


def test_optimization():
    retain_rate = 0.2
    crossover_rate = 0.4
    mutation_rate = 0.4
    delta = 10 ** (-3)
    number_of_generations = 10
    number_of_individuals = 10
    start_time = time.time()
    optimisation.optimization(retain_rate, crossover_rate, mutation_rate,
                              delta, number_of_generations, number_of_individuals)
    end_time = time.time()
    assert end_time - start_time <= 1





