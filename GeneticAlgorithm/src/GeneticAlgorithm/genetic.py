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


def binary_list_to_gray_list(binary_list):
    first = binary_list.copy()
    second = binary_list.copy()
    length = len(binary_list)
    first.pop(length - 1)
    first.insert(0, 0)
    return XOR(first, second)

def gray_list_to_binary_list(gray_list):
    gray = gray_list.copy()
    binary = [0 for _ in range(len(gray_list))]
    while 1 in gray: # пока в списке есть 1
        binary = XOR(binary, gray)
        gray.pop(len(gray) - 1)
        gray.insert(0, 0)
    return binary



def XOR(first_list, second_list):
    result = []
    for i in range(len(first_list)):
        if (first_list[i] == second_list[i]):
            result.append(0)
        else:
            result.append(1)
    return result


# Создание начальной популяции
def generate_population(population_size, chromosome_length, from_value, to_value, function_order):
    population = []
    for _ in range(population_size):
        population.append(generate_chromosome(chromosome_length, from_value, to_value, function_order))
    return population

def generate_chromosome(chromosome_length, from_value, to_value, function_order):
    chromosome = []
    while function_order > 0:
        chromosome.append(decimal_to_binary_list(random.randint(from_value, to_value), chromosome_length))
        function_order -= 1
    return chromosome
    


# Расчет значения функции приспособленности для каждого кандидата в популяции
def evaluate_population(population, fitness_function, restore_function):
    fitness_values = []
    for chromosome in population:
        x = gray_chromosome_to_decimal_chromosome(chromosome)
        fitness_values.append(fitness_function(list(map(lambda subchromosome : restore_function(subchromosome), x))))
    return fitness_values


# Декодирование хромосомы в значение x, y, ...
def gray_chromosome_to_decimal_chromosome(chromosome): # хромосома поподает в коде Грея (список списков из нулей и единиц)
    order = len(chromosome)
    decimal_chromosome = []
    for i in range(order):
        decimal_subchromosome = binary_list_to_decimal(gray_list_to_binary_list(chromosome[i]))
        decimal_chromosome.append(decimal_subchromosome)
    return decimal_chromosome

def get_nearest_2_power(number):
    power = 0
    while number > 2**power:
        power += 1
    return power 


def binary_list_to_decimal(subchromosome):
    string = ''.join(str(x) for x in subchromosome)
    return int('0b' + string, 2)

def decimal_to_binary_list(decimal, chromosome_length):
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
                chromosome[i][indexes[0]], chromosome[i][indexes[1]] = chromosome[i][indexes[1]], chromosome[i][indexes[0]]
    return chromosome


