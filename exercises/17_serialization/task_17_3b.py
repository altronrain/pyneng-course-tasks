# -*- coding: utf-8 -*-
"""
Задание 17.3b

Создать функцию transform_topology, которая преобразует топологию в формат подходящий
для функции draw_topology.

Функция ожидает как аргумент имя файла в формате YAML, в котором хранится
топология.

Функция должна считать данные из YAML файла, преобразовать их соответственно,
чтобы функция возвращала словарь такого вида:
    {('R4', 'Fa 0/1'): ('R5', 'Fa 0/1'),
     ('R4', 'Fa 0/2'): ('R6', 'Fa 0/0')}

Функция transform_topology должна не только менять формат представления
топологии, но и удалять "дублирующиеся" соединения (их лучше всего видно на
схеме, которую генерирует функция draw_topology из файла
draw_network_graph.py).
Тут "дублирующиеся" соединения, это ситуация когда в словаре есть два соединения:
    ("R1", "Eth0/0"): ("SW1", "Eth0/1")
    ("SW1", "Eth0/1"): ("R1", "Eth0/0")

Из-за того что один и тот же линк описывается дважды, на схеме будут лишние
соединения.  Задача оставить только один из этих линков в итоговом словаре, не
важно какой.

Проверить работу функции на файле topology.yaml (должен быть создан в задании
17.3a).  На основании полученного словаря надо сгенерировать изображение
топологии с помощью функции draw_topology.
Не копировать код функции draw_topology из файла draw_network_graph.py.

Результат должен выглядеть так же, как схема в файле task_17_3b_topology.svg

При этом:
* Интерфейсы должны быть записаны с пробелом Fa 0/0
* Расположение устройств на схеме может быть другим
* Соединения должны соответствовать схеме
* На схеме не должно быть "дублирующихся" линков


> Для выполнения этого задания, должен быть установлен graphviz:
> apt-get install graphviz

> И модуль python для работы с graphviz:
> pip install graphviz

"""
import os
import yaml
from pprint import pprint
from draw_network_graph import draw_topology

PATH = "/home/altron/Documents/repos/pyneng-course-tasks/exercises/17_serialization"

def transform_topology(yaml_file):
    """Функция обрабатывает файл топологии сети в формате YAML.
    Полученный словарь словарей преобразовывается к новому виду.
    Убираются дублирующие связи(записи) в карте топологии сети.
    На выход отдается словарь вида:
    {(local_host, local_port): (remote_host, remote_port)}

    Args:
        yaml_file (str): Имя YAML файла с топологией сети

    Returns:
        dict: Файл топологии сети в новом формате
    """
    with open(os.path.join(PATH, yaml_file)) as f:
        data = yaml.safe_load(f)      
    
    new_dict = {}
    for l_host, l_port_data in data.items():
        for l_port, r_host_data in l_port_data.items():
            for r_host, r_port in r_host_data.items():
                try:
                    new_dict[(r_host, r_port)]
                except KeyError:
                    new_dict[(l_host, l_port)] = (r_host, r_port)
    # pprint(new_dict)
    return new_dict
    
    
if __name__ == "__main__":
    draw_topology(transform_topology("topology.yaml"))
    # transform_topology("topology.yaml")
