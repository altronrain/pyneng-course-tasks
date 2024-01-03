# -*- coding: utf-8 -*-

"""
Задание 23.3a

В этом задании надо сделать так, чтобы экземпляры класса Topology
были итерируемыми объектами.
Основу класса Topology можно взять из любого задания 22.1x или задания 23.3.

После создания экземпляра класса, экземпляр должен работать как итерируемый объект.
На каждой итерации должен возвращаться кортеж, который описывает одно соединение.
Порядок вывода соединений может быть любым.


Пример работы класса:

In [1]: top = Topology(topology_example)

In [2]: for link in top:
   ...:     print(link)
   ...:
(('R1', 'Eth0/0'), ('SW1', 'Eth0/1'))
(('R2', 'Eth0/0'), ('SW1', 'Eth0/2'))
(('R2', 'Eth0/1'), ('SW2', 'Eth0/11'))
(('R3', 'Eth0/0'), ('SW1', 'Eth0/3'))
(('R3', 'Eth0/1'), ('R4', 'Eth0/0'))
(('R3', 'Eth0/2'), ('R5', 'Eth0/0'))


Проверить работу класса.
"""
class Topology:
    def __init__(self, topology_dict):
        self.topology = self._normalize(topology_dict)
        
    def __add__(self, other):
        if not isinstance(other, Topology):
            raise TypeError(
                f"unsupported operand type(s) for: 'Topology' and "
                f"'{type(other).__name__}'"
            )
        t3 = self.topology.copy()
        for link in other.topology.items():
            p1, p2 = link
            overlap = self._add_overlap_check(p1, p2)
            if not overlap:
                t3[p1] = p2
        return Topology(t3)
    
    def __getitem__(self, index):
        return list(self.topology.items())[index]
    
    def __len__(self):
        return len(list(self.topology.items()))
    
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

    def _add_overlap_check(self, p1, p2):
        topology_copy = self.topology.copy()
        for k, v in topology_copy.items():
            if (k == p1 and v == p2) or (k == p2 and v == p1):
                print("Такое соединение существует")
                return True
            elif k == p1 or v == p1 or k == p2 or v == p2:
                print("Соединение с одним из портов существует")
                return True
        return False      
            
    def add_link(self, p1, p2):
        overlap = self._add_overlap_check(p1, p2)
        if not overlap:
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

    topology_example2 = {
        ("R1", "Eth0/4"): ("R7", "Eth0/0"),
        ("R1", "Eth0/6"): ("R9", "Eth0/0"),
    }
    t1 = Topology(topology_example)

    for link in t1:
        print(link)
    print(len(t1))