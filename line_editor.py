from exel_reader import rded_data
import os
import shutil
from datetime import datetime

# убираем правовую форму юр.лица в начало строки
def name_change(search_object, string_in):
    result = search_object + " " + string_in.replace(search_object, '').strip().replace('"', '')
    return result.upper()

# пишем логи ошибок
def len_check(value: str, adr: str, check_type: str, length: int):
    if len(value) > length:
        time_n_date = f'{datetime.now().strftime("%Y-%m-%d-%H:%M")}'
        with open(f'{os.getcwd()}/logs/log{time_n_date}.txt', 'a+') as log:
            log.write(f'Строка {adr} {check_type}: "{value}" превышена длина строки в {length}\n')
        shutil.copyfile(f'{os.getcwd()}/test_data.xlsx', f'{os.getcwd()}/logs/error_data{time_n_date}.xlsx')


def row_editor(row: list):
    names = ['ИП', 'ПКП', 'ПК', 'ООО', 'ОАО', 'ПАО', 'ЗАО', 'АО', 'ТД']
    for i in names:
        if i in row[0]:
            row[0] = name_change(i, row[0])
            break


step = 0
# Приводим имя к нормальному формату и проверяем длину строк
for line in rded_data:
    step += 1
    row_editor(line)
    len_check(line[0], f'{step}', 'ИМЯ', 24)
    len_check(line[2], f'{step}', 'АДРЕС', 24)
    len_check(str(line[3]), f'{step}', 'ЛОК.НОМЕР', 4)
    len_check(line[-4], f'{step}', 'БРЕНД', 24)

edited_data = rded_data[:]

