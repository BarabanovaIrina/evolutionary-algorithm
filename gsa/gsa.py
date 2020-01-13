from SALib.sample import saltelli
from SALib.sample.morris import sample as morris_sample
from SALib.analyze import sobol
from SALib.analyze import morris
from optimize.optimisation import fitness_booth_function
import numpy as np

problem = {
    'num_vars': 2,
    'names': ['x', 'y'],
    'bounds': [[0, 10],
               [0, 10]]
}

param_sample_sobol = saltelli.sample(problem, 1000)


Y_sobol = np.zeros(param_sample_sobol.shape[0])

for index, X in enumerate(param_sample_sobol):
    Y_sobol[index] = fitness_booth_function(X)

Si = sobol.analyze(problem, Y_sobol, print_to_console=True)

param_sample_morris = morris_sample(problem, 1000)

Y_morris = np.zeros(param_sample_morris.shape[0])

for index, X in enumerate(param_sample_morris):
    Y_morris[index] = fitness_booth_function(X)

print()
print('Morris\n')

morris.analyze(problem, param_sample_morris, Y_morris, print_to_console=True)