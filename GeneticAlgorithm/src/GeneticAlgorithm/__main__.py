from genetic import *

if __name__ == '__main__':
    first = 10
    second = 9
    first_gray = decimal_to_gray(first)
    second_gray = decimal_to_gray(second)
    print('first = ' + str(first))
    print('first_gray = ' + str(bin(first_gray)[2:]))

    print('second = ' + str(second))
    print('second_gray = ' + str(bin(second_gray)[2:]))

    print('Обратно:')
    print('first_gray = ' + str(bin(first_gray)[2:]))
    print('first = ' + str(gray_to_decimal(first_gray)))
    print('second_gray = ' + str(bin(second_gray)[2:]))
    print('second = ' + str(gray_to_decimal(second_gray)))

    lst = generate_chromosome(10, 2)
    print(lst)
