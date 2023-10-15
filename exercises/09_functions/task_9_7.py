# -*- coding: utf-8 -*-
"""
Задание 9.7

Создать функцию convert_config_to_dict, которая обрабатывает конфигурационный
файл коммутатора и возвращает словарь:
* Все команды верхнего уровня (команды которые НЕ начинаются с пробела), будут ключами.
* Если у команды верхнего уровня есть подкоманды (команды которые начинаются с
  пробела), они должны быть в значении у соответствующего ключа, в виде списка
  (пробелы в начале строки надо удалить).
* Если у команды верхнего уровня нет подкоманд, то значение будет пустым списком

У функции должны быть такие параметры:
* config_filename - ожидает как аргумент имя конфигурационного файла
* ignore_lines - ожидает как аргумент список строк. Если в строке
  файла находится одно из слов в списке ignore_lines, строку надо
  игнорировать, то есть не добавлять в словарь.

Проверить работу функции на примере файла config_sw1.txt

При обработке конфигурационного файла, надо игнорировать строки, которые начинаются
с '!', пустые строки, а также строки в которых содержатся слова из списка ignore.

Пример работы функции:
In [3]: pprint(convert_config_to_dict("config_r2_short.txt", ignore), sort_dicts=False)
{'version 15.2': [],
 'no service timestamps debug uptime': [],
 'no service timestamps log uptime': [],
 'hostname PE_r2': [],
 'no ip http server': [],
 'no ip http secure-server': [],
 'ip route 10.2.2.2 255.255.255.255 Tunnel0': [],
 'ip access-list standard LDP': ['deny   10.0.0.0 0.0.255.255',
                                 'permit 10.0.0.0 0.255.255.255'],
 'ip prefix-list TEST seq 5 permit 10.6.6.6/32': [],
 'mpls ldp router-id Loopback0 force': [],
 'control-plane': [],
 'line con 0': ['exec-timeout 0 0',
                'privilege level 15',
                'logging synchronous'],
 'line aux 0': [],
 'line vty 0 4': ['login', 'transport input all']}

In [4]: pprint(convert_config_to_dict("config_sw1.txt", ignore), sort_dicts=False)
{'version 15.0': [],
 'service timestamps debug datetime msec': [],
 'service timestamps log datetime msec': [],
 'no service password-encryption': [],
 'hostname sw1': [],
 'interface FastEthernet0/0': ['switchport mode access',
                               'switchport access vlan 10'],
 'interface FastEthernet0/1': ['switchport trunk encapsulation dot1q',
                               'switchport trunk allowed vlan 100,200',
                               'switchport mode trunk'],
 'interface FastEthernet0/2': ['switchport mode access',
                               'switchport access vlan 20'],
 'interface FastEthernet0/3': ['switchport trunk encapsulation dot1q',
                               'switchport trunk allowed vlan 100,300,400,500,600',
                               'switchport mode trunk'],
 'interface FastEthernet1/0': ['switchport mode access',
                               'switchport access vlan 20'],
 'interface FastEthernet1/1': ['switchport mode access',
                               'switchport access vlan 30'],
 'interface FastEthernet1/2': ['switchport trunk encapsulation dot1q',
                               'switchport trunk allowed vlan 400,500,600',
                               'switchport mode trunk'],
 'interface Vlan100': ['ip address 10.0.100.1 255.255.255.0'],
 'line con 0': ['exec-timeout 0 0',
                'privilege level 15',
                'logging synchronous'],
 'line aux 0': [],
 'line vty 0 4': ['login', 'transport input all'],
 'end': []}


В заданиях 9го раздела и дальше, кроме указанной функции можно создавать любые
дополнительные функции.
"""
from pprint import pprint
import os

PATH = "/home/altron/Documents/repos/pyneng-course-tasks/exercises/09_functions"

# Вариант 1:
def ignore_line(line, ignore_lines):
    """
    Функция поиска игнорируемых слов из списка в составе строки.
    Если слов в строке не обнаружено - возвращаем False;
    Если при переборе слово найдено - возвращаем True.

    Params:
        line (str): Строка исходного файла конфигурации
        ignore_lines (list): Список игнорируемых слов 

    Returns:
        bool: Возвращает результат обнаружения игнорируемых слов в строке файла конффигурации
    """
    for ignore in ignore_lines:
        if ignore in line:
            return True
    return False


def convert_config_to_dict(config_filename, ignore_lines):
    """
    Функция возвращает словарь на основе файла конфигурации.
    Команды верхнего уровня преобразуются в ключи.
    Подкоманды преобразуются в значение ключа (в виде списка)

    Params:
        config_file (str): Файл конфигурации
        ignore_lines (list): Список игнорируемых слов

    Returns:
        dict: Словарь на основе файла конфигурации
    """
    config_dict = {}
    with open(os.path.join(PATH, config_filename)) as f:
        for line in f:
            if not line.startswith("!") and line != "\n":
                if not ignore_line(line, ignore_lines):
                    if not line.startswith(" "):
                        conf_block = line.strip()
                        config_dict[conf_block] = []
                    else:
                        config_dict[conf_block].append(line.strip())
        return config_dict

# Вариант 2 (в одну функцию):
# def convert_config_to_dict(config_filename, ignore_lines):
#     """
#     Функция возвращает словарь на основе файла конфигурации.
#     Команды верхнего уровня преобразуются в ключи.
#     Подкоманды преобразуются в значение ключа (в виде списка)

#     Params:
#         config_file (str): Файл конфигурации
#         ignore_lines (list): Список игнорируемых слов

#     Returns:
#         dict: Словарь на основе файла конфигурации
#     """
#     config_dict = {}
#     with open(os.path.join(PATH, config_filename)) as f:
#         for line in f:
#             if not line.startswith("!") and line != "\n"
#                 good_line = True
#                 for item in ignore_lines:
#                     good_line = item not in line and good_line
#                 if good_line and not line.startswith(" "):
#                     conf_block = line.strip()
#                     config_dict[conf_block] = []
#                 elif good_line:
#                     config_dict[conf_block].append(line.strip())
#     return config_dict


ignore = ["duplex", "alias", "configuration"]

pprint(convert_config_to_dict("config_sw1.txt", ignore), sort_dicts=False)