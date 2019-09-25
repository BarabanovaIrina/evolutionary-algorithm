from collections import namedtuple

from optimize import log
from optimize.optimisation import (
    optimization,
    init_generation,
    fitness_matyas_function,
    crossover,
    mutation,
    convert_data_for_boxplot
)
from optimize.visualization import (
    box_with_whiskers,
    get_plot_of_optimization
)

if __name__ == '__main__':
    meta_data = namedtuple('meta_data_for_optimization',
                           ['retain_rate',
                            'crossover_rate',
                            'mutation_rate',
                            'delta_for_mutation',
                            'number_of_generations',
                            'number_of_individuals'])
    meta_data_for_optimization = meta_data(0.2, 0.4, 0.4, 10 ** (-3), 100, 10)

    PATH = "./"
    name_of_result_file = 'file.txt'
    history_of_mins = dict()
    history_of_avgs = dict()
    global_data_for_plot = dict(global_min_history=[], global_avg_history=[], )
    log.clean_file(PATH, name_of_result_file)
    stat_data_of_generation = dict()
    for index in range(10):
        stat_data_of_generation = optimization(init_generation, fitness_matyas_function, crossover, mutation,
                                               meta_data_for_optimization)
        log.write_to_file(PATH, index, **stat_data_of_generation, name=name_of_result_file)
        history_of_mins[f'history{index}'] = stat_data_of_generation['list_of_mins']
        history_of_avgs[f'history{index}'] = stat_data_of_generation['list_of_averages']
        global_data_for_plot['global_min_history'].append(stat_data_of_generation['global_min'])
        global_data_for_plot['global_avg_history'].append(stat_data_of_generation['global_avg'])
    min_data_for_boxplot = convert_data_for_boxplot(history_of_mins)
    avg_data_for_boxplot = convert_data_for_boxplot(history_of_avgs)
    box_with_whiskers(min_data_for_boxplot, avg_data_for_boxplot)
    get_plot_of_optimization(global_data_for_plot['global_min_history'],
                             global_data_for_plot['global_avg_history'])
