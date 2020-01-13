from main import init_evolution
from collections import namedtuple
import os
from datetime import datetime
from optimize.optimisation import (
    init_generation,
    fitness,
    crossover,
    uniform_crossover,
    arithmetic_crossover,
    laplace_crossover,
    mutation,
    power_mutation,
    mpt_mutation,
    roulette_wheel_selection,
    tournament_selection,
)
from optimize.log import write_run_params


def variance_check(meta_data_for_optimization, modules_block):
    if 'results' not in os.listdir('../'):
        os.mkdir('../results/')
    path_to_save = '../results/'
    dir_name = datetime.now().strftime("%m%d%Y_%H%M%S")
    whole_path = os.path.join(path_to_save, dir_name)
    os.mkdir(whole_path)
    write_run_params(whole_path, modules_block)
    init_evolution(meta_data_for_optimization, modules_block, dir_for_results=whole_path)


if __name__ == '__main__':
    meta_data = namedtuple('meta_data_for_optimization',
                           ['retain_rate',
                            'crossover_rate',
                            'mutation_rate',
                            'delta_for_mutation',
                            'number_of_generations',
                            'number_of_individuals',
                            'number_of_gens', ])

    modules_block_1 = dict(select_func=roulette_wheel_selection,
                           init_generation=init_generation,
                           fitness=fitness,
                           crossover_func=crossover,
                           mutate_func=mutation)
    modules_block_2 = dict(select_func=roulette_wheel_selection,
                           init_generation=init_generation,
                           fitness=fitness,
                           crossover_func=uniform_crossover,
                           mutate_func=mutation)
    modules_block_3 = dict(select_func=roulette_wheel_selection,
                           init_generation=init_generation,
                           fitness=fitness,
                           crossover_func=arithmetic_crossover,
                           mutate_func=mutation)
    modules_block_4 = dict(select_func=roulette_wheel_selection,
                           init_generation=init_generation,
                           fitness=fitness,
                           crossover_func=laplace_crossover,
                           mutate_func=mpt_mutation)
    meta_data_for_optimization = meta_data(0.2, 0.4, 0.4, 10 ** (-3), 10, 10, 2)
    variance_check(meta_data_for_optimization, modules_block_3)

