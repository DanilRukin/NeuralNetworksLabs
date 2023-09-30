#     Вариант фитнес функции (функции приспособления) 3:
#         X: [-15, -2]
#         Y: [-15, -2]
#         Z = 0.5*(X-3)*(Y-5)*(Y-1)*sin(Y)*cos(2*X)

from genetic import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from threading import Thread
from multiprocessing import Process


# Исходная функция
def fitness_function(x, y):
    return 0.5*(x-3)*(y-5)*(y-1)*sin(y)*cos(2*x)


# Генетический алгоритм
def genetic_algorithm(population_size, value_from, value_to, tournament_size, crossing_probability, mutation_probability, 
                      weak_will_win_probability, num_generations, fitness_function, function_order):
    points_amount = (value_to - value_from) / epsilon
    chromosome_length = get_nearest_2_power(points_amount)
    # создание популяции
    population = generate_population(population_size, chromosome_length, 0,
                                      2**chromosome_length, function_order)
    for i in range(num_generations):
        # оценка фитнес-функции для каждой хромосомы
        fitness_values = evaluate_population(population, fitness_function, lambda subchromosome: restore_number(subchromosome, value_from, value_to, epsilon))
        best_fitness = max(fitness_values)
        best_chromosome = population[fitness_values.index(best_fitness)]
        best_decimal_chromosome = list(map(lambda subchromosome: restore_number(subchromosome, value_from, value_to, epsilon), gray_chromosome_to_decimal_chromosome(best_chromosome)))
        print(f"Поколение {i+1}:")
        print(f"Лучшее решение: x = {best_decimal_chromosome[0]}, y = {best_decimal_chromosome[1]}, f(x, y) = {best_fitness}")
        print("Хромосомы:")
        for chromosome in population:
            x = list(map(lambda subchromosome: restore_number(subchromosome, value_from, value_to, epsilon), gray_chromosome_to_decimal_chromosome(chromosome)))
            fitness = fitness_function(x)
            print(f"{chromosome} -> x = {x[0]}, y = {x[1]}, f(x, y) = {fitness}")
        print("="*20)

        offsprings = []
        for j in range(0, population_size-1, 2):
            parent1 = population[j]
            parent2 = population[j+1]
            # скрещивание
            child1, child2 = crossing(parent1, parent2, crossing_probability)
            # мутации
            child1 = mutate(child1, mutation_probability)
            child2 = mutate(child2, mutation_probability)
            offsprings.append(child1)
            offsprings.append(child2)
        population.extend(offsprings)
        # отбор турнирным методом
        population = [selection(population, evaluate_population(population, fitness_function, lambda subchromosome: restore_number(subchromosome, value_from, value_to, epsilon)),
                                 tournament_size, weak_will_win_probability) for _ in range(population_size)] # размер популяции не изменится
        

def fitness(x):
    return fitness_function(x[0], x[1])

def restore_number(number, value_from, value_to, epsilon):
    points_amount = (value_to - value_from) / epsilon
    power = get_nearest_2_power(points_amount)
    return value_from + number * ((value_to - value_from) / (2**power - 1))

def np_fitness(x):
    return 0.5*(x[0]-3)*(x[1]-5)*(x[1]-1)*np.sin(x[1])*np.cos(2*x[0])

def show_fitness(value_from, value_to, step, np_fitness):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')  # параметры контейнера для вывода графика

    # Подготовка данных
    X = np.arange(value_from, value_to, step)
    Y = np.array(X)
    X, Y = np.meshgrid(X, Y)    # расширение векторов X,Y в матрицы
    Z = np_fitness([X, Y])

    # Построение графика
    ax.plot_surface(X, Y, Z)    # метод для отрисовки графиков с параметрами по умолчанию
    plt.show()


if __name__ == '__main__':
    # Задаем параметры генетического алгоритма
    value_from = -15
    value_to = -2
    epsilon = 0.01

    population_size = 11
    tournament_size = 2

    crossing_probability = 1
    mutation_probability = 0.008
    weak_will_win_probability = 0.000001

    num_generations = 200

    function_order = 2
    th = Process(target=show_fitness, args=(value_from, value_to, 0.25, np_fitness))
    th.start()
    #show_fitness(value_from, value_to, 0.25, np_fitness)
    # Запускаем генетический алгоритм
    genetic_algorithm(population_size, value_from, value_to, tournament_size,
                       crossing_probability, mutation_probability, weak_will_win_probability, num_generations, fitness, function_order)

