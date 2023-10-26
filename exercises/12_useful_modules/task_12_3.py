# -*- coding: utf-8 -*-
"""
Задание 12.3

Создать функцию print_ip_table, которая отображает таблицу доступных
и недоступных IP-адресов.

Функция ожидает как аргументы два списка:
* список доступных IP-адресов
* список недоступных IP-адресов

Результат работы функции - вывод на стандартный поток вывода таблицы вида:

Reachable    Unreachable
-----------  -------------
10.1.1.1     10.1.1.7
10.1.1.2     10.1.1.8
             10.1.1.9

Функция ничего не возвращает, только делает print.

Пример вызова функции
In [6]: reach_ip = ["10.1.1.1", "10.1.1.2"]
In [7]: unreach_ip = ["10.1.1.7", "10.1.1.8", "10.1.1.9"]

In [8]: print_ip_table(reach_ip, unreach_ip)
Reachable    Unreachable
-----------  -------------
10.1.1.1     10.1.1.7
10.1.1.2     10.1.1.8
             10.1.1.9

"""
from tabulate import tabulate
from itertools import zip_longest

def print_ip_table(good_ip_list, bad_ip_list):
    """
    Функция форматирует два списка IP-адресов к табличному виду
    и выводит полученную таблицу на стандартный поток вывода 

    Params:
        good_ip_list (list): Список доступных IP-адресов
        bad_ip_list (list): Список недоступных IP-адресов
    """
    columns = ["Reachable", "Unreachable"]
    table_data = []
    for row in zip_longest(good_ip_list, bad_ip_list, fillvalue=''):
        table_data.append(list(row))
    print(tabulate(table_data, headers=columns))
    

# Вариант из ответов (проще)    
# def print_ip_table(reach_ip, unreach_ip):
#     table = {"Reachable": reach_ip, "Unreachable": unreach_ip}
#     print(tabulate(table, headers="keys"))
    
if __name__ == "__main__":
    reach_ip = ["10.1.1.1", "10.1.1.2"]
    unreach_ip = ["10.1.1.7", "10.1.1.8", "10.1.1.9"]
    print_ip_table(reach_ip, unreach_ip)