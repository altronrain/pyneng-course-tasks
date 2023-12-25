# -*- coding: utf-8 -*-
"""
Задание 21.4

Создать функцию send_and_parse_show_command.

Параметры функции:
* device_dict - словарь с параметрами подключения к одному устройству
* command - команда, которую надо выполнить
* templates_path - путь к каталогу с шаблонами TextFSM
* index - имя индекс файла, значение по умолчанию "index"

Функция должна подключаться к одному устройству, отправлять команду show
с помощью netmiko, а затем парсить вывод команды с помощью TextFSM.

Функция должна возвращать список словарей с результатами обработки
вывода команды (как в задании 21.1a):
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на примере вывода команды sh ip int br
и устройствах из devices.yaml.

Пример вызова функции
In [17]: result = send_and_parse_show_command(
    ...:     devices[1], "sh ip int br", templates_path=full_pth
    ...: )
    ...: pprint(result, width=120)
    ...:
[{'address': '192.168.100.2', 'intf': 'Ethernet0/0', 'protocol': 'up', 'status': 'up'},
 {'address': '10.100.23.2', 'intf': 'Ethernet0/1', 'protocol': 'up', 'status': 'up'},
 {'address': 'unassigned', 'intf': 'Ethernet0/2', 'protocol': 'down', 'status': 'administratively down'},
 {'address': 'unassigned', 'intf': 'Ethernet0/3', 'protocol': 'down', 'status': 'administratively down'},
 {'address': '10.2.2.2', 'intf': 'Loopback0', 'protocol': 'up', 'status': 'up'},
 {'address': 'unassigned', 'intf': 'Loopback9', 'protocol': 'up', 'status': 'up'},
 {'address': 'unassigned', 'intf': 'Loopback19', 'protocol': 'up', 'status': 'up'},
 {'address': '10.100.100.2', 'intf': 'Loopback100', 'protocol': 'up', 'status': 'up'},
 {'address': '10.255.1.2', 'intf': 'Tunnel2', 'protocol': 'down', 'status': 'up'}]

"""
# import os
import yaml
from pathlib import Path
from netmiko import Netmiko
from textfsm import clitable
from pprint import pprint

p = Path('exercises/21_textfsm')

def send_and_parse_show_command(device_dict, command, templates_path, index='index'):
    """Функция подключается к оборудованию, выполняет show команду.
    Далее полученный вывод команды обрабатывается шаблонами TextFSM.
    Возвращает список словарей на основе шаблона,
    соответствующего выполненной комнде.

    Args:
        device_dict (dict): Словарь параметров подключения к оборудованию
        command (str): Команда для выполнения на оборудовании
        templates_path (str): Имя директории с файлами шаблонов
        index (str, optional): Имя файла соответствия шаблонов. Defaults to 'index'.

    Returns:
        list: Список словарей с распарсенным содержимым вывода команды
    """
    # ~Красивый вариант (по результатам tips&tricks)
    # if "NET_TEXTFSM" not in os.environ:
    #     os.environ["NET_TEXTFSM"] = p/templates_path
    # with Netmiko(**device_dict) as cssh:
    #     output = cssh.send_command(
    #         command,
    #         use_textfsm=True,
    #         )
    # return output
    with Netmiko(**device_dict) as cssh:
        output = cssh.send_command(command)
    cli = clitable.CliTable(index, p/templates_path)
    cli.ParseCmd(output, {'Command': command})
    headers = cli.header
    dict_output = [dict(zip(headers, list(row))) for row in cli]
    return dict_output        


if __name__ == "__main__":
    command = "sh ip int br"
    with open(p/"devices.yaml") as f:
        devices = yaml.safe_load(f)
    result = send_and_parse_show_command(
        devices[1], "sh ip int br", templates_path='templates'
    )
    pprint(result, width=120)
