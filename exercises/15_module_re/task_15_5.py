# -*- coding: utf-8 -*-
"""
Задание 15.5

Создать функцию generate_description_from_cdp, которая ожидает как аргумент
имя файла, в котором находится вывод команды show cdp neighbors.

Функция должна обрабатывать вывод команды show cdp neighbors и генерировать
на основании вывода команды описание для интерфейсов.

Например, если у R1 такой вывод команды:
R1>show cdp neighbors
Capability Codes: R - Router, T - Trans Bridge, B - Source Route Bridge
                  S - Switch, H - Host, I - IGMP, r - Repeater

Device ID        Local Intrfce     Holdtme    Capability  Platform  Port ID
SW1              Eth 0/0           140          S I      WS-C3750-  Eth 0/1

Для интерфейса Eth 0/0 надо сгенерировать такое описание
description Connected to SW1 port Eth 0/1

Функция должна возвращать словарь, в котором ключи - имена интерфейсов,
а значения - команда задающая описание интерфейса:
'Eth 0/0': 'description Connected to SW1 port Eth 0/1'


Проверить работу функции на файле sh_cdp_n_sw1.txt.
Пример вызова функции
In [17]: generate_description_from_cdp("sh_cdp_n_sw1.txt")
Out[17]:
{'Eth 0/1': 'description Connected to R1 port Eth 0/0',
 'Eth 0/2': 'description Connected to R2 port Eth 0/0',
 'Eth 0/3': 'description Connected to R3 port Eth 0/0',
 'Eth 0/5': 'description Connected to R6 port Eth 0/1'}

"""
import re
import os
from pprint import pprint

PATH = "/home/altron/Documents/repos/pyneng-course-tasks/exercises/15_module_re"

def generate_description_from_cdp(filename):
    """Функция обрабатывает файл, содержащий вывод команды show cdp neighbors.
    На основе информации из данного файла формируется описание для интерфейсов
    в конфигурации. Данные описания возвращаются в виде словаря.

    Params:
        filename (str): Имя файла для обработки

    Returns:
        dict: Словарь, содержащий описание для интерфейсов конфигурации.
        Формат словаря: {'Interface': 'Description', ...}
    """
    intf_descr_dict = {}
    regex = r"^(?P<device>\w+) +(?P<l_port>\w+ \S+).+?(?P<r_port>\w+ \S+)$"
    with open(os.path.join(PATH, filename)) as f:
        output = f.read()
        
    rmatch = re.finditer(regex, output, re.MULTILINE)
    for m in rmatch:
        #print(m.groups())
        device, l_port, r_port = m.groups()
        intf_descr_dict[l_port] = f"description Connected to {device} port {r_port}"
    return intf_descr_dict


if __name__ == "__main__":
    pprint(generate_description_from_cdp("sh_cdp_n_sw1.txt"))