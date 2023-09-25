# № в списке 10

#     Вариант фитнес функции (функции приспособления) 3:
#         X: [-15, -2]
#         Y: [-15, -2]
#         Z = 0.5*(X-3)*(Y-5)*(Y-1)*sin(Y)*cos(2*X)
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


# Исходная функция
def fitness_function(x, y):
    return 0.5*(x-3)*(y-5)*(y-1)*sin(y)*cos(2*x)


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
def evaluate_population(population):
    fitness_values = []
    for chromosome in population:
        x = decode_chromosome(chromosome)
        fitness_values.append(fitness_function(x, 0))
    return fitness_values


# Декодирование хромосомы в значение x
def decode_chromosome(chromosome):
    n = len(chromosome)
    decimal_value = 0
    for i in range(n):
        decimal_value += chromosome[i] * (2**(n-i-1))
    x = decimal_value / (2**n-1) * 0.31
    return x


def chromsome_to_decimal(chromosome):
    string = ''.join(str(x) for x in chromosome)
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
def selection(population, fitness_values, tournament_size):
    tournament_participants = random.sample(range(len(population)), tournament_size) # выбираем tournament_size участников турнира из исходной популяции
    winner_index = tournament_participants[0]
    for i in tournament_participants[1:]:
        if (fitness_values[i] > winner_index):
            winner_index = fitness_values[i]
    return population[winner_index]


# Скрещивание (одноточечное)
def crossing(parent1, parent2, crossing_probability):
    if random.random() < crossing_probability:
        crossing_point = random.randint(1, len(parent1)-1) # точка скрещивания не может быть на концах хромосомы
        child1 = parent1[:crossing_point] + parent2[crossing_point:]
        child2 = parent2[:crossing_point] + parent1[crossing_point:]
        return child1, child2
    else:
        return parent1, parent2
    

# Мутация (обменом)
def mutate(chromosome, mutation_probability):
    if random.random() < mutation_probability:
        if len(chromosome) > 2:
            indexes = random.sample(range(len(chromosome)), 2)
            chromosome[indexes[0]], chromosome[indexes[1]] = chromosome[indexes[1]], chromosome[indexes[0]]
            # firstIndex = indexes[0]
            # secondIndex = indexes[1]
            # tmp = chromosome[firstIndex]
            # chromosome[firstIndex] = chromosome[secondIndex]
            # chromosome[secondIndex] = tmp
    return chromosome


# Генетический алгоритм
def genetic_algorithm(population_size, chromosome_length, tournament_size, crossing_probability, mutation_probability, num_generations):
    population = generate_population(population_size, chromosome_length)
    for i in range(num_generations):
        fitness_values = evaluate_population(population)
        parents = [selection(population, fitness_values, tournament_size) for i in range(population_size)]
        offspring = []
        for j in range(0, population_size-1, 2):
            parent1 = parents[j]
            parent2 = parents[j+1]
            child1, child2 = crossing(parent1, parent2, crossing_probability)
            child1 = mutate(child1, mutation_probability)
            child2 = mutate(child2, mutation_probability)
            offspring.append(child1)
            offspring.append(child2)
        population = offspring
        best_fitness = max(fitness_values)
        best_chromosome = population[fitness_values.index(best_fitness)-1]
        best_x = decode_chromosome(best_chromosome)
        print(f"Поколение {i+1}:")
        print(f"Лучшее решение: x = {best_x}, f(x) = {best_fitness}")
        print("Хромосомы:")
        for chromosome in population:
            x = decode_chromosome(chromosome)
            fitness = fitness_function(x, 0)
            print(f"{chromosome} -> x = {x}, f(x) = {fitness}")
        print("="*20)


# Задаем параметры генетического алгоритма
population_size = 11
chromosome_length = 5
tournament_size = 2
crossover_probability = 1
mutation_probability = 0.008
num_generations = 20


# Запускаем генетический алгоритм
#genetic_algorithm(population_size, chromosome_length, tournament_size, crossover_probability, mutation_probability, num_generations)


