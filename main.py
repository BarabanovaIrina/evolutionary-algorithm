# создание начальной популяции
import random
import statistics

import vizualization



# функция приспособленности
def fitness(args):
    x, y = args
    return x ** 2 + y ** 2


# функция скрещивания
def crossover(generation):
    while True:
        parent_1 = random.choice(generation)
        parent_2 = random.choice(generation)
        if parent_1 != parent_2:
            break
    return parent_1[0], parent_2[1]



# функция мутации
def mutation(generation, delta):
    sign = random.choice([-1, 1])
    parent = list(random.choice(generation))
    parent[0] = sign * delta
    parent[1] = sign * delta
    return tuple(parent)


def new_offspring(generation, retain_num, cross_num, mutation_num, delta):
    temp = [generation[x] for x in range(retain_num)]
    for _ in range(cross_num):
        temp.append(crossover(generation))
    for _ in range(mutation_num):
        temp.append(mutation(generation, delta))
    return temp


def main_function(generation, retain_num, cross_num, mutation_num, delta, number_of_generations):
    local_minimum = 0
    local_avg = 0
    list_of_mins = []
    list_of_averages = []
    for _ in range(number_of_generations):
        fitness_values = list(map(fitness, generation))
        local_minimum = min(fitness_values)
        local_avg = statistics.mean(fitness_values)
        list_of_mins.append(local_minimum)
        list_of_averages.append(local_avg)
        sorted_generation = [x for _, x in sorted(zip(fitness_values, generation))]

        new_generation = new_offspring(sorted_generation, retain_num, cross_num, mutation_num, delta)
        generation = new_generation

    global_min = min(list_of_mins)
    global_avg = statistics.mean(list_of_averages)

    with open('file.txt', 'w') as file:
        file.write(f'Минимумы всех поколений: {list_of_mins}\n')
        file.write(f'Средние всех поколений: {list_of_averages}\n')
        file.write(f'Глобальный минимум: {global_min}\n')
        file.write(f'Глобальное среднее: {global_avg}\n')

    vizualization.get_plot(number_of_generations, list_of_mins, list_of_averages)


number_of_individuals = 10
generation = [(random.randint(1, 10), random.randint(1, 10),) for _ in range(number_of_individuals)]

RATES = {'retain_rate': 0.2,
         'crossover_rate': 0.4,
         'mutation_rate': 0.4,
         }

META_DATA = {'retain_num': int(len(generation) * RATES['retain_rate']),
             'cross_num': int(len(generation) * RATES['crossover_rate']),
             'mutation_num': int(len(generation) * RATES['mutation_rate']),
             'delta': 10 ** (-3),
             'number_of_generations': 10,
             }

main_function(generation, **META_DATA)
