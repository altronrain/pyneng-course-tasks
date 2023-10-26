# -*- coding: utf-8 -*-
"""
Задание 12.2

Функция ping_ip_addresses из задания 12.1 принимает только список адресов,
но было бы удобно иметь возможность указывать адреса с помощью диапазона,
например, 192.168.100.1-10.

В этом задании необходимо создать функцию convert_ranges_to_ip_list,
которая конвертирует список IP-адресов в разных форматах в список,
где каждый IP-адрес указан отдельно.

Функция ожидает как аргумент список, в котором содержатся IP-адреса
и/или диапазоны IP-адресов.

Элементы списка могут быть в формате:
* 10.1.1.1
* 10.1.1.1-10.1.1.10
* 10.1.1.1-10

Если адрес указан в виде диапазона, надо развернуть диапазон в отдельные
адреса, включая последний адрес диапазона.
Для упрощения задачи, можно считать, что в диапазоне всегда меняется только
последний октет адреса.

Функция возвращает список IP-адресов.

Пример вызова функции
In [3]: convert_ranges_to_ip_list(['8.8.4.4', '1.1.1.1-3', '172.21.41.128-172.21.41.132'])
Out[3]:
['8.8.4.4',
 '1.1.1.1',
 '1.1.1.2',
 '1.1.1.3',
 '172.21.41.128',
 '172.21.41.129',
 '172.21.41.130',
 '172.21.41.131',
 '172.21.41.132']

In [4]: convert_ranges_to_ip_list(['8.8.4.4', '1.1.1.10-12', '10.1.1.1-10.1.1.4'])
Out[4]:
['8.8.4.4',
 '1.1.1.10',
 '1.1.1.11',
 '1.1.1.12',
 '10.1.1.1',
 '10.1.1.2',
 '10.1.1.3',
 '10.1.1.4']

"""
from ipaddress import ip_address

# Вариант 1 (без ipaddress)
def convert_ranges_to_ip_list(ip_list):
    """
    Функция обрабатывает полученный список IP-адресов.
    Указания IP-адресов в виде диапазонов преобразуются к полному списку IP-адресов. 
    
    Params:
        ip_list (list): Список IP-адресов для обработки

    Returns:
        list: Полный список IP-адресов без диапазонов
    """
    list_of_ip = []
    for item in ip_list:
        if "-" not in item:
            list_of_ip.append(item)
        else:
            ip_start, ip_end = item.split("-")
            ip_s_oct123 = ".".join(ip_start.split(".")[0:3]) 
            ip_s_oct4 = ip_start.split(".")[3]
            ip_e_oct4 = ip_end.split(".")[3] if "." in ip_end else ip_end
            for last_oct in range(int(ip_s_oct4), int(ip_e_oct4) + 1):
                list_of_ip.append(f"{ip_s_oct123}.{last_oct}")
    return list_of_ip

# Вариант 2 (с ipaddress)
def convert_ranges_to_ip_list(ip_list):
    """
    Функция обрабатывает полученный список IP-адресов.
    Указания IP-адресов в виде диапазонов преобразуются к полному списку IP-адресов. 
    
    Params:
        ip_list (list): Список IP-адресов для обработки

    Returns:
        list: Полный список IP-адресов без диапазонов
    """
    list_of_ip = []
    for item in ip_list:
        if "-" not in item:
            list_of_ip.append(item)
        else:
            ip_start, ip_end = item.split("-")
            if "." in ip_end:
                inc = int(ip_address(ip_end)) - int(ip_address(ip_start))
            else:
                inc = int(ip_end) - int(ip_start.split(".")[3])
            ip_start = ip_address(ip_start)
            for _ in range(inc + 1):
                list_of_ip.append(str(ip_start))
                ip_start += 1
    return list_of_ip


if __name__ == "__main__":
    convert_ranges_to_ip_list(['8.8.4.4', '1.1.1.10-12', '10.1.1.1-10.1.1.4'])