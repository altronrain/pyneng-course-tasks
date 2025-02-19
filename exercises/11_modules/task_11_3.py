# -*- coding: utf-8 -*-
"""
Задание 11.3

Создать функцию parse_cdp_neighbors, которая обрабатывает вывод команды show
cdp neighbors.

У функции должен быть один параметр command_output, который ожидает как
аргумент вывод команды одной строкой (не имя файла). Для этого надо считать все
содержимое файла в строку, а затем передать строку как аргумент функции (как
передать вывод команды показано в коде ниже).

Функция должна возвращать словарь, который описывает соединения между устройствами.

Например, если как аргумент был передан такой вывод:
R4>show cdp neighbors

Device ID    Local Intrfce   Holdtme     Capability       Platform    Port ID
R5           Fa 0/1          122           R S I           2811       Fa 0/1
R6           Fa 0/2          143           R S I           2811       Fa 0/0

Функция должна вернуть такой словарь:

    {("R4", "Fa0/1"): ("R5", "Fa0/1"),
     ("R4", "Fa0/2"): ("R6", "Fa0/0")}

В словаре интерфейсы должны быть записаны без пробела между типом и именем.
То есть так Fa0/0, а не так Fa 0/0.

Проверить работу функции на содержимом файла sh_cdp_n_sw1.txt. При этом функция
должна работать и на других файлах (тест проверяет работу функции на выводе из
sh_cdp_n_sw1.txt и sh_cdp_n_r3.txt).

Пример работы функции
In [3]: with open("sh_cdp_n_sw1.txt") as f:
   ...:     pprint(parse_cdp_neighbors(f.read()))
   ...:
{('SW1', 'Eth0/1'): ('R1', 'Eth0/0'),
 ('SW1', 'Eth0/2'): ('R2', 'Eth0/0'),
 ('SW1', 'Eth0/3'): ('R3', 'Eth0/0'),
 ('SW1', 'Eth0/5'): ('R6', 'Eth0/1')}

In [4]: with open("sh_cdp_n_r1.txt") as f:
   ...:     pprint(parse_cdp_neighbors(f.read()))
   ...:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1')}

In [5]: with open("sh_cdp_n_r2.txt") as f:
   ...:     pprint(parse_cdp_neighbors(f.read()))
   ...:
{('R2', 'Eth0/0'): ('SW1', 'Eth0/2'), ('R2', 'Eth0/1'): ('SW2', 'Eth0/11')}

In [6]: with open("sh_cdp_n_r3.txt") as f:
   ...:     pprint(parse_cdp_neighbors(f.read()))
   ...:
{('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

"""
import os

PATH = "/home/altron/Documents/repos/pyneng-course-tasks/exercises/11_modules"

def parse_cdp_neighbors(command_output):
    """
    Тут мы передаем вывод команды одной строкой потому что именно в таком виде будет
    получен вывод команды с оборудования. Принимая как аргумент вывод команды,
    вместо имени файла, мы делаем функцию более универсальной: она может работать
    и с файлами и с выводом с оборудования.
    Плюс учимся работать с таким выводом.
    """
#    local_map = []
#    remote_dev = {}
    port_map_dict = {}
    rows = command_output.split("\n")
    for row in rows:
        if "show cdp neighbors" in row:
            local_host = row.split(">")[0]
        if "Eth" in row:
            remote_host, _, local_p, *_, remote_p = row.split()
            local_map = tuple([local_host, "Eth" + local_p])
            remote_map = tuple([remote_host, "Eth" + remote_p])
            port_map_dict[local_map] = remote_map
    return port_map_dict
  

if __name__ == "__main__":
    with open(os.path.join(PATH, "sh_cdp_n_r3.txt")) as f:
        print(parse_cdp_neighbors(f.read()))
