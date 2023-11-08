# -*- coding: utf-8 -*-
"""
Задание 15.4

Создать функцию get_ints_without_description, которая ожидает как аргумент
имя файла, в котором находится конфигурация устройства.

Функция должна обрабатывать конфигурацию и возвращать список имен интерфейсов,
на которых нет описания (команды description).

Пример итогового списка:
["Loopback0", "Tunnel0", "Ethernet0/1", "Ethernet0/3.100", "Ethernet1/0"]

Пример интерфейса с описанием:
interface Ethernet0/2
 description To P_r9 Ethernet0/2
 ip address 10.0.19.1 255.255.255.0
 mpls traffic-eng tunnels
 ip rsvp bandwidth

Интерфейс без описания:
interface Loopback0
 ip address 10.1.1.1 255.255.255.255

Проверить работу функции на примере файла config_r1.txt.

Пример вызова функции
In [15]: get_ints_without_description("config_r1.txt")
Out[15]: ['Loopback0', 'Tunnel0', 'Ethernet0/1', 'Ethernet0/3.100', 'Ethernet1/0']

"""
import re
import os
from pprint import pprint

PATH = "/home/altron/Documents/repos/pyneng-course-tasks/exercises/15_module_re"

def get_ints_without_description(filename):
    """Функция обрабатывает конфигурационный файл и формирует список интерфейсов,
    для которых не в конфигурации не указано описание (description).

    Params:
        filename (str): Исходный файл конфигурации для обработки

    Returns:
        list: Список имён интерфейсов без описания
    """
    intf_wo_descr = []
    regex = r"!\ninterface (\S+)\n [^d]"
    with open(os.path.join(PATH, filename)) as f:
        output = f.read()
        
    rmatch = re.finditer(regex, output)
    for m in rmatch:
        #print(m.groups())
        intf_wo_descr.append(m.group(1))
    return intf_wo_descr 


if __name__ == "__main__":
    pprint(get_ints_without_description("config_r1.txt"))