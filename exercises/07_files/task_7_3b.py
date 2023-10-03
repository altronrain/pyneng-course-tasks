# -*- coding: utf-8 -*-
"""
Задание 7.3b

Сделать копию скрипта задания 7.3a.

Переделать скрипт:
- Запросить у пользователя ввод номера VLAN.
- Выводить информацию только по указанному VLAN.

Пример работы скрипта:
$ python task_7_3b.py
Введите номер влана: 10
10       0a1b.1c80.7000      Gi0/4
10       01ab.c5d0.70d0      Gi0/8

"""

result = []
with open("CAM_table.txt") as f:
    for line in f:
        words = line.split()
        if len(words) >= 4 and line[1].isdigit():
            result.append([int(words[0]),words[1],words[3]])

vl_num = int(input("Введите номер влана: "))
for vl, mac, port in sorted(result):
    if vl == vl_num:
        print(f"{vl:<9}{mac:20}{port}")