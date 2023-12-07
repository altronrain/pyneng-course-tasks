# -*- coding: utf-8 -*-
"""
Задание 18.2c

Скопировать функцию send_config_commands из задания 18.2b и переделать ее таким образом:

Если при выполнении команды возникла ошибка, спросить пользователя надо ли выполнять
остальные команды.

Варианты ответа [y]/n:
* y - выполнять остальные команды. Это значение по умолчанию,
  поэтому нажатие любой комбинации воспринимается как y
* n или no - не выполнять остальные команды

Функция send_config_commands по-прежнему должна возвращать кортеж из двух словарей:
* первый словарь с выводом команд, которые выполнились без ошибки
* второй словарь с выводом команд, которые выполнились с ошибками

Оба словаря в формате
* ключ - команда
* значение - вывод с выполнением команд

Проверить работу функции можно на одном устройстве.

Пример работы функции:

In [11]: result = send_config_commands(r1, commands)
Подключаюсь к 192.168.100.1...
Команда "logging 0255.255.1" выполнилась с ошибкой "Invalid input detected at '^' marker." на устройстве 192.168.100.1
Продолжать выполнять команды? [y]/n: y
Команда "logging" выполнилась с ошибкой "Incomplete command." на устройстве 192.168.100.1
Продолжать выполнять команды? [y]/n: n

In [12]: pprint(result)
({},
 {'logging': 'config term\n'
             'Enter configuration commands, one per line.  End with CNTL/Z.\n'
             'R1(config)#logging\n'
             '% Incomplete command.\n'
             '\n'
             'R1(config)#',
  'logging 0255.255.1': 'config term\n'
                        'Enter configuration commands, one per line.  End with '
                        'CNTL/Z.\n'
                        'R1(config)#logging 0255.255.1\n'
                        '                   ^\n'
                        "% Invalid input detected at '^' marker.\n"
                        '\n'
                        'R1(config)#'})

In [12]: pprint(result, sort_dicts=False)
({},
 {'logging 0255.255.1': 'configure terminal\n'
                        'Enter configuration commands, one per line.  End with CNTL/Z.\n'
                        'R1(config)#logging 0255.255.1\n'
                        '                   ^\n'
                        "% Invalid input detected at '^' marker.\n"
                        '\n'
                        'R1(config)#',
  'logging': 'logging\n% Incomplete command.\n\nR1(config)#'})


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
                question = input('Продолжать выполнять команды? [y]/n: ')
                if question == 'n' or question == 'no':
                    return good_cmds, bad_cmds
            else:
                good_cmds.update({cmd: output})
    return good_cmds, bad_cmds



if __name__ == "__main__":
    # command = "sh ip int br"
    # with open(p/"devices.yaml") as f:
    #     devices = yaml.safe_load(f)

    # for dev in devices:
    #     pprint(send_config_commands(dev, commands))
    
    r1 = {
        'device_type': 'cisco_ios',
        'host': '192.168.139.1',
        'username': 'cisco',
        'password': 'cisco',
        'secret': 'cisco',
        'timeout': '10'
        }
    
    pprint(send_config_commands(r1, commands))