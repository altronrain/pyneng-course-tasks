# -*- coding: utf-8 -*-
"""
Задание 15.2

Создать функцию parse_sh_ip_int_br, которая ожидает как аргумент
имя файла, в котором находится вывод команды show ip int br

Функция должна обрабатывать вывод команды show ip int br и возвращать такие поля:
* Interface
* IP-Address
* Status
* Protocol

Информация должна возвращаться в виде списка кортежей (пример вывода):
[('FastEthernet0/0', '10.0.1.1', 'up', 'up'),
 ('FastEthernet0/1', '10.0.2.1', 'administratively down', 'down'),
 ('FastEthernet0/2', 'unassigned', 'down', 'down')]

Для получения такого результата, используйте регулярные выражения.

Проверить работу функции на примере файла sh_ip_int_br.txt и sh_ip_int_br_2.txt.

Привет вызова функции
In [12]: parse_sh_ip_int_br("sh_ip_int_br.txt")
Out[12]:
[('FastEthernet0/0', '15.0.15.1', 'up', 'up'),
 ('FastEthernet0/1', '10.0.12.1', 'up', 'up'),
 ('FastEthernet0/2', '10.0.13.1', 'up', 'up'),
 ('FastEthernet0/3', 'unassigned', 'administratively down', 'down'),
 ('Loopback0', '10.1.1.1', 'up', 'up'),
 ('Loopback100', '100.0.0.1', 'up', 'up')]

In [13]: parse_sh_ip_int_br("sh_ip_int_br_2.txt")
Out[13]:
[('FastEthernet0/0', '15.0.15.2', 'up', 'up'),
 ('FastEthernet0/1', '10.0.12.2', 'up', 'up'),
 ('FastEthernet0/2', '10.0.13.2', 'down', 'down'),
 ('FastEthernet0/3', 'unassigned', 'administratively down', 'down'),
 ('Loopback0', '10.2.2.2', 'up', 'up')]

"""
import re
import os
from pprint import pprint

PATH = "/home/altron/Documents/repos/pyneng-course-tasks/exercises/15_module_re"

def parse_sh_ip_int_br(filename):
    """Функция обрабатывает переданный ей файл с выводом команды
    и формирует список с информацией о состоянии интерфейсов.
    Значения представляют собой список кортежей.

    Params:
        filename (str): Имя файла для дальнейшей обработки

    Returns:
        list: Список, содержащий сведения о состоянии интерфейсов
        Формат списка: [('Interface', 'IP', 'Status', 'Protocol'), ...]  
    """
    intf_info = []
    regex = r"^(\S+) +([0-9.]+|unassigned) +\w+ \w+ +(\w+ ?\w+) +(\w+)"
    with open(os.path.join(PATH, filename)) as f:
        output = f.read()
    
    rmatch = re.finditer(regex, output, re.MULTILINE)
    for m in rmatch:
        #print(m.groups())
        intf_info.append(m.groups())
    
    return intf_info

if __name__ == "__main__":
    pprint(parse_sh_ip_int_br("sh_ip_int_br_2.txt"))        