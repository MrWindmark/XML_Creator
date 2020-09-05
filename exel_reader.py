import openpyxl

# здесь происходит чтение файла с списком для обработки
wb = openpyxl.load_workbook(filename='test_data.xlsx', data_only=True)
# получение списка листов из файла
sheet = wb.sheetnames
# Имя листа (sheet) к которому мы обращаемся (reading)
shrng_list= wb['List1']

rded_data = []
# читаем из документа wb по списку листов sheet с листа sheet[0] каждую строку через .rows
for row in wb[sheet[0]].rows:
    # сбрасываем прочитанную строку данных
    data_line = []
    for cell in row:
        # добавляем к строке значение каждой ячейки
        data_line.append(cell.internal_value)
    # если ячейка в строке будет пустой, хотя не должна быть - конец работы скрипта чтения
    if data_line[-1] is None:
        break
    else:
        # если же данные заполнены - добавляем строку прочитанных значений
        rded_data.append(data_line)
# по завершению работы скрипта чтения, удаляем первую строку
rded_data.pop(0)