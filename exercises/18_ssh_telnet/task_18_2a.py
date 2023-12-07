# -*- coding: utf-8 -*-
"""
Задание 18.2a

Скопировать функцию send_config_commands из задания 18.2 и добавить параметр log,
который контролирует будет ли выводится на стандартный поток вывода информация о том
к какому устройству выполняется подключение.
По умолчанию, результат должен выводиться.

Пример работы функции:

In [13]: result = send_config_commands(r1, commands)
Подключаюсь к 192.168.100.1...

In [14]: result = send_config_commands(r1, commands, log=False)

In [15]:

Скрипт должен отправлять список команд commands на все устройства
из файла devices.yaml с помощью функции send_config_commands.

Тесты в этом разделе проверяют подключение на устройствах в файле devices.yaml.
Если параметры подключения к вашим устройствам отличаются, надо изменить
параметры в файле devices.yaml.
"""
import yaml
from pathlib import Path
from netmiko import Netmiko
from paramiko.ssh_exception import SSHException
from netmiko import NetmikoBaseException

p = Path('exercises/18_ssh_telnet')
commands = ["logging 10.255.255.1", "logging buffered 20010", "no logging console"]


def send_config_commands(device, config_commands, log=True):
    try:
        if log:
            print(f'Подключаюсь к {device["host"]}...')
        with Netmiko(**device) as cssh:
            cssh.enable()
            output = cssh.send_config_set(config_commands)
            return output
    except (SSHException, NetmikoBaseException) as error:
            print(f'{error}')


if __name__ == "__main__":
    command = "sh ip int br"
    with open(p/"devices.yaml") as f:
        devices = yaml.safe_load(f)

    for dev in devices:
        print(send_config_commands(dev, commands))