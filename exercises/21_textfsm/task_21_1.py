# -*- coding: utf-8 -*-
"""
Задание 21.1

Создать функцию parse_command_output. Параметры функции:
* template - имя файла, в котором находится шаблон TextFSM
  Например, templates/sh_ip_int_br.template
* command_output - вывод соответствующей команды show (строка)

Функция должна возвращать список:
* первый элемент - это список с названиями столбцов
* остальные элементы это списки, в котором находятся результаты обработки вывода

Проверить работу функции на выводе команды sh ip int br с оборудования
и шаблоне templates/sh_ip_int_br.template.

Пример вызова функции
In [5]: with open("output/sh_ip_int_br.txt") as f:
   ...:     pprint(parse_command_output("templates/sh_ip_int_br.template", f.read()))
   ...:
[['intf', 'address', 'status', 'protocol'],
 ['FastEthernet0/0', '15.0.15.1', 'up', 'up'],
 ['FastEthernet0/1', '10.0.12.1', 'up', 'up'],
 ['FastEthernet0/2', '10.0.13.1', 'up', 'up'],
 ['FastEthernet0/3', 'unassigned', 'up', 'up'],
 ['Loopback0', '10.1.1.1', 'up', 'up'],
 ['Loopback100', '100.0.0.1', 'up', 'up']]

"""
import textfsm
from netmiko import ConnectHandler
from pathlib import Path
from pprint import pprint

p = Path('exercises/21_textfsm')

def parse_command_output(template, command_output):
    """Функция обрабатывает вывод команды с помощью шаблона TextFSM
    Результат обработки представляет собой список списков

    Args:
        template (str): Имя файла шаблона TextFSM
        command_output (str): вывод команды с оборудования

    Returns:
        list: Список словарей с распарсенными данными
    """
    with open(template) as t:
        fsm = textfsm.TextFSM(t)
        headers = fsm.header
        result = fsm.ParseText(command_output)
    return [headers, *result]


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
        pprint(parse_command_output(p/"templates/sh_ip_int_br.template", f.read()))