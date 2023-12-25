# -*- coding: utf-8 -*-
"""
Задание 21.3

Создать функцию parse_command_dynamic.

Параметры функции:
* command_output - вывод команды (строка)
* attributes_dict - словарь атрибутов, в котором находятся такие пары ключ-значение:
 * 'Command': команда
 * 'Vendor': вендор
* index_file - имя файла, где хранится соответствие между командами и шаблонами.
  Значение по умолчанию - "index"
* templ_path - каталог, где хранятся шаблоны. Значение по умолчанию - "templates"

Функция должна возвращать список словарей с результатами обработки
вывода команды (как в задании 21.1a):
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на примере вывода команды sh ip int br и sh version.

Пример вызова функции для sh ip int br

In [8]: attributes = {"Command": "show ip int br", "Vendor": "cisco_ios"}
   ...: with open("output/sh_ip_int_br.txt") as f:
   ...:     pprint(parse_command_dynamic(f.read(), attributes), width=120)
   ...:
[{'address': '15.0.15.1', 'intf': 'FastEthernet0/0', 'protocol': 'up', 'status': 'up'},
 {'address': '10.0.12.1', 'intf': 'FastEthernet0/1', 'protocol': 'up', 'status': 'up'},
 {'address': '10.0.13.1', 'intf': 'FastEthernet0/2', 'protocol': 'up', 'status': 'up'},
 {'address': 'unassigned', 'intf': 'FastEthernet0/3', 'protocol': 'up', 'status': 'up'},
 {'address': '10.1.1.1', 'intf': 'Loopback0', 'protocol': 'up', 'status': 'up'},
 {'address': '100.0.0.1', 'intf': 'Loopback100', 'protocol': 'up', 'status': 'up'}]

Пример вызова функции для sh version

In [9]: attributes = {'Command': 'sh version', 'Vendor': 'cisco_ios'}
   ...: with open("output/sh_version.txt") as f:
   ...:     output = f.read()
   ...: print(parse_command_dynamic(output, attributes))

[{'version': '15.3(2)S1', 'hostname': 'R1_LONDON'}]

"""
from textfsm import clitable
from pathlib import Path
from pprint import pprint

p = Path('exercises/21_textfsm')

def parse_command_dynamic(
    command_output, attributes_dict,
    index_file='index', templ_path='templates'
    ):
    """Функция обрабатывает вывод команд с оборудования (из файлов).
    Сама команда и тип оборудования принимаются в качестве словаря.
    Обработка вывода осуществляется на основе шаблонов TextFSM.
    Выбор шаблонов происходит динамически согласно установленному соответствию
    (функционал clitable).

    Args:
        command_output (str): Вывод команды с оборудования
        attributes_dict (_type_): Словарь, содержащий сведения о команде и оборудовании
        index_file (str, optional): Имя файла соответствия шаблонов. Defaults to 'index'.
        templ_path (str, optional): Имя директории с файлами шаблонов. Defaults to 'templates'.

    Returns:
        list: Список словарей с распарсенным содержимым вывода команды
    """
    cli = clitable.CliTable(index_file, Path(templ_path).resolve())
    cli.ParseCmd(command_output, attributes_dict)
    headers = cli.header
    dict_output = [dict(zip(headers, list(row))) for row in cli]
    return dict_output


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
    attributes = {'Command': 'sh version', 'Vendor': 'cisco_ios'}
    with open(p/"output/sh_version.txt") as f:
        output = f.read()
    pprint(parse_command_dynamic(output, attributes))
    
    attributes = {"Command": "show ip int br", "Vendor": "cisco_ios"}
    with open(p/"output/sh_ip_int_br.txt") as f:
        pprint(parse_command_dynamic(f.read(), attributes), width=120)