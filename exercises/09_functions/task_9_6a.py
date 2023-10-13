# -*- coding: utf-8 -*-
"""
Задание 9.6a

Сделать копию функции get_int_vlan_map из задания 9.6.

Дополнить функцию: добавить поддержку конфигурации, когда настройка access-порта
выглядит так:
    interface FastEthernet0/20
        switchport mode access
        duplex auto

То есть, порт находится в VLAN 1

В таком случае, в словарь портов должна добавляться информация, что порт в VLAN 1
Пример словаря:
    {'FastEthernet0/12': 10,
     'FastEthernet0/14': 11,
     'FastEthernet0/20': 1 }

У функции должен быть один параметр config_filename, который ожидает
как аргумент имя конфигурационного файла.

Проверить работу функции на примере файла config_sw2.txt
Пример работы функции
In [2]: get_int_vlan_map("config_sw2.txt")
Out[2]:
({'FastEthernet0/0': 10,
  'FastEthernet0/2': 20,
  'FastEthernet1/0': 20,
  'FastEthernet1/1': 30,
  'FastEthernet1/3': 1,
  'FastEthernet2/0': 1,
  'FastEthernet2/1': 1},
 {'FastEthernet0/1': [100, 200],
  'FastEthernet0/3': [100, 300, 400, 500, 600],
  'FastEthernet1/2': [400, 500, 600]})

In [4]: access, trunk = get_int_vlan_map("config_sw2.txt")

In [5]: access
Out[5]:
{'FastEthernet0/0': 10,
 'FastEthernet0/2': 20,
 'FastEthernet1/0': 20,
 'FastEthernet1/1': 30,
 'FastEthernet1/3': 1,
 'FastEthernet2/0': 1,
 'FastEthernet2/1': 1}

In [6]: trunk
Out[6]:
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
            elif "mode access" in line:
                access_intf_vlan_dict[intf] = 1
            elif "access vlan" in line:
                access_intf_vlan_dict[intf] = int(line.split()[-1])
            elif "allowed vlan" in line:
                trunk_intf_vlan_dict[intf] = []
                for vl in line.split()[-1].split(","):
                    trunk_intf_vlan_dict[intf].append(int(vl))
    
    return access_intf_vlan_dict, trunk_intf_vlan_dict

pprint(get_int_vlan_map("config_sw2.txt"))