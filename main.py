import optimization
import visualization

# if '__name__' == '__main__':
META_DATA = {'retain_rate': 0.2,
             'crossover_rate': 0.4,
             'mutation_rate': 0.4,
             'delta': 10 ** (-3),
             'number_of_generations': 10,
              }

for _ in range(10):
    stat_data_of_generation = optimization.optimization(**META_DATA)
optimization.write_to_file(**stat_data_of_generation)
visualization.get_plot(stat_data_of_generation['list_of_mins'], stat_data_of_generation['list_of_averages'])