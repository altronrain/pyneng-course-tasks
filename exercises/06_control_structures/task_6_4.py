# -*- coding: utf-8 -*-
"""
Задание 6.4

Список files содержит имена файлов:
["cfg_1.txt", "cfg_4.txt", "cfg_8.txt", "cfg_9.txt", "cfg_12.txt", "cfg_15.txt"]

Надо переименовать файлы таким образом:
["cfg_01.txt", "cfg_04.txt", "cfg_08.txt", "cfg_09.txt", "cfg_12.txt", "cfg_15.txt"]

То есть надо сделать так, чтобы после cfg_ всегда были две цифры. Если число
меньше 10, дополнить до 2 цифр нулями в начале.

Написать код, который преобразует имена файлов в нужный формат и добавляет их в
новый список result (тест будет проверять переменную result).
Полученный список result вывести на стандартный поток вывода (stdout) с помощью print.

Исходный список files нельзя менять вручную, все изменения надо сделать с помощью Python.
"""

files = [
    "cfg_1.txt", "cfg_4.txt", "cfg_8.txt", "cfg_9.txt", "cfg_12.txt", "cfg_15.txt"
]

result = []

for file in files:
    num = int(file[4:-4])
    result.append(f"cfg_{num:02}.txt")
#    if num < 10:
#        result.append()

print(result)