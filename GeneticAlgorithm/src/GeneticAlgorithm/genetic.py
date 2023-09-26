# № в списке 10

#     Критерий 1 (критерий останова): 
#         Выполнение алгоритмом априорно заданного числа итераций
#     Скрещивание 1 (оператор скрещивания):
#         Одноточечное скрещивание
#     Мутация 2: 
#         Мутация обменом
#     Селекция 5: 
#         Турнирный отбор

from math import *
import random



def decimal_to_gray(decimal):
    return decimal ^ (decimal >> 1)


def gray_to_decimal(gray):
    binary = 0
    while (gray > 0):
        binary ^= gray
        gray >>= 1
    return binary 


# Создание начальной популяции
def generate_population(population_size, chromosome_length, from_value, to_value, function_order):
    population = []
    for _ in range(population_size):
        population.append(generate_chromosome(chromosome_length, from_value, to_value, function_order))
    return population

def generate_chromosome(chromosome_length, from_value, to_value, function_order):
    chromosome = []
    while function_order > 0:
        chromosome.append(decimal_to_subchromosome(random.randint(from_value, to_value), chromosome_length))
        function_order -= 1
    return chromosome
    


# Расчет значения функции приспособленности для каждого кандидата в популяции
def evaluate_population(population, fitness_function):
    fitness_values = []
    for chromosome in population:
        x = gray_chromosome_to_decimal_chromosome(chromosome)
        fitness_values.append(fitness_function(x))
    return fitness_values


# Декодирование хромосомы в значение x, y, ...
def gray_chromosome_to_decimal_chromosome(chromosome): # хромосома поподает в коде Грея
    order = len(chromosome)
    decimal_chromosome = []
    for i in range(order):
        subchromosome = list(gray_to_decimal(subchromsome_to_decimal(chromosome[i])))
        decimal_chromosome.append(subchromosome)
    return decimal_chromosome

    


def subchromsome_to_decimal(subchromosome):
    string = ''.join(str(x) for x in subchromosome)
    return int(string)

def decimal_to_subchromosome(decimal, chromosome_length):
    string = bin(decimal)[2:]
    lst = []
    chromosome = []
    for ch in string:
        lst.append(ch)
    if (len(lst) < chromosome_length):
        diff = chromosome_length - len(lst)
        for _ in range(diff):
            chromosome.append('0') # дополняем нулями, если длина недостаточна
    chromosome.extend(lst)
    return list(map(lambda ch: int(ch) , chromosome))


# селекция турнирным методом
def selection(population, fitness_values, tournament_size, weak_will_win_probability):
    tournament_participants = random.sample(range(len(population)), tournament_size) # выбираем tournament_size участников турнира из исходной популяции
    winner_index = tournament_participants[0]
    for i in tournament_participants[1:]:
        if (fitness_values[i] > fitness_values[winner_index]):
            if random.random() > weak_will_win_probability:
                winner_index = i
    return population[winner_index]


# Скрещивание (одноточечное)
def crossing(parent1, parent2, crossing_probability):
    if len(parent1) != len(parent2):
        return parent1, parent2
    child1 = []
    child2 = []
    for i in range(len(parent1)):
        if random.random() < crossing_probability:
            crossing_point = random.randint(1, len(parent1[i])-1) # точка скрещивания не может быть на концах хромосомы
            child1.append(parent1[i][:crossing_point] + parent2[i][crossing_point:])
            child2.append(parent2[i][:crossing_point] + parent1[i][crossing_point:])
        else:
            child1.append(parent1[i])
            child2.append(parent2[i])
    return child1, child2
    
    

# Мутация (обменом)
def mutate(chromosome, mutation_probability):
    for i in range(len(chromosome)):
        if random.random() < mutation_probability:
            if len(chromosome[i]) > 2:
                indexes = random.sample(range(len(chromosome[i])), 2)
                chromosome[i][indexes[0]], chromosome[indexes[1]] = chromosome[i][indexes[1]], chromosome[indexes[0]]
    return chromosome


