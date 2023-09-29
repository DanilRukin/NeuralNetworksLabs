from genetic import *

if __name__ == '__main__':
    print(binary_list_to_decimal([1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0]))
    number = 130000
    print('nearest 2 power of ' + str(number) + ' is ' + str(get_nearest_2_power(number)))

