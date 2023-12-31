# -*- coding: utf-8 -*-

"""
Задание 22.1d

Изменить класс Topology из задания 22.1c

Добавить метод add_link, который добавляет указанное соединение, если его еще
 нет в топологии.
Если соединение существует, вывести сообщение "Такое соединение существует",
Если одна из сторон есть в топологии, вывести сообщение
"Соединение с одним из портов существует"


Создание топологии
In [7]: t = Topology(topology_example)

In [8]: t.topology
Out[8]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [9]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))

In [10]: t.topology
Out[10]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R1', 'Eth0/4'): ('R7', 'Eth0/0'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [11]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))
Такое соединение существует

In [12]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/5'))
Соединение с одним из портов существует


"""
from pprint import pprint

class Topology:
    def __init__(self, topology_dict):
        self.topology = self._normalize(topology_dict)
    
    def _normalize(self, topology_dict):
        network_map = {}
        for key, value in topology_dict.items():
            if not network_map.get(value) == key:
                network_map[key] = value
        return network_map
    
    def delete_link(self, p1, p2):
        topology_copy = self.topology.copy()
        for k, v in topology_copy.items():
            if (k == p1 and v == p2) or (k == p2 and v == p1):
                self.topology.pop(k)
        if topology_copy == self.topology:
            print("Такого соединения нет")
            
    def delete_node(self, node):
        topology_copy = self.topology.copy()
        for k, v in topology_copy.items():
            if (node in k) or (node in v):
                self.topology.pop(k)
        if topology_copy == self.topology:
            print("Такого устройства нет")
            
    def add_link(self, p1, p2):
        match_ = False
        topology_copy = self.topology.copy()
        for k, v in topology_copy.items():
            if (k == p1 and v == p2) or (k == p2 and v == p1):
                print("Такое соединение существует")
                match_ = True
            elif k == p1 or v == p1 or k == p2 or v == p2:
                print("Соединение с одним из портов существует")
                match_ = True
        if not match_:
            self.topology[p1] = p2
                


if __name__ == "__main__":
    topology_example = {
        ("R1", "Eth0/0"): ("SW1", "Eth0/1"),
        ("R2", "Eth0/0"): ("SW1", "Eth0/2"),
        ("R2", "Eth0/1"): ("SW2", "Eth0/11"),
        ("R3", "Eth0/0"): ("SW1", "Eth0/3"),
        ("R3", "Eth0/1"): ("R4", "Eth0/0"),
        ("R3", "Eth0/2"): ("R5", "Eth0/0"),
        ("SW1", "Eth0/1"): ("R1", "Eth0/0"),
        ("SW1", "Eth0/2"): ("R2", "Eth0/0"),
        ("SW1", "Eth0/3"): ("R3", "Eth0/0"),
    }
    t = Topology(topology_example)
    pprint(t.topology)
    t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))
    pprint(t.topology)
    t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/5'))
    # pprint(t.topology)
    t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))
