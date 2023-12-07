# -*- coding: utf-8 -*-
"""
Задание 18.2b

Скопировать функцию send_config_commands из задания 18.2a и добавить проверку на ошибки.

При выполнении каждой команды, скрипт должен проверять результат на такие ошибки:
 * Invalid input detected, Incomplete command, Ambiguous command

Если при выполнении какой-то из команд возникла ошибка, функция должна выводить
сообщение на стандартный поток вывода с информацией о том, какая ошибка возникла,
при выполнении какой команды и на каком устройстве, например:
Команда "logging" выполнилась с ошибкой "Incomplete command." на устройстве 192.168.100.1

Ошибки должны выводиться всегда, независимо от значения параметра log.
При этом, параметр log по-прежнему должен контролировать будет ли выводиться сообщение:
Подключаюсь к 192.168.100.1...


Функция send_config_commands теперь должна возвращать кортеж из двух словарей:
* первый словарь с выводом команд, которые выполнились без ошибки
* второй словарь с выводом команд, которые выполнились с ошибками

Оба словаря в формате (примеры словарей ниже):
* ключ - команда
* значение - вывод с выполнением команд

Проверить работу функции можно на одном устройстве.


Пример работы функции send_config_commands:

In [16]: commands
Out[16]:
['logging 0255.255.1',
 'logging',
 'a',
 'logging buffered 20010',
 'ip http server']

In [17]: result = send_config_commands(r1, commands)
Подключаюсь к 192.168.100.1...
Команда "logging 0255.255.1" выполнилась с ошибкой "Invalid input detected at '^' marker." на устройстве 192.168.100.1
Команда "logging" выполнилась с ошибкой "Incomplete command." на устройстве 192.168.100.1
Команда "a" выполнилась с ошибкой "Ambiguous command:  "a"" на устройстве 192.168.100.1

In [18]: pprint(result, width=100, sort_dicts=False)
({'logging buffered 20010': 'logging buffered 20010\nR1(config)#',
  'ip http server': 'ip http server\nR1(config)#'},
 {'logging 0255.255.1': 'configure terminal\n'
                        'Enter configuration commands, one per line.  End with CNTL/Z.\n'
                        'R1(config)#logging 0255.255.1\n'
                        '                   ^\n'
                        "% Invalid input detected at '^' marker.\n"
                        '\n'
                        'R1(config)#',
  'logging': 'logging\n% Incomplete command.\n\nR1(config)#',
  'a': 'a\n% Ambiguous command:  "a"\nR1(config)#'})

In [19]: good, bad = result

In [20]: good.keys()
Out[20]: dict_keys(['logging buffered 20010', 'ip http server'])

In [21]: bad.keys()
Out[21]: dict_keys(['logging 0255.255.1', 'logging', 'a'])


Примеры команд с ошибками:
R1(config)#logging 0255.255.1
                   ^
% Invalid input detected at '^' marker.

R1(config)#logging
% Incomplete command.

R1(config)#a
% Ambiguous command:  "a"

Тесты в этом разделе проверяют подключение на устройствах в файле devices.yaml.
Если параметры подключения к вашим устройствам отличаются, надо изменить
параметры в файле devices.yaml.
"""
import yaml
import re
from pathlib import Path
from netmiko import Netmiko
from pprint import pprint
from paramiko.ssh_exception import SSHException
from netmiko import NetmikoBaseException

p = Path('exercises/18_ssh_telnet')
# списки команд с ошибками и без:
commands_with_errors = ["logging 0255.255.1", "logging", "a"]
correct_commands = ["logging buffered 20010", "ip http server"]

commands = commands_with_errors + correct_commands


def send_config_commands(device, config_commands, log=True):
    good_cmds = {}
    bad_cmds = {}
    try:
        if log:
            print(f'Подключаюсь к {device["host"]}...')
        with Netmiko(**device) as cssh:
            cssh.enable()
            for cmd in config_commands:
                output = cssh.send_config_set(cmd)
                if '%' in output:
                    bad_cmds.update({cmd: output})
                    regex = r"% (.+)\n"
                    rmatch = re.search(regex, output)
                    print(f'Команда {cmd} выполнилась с ошибкой {rmatch.group(1)} на устройстве {device["host"]}')
                else:
                    good_cmds.update({cmd: output})
        return good_cmds, bad_cmds
    except (SSHException, NetmikoBaseException) as error:
            print(f'{error}')


if __name__ == "__main__":
    command = "sh ip int br"
    with open(p/"devices.yaml") as f:
        devices = yaml.safe_load(f)

    for dev in devices:
        pprint(send_config_commands(dev, commands))