# -*- coding:utf-8 -*-
import random
import math


class Point(object):

    def __init__(self, x, y, width_way, direction):
        self.x = x
        self.y = y
        self.width_way = width_way
        self.direction = direction
        self.available_way = []


def get_max_x_and_y(data):  # Data - [[x,y], [x,y]] - противоположенные точки
    max_x = data[0][0]
    if data[1][0] > max_x:
        max_x = data[1][0]
    max_y = data[0][1]
    if data[1][1] > max_y:
        max_y = data[1][1]
    return [max_x, max_y]


def get_min_x_and_y(data):  # Data - [[x,y], [x,y]] - противоположенные точки
    min_x = data[0][0]
    if data[1][0] > min_x:
        min_x = data[1][0]
    min_y = data[0][1]
    if data[1][1] > min_y:
        min_y = data[1][1]
    return [min_x, min_y]


def generate_map():
    size_zone = 3000  # Размер всей игровой зоны
    size_start_zone = 8  # Размер стартовой зоны

    main_way = []

    start_zone_point = [
        random.randint(size_start_zone, size_zone-size_start_zone),
        random.randint(size_start_zone, size_zone-size_start_zone)
    ]  # Рандомные координаты стартовой зоны, с учётом её размеров

    minimal_distance = math.sqrt(
        (size_zone-size_start_zone - size_zone/2)**2 + (size_zone-size_start_zone - size_zone/2)**2
    )  # Минимально допустимое расстояние между стартовой зоной и конечной

    count = 0  # Для проверки числа вхождений ( Костыль )

    end_zone_point = [
        random.randint(size_start_zone, size_zone - size_start_zone),
        random.randint(size_start_zone, size_zone - size_start_zone)
    ]

    min_difference = 250  # Минимальная разница между X и Y

    while True:  # Костыльная генерация конечной точки, нужно переделать почитав про вхождение в окружность
        while (abs(end_zone_point[0]-start_zone_point[0]) <= min_difference) or (abs(end_zone_point[1]-start_zone_point[1]) <= min_difference):
            end_zone_point = [
                random.randint(size_start_zone, size_zone - size_start_zone),
                random.randint(size_start_zone, size_zone - size_start_zone)
            ]
        distance = math.sqrt((start_zone_point[0] - end_zone_point[0])**2 + (start_zone_point[1] - end_zone_point[1])**2)
        if minimal_distance <= distance:
            break

        count += 1
        if count > 20:  # если выпало 1500, 1500 и что-то около этого, что бы он не впадал в долгий цикл.
            start_zone_point = [
                random.randint(size_start_zone, size_zone - size_start_zone),
                random.randint(size_start_zone, size_zone - size_start_zone)
            ]
            count = 0

    start_zone = [
        [start_zone_point[0] - size_start_zone // 2, start_zone_point[1] - size_start_zone // 2],
        [start_zone_point[0] - size_start_zone // 2, start_zone_point[1] + size_start_zone // 2],
        [start_zone_point[0] + size_start_zone // 2, start_zone_point[1] + size_start_zone // 2],
        [start_zone_point[0] + size_start_zone // 2, start_zone_point[1] - size_start_zone // 2],

    ]  # Координаты стартовой зоны

    end_zone = [
        [end_zone_point[0] - size_start_zone // 2, end_zone_point[1] - size_start_zone // 2],
        [end_zone_point[0] - size_start_zone // 2, end_zone_point[1] + size_start_zone // 2],
        [end_zone_point[0] + size_start_zone // 2, end_zone_point[1] + size_start_zone // 2],
        [end_zone_point[0] + size_start_zone // 2, end_zone_point[1] - size_start_zone // 2]
    ]  # Координаты конечной зоны

    start_point = start_zone[0]
    current_distance = math.sqrt((start_point[0] - end_zone_point[0])**2 + (start_point[1] - end_zone_point[1])**2)

    for i in range(1, 4):
        if current_distance > math.sqrt((start_zone[i][0] - end_zone_point[0])**2 + (start_zone[i][1] - end_zone_point[1])**2):
            start_point = start_zone[i]  # Вычисление стартовой точки

    end_point = end_zone[0]
    current_distance = math.sqrt((end_point[0] - start_point[0]) ** 2 + (end_point[1] - start_point[1]) ** 2)

    for i in range(1, 4):
        if current_distance > math.sqrt((end_zone[i][0] - start_point[0]) ** 2 + (end_zone[i][1] - start_point[1]) ** 2):
            end_point = end_zone[i]  # Вычисление конечной точки

    distance_x = abs(start_point[0] - end_point[0])  # Расстояние которое нам нужно пройти по X
    distance_y = abs(start_point[1] - end_point[1])

    current_x = start_point[0]
    current_y = start_point[1]

    number_segments_x = 5  # Число на которое мы будем делить наше расстояние по X. Нужно будет впилить рандом!
    number_segments_y = 5

    distance_one_step_x = distance_x//number_segments_x  # Расстояние которые мы будем проходить за один шаг
    distance_one_step_y = distance_x//number_segments_y

    if start_point[0] > end_point[0]:
        direction_x = -1  # Направление движения по X, если на нужно уменьшать X - то умножение на -1 нас спасёт :3
    else:
        direction_x = 1

    if start_point[1] > end_point[1]:
        direction_y = -1
    else:
        direction_y = 1

    min_width_way = 2
    max_width_way = 6

    while current_x != end_point[0] and current_y != end_point[1]:
        if abs(number_segments_x - number_segments_y) > 1:  # Если движемся в одну сторону больше два и более шага.
            if number_segments_x < number_segments_y:  # Если X больше двигаемся по Y и наоборот.
                current_x += distance_one_step_y * direction_y
                main_way.append(Point(current_x, current_y, random.randint(min_width_way, max_width_way), 1))
                number_segments_y -= 1
            else:
                current_x += distance_one_step_x * direction_x
                main_way.append(Point(current_x, current_y, random.randint(min_width_way, max_width_way), 0))
                number_segments_x -= 1
        else:
            if random.randint(0, 1) == 0:  # Рандомное направление движения
                current_x += distance_one_step_x * direction_x
                main_way.append(Point(current_x, current_y, random.randint(min_width_way, max_width_way), 0))
                number_segments_x -= 1
            else:
                current_y += distance_one_step_y * direction_y
                main_way.append(Point(current_x, current_y, random.randint(min_width_way, max_width_way), 1))
                number_segments_y -= 1

        if number_segments_x == 1 or number_segments_y == 1:  # Если дошли до предпоследней точки
            if number_segments_x == 1:
                while number_segments_y != 1:
                    current_y += distance_one_step_y * direction_y
                    main_way.append(Point(current_x, current_y, random.randint(min_width_way, max_width_way), 1))
                    number_segments_y -= 1
            else:
                while number_segments_x != 1:
                    current_x += distance_one_step_x * direction_x
                    main_way.append(Point(current_x, current_y, random.randint(min_width_way, max_width_way), 0))
                    number_segments_x -= 1
            if random.randint(0, 1) == 0:  # Рандомные последние два шага, которые ведут в точные координаты конечной зоны
                current_x = end_point[0]
                main_way.append(Point(current_x, current_y, random.randint(min_width_way, max_width_way), 0))
                number_segments_x -= 1
                current_y = end_point[1]
                main_way.append(Point(current_x, current_y, random.randint(min_width_way, max_width_way), 1))
                number_segments_y -= 1
            else:
                current_y = end_point[1]
                main_way.append(Point(current_x, current_y, random.randint(min_width_way, max_width_way), 1))
                number_segments_y -= 1
                current_x = end_point[0]
                main_way.append(Point(current_x, current_y, random.randint(min_width_way, max_width_way), 0))
                number_segments_x -= 1

    for i in range(len(main_way)-1):
        if main_way[i].direction == 0:
            if random.randint(0, 1) == 0:
                shift_one = math.ceil(main_way[i].width_way/2)
                shift_two = math.floor(main_way[i].width_way/2)
            else:
                shift_one = math.floor(main_way[i].width_way/2)
                shift_two = math.ceil(main_way[i].width_way/2)

            main_way[i].available_way.append([main_way[i].x, main_way[i].y - shift_one])
            main_way[i].available_way.append([main_way[i].x, main_way[i].y + shift_two])
            main_way[i].available_way.append([main_way[i + 1].x, main_way[i + 1].y + shift_two])
            main_way[i].available_way.append([main_way[i + 1].x, main_way[i + 1].y - shift_one])

            print(i, ' ', main_way[i].available_way)

        else:
            if random.randint(0, 1) == 0:
                shift_one = math.ceil(main_way[i].width_way / 2)
                shift_two = math.floor(main_way[i].width_way / 2)
            else:
                shift_one = math.floor(main_way[i].width_way / 2)
                shift_two = math.ceil(main_way[i].width_way / 2)

            main_way[i].available_way.append([main_way[i].x - shift_one, main_way[i].y])
            main_way[i].available_way.append([main_way[i].x + shift_two, main_way[i].y])
            main_way[i].available_way.append([main_way[i + 1].x + shift_two, main_way[i + 1].y])
            main_way[i].available_way.append([main_way[i + 1].x - shift_one, main_way[i + 1].y])

    for i in range(1, len(main_way)-2):

        previous_max = get_max_x_and_y([main_way[i-1].available_way[0], main_way[i-1].available_way[2]])
        previous_min = get_min_x_and_y([main_way[i-1].available_way[0], main_way[i-1].available_way[2]])

        next_max = get_max_x_and_y([main_way[i + 1].available_way[0], main_way[i + 1].available_way[2]])
        next_min = get_min_x_and_y([main_way[i + 1].available_way[0], main_way[i + 1].available_way[2]])

        max_x_and_y = get_max_x_and_y([main_way[i + 1].available_way[0], main_way[i + 1].available_way[2]])
        min_x_and_y = get_min_x_and_y([main_way[i].available_way[0], main_way[i].available_way[2]])

        border = []
        border.append([min_x_and_y[0]-1, min_x_and_y[1]-1])
        border.append([min_x_and_y[0]-1, max_x_and_y[1]+1])
        border.append([max_x_and_y[0]+1, max_x_and_y[1]+1])
        border.append([max_x_and_y[0]+1, min_x_and_y[1]-1])

        if previous_min[0] < border[0][0] < previous_max[0] and previous_min[1] < border[0][1] < previous_max[1]:
            pass
        else:
            temp = [[border[0][0]]]

        for bla in range(border[0], border[1]):
            print(bla)

generate_map()
