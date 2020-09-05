# Данный скрипт является интелектуальной собственностью Бабушкина Владислава Вячеславовича
# Распространяется на свободной основе на базе лицензии GNU v3
# https://github.com/MrWindmark/XML_Creator/tree/MrWindmark-ver1.0
import os
from line_editor import edited_data


# функция поиска строки в файле
def line_searching(pool_to_search: str, place_to_search: list):
    # проходимся по всем строчкам файла
    for sch_line in place_to_search:
        # если строка содержит искомую
        if pool_to_search in sch_line:
            # возвращаем значение индекса строки, где нашли искомую строчку. цикл при этом завершается
            return place_to_search.index(sch_line)


# функция поиска подстроки в найденном пуле
def sline_searching(main_lines, start_pos: int, line_to_search):
    for n in range(start_pos, len(main_lines)):
        if line_to_search in main_lines[n]:
            return n


# здесь считается число пробелов, необходимых для центрования строки
def space_fill(str_to_check: str):
    if len(str_to_check) < 24:
        space = '&#032;' + (' ' * ((23 - len(str_to_check)) // 2))
    # если же равно - смысла центровать просто нет
    elif len(str_to_check) >= 24:
        space = ''
    return space

# Осуществляем чтение данных конфиг.файла из текущей директории
with open(f'{os.getcwd()}/for_script/Carwash_standart_2005.xml', 'r', encoding='windows-1251') as f:
    r_data = f.read().splitlines()

# список пулов, которые мы обрабатываем: 2-й Unipos, 3-й для моек, 5-й для чека и 16-й для часового пояса
# формат: [искомый пул, следующий за искомым]
pools = [
    '<pool_header ID="2">',  # 0
    '<pool_header ID="3">',  # 1
    '<pool_header ID="5">',  # 2
    '<pool_header ID="16">'  # 3
]

data_dict = {
    'unipos': '<parameter ID="152">',  # 0
    'inn': '<parameter ID="105">',  # 1
    'adr': '<parameter ID="106">',  # 2
    'name': '<parameter ID="31340">',  # 3
    'brand': '<parameter ID="31341">',  # 4
    'gmt': '<parameter ID="3476">'  # 5
}

# поиск по arrows в пределах значений позиций строк pool2, ищем строку с параметром unipos
# test = subline_srchr(arrows, pool2, data_dict.get('unipos'))
# print(f'Строка {test + 3} unipos')
# print(arrows[test+2])
# test = subline_srchr(arrows, pool5, data_dict.get('inn'))
# print(f'Строка {test + 4} inn')
# print(arrows[test+3])
#
# data = '3'
# new = arrows[test+2].replace('1', data)
# print(new)

# версия терминала в 6-й строке
# смещение для часового пояса и порта Unipos - 2
# смещения в 5-м пуле - 3

try:
    os.mkdir('xml')
except OSError:
    print("Создать директорию 'xml' не удалось, возможно она уже существует")
else:
    print("Успешно создана директория 'xml' ")

# здесь производим замены строк на данные из эксельки
for line in edited_data:
    # осуществляем копирование прочитанных данных для работы с копией, а не исходником
    arrows = r_data[:]

    pool2 = line_searching(pools[0], arrows)
    pool3 = line_searching(pools[1], arrows)
    pool5 = line_searching(pools[2], arrows)
    pool16 = line_searching(pools[3], arrows)

    try:
        # находим строку с указанием порта Unipos
        uni_port = sline_searching(arrows, pool2, data_dict.get('unipos'))
    except TypeError:
        print('Нет 2-го пула (Unipos)')
        uni_port = None
    try:
        # находим строку с указанием порта тарифов (для моек)
        pool3_pos = sline_searching(arrows, pool3, pools[1])
    except TypeError:
        print('Нет 3-го пула')
        pool3_pos = None
    # Эта часть кода не работает! А жаль
    # print('line', pool3_pos)
    # print(arrows[pool3_pos])
    # if pool3_pos is not None:
    #     if str(line[-1]).upper() == "АЗС":
    #         for i in range(-1, 323):
    #             arrows.pop(int(pool3_pos) + i)

    try:
        # находим строки 5-го пула для печати чеков
        name = sline_searching(arrows, pool5, data_dict.get('name'))
        inn = sline_searching(arrows, pool5, data_dict.get('inn'))
        adr = sline_searching(arrows, pool5, data_dict.get('adr'))
        brnd = sline_searching(arrows, pool5, data_dict.get('brand'))
    except TypeError:
        print('Нет 5-го пула (чек)')
        name = inn = adr = brnd = None
    try:
        # находим строки для часового пояса
        gmt = sline_searching(arrows, pool16, data_dict.get('gmt'))
    except TypeError:
        print('Нет 16-го пала (часовой пояс)')
        gmt = None

    ver = str(line[4].upper())
    if ver.upper() == 'VERIFONE':
        arrows[6] = f'    <platform byte_ordering="Big_Endian"/>'
    elif ver.upper() == 'ICT':
        arrows[6] = f'    <platform byte_ordering="Little_Endian"/>'
    elif ver.upper() == 'SAGEM':
        arrows[6] = f'    <platform byte_ordering="Little_Endian"/>'

    if uni_port is not None:
        arrows[uni_port + 2] = f'            <value>{line[-3]}</value>'

    if name is not None:
        arrows[name + 3] = f'            <value>{space_fill(line[0])}{line[0][0:23]}</value>'
        arrows[inn + 3] = f'            <value>{line[1]}</value>'
        arrows[adr + 3] = f'            <value>{line[2][0:23]}</value>'
        if line[-4] != 'NAN':
            arrows[brnd + 3] = f'            <value>{space_fill(line[-4])}{line[-4][0:23]}</value>'

    if gmt is not None:
        arrows[gmt + 2] = f'            <value>{line[-2]}</value>'

    with open(f'{os.getcwd()}/xml/2005{str(line[3]).zfill(4)}.xml', 'w', encoding='windows-1251') as file:
        for cur_row in arrows:
            print(cur_row, file=file)


