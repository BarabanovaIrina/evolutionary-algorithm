from optimize import optimisation, log, visualization
from collections import namedtuple

if __name__ == '__main__':
    meta_data = namedtuple('meta_data_for_optimization',
                           ['retain_rate',
                            'crossover_rate',
                            'mutation_rate',
                            'delta_for_mutation',
                            'number_of_generations',
                            'number_of_individuals'])
    meta_data_for_optimization = meta_data(0.2, 0.4, 0.4, 10 ** (-3), 10, 10)

    PATH = "./"
    name_of_result_file = 'file.txt'
    history_of_mins = dict()
    history_of_avgs = dict()
    global_data_for_plot = dict(global_min_history=[], global_avg_history=[], )
    log.clean_file(PATH, name_of_result_file)
    stat_data_of_generation = dict()
    for index in range(10):
        stat_data_of_generation = optimisation.optimization(optimisation.init_generation,
                                                            optimisation.fitness,
                                                            optimisation.crossover,
                                                            optimisation.mutation,
                                                            meta_data_for_optimization)
        log.write_to_file(PATH, index, **stat_data_of_generation, name=name_of_result_file)
        history_of_mins[f'history{index}'] = stat_data_of_generation['list_of_mins']
        history_of_avgs[f'history{index}'] = stat_data_of_generation['list_of_averages']
        global_data_for_plot['global_min_history'].append(stat_data_of_generation['global_min'])
        global_data_for_plot['global_avg_history'].append(stat_data_of_generation['global_avg'])
    min_data_for_boxplot = optimisation.convert_data_for_boxplot(history_of_mins)
    avg_data_for_boxplot = optimisation.convert_data_for_boxplot(history_of_avgs)
    visualization.box_with_whiskers(min_data_for_boxplot, avg_data_for_boxplot)
    visualization.get_plot_of_optimization(global_data_for_plot['global_min_history'],
                                           global_data_for_plot['global_avg_history'])