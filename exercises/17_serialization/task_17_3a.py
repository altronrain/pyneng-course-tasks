# -*- coding: utf-8 -*-
"""
Задание 17.3a

Создать функцию generate_topology_from_cdp, которая обрабатывает вывод
команды show cdp neighbor из нескольких файлов и записывает итоговую
топологию в один словарь.

Функция generate_topology_from_cdp должна быть создана с параметрами:
* list_of_files - список файлов из которых надо считать вывод команды sh cdp neighbor
* save_to_filename - имя файла в формате YAML, в который сохранится топология.
 * значение по умолчанию - None. По умолчанию, топология не сохраняется в файл
 * топология сохраняется только, если save_to_filename как аргумент указано имя файла

Функция должна возвращать словарь, который описывает соединения между устройствами,
независимо от того сохраняется ли топология в файл.

Структура словаря должна быть такой:
{'R4': {'Fa 0/1': {'R5': 'Fa 0/1'},
        'Fa 0/2': {'R6': 'Fa 0/0'}},
 'R5': {'Fa 0/1': {'R4': 'Fa 0/1'}},
 'R6': {'Fa 0/0': {'R4': 'Fa 0/2'}}}

Интерфейсы должны быть записаны с пробелом. То есть, так Fa 0/0, а не так Fa0/0.

Проверить работу функции generate_topology_from_cdp на списке файлов:
* sh_cdp_n_sw1.txt
* sh_cdp_n_r1.txt
* sh_cdp_n_r2.txt
* sh_cdp_n_r3.txt
* sh_cdp_n_r4.txt
* sh_cdp_n_r5.txt
* sh_cdp_n_r6.txt

Проверить работу параметра save_to_filename и записать итоговый словарь
в файл topology.yaml. Он понадобится в следующем задании.

Пример вызова функции
In [11]: pprint(generate_topology_from_cdp(["sh_cdp_n_sw1.txt", "sh_cdp_n_r1.txt"]), sort_dicts=False)
{'SW1': {'Eth 0/1': {'R1': 'Eth 0/0'},
         'Eth 0/2': {'R2': 'Eth 0/0'},
         'Eth 0/3': {'R3': 'Eth 0/0'},
         'Eth 0/4': {'R4': 'Eth 0/0'}},
 'R1': {'Eth 0/0': {'SW1': 'Eth 0/1'}}}

In [12]: f_list
Out[12]:
['sh_cdp_n_r2.txt',
 'sh_cdp_n_r5.txt',
 'sh_cdp_n_r1.txt',
 'sh_cdp_n_sw1.txt',
 'sh_cdp_n_r3.txt',
 'sh_cdp_n_r4.txt',
 'sh_cdp_n_r6.txt']

In [13]: pprint(generate_topology_from_cdp(f_list), sort_dicts=False)
{'R2': {'Eth 0/0': {'SW1': 'Eth 0/2'},
        'Eth 0/1': {'R5': 'Eth 0/0'},
        'Eth 0/2': {'R6': 'Eth 0/1'}},
 'R5': {'Eth 0/0': {'R2': 'Eth 0/1'}, 'Eth 0/1': {'R4': 'Eth 0/1'}},
 'R1': {'Eth 0/0': {'SW1': 'Eth 0/1'}},
 'SW1': {'Eth 0/1': {'R1': 'Eth 0/0'},
         'Eth 0/2': {'R2': 'Eth 0/0'},
         'Eth 0/3': {'R3': 'Eth 0/0'},
         'Eth 0/4': {'R4': 'Eth 0/0'}},
 'R3': {'Eth 0/0': {'SW1': 'Eth 0/3'}},
 'R4': {'Eth 0/0': {'SW1': 'Eth 0/4'}, 'Eth 0/1': {'R5': 'Eth 0/1'}},
 'R6': {'Eth 0/1': {'R2': 'Eth 0/2'}}}
"""
import os
import yaml
from pprint import pprint

from task_17_3 import parse_sh_cdp_neighbors

PATH = "/home/altron/Documents/repos/pyneng-course-tasks/exercises/17_serialization"

def generate_topology_from_cdp(list_of_files, save_to_filename=None):
    """Функция получает на вход список файлов, содержащих вывод команды sh cdp n.
    На основе данных из файлов формируется словарь словарей с топологией сети.
    Предусмотрена возможность записи полученной топологии в файл в YAML формате.

    Args:
        list_of_files (list): Список файлов для обработки
        save_to_filename (str, optional): Имя файла для записи в формате YAML. Defaults to None.

    Returns:
        dict: Словарь словарей с топологией сети на основе данных с устройств
    """
    topology_dict = {}
    for file in list_of_files:
        with open(os.path.join(PATH, file)) as f:
            topology_dict.update(parse_sh_cdp_neighbors(f.read()))
    if save_to_filename:
        with open(os.path.join(PATH, save_to_filename), mode="w") as of:
           yaml.dump(topology_dict, of)
    return topology_dict 


if __name__ == "__main__":
    f_list = [
        'sh_cdp_n_r2.txt',
        'sh_cdp_n_r5.txt',
        'sh_cdp_n_r1.txt',
        'sh_cdp_n_sw1.txt',
        'sh_cdp_n_r3.txt',
        'sh_cdp_n_r4.txt',
        'sh_cdp_n_r6.txt'
    ]
    pprint(generate_topology_from_cdp(f_list, "topology.yaml"), sort_dicts=False)