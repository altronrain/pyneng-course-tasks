# -*- coding: utf-8 -*-
"""
Задание 15.3

Создать функцию convert_ios_nat_to_asa, которая конвертирует правила NAT
из синтаксиса cisco IOS в cisco ASA.

Функция ожидает такие аргументы:
- имя файла, в котором находится правила NAT Cisco IOS
- имя файла, в который надо записать полученные правила NAT для ASA

Функция ничего не возвращает.

Проверить функцию на файле cisco_nat_config.txt.

Пример правил NAT cisco IOS
ip nat inside source static tcp 10.1.2.84 22 interface GigabitEthernet0/1 20022
ip nat inside source static tcp 10.1.9.5 22 interface GigabitEthernet0/1 20023

И соответствующие правила NAT для ASA:
object network LOCAL_10.1.2.84
 host 10.1.2.84
 nat (inside,outside) static interface service tcp 22 20022
object network LOCAL_10.1.9.5
 host 10.1.9.5
 nat (inside,outside) static interface service tcp 22 20023

В файле с правилами для ASA:
- не должно быть пустых строк между правилами
- перед строками "object network" не должны быть пробелы
- перед остальными строками должен быть один пробел

Во всех правилах для ASA интерфейсы будут одинаковыми (inside,outside).
"""
import re
import os
from pprint import pprint

PATH = "/home/altron/Documents/repos/pyneng-course-tasks/exercises/15_module_re"

def make_asa_nat_conf(params, filename):
    """Функция принимает набор параметров, необходимых для составления правил NAT,
    формирует эти правила и осуществляет запись в результирующий файл.

    Params:
        params (list): Список необходимых параметров для формирования правил NAT
        filename (str): Имя результирующего файла конфигурации
    """
    with open(os.path.join(PATH, filename), "w") as f:
        for mode, proto, ip, s_port, d_port in params:
            line = (
                f"object network LOCAL_{ip}\n"
                f" host {ip}\n"
                f" nat (inside,outside) {mode} interface service {proto} {s_port} {d_port}\n"
            )
            f.write(line)


def convert_ios_nat_to_asa(ios_nat_conf, asa_nat_conf):
    """Функция обрабатывает правила NAT в стиле Cisco IOS из файла
    и записывает правила NAT в стиле Cisco ASA в отдельный файл. 

    Params:
        ios_nat_conf (str): Имя файла конфигурации, из которого берем правила NAT
        asa_nat_conf (str): Имя файла конфигурации, в который записываем правила NAT
    """
    nat_rule_info = []
    regex = r"^(?:\w+ ){4}(\w+) (\w+) ([0-9.]+) (\d+) (?:\S+ ){2}(\d+)"
    with open(os.path.join(PATH, ios_nat_conf)) as f:
        output = f.read()
    
    rmatch = re.finditer(regex, output, re.MULTILINE)
    for m in rmatch:
        #print(m.groups())
        nat_rule_info.append(m.groups())
    
    make_asa_nat_conf(nat_rule_info, asa_nat_conf)     
    

if __name__ == "__main__":
    convert_ios_nat_to_asa("cisco_nat_config.txt" , "asa_nat_config.txt")