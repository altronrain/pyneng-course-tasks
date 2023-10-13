# -*- coding: utf-8 -*-
"""
Задание 9.6

Создать функцию get_int_vlan_map, которая обрабатывает конфигурационный
файл коммутатора и возвращает кортеж из двух словарей:
* словарь портов в режиме access, где ключи номера портов, а значения access
  VLAN (числа)
* словарь портов в режиме trunk, где ключи номера портов, а значения список
  разрешенных VLAN (список чисел)

У функции должен быть один параметр config_filename, который ожидает как аргумент
имя конфигурационного файла.

Проверить работу функции на примере файла config_sw1.txt

Пример работы функции
In [2]: get_int_vlan_map("config_sw1.txt")
Out[2]:
({'FastEthernet0/0': 10,
  'FastEthernet0/2': 20,
  'FastEthernet1/0': 20,
  'FastEthernet1/1': 30},
 {'FastEthernet0/1': [100, 200],
  'FastEthernet0/3': [100, 300, 400, 500, 600],
  'FastEthernet1/2': [400, 500, 600]})

In [3]: access, trunk = get_int_vlan_map("config_sw1.txt")

In [4]: access
Out[4]:
{'FastEthernet0/0': 10,
 'FastEthernet0/2': 20,
 'FastEthernet1/0': 20,
 'FastEthernet1/1': 30}

In [5]: trunk
Out[5]:
{'FastEthernet0/1': [100, 200],
 'FastEthernet0/3': [100, 300, 400, 500, 600],
 'FastEthernet1/2': [400, 500, 600]}


В заданиях 9го раздела и дальше, кроме указанной функции можно создавать любые
дополнительные функции.
"""
from pprint import pprint
import os

PATH = "/home/altron/Documents/repos/pyneng-course-tasks/exercises/09_functions"

def get_int_vlan_map(config_filename):
    """
    Функция формирует два словаря на основе файла конфигурации.
    Словари содержат информацию вида "интерфейс"-"vlan(-s)"
    Один словарь для access портов. Vlan для него представляет собой число.
    Второй словарь для trunk портов. Vlans для него представляет собой список.

    Params:
        config_file (str): Файл конфигурации

    Returns:
        tuple: Кортеж из двух словарей для разных типов интерфейсов
    """
    access_intf_vlan_dict = {}
    trunk_intf_vlan_dict = {}
    with open(os.path.join(PATH, config_filename)) as f:
        for line in f:
            if "Ethernet" in line:
                intf = line.split()[-1]
            if "access vlan" in line:
                access_intf_vlan_dict[intf] = int(line.split()[-1])
            elif "allowed vlan" in line:
                trunk_intf_vlan_dict[intf] = []
                for vl in line.split()[-1].split(","):
                    trunk_intf_vlan_dict[intf].append(int(vl))
    
    return access_intf_vlan_dict, trunk_intf_vlan_dict

pprint(get_int_vlan_map("config_sw1.txt"))