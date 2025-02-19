# -*- coding: utf-8 -*-
"""
Задание 11.4

Создать функцию create_network_map, которая обрабатывает вывод команды show cdp
neighbors из нескольких файлов и объединяет его в одну общую топологию.

У функции должен быть один параметр filenames, который ожидает как аргумент
список с именами файлов, в которых находится вывод команды show cdp neighbors.

Функция должна возвращать словарь, который описывает соединения между
устройствами. Структура словаря такая же, как в задании 11.3:
    {("R4", "Fa0/1"): ("R5", "Fa0/1"),
     ("R4", "Fa0/2"): ("R6", "Fa0/0")}

Cгенерировать топологию, которая соответствует выводу из файлов:
* sh_cdp_n_sw1.txt
* sh_cdp_n_r1.txt
* sh_cdp_n_r2.txt
* sh_cdp_n_r3.txt

Не копировать код функции parse_cdp_neighbors.
Если функция parse_cdp_neighbors не может обработать вывод одного из файлов
с выводом команды, надо исправить код функции в задании 11.3.

Пример работы функции
In [3]: pprint(create_network_map(infiles), sort_dicts=False)
{('SW1', 'Eth0/1'): ('R1', 'Eth0/0'),
 ('SW1', 'Eth0/2'): ('R2', 'Eth0/0'),
 ('SW1', 'Eth0/3'): ('R3', 'Eth0/0'),
 ('SW1', 'Eth0/5'): ('R6', 'Eth0/1'),
 ('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [4]: pprint(create_network_map(["sh_cdp_n_sw1.txt", "sh_cdp_n_r1.txt"]), sort_dicts=False)
{('SW1', 'Eth0/1'): ('R1', 'Eth0/0'),
 ('SW1', 'Eth0/2'): ('R2', 'Eth0/0'),
 ('SW1', 'Eth0/3'): ('R3', 'Eth0/0'),
 ('SW1', 'Eth0/5'): ('R6', 'Eth0/1'),
 ('R1', 'Eth0/0'): ('SW1', 'Eth0/1')}

"""
from pprint import pprint
import os

from task_11_3 import parse_cdp_neighbors

PATH = "/home/altron/Documents/repos/pyneng-course-tasks/exercises/11_modules"

def create_network_map(filenames):
    topology = {}
    for file in filenames:
        with open(os.path.join(PATH, file)) as f:
                topology.update(parse_cdp_neighbors(f.read()))
    return topology
                

infiles = [
    "sh_cdp_n_sw1.txt",
    "sh_cdp_n_r1.txt",
    "sh_cdp_n_r2.txt",
    "sh_cdp_n_r3.txt",
]

if __name__ == "__main__":
    pprint(create_network_map(infiles), sort_dicts=False)
    pprint(create_network_map(["sh_cdp_n_sw1.txt", "sh_cdp_n_r1.txt"]), sort_dicts=False)