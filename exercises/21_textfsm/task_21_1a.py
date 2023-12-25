# -*- coding: utf-8 -*-
"""
Задание 21.1a

Создать функцию parse_output_to_dict.

Параметры функции:
* template - имя файла, в котором находится шаблон TextFSM.
  Например, templates/sh_ip_int_br.template
* command_output - вывод соответствующей команды show (строка)

Функция должна возвращать список словарей:
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на выводе команды output/sh_ip_int_br.txt
и шаблоне templates/sh_ip_int_br.template.

Пример работы функции (ключи в словарях отсортированы из-за pprint)
In [2]: with open("output/sh_ip_int_br.txt") as f:
   ...:     pprint(parse_output_to_dict("templates/sh_ip_int_br.template", f.read()), width=100)
   ...:
[{'address': '15.0.15.1', 'intf': 'FastEthernet0/0', 'protocol': 'up', 'status': 'up'},
 {'address': '10.0.12.1', 'intf': 'FastEthernet0/1', 'protocol': 'up', 'status': 'up'},
 {'address': '10.0.13.1', 'intf': 'FastEthernet0/2', 'protocol': 'up', 'status': 'up'},
 {'address': 'unassigned', 'intf': 'FastEthernet0/3', 'protocol': 'up', 'status': 'up'},
 {'address': '10.1.1.1', 'intf': 'Loopback0', 'protocol': 'up', 'status': 'up'},
 {'address': '100.0.0.1', 'intf': 'Loopback100', 'protocol': 'up', 'status': 'up'}]

"""
import textfsm
from netmiko import ConnectHandler
from pathlib import Path
from pprint import pprint

p = Path('exercises/21_textfsm')

def parse_output_to_dict(template, command_output):
    """Функция обрабатывает вывод команды с помощью шаблона TextFSM
    Результат обработки представляет собой список словарей

    Args:
        template (str): Имя файла шаблона TextFSM
        command_output (str): вывод команды с оборудования

    Returns:
        list: Список словарей с распарсенными данными
    """
    with open(template) as t:
        fsm = textfsm.TextFSM(t)
        result = fsm.ParseTextToDicts(command_output)
    return result


# вызов функции должен выглядеть так
if __name__ == "__main__":
    # r1_params = {
    #     "device_type": "cisco_ios",
    #     "host": "192.168.139.1",
    #     "username": "cisco",
    #     "password": "cisco",
    #     "secret": "cisco",
    # }
    # with ConnectHandler(**r1_params) as r1:
    #     r1.enable()
    #     output = r1.send_command("sh ip int br")
    # result = parse_command_output("templates/sh_ip_int_br.template", output)
    # print(result)
    with open(p/"output/sh_ip_int_br.txt") as f:
        pprint(parse_output_to_dict(p/"templates/sh_ip_int_br.template", f.read()), width=100)