#     Вариант фитнес функции (функции приспособления) 3:
#         X: [-15, -2]
#         Y: [-15, -2]
#         Z = 0.5*(X-3)*(Y-5)*(Y-1)*sin(Y)*cos(2*X)

from genetic import *


# Исходная функция
def fitness_function(x, y):
    return 0.5*(x-3)*(y-5)*(y-1)*sin(y)*cos(2*x)

def get_nearest_2_power(number):
    power = 0
    while number < 2**power:
        power =+ 1
    return power

# Генетический алгоритм
def genetic_algorithm(population_size, value_from, value_to, tournament_size, crossing_probability, mutation_probability, 
                      weak_will_win_probability, num_generations, fitness_function, function_order):
    points_amount = (value_to - value_from) / epsilon
    chromosome_length = get_nearest_2_power(points_amount)
    population = generate_population(population_size, chromosome_length, 0, points_amount - 1, function_order)
    for i in range(num_generations):
        fitness_values = evaluate_population(population, fitness_function, lambda subchromosome: restore_number(subchromosome, value_from, value_to, epsilon))
        parents = [selection(population, fitness_values, tournament_size, weak_will_win_probability) for _ in range(population_size)] # популяция сократилась в tournament_size раз
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
        best_decimal_chromosome = list(map(lambda subchromosome: restore_number(subchromosome, value_from, value_to, epsilon), gray_chromosome_to_decimal_chromosome(best_chromosome)))
        print(f"Поколение {i+1}:")
        print(f"Лучшее решение: x = {best_decimal_chromosome[0]}, y = {best_decimal_chromosome[1]}, f(x, y) = {best_fitness}")
        print("Хромосомы:")
        for chromosome in population:
            x = list(map(lambda subchromosome: restore_number(subchromosome, value_from, value_to, epsilon), gray_chromosome_to_decimal_chromosome(chromosome)))
            fitness = fitness_function(x)
            print(f"{chromosome} -> x = {x[0]}, y = {x[1]}, f(x, y) = {fitness}")
        print("="*20)

def fitness(x):
    return fitness_function(x[0], x[1])

def restore_number(number, value_from, value_to, epsilon):
    points_amount = (value_to - value_from) / epsilon
    return value_from + (number / points_amount) * (value_to - value_from)


if __name__ == '__main__':
    # Задаем параметры генетического алгоритма
    value_from = -15
    value_to = -2
    epsilon = 0.0001

    population_size = 11
    tournament_size = 2

    crossing_probability = 1
    mutation_probability = 0.008
    weak_will_win_probability = 0.000001

    num_generations = 20

    function_order = 2

    # Запускаем генетический алгоритм
    genetic_algorithm(population_size, value_from, value_to, tournament_size,
                       crossing_probability, mutation_probability, weak_will_win_probability, num_generations, fitness, function_order)
