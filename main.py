# создание начальной популяции
import random
import statistics
import matplotlib.pyplot as plt

number_of_individuals = 10
generation = [(random.randint(1, 10), random.randint(1, 10),) for _ in range(number_of_individuals)]
number_of_generations = 10
list_of_mins = []
list_of_averaes = []


# функция приспособленности
def fitness(args):
    x, y = args
    return x ** 2 + y ** 2


# функция скрещивания
def crossover(generation):
    while True:
        parent_1 = random.choice(generation)
        parent_2 = random.choice(generation)
        if parent_1!=parent_2:
            break
    return (parent_1[0], parent_2[1])


# функция мутации
def mutation(generation, delta):
    sign = random.choice([-1, 1])
    parent = list(random.choice(generation))
    parent[0] = sign * delta
    parent[1] = sign * delta
    return tuple(parent)


# функция генерирования списка скрещеных индивидов
def call_crossover(generation, cross_num):
    temp = []
    for _ in range(cross_num):
        temp.append(crossover(generation))
    return temp


# функция генереирования списка мутировавших индивидов
def call_mutation(generation, mutation_num, delta):
    temp = []
    for _ in range(mutation_num):
        temp.append(mutation(generation, delta))
    return temp


def generate_new_generation(new_gen, *args):
    for i in range(len(args)):
        new_gen.extend(args[i])


# block of constants
retain_rait = 0.2
retain_num = int(len(generation) * retain_rait)
crossover_rate = 0.4
cross_num = int(len(generation) * crossover_rate)
mutation_rate = 0.4
mutation_num = int(len(generation) * mutation_rate)
delta = 10**(-3)

for i in range(number_of_generations):
    fitness_values = list(map(fitness, generation))
    # print(fitness_values)
    LOCAL_MINIMUM = min(fitness_values)
    # print(LOCAL_MINIMUM)
    LOCAL_AVG = statistics.mean(fitness_values)
    # print(LOCAL_AVG)
    list_of_mins.append(LOCAL_MINIMUM)
    list_of_averaes.append(LOCAL_AVG)

    sorted_generation = [x for _, x in sorted(zip(fitness_values, generation))]

    retain_num = int(len(sorted_generation) * retain_rait)
    best_individuals = [sorted_generation[x] for x in range(retain_num)]

    cross_num = int(len(sorted_generation) * crossover_rate)
    crossover_result = call_crossover(sorted_generation, cross_num)

    mutation_num = int(len(sorted_generation) * mutation_rate)
    mutation_result = call_mutation(sorted_generation, mutation_num, delta)

    new_generation = []
    generate_new_generation(new_generation, best_individuals, crossover_result, mutation_result)
    generation = new_generation

GLOBAL_MINIMUM = min(list_of_mins)
GLOBAL_AVERAGE = statistics.mean(list_of_averaes)

# Vizualization
x = number_of_generations
y1 = list_of_mins
y2 = list_of_averaes
fig, ax = plt.subplots()

ax.plot(y1)
ax.plot(y2)

# Output
print('Минимумы всех поколений: ',list_of_mins)
print('Средние всех поколений: ',list_of_averaes)
print('Глобальный минимум: ', GLOBAL_MINIMUM)
print('Глобальное среднее: ', GLOBAL_AVERAGE)
plt.show()


# Отладочный
# print(LIST_OF_MINS)
# print(LIST_OF_AVGS)
# print(generation)
# print(best_individuals)
# print(crossover_result)
# print(mutation_result)
# print(new_generation)
