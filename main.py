import optimisation
import visualization
import pandas as pd
import log

if __name__ == '__main__':
    META_DATA = {'retain_rate': 0.2,
                 'crossover_rate': 0.4,
                 'mutation_rate': 0.4,
                 'delta': 10 ** (-3),
                 'number_of_generations': 10,
                  }

    history_of_mins = {}
    log.clean_file()
    for index in range(10):
        stat_data_of_generation = optimisation.optimization(**META_DATA)
        log.write_to_file(index, **stat_data_of_generation)
        history_of_mins[f'history{index}'] = stat_data_of_generation['list_of_mins']
    data_to_boxplot = pd.DataFrame(history_of_mins).T
    visualization.box_with_whiskers(data_to_boxplot)
    visualization.get_plot(stat_data_of_generation['list_of_mins'], stat_data_of_generation['list_of_averages'])
